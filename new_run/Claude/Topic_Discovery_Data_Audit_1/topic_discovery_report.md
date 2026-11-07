# BDHS 2022 Child Recode — Topic Discovery and Data Audit

**Run ID:** BDHS0-RUN-20261107T155648Z-37903028  
**Experiment configuration ID:** BDHS0-CFG-224d6748826ef512  
**Run time (UTC):** 2026-11-07T15:56:48.994157+00:00  
**Notebook version:** 0.2.3  
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
| child_anemia | computed for audit | Compute only if metadata exposes one anemia-status field with labeled anemic/non-anemic categories; otherwise review measure, adjustment, cutoff, and standard. | Living children age 6-59 months with valid anemia status/measurement. |
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
| child_anemia | computed for audit | 7593 | 0.0 | 100.00% | 0.0 | 0.0 | not estimable | not available | outcome missing for at least one eligible observation; single observed class; one class has fewer than 5 observations; check cluster support |
| full_age_appropriate_immunisation | TODO / REVIEW — not computed | 1636 | not available | not estimable | not available | not available | not estimable | not available | definition pending human review |
| mortality_related | computed for audit | 8784 | 8784.0 | 0.00% | 276.0 | 8508.0 | 0.0314 | 30.82608695652174 | mortality target has unequal follow-up/censoring; not a standard binary task |

No universal missingness or balance cutoffs are asserted. Thin classes are flagged relative to the requested fold count and then checked by cluster support.

## 5. Leakage findings

Leakage classifications use labels and target construction, not correlations. See leakage_audit.csv for variable-level evidence and actions.

| candidate_outcome | derived_leakage | direct_leakage | legitimate_predictor | proxy_risk | uncertain |
| --- | --- | --- | --- | --- | --- |
| ari_symptoms | 0 | 0 | 4 | 60 | 57 |
| child_anemia | 0 | 1 | 4 | 12 | 10 |
| diarrhea | 0 | 1 | 4 | 100 | 10 |
| fever | 0 | 1 | 4 | 122 | 10 |
| full_age_appropriate_immunisation | 0 | 0 | 4 | 0 | 18 |
| mortality_related | 0 | 1 | 4 | 10 | 10 |
| stunting | 5 | 1 | 3 | 5 | 12 |
| underweight | 5 | 1 | 3 | 5 | 12 |
| wasting | 5 | 1 | 3 | 5 | 12 |

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

**Screen mode: exploratory.** EXPLORATORY run: not based on team-confirmed outcome, leakage, prediction-time or estimand decisions; do not use it to choose the outcome.

