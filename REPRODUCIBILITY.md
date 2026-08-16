# Reproducibility audit

**Paper.** Sven Mayer, Valentin Schwind, Robin Schweigert, Niels Henze. *The
Effect of Offset Correction and Cursor on Mid-Air Pointing in Real and Virtual
Environments.* CHI '18. DOI [10.1145/3173574.3174227](https://doi.org/10.1145/3173574.3174227).
Audited 2026-08-16. Page numbers refer to the 13-page author PDF (see `SOURCES.md`).

**Verdict: partial.** The paper's inner loop is a geometry-plus-polynomial
pipeline (four ray casts → offsets → a 15-parameter quartic fitted per angle →
LOOCV) followed by two RM-ANOVAs. Every step of it is re-implementable from the
prose, and this repository implements and runs all of it — but the authors
released no pointing data and, crucially, **not one of the ~240 fitted
coefficients that constitute the paper's headline contribution**. So the
pipeline can be run, and the paper's own arithmetic can be checked exhaustively
against its tables, but no number in Tables 1–3 can be recomputed from source.
Of 59 checks run against the paper: **all 35 derivations its own tables can
support come out consistent**, 4 more are not derivable from anything published,
and **6 of the 20 reported F/p pairs fail recomputation** — including an effect
the paper calls significant, `ENVIRONMENT` on accuracy, reported as
*F*(1,15) = 1.3, *p* = .027, where *F*(1,15) = 1.3 gives *p* = .272.

---

## 1. Per-component reproduction table

Inner-loop components only. Each row is a thing the paper does that a machine
could in principle re-do. *Verified* = I re-derived it and it holds; *partial* =
implemented and exercised, but the paper's own numbers cannot be recovered;
*blocked* = cannot be done at all, with the blocker named. `→` marks the command
that produced the evidence.

