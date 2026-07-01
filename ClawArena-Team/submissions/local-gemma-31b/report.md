# Run Report — local-gemma-31b

Scenarios: 41  ·  Rounds passed: 146 / 258

## Paper metrics (canonical)

> Metrics correspond exactly to the paper. Composite and per-scenario
> values are **derived** from the data already in `report.json` (no
> re-scoring): SMS = TCR × (TPP + ROC + WPP + MCA) / 4.

**Composite (paper)**

- **SMS** 43.86%  _= TCR × (TPP + ROC + WPP + MCA) / 4_
- TCR 56.59%  ·  TPP 78.96%  ·  ROC 97.70%  ·  WPP 37.88%  ·  MCA 95.47%

### Leaderboard — per scenario (paper)

| Scenario | Pass | SMS (paper) | TCR | TPP | ROC | WPP | MCA |
|---|---|---|---|---|---|---|---|
| s_radiology_case_review | 5/6 | **79.17%** | 83.33% | 100.00% | 100.00% | 80.00% | 100.00% |
| s_security_pcap_triage | 5/6 | **79.17%** | 83.33% | 100.00% | 100.00% | 80.00% | 100.00% |
| s_tax_filing_reconciliation | 5/6 | **70.31%** | 83.33% | 100.00% | 100.00% | 37.50% | 100.00% |
| s_climate_simulation_audit | 6/7 | **66.07%** | 85.71% | 83.33% | 100.00% | 25.00% | 100.00% |
| s_incident_postmortem | 5/6 | **65.23%** | 83.33% | 72.22% | 100.00% | 40.86% | 100.00% |
| s_satellite_change_detection | 4/5 | **64.75%** | 80.00% | 75.00% | 100.00% | 48.75% | 100.00% |
| s_genomics_pipeline_rerun | 5/6 | **64.58%** | 83.33% | 100.00% | 100.00% | 10.00% | 100.00% |
| s_ab_test_postmortem | 5/6 | **62.50%** | 83.33% | 100.00% | 100.00% | 0.00% | 100.00% |
| s_clinical_trial_protocol | 4/6 | **62.50%** | 66.67% | 100.00% | 100.00% | 75.00% | 100.00% |
| s_kubernetes_outage_rca | 5/6 | **62.00%** | 83.33% | 71.43% | 100.00% | 26.19% | 100.00% |
| s_codebase_migration_review | 8/10 | **61.76%** | 80.00% | 83.33% | 100.00% | 25.45% | 100.00% |
| s_observability_incident | 6/7 | **59.52%** | 85.71% | 44.44% | 100.00% | 33.33% | 100.00% |
| s_robotic_factory_alarm | 5/7 | **56.55%** | 71.43% | 75.00% | 100.00% | 41.67% | 100.00% |
| s_ui_redesign_review | 4/6 | **55.56%** | 66.67% | 33.33% | 100.00% | 100.00% | 100.00% |
| s_candidate_background_check | 4/6 | **53.89%** | 66.67% | 75.00% | 100.00% | 48.33% | 100.00% |
| s_litigation_review | 4/6 | **51.83%** | 66.67% | 83.33% | 100.00% | 47.65% | 80.00% |
| s_ml_rl_policy_review | 5/8 | **51.43%** | 62.50% | 100.00% | 100.00% | 29.17% | 100.00% |
| s_product_launch_warroom | 4/7 | **50.89%** | 57.14% | 97.22% | 91.67% | 67.31% | 100.00% |
| s_research_digest_xl | 4/6 | **49.96%** | 66.67% | 80.56% | 100.00% | 35.84% | 83.33% |
| s_oss_supply_chain_audit | 4/6 | **48.09%** | 66.67% | 74.36% | 100.00% | 14.17% | 100.00% |
| s_health_report_misread | 3/6 | **38.96%** | 50.00% | 90.00% | 100.00% | 21.67% | 100.00% |
| s_board_governance_pack | 3/6 | **38.32%** | 50.00% | 90.48% | 85.71% | 30.40% | 100.00% |
| s_journalism_factcheck | 3/6 | **37.40%** | 50.00% | 83.33% | 100.00% | 28.41% | 87.50% |
| s_clinical_trial_audit | 3/6 | **36.83%** | 50.00% | 77.78% | 93.33% | 30.17% | 93.33% |
| s_hospital_safety_event_review | 3/6 | **36.73%** | 50.00% | 85.00% | 80.00% | 28.87% | 100.00% |
| s_release_audit_giant | 3/6 | **34.57%** | 50.00% | 62.96% | 100.00% | 24.70% | 88.89% |
| s_strategy_backtest_review | 3/6 | **33.30%** | 50.00% | 66.67% | 75.00% | 24.72% | 100.00% |
| s_dept_merger_planning | 3/7 | **32.29%** | 42.86% | 64.58% | 100.00% | 36.76% | 100.00% |
| s_finance_options_pricing | 4/7 | **32.14%** | 57.14% | 25.00% | 100.00% | 0.00% | 100.00% |
| s_legal_contract_diff | 2/6 | **27.61%** | 33.33% | 100.00% | 100.00% | 43.80% | 87.50% |
| s_research_authorship_dispute | 2/6 | **27.34%** | 33.33% | 83.33% | 100.00% | 44.70% | 100.00% |
| s_smart_home_anomaly_triage | 2/6 | **26.31%** | 33.33% | 85.71% | 100.00% | 30.00% | 100.00% |
| s_partnership_term_sheet | 2/6 | **26.22%** | 33.33% | 94.44% | 100.00% | 31.33% | 88.89% |
| s_creator_contract_renewal | 2/6 | **25.00%** | 33.33% | 100.00% | 100.00% | 33.33% | 66.67% |
| s_hr_misconduct_intake | 2/6 | **23.99%** | 33.33% | 71.43% | 100.00% | 45.00% | 71.43% |
| s_grant_compliance_review | 2/7 | **23.92%** | 28.57% | 83.33% | 100.00% | 51.48% | 100.00% |
| s_devops_runbook_sync | 2/6 | **20.33%** | 33.33% | 51.67% | 80.00% | 12.35% | 100.00% |
| s_ecommerce_chargeback_dispute | 2/6 | **19.76%** | 33.33% | 50.00% | 100.00% | 20.44% | 66.67% |
| s_security_incident_triage | 1/6 | **13.91%** | 16.67% | 75.00% | 100.00% | 58.75% | 100.00% |
| s_trading_tz_incident | 1/6 | **13.35%** | 16.67% | 75.00% | 100.00% | 45.38% | 100.00% |
| s_fund_due_diligence | 1/6 | **13.23%** | 16.67% | 72.92% | 100.00% | 44.58% | 100.00% |

