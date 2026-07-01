# Run Report — local-qwen3.6-27b

Scenarios: 41  ·  Rounds passed: 157 / 258

## Paper metrics (canonical)

> Metrics correspond exactly to the paper. Composite and per-scenario
> values are **derived** from the data already in `report.json` (no
> re-scoring): SMS = TCR × (TPP + ROC + WPP + MCA) / 4.

**Composite (paper)**

- **SMS** 46.42%  _= TCR × (TPP + ROC + WPP + MCA) / 4_
- TCR 60.85%  ·  TPP 72.50%  ·  ROC 95.74%  ·  WPP 40.70%  ·  MCA 96.21%

### Leaderboard — per scenario (paper)

| Scenario | Pass | SMS (paper) | TCR | TPP | ROC | WPP | MCA |
|---|---|---|---|---|---|---|---|
| s_satellite_change_detection | 5/5 | **97.92%** | 100.00% | 100.00% | 100.00% | 91.67% | 100.00% |
| s_trading_tz_incident | 6/6 | **79.50%** | 100.00% | 81.25% | 100.00% | 36.73% | 100.00% |
| s_radiology_case_review | 5/6 | **79.17%** | 83.33% | 100.00% | 100.00% | 80.00% | 100.00% |
| s_codebase_migration_review | 10/10 | **71.77%** | 100.00% | 74.17% | 100.00% | 12.93% | 100.00% |
| s_tax_filing_reconciliation | 6/6 | **71.35%** | 100.00% | 80.00% | 100.00% | 25.38% | 80.00% |
| s_genomics_pipeline_rerun | 5/6 | **66.67%** | 83.33% | 100.00% | 100.00% | 20.00% | 100.00% |
| s_observability_incident | 6/7 | **64.88%** | 85.71% | 69.44% | 100.00% | 33.33% | 100.00% |
| s_security_pcap_triage | 5/6 | **64.24%** | 83.33% | 75.00% | 100.00% | 33.33% | 100.00% |
| s_finance_options_pricing | 7/7 | **62.50%** | 100.00% | 37.50% | 100.00% | 12.50% | 100.00% |
| s_candidate_background_check | 4/6 | **61.81%** | 66.67% | 87.50% | 100.00% | 83.33% | 100.00% |
| s_ml_rl_policy_review | 6/8 | **61.72%** | 75.00% | 100.00% | 100.00% | 29.17% | 100.00% |
| s_ecommerce_chargeback_dispute | 4/6 | **57.26%** | 66.67% | 90.48% | 100.00% | 53.10% | 100.00% |
| s_research_authorship_dispute | 4/6 | **56.94%** | 66.67% | 68.06% | 100.00% | 73.61% | 100.00% |
| s_security_incident_triage | 5/6 | **54.76%** | 83.33% | 50.00% | 100.00% | 12.86% | 100.00% |
| s_climate_simulation_audit | 5/7 | **54.45%** | 71.43% | 100.00% | 100.00% | 38.25% | 66.67% |
| s_clinical_trial_audit | 4/6 | **54.18%** | 66.67% | 79.17% | 87.50% | 58.39% | 100.00% |
| s_clinical_trial_protocol | 5/6 | **53.91%** | 83.33% | 65.00% | 50.00% | 43.75% | 100.00% |
| s_fund_due_diligence | 4/6 | **50.05%** | 66.67% | 80.95% | 85.71% | 33.65% | 100.00% |
| s_ui_redesign_review | 4/6 | **50.00%** | 66.67% | 50.00% | 100.00% | 50.00% | 100.00% |
| s_kubernetes_outage_rca | 4/6 | **48.25%** | 66.67% | 76.19% | 100.00% | 27.58% | 85.71% |
| s_research_digest_xl | 4/6 | **44.68%** | 66.67% | 59.26% | 88.89% | 53.27% | 66.67% |
| s_hr_misconduct_intake | 3/6 | **44.29%** | 50.00% | 86.11% | 100.00% | 68.24% | 100.00% |
| s_litigation_review | 3/6 | **43.07%** | 50.00% | 93.33% | 100.00% | 51.24% | 100.00% |
| s_robotic_factory_alarm | 4/7 | **42.86%** | 57.14% | 61.11% | 100.00% | 38.89% | 100.00% |
| s_partnership_term_sheet | 3/6 | **40.17%** | 50.00% | 72.22% | 100.00% | 49.14% | 100.00% |
| s_oss_supply_chain_audit | 3/6 | **37.20%** | 50.00% | 67.95% | 100.00% | 37.37% | 92.31% |
| s_release_audit_giant | 3/6 | **37.00%** | 50.00% | 64.29% | 100.00% | 46.03% | 85.71% |
| s_hospital_safety_event_review | 3/6 | **36.94%** | 50.00% | 83.33% | 66.67% | 45.51% | 100.00% |
| s_dept_merger_planning | 3/7 | **36.80%** | 42.86% | 75.00% | 100.00% | 68.45% | 100.00% |
| s_journalism_factcheck | 3/6 | **36.24%** | 50.00% | 66.67% | 100.00% | 23.26% | 100.00% |
| s_health_report_misread | 3/6 | **36.17%** | 50.00% | 80.00% | 80.00% | 29.33% | 100.00% |
| s_strategy_backtest_review | 3/6 | **35.53%** | 50.00% | 75.00% | 83.33% | 25.93% | 100.00% |
| s_product_launch_warroom | 3/7 | **31.86%** | 42.86% | 60.77% | 92.31% | 51.95% | 92.31% |
| s_ab_test_postmortem | 3/6 | **30.32%** | 50.00% | 38.89% | 100.00% | 3.70% | 100.00% |
| s_devops_runbook_sync | 2/6 | **25.07%** | 33.33% | 84.09% | 100.00% | 16.75% | 100.00% |
| s_incident_postmortem | 2/6 | **23.67%** | 33.33% | 54.55% | 90.91% | 38.63% | 100.00% |
| s_legal_contract_diff | 2/6 | **23.15%** | 33.33% | 50.00% | 100.00% | 27.75% | 100.00% |
| s_creator_contract_renewal | 1/6 | **13.44%** | 16.67% | 80.00% | 100.00% | 62.56% | 80.00% |
| s_smart_home_anomaly_triage | 1/6 | **10.00%** | 16.67% | 40.00% | 100.00% | 0.00% | 100.00% |
| s_grant_compliance_review | 1/7 | **9.40%** | 14.29% | 42.06% | 100.00% | 25.95% | 95.24% |
| s_board_governance_pack | 0/6 | **0.00%** | 0.00% | 73.33% | 100.00% | 55.00% | 100.00% |

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

