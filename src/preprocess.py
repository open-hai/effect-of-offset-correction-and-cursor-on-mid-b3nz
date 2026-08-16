"""Preprocessing of raw pointing samples, following Preprocessing (p. 5).

Three steps are stated in the paper and all three leave something open; the
open part is named in the docstring of each function and recorded in
REPRODUCIBILITY.md ("Hidden decisions").
"""

import numpy as np
import pandas as pd

import geometry as geo

SAMPLE_WINDOW_MS = (100.0, 900.0)
OUTLIER_SD = 2.0

POSITION_TRIPLES = [
    ("eye_x", "eye_y", "eye_z"),
    ("finger_x", "finger_y", "finger_z"),
    ("forearm_x", "forearm_y", "forearm_z"),
    ("head_x", "head_y", "head_z"),
]


def window_samples(df: pd.DataFrame, window=SAMPLE_WINDOW_MS) -> pd.DataFrame:
    """Keep samples 100ms-900ms into the one-second hold.

    Paper: "we used the samples between 100ms and 900ms to counteract possible
    hand tremor and possible movements at the beginning and end of the pointing
    phase" (p. 5). Open: whether t is measured from the button press or from
    target onset -- we take it from the button press that starts the hold.
    """
    lo, hi = window
    return df[(df["t_ms"] >= lo) & (df["t_ms"] <= hi)].copy()


def aggregate_trials(df: pd.DataFrame, keys) -> pd.DataFrame:
    """Collapse the windowed samples of a trial to one posture.

    Open: the paper does not say how the samples inside the window are
    combined. We take the arithmetic mean of every tracked coordinate before
    casting the ray (mean-then-cast, not cast-then-mean).
    """
    value_cols = [c for c in df.columns if c not in keys and c != "t_ms"]
    grouped = df.groupby(list(keys), as_index=False)[value_cols].mean()
    return grouped


def align_heads(df: pd.DataFrame, group="participant") -> pd.DataFrame:
    """Translate each participant so all heads sit at the grand-mean head.

    Paper: "the participants were of different sizes so to compensate for
    different heights we aligned the heads of the participants to build one
    universal model" (p. 5). Open: whether the alignment is a translation of
    the whole body, a vertical shift only, or a re-expression of the angles in
    a head-centred frame. We translate every tracked position of a participant
    by (grand-mean head - that participant's mean head).
    """
    if not {"head_x", "head_y", "head_z"}.issubset(df.columns):
        return df
    out = df.copy()
    ref = out[["head_x", "head_y", "head_z"]].mean().to_numpy()
    per = out.groupby(group)[["head_x", "head_y", "head_z"]].transform("mean")
    shift = ref - per.to_numpy()
    for triple in POSITION_TRIPLES:
        if set(triple).issubset(out.columns):
            out[list(triple)] = out[list(triple)].to_numpy() + shift
    return out


def drop_outliers(df: pd.DataFrame, distance_col: str, by) -> pd.DataFrame:
    """Remove postures further than mean + 2 SD from the target.

    Paper: "We then filtered the mid-air pointing postures to remove outliers
    using two times the standard deviation as an upper bound" (p. 5). Open: the
    grouping. We follow the predecessor paper (Mayer et al. 2015), which
    removed outliers "for each ray casting method, condition, and target
    individually", and apply the bound one-sided on the distance.
    """
    def mask(g):
        return g <= g.mean() + OUTLIER_SD * g.std(ddof=1)

    keep = df.groupby(list(by))[distance_col].transform(mask)
    return df[keep.fillna(True)].copy()


def available_methods(df: pd.DataFrame):
    return [m for m in geo.METHODS
            if set(geo.METHOD_COLUMNS[m]).issubset(df.columns)]
