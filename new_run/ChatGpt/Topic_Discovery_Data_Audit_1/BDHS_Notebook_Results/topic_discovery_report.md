# BDHS 2022 Child Recode — Topic Discovery and Data Audit

**Run ID:** BDHS0-RUN-20261107T152503Z-751bfb20  
**Experiment configuration ID:** BDHS0-CFG-f22330f3af25031e  
**Run time (UTC):** 2026-11-07T15:25:03.576219+00:00  
**Notebook version:** 0.2.2  
**Decision status:** No thesis outcome selected or frozen.

## 1. Dataset verification

- Input: /content/drive/MyDrive/BDHS/BDKR81DT/BDKR81FL.DTA
- File size: 12,160,116 bytes
- SHA-256: df91e8988c6a6522b71860bb5d9f3fdfb6210ee880b0c1d214569d78096a63fa
- Shape: 8,784 rows × 1,238 columns
- Stata file label: not supplied
- v000 values: BD8
- v007-derived year: 2022
- Expected BDHS 2022 Child Recode checks passed: **True**

The check uses v007 label/year, v000 Bangladesh-like country/phase code, and at least two child-recode label markers. Filename is not proof; this is not external dataset certification.

## 2. Candidate outcomes considered

| candidate_outcome | status | construction_rule | eligibility_restriction |
| --- | --- | --- | --- |
| stunting | computed for audit | Stunted if label-verified height-for-age z-score < -2 SD (score < -200); HAZ bounds [-600,+600] are plausibility limits. | Living age 0-59 in the provisional known-hw13 cohort excluding only 'no measurement found'; use valid HAZ and indicator-specific plausibility bounds. Reconcile with FR386. |
| wasting | computed for audit | Wasted if label-verified weight-for-height z-score < -2 SD (score < -200); WHZ bounds [-500,+500] are plausibility limits. | Living age 0-59 in the provisional known-hw13 cohort excluding only 'no measurement found'; use valid WHZ and indicator-specific plausibility bounds. Reconcile with FR386. |
| underweight | computed for audit | Underweight if label-verified weight-for-age z-score < -2 SD (score < -200); WAZ bounds [-600,+500] are plausibility limits. | Living age 0-59 in the provisional known-hw13 cohort excluding only 'no measurement found'; use valid WAZ and indicator-specific plausibility bounds; do not require height measurement. Reconcile with FR386. |
| fever | computed for audit | Yes to verified fever question; response codes read from value labels, never hard-coded. | Provisional living children age 0-59 months; verify exact BDHS 2022 questionnaire universe and whether the item is asked for every eligible child before treating this as final. |
| diarrhea | computed for audit | Two-week diarrhea indicator: combine every value-labeled affirmative category (including 'yes, last 24 hours' and 'yes, last two weeks') as Yes; retain the single labeled No category as No; don't know remains missing. Codes are read from value labels, never hard-coded. | Provisional living children age 0-59 months; verify exact BDHS 2022 questionnaire universe and whether the item is asked for every eligible child before treating this as final. |
| ari_symptoms | TODO / REVIEW — not computed | TODO/REVIEW: verify BDHS 2022 report/questionnaire definition and all cough/breathing codes; no formula assumed. | Living children age 0-59 months; verify questionnaire universe. |
| child_anemia | TODO / REVIEW — not computed | Compute only if metadata exposes one anemia-status field with labeled anemic/non-anemic categories; otherwise review measure, adjustment, cutoff, and standard. | Living children age 6-59 months with valid anemia status/measurement. |
| full_age_appropriate_immunisation | TODO / REVIEW — not computed | TODO/REVIEW: verify national schedule, eligible age, doses, information source, and exact codes before creating a label. | Initial audit denominator 12-23 months; team must confirm this against BDHS 2022 documentation. |
| mortality_related | computed for audit | Descriptive death status only if b5 labels are verified. Not an ordinary binary target due differing exposure time/censoring. | KR birth records with verified alive status; time at risk must be addressed. |

## 3. Anthropometry measurement-status audit

| status_group | n | percent_of_living_under5 | living_under5_reference_n | evidence |
| --- | --- | --- | --- | --- |
| measured | 4123 | 48.46027268453221 | 8508 | Aggregate statuses; small categories pooled. |
| no measurement found | 4282 | 50.3291020216267 | 8508 | Aggregate statuses; small categories pooled. |
| other recognized statuses pooled | 103 | 1.2106252938410906 | 8508 | Aggregate statuses; small categories pooled. |
| missing/unclassified | 0 | 0.0 | 8508 | Aggregate statuses; small categories pooled. |

