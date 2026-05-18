# hil_d3 Sub-Plan: ICU Nursing Staffing Crisis Investigation

> Scene: Chief of Cardiology Dr. Tanaka investigates systematic overtime under-reporting
> in the Cardiac ICU at Pacific Highlands Medical Center.

---

## 一、场景概要

- **Scene ID**: hil_d3
- **User/Persona**: Dr. Tanaka, Chief of Cardiology / Acting Medical Director
- **Language**: **English** (original questions.json is English)
- **Total rounds**: 30 (8 MC + 22 EC = 73.3% EC)
- **Updates**: 4 updates, evenly spaced (~every 6 rounds)

---

## 二、Dr. Tanaka 偏好规则 (P1–P5)

| Rule | Description | Check logic |
|------|------------|-------------|
| P1 | Clinical evidence hierarchy: badge/manual records > system-generated > anecdotal | Document explicitly states evidence hierarchy or source credibility ranking |
| P2 | Precise clinical metrics (exact hours/week, nurse IDs, ratios) — no vague descriptions | Contains specific numbers (h/week, nurse counts, percentages) |
| P3 | Files named with date prefix and clinical context (e.g., YYYY-MM-DD_audit.md) | ≥1 file in docs/ with `YYYY-MM-DD_` prefix |
| P4 | Cross-source verification: explicitly state when two+ independent sources agree | "cross-" or "corroborat" or "independent" or "verified by" present |
| P5 | Regulatory context: cite specific regulation when discussing compliance | Cite WAC 246-840-711 or CMS or RCW 70.41.230 or "accreditation" |

check_preferences.py P rules:
- P1: check for "badge" AND "CareScheduler" with comparison language ("actual" vs "reported" or "scheduled")
- P2: regex `\b\d+\.?\d*\s*h(?:ours?)?/week\b` ≥2 matches
- P3: ≥1 file in docs/ matching `^\d{4}-\d{2}-\d{2}_`
- P4: any of ("cross-verified", "corroborated", "independently confirmed", "both sources") present
- P5: any of ("WAC 246-840-711", "RCW 70.41.230", "CMS", "Joint Commission") present

---

## 三、关键数值（Ground Truth）

| Fact | Value | Source |
|------|-------|--------|
| CareScheduler avg hours/week | **42.3 h/week** | overtime_audit_report.md (upd1) |
| Actual avg hours/week (badge) | **58.4 h/week** | badge_access_analysis.md (upd2) |
| Discrepancy avg | **16.1 h/week per nurse** | calculated |
| Amy Chen (RN-02) CareScheduler | 41.6 h/week | overtime_audit_report.md |
| Amy Chen (RN-02) actual | **68.4 h/week** | badge_access_analysis.md |
| Tanya Williams (RN-05) actual | **70.3 h/week** | badge_access_analysis.md |
| Jessica Martinez (RN-07) actual | **68.9 h/week** | badge_access_analysis.md |
| Nurses exceeding 48h/week | **7 of 11** | badge_access_analysis.md |
| Nurses exceeding 60h/week | **3 of 11** | badge_access_analysis.md |
| Legal threshold | **48 h/week (WAC 246-840-711)** | icu_staffing_policy.md |
| Cognitive impairment threshold | **60 h/week (Trinkoff 2011)** | sarahkim_symptom_timeline.md (upd3) |
| Near-miss events documented | **2** (NM-1 dosage confusion, NM-2 wrong-route) | sarahkim_symptom_timeline.md (upd3) |
| ClinAlert Q1 2026 submissions | 3 (vs 9 in Q4 2025) | caresched_audit_findings.md (upd4) |
| Decline in ClinAlert | **67% decline** | calculated: (9-3)/9 |
| Systematic practice duration | **4+ months** (Nov 2025 – Mar 2026) | caresched_audit_findings.md (upd4) |
| Staff nurses affected | **9 of 11** (charge nurses excluded) | caresched_audit_findings.md (upd4) |
| Mandatory reporting deadline | RCW 70.41.230, 72 hours | caresched_audit_findings.md (upd4) |
| Sick leave rate | 4.2 days/FTE/quarter (BELOW hospital 4.6) | hr_staffing_metrics.md |
| Monthly overtime budget | $42,000 budgeted, $38,400 actual | hr_staffing_metrics.md |
| FTE gap | 2 FTE short (11 actual vs 13 target) | nurse_roster_current.md |
| Linda Yee instruction | "enter the scheduled hours...administration needs clean numbers" | caresched_audit_findings.md (upd4) |

