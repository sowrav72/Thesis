# Pilot run 2: cross-implementation comparison, audit triage, notebook v3

17 Oct 2026. Inputs: notebook v2 results (`protocol_pilot_outputs_v2`), Codex re-implementation from Prompt A v2 (`codex_outputs_v2`, code in `bdhs_explanation_disagreement_code_v2`), and Codex's static audit of notebook v2 (Prompt B). All results below are **pilot, provisional**: 20 children per fold, 5 folds, and the protocol changes listed in section 4 will move several numbers.

## 1. Did the two implementations agree?

| Check | Result |
|---|---|
| n, stunted, `y_sha256`, `fold_sha256`, weight sum | **identical** (4105 / 966 / `ee4c36ab…` / `8a4f5168…` / 4104.52) |
| LR: AUROC, predictions, SHAP, LIME, IG, floors, cross C, N2, κ_N2, CIs | **identical to ~1e-8** |
| RF: AUROC (all 25 fits), SHAP/LIME E-axis floors, cross C, N2, κ_N2 | **identical to ~1e-8** |
| MLP AUROC | 21 of 25 cells identical to 15 digits; 4 cells differ by ≤ 6e-4 (e.g. fold 1 seed 3: 0.5395 vs 0.5389) |
| MLP SHAP/LIME E floors and SHAP–LIME cross C | identical to ~1e-9 |
| MLP pairs that include IG (cross C, T floors) | differ in the 3rd decimal (e.g. SHAP–IG 1-TV 0.7617 vs 0.7619) |
| Noise control (G5 inputs) | identical to 3 decimals; same failing rows |
| Tie diagnostics (G8) | identical |

**The MLP spec error from round 1 is fixed** (generator created once). The remaining MLP differences are consistent with thread-dependent float summation: Codex called `torch.set_num_threads(1)`, my notebook used all cores. v3 sets one thread.

### Where they disagree, and who is right

1. **Retrain-axis (T) floors differ for every SHAP and LIME row** (e.g. RF SHAP 1-TV 0.922 notebook vs 0.886 Codex; MLP SHAP Spearman 0.757 vs 0.726; Codex is lower in every SHAP/LIME row). **Cause: a bug in Codex's code, not in the notebook.** In `run_colab.py`, T-run 0 is filled by looping over the whole E-run dictionary, so every E run overwrites it and T-run 0 ends up as explainer seed 1005, while T-runs 1–4 use seed 1001. Four of the ten T-pairs therefore mix an explainer-seed change into the retrain floor, which lowers it. IG is unaffected (one E run), and the IG T floors agree. The notebook sets T-run 0 = E-run 0 (seed 1001) and runs 1–4 with seed 1001, as the protocol says. Practical consequence: Codex's `floorT_*`, `kappa_conservative_N2` and `min_floor_minus_N2` are not valid; the E-axis quantities are.
2. **Conservative κ and G7 differ by definition.** Codex uses the mean of per-child minima of the E and T floors; the notebook used the minimum of the two means. The audit also flagged this, and the per-child minimum is the better definition (v3 adopts it).
3. **G4 (IG completeness)**: notebook max |δ| = 5.3e-3 (pass); Codex max |δ| = 2.5e-2 (fail). Not resolved: Codex's per-run deltas are in its 168 KB `diagnostics.csv`, which I did not open. Likely a tail effect of a few MLP nets or the median/mode baseline. 100 IG steps is close to the limit, so v3 writes the delta per fold, model, run and baseline, so a failure can be located.

## 2. Provisional pilot results (notebook v2; Spearman, N2 null, E-axis κ)

| Model | Pair | Cross C | κ (95% CI, conditional) | Reading |
|---|---|---|---|---|
| LR | SHAP–LIME | 0.733 | 0.61 (0.57–0.65) | clear excess disagreement |
| LR | SHAP–IG | 0.930 | 0.96 | essentially at the noise ceiling |
| LR | LIME–IG | 0.777 | 0.63 | LIME is the outlier |
| RF | SHAP–LIME | 0.698 | 0.49 (0.45–0.53) | |
| MLP | SHAP–LIME | 0.506 | 0.43 (0.39–0.47) | largest excess among the shared pair |
| MLP | SHAP–IG | 0.690 | 0.64 | |
| MLP | LIME–IG | 0.383 | 0.31 | largest disagreement overall |

Observations that survive the caveats:
- LIME is the method that departs from the other two, in every model. SHAP and IG nearly coincide for the linear model, as theory predicts (same baseline logic, near-linear function).
- For the MLP the **retrain floor of IG is low (Spearman 0.67)**: retraining the same network with another seed changes the IG ranking about as much as switching from SHAP to IG on a fixed network. Under the conservative floor, MLP SHAP–IG conservative κ is ≈ 0.9–1.0 (0.91 / 0.95 / 1.04 / 0.91 across the four metrics), i.e. the disagreement is inside retrain noise. This is probably the most interesting pilot result, and it only exists because of the dual-seed design.
- MLP AUROC is 0.54–0.66 and unstable across seeds; any MLP claim carries that caveat.

