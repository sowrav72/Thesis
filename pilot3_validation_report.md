# Pilot run 3: v3 notebook vs v3 Codex re-implementation, audit-of-v3 triage, notebook v3.1

18 Oct 2026. All numbers are PILOT (20 children/fold, 5 folds), provisional.

## 1. v3 notebook vs v3 Codex (independent implementation)
- Identical: n=4105, stunted=966, y/fold hashes, weight sum, LR and RF AUROC, all E-axis floors, cross-method C, N2, ceilings, kappa (to ~1e-9).
- T-axis (retrain) floors now agree (RF SHAP 1-TV 0.9199 both): the v2 discrepancy was a Codex bug, fixed by Prompt A v3.
- G4 IG completeness: notebook 5.6e-3, Codex 3.7e-3 (both pass; the earlier 0.025 did not reproduce).
- All gates agree: PASS except G5 (noise column), known limitation (many real variables are near-zero too). G8: notebook 0.0100 (worst model/method incl. IG_medmode variant) vs Codex 0.0009 (union over primary vectors): definition difference, both pass.
- MLP: 4 of 25 fits differ by <= 6e-4 AUROC (fold1/seed3, fold2/seed3, fold3/seed4, fold4/seed4) even single-threaded; effect on kappa ~1e-4. Cause not identified; recorded as a limitation. (Whether the same cells differed in v2 was not verified.)

## 2. Scientific finding: SHAP background sensitivity
SHAP_bg floor (only the 50-row background draw changes), Spearman: LR 0.895, RF 0.883, MLP 0.856, versus permutation-only floor ~0.99. v3 kappa (E-axis floor) fell versus v2: LR SHAP-IG 0.96 -> 0.83, LR SHAP-LIME 0.61 -> 0.54, RF SHAP-LIME 0.49 -> 0.39, MLP SHAP-LIME 0.43 -> 0.35. Including the background axis in the conservative floor brings LR SHAP-IG back to about 0.95 (hand calculation): SHAP and IG differ by about as much as SHAP differs from itself under another background.
Decision (v3.1): the conservative floor is the per-child minimum over E, T and (for SHAP) background axes. The v3 E+T version is kept as kappa_conservative_ET_N2. Limitation: LIME's reference distribution and IG's baseline are not given an analogous axis.

## 3. Triage of Codex's audit of v3 (11 findings)
| # | Finding | Verdict | v3.1 action |
|---|---|---|---|
| 1 | DHS special codes not normalised | No effect in this cohort: value counts show only code 97 (406 children in v113/v116, already handled); no 9/99 anywhere; numeric ranges sane | Guard: assert no 9/99/999/9999 in categorical predictors, numeric max < 90 |
| 2 | Undefined bootstrap replicates dropped | Valid | Interval = NaN if any replicate undefined; count column; G6 requires zero invalid |
| 3 | G2 seed 0 only | Valid | G2 on mean over all fits; seed-0 value reported |
| 4 | Absolute values ignore sign | Design choice | Keep (magnitude-only estimand); limitation; optional sign-agreement table for the paper tier |
| 5 | Drift override also skips hashes | Valid | Separate THESIS_ALLOW_VERSION_DRIFT and THESIS_ALLOW_HASH_MISMATCH; outcome hash always enforced; overrides recorded |
| 6 | X not hashed | Valid, minor | x_sha256 recorded; pin after first FULL run |
| 7 | G4 <= vs <, scope | Valid, minor | `<`; includes noise-control SHAP/IG calls (timed probe is discarded) |
| 8 | S5 noise-control dimension | Valid | Control always 14 primary predictors + noise |
| 9 | RBO variant | Documented | Known-value unit tests added |
| 10 | All-missing numeric column | Valid, trivial | Early error naming variable |
| 11 | G1 projection rough | Fair | Unchanged (screening estimate) |

## 4. Next
Run notebook v3.1 PILOT on Colab once; check hashes (fold 8a4f5168..., y ee4c36ab...; x_sha256 is new and only recorded). If gates pass except G5, run FULL unchanged.

