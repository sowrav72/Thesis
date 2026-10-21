# Research gaps and problem statement: verified update (16 Oct 2026, revised after the two reading reports)

Full version with tables, links and read levels: the doc "Research Gaps and Problem Statement (Verified Update)". Matrix: literature_matrix_hybrid_master_v3.xlsx. This file is the short copy for later sessions.

## Verdict on the hybrid matrix
- Core facts re-checked and confirmed: T01 (84% = 21/25 interviewees; rank agreement < 0.1 on AG News LSTM), T11 (maternal height used, no SHAP, BDHS 2022 n=1,963), T13, T20.
- Fixed: T04 title cell; T01 venue is TMLR 2024; T32 category "e" -> 6; category summary rebuilt with counts; T24 AUROC 99.79% flagged implausible.
- Seven abstract-only IEEE rows from the extended matrix (E20, E21, E23, E24, E25, E27, E28) restored as T43-T49.

## Old claims that change
- Drop: "only one mitigation published". Five more exist: AGREED (ICLR 2026), GRANITE (AISTATS 2026), PEAR (Schwarzschild 2023), Parashar et al. 2026, Mitrut et al. 2024.
- Narrow: "SHAP-LIME-IG across LR/RF/MLP jointly" (IG cannot run on RF); "no DHS disagreement study" (Nabuuso, ICPRAM 2025, Uganda DHS, qualitative).
- Keep, narrowed: noise-floor gap. Hwang et al. measure SHAP's own variability (within SHAP only).
- Drop as a gap: "maternal height/BMI is leakage". Treat as hypothesis; Arm A vs Arm B tests it (RQ3).

## Revised gaps
- G1 disagreement reported without a noise floor (main gap). Confirmed by the full-text reading of Hwang et al. (NeurIPS 2026 Evaluations and Datasets per the PDF): SHAP only, LIME and IG variability unmeasured.
- G2 model-type comparisons ignore method-model compatibility.
- G3 no quantitative explanation comparison on clustered health-survey data (BDHS).
- G4 mitigations exist but are untested in this setting. Regional evidence can be inflated by tiny clusters (Parashar preprint), so mitigation tests need a granularity control.

## What the full-text readings changed (from the user's two reading reports; PDFs not opened by me)
- Hwang et al. (multiplicity): use rank and set metrics, never l2 alone (l2 exceedance 0% vs top-3 Jaccard 24-49%); dual-seed protocol R=5; report stable-core features; K-Means backgrounds stabilize but shift the estimand, so judge the shared-background mitigation against the full-background reference; one GMSC config took ~24 h on an L40S, so size compute for Colab.
- Parashar et al.: the report read the Aug 2024 ResearchSquare preprint, which differs from the Evolutionary Intelligence version (abstract only). Do not cite the 100% agreement (about 1.3 points per cluster; best of 90 pairs chosen post hoc).
- Hwang et al., SHAP-based Explanations are Sensitive to Feature Representation (FAccT 2025, new row T50): fix feature representation across explainers; robustness check on binning/encoding of child age (b19). A design factor, not a gap.
- Corrections: arXiv page for Hwang (multiplicity) lists Rosenblatt before Whang (kept) and shows no venue; NeurIPS 2026 is per the PDF.

## Problem statement (paste-ready)
Post hoc feature-attribution methods (SHAP, LIME and Integrated Gradients) are widely used to explain machine-learning models on health-survey data, yet published BDHS and DHS studies typically report a single explainer on a single winning model. The disagreement literature shows that explainers often conflict (Krishna et al., 2024), but it does not separate genuine conflict between methods from each method's own run-to-run and retraining variability, and it has not been tested on clustered survey data. For child stunting on BDHS 2022, where predictive signal is modest (AUROC about 0.63-0.64 in our cluster-grouped pilot), it is therefore unknown whether the reported "most important predictors" reflect the data or the choice of model and explainer. Mitigations have been proposed on benchmark data, but none has been evaluated in this setting. This thesis (1) measures SHAP-LIME disagreement on logistic regression, random forest and MLP models, and SHAP-LIME-IG disagreement on the differentiable models, each relative to a noise floor from repeated explainer runs and retrained models, calibrated against randomized null rankings; and (2) tests whether three simple mitigations reduce disagreement beyond that floor while preserving deletion-based faithfulness.

## Research questions
1. SHAP-LIME disagreement on LR, RF, MLP, and how much exceeds each explainer's noise floor?
2. IG vs SHAP/LIME on the differentiable models, and sensitivity to the IG baseline?
3. Does disagreement change with predictor set (Arm A vs Arm B with maternal height) or model type?
4. Do source-variable aggregation, shared background/baseline and rank consensus reduce excess disagreement while keeping faithfulness above random deletion?

## Guardrails
- Do not claim "first"; say "noise-calibrated, compatibility-aware comparison on clustered health-survey data".
- Never write IG on random forests.
- Say "cluster-aware validation", not "accounts for survey design", unless fits use survey weights.
- Never judge rank agreement with an l2-style magnitude metric alone.
- Do not cite Parashar's 100% agreement.
- Update the AUROC figure after the feature set is locked.
- Unread lead: arXiv 2311.10811 (fetch rate-limited).
