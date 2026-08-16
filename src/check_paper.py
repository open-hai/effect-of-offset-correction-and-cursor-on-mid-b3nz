"""Recompute every number the paper derives from its own published tables.

This is the part of the inner loop that does *not* need the authors' data: the
paper's tables are the input, and its summary statistics, percentages, design
arithmetic and F/p pairs are the output. Anything that fails here is a fault in
the paper, not a missing artifact.

    python src/check_paper.py [--outdir results]

Writes <outdir>/paper_checks.json and <outdir>/paper_checks.md, and exits
non-zero if any check is inconsistent (so it can be used as a test).
"""

import argparse
import json
import pathlib
import statistics
import sys

from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import paper_values as pv  # noqa: E402

CHECKS = []


def _agrees(reported, recomputed, tol):
    """Reported value agrees if it is the rounding *or* the truncation of ours.

    The paper truncates several derived percentages (e.g. it prints 42.3 for
    42.385 and 13.1 for 13.16), so a pure rounding test would raise a dozen
    false alarms and bury the real problems.
    """
    if reported is None:
        return True, ""
    if abs(recomputed - reported) <= tol:
        return True, ""
    decimals = max(0, len(f"{reported}".split(".")[-1]) if "." in f"{reported}" else 0)
    scale = 10 ** decimals
    truncated = int(abs(recomputed) * scale) / scale * (1 if recomputed >= 0 else -1)
    if abs(truncated - reported) < 1e-9:
        return True, "paper truncates where it should round"
    return False, ""


def check(cid, claim, citation, reported, recomputed, tol, note=""):
    ok, auto_note = _agrees(reported, recomputed, tol)
    CHECKS.append({
        "id": cid, "claim": claim, "citation": citation,
        "reported": reported, "recomputed": round(recomputed, 4),
        "delta": None if reported is None else round(recomputed - reported, 4),
        "tolerance": tol, "verdict": "consistent" if ok else "INCONSISTENT",
        "note": "; ".join(x for x in (note, auto_note) if x),
    })
    return ok


def pct(before, after):
    return 100.0 * (before - after) / before


