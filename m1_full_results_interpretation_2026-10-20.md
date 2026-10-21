# M1 shared-reference module — FULL-run results and interpretation (20 Oct 2026)

Source: `m1_outputs(full)` from `bdhs_xai_m1_shared_reference_v1_1.ipynb` (MODE=FULL, feature set S0, n=4,105, 200 explained children, 5 reference draws x 3 explainer seeds).

## Integrity
- Fold hash 8a4f5168…, X hash 3eb260a0…, y hash ee4c36ab… all match the expected values; no overrides (version_drift=false, hash_mismatch=false, strict=true).
- All 8 gates passed: GM0 unit tests (LR IG-avg vs closed form 1.6e-9; SHAP 8e-17), GM1 (projected 2.10 h, measured work 1.19 h), GM2 (M0 reproduces FULL: max |diff| C = 0.0034, floors 0.0013), GM3a SHAP additivity 1.8e-9, GM3b IG completeness (per-baseline 7.5e-3 < 1e-2; averaged 5.3e-4), GM4 LIME R2 did not drop (-0.003), GM5 order check, GM6 constraint baseline violation 0% in real rows.

## Primary result (Spearman, delta = (C-N2)[M1] - (C-N2)[M0]; Bonferroni 7-cell interval)
| Cell | Delta M1-M0 | adj. CI | M1-C1 (sharing) | C1-M0 (ref. type/size) | Verdict |
|---|---|---|---|---|---|
| LR SHAP-LIME | -0.015 | [-0.028, -0.003] | +0.016 [0.007, 0.024] | -0.030 | no clear change (small decrease, below 0.05) |
| LR SHAP-IG | +0.044 | [0.033, 0.055] | +0.084 | -0.040 | below 0.05; near-identity by construction, not evidence |
| LR LIME-IG | -0.065 | [-0.078, -0.053] | +0.024 [0.013, 0.035] | -0.089 | INCREASED disagreement |
| RF SHAP-LIME | -0.005 | [-0.019, 0.009] | +0.014 [0.007, 0.022] | -0.019 | no clear change |
| MLP SHAP-LIME | -0.041 | [-0.058, -0.023] | +0.011 [-0.003, 0.025] | -0.052 | no clear change (small decrease, below 0.05) |
| MLP SHAP-IG | +0.168 | [0.144, 0.192] | +0.085 [0.075, 0.095] | +0.083 | REDUCED and faithful; sharing effect confirmed |
| MLP LIME-IG | -0.036 | [-0.061, -0.010] | +0.006 [-0.009, 0.022] | -0.042 | no clear change (small decrease) |

Reading: 1 of 7 cells meets the pre-specified "reduced" rule (MLP SHAP-IG). Raw MLP SHAP-IG Spearman 0.682 -> 0.913; null-adjusted gain 0.168. About half comes from replacing the mean baseline by averaged real baselines (C1-M0 = +0.083), half from sharing (M1-C1 = +0.085).
Every LIME-containing cell gets worse or stays flat when LIME's training_data is a 50-row reference (C1-M0 negative in all five); sharing recovers only 0.006-0.024. Conjecture (untested): LIME's reference set defines bins/scales/sampling, not a baseline expectation, so "sharing" it does not align LIME with SHAP/IG.

## Faithfulness (deletion with real-child replacements)
- F1 (beats random order) holds for every explainer and arm under both schemes.
- SHAP and IG: M1 vs M0 deletion advantage differs by < 0.005, CI includes 0 (preserved, not improved).
- F2 fails only for MLP LIME (both schemes): lower bound of A_M1 - A_M0 is about -0.0054 vs allowed -0.10*A_M0 (about -0.0034 cond). Point estimate about -5% (conditional) and -3% (marginal). Moot for verdicts (those cells are not "reduced").
- MLP LIME beats random for only 67.5% (cond) of children; MLP AUROC 0.599 and LIME local R2 about 0.23: weak model, weak surrogate.

## Realism diagnostics
Real training rows violate C1/C2 in 0% of cases (GM6 ok, constraints informative). Composite rows violate 6.6-13.1% (C1) and 8.5-20.6% (C2); conditional scheme is more realistic than marginal. Deletion is therefore approximately, not fully, on-manifold; conclusions agree across both schemes.

## Caveats to state in the thesis
- 1/7 cells; the headline is mixed, not "M1 works".
- LR SHAP-IG agreement is near-identity by construction.
- Faithfulness preserved is not faithfulness improved; higher agreement does not mean more correct explanations.
- Intervals are conditional on the fitted folds and 200 children; protocol developed over three pilots on the same data ("pre-specified", not "pre-registered").
- Reference sensitivity of SHAP/IG/LIME is known; novelty is the noise-calibrated, cross-model quantification and the sharing-vs-reference-type decomposition.