## 5. v3.1 PILOT result (Colab, 18 Oct 2026)
Hashes: fold 8a4f5168..., y ee4c36ab... match; overrides all false; x_sha256 = 3eb260a03428d8e08e3b2d34bd6d9be932576a71445c9202b307dda3e544093a (now enforced in v3.1.1). Measured work 0.26 h.
Gates: G0-G4, G6-G8 PASS; G5 FAIL (known, reported as limitation). G2 (all fits): LR 0.619, MLP 0.599, RF 0.641; G4b max IG delta 5.56e-3 (incl. noise control); G6 widths 0.065/0.081/0.080, 0 invalid bootstrap replicates; G7 (E,T,background): LR 0.439, RF 0.366, MLP 0.488; G8 max share 0.0100 (IG_medmode sensitivity variant only, exactly at the limit).
Reproducibility: every E-axis table is identical to the v3 pilot to full precision (same data, same code path), which is evidence that the pipeline is deterministic.

Spearman, N2 null, kappa: E-axis floor -> conservative (E, T, SHAP background):
| Model | Pair | kappa (E) | kappa conservative |
|---|---|---|---|
| LR | SHAP-LIME | 0.54 | 0.60 |
| LR | SHAP-IG | 0.83 | 0.95 |
| LR | LIME-IG | 0.63 | 0.63 |
| RF | SHAP-LIME | 0.39 | 0.45 |
| MLP | SHAP-LIME | 0.35 | 0.46 |
| MLP | SHAP-IG | 0.57 | 0.96 |
| MLP | LIME-IG | 0.31 | 0.42 |
Reading: SHAP-IG disagreement is within explanation noise for LR and MLP (conservative kappa about 0.95); every pair involving LIME shows real excess disagreement (conservative kappa 0.42-0.63). Intervals are conditional on the fitted folds and selected children (too narrow). MLP AUROC is weak (0.60).
Pre-stated rule for FULL: if G8 fails only through the IG_medmode sensitivity variant, report it as a documented exception; do not change the gate or the code.

## 6. FULL run result (v3.1.1, Colab, 18 Oct 2026; 40 children per fold = 200 children, 5 folds)
Integrity: mode FULL; fold, y and predictor-matrix hashes all match; no overrides; measured work 0.46 h.
Gates: all PASS except G5 (unchanged, known: the noise control always uses 20 children per fold, so it is identical to the pilot). G4b max IG delta 7.2e-3 (limit 1e-2); G6 widths LR 0.041, RF 0.061, MLP 0.055 with 0 invalid replicates; G7 LR 0.437, RF 0.355, MLP 0.488; G8 max share 0.0050 (no exception needed).

Spearman, N2 null. cross C; excess disagreement; kappa (E-axis floor) -> conservative kappa (E, T, SHAP background):
| Model | Pair | C | excess | kappa (E) [95% CI, conditional] | conservative kappa |
|---|---|---|---|---|---|
| LR | SHAP-LIME | 0.730 | 0.240 | 0.529 [0.508, 0.550] | 0.587 |
| LR | SHAP-IG | 0.930 | 0.070 | 0.843 [0.827, 0.859] | 0.959 |
| LR | LIME-IG | 0.774 | 0.196 | 0.620 [0.596, 0.642] | 0.620 |
| RF | SHAP-LIME | 0.675 | 0.266 | 0.374 [0.343, 0.404] | 0.434 |
| MLP | SHAP-LIME | 0.503 | 0.438 | 0.375 [0.348, 0.403] | 0.500 |
| MLP | SHAP-IG | 0.682 | 0.306 | 0.578 [0.551, 0.606] | 0.981 |
| MLP | LIME-IG | 0.380 | 0.572 | 0.303 [0.276, 0.330] | 0.420 |
Pilot-to-FULL stability: kappa moved by <= 0.02 for every pair (e.g. LR SHAP-LIME 0.541 -> 0.529). The other three metrics (1-TV, Jaccard@5, RBO) tell the same story; MLP SHAP-IG Jaccard@5 conservative kappa is 1.035 (1.008 for the E+T version; both outside [0,1], reported, not clipped). [Corrected 19 Oct 2026 against cross_method_vs_floor.csv.]
Reading: (1) pairs involving LIME show real excess disagreement for every model; (2) SHAP-IG disagreement is inside explanation noise for LR and MLP under the conservative floor, but not under the E-axis floor alone (MLP: 0.58 vs 0.98), so that conclusion depends on counting retrain and background variability as noise; (3) the MLP is weak (AUROC 0.60) and its IG retrain floor is low (Spearman 0.65). Intervals are conditional on the fitted folds and selected children and are narrow; the between-fold spread is in kappa_by_fold.csv.