| candidate_outcome | model | roc_auc_mean | roc_auc_sd | average_precision_mean | average_precision_sd | folds_completed | folds_requested_for_candidate | positive_clusters | negative_clusters | eligible_valid_n_used | prevalence_baseline_for_average_precision | screen_mode | group_variable | grouping_provisional | grouping_design_confirmation_pending | runtime_seconds | status | error_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stunting | Logistic Regression | 0.5435032323532522 | 0.005587429323002758 | 0.2790248564127956 | 0.010748064923080778 | 5 | 5 | 475 | 664 | 4105 | 0.235212894763393 | exploratory | joint v001+v021 equivalence partition | True | True | 0.8089013169999362 | completed | not available |
| stunting | Random Forest | 0.5353294411847191 | 0.018853122181328893 | 0.26801251238718793 | 0.018721438249504105 | 5 | 5 | 475 | 664 | 4105 | 0.235212894763393 | exploratory | joint v001+v021 equivalence partition | True | True | 3.3523269689999324 | completed | not available |
| wasting | Logistic Regression | 0.5396845716257183 | 0.027179925630602106 | 0.13348361378446819 | 0.011839257093467672 | 5 | 5 | 341 | 666 | 4104 | 0.11762090983862199 | exploratory | joint v001+v021 equivalence partition | True | True | 0.5693064110000705 | completed | not available |
| wasting | Random Forest | 0.5342631809077314 | 0.006575771418548049 | 0.13660506726408642 | 0.0052987598025423955 | 5 | 5 | 341 | 666 | 4104 | 0.11762090983862199 | exploratory | joint v001+v021 equivalence partition | True | True | 4.586378944999979 | completed | not available |
| underweight | Logistic Regression | 0.5454945862617534 | 0.010864137048484119 | 0.2784708895831388 | 0.024901665909549536 | 5 | 5 | 469 | 663 | 4158 | 0.22748079227816134 | exploratory | joint v001+v021 equivalence partition | True | True | 0.4521764509999002 | completed | not available |
| underweight | Random Forest | 0.5345926620837294 | 0.018403449201612476 | 0.26641155589375043 | 0.021606853765179606 | 5 | 5 | 469 | 663 | 4158 | 0.22748079227816134 | exploratory | joint v001+v021 equivalence partition | True | True | 2.3974938699999484 | completed | not available |
| fever | Logistic Regression | 0.5025280655893202 | 0.011027274853584821 | 0.3104279302562075 | 0.01796305813816662 | 5 | 5 | 642 | 674 | 8487 | 0.30964754374958103 | exploratory | joint v001+v021 equivalence partition | True | True | 0.24231426599999395 | completed | not available |
| fever | Random Forest | 0.4981177435312591 | 0.0033988014102212007 | 0.31057972915589055 | 0.012065686099051414 | 5 | 5 | 642 | 674 | 8487 | 0.30964754374958103 | exploratory | joint v001+v021 equivalence partition | True | True | 3.876341721000017 | completed | not available |
| diarrhea | Logistic Regression | 0.5033103631798727 | 0.015210032533899473 | 0.05115570092907244 | 0.00806319543627228 | 5 | 5 | 268 | 674 | 8485 | 0.048273028301909285 | exploratory | joint v001+v021 equivalence partition | True | True | 0.2085724549999668 | completed | not available |
| diarrhea | Random Forest | 0.5126519139682336 | 0.016544268804851887 | 0.053591917826067835 | 0.005507780153087925 | 5 | 5 | 268 | 674 | 8485 | 0.048273028301909285 | exploratory | joint v001+v021 equivalence partition | True | True | 4.3479939569999715 | completed | not available |