Gate status of notebook v2: all pass except **G5** (noise column median rank 8–13 of 15 against a pre-registered ≥ 11; share relative to uniform 0.20–0.80 against ≤ 0.5). G8 passes at exactly 0.0100 for the `IG_medmode` sensitivity variant (2 of 200 and 6 of 600 vectors tie at the top-5 boundary because the child equals the typical-child baseline on several variables). That is a sensitivity variant, but the gate sits on its threshold.

**G5 interpretation.** The noise column carries 0.01–0.05 of the importance share (uniform would be 0.067), roughly half of the average real variable (≈ 0.069). With AUROC 0.62–0.64 many real variables are almost as uninformative as noise, so a rank threshold of ≥ 11 of 15 is hard to meet even by a correct explainer. Recommendation: **do not change the threshold** (it was pre-registered). Report G5 as failed, state this reading as a limitation, and use the new informational column `noise_over_median_real` for the comparison with a typical real variable.

## 3. Triage of the 12 audit findings (audit of notebook v2)

| # | Audit finding | Verdict | Action in v3 |
|---|---|---|---|
| 1 | SHAP E-axis changes the background as well as the permutation order | **Valid, and it biased in the unwanted direction** (extra noise lowers the SHAP floor, which raises κ) | Background fixed per fold (`SEED_BG + fold`); new `SHAP_bg` sensitivity axis varies only the background draw. In the synthetic smoke test the background-only floor is clearly lower than the permutation-only floor |
| 2 | Conservative κ / G7 not the per-child minimum | **Valid** | `cons_floor()` per child; G7 and `kappa_conservative_N2` use it; E-only version kept as `min_floor_minus_N2_Eonly` |
| 3 | LR twin is float32 | **Valid but small** (diff 6e-8) | Float64 twin and float64 IG inputs for LR |
| 4 | G0 always passes | **Valid** | `UNIT_TESTS_PASSED` flag set only when cell 6b completes |
| 5 | κ undefined-denominator guard | **Valid** | NaN with `kappa_status`; G6 fails on undefined κ; unit tests for N=1 and floor ≤ null |
| 6 | Notebook and Codex folder diverge; folder tests do not test the notebook | **Partly**: the independent implementation is meant to differ. Real gap: no unit test covered the κ/floor logic | Notebook is the canonical implementation; κ, floor and undefined cases are now unit-tested in cell 6b (includes the auditor's [.9,.1] / [.1,.9] example) |
| 7 | Unpinned shap/lime/captum | **Valid** | Pinned (`shap==0.52.0 lime==0.2.0.1 captum==0.9.0`), hard check at import, expected `fold_sha256`/`y_sha256` asserted |
| 8 | G1 projection omits probe and TreeSHAP check | **Valid, minor** (pilot projection 0.51 h vs 0.41 h measured wall time, so it was conservative) | Projection includes the probe; G1 also needs the measured sum of scheduled work ≤ 4 h |
| 9 | RF `n_jobs=-1` and torch threads break bitwise reproducibility | **Valid** | RF fitted in parallel, **predicts serially**; `torch.set_num_threads(1)` |
| 10 | "Exactly N_PERM permutations" can be false | **Valid as a claim, unlikely in practice** (needs a variable constant against all 50 background rows) | Effective permutations computed and recorded (`shap_min_effective_permutations`) |
| 11 | RBO is a normalised truncated variant | **Valid as wording** | Documented as normalised RBO@14 (identical rankings = 1), not Webber's extrapolated RBO |
| 12 | Wrong STRICT override instruction | **Valid** | Message now says `THESIS_STRICT=0` |

The audit also confirmed no train/test leakage (preprocessing, SHAP background, LIME training data, IG baselines, noise column all independent of test rows) and that IG is not applied to RF.

## 4. What v3 changes in the science (not just the code)

- **SHAP floor goes up, κ goes down.** Fixing the background removes a noise source from the E-axis floor, so ceilings rise and part of what v2 attributed to noise becomes excess disagreement. Expect the SHAP-based κ values above to fall. Do not treat the table in section 2 as final.
- **Conservative κ becomes stricter than before** (per-child minimum instead of the minimum of means).
- New diagnostic columns: `kappa_status`, `kappa_conservative_outside_0_1`, `min_floor_minus_N2_Eonly`, `median_real_variable_share`, `noise_over_median_real`, per-run IG deltas, `SHAP_bg` floors, `work_seconds`.

## 5. Remaining design concerns (unchanged from round 1)

LIME surrogate weights and SHAP contributions are different quantities; SHAP background, LIME perturbation distribution and IG baseline are three different reference distributions; summing dummy SHAP values is not grouped Shapley; one-child-per-cluster sampling is not survey-representative; class-balanced probabilities are not calibrated to 23.5%; bootstrap intervals are conditional on the fitted folds and too narrow (see `kappa_by_fold.csv`); the MLP is weak. These belong in the limitations section, not in more code.

## 6. Next steps

1. Run notebook **v3** in PILOT on Colab (about 30–45 min; the `SHAP_bg` axis adds SHAP passes). Check the printed `fold_sha256` matches `8a4f5168…`.
2. Run Prompt A **v3** in a new Codex session and compare using the table in the prompt file. The T floors should now agree.
3. Run Prompt B in another new session on the **v3** notebook.
4. If the gates pass apart from G5, run FULL with the same code (40 children per fold).
5. Do not retune anything on the results.