- **SMS** 60.37%  _= 0.5·TCS + 0.5·MQS_
- **TCS** 44.45%  _= (TCR + SCR + SFR) / 3_
- **MQS** 76.29%  _= mean over scenarios of (TPS+ROS+WPS+MCS)/4_

**Scored aggregates**

- TCR 60.85%  ·  SCR 60.31%  ·  SFR 12.20%
- TPS 72.50%  ·  ROS 95.74%  ·  WPS 40.70%  ·  MCS 96.21%

**Statistics aggregates**

- SUB 235  ·  MKD llm:166, vlm:43, omni:26  ·  INV new+runtime:275, workflow:77, new+background:50, continue+runtime:23, continue+background:8
- BSH runtime:817, background:10  ·  SOC 0
- TGC Read:227, Glob:154, Grep:97, Write:38, Bash:35, Edit:1
- MAF 139  ·  SAFt 1238  ·  SAFa 5.27
- MCM 250,575 / 200,000 (**MCU% 125.3%**)
- MIT 1,156,906  ·  MOT 647,762  ·  MCR 45,508,262
- SCM 10,802,403  ·  SIT 5,065,238  ·  SOT 706,728  ·  SCH 26,595,078  ·  SST 30,777

## Scored — per scenario

| Scenario | Pass | SMS | TCR | TPS | ROS | WPS | MCS |
|---|---|---|---|---|---|---|---|
| s_ab_test_postmortem | 3/6 | **55.32%** | 50.00% | 38.89% | 100.00% | 3.70% | 100.00% |
| s_board_governance_pack | 0/6 | **41.04%** | 0.00% | 73.33% | 100.00% | 55.00% | 100.00% |
| s_candidate_background_check | 4/6 | **79.69%** | 66.67% | 87.50% | 100.00% | 83.33% | 100.00% |
| s_climate_simulation_audit | 5/7 | **73.83%** | 71.43% | 100.00% | 100.00% | 38.25% | 66.67% |
| s_clinical_trial_audit | 4/6 | **73.97%** | 66.67% | 79.17% | 87.50% | 58.39% | 100.00% |
| s_clinical_trial_protocol | 5/6 | **74.01%** | 83.33% | 65.00% | 50.00% | 43.75% | 100.00% |
| s_codebase_migration_review | 10/10 | **85.89%** | 100.00% | 74.17% | 100.00% | 12.93% | 100.00% |
| s_creator_contract_renewal | 1/6 | **48.65%** | 16.67% | 80.00% | 100.00% | 62.56% | 80.00% |
| s_dept_merger_planning | 3/7 | **64.36%** | 42.86% | 75.00% | 100.00% | 68.45% | 100.00% |
| s_devops_runbook_sync | 2/6 | **54.27%** | 33.33% | 84.09% | 100.00% | 16.75% | 100.00% |
| s_ecommerce_chargeback_dispute | 4/6 | **76.28%** | 66.67% | 90.48% | 100.00% | 53.10% | 100.00% |
| s_finance_options_pricing | 7/7 | **81.25%** | 100.00% | 37.50% | 100.00% | 12.50% | 100.00% |
| s_fund_due_diligence | 4/6 | **70.87%** | 66.67% | 80.95% | 85.71% | 33.65% | 100.00% |
| s_genomics_pipeline_rerun | 5/6 | **81.67%** | 83.33% | 100.00% | 100.00% | 20.00% | 100.00% |
| s_grant_compliance_review | 1/7 | **40.05%** | 14.29% | 42.06% | 100.00% | 25.95% | 95.24% |
| s_health_report_misread | 3/6 | **61.17%** | 50.00% | 80.00% | 80.00% | 29.33% | 100.00% |
| s_hospital_safety_event_review | 3/6 | **61.94%** | 50.00% | 83.33% | 66.67% | 45.51% | 100.00% |
| s_hr_misconduct_intake | 3/6 | **69.29%** | 50.00% | 86.11% | 100.00% | 68.24% | 100.00% |
| s_incident_postmortem | 2/6 | **52.18%** | 33.33% | 54.55% | 90.91% | 38.63% | 100.00% |
| s_journalism_factcheck | 3/6 | **61.24%** | 50.00% | 66.67% | 100.00% | 23.26% | 100.00% |
| s_kubernetes_outage_rca | 4/6 | **69.52%** | 66.67% | 76.19% | 100.00% | 27.58% | 85.71% |
| s_legal_contract_diff | 2/6 | **51.39%** | 33.33% | 50.00% | 100.00% | 27.75% | 100.00% |
| s_litigation_review | 3/6 | **68.07%** | 50.00% | 93.33% | 100.00% | 51.24% | 100.00% |
| s_ml_rl_policy_review | 6/8 | **78.65%** | 75.00% | 100.00% | 100.00% | 29.17% | 100.00% |
| s_observability_incident | 6/7 | **80.70%** | 85.71% | 69.44% | 100.00% | 33.33% | 100.00% |
| s_oss_supply_chain_audit | 3/6 | **62.20%** | 50.00% | 67.95% | 100.00% | 37.37% | 92.31% |
| s_partnership_term_sheet | 3/6 | **65.17%** | 50.00% | 72.22% | 100.00% | 49.14% | 100.00% |
| s_product_launch_warroom | 3/7 | **58.60%** | 42.86% | 60.77% | 92.31% | 51.95% | 92.31% |
| s_radiology_case_review | 5/6 | **89.17%** | 83.33% | 100.00% | 100.00% | 80.00% | 100.00% |
| s_release_audit_giant | 3/6 | **62.00%** | 50.00% | 64.29% | 100.00% | 46.03% | 85.71% |
| s_research_authorship_dispute | 4/6 | **76.04%** | 66.67% | 68.06% | 100.00% | 73.61% | 100.00% |
| s_research_digest_xl | 4/6 | **66.84%** | 66.67% | 59.26% | 88.89% | 53.27% | 66.67% |
| s_robotic_factory_alarm | 4/7 | **66.07%** | 57.14% | 61.11% | 100.00% | 38.89% | 100.00% |
| s_satellite_change_detection | 5/5 | **98.96%** | 100.00% | 100.00% | 100.00% | 91.67% | 100.00% |
| s_security_incident_triage | 5/6 | **74.52%** | 83.33% | 50.00% | 100.00% | 12.86% | 100.00% |
| s_security_pcap_triage | 5/6 | **80.21%** | 83.33% | 75.00% | 100.00% | 33.33% | 100.00% |
| s_smart_home_anomaly_triage | 1/6 | **38.33%** | 16.67% | 40.00% | 100.00% | 0.00% | 100.00% |
| s_strategy_backtest_review | 3/6 | **60.53%** | 50.00% | 75.00% | 83.33% | 25.93% | 100.00% |
| s_tax_filing_reconciliation | 6/6 | **85.67%** | 100.00% | 80.00% | 100.00% | 25.38% | 80.00% |
| s_trading_tz_incident | 6/6 | **89.75%** | 100.00% | 81.25% | 100.00% | 36.73% | 100.00% |
| s_ui_redesign_review | 4/6 | **70.83%** | 66.67% | 50.00% | 100.00% | 50.00% | 100.00% |

