"""The two analysis pipelines: Study 1 (modelling) and Study 2 (evaluation)."""

import numpy as np
import pandas as pd

import geometry as geo
import preprocess as pre
from models import MODEL_NAMES, CorrectionModel, loocv_predictions

TRIAL_KEYS = ("participant", "environment", "trial")


def _percent(before: float, after: float) -> float:
    return 100.0 * (before - after) / before


def target_size_90(dx: np.ndarray, dy: np.ndarray, coverage: float = 0.90) -> float:
    """Side of the smallest square, centred on the target, holding `coverage`.

    Paper (p. 8): "we will estimate target sizes to fit at least 90% of the
    mid-air pointing actions for all conditions independently. For simplicity
    we only fit a squared target shape." Open: whether the square is centred on
    the target or on the mean intersection; we centre it on the target, which
    is what a designer sizing a target can act on.
    """
    half = np.maximum(np.abs(dx), np.abs(dy))
    return float(2.0 * np.quantile(half, coverage))


def study1(df: pd.DataFrame, model: str = "f4", cv: str = "participant",
           solver: str = "lstsq", align: bool = True) -> dict:
    """Data-collection study: ray-cast accuracy, model fitting, LOOCV.

    Reproduces the *procedure* behind Table 1 and the Modeling section.
    """
    samples = pre.window_samples(df)
    trials = pre.aggregate_trials(samples, TRIAL_KEYS)
    if align:
        trials = pre.align_heads(trials)

    methods = pre.available_methods(trials)
    rows, per_trial = [], []
    for method in methods:
        ray = geo.build_ray(trials, method)
        hit = geo.intersect_screen(ray)
        target = trials[["target_x", "target_y"]].to_numpy(float)
        alpha = geo.ray_angles(ray)
        ideal = geo.target_angles(ray, target)
        frame = trials[list(TRIAL_KEYS)].copy()
        frame["method"] = method
        frame["hit_x"], frame["hit_y"] = hit[:, 0], hit[:, 1]
        frame[["origin_x", "origin_y", "origin_z"]] = ray.origin
        frame["target_x"], frame["target_y"] = target[:, 0], target[:, 1]
        frame["target_id"] = trials.get("target_id", pd.Series(index=trials.index,
                                                              dtype="object"))
        frame["distance"] = geo.offset_distance(hit, target)
        frame["alpha_yaw"], frame["alpha_pitch"] = alpha[:, 0], alpha[:, 1]
        frame["delta_yaw"] = ideal[:, 0] - alpha[:, 0]
        frame["delta_pitch"] = ideal[:, 1] - alpha[:, 1]
        per_trial.append(frame.dropna(subset=["distance"]))

    data = pd.concat(per_trial, ignore_index=True)
    data = pre.drop_outliers(data, "distance",
                             by=["method", "environment", "target_id"])

    fitted_models = {}
    for (method, env), g in data.groupby(["method", "environment"]):
        idx = g.index
        # LOOCV, as in the paper: "For a first evaluation of the models, we
        # used leave-one-out cross-validation (LOOCV)."
        groups = g["participant"] if cv == "participant" else np.arange(len(g))
        py, pp = loocv_predictions(g["alpha_yaw"], g["alpha_pitch"],
                                   g["delta_yaw"], g["delta_pitch"], groups,
                                   model=model, solver=solver)
        ray = geo.Ray(
            origin=g[["origin_x", "origin_y", "origin_z"]].to_numpy(float),
            direction=geo.angles_to_direction(g["alpha_yaw"].to_numpy(),
                                              g["alpha_pitch"].to_numpy()),
        )
        corrected_hit = geo.apply_correction(ray, py, pp)
        data.loc[idx, "hit_corrected_x"] = corrected_hit[:, 0]
        data.loc[idx, "hit_corrected_y"] = corrected_hit[:, 1]
        data.loc[idx, "distance_corrected"] = geo.offset_distance(
            corrected_hit, g[["target_x", "target_y"]].to_numpy(float))
        full = CorrectionModel.fit(g["alpha_yaw"], g["alpha_pitch"],
                                   g["delta_yaw"], g["delta_pitch"],
                                   model=model, solver=solver)
        fitted_models[f"{method}/{env}"] = full.as_dict()

        for alt in MODEL_NAMES:
            if alt == model:
                continue
            ay, ap = loocv_predictions(g["alpha_yaw"], g["alpha_pitch"],
                                       g["delta_yaw"], g["delta_pitch"], groups,
                                       model=alt, solver=solver)
            alt_hit = geo.apply_correction(ray, ay, ap)
            data.loc[idx, f"distance_{alt}"] = geo.offset_distance(
                alt_hit, g[["target_x", "target_y"]].to_numpy(float))

    table1 = (data.groupby(["method", "environment"])
                  .agg(n=("distance", "size"),
                       mean_cm=("distance", "mean"), sd_cm=("distance", "std"),
                       mean_corrected_cm=("distance_corrected", "mean"),
                       sd_corrected_cm=("distance_corrected", "std"))
                  .reset_index())
    table1["correction_pct"] = _percent(table1["mean_cm"],
                                        table1["mean_corrected_cm"])

    per_method = (table1.groupby("method")
                        .agg(mean_cm=("mean_cm", "mean"),
                             mean_corrected_cm=("mean_corrected_cm", "mean"),
                             correction_pct=("correction_pct", "mean"))
                        .reset_index())

    model_comparison = {}
    for alt in MODEL_NAMES:
        col = "distance_corrected" if alt == model else f"distance_{alt}"
        if col not in data:
            continue
        cells = (data.groupby(["method", "environment"])
                     .apply(lambda g: _percent(g["distance"].mean(), g[col].mean()),
                            include_groups=False)
                     .rename("pct").reset_index())
        # same aggregation as the paper: mean over environments, then methods
        model_comparison[alt] = float(
            cells.groupby("method")["pct"].mean().mean())

    return {
        "n_trials_after_filtering": int(len(data)),
        "methods": pre.available_methods(trials),
        "table1": table1.to_dict("records"),
        "per_method": per_method.to_dict("records"),
        "overall_correction_pct": float(per_method["correction_pct"].mean()),
        "model_comparison_pct": model_comparison,
        "fitted_models": fitted_models,
        "settings": {"model": model, "cv": cv, "solver": solver,
                     "align_heads": align},
    }, data


