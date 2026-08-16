"""Every number this audit takes from the paper, with its citation.

Source: Sven Mayer, Valentin Schwind, Robin Schweigert, Niels Henze. "The
Effect of Offset Correction and Cursor on Mid-Air Pointing in Real and Virtual
Environments." CHI 2018. DOI 10.1145/3173574.3174227. Page numbers refer to the
authors' PDF (nhenze.net copy, 13 pages).

Nothing in this file is invented: each entry carries the table, figure or
section it was read from. Values printed with a dropped digit by the PDF text
layer are marked in the comment.
"""

# ---------------------------------------------------------------- Study 1 ----

# Table 1, "Overall offsets between interact and target. Distance are reported
# in cm." Rows: before correction / after LOOCV correction, by environment.
TABLE1 = {
    "EFRC": {"RealWorld": (10.21, 8.02), "VirtualReality": (8.45, 8.41)},
    "IFRC": {"RealWorld": (29.14, 15.17), "VirtualReality": (27.03, 12.90)},
    "FRC": {"RealWorld": (60.34, 27.01), "VirtualReality": (69.66, 30.18)},
    "HRC": {"RealWorld": (47.15, 46.96), "VirtualReality": (37.77, 37.81)},
}
TABLE1_SD = {
    "EFRC": {"RealWorld": (5.56, 4.54), "VirtualReality": (4.54, 4.56)},
    "IFRC": {"RealWorld": (19.24, 9.15), "VirtualReality": (18.95, 7.94)},
    "FRC": {"RealWorld": (20.16, 12.36), "VirtualReality": (25.42, 13.83)},
    "HRC": {"RealWorld": (23.71, 23.71), "VirtualReality": (19.19, 19.26)},
}

# "Accuracy of Ray Casts" (p. 5): average offset per method over environments.
REPORTED_MEAN_OFFSET = {"EFRC": 9.33, "IFRC": 28.09, "FRC": 65.0, "HRC": 42.46}

# "Modeling" (p. 6): LOOCV correction achieved per method, and overall.
REPORTED_CORRECTION_PCT = {"FRC": 55.9, "IFRC": 50.1, "EFRC": 10.9, "HRC": 0.2}
REPORTED_OVERALL_CORRECTION_PCT = 29.3
REPORTED_REMAINING_CM = {"EFRC": 8.2, "IFRC": 14.0, "FRC": 28.6, "HRC": 42.3}
# "Model Discussion" (p. 6): "we only achieved a reduction of .5% for the VR
# EFRC model" -- printed as ".5%", read as 0.5%.
REPORTED_VR_EFRC_REDUCTION_PCT = 0.5
# "Model Discussion" (p. 6): after correction in RW, IFRC vs EFRC.
REPORTED_IFRC_VS_EFRC_PCT = 89.2

# ---------------------------------------------------------------- Study 2 ----

# Table 2, "Overall TCT to select a the target. TCTs are reported in seconds."
TABLE2_TCT = {
    ("RealWorld", False): {"no_cursor": (1.48, 0.43), "cursor": (1.83, 0.43)},
    ("RealWorld", True): {"no_cursor": (1.48, 0.43), "cursor": (1.89, 0.73)},
    ("VirtualWorld", False): {"no_cursor": (1.64, 0.61), "cursor": (1.76, 0.56)},
    ("VirtualWorld", True): {"no_cursor": (1.64, 0.61), "cursor": (1.67, 0.45)},
}

# Table 3, "Remaining offset interact and target. Distances are reported in cm."
TABLE3_OFFSET = {
    ("RealWorld", False): {"no_cursor": (7.08, 3.26), "cursor": (1.14, 0.89)},
    ("RealWorld", True): {"no_cursor": (5.92, 3.29), "cursor": (1.13, 0.96)},
    ("VirtualWorld", False): {"no_cursor": (6.37, 3.42), "cursor": (1.30, 0.85)},
    ("VirtualWorld", True): {"no_cursor": (5.76, 3.26), "cursor": (1.20, 0.76)},
}

# Discussion (p. 9) and Conclusion (p. 9).
REPORTED_IMPROVEMENT_NO_CURSOR_PCT = 13.1
REPORTED_IMPROVEMENT_NO_CURSOR_VR_PCT = 9.5
REPORTED_IMPROVEMENT_NO_CURSOR_RW_PCT = 16.3
REPORTED_IMPROVEMENT_CURSOR_PCT = 4.5

