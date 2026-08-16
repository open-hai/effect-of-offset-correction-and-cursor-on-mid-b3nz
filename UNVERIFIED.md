# Unverified

Everything this audit could not confirm, with the specific reason. Nothing on
this list should be read as a criticism that the paper is wrong — only that I
could not check it.

## Blocked by the missing data

The 8,400 postures of Study 1 and the 6,720 trials of Study 2 were never
released (`SOURCES.md`, 22 searches). Consequently:

| Claim | Citation | Blocker |
|---|---|---|
| Every cell of Table 1 — the eight before/after mean offsets and their SDs | Table 1 | No postures. The *relations between* the cells reproduce; the cells themselves cannot be recomputed |
| The four Study-1 RM-ANOVAs, EFRC/IFRC/FRC/HRC across environments | p. 5 | No postures. All four reported *F*/*p* pairs are internally consistent, which is the most that can be said |
| Both Study-2 three-way RM-ANOVAs | p. 8 | No trials. Five of the fourteen reported *F*/*p* pairs are internally inconsistent (see `REPRODUCIBILITY.md`), but whether the *F* values themselves are right is unknowable |
| Tables 2 and 3 (TCT and remaining offset per condition) | Tables 2–3 | No trials |
| The estimated 90 %-capture target sizes, 17.6 / 18.8 / 4.1 / 4.5 cm | p. 8 | Needs the per-trial 2-D endpoint distribution; Table 3 publishes only the mean and SD of the scalar distance. My Rayleigh-assumption estimate (22.0 cm where the paper says 17.6 cm) is a diagnostic of that gap, **not** a claim that the paper is wrong |
| The per-condition target shrinks 6.9 / 11.6 / 6.5 / 8.9 % | p. 8 | Same. Only their mean, 8.5 %, is checkable |
| The number of trials removed by the 2 SD filter | Never reported | Not published. Without it, Table 1's SDs and any effect size cannot be validated |
| Figure 4 and Figure 6 as data | Figures 4, 6 | Only rendered as images; no underlying values published. `src/figures.py` redraws Figure 4's *form* from a pipeline run, not its content |
| That the fitted models generalise as claimed | Modeling, p. 6 | The coefficients do not exist publicly, so the model cannot be applied, tested, or ported |

## Blocked by publisher access

| What | Blocker |
|---|---|
| The ACM Digital Library landing page, including any supplementary-material tab, artifact badge or auxiliary file | `dl.acm.org` returns HTTP 403 to every non-browser client from this environment, and the DOI resolver is not fetchable either. No supplementary artifact is referenced by the paper, by the authors' own publication page, or by the Semantic Scholar record, so the balance of evidence is that there is none — but I could not look at the page itself and do not claim to have |
| The direct supplement download endpoint | HTTP 403 |
| The ResearchGate copy's file list | HTTP 403 |
| The CHI video figure (`youtube.com/watch?v=Mu_8iJer2BM`) | HTTP 429 from this environment. It is linked from the first author's own publication page, which I did fetch (HTTP 200) |
| Whether the paper carries an ACM artifact badge | Same 403. CHI 2018 predates the ACM badging of CHI papers, so I would expect none |

## Under-specified in the paper (implemented on an assumption)

Each of these is implemented in `src/` under an explicit assumption, and each
assumption is recorded with its sensitivity in `REPRODUCIBILITY.md` §3. They are
listed again here because an assumption is not a verification:

- how samples within the 100–900 ms window become one posture (D1) and where
  that window starts (D2);
- the grouping and sidedness of the 2 SD outlier bound (D3);
- what "aligned the heads of the participants" does (D4);
- whether LOOCV is leave-one-participant-out or leave-one-trial-out (D5) —
  the single most consequential unstated choice, because the model's claim is
  user-independence;
- the reference frame for α_pitch and α_yaw (D7);
- which model, fitted on what, Study 2 applied in real time (D8, D9);
- what instant of a Study-2 trial defines the recorded endpoint (D10);
- the cursor's size, update rate and smoothing (D11) — not implemented here at
  all, since this repository renders nothing;
- how the 90 %-capture square is centred and estimated (D15).

## Claims about the outer loop, out of scope by construction

Not attempted, not simulated, not scored: the 20-participant data collection,
the 16-participant evaluation, the raw-TLX workload measures, the Miles/Porta
eye-dominance screening, the 14 anthropometric measurements per participant,
consent and demographics, and recruitment. The paper's substantive human
findings — that people point differently in VR, that a cursor trades time for
accuracy, that correction helps when no cursor is shown — rest on those, and
this audit takes no position on any of them.

## One thing I checked and could not settle

The paper says the errors of Mayer et al. 2015 are "**overall** … 4.8 times
larger for EFRC, 1.9 for IFRC and 3.7 for FRC than the errors of the presented
study" (p. 6). Those three ratios reproduce exactly (4.76, 1.90, 3.69) **only**
if "overall" means the RealWorld column of Table 1 compared against the 2015
paper's *standing, 2 m* row. Read as the average over both environments — which
is what "overall" means everywhere else in the paper — the ratios are 5.21,
1.97 and 3.43. I cannot tell which the authors meant; the arithmetic says the
first, the wording says the second.
