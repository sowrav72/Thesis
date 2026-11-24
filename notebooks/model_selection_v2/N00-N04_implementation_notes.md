# N00–N04 implementation notes (plan v2.2, sections 3–6) — revised 25 Nov 2026

Change-control record. Approve or change these choices **in the plan first**, then in the code.

## Notebooks
| Notebook | Plan stage | Purpose |
|---|---|---|
| N00 | 0 | folders, helper file, versions/seeds, reproducibility tests (incl. fixed-epoch MLP) |
| N01 | 1 | cohort from the **original KR file** (needs `BDKR81FL.DTA`), sample flow, b5/v135 audit, sign-off |
| **N01B** | 1 | **same stage for the supplied extract** (what you have now); sign-off records D1/U1 as open |
| N02 | 2 | design/strata counts, missingness, T3, **written special-code decisions**, frozen predictor list |
| N03 | 3 | PSU-disjoint split + manifest checksum, training-only preprocessing per fold, unseen-level count, 30 assertions |
| N04 | 4 | tuning, selection, record audit, label-shuffle canary, locked test (once) |

## What the review changed (25 Nov 2026)
1. **Final MLP now trains on all development rows.** Development CV still uses the inner early-stopping split to find each configuration's best epoch. The final MLP is re-initialised (same seed) and trained on every development row for a fixed budget = median of the selected configuration's five fold-level best epochs (rounded up). The test set plays no part. Asserted: rows used = all development rows.
2. **Special codes are explicit decisions**, saved as `coding_decisions.csv` and recorded in the predictor-freeze table. Proposed defaults (yours to change): v113/v116 code 97 → own level `not_applicable_97`; v701 code 8 and v705 code 98 (don't know, 7 children each) → `missing`. N03/N04 read the saved table, so every stage uses the same coding.
3. **b5 / v135 audit** added to N01 (no filter added; shows b5/v135 values among children with a valid HAZ).
4. **Epoch audit strengthened.** The full epoch-order schedule of every MLP run is logged. The audit checks each variant's schedule is a prefix of the longest one (variants may stop at different epochs — intended). Best epoch and epochs run are logged for every run.
5. Wording: a **common initialisation seed**, not identical weights (architectures differ).
6. **Unknown-category policy** written into the helper and N03; N03 counts how often it applies.
7. Test-set flag is documented as a guard against accidental re-runs, **not access control**; the manifest checksum is re-verified before the locked test.

Not changed: review point 3's "mother interviewed" step stays an assumption until reconciled with the report.

## Observations from the supplied extract (4,105 rows × 24 columns; counts only)
- **Absent from the extract:** `hw70`, `b5`, `v135`, `v501`, `caseid`, `v003`. A ready-made `stunting` column exists (966 stunted, 23.5%). So D1 (hw70 < -200 rule), the DHS validity rules and the sample-flow reconciliation (U1) **cannot be checked from this file**, nor can code 97 vs v135 or v701/v705 missingness vs v501.
- 670 PSUs, 16 strata, at least 17 PSUs in every stratum (no sparse strata); 1–17 children per PSU (median 6).
- `b11` is in months (8–260, 181 distinct values): the plan's "categorical" needs the binning in D14. 1,550 missing with bord = 1, 11 missing with bord > 1, none present with bord = 1.
- v113 and v116 code 97: the same 406 children in both → looks like a questionnaire-universe code. The file stores no text value labels, so its meaning must come from the DHS recode manual.
- v701/v705: 52 missing on the same rows; "don't know" codes (8 / 98): 7 children each. v445: no flagged codes (2 missing).
- `sample_weight` equals v005/1,000,000 (women's weight; U4 open).
- T3 flags (descriptive): bord–v012 Spearman 0.67; v701–v705 Cramér's V 0.52.

## Decisions I made (need your approval)
- **D13** Test partition = outer fold 0; same-record rule for all model variants (training/validation rows) and for MLP variants (fitting rows, early-stopping rows, record order per epoch number).
- **D14** `b11` bins <24, 24–35, 36–47, 48+ months (fixed, not learned) + `first_birth_NA` (missing, bord = 1) + `missing` (missing, bord > 1).
- **D15** Threshold for threshold-dependent metrics: F1-maximising threshold on pooled development out-of-fold predictions.
- **D16** MLP early stopping on an inner PSU-disjoint split of the training rows (development CV only). Final MLP: fixed epoch budget, all development rows (see above).
- **D17** Rare categories (training count < 30) → `__rare__`; AP tie tolerance 0.002; log-loss tie 0.0001; "simpler" = LR smaller C, RF smaller depth/leaf ratio, XGB fewer depth×trees, MLP fewer parameters. Tree slot: higher mean AP; if within tolerance, lower mean log loss.
- **D18** Cohort rules in N01: eligible = hw70 present; hw70 ≥ 9990 removed; |HAZ| > 6 SD removed. (Not applicable to the extract.)
- **D19** Special-code defaults listed under change 2.
- Fixed settings: LR L2 (default), lbfgs, max_iter 2000; RF 300 trees, random_state 42, n_jobs 2; XGB subsample = colsample = 0.8, reg_lambda 1, min_child_weight 1, hist, random_state 42; MLP Adam (weight_decay = L2 penalty), batch 64, max 100 epochs, patience 10, no class weights.

## Limitations to state honestly
- In development CV the MLP updates weights on about 80% of the training rows (the rest is early stopping), while LR/RF/XGBoost use all training rows. MLP CV scores are therefore based on a smaller fitting set. The final MLP uses all development rows. Option to remove the mismatch: refit each MLP variant on all training rows for its best epoch inside every CV fold (about 2× MLP time). Not done; your call.
- The fold-level best epochs come from a smaller fitting set than the final model sees; the epoch budget is an approximation.
- The label-shuffle canary does not prove every leakage path is absent.
- One-hot column sets can differ slightly between folds (a rare level can appear in one fold only); handled inside each fold.

## What was tested
- Fake KR-like file (6,800 rows): N00–N04 end to end, 30/30 checks in N03 and N04, final MLP trained on all development rows.
- Your extract: N00, N01B, N02, N03 and the N04 tuning cells ran without errors (30/30 checks in N03). The **locked-test cell was not run**, so the test partition is still unopened. No model scores were looked at or reported.
- Not run in Colab itself.
