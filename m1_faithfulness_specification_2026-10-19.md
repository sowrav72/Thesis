# M1 (shared reference) and deletion-faithfulness: specification v2 (19 Oct 2026)

Status: **specification only. Nothing in this document has been run.** It is frozen before any M1 code is run on the data; changes after results are seen must be logged as deviations.

v2 changes (made before any M1 code existed, after the request for realistic rather than artificial inputs): (i) deletion-faithfulness is now primarily **conditional (realistic) deletion** with neighbour rows, marginal deletion is secondary; (ii) realism diagnostics added; (iii) reference size fallback raises K for all explainers together; (iv) multiplicity uses Bonferroni intervals; (v) marginal deletion reference rows 100 and random orders 30 (compute); (vi) baseline-averaged IG in M1 and C1 uses 200 steps per baseline (M0 keeps 100 to reproduce the main run) after a pre-run numerical check showed that real-child baselines need more steps for the per-baseline completeness error to stay well inside the gate, and the completeness error of the *averaged* attribution is checked directly; (vii) **interpretation amendment, made before any result of this notebook was seen** (after an external review): M1 − M0 differs from M0 in more than sharing (reference size, LIME's reference, IG's baseline type), so the C1 control carries the mechanism claim. The numeric decision rule is unchanged (M1 − M0, Spearman Δ ≥ 0.05, adjusted interval > 0, faithfulness preserved), but every verdict now also states whether M1 − C1 has an adjusted interval above 0 ("sharing effect confirmed") or not ("reduction not attributable to sharing"). C1 is described precisely: SHAP keeps B, identical to M1; LIME and IG get independent draws B′ and B″; B, B′, B″ are three different draws, so no pair of explainers shares a reference. M0 → C1 is the effect of reference type and size; C1 → M1 is the effect of sharing. Everything below that reports a result is a *plan*; in the proposal it appears as "planned work" until the run exists.

## 1. Question and hypothesis

RQ3: does giving SHAP, LIME and IG the **same reference distribution** reduce their disagreement on the same fitted models and the same children, without making the explanations less faithful to the model?

Motivation from the FULL run (measured, not assumed): by default the three explainers use different references (SHAP: 50 fixed training rows; LIME: the full training fold; IG: the training mean of the encoded inputs). SHAP's own ranking changes with the 50-row draw alone (Spearman 0.85–0.90), and IG changes with its baseline (0.75 LR, 0.68 MLP). So part of the measured disagreement may come from configuration, not from the methods themselves.

Hypothesis (directional, may fail): H_M1 — aligning the reference raises child-specific agreement, most for pairs involving LIME and for the MLP. Residual disagreement after alignment is attributed to method differences (LIME's local surrogate and kernel, IG's path integral, Shapley averaging), not to the reference.

What M1 cannot do: it aligns the *reference distribution*, not the *estimand*. LIME's surrogate coefficients, SHAP's Shapley values and IG's path attributions remain different quantities; we compare only importance rankings and normalised magnitudes (|attribution|), as in the main protocol.

## 2. Arms

| Arm | SHAP | LIME | IG |
|---|---|---|---|
| **M0 default** (recomputed in the same run) | background = 50 training rows B0 (draw seed SEED_BG + fold), as in v3.1.1 | LimeTabularExplainer on the full training fold | baseline = training mean of encoded inputs |
| **M1 shared** | background = B_r | LimeTabularExplainer on **B_r** as `training_data` | average of signed IG over **all 50 baselines in B_r** (each baseline = one encoded real row; 100 Gauss–Legendre steps each) |
| **C1 control: independent references for LIME and IG (SHAP keeps B)** | B_r | independent 50-row draw B'_r | independent 50-row draw B''_r |

- B_r: 50 rows drawn without replacement from the training fold's imputed rows, R_B = 5 draws. **B_0 is the default draw of the main run** (seed SEED_BG + fold); B_1…B_4 use seed SEED_BG + 1000·r + fold. C1 draws B'_r and B''_r with seeds offset by +100 and +200 from the B_r seeds, so the three references differ for every r.
- K = 50 is the primary size because it equals the default SHAP background, so **SHAP in M1 with r = 0 is identical to SHAP in M0**; at r = 0 any change comes from LIME and IG alone, and r = 1…4 add the effect of a different shared draw. K = 200 is an optional sensitivity run (SHAP cost grows about linearly with K).
- Realism of references: every reference row in B_r, B'_r, B''_r and in the deletion sets is a **real child from the training fold** (no synthetic or averaged rows). The default IG baseline of M0, the training mean of the encoded inputs, is *not* a realisable child (fractional dummy values); it is kept in M0 only so that M0 reproduces the FULL run, and M1 replaces it with 50 real baselines. The sensitivity baseline `IG_medmode` of the main run (median numeric, modal categories) is also realisable. LIME's own perturbations (independent draws per variable) are unrealistic by construction and are not changed.
- IG averaging: signed attributions are averaged over baselines first, then summed over the dummy columns of each variable, then |·| is taken (same pipeline as primary IG). This is an expected-attribution form, not "expected gradients" (alpha is not sampled).
- Why C1: without it, a rise in agreement could come from "everything now uses a 50-row reference" rather than from sharing the *same* rows. M1 minus C1 isolates the effect of sharing.
- Models: the same fitted models as the main run (training seed TS[0]); LR, RF (SHAP and LIME only), MLP (all three). Same 200 explained children (40 per fold, one per cluster). No retraining, so M1 does not re-estimate the T-axis floor.
- Explainer seeds: R_E = 3 per arm and B draw (C is a mean over seed pairs, so fewer pairs only add variance, not bias). Permutation SHAP N_PERM = 10, LIME 5,000 samples, IG 100 steps per baseline: unchanged from the main run.

