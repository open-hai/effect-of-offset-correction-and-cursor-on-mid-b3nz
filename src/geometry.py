"""Ray-cast geometry for mid-air pointing (Mayer et al., CHI 2018).

The paper defines four ray casts (Apparatus, p. 4) and measures the offset as
"the distance between the position where the ray cast intersects with the
projection screen and the position of the target" (Preprocessing, p. 5).

Coordinate convention used here (our choice; the paper states none):
    +x  to the participant's right, along the screen width
    +y  up, along the screen height
    +z  from the participant towards the screen (screen normal)
The screen is the plane z = SCREEN_DISTANCE.
"""

from dataclasses import dataclass

import numpy as np

# Screen and target grid as stated in the paper (Apparatus, p. 4).
SCREEN_W_CM = 269.4
SCREEN_H_CM = 136.2
SCREEN_DISTANCE_CM = 200.0
GRID_COLS = 7
GRID_ROWS = 5
SPACING_X_CM = 44.9
SPACING_Y_CM = 34.05  # paper prints "34.cm"; 136.2 / (5 - 1) = 34.05

METHODS = ("EFRC", "IFRC", "FRC", "HRC")

# Columns each ray cast consumes, beyond the shared trial columns.
METHOD_COLUMNS = {
    "EFRC": ["eye_x", "eye_y", "eye_z", "finger_x", "finger_y", "finger_z"],
    "IFRC": [
        "finger_x", "finger_y", "finger_z",
        "finger_dir_x", "finger_dir_y", "finger_dir_z",
    ],
    "FRC": [
        "forearm_x", "forearm_y", "forearm_z",
        "forearm_dir_x", "forearm_dir_y", "forearm_dir_z",
    ],
    "HRC": [
        "eye_x", "eye_y", "eye_z",
        "head_dir_x", "head_dir_y", "head_dir_z",
    ],
}


@dataclass(frozen=True)
class Ray:
    origin: np.ndarray  # (n, 3)
    direction: np.ndarray  # (n, 3), not necessarily normalised


def target_grid() -> np.ndarray:
    """The 35 targets in a 7x5 grid, centred on the screen, in cm.

    Paper: "The 35 presented targets were arranged in a 7x5 (column x row)
    grid ... The spacing of the target grid was 44.9cm x 34.cm" (p. 4).
    """
    xs = (np.arange(GRID_COLS) - (GRID_COLS - 1) / 2) * SPACING_X_CM
    ys = (np.arange(GRID_ROWS) - (GRID_ROWS - 1) / 2) * SPACING_Y_CM
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    return np.column_stack([gx.ravel(), gy.ravel()])


def build_ray(df, method: str) -> Ray:
    """Construct one of the four ray casts from a per-trial frame."""
    if method == "EFRC":
        origin = df[["eye_x", "eye_y", "eye_z"]].to_numpy(float)
        tip = df[["finger_x", "finger_y", "finger_z"]].to_numpy(float)
        return Ray(origin, tip - origin)
    if method == "IFRC":
        origin = df[["finger_x", "finger_y", "finger_z"]].to_numpy(float)
        direction = df[["finger_dir_x", "finger_dir_y", "finger_dir_z"]].to_numpy(float)
        return Ray(origin, direction)
    if method == "FRC":
        origin = df[["forearm_x", "forearm_y", "forearm_z"]].to_numpy(float)
        direction = df[["forearm_dir_x", "forearm_dir_y", "forearm_dir_z"]].to_numpy(float)
        return Ray(origin, direction)
    if method == "HRC":
        origin = df[["eye_x", "eye_y", "eye_z"]].to_numpy(float)
        direction = df[["head_dir_x", "head_dir_y", "head_dir_z"]].to_numpy(float)
        return Ray(origin, direction)
    raise ValueError(f"unknown ray cast method: {method}")


def intersect_screen(ray: Ray, screen_z: float = SCREEN_DISTANCE_CM) -> np.ndarray:
    """Intersection of each ray with the plane z = screen_z, as (n, 2) in cm.

    Rays pointing away from the screen produce NaN.
    """
    o, d = ray.origin, ray.direction
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (screen_z - o[:, 2]) / d[:, 2]
    t = np.where(t > 0, t, np.nan)
    hit = o + t[:, None] * d
    return hit[:, :2]


def direction_to_angles(direction: np.ndarray) -> np.ndarray:
    """(yaw, pitch) of a direction vector in degrees, relative to +z.

    yaw   = rotation about the vertical axis (horizontal deviation)
    pitch = elevation above the horizontal plane (vertical deviation)
    """
    d = np.asarray(direction, float)
    yaw = np.degrees(np.arctan2(d[:, 0], d[:, 2]))
    pitch = np.degrees(np.arctan2(d[:, 1], np.hypot(d[:, 0], d[:, 2])))
    return np.column_stack([yaw, pitch])


def angles_to_direction(yaw_deg: np.ndarray, pitch_deg: np.ndarray) -> np.ndarray:
    yaw = np.radians(yaw_deg)
    pitch = np.radians(pitch_deg)
    cp = np.cos(pitch)
    return np.column_stack([np.sin(yaw) * cp, np.sin(pitch), np.cos(yaw) * cp])


def ray_angles(ray: Ray) -> np.ndarray:
    """alpha_yaw, alpha_pitch of the cast ray (degrees)."""
    return direction_to_angles(ray.direction)


def target_angles(ray: Ray, target_xy: np.ndarray,
                  screen_z: float = SCREEN_DISTANCE_CM) -> np.ndarray:
    """Angles of the ideal ray from the same origin to the target (degrees)."""
    tgt = np.column_stack([target_xy, np.full(len(target_xy), screen_z)])
    return direction_to_angles(tgt - ray.origin)


def apply_correction(ray: Ray, delta_yaw: np.ndarray, delta_pitch: np.ndarray,
                     screen_z: float = SCREEN_DISTANCE_CM) -> np.ndarray:
    """Rotate each ray by the predicted correction angles and re-intersect."""
    a = ray_angles(ray)
    corrected = angles_to_direction(a[:, 0] + delta_yaw, a[:, 1] + delta_pitch)
    return intersect_screen(Ray(ray.origin, corrected), screen_z)


def offset_distance(hit_xy: np.ndarray, target_xy: np.ndarray) -> np.ndarray:
    """Euclidean distance on the screen plane, in cm."""
    return np.linalg.norm(hit_xy - target_xy, axis=1)