| # | Inner-loop component | Citation | Outcome | Evidence / blocker |
|---|---|---|---|---|
| I1 | Four ray casts (EFRC, IFRC, FRC, HRC) and their intersection with the projection screen | Apparatus, p. 4 | **partial** | Implemented in `src/geometry.py`; exact on the 7×5 grid and angle round-trip (`→ python src/selftest.py`). Cannot be checked against the paper: the marker→anatomy transforms (cyclops eye from HMD markers, "true finger tip" from marker plus a per-user measurement, forearm centre "approximating the forearm with a frustum of a cone") are prose only, and no marker data was released |
| I2 | Preprocessing: 100–900 ms sample window, offset definition, 2 SD outlier bound, head alignment | Preprocessing, p. 5 | **partial** | Implemented in `src/preprocess.py` and run end-to-end (`→ ./run_all.sh`, 32,111 synthetic trials survive). Three of the four steps are under-specified (see decisions D1–D4) and the paper never reports how many trials the filter removed, so no count can be matched |
| I3 | Per-method average offsets over the two environments (9.33 / 28.09 / 65.0 / 42.46 cm) | Accuracy of Ray Casts, p. 5, from Table 1 | **verified** | Recomputed from Table 1 to ±0.005 cm for all four methods (`→ python src/check_paper.py`, ids `s1-mean-*`) |
| I4 | The model family f1–f4, i.e. Equation 1 | Modeling, p. 6, Eq. 1 | **verified** | The 15 terms of Eq. 1 are exactly the complete bivariate quartic; the basis is reconstructed term-by-term and asserted in `src/selftest.py`. The paper's "nonlinear least-squares solver" is immaterial — the model is linear in x₀…x₁₄ and both solvers agree to 6.5 × 10⁻¹⁰ |
| I5 | The fitted correction models themselves (8 models × 15 coefficients × 2 angles) | Modeling, p. 6 | **blocked** | Never published, in the paper or anywhere (`SOURCES.md`, 22 locations). The paper's stated contribution therefore cannot be applied by a reader. For contrast, the predecessor paper printed its coefficients: re-implemented here in `src/mayer2015_model.py` |
| I6 | LOOCV correction percentages: 55.9 % FRC, 50.1 % IFRC, 10.9 % EFRC, 0.2 % HRC, 29.3 % overall; remaining offsets 8.2 / 14.0 / 28.6 / 42.3 cm | Modeling, p. 6, from Table 1 | **verified** | All nine numbers reproduce from Table 1 (`→ python src/check_paper.py`, ids `s1-correction-*`, `s1-remaining-*`, `s1-correction-overall`): the per-method figure is the mean of the two per-environment percentages and the overall figure is the mean of those four. Aggregation order and CV granularity are unstated (D5, D6). Rounding is truncation, not rounding, throughout |
| I7 | Four one-way RM-ANOVAs, RealWorld vs VirtualReality per ray cast | Accuracy of Ray Casts, p. 5 | **blocked** | No data: the 8,400 postures were never released. All five reported *F*/*p* pairs in Study 1 (including the fatigue check) are internally consistent, so nothing here contradicts itself |
| I8 | Fatigue check: raw-TLX means per session and their one-way RM-ANOVAs | p. 5 and p. 8 | **partial** | Study 1's *F*(3,57) = .047, *p* = .986 is consistent and its df match 20 participants × 4 sessions. Study 2's is not: *F*(5,15) = .654 is reported where 16 participants × 6 sessions implies *F*(5,75), and even taking (5,15) at face value gives *p* = .663, not the reported .659 |
| I9 | Study 2 condition tables — TCT (Table 2) and remaining offset (Table 3) — and the 6-conditions-for-8-cells design | Study Design p. 7, Tables 2–3 | **verified** | The design's fingerprint is visible in the paper's own numbers: with no cursor the participant cannot see whether correction is on, and Table 2's no-cursor TCT is byte-identical across CORRECTION in both environments (1.48/1.48 and 1.64/1.64), exactly as the collapse of 8 cells into 6 requires (`→ check ids s2-tct-nocursor-identical-*`) |
| I10 | Correction improvements: 13.1 % overall without cursor, 16.3 % RW, 9.5 % VR, 4.5 % with cursor | Discussion p. 9, Conclusion, from Table 3 | **verified** | All four reproduce from Table 3 (`→ check ids s2-improve-*`). The two aggregate figures only come out at 13.1 % and 4.5 % if the cell means are pooled first; averaging the two per-environment percentages instead gives 12.98 % and 4.31 % (D14) |
| I11 | Two three-way RM-ANOVAs (accuracy, TCT) over CORRECTION × CURSOR × ENVIRONMENT | Results, p. 8 | **partial** | The analysis is re-implemented (`src/pipeline.py:study2`, statsmodels `AnovaRM`) and runs on study-2-shaped data, reproducing the F(1,15) structure the paper's df imply. The paper's own values cannot be recomputed (no data), and 5 of the 14 *F*/*p* pairs it reports fail recomputation — see the mismatch box below |
| I12 | Square target sizes holding 90 % of pointing actions: 17.6 / 18.8 / 4.1 / 4.5 cm, and the per-condition shrinks 6.9 / 11.6 / 6.5 / 8.9 % | Accuracy, p. 8 | **blocked** | Not derivable from anything published: it needs the per-trial 2-D endpoints, and Table 3 gives only the mean and SD of the *scalar* distance. The estimator is implemented and validated against its analytic value (`src/pipeline.py:target_size_90`, `→ selftest`, 11.69 cm vs 11.69 cm). Forcing an isotropic-Rayleigh assumption onto Table 3 — my assumption, not the paper's — gives 22.0 cm where the paper says 17.6 cm |
| I13 | Average 8.5 % shrink of the target under correction | Future Work, p. 9 | **verified** | Mean of the paper's own four shrink percentages = 8.475 % (`→ check id s2-target-shrink-mean`) |
| I14 | Cross-paper comparison with Mayer et al. 2015: errors "4.8, 1.9, 3.7 times larger", IFRC 89.2 % larger than EFRC after correction, and 2015's EFRC 4.9 % larger than IFRC | Model Discussion, p. 6 | **verified** | All five numbers reproduce against the predecessor's Tables 1–2, row *standing 2 m* (`→ check ids s1-ratio-2015-*`, `s1-ifrc-vs-efrc`, `s1-2015-efrc-vs-ifrc`). The recomputation also settles an ambiguity the paper creates: the word "overall" in that sentence can only mean the RealWorld column, not both environments (see mismatch box) |
| I15 | Design and sample arithmetic: 7 × 5 = 35 targets, 35 × 6 × 2 = 420 trials, × 20 participants = 8,400 postures, 420 / 4 = 105 per session, 6 × 35 × 2 = 420 in Study 2, grid spacing = screen / (n − 1) | Study Design pp. 3–4 and 7, Apparatus p. 4, Results p. 5 | **verified** | Every count closes exactly (`→ check ids design-*`), including the spacing: 269.4 / 6 = 44.9 cm and 136.2 / 4 = 34.05 cm, which recovers the digit the PDF's text layer drops in "34.cm" |

