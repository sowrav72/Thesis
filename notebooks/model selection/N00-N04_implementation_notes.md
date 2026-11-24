# N00–N04 implementation notes (plan v2.2, sections 3–6) — 24 Nov 2026

Change-control record: these are the choices the code makes where plan v2.2 is silent or needs a decision. Per the plan's own rule, approve or change them **in the plan first**, then in the code.

## What was built
| Notebook | Plan stage | Output |
|---|---|---|
| N00 | 0 | folders, helper file, versions/seeds, reproducibility test, KR file hash |
| N01 | 1 | cohort rebuilt from original KR, T1 sample flow, value-label and U2 audit tables, private audit files, **sign-off gate** |
| N02 | 2 | design/strata counts, missingness, prevalence, T3 associations, frozen predictor list, **sign-off gate** |
| N03 | 3 | fixed PSU-disjoint split + manifest checksum, training-only preprocessing per fold, 31 leakage assertions |
| N04 | 4 | 4 families × bounded grids × 5 dev folds, tuning log, selection, same-record audit, label-shuffle canary, locked test (run once) |

## Leakage controls
- Split by PSU (v021) before any fitting; no PSU in both development and test (asserted, re-asserted before scoring).
- Medians, scaling, category levels and the rare-category rule are fitted on training rows only, once per development fold; the spec stores a hash of the row ids it was fitted on and N03 asserts it equals the training ids.
- Predictor list is checked against a forbidden list (hw70/hw71–73, IDs, weights, PSU/stratum, m14/m15/v438, etc.).
- N02 builds no outcome-by-predictor tables.
- Test rows are not transformed or scored until the single locked-test cell in N04; a flag file blocks a second run.
- Split manifest checksum is verified again before the locked test.
- Label-shuffle canary in N04: LR trained on shuffled labels must score AP ≈ prevalence.

## Same records for every model variant (your requirement)
- All LR/RF/XGB/MLP configurations read the **same fold arrays** from N03. Every run logs a hash of its training and validation row ids; N04 asserts the hash is identical across all runs of a fold.
- MLP "epoch" rule: all variants use the same fitting rows (training rows minus the frozen early-stopping rows), the same early-stopping rows, the same initial-weight seed, and the same record order in every epoch. Epoch `e` uses `get_epoch_order(n_rows, e, MLP_DATA_ORDER_SEED + fold)`, which depends only on the epoch number and seed — not on layers, learning rate or weight decay. Each epoch uses every fitting record exactly once (asserted in the training loop).
- Independently tested by recording the orders requested by two different MLP variants: identical in all 20 compared epochs.

## Decisions I made (need your approval)
- **D13** Test partition = outer fold 0 (plan 5.1 says "one fold" without saying which). Same-record/epoch rule above is also added.
- **D14** `b11` is birth interval in months in the KR file, but the plan lists it as categorical. Fixed pre-declared bins: <24, 24–35, 36–47, 48+; plus `first_birth_NA` (missing and bord = 1) and `missing` (missing and bord > 1). Not learned from data.
- **D15** Threshold rule for threshold-dependent metrics: the threshold that maximises F1 on pooled development out-of-fold predictions of the selected configuration.
- **D16** MLP early stopping uses an inner PSU-disjoint split (about 20% of PSUs) of the training rows, frozen in N03. Early stopping on the scoring fold would leak into model selection.
- **D17** Rare categories: training count < 30 grouped into `__rare__` (count-based, training rows only). AP tie tolerance 0.002; log-loss tie 0.0001; "simpler" = LR smaller C, RF smaller depth/leaf ratio, XGB fewer depth×trees, MLP fewer parameters. Tree slot (RF vs XGB): higher mean AP; if within tolerance, lower mean log loss.
- **D18** Cohort rules in N01: eligible = hw70 present; special codes ≥ 9990 removed; |HAZ| > 6 SD removed; the "mother interviewed" step removes nothing because KR holds children of interviewed women (assumption — verify against the 4,420 vs 4,199 gap).
- Fixed model settings not spelled out in the plan: LR L2 (scikit-learn default), lbfgs, max_iter 2000; RF 300 trees, random_state 42, n_jobs 2; XGB subsample = colsample = 0.8, reg_lambda 1, min_child_weight 1, hist, random_state 42; MLP Adam (weight_decay = L2 penalty), batch 64, max 100 epochs, patience 10 on early-stopping log loss, no class weights.
- One-hot column sets can differ slightly between folds (a rare level can appear in one fold only). This is handled inside each fold; the feature map for the final models comes from the full-development fit.

## Not verified
- Everything was dry-run only on a **fake** KR-like file (6,800 rows). No real BDHS data was touched, so no real results exist.
- Not run inside Colab itself (Drive mount path assumed `/content/drive/MyDrive/THESIS_V2`).
- Real value labels, special codes, the b11 coding, the eligibility rule and the v701/v705 and v113/v116 universes must be read from your N01 output and signed off (U1, U2).
- Weights are not used anywhere in modelling (U4 stays open).
