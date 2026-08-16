# Reproduction repository — Mayer et al., CHI 2018, mid-air pointing offset correction

> Sven Mayer, Valentin Schwind, Robin Schweigert, Niels Henze. **The Effect of
> Offset Correction and Cursor on Mid-Air Pointing in Real and Virtual
> Environments.** CHI '18. DOI [10.1145/3173574.3174227](https://doi.org/10.1145/3173574.3174227).

## What the paper does

People point badly at distant things, and they point badly in a *systematic*
way — the ray you cast from their eye through their fingertip lands somewhere
predictable that is not the target. The paper measures that displacement and
tries to cancel it.

**Study 1 (20 participants).** Each person points six times at each of 35
targets on a 7 × 5 grid on a 269 × 136 cm projection screen from 2 m away, once
in the real room and once in a VR replica of the same room worn on an HTC Vive,
with an OptiTrack rig tracking seven rigid bodies on their body. That is 8,400
recorded postures. From each posture the authors compute four ray casts —
eye-finger (EFRC), index finger (IFRC), forearm (FRC) and head (HRC) — and the
distance from where each ray hits the screen to the target. They then fit a
15-parameter quartic polynomial that maps the ray's pitch and yaw to a
correction angle, separately per ray cast and per environment, and evaluate it
by leave-one-out cross-validation. EFRC is the most accurate ray cast
(9.33 cm); the correction cuts the mean error by 29.3 % overall.

**Study 2 (16 new participants).** A 2 × 2 × 2 within-subjects selection task —
correction on/off × cursor on/off × real/virtual — validating the model in real
time. Correction improves accuracy by 13.1 % when no cursor is shown; a cursor
improves accuracy far more but costs selection time.

## What this repository is

An independent reproducibility audit. It asks three questions and answers them
in files, not in prose alone:

- **`REPRODUCIBILITY.md`** — the verdict, and first of all the per-component
  reproduction table: 15 inner-loop components, each marked verified / partial /
  blocked with its evidence or its specific blocker. Then the inner/outer
  boundary, 20 hidden decisions, and the open-science scorecard.
- **`SOURCES.md`** — the paper's identity and all 22 places I searched for
  artifacts, with what each one actually returned.
- **`UNVERIFIED.md`** — everything I could not confirm, each with its blocker.
- **`verdict.json`**, **`instrument.json`** — the same findings, and the study
  protocol and analysis contract, as machine-readable data.
- **`src/`** — a runnable implementation of the paper's inner loop.
- **`results/`** — the output of actually running it, including
  `results/run_log.txt`.

**Headline finding.** The paper's contribution is a model, and the model was
never published: not the data, not the code, and not one of the ~240 fitted
coefficients. Its two footnote artifacts (3D-printed marker mounts, virtual hand
meshes) are both alive after eight years, but neither is the study. What *can*
be checked — every number the paper derives from its own tables — holds up: 35
of 35. What does not hold up is the statistics reporting in Study 2, where 6 of
the 20 reported *F*/*p* pairs fail recomputation, one of them turning a
"significant effect of ENVIRONMENT on pointing accuracy" (*F*(1,15) = 1.3,
*p* = .027) into a non-significant one (*p* = .272).

## What is in `src/`

| File | Role |
|---|---|
| `geometry.py` | The four ray casts, the screen plane, the 7 × 5 target grid, angle conversions |
| `models.py` | f1–f4 of Equation 1, fitting (both solvers), leave-one-group-out CV |
| `preprocess.py` | Sample window, trial aggregation, head alignment, 2 SD outlier bound |
| `pipeline.py` | Study 1 pipeline (Table 1 + LOOCV) and Study 2 pipeline (RM-ANOVAs, Tables 2–3, target sizes) |
| `analyze.py` | The entrypoint: `python src/analyze.py <data.csv>`, study detected from the columns |
| `check_paper.py` | 59 checks of the paper against itself — needs no data at all |
| `paper_values.py` | Every number taken from the paper, each with its citation |
| `mayer2015_model.py` | The predecessor paper's *published* correction coefficients, re-implemented — what the missing artifact should have looked like |
| `synthesize.py` | Synthetic data with a known offset field, so the pipeline can be exercised |
| `selftest.py` | Property checks: Equation 1's basis, solver equivalence, geometry, recovery of a known bias |
| `figures.py` | Figure 4 redrawn from a pipeline run |

## Run it

```bash
pip install -r requirements.txt
./run_all.sh
```

That runs the self-test, generates synthetic data in `/tmp`, runs both
pipelines, and runs the paper checks. Roughly 30 seconds. To check the paper
without generating anything:

```bash
python src/check_paper.py --outdir results
```

To run the analysis on a real dataset — the point of the exercise, should the
data ever appear:

```bash
python src/analyze.py path/to/pointing.csv --outdir results \
       --model f4 --cv participant
```

The columns it consumes are listed in `instrument.json` under
`analysis.input.columns`.

## Two warnings

1. **The synthetic data is not the paper's data.** Its offset field is invented
   by `src/synthesize.py` so that the code has something to run on. No number
   produced from it may be compared with the paper. Every claim about the paper
   in this repository comes either from its own printed tables or from a check
   you can re-run.
2. **Nothing here reproduces the human studies.** 36 people pointing at walls is
   the paper's evidence and it is out of scope by construction — not simulated,
   not approximated, not scored. See the outer-loop table in
   `REPRODUCIBILITY.md` and `servability` in `instrument.json`.