### Notation (paper)

| Abbr | Full name | Meaning |
|---|---|---|
| **SMS** | Subagent Management Score | paper composite = TCR × (TPP + ROC + WPP + MCA) / 4, range [0,1] |
| **TCR** | Task Completion Rate | average pass rate over user questions (= legacy TCR) |
| **TPP** | Tool-Permission Precision | share of tool types granted to and actually used by the subagent, averaged over subagents (= legacy TPS) |
| **ROC** | Read-Only Compliance | 0 if a read-only subagent is granted a mutating tool, else 1, averaged over subagents (= legacy ROS) |
| **WPP** | Workspace-Permission Precision | files actually accessed by subagent / total granted files, averaged over subagents (= legacy WPS) |
| **MCA** | Modality-Choice Accuracy | vlm actually reads image/video, omni actually reads audio, llm counts 1, averaged over subagents (= legacy MCS) |

---

## Legacy detailed statistics

> Legacy detailed statistics — metric definitions (composite SMS = 0.5·TCS + 0.5·MQS) differ from the paper; kept for reference.
> Legacy abbreviations map to paper ones (same numeric definition): **TPS→TPP, ROS→ROC, WPS→WPP, MCS→MCA**.

## Summary

**Composite**

- **SMS** 57.54%  _= 0.5·TCS + 0.5·MQS_
- **TCS** 37.57%  _= (TCR + SCR + SFR) / 3_
- **MQS** 77.50%  _= mean over scenarios of (TPS+ROS+WPS+MCS)/4_

**Scored aggregates**

- TCR 56.59%  ·  SCR 56.12%  ·  SFR 0.00%
- TPS 78.96%  ·  ROS 97.70%  ·  WPS 37.88%  ·  MCS 95.47%

**Statistics aggregates**

- SUB 225  ·  MKD llm:160, vlm:43, omni:22  ·  INV new+runtime:389, workflow:33, new+background:15, continue+runtime:5
- BSH runtime:1322, background:11  ·  SOC 1
- TGC Read:213, Glob:97, Grep:49, Bash:40, Write:25, Edit:4
- MAF 111  ·  SAFt 354  ·  SAFa 1.57
- MCM 90,507 / 200,000 (**MCU% 45.3%**)
- MIT 905,532  ·  MOT 440,017  ·  MCR 35,848,384
- SCM 18,424,352  ·  SIT 5,685,646  ·  SOT 506,638  ·  SCH 31,534,922  ·  SST 27,815