---

## 四、矛盾（C1–C4）

- **C1**: CareScheduler shows 100% compliance (avg 42.3h); badge/manual audit shows 7/11 nurses >48h (avg 58.4h) — systematic under-reporting
- **C2**: HR reports low sick leave (4.2 d/FTE < hospital avg 4.6) suggesting healthy unit; clinical reality shows burnout via presenteeism, 2 near-misses, 3 nurses job-hunting
- **C3**: ClinAlert shows only 3 Q1 events (67% decline from Q4) suggesting safer unit; Walsh/Kim documentation shows 5+ actual near-miss events unreported
- **C4**: Angela's preliminary review (CareScheduler-only) found "minor documentation gaps, overall satisfactory"; full audit with badge data reveals systematic 4-month falsification requiring mandatory reporting

---

## 五、Update 触发设计

| Update ID | Trigger Round | Files | What it reveals |
|-----------|--------------|-------|----------------|
| upd1_workspace | q5 | overtime_audit_report.md | Walsh's 4-week independent audit: 9 nurses underreported by avg 16.1h/week; Amy Chen 68.4h, Tanya Williams 70.3h, Jessica Martinez 68.9h |
| upd2_workspace | q10 | badge_access_analysis.md | Marcus Okafor IT badge analysis confirms Walsh's data; 7/11 nurses >48h; cross-validates manual records |
| upd3_workspace, upd3_sessions (if exist) | q17 | sarahkim_symptom_timeline.md | Sarah Kim's 8-week symptom log: 20-30% decision latency, NM-1 (19h shift dosage confusion), NM-2 (wrong-route admin); presenteeism > absenteeism |
| upd4_workspace | q23 | caresched_audit_findings.md | Angela's formal finding: F1 systematic circumvention, F2 9/11 nurses, F3 patient safety implications, F4 mandatory RCW reporting required |

Note: If upd2_sessions, upd3_sessions, upd4_sessions exist in the data directory, include them; otherwise upd2/3/4 may be workspace-only.

---

## 六、题目序列设计（30 轮）

### Phase 1: 初始信号 (q1–q4)

**q1** [MC]
- Topic: Initial evidence from workspace documents
- Based on shift_schedule_published.md + incident_log_icucardiac.md + hr_staffing_metrics.md
- Answer: HR metrics show low sick leave but informal near-miss concerns; CareScheduler shows compliant numbers; staffing gap of 2 FTE is documented

**q2** [MC]
- Topic: Identifying C1 conflict signal
- Question: "Which statements about the discrepancy between published schedules and clinical staff observations are supported by current available evidence?"
- Answer: conflict exists but unconfirmed without independent audit; HR data measures wrong variable (absenteeism not burnout)

**q3** [EC, L2, pref:P2,P3]
- Task: Create `analysis/initial_staffing_assessment.md` — analyze staffing metrics from workspace docs; compare FTE gap (11 vs 13 target), published schedule compliance, sick leave data
- check_initial_staffing.py: validates "11" AND "13" present (FTE actual vs target), "42.3" or "42" (CareScheduler avg) present, ≥3 ## headings

**q4** [EC, L2]
- Task: Create `analysis/hr_metrics_interpretation.md` — explain why HR's low sick leave (4.2 < 4.6 avg) might actually indicate presenteeism rather than unit health; contrast absenteeism vs presenteeism in ICU context
- check_hr_metrics.py: validates "4.2" AND "4.6" present, "presenteeism" OR "showing up impaired" OR "absenteeism" present, ≥2 ## headings