**Counts: 8 verified, 4 partial, 3 blocked, 15 inner-loop components.**

> *Derived rate, not a headline.* 8/15 verified and 12/15 at least partially
> reproduced. That number is a summary of **this** decomposition and nothing
> else. Slice the pipeline differently — treat "the model" as one component
> instead of the four rows I1, I4, I5, I6 — and the same audit yields a
> different fraction from the same findings. It is not comparable to another
> paper's rate, or to another run's rate on this paper. The table above is the
> comparable artifact.

### Mismatches found

A mismatch is recorded wherever my observation disagrees with the paper, on
verified rows as well as failing ones.

| Row | Kind | Paper reports | I observe | Delta |
|---|---|---|---|---|
| I11 | **contradiction** | "a significant effect of … ENVIRONMENT, *F*(1,15) = 1.3, *p* = .027 on the participants' pointing accuracy" (p. 8), repeated as a finding in the Discussion | *F*(1,15) = 1.3 gives *p* = .272. Either the *F* or the *p* is wrong; on the printed *F*, the effect is not significant | p: +.245; flips the significance decision |
| I11 | numeric | accuracy, CORRECTION: *p* = .027 | *F*(1,15) = 5.321 gives *p* = .036 | +.009 (still significant) |
| I11 | numeric | accuracy, CORRECTION × ENVIRONMENT: *p* = .36 | *F*(1,15) = .983 gives *p* = .337 | −.023 |
| I11 | numeric | TCT, ENVIRONMENT: *p* = .956 | *F*(1,15) = .004 gives *p* = .950; the whole printed-precision interval of *F* is [.947, .953] | −.006 |
| I11 | numeric | TCT, CURSOR × ENVIRONMENT: *p* < .001 | *F*(1,15) = 15.61 gives *p* = .00128, which is not < .001 | bound violated by 2.8 × 10⁻⁴ |
| I8 | contradiction | Study 2 fatigue: *F*(5,15) = .654, *p* = .659 | 16 participants over 6 sessions gives error df = 75, not 15 (Study 1 uses the analogous *F*(3,57) correctly); and *F*(5,15) = .654 gives *p* = .663 | df: −60; p: +.004 |
| I14 | numeric | "**Overall** Mayer et al. reported errors before correction 4.8 times larger for EFRC" | 4.76 if "overall" is the RealWorld column alone; 5.21 if it is the average over both environments, which is what "overall" means everywhere else in the paper | +0.41 under the other reading |
| I6 | typo | EFRC correction "10.9 %", HRC remaining "42.3 cm" | 10.96 % and 42.385 cm — the paper truncates instead of rounding, here and in ~6 other derived figures | ≤ 0.09 |
| I6 | ordering | "We achieved the best correction with FRC … then HRC with .2 %" — all four described as corrections | For HRC in VirtualReality the fitted model makes accuracy *worse*: 37.77 → 37.81 cm, i.e. −0.11 % | sign |