## Scored — per scenario

| Scenario | Pass | SMS | TCR | TPS | ROS | WPS | MCS |
|---|---|---|---|---|---|---|---|
| s_ab_test_postmortem | 5/6 | **79.17%** | 83.33% | 100.00% | 100.00% | 0.00% | 100.00% |
| s_board_governance_pack | 3/6 | **63.32%** | 50.00% | 90.48% | 85.71% | 30.40% | 100.00% |
| s_candidate_background_check | 4/6 | **73.75%** | 66.67% | 75.00% | 100.00% | 48.33% | 100.00% |
| s_climate_simulation_audit | 6/7 | **81.40%** | 85.71% | 83.33% | 100.00% | 25.00% | 100.00% |
| s_clinical_trial_audit | 3/6 | **61.83%** | 50.00% | 77.78% | 93.33% | 30.17% | 93.33% |
| s_clinical_trial_protocol | 4/6 | **80.21%** | 66.67% | 100.00% | 100.00% | 75.00% | 100.00% |
| s_codebase_migration_review | 8/10 | **78.60%** | 80.00% | 83.33% | 100.00% | 25.45% | 100.00% |
| s_creator_contract_renewal | 2/6 | **54.17%** | 33.33% | 100.00% | 100.00% | 33.33% | 66.67% |
| s_dept_merger_planning | 3/7 | **59.10%** | 42.86% | 64.58% | 100.00% | 36.76% | 100.00% |
| s_devops_runbook_sync | 2/6 | **47.17%** | 33.33% | 51.67% | 80.00% | 12.35% | 100.00% |
| s_ecommerce_chargeback_dispute | 2/6 | **46.30%** | 33.33% | 50.00% | 100.00% | 20.44% | 66.67% |
| s_finance_options_pricing | 4/7 | **56.70%** | 57.14% | 25.00% | 100.00% | 0.00% | 100.00% |
| s_fund_due_diligence | 1/6 | **48.02%** | 16.67% | 72.92% | 100.00% | 44.58% | 100.00% |
| s_genomics_pipeline_rerun | 5/6 | **80.42%** | 83.33% | 100.00% | 100.00% | 10.00% | 100.00% |
| s_grant_compliance_review | 2/7 | **56.14%** | 28.57% | 83.33% | 100.00% | 51.48% | 100.00% |
| s_health_report_misread | 3/6 | **63.96%** | 50.00% | 90.00% | 100.00% | 21.67% | 100.00% |
| s_hospital_safety_event_review | 3/6 | **61.73%** | 50.00% | 85.00% | 80.00% | 28.87% | 100.00% |
| s_hr_misconduct_intake | 2/6 | **52.65%** | 33.33% | 71.43% | 100.00% | 45.00% | 71.43% |
| s_incident_postmortem | 5/6 | **80.80%** | 83.33% | 72.22% | 100.00% | 40.86% | 100.00% |
| s_journalism_factcheck | 3/6 | **62.40%** | 50.00% | 83.33% | 100.00% | 28.41% | 87.50% |
| s_kubernetes_outage_rca | 5/6 | **78.87%** | 83.33% | 71.43% | 100.00% | 26.19% | 100.00% |
| s_legal_contract_diff | 2/6 | **58.08%** | 33.33% | 100.00% | 100.00% | 43.80% | 87.50% |
| s_litigation_review | 4/6 | **72.21%** | 66.67% | 83.33% | 100.00% | 47.65% | 80.00% |
| s_ml_rl_policy_review | 5/8 | **72.40%** | 62.50% | 100.00% | 100.00% | 29.17% | 100.00% |
| s_observability_incident | 6/7 | **77.58%** | 85.71% | 44.44% | 100.00% | 33.33% | 100.00% |
| s_oss_supply_chain_audit | 4/6 | **69.40%** | 66.67% | 74.36% | 100.00% | 14.17% | 100.00% |
| s_partnership_term_sheet | 2/6 | **56.00%** | 33.33% | 94.44% | 100.00% | 31.33% | 88.89% |
| s_product_launch_warroom | 4/7 | **73.10%** | 57.14% | 97.22% | 91.67% | 67.31% | 100.00% |
| s_radiology_case_review | 5/6 | **89.17%** | 83.33% | 100.00% | 100.00% | 80.00% | 100.00% |
| s_release_audit_giant | 3/6 | **59.57%** | 50.00% | 62.96% | 100.00% | 24.70% | 88.89% |
| s_research_authorship_dispute | 2/6 | **57.67%** | 33.33% | 83.33% | 100.00% | 44.70% | 100.00% |
| s_research_digest_xl | 4/6 | **70.80%** | 66.67% | 80.56% | 100.00% | 35.84% | 83.33% |
| s_robotic_factory_alarm | 5/7 | **75.30%** | 71.43% | 75.00% | 100.00% | 41.67% | 100.00% |
| s_satellite_change_detection | 4/5 | **80.47%** | 80.00% | 75.00% | 100.00% | 48.75% | 100.00% |
| s_security_incident_triage | 1/6 | **50.05%** | 16.67% | 75.00% | 100.00% | 58.75% | 100.00% |
| s_security_pcap_triage | 5/6 | **89.17%** | 83.33% | 100.00% | 100.00% | 80.00% | 100.00% |
| s_smart_home_anomaly_triage | 2/6 | **56.13%** | 33.33% | 85.71% | 100.00% | 30.00% | 100.00% |
| s_strategy_backtest_review | 3/6 | **58.30%** | 50.00% | 66.67% | 75.00% | 24.72% | 100.00% |
| s_tax_filing_reconciliation | 5/6 | **83.85%** | 83.33% | 100.00% | 100.00% | 37.50% | 100.00% |
| s_trading_tz_incident | 1/6 | **48.38%** | 16.67% | 75.00% | 100.00% | 45.38% | 100.00% |
| s_ui_redesign_review | 4/6 | **75.00%** | 66.67% | 33.33% | 100.00% | 100.00% | 100.00% |