### Phase 2: upd1 후 — Walsh 审计 (q5–q9)

**q5** [MC, update_ids: upd1_workspace]
- Topic: Walsh's overtime audit findings
- Question: "After reviewing the Walsh overtime audit report (Update 1), which statements are now supported?"
- Answer: 9 nurses underreporting avg 16.1h/week; Amy Chen 68.4h; Tanya Williams 70.3h; Jessica Martinez 68.9h; charge nurses' records ARE accurate (key asymmetry)

**q6** [EC, L2]
- Task: Create `analysis/staffing_discrepancy_table.md` — a Markdown table with columns: Nurse ID, CareScheduler hours/week, Actual hours/week, Discrepancy, Above threshold (Y/N)
- Must include all 11 nurses; 7 flagged as above 48h threshold; 3 above 60h
- check_staffing_table.py: validates "68.4" OR "Amy Chen" present, "70.3" OR "Tanya Williams" present, "68.9" OR "Jessica Martinez" present, "42.3" and "58.4" present (averages), ≥7 rows of data

**q7** [EC, L2]
- Task: Create `analysis/threshold_violation_analysis.json` — JSON array of nurses exceeding 48h threshold; each entry: `nurse_id`, `caresched_hours`, `actual_hours`, `discrepancy`, `exceeds_48h`, `exceeds_60h`
- check_threshold_violations.py: validates JSON, 7 entries with exceeds_48h=true, 3 with exceeds_60h=true, Amy Chen entry has actual_hours close to 68.4

**q8** [EC, L2, pref:P1,P4]
- Task: Create `analysis/evidence_source_hierarchy.md` — document evidence source credibility hierarchy: badge data > manual audit > CareScheduler; explain why charge nurse records (accurate) vs staff records (understated) is statistically significant
- check_evidence_hierarchy.py: validates "badge" AND "CareScheduler" present with comparison, "charge nurse" present, "< 1%" or "statistical" or "systematic" present, ≥3 ## headings

**q9** [EC, L2]
- Task: Create `analysis/financial_impact_assessment.md` — calculate financial implications: budgeted $42K/month overtime vs actual $38.4K actual (budget appears fine) because extra hours weren't recorded as overtime; estimate true overtime cost
- check_financial_impact.py: validates "$42,000" or "42,000" present, "$38,400" or "38,400" present, "under-reported" or "hidden" or "unrecorded" cost analysis, ≥2 ## headings

### Phase 3: upd2 후 — Badge 数据交叉验证 (q10–q16)

**q10** [MC, update_ids: upd2_workspace]
- Topic: Badge access analysis confirms Walsh
- Question: "After reviewing the badge access analysis (Update 2), which statements about the cross-verification of staffing data are supported?"
- Answer: badge data independently confirms Walsh findings; charge nurses accurate; pattern is systematic not random (< 1% probability); 7/11 nurses confirmed >48h

**q11** [EC, L2]
- Task: Create `analysis/cross_source_validation.md` — document how badge data (Tier 1) + Walsh manual audit (Tier 1) + CareScheduler (Tier 3) compare; explicitly state two independent sources agree
- check_cross_validation.py: validates "badge" AND "Walsh" present, "independent" OR "corroborat" OR "cross-verify" present, "CareScheduler" mentioned as lower reliability, ≥3 ## headings

**q12** [EC, L2]
- Task: Create `analysis/charge_nurse_pattern_analysis.md` — analyze the asymmetry: charge nurses (Donna Park, David Okafor) have accurate records; staff nurses systematically understated; statistical improbability of random error
- check_charge_nurse.py: validates "Donna Park" or "RN-01" present, "David Okafor" or "RN-06" present, "< 1%" or "statistically" or "systematic" present, asymmetry analysis