Fold-level results (average precision, not trapezoidal PR-AUC): | candidate_outcome | model | fold | roc_auc | average_precision | ap_no_skill_reference_test_prevalence | test_n | test_positive_n | test_negative_n | screen_mode | group_variable | grouping_provisional | grouping_design_confirmation_pending | fold_runtime_seconds | train_test_group_overlap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stunting | Logistic Regression | 1 | 0.5420287958115184 | 0.2696934949906655 | 0.24146649810366624 | 791 | 191 | 600 | exploratory | joint v001+v021 equivalence partition | True | True | 0.22519882100004907 | False |
| stunting | Logistic Regression | 2 | 0.5463041489980877 | 0.2724129052962977 | 0.23086269744835966 | 823 | 190 | 633 | exploratory | joint v001+v021 equivalence partition | True | True | 0.19713965799996913 | False |
| stunting | Logistic Regression | 3 | 0.534425636574074 | 0.288296589293081 | 0.2523364485981308 | 856 | 216 | 640 | exploratory | joint v001+v021 equivalence partition | True | True | 0.09972195399996053 | False |
| stunting | Logistic Regression | 4 | 0.5484778184778185 | 0.29292169203851304 | 0.22526817640047675 | 839 | 189 | 650 | exploratory | joint v001+v021 equivalence partition | True | True | 0.08187030800002049 | False |
| stunting | Logistic Regression | 5 | 0.546279761904762 | 0.2717996004454206 | 0.22613065326633167 | 796 | 180 | 616 | exploratory | joint v001+v021 equivalence partition | True | True | 0.19059977000006256 | False |
| stunting | Random Forest | 1 | 0.5338525305410122 | 0.2799136238894993 | 0.24146649810366624 | 791 | 191 | 600 | exploratory | joint v001+v021 equivalence partition | True | True | 0.8228348630000255 | False |
| stunting | Random Forest | 2 | 0.5126049721460048 | 0.25417638783721197 | 0.23086269744835966 | 823 | 190 | 633 | exploratory | joint v001+v021 equivalence partition | True | True | 0.6227052860000413 | False |
| stunting | Random Forest | 3 | 0.5411892361111112 | 0.2923571438635079 | 0.2523364485981308 | 856 | 216 | 640 | exploratory | joint v001+v021 equivalence partition | True | True | 0.6894803180000508 | False |
| stunting | Random Forest | 4 | 0.5257834757834757 | 0.24619785816479603 | 0.22526817640047675 | 839 | 189 | 650 | exploratory | joint v001+v021 equivalence partition | True | True | 0.6014844619999167 | False |
| stunting | Random Forest | 5 | 0.5632169913419913 | 0.2674175481809242 | 0.22613065326633167 | 796 | 180 | 616 | exploratory | joint v001+v021 equivalence partition | True | True | 0.6075653499999589 | False |
| wasting | Logistic Regression | 1 | 0.5287140902872777 | 0.12438086529359829 | 0.12033694344163658 | 831 | 100 | 731 | exploratory | joint v001+v021 equivalence partition | True | True | 0.084930027999917 | False |
| wasting | Logistic Regression | 2 | 0.522045808078099 | 0.14071107917698505 | 0.12454655380894801 | 827 | 103 | 724 | exploratory | joint v001+v021 equivalence partition | True | True | 0.10243154300007973 | False |
| wasting | Logistic Regression | 3 | 0.5398825966850829 | 0.11977172483593444 | 0.10837438423645321 | 812 | 88 | 724 | exploratory | joint v001+v021 equivalence partition | True | True | 0.07290263099991989 | False |
| wasting | Logistic Regression | 4 | 0.5864468864468864 | 0.14889559475915587 | 0.114321608040201 | 796 | 91 | 705 | exploratory | joint v001+v021 equivalence partition | True | True | 0.16652553699998407 | False |
| wasting | Logistic Regression | 5 | 0.5213334766312452 | 0.13365880485666726 | 0.12052505966587113 | 838 | 101 | 737 | exploratory | joint v001+v021 equivalence partition | True | True | 0.1292656560000296 | False |
| wasting | Random Forest | 1 | 0.5419972640218879 | 0.1328519094711722 | 0.12033694344163658 | 831 | 100 | 731 | exploratory | joint v001+v021 equivalence partition | True | True | 1.3440719070000569 | False |
| wasting | Random Forest | 2 | 0.5258542080137317 | 0.14407094929594397 | 0.12454655380894801 | 827 | 103 | 724 | exploratory | joint v001+v021 equivalence partition | True | True | 1.2455820620000395 | False |
| wasting | Random Forest | 3 | 0.5365551230537419 | 0.1311459278179508 | 0.10837438423645321 | 812 | 88 | 724 | exploratory | joint v001+v021 equivalence partition | True | True | 0.7542844810000133 | False |
| wasting | Random Forest | 4 | 0.5376899696048633 | 0.13983991066916848 | 0.114321608040201 | 796 | 91 | 705 | exploratory | joint v001+v021 equivalence partition | True | True | 0.6588384269999779 | False |
| wasting | Random Forest | 5 | 0.5292193398444323 | 0.13511663906619653 | 0.12052505966587113 | 838 | 101 | 737 | exploratory | joint v001+v021 equivalence partition | True | True | 0.5666053710000369 | False |
| underweight | Logistic Regression | 1 | 0.5545410673142785 | 0.3063395624689105 | 0.2591687041564792 | 818 | 212 | 606 | exploratory | joint v001+v021 equivalence partition | True | True | 0.20977284499997495 | False |
| underweight | Logistic Regression | 2 | 0.5325996347117501 | 0.24210732806868895 | 0.19926650366748166 | 818 | 163 | 655 | exploratory | joint v001+v021 equivalence partition | True | True | 0.06772801199997502 | False |
| underweight | Logistic Regression | 3 | 0.5529531388152078 | 0.26623928750226444 | 0.2111650485436893 | 824 | 174 | 650 | exploratory | joint v001+v021 equivalence partition | True | True | 0.046766477999995004 | False |
| underweight | Logistic Regression | 4 | 0.5526854595259392 | 0.2859191282636071 | 0.23214285714285715 | 896 | 208 | 688 | exploratory | joint v001+v021 equivalence partition | True | True | 0.050903396999956385 | False |
| underweight | Logistic Regression | 5 | 0.5346936309415917 | 0.2917491416122234 | 0.23566084788029926 | 802 | 189 | 613 | exploratory | joint v001+v021 equivalence partition | True | True | 0.06657171300003029 | False |
| underweight | Random Forest | 1 | 0.5374984432405505 | 0.2991175446374488 | 0.2591687041564792 | 818 | 212 | 606 | exploratory | joint v001+v021 equivalence partition | True | True | 0.610187208999946 | False |
| underweight | Random Forest | 2 | 0.535849763499274 | 0.2517841319133822 | 0.19926650366748166 | 818 | 163 | 655 | exploratory | joint v001+v021 equivalence partition | True | True | 0.5878071749999663 | False |
| underweight | Random Forest | 3 | 0.5166534040671972 | 0.24377270806532653 | 0.2111650485436893 | 824 | 174 | 650 | exploratory | joint v001+v021 equivalence partition | True | True | 0.5112823660000458 | False |
| underweight | Random Forest | 4 | 0.5199400436046512 | 0.263175096810899 | 0.23214285714285715 | 896 | 208 | 688 | exploratory | joint v001+v021 equivalence partition | True | True | 0.3233297350000157 | False |
| underweight | Random Forest | 5 | 0.5630216560069741 | 0.27420829804169566 | 0.23566084788029926 | 802 | 189 | 613 | exploratory | joint v001+v021 equivalence partition | True | True | 0.3586580959999992 | False |
| fever | Logistic Regression | 1 | 0.4978230987735596 | 0.31659969031970314 | 0.3217993079584775 | 1734 | 558 | 1176 | exploratory | joint v001+v021 equivalence partition | True | True | 0.04145308899990141 | False |
| fever | Logistic Regression | 2 | 0.49339051344282386 | 0.3081596151492818 | 0.3111111111111111 | 1665 | 518 | 1147 | exploratory | joint v001+v021 equivalence partition | True | True | 0.0478027279999651 | False |
| fever | Logistic Regression | 3 | 0.498209687801738 | 0.28107384718565587 | 0.2855436081242533 | 1674 | 478 | 1196 | exploratory | joint v001+v021 equivalence partition | True | True | 0.049229467000031946 | False |
| fever | Logistic Regression | 4 | 0.5215386226928295 | 0.31758906600036296 | 0.3091133004926108 | 1624 | 502 | 1122 | exploratory | joint v001+v021 equivalence partition | True | True | 0.048467436999999336 | False |
| fever | Logistic Regression | 5 | 0.5016784052356501 | 0.3287174326260338 | 0.3206703910614525 | 1790 | 574 | 1216 | exploratory | joint v001+v021 equivalence partition | True | True | 0.04886833700004445 | False |
| fever | Random Forest | 1 | 0.4984631397361812 | 0.3201642734788371 | 0.3217993079584775 | 1734 | 558 | 1176 | exploratory | joint v001+v021 equivalence partition | True | True | 0.7443259640000406 | False |
| fever | Random Forest | 2 | 0.499291419954018 | 0.3144873676962848 | 0.3111111111111111 | 1665 | 518 | 1147 | exploratory | joint v001+v021 equivalence partition | True | True | 0.8067901379999967 | False |
| fever | Random Forest | 3 | 0.5029430388603573 | 0.2948773479518306 | 0.2855436081242533 | 1674 | 478 | 1196 | exploratory | joint v001+v021 equivalence partition | True | True | 0.7520594019999862 | False |
| fever | Random Forest | 4 | 0.49575228497773616 | 0.30105038589864264 | 0.3091133004926108 | 1624 | 502 | 1122 | exploratory | joint v001+v021 equivalence partition | True | True | 0.7772107060000053 | False |
| fever | Random Forest | 5 | 0.49413883412800297 | 0.3223192707538576 | 0.3206703910614525 | 1790 | 574 | 1216 | exploratory | joint v001+v021 equivalence partition | True | True | 0.7895429619999277 | False |. Fold evaluation status and skipped-fold reasons are in signal_check_fold_audit.csv.