## 3. Primary outcome (decided now, before any M1 run)

For each model × pair (7 cells: LR SHAP–LIME, SHAP–IG, LIME–IG; RF SHAP–LIME; MLP SHAP–LIME, SHAP–IG, LIME–IG) and each explained child i, with Spearman on |attribution|:

  **Δ_i = (C_i^M1 − N2_i^M1) − (C_i^M0 − N2_i^M0)**

where C_i is the child's cross-method similarity averaged over explainer-seed pairs (and over B draws r for M1), and N2_i is the child's null similarity to other children in the same fold under the same arm. Using C − N2 (child-specific agreement above the cross-child baseline) guards against "agreement" that arises only because explanations become more generic across children.

Reported: mean Δ with a paired bootstrap 95% CI over children (conditional on fitted folds and selected children; between-fold and between-B-draw spread reported next to it); the same for the other three metrics (1 − TV, Jaccard@5, RBO) as secondary; per-B-draw Δ so the effect can be seen not to hinge on one draw.

**Decision rule per cell** (family of 7 cells; the decision interval is the Bonferroni-adjusted bootstrap interval at level 1 − 0.05/7, which is more conservative than Holm; unadjusted 95% intervals are also reported): "disagreement reduced" if mean Δ ≥ 0.05, the adjusted interval excludes 0, **and** the faithfulness criteria of Section 4 hold for both explainers in the pair. The 0.05 threshold is a practical-size choice (it equals the gate margin used for floors above the null in the main protocol), not a statistical result. "Increased" if mean Δ ≤ −0.05 with the adjusted interval excluding 0. Otherwise "no clear change". All three outcomes are reportable; none invalidates the title.

Secondary (not decision-bearing): excess disagreement and κ per arm. These are **not like-for-like** across arms: M0 has a background axis only for SHAP, M1 for all three explainers, and M1 has no retraining axis. They are reported with floors on the E-axis (and background axis where defined) and labelled accordingly.

## 4. Deletion-faithfulness check (realistic by default)

Purpose: detect "agreement by degeneracy" (explainers converging because both became uninformative) and give each arm a model-grounded score. It is **not** a proof of correctness (see limits).

Definition, for model f (predicted probability of stunting; the same quantity that was explained), explained child x (a test-fold child), explainer e:
- Ranking: variables ordered by |attribution| from explainer-seed run 0 (the single run a user would see).
- Deleting a set S of variables means replacing x's values for S by values from other real children, in one of two schemes:
  - **Conditional (primary, realistic):** take the 50 training-fold children **closest to x on the variables that are kept** (Gower distance: numeric |difference| divided by the 5th–95th percentile range, capped at 1; categorical 0/1 mismatch; mean over kept variables), and copy their values of S into x (S is copied jointly from one real child). The composite therefore keeps x's own profile on the remaining variables and borrows a plausible combination for S from children who look like x elsewhere.
  - **Marginal (secondary):** replace S jointly by the values of each of 100 real training children (the deletion reference set R, disjoint from every B), average f over the 100 composites. This is closest to the Shapley value function and can favour SHAP-type attributions; composites can be implausible (see the realism diagnostics).
- For k = 1…7 (half of the 14 variables): S_k = top-k variables; f_k = mean of f over the composites; d_k = |f_k − f(x)|; score D_e(x) = mean_k d_k.
- Random baseline D_rand(x): the same score averaged over 30 random variable orders (common random numbers across arms and explainers); advantage **A_e(x) = D_e(x) − D_rand(x)**. For M0 the reverse order (least important first) is also scored as context.

Criteria per scheme, model and explainer (decision uses the **conditional** scheme; marginal is reported and a disagreement between the two schemes is stated):
- (F1) mean A_e > 0 with a 95% bootstrap CI excluding 0 (the ranking removes more prediction change than random order);
- (F2) non-inferiority: the lower 95% bound of mean(A_M1 − A_M0) is greater than −0.10 · mean(A_M0). If mean A_M0 ≤ 0 the cell is labelled "faithfulness uninformative" and cannot be called "reduced and faithful".

**Realism diagnostics (descriptive, no pass/fail):** for a sample of 8 explained children per fold and deleted sets of size 3 and 7, for both schemes: (a) the share of composite rows violating two logical constraints of the survey variables, and (b) the median Gower distance from a composite row to its nearest real training child, next to the same distance for the real explained children. Constraints (mother's age at this child's birth ≈ v012 − b19/12, with completed-year rounding): C1, v212 ≤ v012 − b19/12 + 1; C2, for first births (bord = 1), |v212 − (v012 − b19/12)| ≤ 2. The violation rate of the *real training rows* is computed first; a constraint with a baseline violation rate above 2% is dropped and the drop is reported.

