"""Analysis entrypoint.

    python src/analyze.py <INPUT.csv> [--outdir results] [--model f4]
                          [--cv participant|trial] [--solver lstsq|nls]

The study is detected from the columns: a file carrying CURSOR and CORRECTION
is treated as the evaluation study (Study 2), anything else as the data
collection study (Study 1). Both write JSON and CSV into --outdir.
"""

import argparse
import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import pipeline  # noqa: E402


def detect_study(df: pd.DataFrame) -> int:
    return 2 if {"cursor", "correction"}.issubset(df.columns) else 1


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="CSV of pointing data")
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--model", default="f4", choices=["f1", "f2", "f3", "f4"])
    ap.add_argument("--cv", default="participant", choices=["participant", "trial"])
    ap.add_argument("--solver", default="lstsq", choices=["lstsq", "nls"])
    ap.add_argument("--no-align-heads", action="store_true")
    args = ap.parse_args(argv)

    df = pd.read_csv(args.input)
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    study = detect_study(df)
    stem = pathlib.Path(args.input).stem

    if study == 1:
        result, trials = pipeline.study1(df, model=args.model, cv=args.cv,
                                         solver=args.solver,
                                         align=not args.no_align_heads)
        trials.to_csv(outdir / f"{stem}_trials.csv", index=False)
        import figures
        fig_path = figures.figure4(trials, outdir / f"{stem}_figure4.png")
        print(f"Study 1 pipeline on {args.input}")
        print(f"  trials after windowing/aggregation/outlier removal: "
              f"{result['n_trials_after_filtering']}")
        print(f"  ray casts computed: {', '.join(result['methods'])}")
        print("  offset before / after correction (cm), by method x environment:")
        for r in result["table1"]:
            print(f"    {r['method']:<5} {r['environment']:<15} "
                  f"n={r['n']:>5}  {r['mean_cm']:7.2f} -> "
                  f"{r['mean_corrected_cm']:7.2f}  "
                  f"({r['correction_pct']:5.1f}%)")
        print(f"  overall correction ({args.model}, "
              f"leave-one-{args.cv}-out CV): "
              f"{result['overall_correction_pct']:.1f}%")
        print("  model family comparison (overall % correction): " +
              ", ".join(f"{k}={v:.1f}%"
                        for k, v in result["model_comparison_pct"].items()))
        print(f"  wrote {fig_path} (Figure 4 redrawn)")
    else:
        result = pipeline.study2(df)
        print(f"Study 2 pipeline on {args.input}")
        for dv in ("distance", "tct"):
            print(f"  RM-ANOVA on {dv}:")
            for e in result["anova"][dv]:
                print(f"    {e['effect']:<38} F({e['df1']:.0f},{e['df2']:.0f})="
                      f"{e['F']:8.3f}  p={e['p']:.4f}")
        print("  correction improvement:")
        for cursor, v in result["correction_improvement"].items():
            print(f"    cursor={cursor}: pooled {v['pooled_pct']:.1f}%, "
                  f"mean-of-ratios {v['mean_of_ratios_pct']:.1f}%, "
                  + ", ".join(f"{k} {x:.1f}%"
                              for k, x in v["per_environment_pct"].items()))
        print("  square target side holding 90% of pointing actions (cm):")
        for s in result["target_sizes"]:
            print(f"    env={s['environment']:<13} correction={str(s['correction']):<5} "
                  f"cursor={str(s['cursor']):<5} {s['target_side_cm_90pct']:.1f}")

    path = outdir / f"{stem}_study{study}.json"
    path.write_text(json.dumps(result, indent=2, default=_json_default))
    print(f"  wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
