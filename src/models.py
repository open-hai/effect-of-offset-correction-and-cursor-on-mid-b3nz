"""The four offset-correction model families f1-f4 and their fitting/LOOCV.

Paper (Modeling, p. 6): f1 is "a one-dimensional second degree polynomial
function (parabola)"; f2 and f3 are "complete two-dimensional polynomial
functions", f2 of degree 1 and f3 of degree 2; f4 is the 15-parameter function
of Equation 1, which is the complete two-dimensional polynomial of degree 4.
"We used a nonlinear least-squares solver to fit out data."

Every one of these models is *linear in its parameters*, so the design-matrix
least-squares solution is the global optimum. `solver="nls"` runs
scipy.optimize.least_squares anyway, to check that the paper's stated solver
choice makes no difference (see tests in check_paper.py / analyze.py output).
"""

from itertools import product

import numpy as np
from scipy.optimize import least_squares

MODEL_NAMES = ("f1", "f2", "f3", "f4")


def design_matrix(alpha_yaw, alpha_pitch, model: str, axis: str) -> np.ndarray:
    """Columns of the polynomial basis for one correction axis.

    axis is "yaw" or "pitch"; it only matters for f1, which is one-dimensional
    and therefore uses the alpha of the axis it predicts.
    """
    p = np.asarray(alpha_pitch, float)
    y = np.asarray(alpha_yaw, float)
    one = np.ones_like(p)
    if model == "f1":
        a = y if axis == "yaw" else p
        return np.column_stack([one, a, a ** 2])
    if model == "f2":
        return np.column_stack([one, p, y])
    if model == "f3":
        return np.column_stack([one, p, y, p * p, p * y, y * y])
    if model == "f4":
        cols = [one]
        for i, j in sorted(
            (i, j) for i, j in product(range(5), repeat=2) if 0 < i + j <= 4
        ):
            cols.append((p ** i) * (y ** j))
        return np.column_stack(cols)  # 15 columns: complete bivariate quartic
    raise ValueError(f"unknown model: {model}")


def fit_axis(alpha_yaw, alpha_pitch, delta, model: str, axis: str,
             solver: str = "lstsq") -> np.ndarray:
    X = design_matrix(alpha_yaw, alpha_pitch, model, axis)
    d = np.asarray(delta, float)
    beta, *_ = np.linalg.lstsq(X, d, rcond=None)
    if solver == "nls":
        res = least_squares(lambda b: X @ b - d, x0=np.zeros(X.shape[1]))
        return res.x
    if solver != "lstsq":
        raise ValueError(f"unknown solver: {solver}")
    return beta


def predict_axis(alpha_yaw, alpha_pitch, beta, model: str, axis: str) -> np.ndarray:
    return design_matrix(alpha_yaw, alpha_pitch, model, axis) @ beta


class CorrectionModel:
    """A pair of fitted polynomials, one for delta_yaw and one for delta_pitch."""

    def __init__(self, model: str, beta_yaw, beta_pitch):
        self.model = model
        self.beta_yaw = np.asarray(beta_yaw, float)
        self.beta_pitch = np.asarray(beta_pitch, float)

    @classmethod
    def fit(cls, alpha_yaw, alpha_pitch, delta_yaw, delta_pitch,
            model: str = "f4", solver: str = "lstsq") -> "CorrectionModel":
        return cls(
            model,
            fit_axis(alpha_yaw, alpha_pitch, delta_yaw, model, "yaw", solver),
            fit_axis(alpha_yaw, alpha_pitch, delta_pitch, model, "pitch", solver),
        )

    def predict(self, alpha_yaw, alpha_pitch):
        return (
            predict_axis(alpha_yaw, alpha_pitch, self.beta_yaw, self.model, "yaw"),
            predict_axis(alpha_yaw, alpha_pitch, self.beta_pitch, self.model, "pitch"),
        )

    def as_dict(self):
        return {
            "model": self.model,
            "beta_yaw": self.beta_yaw.tolist(),
            "beta_pitch": self.beta_pitch.tolist(),
        }


def loocv_predictions(alpha_yaw, alpha_pitch, delta_yaw, delta_pitch, groups,
                      model: str = "f4", solver: str = "lstsq"):
    """Leave-one-group-out cross-validated correction predictions.

    `groups` selects the granularity the paper leaves open: pass participant
    ids for leave-one-participant-out (what Mayer et al. 2015 did), or a unique
    id per trial for leave-one-trial-out.
    """
    alpha_yaw = np.asarray(alpha_yaw, float)
    alpha_pitch = np.asarray(alpha_pitch, float)
    delta_yaw = np.asarray(delta_yaw, float)
    delta_pitch = np.asarray(delta_pitch, float)
    groups = np.asarray(groups)

    pred_yaw = np.full(len(groups), np.nan)
    pred_pitch = np.full(len(groups), np.nan)
    for g in np.unique(groups):
        test = groups == g
        train = ~test
        if train.sum() <= design_matrix(alpha_yaw[train], alpha_pitch[train],
                                        model, "yaw").shape[1]:
            continue
        fitted = CorrectionModel.fit(
            alpha_yaw[train], alpha_pitch[train],
            delta_yaw[train], delta_pitch[train], model, solver,
        )
        py, pp = fitted.predict(alpha_yaw[test], alpha_pitch[test])
        pred_yaw[test] = py
        pred_pitch[test] = pp
    return pred_yaw, pred_pitch