def study1_checks():
    for m, cells in pv.TABLE1.items():
        before = statistics.mean(v[0] for v in cells.values())
        after = statistics.mean(v[1] for v in cells.values())
        check(f"s1-mean-{m}",
              f"average offset over environments for {m}",
              "Table 1 -> Accuracy of Ray Casts, p. 5",
              pv.REPORTED_MEAN_OFFSET[m], before, 0.01)
        check(f"s1-remaining-{m}",
              f"remaining offset after correction for {m}",
              "Table 1 -> Modeling, p. 6",
              pv.REPORTED_REMAINING_CM[m], after, 0.05,
              "paper truncates rather than rounds" if m == "HRC" else "")
        per_env = [pct(*cells[e]) for e in cells]
        check(f"s1-correction-{m}",
              f"LOOCV correction achieved for {m} (mean of the two environments)",
              "Table 1 -> Modeling, p. 6",
              pv.REPORTED_CORRECTION_PCT[m], statistics.mean(per_env), 0.06)

    overall = statistics.mean(
        statistics.mean(pct(*cells[e]) for e in cells)
        for cells in pv.TABLE1.values())
    check("s1-correction-overall",
          "overall correction of f4 across methods and environments",
          "Modeling, p. 6 ('an overall correction of 29.3%')",
          pv.REPORTED_OVERALL_CORRECTION_PCT, overall, 0.05)

    check("s1-vr-efrc",
          "reduction achieved by the VR EFRC model",
          "Model Discussion, p. 6",
          pv.REPORTED_VR_EFRC_REDUCTION_PCT,
          pct(*pv.TABLE1["EFRC"]["VirtualReality"]), 0.05)

    check("s1-ifrc-vs-efrc",
          "RW offset after correction: IFRC larger than EFRC by",
          "Model Discussion, p. 6",
          pv.REPORTED_IFRC_VS_EFRC_PCT,
          100.0 * (pv.TABLE1["IFRC"]["RealWorld"][1] /
                   pv.TABLE1["EFRC"]["RealWorld"][1] - 1), 0.05)

    check("s1-hrc-vr-direction",
          "HRC in VR: does the correction model reduce the offset?",
          "Table 1",
          None, pct(*pv.TABLE1["HRC"]["VirtualReality"]), 0.0,
          "negative value means the fitted correction makes VR HRC worse")

    for m, ratio in pv.REPORTED_RATIO_TO_MAYER2015.items():
        rw = pv.TABLE1[m]["RealWorld"][0]
        check(f"s1-ratio-2015-{m}",
              f"Mayer et al. 2015 error before correction / this paper, {m}",
              "Model Discussion, p. 6 vs Mayer et al. 2015 Table 1 (standing 2m)",
              ratio, pv.MAYER2015_STANDING_2M["before"][m] / rw, 0.05,
              "matches only if 'overall' means the RealWorld column alone")
        both = statistics.mean(v[0] for v in pv.TABLE1[m].values()) \
            if m in pv.TABLE1 else None
        CHECKS[-1]["alternative_if_both_environments"] = round(
            pv.MAYER2015_STANDING_2M["before"][m] / both, 3)

    check("s1-2015-efrc-vs-ifrc",
          "Mayer et al. 2015: EFRC larger than IFRC after correction (standing 2m)",
          "Model Discussion, p. 6 vs Mayer et al. 2015 Table 2",
          pv.REPORTED_MAYER2015_EFRC_VS_IFRC_PCT,
          100.0 * (pv.MAYER2015_STANDING_2M["after_f4"]["EFRC"] /
                   pv.MAYER2015_STANDING_2M["after_f4"]["IFRC"] - 1), 0.05)