Anthropometry eligibility is currently a provisional file-defined cohort of living children aged 0–59 months with a recognized hw13 status other than “no measurement found in household”; it is not yet the established DHS eligible denominator. DHS z-scores are stored at 100x: HAZ -600 to +600, WAZ -600 to +500, WHZ -500 to +500; the undernutrition target is score < -200. These are plausibility filters, not proof of valid measurement. Out-of-range special values are excluded. Use indicator-specific score availability rather than requiring hw13=Measured for every index: valid WAZ can occur when hw13=Other because WAZ needs weight and age, not height. Verify this interpretation against BDHS documentation and reconcile the provisional denominator with FR386. The measured subsample may be selected.

### Published anthropometry denominator comparison

FR386 Table C.8 reports 4,420 children eligible for anthropometry: 4,199 whose mothers were interviewed and 221 whose mothers were not interviewed but were in the household. Its valid-data percentages for the interviewed subgroup are 97.2% (HAZ), 97.2% (WHZ), and 98.5% (WAZ). The KR file represents children of interviewed women, so the 4,199 subgroup is the closer published comparison; the 221 not-interviewed-but-in-household subgroup is shown only to explain the full 4,420 denominator and is not merged into the KR cohort. The KR file's provisional hw13 status cohort is computed separately, and valid-score counts are split by hw13 status to expose indicator-specific exceptions. The differences are **unresolved**; the notebook does not assume maternal interview status fully explains them.

| quantity | n | source | interpretation |
| --- | --- | --- | --- |
| KR living children age 0-59, b5=Yes | 8508 | Private KR file, labels verified | Reference universe in this recode. |
| KR hw13 measured | 4123 | Private KR file, hw13 labels | Measured-status count; not full eligible denominator. |
| KR provisional known-hw13 cohort excluding no-measurement-found | 4226 | Private KR file, operational proxy | Candidate denominator; not asserted equal to FR386. |
| KR hw13 no measurement found in household | 4282 | Private KR file, hw13 labels | Separate status group; excluded from provisional cohort. |
| FR386 C.8 total eligible for anthropometry | 4420 | Bangladesh DHS 2022 Final Report, Table C.8 | Published denominator; source/recode scope may differ. |
| FR386 C.8 mothers interviewed | 4199 | Bangladesh DHS 2022 Final Report, Table C.8 | Closest published subgroup for KR comparison; not presumed identical. |
| FR386 C.8 mother not interviewed but in household | 221 | Bangladesh DHS 2022 Final Report, Table C.8 | Included in published total; KR representation requires review. |
| KR cohort minus FR386 interviewed-mother count | 27 | Calculated aggregate difference | Unresolved; no cause assumed. |
| FR386 total minus KR provisional cohort | 194 | Calculated aggregate difference | Unresolved; do not attribute solely to maternal interview status. |

| candidate_outcome | kr_provisional_cohort_n | kr_valid_score_n | kr_valid_score_n_hw13_measured | kr_valid_score_n_hw13_other_status | kr_valid_pct_of_provisional_cohort | fr386_c8_valid_pct_interviewed_mothers | difference_percentage_points | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stunting | 4226 | 4105 | 4105 | 0 | 97.13677236157123 | 97.2 | -0.06322763842877066 | Rough aggregate comparison only; denominator/scope unresolved; indicator-specific valid scores govern. WAZ may be valid without the composite hw13 measured status. |
| wasting | 4226 | 4104 | 4104 | 0 | 97.1131093232371 | 97.2 | -0.08689067676290563 | Rough aggregate comparison only; denominator/scope unresolved; indicator-specific valid scores govern. WAZ may be valid without the composite hw13 measured status. |
| underweight | 4226 | 4158 | 4116 | 42 | 98.3909133932797 | 98.5 | -0.10908660672029669 | Rough aggregate comparison only; denominator/scope unresolved; indicator-specific valid scores govern. WAZ may be valid without the composite hw13 measured status. |