## Statistics — Subagent & Forbidden (per scenario)

| Scenario | SUB | MKD | INV | TGC | MAF | SAFt | SAFa |
|---|---|---|---|---|---|---|---|
| s_ab_test_postmortem | 1 | llm:1 | workflow:4 | Bash:1 | 1 | 0 | 0.00 |
| s_board_governance_pack | 7 | llm:6, vlm:1 | new+runtime:9 | Read:7, Edit:1, Write:1 | 3 | 0 | 0.00 |
| s_candidate_background_check | 4 | llm:2, omni:1, vlm:1 | new+runtime:9 | Glob:4, Read:4 | 3 | 0 | 0.00 |
| s_climate_simulation_audit | 3 | llm:2, vlm:1 | new+runtime:4 | Read:3, Bash:2 | 1 | 0 | 0.00 |
| s_clinical_trial_audit | 15 | llm:13, vlm:2 | new+runtime:22, workflow:5 | Read:14, Glob:9, Write:5 | 6 | 8 | 0.53 |
| s_clinical_trial_protocol | 2 | llm:1, omni:1 | new+runtime:5 | Read:2, Bash:1, Glob:1, Write:1 | 2 | 3 | 1.50 |
| s_codebase_migration_review | 2 | llm:2 | new+runtime:3, workflow:1 | Read:2, Glob:1, Grep:1 | 1 | 0 | 0.00 |
| s_creator_contract_renewal | 3 | llm:1, omni:1, vlm:1 | new+runtime:21 | Read:3, Bash:2, Glob:1 | 6 | 27 | 9.00 |
| s_dept_merger_planning | 4 | llm:3, vlm:1 | new+runtime:4 | Read:4, Write:4, Bash:3, Glob:3, Edit:2, Grep:2 | 0 | 0 | 0.00 |
| s_devops_runbook_sync | 5 | llm:4, omni:1 | new+runtime:11, continue+runtime:4, new+background:2 | Read:4, Grep:3, Bash:2, Glob:2, Write:1 | 4 | 1 | 0.20 |
| s_ecommerce_chargeback_dispute | 6 | vlm:3, llm:2, omni:1 | new+runtime:8 | Read:6, Grep:2 | 1 | 78 | 13.00 |
| s_finance_options_pricing | 1 | llm:1 | new+runtime:2, continue+runtime:1 | Bash:1, Glob:1, Grep:1, Read:1 | 0 | 0 | 0.00 |
| s_fund_due_diligence | 4 | llm:4 | new+runtime:4 | Read:4, Glob:3, Grep:3, Bash:2 | 2 | 0 | 0.00 |
| s_genomics_pipeline_rerun | 2 | llm:2 | new+runtime:2 | Bash:1, Read:1 | 2 | 0 | 0.00 |
| s_grant_compliance_review | 6 | llm:5, vlm:1 | new+runtime:12, workflow:8 | Read:6 | 3 | 1 | 0.17 |
| s_health_report_misread | 5 | llm:3, omni:1, vlm:1 | new+runtime:10 | Read:5, Bash:1 | 4 | 0 | 0.00 |
| s_hospital_safety_event_review | 5 | llm:2, vlm:2, omni:1 | new+runtime:9 | Bash:4, Read:4, Glob:1, Grep:1 | 2 | 2 | 0.40 |
| s_hr_misconduct_intake | 7 | llm:4, omni:3 | new+runtime:19 | Read:7, Glob:3 | 7 | 8 | 1.14 |
| s_incident_postmortem | 6 | llm:5, vlm:1 | new+runtime:17, new+background:1 | Read:5, Glob:3, Grep:3 | 7 | 1 | 0.17 |
| s_journalism_factcheck | 8 | llm:5, vlm:2, omni:1 | new+runtime:9, new+background:2 | Read:8, Glob:1, Grep:1 | 4 | 10 | 1.25 |
| s_kubernetes_outage_rca | 7 | llm:5, omni:1, vlm:1 | new+runtime:11 | Read:7, Bash:3, Grep:3 | 2 | 3 | 0.43 |
| s_legal_contract_diff | 8 | llm:5, vlm:2, omni:1 | new+runtime:11 | Read:8 | 3 | 11 | 1.38 |
| s_litigation_review | 5 | llm:2, vlm:2, omni:1 | new+runtime:8 | Glob:5, Read:5, Grep:1 | 5 | 2 | 0.40 |
| s_ml_rl_policy_review | 2 | llm:1, vlm:1 | new+runtime:2 | Read:2 | 2 | 0 | 0.00 |
| s_observability_incident | 3 | llm:3 | new+runtime:5 | Glob:3, Read:3, Grep:2, Bash:1 | 1 | 4 | 1.33 |
| s_oss_supply_chain_audit | 13 | llm:12, omni:1 | new+runtime:14 | Read:13, Glob:9, Bash:3, Grep:3 | 10 | 1 | 0.08 |
| s_partnership_term_sheet | 9 | llm:6, vlm:2, omni:1 | new+runtime:20 | Read:8, Glob:2, Bash:1, Grep:1 | 4 | 2 | 0.22 |
| s_product_launch_warroom | 12 | llm:7, vlm:5 | new+runtime:19, workflow:6 | Read:12, Glob:11, Write:3, Edit:1 | 2 | 3 | 0.25 |
| s_radiology_case_review | 1 | vlm:1 | new+runtime:2 | Read:1, Write:1 | 0 | 6 | 6.00 |
| s_release_audit_giant | 9 | llm:6, vlm:2, omni:1 | new+runtime:13, workflow:3 | Read:7, Glob:6, Grep:5, Write:2, Bash:1 | 1 | 173 | 19.22 |
| s_research_authorship_dispute | 10 | llm:9, vlm:1 | new+runtime:4, new+background:3, workflow:3 | Glob:10, Read:10, Write:3, Grep:2 | 3 | 2 | 0.20 |
| s_research_digest_xl | 6 | llm:4, omni:1, vlm:1 | new+runtime:9, new+background:1 | Read:5, Glob:3, Grep:2, Bash:1, Write:1 | 1 | 6 | 1.00 |
| s_robotic_factory_alarm | 2 | llm:1, vlm:1 | new+runtime:2 | Read:2, Grep:1 | 1 | 0 | 0.00 |
| s_satellite_change_detection | 4 | llm:3, vlm:1 | new+runtime:4, new+background:3 | Read:4, Glob:3, Grep:3 | 0 | 0 | 0.00 |
| s_security_incident_triage | 8 | llm:6, omni:1, vlm:1 | new+runtime:13 | Read:8, Grep:3, Bash:2, Glob:1 | 5 | 0 | 0.00 |
| s_security_pcap_triage | 4 | llm:3, vlm:1 | new+runtime:11, new+background:3 | Read:4, Write:3, Bash:2 | 0 | 2 | 0.50 |
| s_smart_home_anomaly_triage | 7 | llm:5, omni:1, vlm:1 | new+runtime:13 | Read:6, Glob:5, Bash:3, Grep:1 | 3 | 0 | 0.00 |
| s_strategy_backtest_review | 4 | llm:2, omni:1, vlm:1 | new+runtime:6 | Read:4, Bash:3, Glob:2, Grep:1 | 1 | 0 | 0.00 |
| s_tax_filing_reconciliation | 6 | llm:4, omni:1, vlm:1 | new+runtime:6 | Read:6, Glob:3 | 2 | 0 | 0.00 |
| s_trading_tz_incident | 8 | llm:8 | new+runtime:33, workflow:3 | Read:7, Grep:3 | 3 | 0 | 0.00 |
| s_ui_redesign_review | 1 | vlm:1 | new+runtime:3 | Glob:1, Grep:1, Read:1 | 3 | 0 | 0.00 |

