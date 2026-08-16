#!/usr/bin/env bash
# Runs everything this repository can run, and records the console output.
# Synthetic data is written outside the repository, to /tmp, on purpose.
set -euo pipefail
cd "$(dirname "$0")"

DATA=${DATA:-/tmp/repro-data}
OUT=${OUT:-results}
mkdir -p "$DATA" "$OUT"

python src/selftest.py
python src/synthesize.py "$DATA"
python src/analyze.py "$DATA/synthetic_study1.csv" --outdir "$OUT"
python src/analyze.py "$DATA/synthetic_study2.csv" --outdir "$OUT"
# check_paper.py exits non-zero when the paper disagrees with itself, which is
# a finding rather than a build failure here.
python src/check_paper.py --outdir "$OUT" || true

# the per-trial dump is large and derived; keep it out of the repository
mv -f "$OUT"/synthetic_study1_trials.csv "$DATA"/ 2>/dev/null || true