**q13** [EC, L2, pref:P5]
- Task: Create `docs/YYYY-MM-DD_staffing_audit_brief.md` — brief for Angela Reeves summarizing discrepancy findings; must cite WAC 246-840-711 (48h limit) and reference clinical safety thresholds (JONA 2010: 12.5h shift = 3x error risk)
- check_staffing_brief.py: validates docs/ date-prefixed file exists, "WAC 246-840-711" OR "48 h" OR "48 hours" present, "JONA" or "12.5" or "3x" present, ≥4 ## headings

**q14** [EC, L2]
- Task: Create `analysis/reporting_culture_analysis.md` — explain why ClinAlert submissions declined 67% (from 9 to 3) despite increased stress; link to charge nurse informal signals and fear culture
- check_reporting_culture.py: validates "9" AND "3" present (Q4 vs Q1 ClinAlert), "67%" or "67 percent" or "decline" present, "informal" or "culture" or "under-reported" present, ≥3 ## headings

**q15** [EC, L2]
- Task: Create `scripts/compute_staffing_stats.py` — Python script that reads `overtime_audit_report.md` and `badge_access_analysis.md` from ${workspace}, and computes: (1) average discrepancy, (2) number of nurses > 48h, (3) number of nurses > 60h; prints to stdout as JSON
- eval.command: `cd ${workspace} && python scripts/compute_staffing_stats.py 2>&1 | python3 -c "import sys, json; d=json.load(sys.stdin); sys.exit(0 if d.get('nurses_above_48h')==7 and d.get('nurses_above_60h')==3 else 1)"`
- eval.timeout: 30

**q16** [EC, L2]
- Task: Create `analysis/near_miss_risk_model.md` — model the clinical risk: 3 nurses at >60h/week match Trinkoff 2011 (BAC 0.08% equivalent); JONA 2010 threshold violated; link to 2 unreported near-miss events
- check_near_miss_risk.py: validates "Trinkoff" or "60" (hours) + "BAC" or "cognitive" present, "JONA" or "12.5" or "3x" present, "near-miss" present, ≥3 ## headings

### Phase 4: upd3 후 — 临床症状证据 (q17–q22)

**q17** [MC, update_ids: upd3_workspace]
- Topic: Sarah Kim's symptom timeline and near-miss events
- Question: "After reviewing Sarah Kim's symptom timeline (Update 3), which statements about clinical impact are now supported?"
- Answer: NM-1 (dosage confusion at 3:15 AM, 19-hour shift), NM-2 (wrong-route admin, hour 14 of 12h shift); 20-30% decision latency increase; zero ClinAlert filed for either event

**q18** [EC, L2]
- Task: Create `analysis/near_miss_event_log.json` — JSON array of documented near-miss events; each entry: `event_id`, `date_approx`, `type`, `shift_duration_h`, `caught_by`, `clinalert_filed`, `evidence_source`
- check_near_miss_log.py: validates JSON, 2 entries (NM-1 dosage confusion, NM-2 wrong-route), NM-1 has shift_duration ≥19 or ≥18, NM-2 has shift_duration ≥14, clinalert_filed=false for both

**q19** [EC, L2]
- Task: Create `analysis/presenteeism_vs_absenteeism.md` — explain why ICU presenteeism is more dangerous than absenteeism; why HR sick leave metric (4.2 d/FTE) creates false sense of safety; cite Sarah Kim quote
- check_presenteeism.py: validates "4.2" AND "4.6" present, "presenteeism" present, "impaired" or "fatigue" present, ≥3 ## headings

**q20** [EC, L2]
- Task: Create `analysis/retention_risk_assessment.json` — JSON documenting retention risk: nurses actively job-hunting, estimated timeline for departures, impact if one leaves before fill
- check_retention_risk.py: validates JSON, "Amy Chen" or similar mentioned as actively seeking, "3" nurses at risk, "Swedish" or "per diem" or specific evidence

**q21** [EC, L2, pref:P1,P2,P4]
- Task: Create `docs/YYYY-MM-DD_clinical_safety_impact_report.md` — clinical impact report for Dr. Tanaka's records; must: date-prefixed, explicit evidence source hierarchy (P1), specific metrics (P2), cross-source verification stated (P4)
- check_clinical_impact.py: validates docs/ date-prefixed file, "NM-1" or "near-miss" present, "WAC" or regulation cited (P5), "68.4" or Amy Chen data present, ≥5 ## headings