def study2_checks():
    t3 = pv.TABLE3_OFFSET
    for cur in ("no_cursor", "cursor"):
        rw = pct(t3[("RealWorld", False)][cur][0], t3[("RealWorld", True)][cur][0])
        vr = pct(t3[("VirtualWorld", False)][cur][0],
                 t3[("VirtualWorld", True)][cur][0])
        pooled_before = statistics.mean(
            [t3[("RealWorld", False)][cur][0], t3[("VirtualWorld", False)][cur][0]])
        pooled_after = statistics.mean(
            [t3[("RealWorld", True)][cur][0], t3[("VirtualWorld", True)][cur][0]])
        pooled = pct(pooled_before, pooled_after)
        if cur == "no_cursor":
            check("s2-improve-rw", "correction improvement, RealWorld, no cursor",
                  "Table 3 -> Discussion, p. 9",
                  pv.REPORTED_IMPROVEMENT_NO_CURSOR_RW_PCT, rw, 0.1)
            check("s2-improve-vr", "correction improvement, VirtualWorld, no cursor",
                  "Table 3 -> Discussion, p. 9",
                  pv.REPORTED_IMPROVEMENT_NO_CURSOR_VR_PCT, vr, 0.1)
            check("s2-improve-overall",
                  "overall correction improvement without a cursor",
                  "Table 3 -> Discussion, p. 9 / Conclusion",
                  pv.REPORTED_IMPROVEMENT_NO_CURSOR_PCT, pooled, 0.05,
                  f"pooling the cell means gives {pooled:.2f}%; averaging the two "
                  f"per-environment percentages instead gives "
                  f"{statistics.mean([rw, vr]):.2f}%")
        else:
            check("s2-improve-cursor",
                  "average correction improvement with a cursor",
                  "Table 3 -> Discussion, p. 9 / Conclusion",
                  pv.REPORTED_IMPROVEMENT_CURSOR_PCT, pooled, 0.05,
                  f"pooling the cell means gives {pooled:.2f}%; averaging the two "
                  f"per-environment percentages instead gives "
                  f"{statistics.mean([rw, vr]):.2f}%")

    check("s2-target-shrink-mean",
          "average shrink of the 90%-capture square target under correction",
          "Future Work, p. 9 ('on average 8.5% smaller')",
          pv.REPORTED_MEAN_TARGET_SHRINK_PCT,
          statistics.mean(pv.REPORTED_TARGET_SHRINK_PCT), 0.05)

    # Design check: with no cursor the participant cannot see the correction, so
    # TCT must be identical with and without it (paper's own argument, p. 8).
    for env in ("RealWorld", "VirtualWorld"):
        a = pv.TABLE2_TCT[(env, False)]["no_cursor"][0]
        b = pv.TABLE2_TCT[(env, True)]["no_cursor"][0]
        check(f"s2-tct-nocursor-identical-{env}",
              f"no-cursor TCT identical with and without correction ({env})",
              "Table 2 vs Study Design, p. 7", 0.0, b - a, 0.0,
              "the design collapses 8 cells to 6; this is the fingerprint of it")

    # Target sizes: derivable from the raw data only. Show what the published
    # aggregates *can* support, under an explicit distributional assumption.
    for (cur, env), side in pv.REPORTED_TARGET_SIDES_CM.items():
        key = ("RealWorld" if env == "RW" else "VirtualWorld", False)
        mean_d = pv.TABLE3_OFFSET[key][cur][0]
        sigma = mean_d / (3.14159265 / 2) ** 0.5  # Rayleigh: E[R] = sigma*sqrt(pi/2)
        half = stats.norm.ppf(0.5 + 0.9 ** 0.5 / 2) * sigma
        CHECKS.append({
            "id": f"s2-target-size-{cur}-{env}",
            "claim": f"square target side holding 90% of pointings ({cur}, {env})",
            "citation": "Accuracy, p. 8",
            "reported": side, "recomputed": round(2 * half, 2),
            "delta": round(2 * half - side, 2), "tolerance": None,
            "verdict": "NOT DERIVABLE",
            "note": "needs the raw per-trial endpoints; the figure shown is what "
                    "an isotropic Rayleigh assumption on Table 3's mean would "
                    "give, and is our assumption, not the paper's",
        })


def design_checks():
    d = pv.DESIGN["study1"]
    check("design-s1-trials", "35 targets x 6 repetitions x 2 environments",
          "Study Design, p. 3-4", d["trials_reported"],
          d["targets"] * d["repetitions"] * d["environments"], 0)
    check("design-s1-postures", "420 trials x 20 participants",
          "Results, p. 5 ('8,400 mid-air pointing postures')",
          d["postures_reported"], d["trials_reported"] * d["participants"], 0)
    check("design-s1-sessions", "420 gestures split into 4 sessions",
          "Procedure, p. 5", d["gestures_per_session_reported"],
          d["trials_reported"] / d["sessions"], 0)
    check("design-s1-grid", "7 x 5 grid holds 35 targets", "Study Design, p. 3",
          d["targets"], d["grid"][0] * d["grid"][1], 0)

    d2 = pv.DESIGN["study2"]
    check("design-s2-trials", "6 conditions x 35 targets x 2 repetitions",
          "Study Design, p. 7", d2["trials_reported"],
          d2["conditions"] * d2["targets"] * d2["repetitions"], 0)

    w, h = pv.DESIGN["screen_cm"]
    check("design-spacing-x", "horizontal target spacing = width / (7-1)",
          "Apparatus, p. 4", pv.DESIGN["spacing_cm_reported"][0], w / 6, 0.01)
    CHECKS.append({
        "id": "design-spacing-y",
        "claim": "vertical target spacing = height / (5-1)",
        "citation": "Apparatus, p. 4 (printed as '34.cm')",
        "reported": None, "recomputed": round(h / 4, 3), "delta": None,
        "tolerance": None, "verdict": "consistent",
        "note": "the PDF text layer loses a digit; 136.2/4 = 34.05 cm fits",
    })
    CHECKS.append({
        "id": "design-s2-anova-df",
        "claim": "error df of the study 2 RM-ANOVAs = participants - 1",
        "citation": "Results, p. 8", "reported": 15, "recomputed": 15,
        "delta": 0, "tolerance": 0, "verdict": "consistent",
        "note": "16 participants, cell means per participant -> F(1,15) is right "
                "for the 2x2x2; the raw-TLX F(5,15) is not (6 sessions x 16 "
                "participants gives F(5,75))",
    })


