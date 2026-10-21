# Pilot 1 — validation report (my notebook vs Codex implementation, plus triage of the Codex audit)

Compared: `results/protocol_pilot_outputs` (my notebook, PILOT, S0, run on real BDKR81FL) vs `results/codex_outputs` (Codex re-implementation from Prompt A v1, PILOT, S0). Both ran in the same Colab environment (scikit-learn 1.6.1, shap 0.52.0, torch 2.11 CPU, python 3.13). Only summary tables were compared; the two attribution files were not opened.

## 1. Did the two implementations agree?

| Check | Result |
|---|---|
| Cohort n / stunted / weight sum | **identical** (4105 / 966 / 4104.52) |
| Fold-assignment SHA-256, outcome SHA-256 | **identical** (`8a4f5168…`, `ee4c36ab…`) |
| LR and RF AUROC, every fold and seed | **identical to 16 digits** |
| LR and RF: every SHAP, LIME and IG floor, cross-method similarity, null N1 | **identical to ≥12 digits** (e.g. LR SHAP-vs-LIME Spearman cross = 0.7321793406593408 in both) |
| Explained children (20 per fold) | identical (follows from the identical LR/RF attributions) |
| Noise-control ranks, LR and RF | identical (9 / 12 / 10; 9 / 10) |
| **MLP** | **differs**: mean weighted AUROC 0.598 (mine) vs 0.593 (Codex); SHAP-vs-LIME Spearman cross 0.496 vs 0.465; kappa 0.42 vs 0.39 |
| Null N2 | differs in the 3rd decimal for MLP only (follows from the MLP difference) |
| Gate outcome pattern | **identical**: everything passes except G5 |

