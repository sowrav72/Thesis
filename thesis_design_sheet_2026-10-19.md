# Thesis design sheet (draft for sign-off, 19 Oct 2026)

Purpose: fix title, research questions, data, outcome, models, explainers, metrics and the minimum contribution **before** the proposal is written. Everything marked [DONE] is backed by the FULL run of notebook v3.1.1 (Colab, 18 Oct 2026; hashes verified; all gates pass except G5). Everything marked [NOT DONE] is a plan, not a result, and must be written in the proposal as planned work.

## 1. Working title

Recommended formal title (keeps the teacher's wording, adds outcome, dataset and the key method idea):

> **Quantifying and Reducing Disagreement Among SHAP, LIME and Integrated Gradients Explanations Across Model Types: A Noise-Calibrated Study of Child Stunting on BDHS 2022 Data**

Short title for slides and the abstract header: *Explanation Disagreement in Child Stunting Models: Quantifying and Reducing SHAP–LIME–IG Conflict on BDHS 2022 Data*.

Why not drop "Reducing": the teacher's direction contains it. It is honest only if the reduction part is actually tested (RQ3). Testing a mitigation and finding it does not help is still a valid result under this title.

## 2. Research questions

| # | Question | Tier | Evidence now |
|---|---|---|---|
| RQ1 | How large is SHAP–LIME disagreement for LR, RF and MLP stunting models, and how much of it exceeds each explainer's own noise (explainer-seed, retraining, SHAP-background variability)? | Minimum | [DONE] FULL run |
| RQ2 | For the differentiable models (LR, MLP): how do SHAP, LIME and IG relate to each other, and how sensitive is IG to its baseline and to dummy aggregation? (IG is not applicable to RF.) | Minimum | [DONE] FULL run + IG variants |
| RQ3 | Does a **shared-reference mitigation** reduce excess disagreement relative to the default configuration, while deletion-based faithfulness stays above random deletion? | Minimum | [NOT DONE] needs design + run |
| RQ4 | Does rank consensus across explainers, or adding maternal height (Arm B), change the picture? | Conference paper | [NOT DONE] |

Note on numbering: the earlier 4-question list had "predictor set" as RQ3 and mitigations as RQ4. Arm B needs a new model fit, a new feature (v438) and advisor approval, so it moves to the paper tier. The mitigation test moves up because the title promises it.

## 3. Data, cohort, outcome (exact, as run)

- Source: BDHS 2022 Kids Recode (BDKR81FL.DTA), 8,784 child records and 674 clusters in the file (counts you reported from the Colab load). Cluster = v001 (PSU); the analytic cohort of 4,105 children has 670 clusters (from the run metadata of the independent M1 pipeline; our own M1 notebook also records it).
- Analytic cohort: living children (b5 = 1) with a valid height-for-age z-score (hw70 < 9990): **n = 4,105**.
- Outcome: stunted = HAZ < -2 (hw70 < -200): **966 children (23.5%)**.
- Predictors (14, "S0"): b4, b19, bord, v012, v106, v190, v025, v024, v130, v136, v151, v113, v116, v212. Categorical: the coded variables (one-hot inside models); explanations are computed per source variable (14 players).
- Special codes: checked in the cohort; only v113/v116 code 97 (406 children, "not de-jure resident") occurs and is a separate level; v116 code 15 kept as a real answer. No 9/99 codes occur (guard in code).
- Validation: 5-fold, cluster-grouped, stratified (StratifiedGroupKFold, seed 20261016); fold hash 8a4f5168…, outcome hash ee4c36ab…, predictor-matrix hash 3eb260a0….
- Survey weights are used only for AUROC, not for fitting. Say "cluster-aware validation", not "accounts for survey design".

## 4. Models and performance (as run; weighted AUROC, mean over folds and training seeds)

| Model | Settings | AUROC |
|---|---|---|
| Logistic regression | C = 0.1, class-balanced, deterministic solver | 0.619 |
| Random forest | 300 trees, max depth 5, min leaf 5, balanced subsample | 0.641 |
| MLP (PyTorch) | 1 hidden layer of 32 ReLU units, 90 epochs, lr 1e-3, weight decay 1e-4, batch 128, positive-class weighting | 0.599 |

Predictive signal is modest and the MLP is weak. The thesis explains **these fitted models**; it makes no claim about causes of stunting. Reported probabilities are not calibrated to 23.5% prevalence (class-balanced fitting).

## 5. Explainers and compatibility

| | SHAP | LIME | Integrated Gradients |
|---|---|---|---|
| LR | Permutation SHAP (variable-level) | LIME tabular | yes, through a float64 PyTorch twin of the fitted LR (checked equal to sklearn) |
| RF | Permutation SHAP (TreeSHAP used only as a reference check, Spearman 0.93 vs permutation) | LIME tabular | **not applicable** (non-differentiable) |
| MLP | Permutation SHAP | LIME tabular | yes (Captum) |

Settings: SHAP 10 permutations, 50 training-row background (fixed per fold); LIME 5,000 samples, quartile discretization, all features; IG 100 Gauss–Legendre steps, baseline = training mean of the encoded inputs (sensitivity: median/mode baseline; sum of absolute dummy attributions). Explained quantity: predicted probability of stunting. Explanations: 200 children (40 per fold, at most one per cluster, same children for every model and method).

Fair-comparison statement: SHAP–LIME is compared on all three models; IG is compared on LR and MLP only; cross-model comparisons use the same method on different models. The three explainers use **different reference distributions** by default (SHAP 50-row background, LIME full-training discretized sampling, IG mean baseline). The measured disagreement is therefore the disagreement of default configurations, and RQ3 targets exactly this.

## 6. Measurement design [DONE]

- Importance = |attribution| per variable; metrics: 1 − total variation, Spearman, Jaccard@5, normalised RBO@14 (not Webber's extrapolated RBO). Never judge rank agreement by an l2-style magnitude metric.
- Noise floors (same method, same child): E-axis (5 explainer seeds, model fixed), T-axis (5 retraining seeds; RF and MLP only; LR is deterministic), B-axis (SHAP only: background draw changes).
- Nulls: N1 (random Dirichlet importance vectors; calibration check, Spearman ≈ 0), N2 (explanations of other children in the same fold, symmetrised).
- Reported quantities: cross-method similarity C; ceiling = N2 + (1 − N2)·√(rA·rB) where r = (floor − N2)/(1 − N2); **excess disagreement = ceiling − C**; κ = (C − N2)/(ceiling − N2). κ is a ceiling ratio, **not** a bounded agreement coefficient; values outside [0, 1] are reported, never clipped. Two versions: E-axis floors, and conservative (per-child minimum over E, T and B floors).
- Uncertainty: bootstrap over explained children (one per cluster); intervals are conditional on the selected children and fitted folds and are too narrow. Between-fold spread (kappa_by_fold.csv) is reported alongside.
- Gates G0–G8 were fixed before the final run; G5 (noise column) fails and is reported as a limitation. Use the wording "pre-specified before the final run", **not** "pre-registered": the protocol was refined over three pilots on the same data and this must be disclosed.

## 7. Results already in hand (FULL run, Spearman, N2 null)

| Model | Pair | C | Excess disagreement | κ (E-axis floor), 95% CI | κ conservative |
|---|---|---|---|---|---|
| LR | SHAP–LIME | 0.730 | 0.240 | 0.529 (0.508–0.550) | 0.587 |
| LR | SHAP–IG | 0.930 | 0.070 | 0.843 (0.827–0.859) | 0.959 |
| LR | LIME–IG | 0.774 | 0.196 | 0.620 (0.596–0.642) | 0.620 |
| RF | SHAP–LIME | 0.675 | 0.266 | 0.374 (0.343–0.404) | 0.434 |
| MLP | SHAP–LIME | 0.503 | 0.438 | 0.375 (0.348–0.403) | 0.500 |
| MLP | SHAP–IG | 0.682 | 0.306 | 0.578 (0.551–0.606) | 0.981 |
| MLP | LIME–IG | 0.380 | 0.572 | 0.303 (0.276–0.330) | 0.420 |

Supported statements:
1. Every pair involving LIME shows excess disagreement in every model (conservative κ 0.42–0.62).
2. SHAP–IG disagreement is close to the explanation-noise ceiling for LR and MLP under the conservative floor (Spearman κ 0.96 and 0.98; across the four metrics 0.85–0.96 for LR and 0.93–1.03 for MLP) but not under the E-axis floor alone (0.84 for LR; 0.58 for MLP). The conclusion depends on counting retraining and SHAP-background variability as noise; state this. "Within noise" means the gap is no larger than what retraining or background changes alone produce; it does not mean the two explainers are interchangeable. κ above 1 (MLP SHAP–IG Jaccard@5: 1.035) is reported, not clipped.
3. SHAP's ranking changes with the background draw alone (Spearman 0.85–0.90) and the MLP's IG ranking changes with the retraining seed (0.65): single-run explanations are not stable on this data.
4. IG depends on its baseline: median/mode baseline vs mean baseline Spearman 0.75 (LR), 0.68 (MLP).
5. Pilot-to-FULL stability: κ moved by at most 0.02 for every pair.

## 8. Three scopes

**Minimum viable thesis (everything needed for a defensible thesis):** RQ1 and RQ2 as above on BDHS 2022 stunting, Arm A (14 predictors), LR/RF/MLP, 200 explained children; plus **RQ3 with one mitigation (M1, shared reference)** evaluated against the default configuration and the noise floor, with a deletion-faithfulness check against random deletion. Compute: the whole measurement run took 0.46 h of measured work on Colab (projected 0.91 h); M1 is estimated at the same order [NOT DONE, to be verified].

**Stronger conference-paper scope:** MVP plus M2 (rank consensus, judged on stability and faithfulness, not on closeness to its own inputs, which would be circular), Arm B (adds maternal height v438; needs advisor approval), robustness to feature representation (child age b19 binning), per-fold analysis of κ, and an expanded explained sample if Colab time allows.

**Optional extensions:** a second outcome (e.g. diarrhoea), another DHS round or country, gradient-boosted trees with TreeSHAP, a larger MLP or any GPU-heavy run on the university computer, stable-core feature reporting.

## 9. Claims we may and may not make

May: "noise-calibrated, compatibility-aware comparison of SHAP, LIME and IG on clustered health-survey data"; "single-run attribution rankings on this data are not stable"; the numbered statements in section 7.
May not: "first" or "novel measurement of disagreement" (Krishna et al. 2024 measured it; Hwang et al. measured SHAP's own variability, SHAP only); IG on random forests; any claim about determinants of stunting; "reduces disagreement" before RQ3 is run; Parashar's 100% agreement; "accounts for survey design".

## 10. Risks and weak points (be ready for these questions)

1. Weak models (AUROC 0.60–0.64). Gate G5 fails: the random-noise column has a median rank of 8–13 out of 15 across the eight model/explainer cells (rank 1 = most important; the gate required a median rank of at least 11, i.e. near the bottom), and for MLP/SHAP and MLP/IG its importance-share ratio is 0.58 and 0.80 (gate: at most 0.5). So the fitted models lean on noise almost as much as on weak real variables; part of what the explainers rank is noise. Explanations of weak models may disagree more than those of strong ones; we do not claim otherwise.
2. κ is non-standard; headline numbers should be C, floors and excess disagreement, with κ as a normalised summary.
3. N2 mixes child heterogeneity into the null; N1 is a theoretical check only.
4. Different reference distributions across explainers are a design cause of disagreement (this is the point of M1), but LIME coefficients and SHAP/IG contributions are also different quantities on different scales; we compare |rank| only.
5. One child per cluster per fold is not survey-representative (200 children, 5 fixed folds).
6. Summed dummy-level SHAP/IG is variable-level aggregation, not grouped Shapley values.
7. The method was developed over three pilots on the same data; findings are exploratory with respect to protocol design.
8. M1 and faithfulness are untested; faithfulness (deletion) can look good for a trivially bad explainer, hence the random-deletion baseline.
9. One country, one survey round, one outcome.

## 11. Timeline to 25 Oct (6 days)

- 19–20 Oct: sign off this sheet (title, tiers, M1); write the M1 and deletion-faithfulness specification (planned work).
- 20–23 Oct: write the proposal: abstract, introduction, related work (from the verified matrix), methodology (sections 3–6), preliminary results (section 7), plan and risks.
- 23–24 Oct: slides (12 main slides per the teacher's template; light background, no animation); advisor review.
- 25 Oct: submit the first draft.
Implementing and running M1 before 25 Oct is optional and only worth it if reviewed code can be run by 23 Oct; an untested mitigation must not be rushed into the draft.

## 11b. Verification log (19 Oct 2026)

Section 7 table, section 6 formulas (ceiling and κ recomputed by hand for LR SHAP–LIME Spearman: ceiling 0.970, κ 0.529), IG-baseline sensitivities (0.747 LR, 0.681 MLP), SHAP-background floors (0.898 LR, 0.888 RF, 0.850 MLP), TreeSHAP check (0.928), run time, cohort counts (8,784 / 4,105 / 966) and the hashes were checked against the FULL files (cross_method_vs_floor, noise_floor, ig_variants, gate_report, run_metadata, data_profile). Corrections made: the 674-cluster figure applies to the whole file, not the analytic cohort; the MLP SHAP–IG Jaccard@5 conservative κ is 1.035 (1.008 is the E+T version; the pilot-3 report was corrected). Items not yet verifiable from files: pilot-to-FULL κ stability is taken from the pilot-3 report (pilot κ vs FULL κ, both from our runs).
Housekeeping: the notebook still labels its settings cell "PRE-REGISTERED SETTINGS"; rename to "PRE-SPECIFIED SETTINGS" in any version shown to the teacher or reviewers.

## 12. Decisions needed from the team

1. Title: recommended formal title above?
2. Include M1 (shared reference) in the minimum scope?
3. Move Arm B (v438) to the paper tier and ask the advisor for approval?
4. Use "pre-specified" instead of "pre-registered" throughout?

## 13. Status update, 20 Oct 2026 (supersedes the [NOT DONE] marks above for RQ3)

- RQ3 / M1 is now **[DONE]**: FULL run of bdhs_xai_m1_shared_reference_v1_1 (all gates passed; measured work 1.19 h on Colab, projected 2.10 h). Result: 1 of 7 cells meets the pre-specified "reduced" rule (MLP SHAP-IG, delta +0.168, adjusted CI 0.144-0.192, sharing effect M1-C1 +0.085, faithfulness preserved). LIME cells do not improve. Details: claude/m1_full_results_interpretation_2026-10-20.md.
- Older documents that still say "three mitigations" (research_gaps_problem_statement_2026-10-16.md) or "AUROC about 0.63-0.64" are stale: the minimum scope tests one mitigation (M1) and AUROC is 0.599-0.641 (LR 0.619, RF 0.641, MLP 0.599).
- Proposal slides, draft 1: Artifact "Thesis Proposal Slides (Draft 1)" (12 main + 6 backup slides).