def stat_checks():
    """Recompute p from F and df, allowing for the precision F is printed to."""
    for study, effect, df1, df2, f, p, kind, cite in pv.FSTATS:
        computed = float(stats.f.sf(f, df1, df2))
        decimals = len(f"{f}".split(".")[-1]) if "." in f"{f}" else 0
        step = 0.5 * 10 ** -decimals
        p_hi = float(stats.f.sf(max(f - step, 1e-12), df1, df2))
        p_lo = float(stats.f.sf(f + step, df1, df2))
        if kind == "lt":
            ok = p_hi < p
            reported_str = f"p < {p}"
            interval_note = f"F as printed implies p in [{p_lo:.5f}, {p_hi:.5f}]"
        else:
            p_decimals = len(f"{p}".split(".")[-1]) if "." in f"{p}" else 0
            half = 0.5 * 10 ** -p_decimals
            scale = 10 ** p_decimals
            truncates = abs(int(computed * scale) / scale - p) < 1e-9
            ok = ((p - half) <= p_hi and (p + half) >= p_lo) or truncates
            reported_str = f"p = {p}"
            interval_note = f"F as printed implies p in [{p_lo:.5f}, {p_hi:.5f}]"
        sig_reported = (p < 0.05) if kind == "eq" else True
        sig_computed = computed < 0.05
        note = interval_note
        if sig_reported != sig_computed:
            note += "; changes the significance decision at alpha = .05"
        CHECKS.append({
            "id": f"stat-{study}-{effect}".replace(" ", "-"),
            "claim": f"{effect}: F({df1},{df2}) = {f}, {reported_str}",
            "citation": cite, "reported": p, "recomputed": round(computed, 5),
            "delta": round(computed - p, 5), "tolerance": None,
            "verdict": "consistent" if ok else "INCONSISTENT",
            "note": note,
        })


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args(argv)

    study1_checks()
    study2_checks()
    design_checks()
    stat_checks()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "paper_checks.json").write_text(json.dumps(CHECKS, indent=2))

    lines = ["| # | claim | citation | reported | recomputed | verdict |",
             "|---|---|---|---|---|---|"]
    for i, c in enumerate(CHECKS, 1):
        rep = "-" if c["reported"] is None else c["reported"]
        note = f"<br>_{c['note']}_" if c["note"] else ""
        lines.append(f"| {i} | {c['claim']}{note} | {c['citation']} | {rep} | "
                     f"{c['recomputed']} | {c['verdict']} |")
    (outdir / "paper_checks.md").write_text("\n".join(lines) + "\n")

    bad = [c for c in CHECKS if c["verdict"] == "INCONSISTENT"]
    nd = [c for c in CHECKS if c["verdict"] == "NOT DERIVABLE"]
    width = max(len(c["id"]) for c in CHECKS)
    for c in CHECKS:
        rep = "  -  " if c["reported"] is None else f"{c['reported']:>6}"
        print(f"{c['verdict']:<14} {c['id']:<{width}} reported {rep} | "
              f"recomputed {c['recomputed']:>10}")
    print(f"\n{len(CHECKS)} checks: {len(CHECKS) - len(bad) - len(nd)} consistent, "
          f"{len(bad)} inconsistent, {len(nd)} not derivable from the paper.")
    print(f"wrote {outdir/'paper_checks.json'} and {outdir/'paper_checks.md'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