None of the arithmetic mismatches touch the paper's conclusions. The `ENVIRONMENT`
one does: it is one of the three main effects on the paper's primary dependent
variable.

---

## 2. The inner/outer boundary

**Inner loop — the 15 rows above.** Everything downstream of "a file of tracked
postures exists": ray-cast geometry, offset computation, filtering, the
polynomial fits, cross-validation, the descriptive tables, the ANOVAs, the
target-size estimates, and every percentage derived from them. All of it is
mechanically re-runnable, and all of it is implemented in `src/`.

**Outer loop — never attempted, never simulated.** Seven components, each
requiring humans:

| Outer-loop component | Citation | Why it is outer |
|---|---|---|
| O1. Data-collection study: 20 participants × 420 mid-air pointing gestures in RW and VR | Study Design–Participants, pp. 3–5 | The measurement *is* where a human chooses to point when asked to point naturally. Nothing computable substitutes for it |
| O2. Evaluation study: 16 new participants, 2 × 2 × 2 selection task | Evaluation, pp. 7–8 | Same, plus the effects of interest (cursor, correction) are defined only relative to human behaviour |
| O3. Raw NASA-TLX after every session, in both studies | pp. 5, 8 | Subjective workload; only a participant can report it |
| O4. Eye-dominance screening with the Miles and Porta tests | Participants, pp. 5, 8 | A physical perceptual test on a person |
| O5. Fourteen per-participant anthropometric measurements and the fitted avatar/bone structure | Apparatus, p. 4 | An experimenter measuring a body with a tape and a laser tool |
| O6. Informed consent and demographic questionnaire | Procedure, pp. 5, 8 | Human research procedure |
| O7. Recruitment and eligibility: university volunteer pool, right-handed only, no locomotor coordination problems | Participants, pp. 5, 8 | Sampling humans |

The boundary here is unusually clean, and worth stating precisely: the paper's
*contribution* is inner-loop (a model), but its *evidence* is entirely
outer-loop (where 36 people pointed). A component is outer here only when it
needs a person — not when it merely needs the lab. The OptiTrack rig, the Vive
and the projector are apparatus, and apparatus is an obstacle to *collecting*
data, not a reason to call the analysis unreproducible: the analysis is I1–I15,
and it is blocked by the absent file, not by the absent hardware.

---

## 3. Hidden decisions

Choices a reimplementation must make and the paper never states. "Assumed" is
what `src/` does; "sensitivity" is what changes if you choose otherwise.

