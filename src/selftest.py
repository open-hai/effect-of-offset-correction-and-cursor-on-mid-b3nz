"""Self-test of the inner-loop implementation.

No participant data exists to test against (the authors released none), so this
checks the properties that *can* be checked: that the model basis is the
function printed in Equation 1, that the paper's stated solver choice is
immaterial, that the geometry round-trips, and that a known synthetic offset
field is recovered by the fitting and cross-validation code.

    python src/selftest.py
"""

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import geometry as geo  # noqa: E402
import models  # noqa: E402
import pipeline  # noqa: E402
import synthesize  # noqa: E402


def test_f4_is_equation_1():
    """Equation 1 lists 15 terms; the complete bivariate quartic has 15 terms."""
    p, y = np.array([0.7]), np.array([-1.3])
    X = models.design_matrix(y, p, "f4", "yaw")
    assert X.shape == (1, 15), X.shape
    eq1 = {
        p[0] ** 4, y[0] ** 4, p[0] ** 3 * y[0], p[0] * y[0] ** 3,
        p[0] ** 3, y[0] ** 3, p[0] ** 2 * y[0] ** 2, p[0] ** 2 * y[0],
        p[0] * y[0] ** 2, p[0] ** 2, y[0] ** 2, p[0] * y[0], p[0], y[0], 1.0,
    }
    got = set(np.round(X[0], 12))
    assert got == set(np.round(sorted(eq1), 12)), (sorted(got), sorted(eq1))
    for name, k in (("f1", 3), ("f2", 3), ("f3", 6)):
        assert models.design_matrix(y, p, name, "pitch").shape[1] == k
    print("  f4 basis == Equation 1 (15 terms, complete bivariate quartic)   ok")


def test_solvers_agree():
    """The paper says 'nonlinear least-squares'; the model is linear in x0..x14."""
    rng = np.random.default_rng(0)
    ay, ap = rng.normal(0, 8, 500), rng.normal(0, 6, 500)
    d = 0.4 * ap ** 2 - 0.2 * ay + 1.1 + rng.normal(0, 0.1, 500)
    a = models.fit_axis(ay, ap, d, "f4", "pitch", solver="lstsq")
    b = models.fit_axis(ay, ap, d, "f4", "pitch", solver="nls")
    pa = models.design_matrix(ay, ap, "f4", "pitch") @ a
    pb = models.design_matrix(ay, ap, "f4", "pitch") @ b
    err = float(np.max(np.abs(pa - pb)))
    assert err < 1e-6, err
    print(f"  lstsq vs scipy nonlinear least_squares: max |dy| = {err:.2e}   ok")


def test_geometry_roundtrip():
    rng = np.random.default_rng(1)
    yaw, pitch = rng.uniform(-40, 40, 200), rng.uniform(-30, 30, 200)
    back = geo.direction_to_angles(geo.angles_to_direction(yaw, pitch))
    assert np.allclose(back[:, 0], yaw) and np.allclose(back[:, 1], pitch)
    origin = np.tile(np.array([0.0, 160.0, 0.0]), (35, 1))
    targets = geo.target_grid()
    tgt3 = np.column_stack([targets, np.full(35, geo.SCREEN_DISTANCE_CM)])
    hit = geo.intersect_screen(geo.Ray(origin, tgt3 - origin))
    assert np.allclose(hit, targets, atol=1e-9)
    assert len(targets) == geo.GRID_COLS * geo.GRID_ROWS == 35
    print("  angle round-trip and screen intersection exact on the 7x5 grid  ok")


def test_recovers_known_offset():
    df = synthesize.make_study1(n_participants=6, repetitions=2, n_samples=5)
    result, trials = pipeline.study1(df, model="f4", cv="participant")
    per = {r["method"]: r for r in result["per_method"]}
    for method in ("EFRC", "IFRC", "FRC"):
        before, after = per[method]["mean_cm"], per[method]["mean_corrected_cm"]
        assert after < before, (method, before, after)
    assert result["overall_correction_pct"] > 20
    print("  synthetic bias field is reduced by LOOCV correction for every "
          "ray cast   ok")
    print(f"    (synthetic-only numbers: overall correction "
          f"{result['overall_correction_pct']:.1f}%, "
          f"{result['n_trials_after_filtering']} trials)")


def test_target_size():
    rng = np.random.default_rng(2)
    d = rng.normal(0, 3.0, size=(20000, 2))
    side = pipeline.target_size_90(d[:, 0], d[:, 1])
    expected = 2 * 3.0 * 1.9484  # (2*Phi(z)-1)^2 = 0.9
    assert abs(side - expected) / expected < 0.03, (side, expected)
    print(f"  90%-capture square recovers the analytic value "
          f"({side:.2f} vs {expected:.2f} cm)   ok")


if __name__ == "__main__":
    print("inner-loop self-test")
    test_f4_is_equation_1()
    test_solvers_agree()
    test_geometry_roundtrip()
    test_target_size()
    test_recovers_known_offset()
    print("all self-tests passed")