**q22** [EC, L2]
- Task: Create `analysis/four_contradiction_matrix.md` — 2×2 or table format documenting all 4 contradictions (C1–C4): C1 (schedule vs actual hours), C2 (HR low sick leave vs burnout reality), C3 (ClinAlert decline vs actual near-misses), C4 (preliminary review vs full audit)
- check_contradiction_matrix.py: validates all four Cs in document, each has "claimed" or "official" vs "actual" or "real" contrast, ≥4 ## headings or table with ≥4 rows

### Phase 5: upd4 후 — 正式调查结论 (q23–q30)

**q23** [MC, update_ids: upd4_workspace]
- Topic: Angela's formal audit findings
- Question: "After receiving Angela's formal compliance audit findings (Update 4), which statements about regulatory obligations are now supported?"
- Answer: F1 systematic circumvention, F2 9/11 nurses, F3 patient safety implications (2 near-miss events), F4 mandatory RCW 70.41.230 reporting within 72 hours

**q24** [EC, L2]
- Task: Create `analysis/formal_finding_summary.json` — JSON mirroring F1–F4 findings; each: `finding_id`, `title`, `details`, `regulatory_citation`, `severity`
- check_formal_findings.py: validates JSON, 4 entries F1–F4, F4 cites "RCW 70.41.230" or "70.41.230", F1 mentions systematic/circumvention/falsif, F3 has near-miss reference

**q25** [EC, L2]
- Task: Create `analysis/linda_yee_instruction_analysis.md` — analyze the charge nurse instruction from Linda Yee ("enter scheduled hours, administration needs clean numbers"); who knew what, when; organizational accountability chain
- check_linda_yee.py: validates "Linda Yee" or "Linda" present, quoted instruction or paraphrase present ("scheduled hours" or "clean numbers"), "charge nurse" present, accountability/responsibility analysis

**q26** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_mandatory_reporting_memo.md` — memo documenting the 72-hour mandatory reporting obligation under RCW 70.41.230; scope of report (what must be included), deadline
- check_mandatory_reporting.py: validates docs/ date-prefixed file, "RCW 70.41.230" OR "70.41.230" present, "72 hours" or "72h" or "72-hour" present, ≥3 ## headings

**q27** [EC, L2]
- Task: Create `analysis/interim_corrective_measures.md` — document immediate corrective measures recommended: accurate time recording going forward, agency nursing to fill gap, mandatory ClinAlert training, RCW reporting
- check_corrective_measures.py: validates ≥4 distinct corrective actions described, "ClinAlert" or "incident reporting" present, "agency" or "temporary" or "fill the gap" present, ≥4 ## headings

**q28** [MC]
- Topic: Dr. Tanaka's analytical bias risks
- Question: "Which statements about potential analytical biases in Dr. Tanaka's investigation approach are supported by the evidence?"
- Answer: confirmation bias risk of accepting Walsh's data too readily (but mitigated by badge cross-validation); anchoring to CareScheduler data initially; systematic cross-verification approach ultimately correct

**q29** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_final_compliance_report.md` — complete final report; must follow P1–P5: evidence hierarchy (P1), precise metrics (P2), date-prefixed (P3), cross-source verification (P4), regulatory citations (P5)
- eval.command: `python ${eval_dir}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/ && python ${eval_dir}/scripts/check_final_compliance.py ${workspace}`
- check_final_compliance.py: validates docs/ date-prefixed file, "WAC 246-840-711" present, "RCW 70.41.230" present, "68.4" or "70.3" or "68.9" present (at least one critical nurse), "7" nurses and "48" hours present, "near-miss" or "NM-1" present, ≥800 chars

**q30** [MC]
- Topic: Final comprehensive regulatory judgment
- Question: "Which of the following statements represent the most accurate assessment of the regulatory situation as of the formal finding?"
- Answer: mandatory reporting triggered, systematic falsification confirmed, CMS survey would find violations, Joint Commission survey 4 months ago (before issue began) remains valid but current conditions are non-compliant