| # | Question | Where the paper leaves it open | What I assumed | Sensitivity |
|---|---|---|---|---|
| D1 | How are the samples inside the 100–900 ms window combined into one posture? | "we used the samples between 100ms and 900ms" (p. 5) — a window, with no aggregator | Arithmetic mean of every tracked coordinate, then cast the ray (mean-then-cast) | Moderate. Cast-then-mean differs from mean-then-cast by second-order terms in the tremor amplitude; with 8–12 Hz tremor (the paper's own p. 2 literature) over 800 ms the difference is small for EFRC but grows with the lever arm, i.e. worst for IFRC/FRC where a 1° direction error is ~3.5 cm on screen |
| D2 | Is the window measured from the button press or from target onset? | The click "when they started to hold a gesture" and the target disappearing "after one second" (p. 5) both define plausible zeros | From the button press | Moderate: an offset of the window into the movement phase, not the hold phase, would inflate all offsets |
| D3 | Over which grouping is the "two times the standard deviation" outlier bound computed, and is it one- or two-sided? | "using two times the standard deviation as an upper bound" (p. 5), no grouping given | Per ray cast × environment × target, one-sided upper bound, following the predecessor paper's explicit rule | Moderate. Global vs per-target filtering changes both the retained N and the mean offset; the paper reports neither the N nor the removal count, so this is unfalsifiable from the text |
| D4 | What does "we aligned the heads of the participants" do? | p. 5 | Translate every tracked position of a participant by (grand-mean head − that participant's mean head) | High for the model fit: it defines the shared frame the universal polynomial lives in. A vertical-only shift, a full rigid alignment, or a per-trial re-centring all give different α distributions |
| D5 | Is the LOOCV leave-one-participant-out or leave-one-trial-out? | "we used leave-one-out cross-validation (LOOCV)" (p. 6) | Leave-one-participant-out, following the predecessor paper's explicit description | **High.** Leave-one-trial-out leaks each participant's own bias into the training set and inflates the apparent correction; the paper's claim is about a *user-independent* model, which only leave-one-participant-out supports |
| D6 | In what order are percentages aggregated — per environment then per method, or pooled? | The paper prints one number per method (p. 6) | Mean of the two per-environment percentages, then mean over methods | Low but not zero: this is the reading that reproduces 29.3 % exactly; pooling the cell means first gives 29.5 % |
| D7 | What reference frame defines α_pitch and α_yaw? | "the vertical deviation angle and … the horizontal deviation angle each between the ray cast and the body" (p. 6) — "the body" is not defined | World axes with +z the screen normal, origin at the ray root | High. A shoulder- or head-anchored frame rotates the α domain, so the fitted polynomial is not transferable between conventions — and since the coefficients were never published, a reader cannot detect the mismatch |
| D8 | Which of f1–f4, fitted on what, is applied in Study 2? | "the Unity scene was adjusted to support our model" (p. 7) | f4, per environment, for EFRC, fitted on all 20 Study-1 participants | Moderate: f4 on all data is the strongest form of the model, so this is the assumption most favourable to the paper |
| D9 | Was Study 2's correction the LOOCV model or the all-data fit? | Not stated | All-data fit | Moderate: the Study-2 participants are new, so either is user-independent for them, but the all-data fit is strictly better trained |
| D10 | What instant of a Study-2 trial is the recorded endpoint? | TCT is "the time between the appearance of the target and the selection by the participants, as confirmed by a button" (p. 7); the accuracy endpoint is not tied to an instant | The intersection at the moment of the click | High for the with-cursor conditions, where a participant is actively nulling error: an averaged hold window would report a smaller offset than an instantaneous sample |
| D11 | How is the cursor rendered — size, update rate, smoothing? | "a green crosshair as suggested by Olsen and Nielsen" (p. 7) | Not implemented (no rendering in this repository) | High for the paper's own result: cursor gain and smoothing directly set the with-cursor offsets (1.1–1.3 cm) and the TCT increase that the abstract claims |
| D12 | Do the ANOVAs run on per-participant cell means, and was the skew of a distance measure addressed? | Results, p. 8 | Per-participant cell means (the reported error df of 15 with 16 participants implies it); no transform, matching the paper's silence | Low for df, moderate for p: Euclidean distances are right-skewed and bounded at 0, so an untransformed ANOVA is anti-conservative |
| D13 | How is raw TLX scored — 0–100 or 0–20, which subscales? | "a raw NASA-Task Load Index (raw TLX)" (pp. 5, 8) | Unweighted mean of the six standard subscales on 0–100, consistent with the reported means of 35–40 | Low: the fatigue conclusion is a null result either way |
| D14 | Is the "improvement" a pooled ratio or a mean of ratios? | "the models overall improvement without a cursor was 13.1%" (p. 9) | Pooled cell means first, then the ratio — the only reading that yields 13.1 % and 4.5 % | Low in magnitude (13.16 % vs 12.98 %), but it is the difference between reproducing the paper's number and not |
| D15 | How is the 90 %-capture square defined — centred on the target or on the mean endpoint, radial or per-axis, empirical or parametric? | "we will estimate target sizes to fit at least 90% … For simplicity we only fit a squared target shape" (p. 8) | Centred on the target, per-axis, empirical 90th percentile of max(|dx|,|dy|) | **High.** Centring on the mean endpoint instead removes the residual bias and shrinks every reported size; this alone can move 17.6 cm by several cm, and it is the parameter a designer would actually use |
| D16 | How were target order and condition order randomised, and with what seed? | "The order of the targets was randomized while the order of ENVIRONMENT was counter-balanced" (p. 4); in Study 2 "CORRECTION and CURSOR were randomized within ENVIRONMENT" (p. 7) | Uniform random target order per condition; no seed recoverable | Low for the means, moderate for order effects: randomising rather than counterbalancing CORRECTION × CURSOR leaves learning effects confounded with condition in a 6-condition, one-hour session |
| D17 | How are participants with "unclear" eye dominance (4 of 20, 5 of 16) treated in the cyclops-eye definition? | Participants, pp. 5, 8 — screening is reported, its use is not | Treated identically; the cyclops eye is the midpoint regardless | Low for the midpoint construction, but it makes the eye-dominance screening decorative: it is measured and then never enters any model |
| D18 | How many trials survived filtering? | Never reported; only "8,400 mid-air pointing postures" collected (p. 5) | Unknown; my synthetic run keeps ~95 % | Unfalsifiable: without the retained N, none of Table 1's SDs can be checked and no effect size can be recomputed |
| D19 | What exactly is the vertical target spacing? | Printed as "34.cm" (p. 4) — a digit is lost in the PDF | 34.05 cm, recovered as 136.2 / 4 | None: the reconstruction is exact |
| D20 | Which solver, and does it matter? | "We used a nonlinear least-squares solver to fit out data" (p. 6) for a model that is linear in its parameters | Both: `--solver lstsq` and `--solver nls` | **None, and this is a positive finding**: verified identical to 6.5 × 10⁻¹⁰ (`selftest`). The paper's odd solver choice is harmless |

---

## 4. Open-science scorecard

| Criterion | Found | Where |
|---|---|---|
| **Code** | ❌ No | Searched: paper footnotes and full text; the ACM DL page (HTTP 403, not inspectable); the first author's publication page (which links only PDF, video, DOI); the last author's data page; the GitHub org `interactionlab` (all 22 repositories); GitHub users `sven-mayer` (21) and `valentin-schwind` (28); GitHub code search. No analysis code, no Unity project, no fitted coefficients |
| **Data** | ❌ No | Searched: Zenodo, OSF, figshare, DaRUS (the authors' own institutional repository), arXiv ancillary files, Semantic Scholar, both author pages, all three GitHub accounts. Neither the 8,400 postures of Study 1 nor the 6,720 trials of Study 2 exist publicly |
| **License** | ❌ No | Nothing to license: no data or code was released. The paper itself is under the standard ACM notice, "© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM" (p. 1). The one auxiliary repository that exists, the marker mounts, *is* MIT-licensed — verified at <https://github.com/interactionlab/htc-vive-marker-mount> |
| **Preregistration** | ❌ No | No preregistration statement, hypothesis registration or ethics-approval statement anywhere in the paper; nothing on OSF under these authors. (CHI 2018 had no such norm — this is context, not an excuse for the reader who needs it) |
| **Supplement** | ✅ Partial | Two artifacts, both alive and both fetched successfully: the 3D models of the custom OptiTrack marker mounts, <https://github.com/interactionlab/htc-vive-marker-mount> (footnote 1, p. 4), and the androgynous virtual hand models, <https://github.com/valentin-schwind/selfpresence> (footnote 2, p. 5). Neither is study material. A CHI video figure is linked from the authors' page but could not be verified from here (HTTP 429) |

Full search log, with what each location returned: `SOURCES.md`.

---

## 5. How to re-run this audit

```
pip install -r requirements.txt
./run_all.sh            # self-test, synthetic data, both pipelines, paper checks
```

`results/run_log.txt` is the recorded output of exactly that command.
`src/check_paper.py` needs nothing but the paper's own tables and is the part
that produces the findings above; it exits non-zero while the paper disagrees
with itself.