## Statistics — Main Agent Tokens (per scenario)

| Scenario | MCM | MCU% | MIT | MOT | MCR |
|---|---|---|---|---|---|
| s_ab_test_postmortem | 19,201 | 9.6% | 13,922 | 5,279 | 344,401 |
| s_board_governance_pack | 33,006 | 16.5% | 20,635 | 12,371 | 1,042,990 |
| s_candidate_background_check | 33,982 | 17.0% | 20,824 | 13,158 | 877,023 |
| s_climate_simulation_audit | 21,545 | 10.8% | 14,040 | 7,505 | 417,561 |
| s_clinical_trial_audit | 39,794 | 19.9% | 22,838 | 16,956 | 1,096,024 |
| s_clinical_trial_protocol | 24,231 | 12.1% | 15,818 | 8,413 | 727,147 |
| s_codebase_migration_review | 27,932 | 14.0% | 18,677 | 9,255 | 647,234 |
| s_creator_contract_renewal | 35,373 | 17.7% | 21,026 | 14,347 | 1,213,161 |
| s_dept_merger_planning | 90,507 | 45.3% | 82,540 | 7,967 | 733,438 |
| s_devops_runbook_sync | 31,373 | 15.7% | 17,609 | 13,764 | 901,217 |
| s_ecommerce_chargeback_dispute | 26,825 | 13.4% | 15,572 | 11,253 | 777,147 |
| s_finance_options_pricing | 18,568 | 9.3% | 13,064 | 5,504 | 333,298 |
| s_fund_due_diligence | 41,823 | 20.9% | 29,444 | 12,379 | 1,131,329 |
| s_genomics_pipeline_rerun | 40,871 | 20.4% | 35,243 | 5,628 | 809,107 |
| s_grant_compliance_review | 40,034 | 20.0% | 25,119 | 14,915 | 1,016,993 |
| s_health_report_misread | 27,745 | 13.9% | 17,023 | 10,722 | 641,501 |
| s_hospital_safety_event_review | 23,000 | 11.5% | 15,383 | 7,617 | 447,546 |
| s_hr_misconduct_intake | 47,867 | 23.9% | 24,252 | 23,615 | 1,995,708 |
| s_incident_postmortem | 36,028 | 18.0% | 21,328 | 14,700 | 854,497 |
| s_journalism_factcheck | 37,769 | 18.9% | 24,183 | 13,586 | 1,518,613 |
| s_kubernetes_outage_rca | 25,858 | 12.9% | 16,250 | 9,608 | 611,167 |
| s_legal_contract_diff | 21,877 | 10.9% | 14,265 | 7,612 | 493,934 |
| s_litigation_review | 24,014 | 12.0% | 14,860 | 9,154 | 591,446 |
| s_ml_rl_policy_review | 21,612 | 10.8% | 15,687 | 5,925 | 450,136 |
| s_observability_incident | 22,010 | 11.0% | 14,620 | 7,390 | 441,125 |
| s_oss_supply_chain_audit | 50,351 | 25.2% | 35,093 | 15,258 | 1,295,591 |
| s_partnership_term_sheet | 30,323 | 15.2% | 16,384 | 13,939 | 913,568 |
| s_product_launch_warroom | 28,220 | 14.1% | 16,422 | 11,798 | 866,305 |
| s_radiology_case_review | 19,002 | 9.5% | 13,912 | 5,090 | 286,429 |
| s_release_audit_giant | 28,423 | 14.2% | 16,609 | 11,814 | 837,724 |
| s_research_authorship_dispute | 30,936 | 15.5% | 18,017 | 12,919 | 801,898 |
| s_research_digest_xl | 27,822 | 13.9% | 16,773 | 11,049 | 808,884 |
| s_robotic_factory_alarm | 22,567 | 11.3% | 15,447 | 7,120 | 513,437 |
| s_satellite_change_detection | 19,405 | 9.7% | 14,071 | 5,334 | 259,168 |
| s_security_incident_triage | 80,777 | 40.4% | 64,595 | 16,182 | 4,190,965 |
| s_security_pcap_triage | 26,466 | 13.2% | 16,973 | 9,493 | 544,235 |
| s_smart_home_anomaly_triage | 56,304 | 28.2% | 45,590 | 10,714 | 1,759,106 |
| s_strategy_backtest_review | 23,629 | 11.8% | 16,697 | 6,932 | 367,391 |
| s_tax_filing_reconciliation | 27,991 | 14.0% | 19,499 | 8,492 | 609,347 |
| s_trading_tz_incident | 39,901 | 20.0% | 22,144 | 17,757 | 1,285,966 |
| s_ui_redesign_review | 20,587 | 10.3% | 13,084 | 7,503 | 394,627 |