These are preliminary unweighted cluster-held-out screening metrics, not final performance or population estimates. Fold preprocessing is fit on training data only. AP baselines use each test-fold prevalence; see signal_check_fold_metrics.csv. Fold means are descriptive. If joint v001/v021 equivalence-partition grouping is used, results are a provisional feasibility diagnostic requiring human confirmation of survey-design meaning before final interpretation; no canonical PSU or outcome is selected.

## 8. Topic evidence matrix

| candidate_outcome | label_validity | eligible_n | valid_n | missing_n | missing_pct | positive_n | negative_n | prevalence | imbalance_ratio | leakage_evidence | cluster_support | predictability_feasibility | predictor_interpretability | literature_relevance | colab_feasibility | team_decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stunting | Metadata-checked; human definition review remains. | 4226 | 4105.0 | 121.0 | 2.863227638428774 | 966.0 | 3139.0 | 0.23532277710109623 | 3.249482401656315 | direct_leakage=1; derived_leakage=5; proxy_risk=5; legitimate_predictor=3; uncertain=12; see leakage_audit.csv. | v001: clusters=670, positive=475, negative=664 \| v021: clusters=670, positive=475, negative=664 | [exploratory mode] Provisional grouped screen; PSU documentation confirmation pending; see signal_check.csv and signal_check_fold_metrics.csv. | 3 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Pilot runtime 4.2 seconds; repeat in target Colab. | NOT SELECTED — human team decision required. |
| wasting | Metadata-checked; human definition review remains. | 4226 | 4104.0 | 122.0 | 2.8868906767628966 | 483.0 | 3621.0 | 0.11769005847953216 | 7.496894409937888 | direct_leakage=1; derived_leakage=5; proxy_risk=5; legitimate_predictor=3; uncertain=12; see leakage_audit.csv. | v001: clusters=670, positive=341, negative=666 \| v021: clusters=670, positive=341, negative=666 | [exploratory mode] Provisional grouped screen; PSU documentation confirmation pending; see signal_check.csv and signal_check_fold_metrics.csv. | 3 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Pilot runtime 5.2 seconds; repeat in target Colab. | NOT SELECTED — human team decision required. |
| underweight | Metadata-checked; human definition review remains. | 4226 | 4158.0 | 68.0 | 1.609086606720303 | 946.0 | 3212.0 | 0.2275132275132275 | 3.395348837209302 | direct_leakage=1; derived_leakage=5; proxy_risk=5; legitimate_predictor=3; uncertain=12; see leakage_audit.csv. | v001: clusters=670, positive=469, negative=663 \| v021: clusters=670, positive=469, negative=663 | [exploratory mode] Provisional grouped screen; PSU documentation confirmation pending; see signal_check.csv and signal_check_fold_metrics.csv. | 3 pilot fields passed; 1 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Pilot runtime 2.8 seconds; repeat in target Colab. | NOT SELECTED — human team decision required. |
| fever | Metadata-checked; human definition review remains. | 8508 | 8487.0 | 21.0 | 0.2468265162200282 | 2630.0 | 5857.0 | 0.3098857075527277 | 2.226996197718631 | direct_leakage=1; derived_leakage=0; proxy_risk=122; legitimate_predictor=4; uncertain=10; see leakage_audit.csv. | v001: clusters=674, positive=642, negative=674 \| v021: clusters=674, positive=642, negative=674 | [exploratory mode] Provisional grouped screen; PSU documentation confirmation pending; see signal_check.csv and signal_check_fold_metrics.csv. | 4 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Pilot runtime 4.1 seconds; repeat in target Colab. | NOT SELECTED — human team decision required. |
| diarrhea | Metadata-checked; human definition review remains. | 8508 | 8485.0 | 23.0 | 0.27033380347907854 | 410.0 | 8075.0 | 0.04832056570418385 | 19.695121951219512 | direct_leakage=1; derived_leakage=0; proxy_risk=100; legitimate_predictor=4; uncertain=10; see leakage_audit.csv. | v001: clusters=674, positive=268, negative=674 \| v021: clusters=674, positive=268, negative=674 | [exploratory mode] Provisional grouped screen; PSU documentation confirmation pending; see signal_check.csv and signal_check_fold_metrics.csv. | 4 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Pilot runtime 4.6 seconds; repeat in target Colab. | NOT SELECTED — human team decision required. |
| ari_symptoms | Pending; no outcome constructed. | 8508 | not available | not available | not available | not available | not available | not available | not available | direct_leakage=0; derived_leakage=0; proxy_risk=60; legitimate_predictor=4; uncertain=57; see leakage_audit.csv. | Not assessed; PSU/outcome pending. | Not completed: Not run. | 4 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| child_anemia | Metadata-checked; human definition review remains. | 7593 | 0.0 | 7593.0 | 100.0 | 0.0 | 0.0 | not available | not available | direct_leakage=1; derived_leakage=0; proxy_risk=12; legitimate_predictor=4; uncertain=10; see leakage_audit.csv. | v001: clusters=0, positive=0, negative=0 \| v021: clusters=0, positive=0, negative=0 | Not completed: Only one outcome class remains after eligibility and valid-group filtering. | 4 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| full_age_appropriate_immunisation | Pending; no outcome constructed. | 1636 | not available | not available | not available | not available | not available | not available | not available | direct_leakage=0; derived_leakage=0; proxy_risk=0; legitimate_predictor=4; uncertain=18; see leakage_audit.csv. | Not assessed; PSU/outcome pending. | Not completed: Not run. | 4 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |
| mortality_related | Metadata-checked; human definition review remains. | 8784 | 8784.0 | 0.0 | 0.0 | 276.0 | 8508.0 | 0.031420765027322405 | 30.82608695652174 | direct_leakage=1; derived_leakage=0; proxy_risk=10; legitimate_predictor=4; uncertain=10; see leakage_audit.csv. | v001: clusters=674, positive=204, negative=674 \| v021: clusters=674, positive=204, negative=674 | Not completed: Not run. | 4 pilot fields passed; 0 held for review; not final features. | Pending full-paper review; G2 remains provisional. | Not benchmarked. | NOT SELECTED — human team decision required. |

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
6. Confirm each candidate outcome definition and its candidate-specific leakage audit by both researchers before treating any feasibility result as evidence for choosing the outcome (exploratory runs are allowed; confirmed mode enforces this).
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

- Run ID: BDHS0-RUN-20261107T155648Z-37903028
- Experiment configuration ID: BDHS0-CFG-224d6748826ef512
- Configuration identity SHA-256: 224d6748826ef5126f16640922ccc4f4ca67e51061cfdddb6de173789b9fd87d
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

The variable dictionary comparison checks labels and value-label counts; when the reference CSV has a value_labels column, code-to-text mappings are also compared; otherwise only counts are compared. The literature matrix is a working inventory only. Its status fields are carried forward as supplied and do not independently verify paper claims, full-text coverage, or novelty.