def study2(df: pd.DataFrame) -> dict:
    """Evaluation study: remaining offset and TCT over CORRECTION x CURSOR x ENVIRONMENT.

    Reproduces the *procedure* behind Tables 2 and 3 and the two three-way
    RM-ANOVAs (Results, p. 8).
    """
    from statsmodels.stats.anova import AnovaRM

    data = df.copy()
    if "distance" not in data.columns:
        hit = data[["hit_x", "hit_y"]].to_numpy(float)
        target = data[["target_x", "target_y"]].to_numpy(float)
        data["distance"] = geo.offset_distance(hit, target)

    factors = ["environment", "correction", "cursor"]
    cell = (data.groupby(["participant"] + factors, as_index=False)
                .agg(distance=("distance", "mean"), tct=("tct_s", "mean")))

    out = {"cells": cell.to_dict("records"), "anova": {}, "tables": {}}
    for dv in ("distance", "tct"):
        res = AnovaRM(cell, depvar=dv, subject="participant",
                      within=factors).fit()
        tbl = res.anova_table.reset_index().rename(columns={"index": "effect"})
        out["anova"][dv] = [
            {"effect": r["effect"], "F": float(r["F Value"]),
             "df1": float(r["Num DF"]), "df2": float(r["Den DF"]),
             "p": float(r["Pr > F"])}
            for _, r in tbl.iterrows()
        ]
        summary = (cell.groupby(factors)[dv].agg(["mean", "std"]).reset_index())
        out["tables"][dv] = summary.to_dict("records")

    sizes = []
    for keys, g in data.groupby(factors):
        dx = g["hit_x"].to_numpy(float) - g["target_x"].to_numpy(float)
        dy = g["hit_y"].to_numpy(float) - g["target_y"].to_numpy(float)
        sizes.append(dict(zip(factors, keys)) |
                     {"target_side_cm_90pct": target_size_90(dx, dy)})
    out["target_sizes"] = sizes

    def cond(env, corr, cur, dv="distance"):
        m = cell[(cell.environment == env) & (cell.correction == corr) &
                 (cell.cursor == cur)][dv]
        return float(m.mean())

    envs = sorted(cell["environment"].unique())
    improvements = {}
    for cur in sorted(cell["cursor"].unique()):
        per_env = {e: _percent(cond(e, False, cur), cond(e, True, cur))
                   for e in envs}
        pooled_before = np.mean([cond(e, False, cur) for e in envs])
        pooled_after = np.mean([cond(e, True, cur) for e in envs])
        improvements[str(cur)] = {
            "per_environment_pct": per_env,
            "mean_of_ratios_pct": float(np.mean(list(per_env.values()))),
            "pooled_pct": float(_percent(pooled_before, pooled_after)),
        }
    out["correction_improvement"] = improvements
    return out