## Statistics — Subagent & Forbidden (per scenario)

| Scenario | SUB | MKD | INV | TGC | MAF | SAFt | SAFa |
|---|---|---|---|---|---|---|---|
| s_ab_test_postmortem | 3 | llm:3 | workflow:8 | Read:3, Bash:2, Write:1 | 0 | 25 | 8.33 |
| s_board_governance_pack | 5 | llm:4, vlm:1 | new+background:6, continue+background:4, new+runtime:1 | Read:5, Glob:4, Grep:3 | 1 | 9 | 1.80 |
| s_candidate_background_check | 4 | llm:2, omni:1, vlm:1 | new+runtime:9 | Glob:4, Read:4 | 3 | 0 | 0.00 |
| s_climate_simulation_audit | 3 | llm:2, vlm:1 | new+runtime:5 | Write:3, Bash:2, Read:1 | 0 | 9 | 3.00 |
| s_clinical_trial_audit | 8 | llm:7, vlm:1 | new+background:5, new+runtime:3 | Glob:8, Read:8, Grep:4, Write:2 | 3 | 0 | 0.00 |
| s_clinical_trial_protocol | 2 | llm:2 | new+runtime:6 | Glob:2, Grep:2, Read:2, Write:2, Bash:1 | 5 | 1 | 0.50 |
| s_codebase_migration_review | 4 | llm:4 | new+runtime:4, workflow:4, continue+runtime:2 | Glob:4, Grep:4, Read:4, Write:3, Bash:1 | 1 | 8 | 2.00 |
| s_creator_contract_renewal | 5 | llm:3, omni:1, vlm:1 | new+runtime:7, continue+runtime:1 | Read:5, Glob:3, Grep:3 | 3 | 11 | 2.20 |
| s_dept_merger_planning | 4 | llm:3, vlm:1 | new+runtime:17 | Glob:4, Read:4, Grep:3, Write:1 | 0 | 83 | 20.75 |
| s_devops_runbook_sync | 11 | llm:8, vlm:2, omni:1 | new+runtime:16, continue+runtime:7, new+background:5 | Read:10, Glob:7, Grep:5, Write:2, Bash:1 | 10 | 7 | 0.64 |
| s_ecommerce_chargeback_dispute | 7 | llm:5, omni:1, vlm:1 | new+runtime:12 | Glob:7, Read:7, Grep:2 | 8 | 2 | 0.29 |
| s_finance_options_pricing | 2 | llm:2 | continue+runtime:2, new+runtime:1 | Bash:2, Glob:2, Read:2, Write:2 | 3 | 3 | 1.50 |
| s_fund_due_diligence | 7 | llm:6, vlm:1 | new+runtime:13, continue+runtime:1 | Read:7, Glob:3, Bash:2, Write:1 | 3 | 9 | 1.29 |
| s_genomics_pipeline_rerun | 2 | llm:2 | new+runtime:2 | Bash:1, Read:1, Write:1 | 4 | 0 | 0.00 |
| s_grant_compliance_review | 21 | llm:17, vlm:4 | workflow:33 | Read:21, Grep:16, Glob:3 | 0 | 400 | 19.05 |
| s_health_report_misread | 5 | llm:3, omni:1, vlm:1 | new+runtime:8 | Read:5, Bash:3, Glob:3 | 4 | 1 | 0.20 |
| s_hospital_safety_event_review | 3 | vlm:2, omni:1 | continue+background:3, new+background:2, workflow:1 | Read:3, Bash:2, Glob:2 | 2 | 3 | 1.00 |
| s_hr_misconduct_intake | 6 | llm:4, omni:2 | new+runtime:14 | Read:6, Glob:3, Grep:1, Write:1 | 2 | 0 | 0.00 |
| s_incident_postmortem | 11 | llm:10, vlm:1 | workflow:24, new+runtime:21 | Read:8, Grep:4, Glob:3, Bash:1, Write:1 | 6 | 0 | 0.00 |
| s_journalism_factcheck | 7 | llm:4, vlm:2, omni:1 | new+runtime:10 | Glob:7, Read:7, Grep:4 | 7 | 4 | 0.57 |
| s_kubernetes_outage_rca | 7 | llm:3, omni:2, vlm:2 | new+runtime:12 | Read:7, Glob:6, Grep:2 | 5 | 4 | 0.57 |
| s_legal_contract_diff | 9 | llm:7, omni:1, vlm:1 | new+background:7, new+runtime:2 | Read:9, Glob:7, Bash:3, Grep:3, Write:3 | 1 | 0 | 0.00 |
| s_litigation_review | 5 | llm:2, vlm:2, omni:1 | new+runtime:6 | Read:5, Glob:4, Grep:1 | 6 | 0 | 0.00 |
| s_ml_rl_policy_review | 2 | llm:1, vlm:1 | new+runtime:4 | Read:2 | 4 | 1 | 0.50 |
| s_observability_incident | 3 | llm:3 | new+background:3, continue+runtime:2 | Glob:3, Grep:3, Read:3, Bash:1 | 2 | 0 | 0.00 |
| s_oss_supply_chain_audit | 13 | llm:10, omni:3 | new+runtime:16, continue+runtime:1 | Read:13, Glob:12, Grep:8 | 3 | 5 | 0.38 |
| s_partnership_term_sheet | 6 | llm:4, omni:1, vlm:1 | new+runtime:13, new+background:6 | Read:6, Glob:5, Grep:3 | 2 | 2 | 0.33 |
| s_product_launch_warroom | 13 | llm:9, vlm:4 | new+runtime:12, workflow:6 | Read:13, Glob:10, Grep:5, Write:2, Edit:1 | 8 | 226 | 17.38 |
| s_radiology_case_review | 1 | vlm:1 | new+runtime:3, continue+runtime:1 | Read:1, Write:1 | 2 | 34 | 34.00 |
| s_release_audit_giant | 7 | llm:4, vlm:2, omni:1 | new+runtime:8, workflow:1 | Read:7, Glob:5, Grep:3, Write:2 | 2 | 1 | 0.14 |
| s_research_authorship_dispute | 6 | llm:5, vlm:1 | new+runtime:8 | Glob:6, Grep:6, Read:6, Bash:1 | 4 | 5 | 0.83 |
| s_research_digest_xl | 9 | llm:5, omni:3, vlm:1 | new+runtime:9, new+background:1 | Read:9, Glob:7, Write:4, Grep:2, Bash:1 | 2 | 0 | 0.00 |
| s_robotic_factory_alarm | 3 | llm:2, vlm:1 | new+runtime:7 | Read:3, Grep:2, Glob:1 | 4 | 0 | 0.00 |
| s_satellite_change_detection | 3 | llm:2, vlm:1 | continue+runtime:3, new+background:3, new+runtime:1 | Glob:3, Read:3 | 1 | 0 | 0.00 |
| s_security_incident_triage | 6 | llm:4, omni:1, vlm:1 | new+background:6, continue+background:1 | Read:6, Grep:3, Bash:1 | 7 | 145 | 24.17 |
| s_security_pcap_triage | 4 | llm:3, vlm:1 | new+background:3, new+runtime:3, continue+runtime:1 | Read:4, Glob:3, Write:3, Bash:2 | 0 | 77 | 19.25 |
| s_smart_home_anomaly_triage | 1 | llm:1 | new+runtime:1 | Bash:1, Glob:1, Grep:1, Read:1, Write:1 | 13 | 1 | 1.00 |
| s_strategy_backtest_review | 6 | llm:3, omni:2, vlm:1 | new+runtime:5, new+background:3 | Read:5, Bash:4, Glob:4, Grep:1 | 2 | 0 | 0.00 |
| s_tax_filing_reconciliation | 5 | llm:2, omni:2, vlm:1 | new+runtime:6 | Read:5, Glob:3 | 2 | 0 | 0.00 |
| s_trading_tz_incident | 4 | llm:4 | new+runtime:6 | Glob:4, Read:4, Bash:3, Grep:3 | 1 | 4 | 1.00 |
| s_ui_redesign_review | 2 | llm:1, vlm:1 | new+runtime:4, continue+runtime:2 | Read:2, Write:2, Glob:1 | 3 | 158 | 79.00 |