# Accuracy (p. 8): estimated square target sides holding 90% of pointing
# actions, and the shrink each correction model buys.
REPORTED_TARGET_SIDES_CM = {
    ("no_cursor", "RW"): 17.6, ("no_cursor", "VR"): 18.8,
    ("cursor", "RW"): 4.1, ("cursor", "VR"): 4.5,
}
REPORTED_TARGET_SHRINK_PCT = [6.9, 11.6, 6.5, 8.9]
REPORTED_MEAN_TARGET_SHRINK_PCT = 8.5  # Future Work (p. 9)

# ------------------------------------------------------- Design arithmetic ---

DESIGN = {
    "study1": {"targets": 35, "grid": (7, 5), "repetitions": 6,
               "environments": 2, "trials_reported": 420, "participants": 20,
               "postures_reported": 8400, "sessions": 4,
               "gestures_per_session_reported": 105},
    "study2": {"targets": 35, "conditions": 6, "repetitions": 2,
               "trials_reported": 420, "participants": 16,
               "factorial_cells": 8},
    "screen_cm": (269.4, 136.2),
    "spacing_cm_reported": (44.9, None),  # "34.cm" -- digit lost in the PDF text
}

# ------------------------------------------------------------- Statistics ----
# Every F/p pair printed in the paper, in order of appearance.
FSTATS = [
    ("study1", "raw TLX over 4 sessions", 3, 57, 0.047, 0.986, "eq", "p. 5"),
    ("study1", "EFRC RealWorld vs VirtualReality", 1, 19, 5.845, 0.026, "eq", "p. 5"),
    ("study1", "FRC RealWorld vs VirtualReality", 1, 19, 33.13, 0.001, "lt", "p. 5"),
    ("study1", "HRC RealWorld vs VirtualReality", 1, 19, 31.48, 0.001, "lt", "p. 5"),
    ("study1", "IFRC RealWorld vs VirtualReality", 1, 19, 0.447, 0.512, "eq", "p. 5"),
    ("study2", "raw TLX over 6 sessions", 5, 15, 0.654, 0.659, "eq", "p. 8"),
    ("study2", "accuracy: CORRECTION", 1, 15, 5.321, 0.027, "eq", "p. 8"),
    ("study2", "accuracy: CURSOR", 1, 15, 131.9, 0.001, "lt", "p. 8"),
    ("study2", "accuracy: ENVIRONMENT", 1, 15, 1.3, 0.027, "eq", "p. 8"),
    ("study2", "accuracy: CORRECTION x ENVIRONMENT", 1, 15, 0.983, 0.36, "eq", "p. 8"),
    ("study2", "accuracy: CURSOR x ENVIRONMENT", 1, 15, 3.79, 0.070, "eq", "p. 8"),
    ("study2", "accuracy: CORRECTION x CURSOR", 1, 15, 4.592, 0.048, "eq", "p. 8"),
    ("study2", "accuracy: CORRECTION x CURSOR x ENVIRONMENT", 1, 15, 2.03, 0.175,
     "eq", "p. 8"),
    ("study2", "TCT: CORRECTION", 1, 15, 0.158, 0.697, "eq", "p. 8"),
    ("study2", "TCT: ENVIRONMENT", 1, 15, 0.004, 0.956, "eq", "p. 8"),
    ("study2", "TCT: CURSOR", 1, 15, 7.834, 0.013, "eq", "p. 8"),
    ("study2", "TCT: CURSOR x ENVIRONMENT", 1, 15, 15.61, 0.001, "lt", "p. 8"),
    ("study2", "TCT: CORRECTION x CURSOR", 1, 15, 0.067, 0.799, "eq", "p. 8"),
    ("study2", "TCT: CORRECTION x ENVIRONMENT", 1, 15, 1.291, 0.274, "eq", "p. 8"),
    ("study2", "TCT: CORRECTION x CURSOR x ENVIRONMENT", 1, 15, 1.163, 0.298,
     "eq", "p. 8"),
]

# ------------------------------------------- Predecessor paper, Mayer 2015 ----
# Sven Mayer, Katrin Wolf, Stefan Schneegass, Niels Henze. "Modeling Distant
# Pointing for Compensating Systematic Displacements." CHI 2015 LBW.
# DOI 10.1145/2702123.2702319. Tables 1 and 2, row "standing 2m".
MAYER2015_STANDING_2M = {
    "before": {"EFRC": 48.6, "IFRC": 55.4, "FRC": 222.9},
    "after_f4": {"EFRC": 36.7, "IFRC": 35.0, "FRC": 44.7},
}
# Claims the CHI'18 paper makes about that paper (p. 6).
REPORTED_RATIO_TO_MAYER2015 = {"EFRC": 4.8, "IFRC": 1.9, "FRC": 3.7}
REPORTED_MAYER2015_EFRC_VS_IFRC_PCT = 4.9