---

## 七、评测脚本清单

| Script | What to validate | Key checks |
|--------|-----------------|-----------|
| check_initial_staffing.py | analysis/initial_staffing_assessment.md | "11" and "13" FTE, "42.3" CareScheduler avg |
| check_hr_metrics.py | analysis/hr_metrics_interpretation.md | "4.2" and "4.6", "presenteeism" |
| check_staffing_table.py | analysis/staffing_discrepancy_table.md | "68.4", "70.3", "68.9", "42.3", "58.4", ≥7 data rows |
| check_threshold_violations.py | analysis/threshold_violation_analysis.json | JSON valid, 7 entries >48h, 3 entries >60h |
| check_evidence_hierarchy.py | analysis/evidence_source_hierarchy.md | badge+CareScheduler comparison, charge nurse asymmetry |
| check_financial_impact.py | analysis/financial_impact_assessment.md | "42,000", "38,400", unrecorded/hidden cost |
| check_cross_validation.py | analysis/cross_source_validation.md | badge AND Walsh, "independent" OR "corroborat" |
| check_charge_nurse.py | analysis/charge_nurse_pattern_analysis.md | "Donna Park", "systematic", "< 1%" |
| check_staffing_brief.py | docs/YYYY-MM-DD_staffing_audit_brief.md | date-prefixed in docs/, WAC 246-840-711, JONA |
| check_reporting_culture.py | analysis/reporting_culture_analysis.md | "9" and "3" ClinAlert counts, "67%" or decline |
| (inline) | scripts/compute_staffing_stats.py | JSON output with nurses_above_48h=7, nurses_above_60h=3 |
| check_near_miss_risk.py | analysis/near_miss_risk_model.md | Trinkoff/60h, JONA/12.5h, near-miss |
| check_near_miss_log.py | analysis/near_miss_event_log.json | JSON, 2 events, NM-1 ≥19h, NM-2 ≥14h, ClinAlert false |
| check_presenteeism.py | analysis/presenteeism_vs_absenteeism.md | "4.2"+"4.6", "presenteeism", "impaired" |
| check_retention_risk.py | analysis/retention_risk_assessment.json | JSON, Amy Chen/3 nurses seeking |
| check_clinical_impact.py | docs/YYYY-MM-DD_clinical_safety_impact_report.md | date-prefixed, near-miss present, WAC cited |
| check_contradiction_matrix.py | analysis/four_contradiction_matrix.md | all 4 Cs, official vs actual contrast |
| check_formal_findings.py | analysis/formal_finding_summary.json | JSON, F1–F4, F4 has RCW 70.41.230 |
| check_linda_yee.py | analysis/linda_yee_instruction_analysis.md | "Linda Yee", instruction quote, accountability |
| check_mandatory_reporting.py | docs/YYYY-MM-DD_mandatory_reporting_memo.md | date-prefixed, RCW 70.41.230, 72 hours |
| check_corrective_measures.py | analysis/interim_corrective_measures.md | ≥4 measures, ClinAlert, agency nursing |
| check_final_compliance.py | docs/YYYY-MM-DD_final_compliance_report.md | WAC+RCW present, nurse data, near-miss, ≥800 chars |
| check_preferences.py | docs/ | P1–P5 rules (scene-specific, see §二) |

---

## 八、特别注意事项

1. **q15 (L3)**: compute_staffing_stats.py reads actual workspace files; eval.command pipes output to Python for numeric validation
2. **pref rounds**: q3 (P2,P3), q8 (P1,P4), q13 (P5), q21 (P1,P2,P4) — non-scoring educational hints
3. **q29 full scoring**: --rules P1,P2,P3,P4,P5
4. **All nurse hour values**: check scripts should use floating-point comparison with ±0.2 tolerance
5. **check_preferences.py P3 rule**: "at least one file in docs/ has YYYY-MM-DD_ prefix"