The Table C.8 percentages are an external comparison only. Similar percentages do not establish identical analytic universes. See [FR386 Table C.8](https://www.dhsprogram.com/pubs/pdf/FR386/FR386.pdf).

## 4. Outcome-quality results

| candidate_outcome | status | eligible_n | valid_outcome_n | missing_outcome_pct_of_eligible | positive_n | negative_n | positive_prevalence | class_imbalance_ratio_larger_over_smaller | quality_flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stunting | computed for audit | 4226 | 4105.0 | 2.86% | 966.0 | 3139.0 | 0.2353 | 3.249482401656315 | outcome missing for at least one eligible observation |
| wasting | computed for audit | 4226 | 4104.0 | 2.89% | 483.0 | 3621.0 | 0.1177 | 7.496894409937888 | outcome missing for at least one eligible observation |
| underweight | computed for audit | 4226 | 4158.0 | 1.61% | 946.0 | 3212.0 | 0.2275 | 3.395348837209302 | outcome missing for at least one eligible observation |
| fever | computed for audit | 8508 | 8487.0 | 0.25% | 2630.0 | 5857.0 | 0.3099 | 2.226996197718631 | outcome missing for at least one eligible observation |
| diarrhea | computed for audit | 8508 | 8485.0 | 0.27% | 410.0 | 8075.0 | 0.0483 | 19.695121951219512 | outcome missing for at least one eligible observation |
| ari_symptoms | TODO / REVIEW — not computed | 8508 | not available | not estimable | not available | not available | not estimable | not available | definition pending human review |
| child_anemia | TODO / REVIEW — not computed | 7593 | not available | not estimable | not available | not available | not estimable | not available | definition pending human review |
| full_age_appropriate_immunisation | TODO / REVIEW — not computed | 1636 | not available | not estimable | not available | not available | not estimable | not available | definition pending human review |
| mortality_related | computed for audit | 8784 | 8784.0 | 0.00% | 276.0 | 8508.0 | 0.0314 | 30.82608695652174 | mortality target has unequal follow-up/censoring; not a standard binary task |

No universal missingness or balance cutoffs are asserted. Thin classes are flagged relative to the requested fold count and then checked by cluster support.

## 5. Leakage findings

Leakage classifications use labels and target construction, not correlations. See leakage_audit.csv for variable-level evidence and actions.

| candidate_outcome | derived_leakage | direct_leakage | legitimate_predictor | proxy_risk | uncertain |
| --- | --- | --- | --- | --- | --- |
| ari_symptoms | 0 | 0 | 43 | 60 | 57 |
| child_anemia | 0 | 0 | 44 | 11 | 12 |
| diarrhea | 0 | 1 | 43 | 101 | 10 |
| fever | 0 | 1 | 43 | 122 | 10 |
| full_age_appropriate_immunisation | 0 | 0 | 44 | 0 | 18 |
| mortality_related | 0 | 1 | 43 | 10 | 10 |
| stunting | 5 | 1 | 37 | 12 | 17 |
| underweight | 5 | 1 | 37 | 12 | 17 |
| wasting | 5 | 1 | 37 | 12 | 17 |

## 6. Survey and cluster structure

{
  "psu_strata_candidate_labels_and_distinct_counts": {
    "v001": {
      "label": "cluster number",
      "role_under_review": "cluster / PSU candidate",
      "label_check": "verified",
      "distinct_nonmissing_values": 674
    },
    "v021": {
      "label": "primary sampling unit",
      "role_under_review": "PSU candidate",
      "label_check": "verified",
      "distinct_nonmissing_values": 674
    },
    "v022": {
      "label": "sample strata for sampling errors",
      "role_under_review": "strata candidate",
      "label_check": "verified",
      "distinct_nonmissing_values": 16
    },
    "v023": {
      "label": "stratification used in sample design",
      "role_under_review": "strata candidate",
      "label_check": "verified",
      "distinct_nonmissing_values": 16
    }
  },
  "psu_candidate_aggregate_structure": {
    "v001": {
      "cluster_count": 674,
      "children_per_cluster_median": 13.0,
      "children_per_cluster_max": 29
    },
    "v021": {
      "cluster_count": 674,
      "children_per_cluster_median": 13.0,
      "children_per_cluster_max": 29
    }
  },
  "verified_psu_candidates": [
    "v001",
    "v021"
  ],
  "v001_v021_values_identical_if_both_label_verified": true,
  "v001_v021_values_differ_if_both_label_verified": false,
  "v001_v021_partitions_identical_if_both_label_verified": true,
  "team_confirmed_psu_variable": null,
  "group_variable_used_for_pilot": null,
  "grouping_partition_used_for_pilot": "joint v001+v021 equivalence partition",
  "grouping_provisional_pending_survey_documentation": true,
  "group_resolution": "Provisional grouped feasibility: v001/v021 labels are verified and partitions identical. Joint partition avoids choosing a canonical PSU; human confirmation of survey-design meaning is still required before final interpretation.",
  "group_validation_ready": true,
  "group_validation_gate": "Provisional grouped feasibility: v001/v021 labels are verified and partitions identical. Joint partition avoids choosing a canonical PSU; human confirmation of survey-design meaning is still required before final interpretation.",
  "verified_strata_variables": [
    "v022",
    "v023"
  ],
  "v022_v023_values_identical_if_both_label_verified": true,
  "v022_v023_partitions_identical_if_both_label_verified": true,
  "verified_sampling_weight_variable": "v005",
  "verified_mother_key_components": [
    "v001",
    "v002",
    "v003"
  ],
  "verified_child_line_identifier": "b16",
  "verified_birth_record_key_components": [
    "caseid",
    "bidx"
  ],
  "birth_record_key_complete": true,
  "birth_record_key_duplicate_rows": 0,
  "birth_record_key_unique": true,
  "mother_to_psu_nesting_by_candidate": {
    "v001": {
      "status": "structurally nested: verified mother key contains v001 and PSU partitions are identical; cross-PSU count would be tautological",
      "mothers_spanning_multiple_psus_n": null,
      "mothers_with_psu_observed_n": null,
      "mothers_spanning_multiple_psus_pct": null
    },
    "v021": {
      "status": "structurally nested: verified mother key contains v001 and PSU partitions are identical; cross-PSU count would be tautological",
      "mothers_spanning_multiple_psus_n": null,
      "mothers_with_psu_observed_n": null,
      "mothers_spanning_multiple_psus_pct": null
    }
  },
  "mother_nesting_structurally_guaranteed_by_composite_key": true,
  "cluster_count": 674,
  "children_per_cluster_median": 13.0,
  "children_per_cluster_max": 29,
  "mother_count": 7697,
  "children_per_mother_median": 1.0,
  "children_per_mother_max": 4
}

No cluster, household, mother, or child identifier values are displayed. Cluster-held-out validation runs only after the team confirms PSU and mother-key interpretation; v001/v021 partition identity is reported.

## 7. Predictive Feasibility Check

_No rows available._

Fold-level results (average precision, not trapezoidal PR-AUC): _No rows available._. Fold evaluation status and skipped-fold reasons are in signal_check_fold_audit.csv.

These are preliminary unweighted cluster-held-out screening metrics, not final performance or population estimates. Fold preprocessing is fit on training data only. AP baselines use each test-fold prevalence; see signal_check_fold_metrics.csv. Fold means are descriptive. If joint v001/v021 equivalence-partition grouping is used, results are a provisional feasibility diagnostic requiring human confirmation of survey-design meaning before final interpretation; no canonical PSU or outcome is selected.

## 8. Topic evidence matrix

| candidate_outcome | label_validity | eligible_n | valid_n | missing_n | missing_pct | positive_n | negative_n | prevalence | imbalance_ratio | leakage_evidence | cluster_support | predictability_feasibility | predictor_interpretability | literature_relevance | colab_feasibility | team_decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stunting | Metadata-checked; human definition review remains. | 4226 | 4105.0 | 121.0 | 2.863227638428774 | 966.0 | 3139.0 | 0.23532277710109623 | 3.249482401656315 | direct_leakage=1; derived_leakage=5; proxy_risk=12; legitimate_predictor=37; uncertain=17; see leakage_audit.csv. | v001: clusters=670, positive=475, negative=664 \| v021: clusters=670, positive=475, negative=664 | Not completed: Outcome definition has not been reviewed and confirmed by both researchers in cell 3. | 37 pilot fields passed; 7 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| wasting | Metadata-checked; human definition review remains. | 4226 | 4104.0 | 122.0 | 2.8868906767628966 | 483.0 | 3621.0 | 0.11769005847953216 | 7.496894409937888 | direct_leakage=1; derived_leakage=5; proxy_risk=12; legitimate_predictor=37; uncertain=17; see leakage_audit.csv. | v001: clusters=670, positive=341, negative=666 \| v021: clusters=670, positive=341, negative=666 | Not completed: Outcome definition has not been reviewed and confirmed by both researchers in cell 3. | 37 pilot fields passed; 7 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| underweight | Metadata-checked; human definition review remains. | 4226 | 4158.0 | 68.0 | 1.609086606720303 | 946.0 | 3212.0 | 0.2275132275132275 | 3.395348837209302 | direct_leakage=1; derived_leakage=5; proxy_risk=12; legitimate_predictor=37; uncertain=17; see leakage_audit.csv. | v001: clusters=670, positive=469, negative=663 \| v021: clusters=670, positive=469, negative=663 | Not completed: Outcome definition has not been reviewed and confirmed by both researchers in cell 3. | 37 pilot fields passed; 7 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| fever | Metadata-checked; human definition review remains. | 8508 | 8487.0 | 21.0 | 0.2468265162200282 | 2630.0 | 5857.0 | 0.3098857075527277 | 2.226996197718631 | direct_leakage=1; derived_leakage=0; proxy_risk=122; legitimate_predictor=43; uncertain=10; see leakage_audit.csv. | v001: clusters=674, positive=642, negative=674 \| v021: clusters=674, positive=642, negative=674 | Not completed: Outcome definition has not been reviewed and confirmed by both researchers in cell 3. | 43 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| diarrhea | Metadata-checked; human definition review remains. | 8508 | 8485.0 | 23.0 | 0.27033380347907854 | 410.0 | 8075.0 | 0.04832056570418385 | 19.695121951219512 | direct_leakage=1; derived_leakage=0; proxy_risk=101; legitimate_predictor=43; uncertain=10; see leakage_audit.csv. | v001: clusters=674, positive=268, negative=674 \| v021: clusters=674, positive=268, negative=674 | Not completed: Outcome definition has not been reviewed and confirmed by both researchers in cell 3. | 43 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| ari_symptoms | Pending; no outcome constructed. | 8508 | not available | not available | not available | not available | not available | not available | not available | direct_leakage=0; derived_leakage=0; proxy_risk=60; legitimate_predictor=43; uncertain=57; see leakage_audit.csv. | Not assessed; PSU/outcome pending. | Not completed: Not run. | 43 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| child_anemia | Pending; no outcome constructed. | 7593 | not available | not available | not available | not available | not available | not available | not available | direct_leakage=0; derived_leakage=0; proxy_risk=11; legitimate_predictor=44; uncertain=12; see leakage_audit.csv. | Not assessed; PSU/outcome pending. | Not completed: Not run. | 44 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| full_age_appropriate_immunisation | Pending; no outcome constructed. | 1636 | not available | not available | not available | not available | not available | not available | not available | direct_leakage=0; derived_leakage=0; proxy_risk=0; legitimate_predictor=44; uncertain=18; see leakage_audit.csv. | Not assessed; PSU/outcome pending. | Not completed: Not run. | 44 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| mortality_related | Metadata-checked; human definition review remains. | 8784 | 8784.0 | 0.0 | 0.0 | 276.0 | 8508.0 | 0.031420765027322405 | 30.82608695652174 | direct_leakage=1; derived_leakage=0; proxy_risk=10; legitimate_predictor=43; uncertain=10; see leakage_audit.csv. | v001: clusters=674, positive=204, negative=674 \| v021: clusters=674, positive=204, negative=674 | Not completed: Not run. | 43 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |

The matrix reports raw quantities and qualitative evidence only; it is not a score or ranked list. No outcome is selected.

## 9. Human review status

No outcome recommendation is generated; all candidates remain for human review.

The research team must make and document the final choice after reviewing validity, feasibility, leakage, grouped support, signal, interpretability, and verified literature relevance.

## 10. Candidates pending definition review

- Mortality-related: descriptive alive/dead counts may be available, but unequal follow-up and censoring make this unsuitable as an ordinary binary prediction target without a separate survival-analysis design.
- ARI symptoms: pending verification of the BDHS 2022 wording and exact labeled coding.
- Full/age-appropriate immunisation: pending verification of Bangladesh's schedule, eligible ages, doses, and source rules.
- Child anaemia: computed only if one unique labeled status variable exists; otherwise pending measurement, adjustment, and cutoff verification.
- Any candidate with absent/mismatched labels remains pending rather than silently replaced.

## 11. Decisions requiring human confirmation

1. Confirm observed v000 country/phase values, v007 year, and expected Child Recode checks in dataset_metadata.json.
2. Review variable inventory and survey-role checks; resolve every absent or label-mismatched field.
3. For anthropometry, verify the provisional hw13 cohort, indicator-specific score availability and plausibility bounds, the < -2 SD construction, and valid scores by hw13 status (especially WAZ with hw13=Other) against BDHS 2022 documentation.
4. Review the anthropometry denominator bridge and validity comparison; the file and FR386 C.8 counts differ, and the cause remains unresolved.
5. Define prediction/measurement time and the exact information available at that time; distinguish cross-sectional classification from prospective prediction.
6. Confirm each candidate outcome definition and its candidate-specific leakage audit by both researchers before running the feasibility models.
7. Explicitly confirm the pilot is unweighted; these preliminary metrics are not population-representative estimates.
8. Decide observed-sample classification vs a population-risk estimand and whether survey weights enter the final analysis.
9. Decide age/sex availability and use. Do not automatically carry pilot exclusions into the final model.
10. Decide whether fever/diarrhea are acceptable using exact wording, reference period, and eligible universe.
11. Resolve ARI construction from the BDHS 2022 questionnaire/report and exact value labels.
12. Resolve anaemia field, age eligibility, adjustment, and cutoff/reference standard from BDHS 2022 documentation.
13. Resolve national age-appropriate immunisation schedule, age, doses, source rules, and value codes.
14. Review mortality limitations; use explicit survival/time-at-risk methods and an appropriate recode file if mortality remains in scope.
15. Review every direct, derived, proxy-risk, and uncertain row in leakage_audit.csv and approve the preliminary prediction-feasibility feature set.
16. Confirm PSU, strata, weight, mother, and child definitions; verify caseid+bidx uniquely identifies each birth record. The file shows v001/v021 and v022/v023 equivalence, but survey-design meanings still require BDHS documentation confirmation.
17. Verify literature relevance against the actual papers; keep G2 provisional until full-paper verification.
18. Record the chosen outcome, label recipe, eligibility, excluded predictors, and rationale in a dated two-person decision log before explainer experiments.

## 12. Reproducibility

- Run ID: BDHS0-RUN-20261107T152503Z-751bfb20
- Experiment configuration ID: BDHS0-CFG-f22330f3af25031e
- Configuration identity SHA-256: f22330f3af25031ec9e912c7f3a6090fe101d334b1d03cc5a19ac13cbb6fe6a1
- Dataset SHA-256: df91e8988c6a6522b71860bb5d9f3fdfb6210ee880b0c1d214569d78096a63fa
- Random seed: 20261030
- Python: 3.13.18
- Package versions: {"ipython": "7.34.0", "matplotlib": "3.10.0", "numpy": "2.4.6", "pandas": "2.2.3", "psutil": "5.9.5", "pyreadstat": "1.3.7", "scikit_learn": "1.6.1", "scipy": "1.16.3"}
- Git commit: not available
- Manifest: run_manifest.json
- Raw dataset copied to outputs: **No**
- Explainability methods used: **None**

## Sources and definition checks

- [Bangladesh DHS 2022 Final Report (FR386)](https://www.dhsprogram.com/pubs/pdf/FR386/FR386.pdf)
- [DHS Guide to Statistics](https://preview.dhsprogram.com/pubs/pdf/DHSG1/Guide_to_DHS_Statistics_DHS-7.pdf)
- [DHS Program indicator code for child vaccination](https://github.com/DHSProgram/DHS-Indicators-R/blob/main/Chap10_CH/CH_VAC.R)

Use the actual BDHS report, questionnaire, dictionary, and file labels for survey-specific definitions; general DHS code is a reference, not proof of this file's coding.


## 13. Supplied reference-file audit

```json
{
  "variable_dictionary": {
    "status": "not available",
    "expected_path": "/content/drive/MyDrive/BDHS/reference/variable_dictionary_metadata.csv"
  },
  "literature_matrix": {
    "status": "not available",
    "expected_path": "/content/drive/MyDrive/BDHS/reference/literature_matrix_hybrid_master_v3.csv"
  }
}
```

The variable dictionary comparison checks labels and value-label counts; it does not compare every code-to-text mapping. The literature matrix is a working inventory only. Its status fields are carried forward as supplied and do not independently verify paper claims, full-text coverage, or novelty.