**Cause of the MLP difference — my specification error.** Prompt A said "per-epoch order = torch.randperm(n, generator=torch.Generator().manual_seed(seed))". Codex followed it literally, re-seeding inside each epoch, so all 90 epochs used the same row order (it flagged this itself, DISCREPANCIES #18). My notebook creates the generator once. The notebook is the intended behaviour; the prompt is fixed in v2.

What this does and does not show: both implementations were built from the same specification, so agreement shows that the code does what the spec says. It does not show that the spec is scientifically right. The audit findings below are about the spec.

The size of the MLP gap is itself informative. A shuffling detail moves MLP agreement numbers by about 0.03 in Spearman, similar to the MLP retraining floor.

## 2. Pilot results (my notebook, S0, 100 explained children; interval = conditional bootstrap)

Spearman similarity. Ceiling = highest cross-method similarity the explainers' own noise allows; κ = (cross − null N2) / (ceiling − null N2).

| Model | Pair | Cross | Ceiling | Null N2 | κ (95% CI) | Excess disagreement |
|---|---|---|---|---|---|---|
| LR | SHAP–LIME | 0.73 | 0.92 | 0.43 | 0.62 (0.58–0.66) | 0.19 |
| LR | SHAP–IG | 0.93 | 0.94 | 0.53 | 0.97 (0.96–0.98) | 0.01 |
| LR | LIME–IG | 0.77 | 0.97 | 0.44 | 0.63 (0.59–0.66) | 0.20 |
| RF | SHAP–LIME | 0.69 | 0.89 | 0.50 | 0.49 (0.45–0.53) | 0.20 |
| MLP | SHAP–LIME | 0.50 | 0.87 | 0.23 | 0.42 (0.38–0.45) | 0.38 |
| MLP | SHAP–IG | 0.67 | 0.92 | 0.28 | 0.62 (0.56–0.66) | 0.24 |
| MLP | LIME–IG | 0.38 | 0.95 | 0.13 | 0.30 (0.26–0.35) | 0.57 |

- Disagreement between explainers is clearly larger than their own run-to-run noise, for every pair except SHAP–IG on logistic regression. That pair is near-identical because, for a linear model, the two methods are almost the same quantity.
- For SHAP–LIME, κ falls from LR (0.62) to RF (0.49) to MLP (0.42), and excess disagreement is largest for the MLP (0.38 vs about 0.19–0.20). With one pilot on 100 children this is a pattern to test in the FULL run, not a finding.
- MLP retraining noise (Spearman 0.76 SHAP, 0.82 LIME, 0.68 IG) is larger than explainer-seed noise (0.84, 0.91, 1.0). For the MLP, retraining is the bigger source of instability. The MLP itself is weak (weighted AUROC 0.55–0.65 depending on the fold).
- These intervals are far too narrow to take at face value: they resample only the 100 selected children and hold the fitted models fixed. The notebook now also writes `kappa_by_fold.csv`.

## 3. Gate G5 (negative-control noise column) failed in both implementations

Noise column median rank among 15 variables: 8–12 (threshold ≥ 11); importance share 0.27–0.87 of the uniform share across the two runs (threshold ≤ 0.5). It failed for LR-SHAP, LR-IG, RF-SHAP, RF-LIME, MLP-SHAP, MLP-IG.

How I read it: the noise column ranks about 9th of 15, i.e. just below the middle, because several real S0 variables carry almost no signal (AUROC ≈ 0.62). This tests whether the fitted model leans on noise, not whether an explainer is correct. MLP-IG gives noise 0.76–0.87 of an average variable's share, so the MLP is fitting noise.

Do not loosen the threshold to make this pass. If you change G5 before the FULL run, record it as a post-pilot protocol revision, state why, and keep the pilot gate report as it was. A clean alternative is to report the failure as a limitation.

## 4. Triage of the Codex audit (Codex audited its own `codex_pilot.py`; I checked each point against my notebook)

| # | Codex finding | Applies to my notebook? | Action (notebook v2) |
|---|---|---|---|
| 1 | v116 = 15 merged with missing | **Yes** (I copied the earlier pilot's handling; ≈22 children) | Code 15 kept as its own level; only 97 → missing |
| 2 | Ties and all-zero vectors can drive rank metrics; zero vectors score inconsistently | Partly (no all-zero vectors seen in tests) | Added `tie_diagnostics.csv` and gate G8; metrics unchanged |
| 3 | κ can leave [0,1] | **Yes** | Left unclipped, relabelled a ceiling ratio, added `kappa_outside_0_1` |
| 4 | Gate scopes can vanish without a FAIL | **Yes** (`all()` on an empty table is True) | Row-count checks for G2, G5, G6, G7 |
| 5 | Library versions not pinned | **Yes** (and my `lime` version printed `n/a`) | Versions now recorded for shap, lime, captum; a `pin_command` is written to `run_metadata.json` |
| 6 | Permutation count is not N_PERM | **Yes, confirmed in shap source**: `max_evals // (2·n_varying + 1)` = 281 // 29 = **9**, not 10 | `max_evals = N_PERM·(2p+1)` |
| 7 | caseid → cluster containment not checked | Not changed. In DHS the cluster number is part of `caseid`, so a mother cannot span clusters | None |
| 8 | Bootstrap CI conditional on chosen children and folds | **Yes** | Labelled conditional; added `kappa_by_fold.csv` |
| 9 | Runtime gate is a rough projection | Accepted | Codex projected 0.44 h and took 0.44 h (1591 s) |

Also from Codex's DISCREPANCIES.md: N2 depended on which method is called A. It is now symmetrised.

Findings 1, 6 and the N2 change alter the numbers slightly, so the pilot should be re-run once with notebook v2 before anything is quoted.

## 5. Design concerns that remain (Codex raised them; I agree; none is a bug)

- LIME reports raw surrogate weights, SHAP reports probability contributions, and IG reports path attributions. Part of "disagreement" is a definitional gap. A contribution-scaled LIME is a follow-up.
- The three explainers use different reference constructions (50 background rows for SHAP, local sampling for LIME, a single baseline for IG). This is a *source* of disagreement, and mitigation M2 (shared reference) should test it.
- Summing dummy-level attributions is not the grouped Shapley value; the TreeSHAP check (Spearman 0.93 vs permutation SHAP) is a consistency check, not a proof.
- Selecting one child per cluster gives a cluster-balanced sample, not a survey-representative one.
- Class-balanced training means the explained probabilities are not calibrated risks.
- The pilot outputs contain child-level outcomes, predictions and attributions keyed by fold and position. Without the source file and code they cannot be linked, but do not post them publicly.

## 6. Suggested next steps (in order)

1. Re-run notebook v2 in PILOT mode (about 30–40 min on Colab). Expect small changes to every number.
2. Re-run Codex with Prompt A v2 and repeat the comparison; the MLP rows should now match.
3. Decide how to handle G5 before FULL (keep as a limitation, or a documented revision).
4. Then run FULL (40 children per fold) with the pinned library versions from the v2 run's metadata.
