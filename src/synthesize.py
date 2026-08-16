"""Synthetic pointing data, for smoke-testing the pipeline.

The authors released no data (see SOURCES.md), so the pipeline cannot be run on
the paper's own 8,400 postures. This generator produces data with the *shape*
the pipeline consumes and a *known* systematic offset, so that the
implementation can be exercised end to end and the recovery of a known
correction can be checked. Nothing here is a claim about what the paper's
participants did: the numbers are invented and must never be compared with the
paper's results.
"""

import numpy as np
import pandas as pd

import geometry as geo

RNG_SEED = 20180421  # CHI 2018 opening day; any seed does


def _systematic_bias(target_xy, kind):
    """A smooth, target-dependent bias field, in degrees of yaw/pitch."""
    x = target_xy[:, 0] / geo.SCREEN_W_CM
    y = target_xy[:, 1] / geo.SCREEN_H_CM
    if kind == "EFRC":
        return 1.5 - 2.0 * x + 1.0 * x ** 2, -1.0 + 1.5 * y
    if kind == "IFRC":
        return -4.0 - 3.0 * x + 2.0 * x * y, 3.0 + 2.5 * y - 1.5 * y ** 2
    if kind == "FRC":
        return -9.0 - 5.0 * x, 7.0 + 4.0 * y
    return 2.0 * x, 2.0 * y  # HRC: pulled towards the grid centre


def make_study1(n_participants=20, repetitions=6, n_samples=9,
                seed=RNG_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    targets = geo.target_grid()
    rows = []
    for p in range(1, n_participants + 1):
        eye_height = rng.normal(163.0, 9.0)
        for env in ("RealWorld", "VirtualReality"):
            env_gain = 1.0 if env == "RealWorld" else 0.85
            trial = 0
            for rep in range(repetitions):
                for t_id, tgt in enumerate(targets):
                    trial += 1
                    eye = np.array([rng.normal(0, 1.0), eye_height,
                                    rng.normal(0, 1.5)])
                    to_target = np.array([tgt[0], tgt[1], geo.SCREEN_DISTANCE_CM]) - eye
                    ideal = geo.direction_to_angles(to_target[None, :])[0]
                    by, bp = _systematic_bias(tgt[None, :], "EFRC")
                    iy, ip = _systematic_bias(tgt[None, :], "IFRC")
                    fy, fp = _systematic_bias(tgt[None, :], "FRC")
                    hy, hp = _systematic_bias(tgt[None, :], "HRC")
                    for s in range(n_samples):
                        t_ms = 50.0 + s * (900.0 / n_samples)
                        jit = rng.normal(0, 0.6, size=8)
                        fdir = geo.angles_to_direction(
                            np.array([ideal[0] + env_gain * by[0] + jit[0]]),
                            np.array([ideal[1] + env_gain * bp[0] + jit[1]]))[0]
                        finger = eye + 55.0 * fdir  # arm length along the eye-finger ray
                        ifdir = geo.angles_to_direction(
                            np.array([ideal[0] + env_gain * iy[0] + jit[2]]),
                            np.array([ideal[1] + env_gain * ip[0] + jit[3]]))[0]
                        forearm = finger - np.array([0.0, 5.0, 25.0])
                        frdir = geo.angles_to_direction(
                            np.array([ideal[0] + env_gain * fy[0] + jit[4]]),
                            np.array([ideal[1] + env_gain * fp[0] + jit[5]]))[0]
                        hdir = geo.angles_to_direction(
                            np.array([ideal[0] + env_gain * hy[0] + jit[6]]),
                            np.array([ideal[1] + env_gain * hp[0] + jit[7]]))[0]
                        rows.append({
                            "participant": p, "environment": env, "trial": trial,
                            "target_id": t_id, "target_x": tgt[0], "target_y": tgt[1],
                            "t_ms": t_ms,
                            "eye_x": eye[0], "eye_y": eye[1], "eye_z": eye[2],
                            "head_x": eye[0], "head_y": eye[1], "head_z": eye[2],
                            "head_dir_x": hdir[0], "head_dir_y": hdir[1],
                            "head_dir_z": hdir[2],
                            "finger_x": finger[0], "finger_y": finger[1],
                            "finger_z": finger[2],
                            "finger_dir_x": ifdir[0], "finger_dir_y": ifdir[1],
                            "finger_dir_z": ifdir[2],
                            "forearm_x": forearm[0], "forearm_y": forearm[1],
                            "forearm_z": forearm[2],
                            "forearm_dir_x": frdir[0], "forearm_dir_y": frdir[1],
                            "forearm_dir_z": frdir[2],
                        })
    return pd.DataFrame(rows)


def make_study2(n_participants=16, repetitions=2, seed=RNG_SEED + 1) -> pd.DataFrame:
    """Per-trial evaluation data: 6 conditions x 35 targets x 2 repetitions."""
    rng = np.random.default_rng(seed)
    targets = geo.target_grid()
    rows = []
    for p in range(1, n_participants + 1):
        skill = rng.normal(1.0, 0.15)
        for env in ("RealWorld", "VirtualWorld"):
            for cursor in (False, True):
                for correction in (False, True):
                    for rep in range(repetitions):
                        for t_id, tgt in enumerate(targets):
                            base = 6.5 if not cursor else 1.2
                            gain = 0.90 if correction else 1.0
                            sigma = base * skill * gain / 1.25
                            dx, dy = rng.normal(0, sigma, size=2)
                            tct = rng.lognormal(
                                np.log(1.75 if cursor else 1.55), 0.25)
                            rows.append({
                                "participant": p, "environment": env,
                                "cursor": cursor, "correction": correction,
                                "repetition": rep, "target_id": t_id,
                                "target_x": tgt[0], "target_y": tgt[1],
                                "hit_x": tgt[0] + dx, "hit_y": tgt[1] + dy,
                                "tct_s": tct,
                            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "data"
    import pathlib
    d = pathlib.Path(out)
    d.mkdir(parents=True, exist_ok=True)
    make_study1().to_csv(d / "synthetic_study1.csv", index=False)
    make_study2().to_csv(d / "synthetic_study2.csv", index=False)
    print(f"wrote {d/'synthetic_study1.csv'} and {d/'synthetic_study2.csv'}")
