| # | claim | citation | reported | recomputed | verdict |
|---|---|---|---|---|---|
| 1 | average offset over environments for EFRC | Table 1 -> Accuracy of Ray Casts, p. 5 | 9.33 | 9.33 | consistent |
| 2 | remaining offset after correction for EFRC | Table 1 -> Modeling, p. 6 | 8.2 | 8.215 | consistent |
| 3 | LOOCV correction achieved for EFRC (mean of the two environments)<br>_paper truncates where it should round_ | Table 1 -> Modeling, p. 6 | 10.9 | 10.9615 | consistent |
| 4 | average offset over environments for IFRC | Table 1 -> Accuracy of Ray Casts, p. 5 | 28.09 | 28.085 | consistent |
| 5 | remaining offset after correction for IFRC | Table 1 -> Modeling, p. 6 | 14.0 | 14.035 | consistent |
| 6 | LOOCV correction achieved for IFRC (mean of the two environments) | Table 1 -> Modeling, p. 6 | 50.1 | 50.1081 | consistent |
| 7 | average offset over environments for FRC | Table 1 -> Accuracy of Ray Casts, p. 5 | 65.0 | 65.0 | consistent |
| 8 | remaining offset after correction for FRC | Table 1 -> Modeling, p. 6 | 28.6 | 28.595 | consistent |
| 9 | LOOCV correction achieved for FRC (mean of the two environments) | Table 1 -> Modeling, p. 6 | 55.9 | 55.9561 | consistent |
| 10 | average offset over environments for HRC | Table 1 -> Accuracy of Ray Casts, p. 5 | 42.46 | 42.46 | consistent |
| 11 | remaining offset after correction for HRC<br>_paper truncates rather than rounds; paper truncates where it should round_ | Table 1 -> Modeling, p. 6 | 42.3 | 42.385 | consistent |
| 12 | LOOCV correction achieved for HRC (mean of the two environments) | Table 1 -> Modeling, p. 6 | 0.2 | 0.1485 | consistent |
| 13 | overall correction of f4 across methods and environments | Modeling, p. 6 ('an overall correction of 29.3%') | 29.3 | 29.2936 | consistent |
| 14 | reduction achieved by the VR EFRC model | Model Discussion, p. 6 | 0.5 | 0.4734 | consistent |
| 15 | RW offset after correction: IFRC larger than EFRC by | Model Discussion, p. 6 | 89.2 | 89.1521 | consistent |
| 16 | HRC in VR: does the correction model reduce the offset?<br>_negative value means the fitted correction makes VR HRC worse_ | Table 1 | - | -0.1059 | consistent |
| 17 | Mayer et al. 2015 error before correction / this paper, EFRC<br>_matches only if 'overall' means the RealWorld column alone_ | Model Discussion, p. 6 vs Mayer et al. 2015 Table 1 (standing 2m) | 4.8 | 4.76 | consistent |
| 18 | Mayer et al. 2015 error before correction / this paper, IFRC<br>_matches only if 'overall' means the RealWorld column alone_ | Model Discussion, p. 6 vs Mayer et al. 2015 Table 1 (standing 2m) | 1.9 | 1.9012 | consistent |
| 19 | Mayer et al. 2015 error before correction / this paper, FRC<br>_matches only if 'overall' means the RealWorld column alone_ | Model Discussion, p. 6 vs Mayer et al. 2015 Table 1 (standing 2m) | 3.7 | 3.6941 | consistent |
| 20 | Mayer et al. 2015: EFRC larger than IFRC after correction (standing 2m) | Model Discussion, p. 6 vs Mayer et al. 2015 Table 2 | 4.9 | 4.8571 | consistent |
| 21 | correction improvement, RealWorld, no cursor | Table 3 -> Discussion, p. 9 | 16.3 | 16.3842 | consistent |
| 22 | correction improvement, VirtualWorld, no cursor | Table 3 -> Discussion, p. 9 | 9.5 | 9.5761 | consistent |
| 23 | overall correction improvement without a cursor<br>_pooling the cell means gives 13.16%; averaging the two per-environment percentages instead gives 12.98%; paper truncates where it should round_ | Table 3 -> Discussion, p. 9 / Conclusion | 13.1 | 13.1599 | consistent |
| 24 | average correction improvement with a cursor<br>_pooling the cell means gives 4.51%; averaging the two per-environment percentages instead gives 4.28%_ | Table 3 -> Discussion, p. 9 / Conclusion | 4.5 | 4.5082 | consistent |
| 25 | average shrink of the 90%-capture square target under correction | Future Work, p. 9 ('on average 8.5% smaller') | 8.5 | 8.475 | consistent |
| 26 | no-cursor TCT identical with and without correction (RealWorld)<br>_the design collapses 8 cells to 6; this is the fingerprint of it_ | Table 2 vs Study Design, p. 7 | 0.0 | 0.0 | consistent |
| 27 | no-cursor TCT identical with and without correction (VirtualWorld)<br>_the design collapses 8 cells to 6; this is the fingerprint of it_ | Table 2 vs Study Design, p. 7 | 0.0 | 0.0 | consistent |
| 28 | square target side holding 90% of pointings (no_cursor, RW)<br>_needs the raw per-trial endpoints; the figure shown is what an isotropic Rayleigh assumption on Table 3's mean would give, and is our assumption, not the paper's_ | Accuracy, p. 8 | 17.6 | 22.02 | NOT DERIVABLE |
| 29 | square target side holding 90% of pointings (no_cursor, VR)<br>_needs the raw per-trial endpoints; the figure shown is what an isotropic Rayleigh assumption on Table 3's mean would give, and is our assumption, not the paper's_ | Accuracy, p. 8 | 18.8 | 19.81 | NOT DERIVABLE |
| 30 | square target side holding 90% of pointings (cursor, RW)<br>_needs the raw per-trial endpoints; the figure shown is what an isotropic Rayleigh assumption on Table 3's mean would give, and is our assumption, not the paper's_ | Accuracy, p. 8 | 4.1 | 3.55 | NOT DERIVABLE |
| 31 | square target side holding 90% of pointings (cursor, VR)<br>_needs the raw per-trial endpoints; the figure shown is what an isotropic Rayleigh assumption on Table 3's mean would give, and is our assumption, not the paper's_ | Accuracy, p. 8 | 4.5 | 4.04 | NOT DERIVABLE |
| 32 | 35 targets x 6 repetitions x 2 environments | Study Design, p. 3-4 | 420 | 420 | consistent |
| 33 | 420 trials x 20 participants | Results, p. 5 ('8,400 mid-air pointing postures') | 8400 | 8400 | consistent |
| 34 | 420 gestures split into 4 sessions | Procedure, p. 5 | 105 | 105.0 | consistent |
| 35 | 7 x 5 grid holds 35 targets | Study Design, p. 3 | 35 | 35 | consistent |
| 36 | 6 conditions x 35 targets x 2 repetitions | Study Design, p. 7 | 420 | 420 | consistent |
| 37 | horizontal target spacing = width / (7-1) | Apparatus, p. 4 | 44.9 | 44.9 | consistent |
| 38 | vertical target spacing = height / (5-1)<br>_the PDF text layer loses a digit; 136.2/4 = 34.05 cm fits_ | Apparatus, p. 4 (printed as '34.cm') | - | 34.05 | consistent |
| 39 | error df of the study 2 RM-ANOVAs = participants - 1<br>_16 participants, cell means per participant -> F(1,15) is right for the 2x2x2; the raw-TLX F(5,15) is not (6 sessions x 16 participants gives F(5,75))_ | Results, p. 8 | 15 | 15 | consistent |
| 40 | raw TLX over 4 sessions: F(3,57) = 0.047, p = 0.986<br>_F as printed implies p in [0.98614, 0.98656]_ | p. 5 | 0.986 | 0.98635 | consistent |
| 41 | EFRC RealWorld vs VirtualReality: F(1,19) = 5.845, p = 0.026<br>_F as printed implies p in [0.02583, 0.02584]_ | p. 5 | 0.026 | 0.02584 | consistent |
| 42 | FRC RealWorld vs VirtualReality: F(1,19) = 33.13, p < 0.001<br>_F as printed implies p in [0.00002, 0.00002]_ | p. 5 | 0.001 | 2e-05 | consistent |
| 43 | HRC RealWorld vs VirtualReality: F(1,19) = 31.48, p < 0.001<br>_F as printed implies p in [0.00002, 0.00002]_ | p. 5 | 0.001 | 2e-05 | consistent |
| 44 | IFRC RealWorld vs VirtualReality: F(1,19) = 0.447, p = 0.512<br>_F as printed implies p in [0.51157, 0.51204]_ | p. 5 | 0.512 | 0.5118 | consistent |
| 45 | raw TLX over 6 sessions: F(5,15) = 0.654, p = 0.659<br>_F as printed implies p in [0.66291, 0.66359]_ | p. 8 | 0.659 | 0.66325 | INCONSISTENT |
| 46 | accuracy: CORRECTION: F(1,15) = 5.321, p = 0.027<br>_F as printed implies p in [0.03575, 0.03576]_ | p. 8 | 0.027 | 0.03576 | INCONSISTENT |
| 47 | accuracy: CURSOR: F(1,15) = 131.9, p < 0.001<br>_F as printed implies p in [0.00000, 0.00000]_ | p. 8 | 0.001 | 0.0 | consistent |
| 48 | accuracy: ENVIRONMENT: F(1,15) = 1.3, p = 0.027<br>_F as printed implies p in [0.26343, 0.28114]; changes the significance decision at alpha = .05_ | p. 8 | 0.027 | 0.27209 | INCONSISTENT |
| 49 | accuracy: CORRECTION x ENVIRONMENT: F(1,15) = 0.983, p = 0.36<br>_F as printed implies p in [0.33707, 0.33730]_ | p. 8 | 0.36 | 0.33718 | INCONSISTENT |
| 50 | accuracy: CURSOR x ENVIRONMENT: F(1,15) = 3.79, p = 0.07<br>_F as printed implies p in [0.07037, 0.07070]_ | p. 8 | 0.07 | 0.07053 | consistent |
| 51 | accuracy: CORRECTION x CURSOR: F(1,15) = 4.592, p = 0.048<br>_F as printed implies p in [0.04892, 0.04894]_ | p. 8 | 0.048 | 0.04893 | consistent |
| 52 | accuracy: CORRECTION x CURSOR x ENVIRONMENT: F(1,15) = 2.03, p = 0.175<br>_F as printed implies p in [0.17420, 0.17519]_ | p. 8 | 0.175 | 0.17469 | consistent |
| 53 | TCT: CORRECTION: F(1,15) = 0.158, p = 0.697<br>_F as printed implies p in [0.69615, 0.69706]_ | p. 8 | 0.697 | 0.6966 | consistent |
| 54 | TCT: ENVIRONMENT: F(1,15) = 0.004, p = 0.956<br>_F as printed implies p in [0.94740, 0.95361]_ | p. 8 | 0.956 | 0.95041 | INCONSISTENT |
| 55 | TCT: CURSOR: F(1,15) = 7.834, p = 0.013<br>_F as printed implies p in [0.01349, 0.01349]_ | p. 8 | 0.013 | 0.01349 | consistent |
| 56 | TCT: CURSOR x ENVIRONMENT: F(1,15) = 15.61, p < 0.001<br>_F as printed implies p in [0.00128, 0.00128]_ | p. 8 | 0.001 | 0.00128 | INCONSISTENT |
| 57 | TCT: CORRECTION x CURSOR: F(1,15) = 0.067, p = 0.799<br>_F as printed implies p in [0.79854, 0.80001]_ | p. 8 | 0.799 | 0.79927 | consistent |
| 58 | TCT: CORRECTION x ENVIRONMENT: F(1,15) = 1.291, p = 0.274<br>_F as printed implies p in [0.27360, 0.27378]_ | p. 8 | 0.274 | 0.27369 | consistent |
| 59 | TCT: CORRECTION x CURSOR x ENVIRONMENT: F(1,15) = 1.163, p = 0.298<br>_F as printed implies p in [0.29778, 0.29798]_ | p. 8 | 0.298 | 0.29788 | consistent |