Known limits of this check (state them in the thesis): the metric is magnitude-only and ignores sign; with AUROC 0.60–0.64 the models' prediction changes are small, so advantages are small in absolute terms; conditional deletion under-weights variables that are predictable from the kept ones (correlated variables share credit); and since the models lean on a noise column (gate G5 fails), "faithful to the model" includes faithfulness to some noise.

## 5. Unit tests and gates (must pass before the run is interpreted)

- U1: for LR on the **logit** output, IG averaged over B baselines equals linear SHAP w_j (x_j − mean_B x_j) summed over dummies, to 1e-8. (If this holds, the LR SHAP–IG result under M1 is close to an identity up to the sigmoid, so it is a sanity check, not evidence for M1.)
- U2: LIME on B_r constructs and explains for every fold and every B draw (no exceptions; if it fails, K is raised to 100 **for all explainers together** and the change is reported). Record LIME local R² per arm; a drop of more than 0.10 versus M0 is reported.
- U3: SHAP additivity error < 1e-3; IG completeness |delta| < 1e-2 **per baseline** (maximum over baselines) **and** for the averaged attribution (|Σ attribution − (f(x) − mean_b f(b))| < 1e-2).
- U4: M0 recomputed in this run reproduces the FULL-run cross_C (Spearman, all 7 cells) within 0.02 and the E-axis floors within 0.02; otherwise stop (pipeline mismatch).
- U5: scoring-code check on a toy model that depends on one variable only: ordering that variable first scores above the random mean, which scores above ordering it last, in both schemes. On the real models, the explainer order is not worse than the reverse order on average for any explainer in M0 (otherwise investigate).
- G-hash: fold, outcome and predictor-matrix hashes as in v3.1.1; pinned library versions.
- G-time: a timed probe projects total cost; **hard cap 3 h on Colab**; fallback in order: R_B 5 → 3, then drop C1 for RF/LR, never drop M0 or M1.

## 6. Data-leakage and design checks

- B_r, B'_r, B''_r, R come from the training fold only; the explained children and fitted-model test folds are untouched. R is disjoint from every B.
- Nothing about M1 is tuned on the explained children; the thresholds above are fixed here.
- The protocol (main run) was developed over three pilots on the same data; M1 is the first run of this module. Report as "pre-specified before the M1 run", disclose the history of the main protocol, and log every post-hoc change.
- Multiplicity: 7 cells × 4 metrics; only Spearman Δ in 7 cells is decision-bearing (Bonferroni); the rest is descriptive.

## 7. Claims allowed after the run

- May say (if the data support it): "in this setting, aligning the reference distribution changes child-specific agreement by Δ (95% CI …) for pair X on model Y; faithfulness [was / was not] preserved under the deletion check".
- May not say: "reduces disagreement" in general; that explanations became "more correct"; anything about causes of stunting; that M1 is new (reference/baseline sensitivity of SHAP, IG and LIME is already documented in the literature, to be cited only from the verified matrix); anything about RF and IG (not applicable).
- The conservative reading to state in the abstract: M1 is a configuration-alignment test, and the part of disagreement that survives it is reported as method-intrinsic *for these settings*.

## 8. Cost, scope and tiers

Estimated from the main run (measured work 0.46 h for LR, RF and MLP with R_E = 5, R_T = 5 and the noise control): M1 needs 3 arms × R_B = 5 draws × R_E = 3 seeds of SHAP and LIME per model and fold, plus averaged IG over 50 baselines, plus the faithfulness scoring (about 100 orderings × 7 sizes × 150 composite rows per child and model). The projection is **not yet measured**; the timed probe in Section 5 decides, with the 3 h cap.

- **Minimum thesis:** arms M0, M1, C1 (C1 may be reduced as in G-time), primary outcome Δ in the 7 cells, deletion check F1/F2, unit tests U1–U5.
- **Conference paper:** add M2 (rank consensus across explainers, judged by stability and deletion-faithfulness, **not** by closeness to its own inputs, which would be circular), the K = 200 sensitivity, the averaged-over-seeds ranking sensitivity, sign-agreement table, and Arm B (maternal height v438, after advisor approval).
- **Optional:** greedy-oracle deletion order, other outcomes or survey rounds, larger networks or GPU-heavy runs on university hardware.

## 9. Timeline (to 25 Oct)

- 19 Oct: this specification frozen (needs your sign-off).
- 20 Oct: implement the M1 notebook (copy of v3.1.1 plus M1 cells), smoke-test on synthetic data in the sandbox as before; optional independent Codex implementation of M1 and the faithfulness score for cross-checking.
- 21 Oct: Colab run (probe first, then FULL).
- 22 Oct: results triage against Section 3–5 rules; write the results table.
- 20–24 Oct in parallel: proposal text and slides. If M1 is not finished by 23 Oct, the draft states it as planned work, with this document as the plan.