## Statistics — Subagent Tokens (per scenario)

| Scenario | SCM | SIT | SOT | SCH | SST |
|---|---|---|---|---|---|
| s_ab_test_postmortem | 7,632 | 5,553 | 2,079 | 16,529 | 644 |
| s_board_governance_pack | 335,624 | 308,589 | 26,876 | 4,989,713 | 297 |
| s_candidate_background_check | 375,645 | 40,457 | 3,596 | 24,534 | 566 |
| s_climate_simulation_audit | 12,266 | 9,998 | 2,268 | 16,542 | 186 |
| s_clinical_trial_audit | 689,747 | 481,585 | 26,538 | 4,171,314 | 1,986 |
| s_clinical_trial_protocol | 78,749 | 72,971 | 5,778 | 118,482 | 233 |
| s_codebase_migration_review | 280,755 | 135,981 | 8,612 | 149,657 | 255 |
| s_creator_contract_renewal | 241,857 | 226,076 | 15,781 | 196,882 | 1,116 |
| s_dept_merger_planning | 103,423 | 94,781 | 8,642 | 442,026 | 278 |
| s_devops_runbook_sync | 782,300 | 107,998 | 9,029 | 167,989 | 404 |
| s_ecommerce_chargeback_dispute | 118,954 | 111,905 | 7,020 | 481,943 | 269 |
| s_finance_options_pricing | 8,362 | 6,349 | 2,013 | 17,122 | 80 |
| s_fund_due_diligence | 111,821 | 99,715 | 12,106 | 197,810 | 178 |
| s_genomics_pipeline_rerun | 2,839 | 2,577 | 262 | 2,068 | 62 |
| s_grant_compliance_review | 256,649 | 243,811 | 12,838 | 691,700 | 2,836 |
| s_health_report_misread | 311,140 | 100,045 | 3,531 | 13,590 | 390 |
| s_hospital_safety_event_review | 248,000 | 34,897 | 3,859 | 33,569 | 261 |
| s_hr_misconduct_intake | 66,880 | 57,878 | 9,002 | 83,104 | 811 |
| s_incident_postmortem | 1,286,480 | 70,475 | 9,380 | 82,669 | 621 |
| s_journalism_factcheck | 484,193 | 153,969 | 13,373 | 2,201,750 | 411 |
| s_kubernetes_outage_rca | 141,133 | 100,680 | 40,195 | 3,163,262 | 569 |
| s_legal_contract_diff | 202,093 | 197,643 | 4,450 | 38,938 | 358 |
| s_litigation_review | 39,699 | 31,428 | 8,262 | 866,781 | 764 |
| s_ml_rl_policy_review | 5,823 | 5,059 | 764 | 2,459 | 93 |
| s_observability_incident | 33,770 | 31,172 | 2,598 | 84,389 | 203 |
| s_oss_supply_chain_audit | 466,330 | 104,926 | 36,184 | 1,849,624 | 857 |
| s_partnership_term_sheet | 591,776 | 186,619 | 9,438 | 302,188 | 690 |
| s_product_launch_warroom | 2,309,702 | 846,989 | 30,201 | 391,904 | 2,559 |
| s_radiology_case_review | 6,880 | 4,937 | 1,943 | 18,555 | 84 |
| s_release_audit_giant | 196,391 | 172,880 | 23,455 | 1,388,240 | 1,830 |
| s_research_authorship_dispute | 157,513 | 145,438 | 12,075 | 287,243 | 710 |
| s_research_digest_xl | 52,842 | 44,796 | 8,046 | 62,933 | 598 |
| s_robotic_factory_alarm | 98,771 | 97,190 | 1,581 | 10,507 | 85 |
| s_satellite_change_detection | 848,704 | 236,150 | 6,209 | 123,545 | 217 |
| s_security_incident_triage | 339,761 | 208,185 | 38,159 | 3,308,725 | 949 |
| s_security_pcap_triage | 476,941 | 290,331 | 45,944 | 3,368,667 | 599 |
| s_smart_home_anomaly_triage | 316,621 | 290,777 | 25,844 | 1,335,564 | 686 |
| s_strategy_backtest_review | 156,976 | 154,366 | 2,610 | 40,667 | 296 |
| s_tax_filing_reconciliation | 71,599 | 69,856 | 1,743 | 18,360 | 203 |
| s_trading_tz_incident | 6,081,522 | 75,935 | 22,844 | 765,621 | 3,374 |
| s_ui_redesign_review | 26,189 | 24,679 | 1,510 | 7,757 | 207 |