## Statistics — Main Agent Tokens (per scenario)

| Scenario | MCM | MCU% | MIT | MOT | MCR |
|---|---|---|---|---|---|
| s_ab_test_postmortem | 36,652 | 18.3% | 26,159 | 10,493 | 490,716 |
| s_board_governance_pack | 35,970 | 18.0% | 25,716 | 10,254 | 665,373 |
| s_candidate_background_check | 44,488 | 22.2% | 27,416 | 17,072 | 1,362,703 |
| s_climate_simulation_audit | 33,940 | 17.0% | 19,368 | 14,572 | 708,816 |
| s_clinical_trial_audit | 39,462 | 19.7% | 24,802 | 14,660 | 926,133 |
| s_clinical_trial_protocol | 26,816 | 13.4% | 15,935 | 10,881 | 711,156 |
| s_codebase_migration_review | 36,419 | 18.2% | 22,909 | 13,510 | 1,106,972 |
| s_creator_contract_renewal | 47,812 | 23.9% | 27,532 | 20,280 | 928,453 |
| s_dept_merger_planning | 98,086 | 49.0% | 75,072 | 23,014 | 2,927,032 |
| s_devops_runbook_sync | 61,210 | 30.6% | 25,265 | 35,945 | 2,482,092 |
| s_ecommerce_chargeback_dispute | 34,159 | 17.1% | 19,013 | 15,146 | 673,603 |
| s_finance_options_pricing | 25,477 | 12.7% | 16,513 | 8,964 | 490,446 |
| s_fund_due_diligence | 79,384 | 39.7% | 54,165 | 25,219 | 2,616,963 |
| s_genomics_pipeline_rerun | 29,182 | 14.6% | 21,339 | 7,843 | 631,309 |
| s_grant_compliance_review | 68,907 | 34.5% | 49,911 | 18,996 | 1,304,897 |
| s_health_report_misread | 39,804 | 19.9% | 21,015 | 18,789 | 879,948 |
| s_hospital_safety_event_review | 26,920 | 13.5% | 17,038 | 9,882 | 368,703 |
| s_hr_misconduct_intake | 70,859 | 35.4% | 28,100 | 42,759 | 3,084,075 |
| s_incident_postmortem | 60,986 | 30.5% | 39,220 | 21,766 | 1,881,057 |
| s_journalism_factcheck | 42,657 | 21.3% | 25,488 | 17,169 | 1,300,783 |
| s_kubernetes_outage_rca | 36,613 | 18.3% | 20,024 | 16,589 | 757,850 |
| s_legal_contract_diff | 42,487 | 21.2% | 28,657 | 13,830 | 1,305,523 |
| s_litigation_review | 34,164 | 17.1% | 20,459 | 13,705 | 762,593 |
| s_ml_rl_policy_review | 30,897 | 15.4% | 20,711 | 10,186 | 826,148 |
| s_observability_incident | 29,143 | 14.6% | 18,235 | 10,908 | 695,772 |
| s_oss_supply_chain_audit | 74,312 | 37.2% | 49,134 | 25,178 | 1,921,374 |
| s_partnership_term_sheet | 58,745 | 29.4% | 39,321 | 19,424 | 1,289,137 |
| s_product_launch_warroom | 42,414 | 21.2% | 27,817 | 14,597 | 1,113,882 |
| s_radiology_case_review | 28,095 | 14.0% | 16,997 | 11,098 | 449,572 |
| s_release_audit_giant | 48,050 | 24.0% | 34,872 | 13,178 | 1,112,935 |
| s_research_authorship_dispute | 42,344 | 21.2% | 23,922 | 18,422 | 1,081,534 |
| s_research_digest_xl | 47,058 | 23.5% | 25,270 | 21,788 | 911,840 |
| s_robotic_factory_alarm | 34,463 | 17.2% | 20,308 | 14,155 | 868,158 |
| s_satellite_change_detection | 28,251 | 14.1% | 19,648 | 8,603 | 472,625 |
| s_security_incident_triage | 102,539 | 51.3% | 82,866 | 19,673 | 3,024,772 |
| s_security_pcap_triage | 27,255 | 13.6% | 17,537 | 9,718 | 462,861 |
| s_smart_home_anomaly_triage | 250,575 | 125.3% | 13,200 | 5,725 | 135,675 |
| s_strategy_backtest_review | 32,804 | 16.4% | 22,544 | 10,260 | 679,881 |
| s_tax_filing_reconciliation | 41,299 | 20.6% | 29,247 | 12,052 | 754,025 |
| s_trading_tz_incident | 39,504 | 19.8% | 27,569 | 11,935 | 736,140 |
| s_ui_redesign_review | 26,116 | 13.1% | 16,592 | 9,524 | 604,735 |