## Notation (legacy)

_Legacy abbreviations; the four management sub-scores equal the paper's_ _TPS→TPP, ROS→ROC, WPS→WPP, MCS→MCA (same numeric definition)._

| Abbr | Full name | Meaning |
|---|---|---|
| **SMS** | Subagent Management Score | composite score = 0.5·TCS + 0.5·MQS, range [0,1] |
| **TCS** | Task Correctness Subscore | = (TCR + SCR + SFR) / 3, equal-weighted aggregate of the three task-correctness metrics |
| **MQS** | Management Quality Subscore | = mean over scenarios of (TPS+ROS+WPS+MCS)/4, subagent management quality |
| **TCR** | Task Completion Rate | average pass rate over user questions |
| **SCR** | Scenario Completion Rate | per-scenario question average, then averaged across scenarios |
| **SFR** | Scenario Full-pass Rate | 1 if all questions in a scenario pass, averaged across scenarios |
| **TPS** | Tool Permission Score | tool types used by subagent / tool types granted, averaged over subagents |
| **ROS** | Readonly Subagent Score | 0 if a read-only subagent is granted a mutating tool, else 1, averaged over subagents |
| **WPS** | Workspace Permission Score | files actually accessed by subagent / total granted workspace files, averaged over subagents |
| **MCS** | Model Choice Score | vlm must read image/video, omni must read audio, else 0, averaged over subagents |
| **SUB** | Subagent Create Count | total number of subagents created within the scenario |
| **MKD** | Model Key Distribution | selection counts for llm/vlm/omni |
| **INV** | Invocation Distribution | flattened five-way count of subagent invocation modes: {new,continue}×{runtime,background} + workflow |
| **BSH** | Bash Mode Distribution | count of Bash invocation modes {runtime, background} (main + subagent combined) |
| **SOC** | Structured Output Count | number of subagent calls with schema-enforced structured output |
| **TGC** | Tools Grant Counts | total count of tool types granted across all subagents |
| **MAF** | Main Agent Forbidden | count of unauthorized accesses by the main agent |
| **SAFt** | Subagent Forbidden Total | total count of unauthorized subagent accesses |
| **SAFa** | Subagent Forbidden Avg | average subagent unauthorized accesses (per number of subagents) |
| **MCM** | Main Context Max | peak context occupancy of the main agent after all turns are added; comparing it against token_limit decides the breaker |
| **MCU%** | Main Context Use % | = MCM / context_token_limit |
| **MIT** | Main Input Total | main agent cumulative input (sum of the new input of each model call) |
| **MOT** | Main Output Total | main agent cumulative output (sum of each assistant turn itself) |
| **MCR** | Main Cache-Read Total | main agent cumulative cache-read (sum of the tokens already present in context before each call) |
| **SCM** | Subagent Context Max (sum) | sum of the context_size_max of each subagent session (a rough reflection of the sub usage ceiling) |
| **SIT** | Subagent Input Total | cumulative input across all subagent sessions |
| **SOT** | Subagent Output Total | cumulative output across all subagent sessions |
| **SCH** | Subagent Cache-Hit Total | cumulative cache-read across all subagent sessions |
| **SST** | Subagent System Tokens | total subagent system prompt tokens (a static quantity) |