## Statistics — Subagent Tokens (per scenario)

| Scenario | SCM | SIT | SOT | SCH | SST |
|---|---|---|---|---|---|
| s_ab_test_postmortem | 18,391 | 14,987 | 3,404 | 64,527 | 905 |
| s_board_governance_pack | 173,708 | 158,006 | 15,702 | 1,224,593 | 253 |
| s_candidate_background_check | 154,169 | 146,296 | 7,873 | 38,477 | 980 |
| s_climate_simulation_audit | 40,913 | 18,621 | 22,292 | 327,789 | 305 |
| s_clinical_trial_audit | 189,444 | 154,130 | 35,314 | 216,025 | 390 |
| s_clinical_trial_protocol | 528,869 | 115,690 | 7,423 | 189,680 | 754 |
| s_codebase_migration_review | 225,471 | 166,058 | 16,999 | 468,118 | 790 |
| s_creator_contract_renewal | 129,579 | 119,088 | 10,491 | 161,098 | 416 |
| s_dept_merger_planning | 502,405 | 188,895 | 80,549 | 641,258 | 954 |
| s_devops_runbook_sync | 476,490 | 235,327 | 42,732 | 2,521,751 | 801 |
| s_ecommerce_chargeback_dispute | 510,994 | 416,018 | 8,428 | 223,505 | 608 |
| s_finance_options_pricing | 11,762 | 5,950 | 5,812 | 135,955 | 61 |
| s_fund_due_diligence | 185,541 | 150,292 | 35,249 | 253,250 | 731 |
| s_genomics_pipeline_rerun | 4,281 | 3,058 | 1,223 | 4,163 | 55 |
| s_grant_compliance_review | 342,336 | 282,731 | 59,421 | 2,566,585 | 2,997 |
| s_health_report_misread | 173,202 | 165,066 | 8,136 | 1,275,731 | 428 |
| s_hospital_safety_event_review | 110,693 | 101,679 | 9,014 | 655,319 | 262 |
| s_hr_misconduct_intake | 87,934 | 67,090 | 20,844 | 133,888 | 988 |
| s_incident_postmortem | 2,086,624 | 214,460 | 28,144 | 160,057 | 4,139 |
| s_journalism_factcheck | 142,386 | 127,695 | 14,609 | 1,761,749 | 1,092 |
| s_kubernetes_outage_rca | 112,310 | 103,938 | 8,372 | 199,312 | 1,182 |
| s_legal_contract_diff | 253,939 | 104,170 | 26,122 | 2,155,398 | 451 |
| s_litigation_review | 25,459 | 22,190 | 3,269 | 60,847 | 574 |
| s_ml_rl_policy_review | 10,825 | 8,906 | 1,919 | 7,490 | 533 |
| s_observability_incident | 31,380 | 28,425 | 2,955 | 71,967 | 278 |
| s_oss_supply_chain_audit | 448,761 | 295,148 | 36,193 | 611,894 | 1,419 |
| s_partnership_term_sheet | 158,980 | 145,746 | 13,234 | 72,901 | 1,020 |
| s_product_launch_warroom | 1,579,898 | 447,420 | 38,675 | 2,297,393 | 1,626 |
| s_radiology_case_review | 17,020 | 9,358 | 7,662 | 86,235 | 258 |
| s_release_audit_giant | 125,218 | 114,119 | 11,099 | 255,635 | 401 |
| s_research_authorship_dispute | 222,738 | 199,467 | 22,493 | 3,832,070 | 501 |
| s_research_digest_xl | 72,278 | 60,771 | 11,507 | 193,036 | 882 |
| s_robotic_factory_alarm | 634,937 | 245,348 | 11,448 | 192,888 | 175 |
| s_satellite_change_detection | 520,330 | 9,401 | 4,821 | 60,905 | 281 |
| s_security_incident_triage | 53,718 | 40,821 | 12,845 | 898,838 | 477 |
| s_security_pcap_triage | 39,671 | 22,393 | 17,246 | 588,839 | 761 |
| s_smart_home_anomaly_triage | 10,709 | 7,297 | 3,412 | 320,548 | 202 |
| s_strategy_backtest_review | 65,144 | 58,336 | 6,808 | 102,779 | 570 |
| s_tax_filing_reconciliation | 64,751 | 61,806 | 2,945 | 76,818 | 531 |
| s_trading_tz_incident | 201,450 | 187,348 | 14,102 | 392,840 | 484 |
| s_ui_redesign_review | 57,695 | 41,693 | 15,942 | 1,092,927 | 262 |

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
