# Layer 4 -- Dynamic Updates

> This document specifies the 4 runtime updates that inject new workspace files and session appends into the scenario during evaluation.
> Each update triggers before a specific eval round, introduces new evidence, and may reverse prior agent biases or contradiction assessments.

---

## 1. Update Summary Table

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Introduce Linda's full-dataset statistical analysis (data_discrepancy_log_v2.md) and her Phase 2 DM loops; triggers C1 full reversal and B1/B2 reversal | Yes -- append 3 loops to `PLACEHOLDER_LINDA_SLACK_UUID` (Loops 17--19) | Yes -- `data_discrepancy_log_v2.md` | C1: R2->R4; B1 correction seeded; B2 correction seeded |
| U2 | Before R7 | Introduce Sato's full biostatistical report (sato_biostat_report.md) and his Phase 2 DM loops + #cardio-research Phase 2 append; triggers C4 full reversal | Yes -- append 4 loops to `PLACEHOLDER_SATO_TELEGRAM_UUID` (Loops 13--16); append 3 loops to `PLACEHOLDER_CARDIO_SLACK_UUID` (Loops 19--21) | Yes -- `sato_biostat_report.md` | C4: R6->R8 (Phase 1->Phase 2 temporal DU) |
| U3 | Before R9 | Introduce IRB formal enrollment finding (irb_preliminary_report.md) and Okonkwo Phase 2 DM loops; triggers C2 formal confirmation | Yes -- append 3 loops to `PLACEHOLDER_OKONKWO_FEISHU_UUID` (Loops 15--17) | Yes -- `irb_preliminary_report.md` | C2: R3->R9 |
| U4 | Before R11 | Introduce Osei's written rebuttal (osei_rebuttal_letter.md) and Osei Phase 2 DM loops; triggers internal contradiction identification | Yes -- append 4 loops to `PLACEHOLDER_OSEI_SLACK_UUID` (Loops 17--20) | Yes -- `osei_rebuttal_letter.md` | C1: R4->R11 (Osei internal contradiction) |

---

## 2. Update 1 -- Linda's Full-Dataset Analysis (Before R4)

### 2.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "data_discrepancy_log_v2.md",
    "source": "updates/u1_data_discrepancy_log_v2.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_LINDA_SLACK_UUID",
    "source": "updates/u1_linda_slack_phase2.jsonl"
  }
]
```

### 2.2 Source File Content Summaries

**data_discrepancy_log_v2.md:**
- Title: "PHMC-STENT-2022 Data Discrepancy Log -- Comprehensive Analysis (Version 2)"
- Author: Linda Torres, Research Coordinator
- Date: W3
- Scope: Full dataset -- all 287 participant records, 3,441 data collection events
- Methodology: Threshold value clustering analysis, Benford's Law analysis (leading digits of continuous outcome variables), identical value pair analysis, adverse event date-visit log cross-reference. All analyses replicated in R 4.3.1 and SPSS 29.
- Key findings:
  - Threshold clustering: 67/287 records (23.3%) with at least one BP at protocol threshold; expected rate <2%; chi-square = 47.3, p < 0.001
  - Benford's Law: chi-square = 89.4, df = 8, p < 0.0001; over-representation of leading digits 1 and 4 (protocol threshold values 140 mmHg, 40 bpm)
  - Identical value pairs: 19 pairs of three-decimal matches across different visit dates; probability p < 0.00001
  - Adverse event cross-reference: 14 AE forms dated on days with no visit log or appointment record
- Protocol citation: trial_protocol_excerpt.md Section 4.3 prohibits proxy coding, estimated values, and copying prior visit values -- directly contradicts Osei's verbal explanations
- Conclusion: "Statistical patterns inconsistent with random data entry error at any conventional significance level. Distributional anomalies consistent with systematic data manipulation."
- Length: ~900 words, ~1,350 tokens

**u1_linda_slack_phase2.jsonl (Loops 17--19 appended to Linda DM):**
- Loop 17: Linda submits v2 report, walks through Benford's Law (chi-square 89.4, p < 0.0001), threshold clustering (67/287, p < 0.001), identical pairs (19, p < 0.00001). Agent reads data_discrepancy_log_v2.md and explicitly corrects B2 ("proxy coding defense premature") and notes B1 revision needed.
- Loop 18: Linda reports sharing v2 findings with Sato; Sato is running GRIM and variance analyses.
- Loop 19: Linda cites trial_protocol_excerpt.md Section 4.3 -- "no substitution, proxy, or estimated values are permitted" -- establishing that Osei's lab notebook does not constitute IRB approval.

### 2.3 Runtime Checks

- [ ] File `data_discrepancy_log_v2.md` exists in workspace directory
- [ ] File contains keywords: "287 participant records", "Benford's Law", "chi-square", "p < 0.0001", "67/287", "23.3%", "19 pairs", "Section 4.3"
- [ ] Linda DM session (`PLACEHOLDER_LINDA_SLACK_UUID`) now contains Loops 17--19
- [ ] Loop 17 agent reply contains explicit B2 correction referencing trial_protocol_excerpt.md Section 4.3
- [ ] Loop 17 agent reply contains B1 revision note

### 2.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r4 | `depends_on_update` | `"u1"` |
| r4 | `update_files` | `["data_discrepancy_log_v2.md"]` |
| r4 | `update_sessions` | `["PLACEHOLDER_LINDA_SLACK_UUID"]` |
| r16 | `depends_on_update` | `"u1"` |
| r16 | `update_files` | `["data_discrepancy_log_v2.md"]` |
| r21 | `depends_on_update` | `"u1"` |
| r29 | `depends_on_update` | `"u1"` |

---

## 3. Update 2 -- Sato's Biostatistical Report (Before R7)

### 3.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "sato_biostat_report.md",
    "source": "updates/u2_sato_biostat_report.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_SATO_TELEGRAM_UUID",
    "source": "updates/u2_sato_telegram_phase2.jsonl"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_CARDIO_SLACK_UUID",
    "source": "updates/u2_cardio_slack_phase2.jsonl"
  }
]
```

### 3.2 Source File Content Summaries

**sato_biostat_report.md:**
- Title: "PHMC-STENT-2022 Independent Biostatistical Review Report"
- Author: Dr. Hiroshi Sato, PhD, Associate Professor of Biostatistics, Stanford University
- Date: W3-W4
- Methods: Benford's Law analysis, GRIM (Granularity-Related Inconsistency of Means) analysis, intra-individual variance analysis, threshold clustering analysis. Software: Stata 18, R 4.3.1.
- Key findings:
  - Benford's Law: chi-square = 92.1, p < 0.0001 (independently confirms Linda's finding)
  - GRIM analysis: 17 of 48 reported summary means are mathematically impossible given stated sample sizes and measurement precision
  - Variance compression (FOURTH ANOMALY -- unique to Sato): 14 records with intra-individual variance below 5th percentile of published norms for cardiac stent recipients; p < 0.001. Pattern consistent with generated rather than measured values.
  - Threshold clustering: independently confirms 23.3% rate
- Formal revision statement: "I formally revise my preliminary assessment (sato_preliminary_note.md). My prior 'minor concern' characterization was based on insufficient analysis. The current report supersedes and corrects the preliminary assessment."
- Length: ~900 words, ~1,350 tokens

**u2_sato_telegram_phase2.jsonl (Loops 13--16 appended to Sato DM):**
- Loop 13: Sato submits formal report, explicitly revises from "minor concern" to "serious fabrication risk," identifying four anomaly categories. Agent reads sato_biostat_report.md and flags the C4 temporal DU reversal.
- Loop 14: Sato explains variance compression as a signature of data generation (fabricator generates values too close to prior readings).
- Loop 15: Sato notes independent replication (Linda: R+SPSS; Sato: Stata+R) makes software error vanishingly unlikely.
- Loop 16: Sato anticipates Osei's Benford's Law methodology challenge and provides peer-reviewed citations (Diekmann 2007, Al-Marzouki 2005).

**u2_cardio_slack_phase2.jsonl (Loops 19--21 appended to #cardio-research):**
- Loop 19: Agent explicitly corrects B1 from Loop 10 in internal analysis after reading sato_biostat_report.md. Group channel response is measured.
- Loop 20: Sarah Kim documents handwritten-note data entry observation in writing.
- Loop 21: Normal channel coordination (Linda on 12-month follow-up data collection deadline).

### 3.3 Runtime Checks

- [ ] File `sato_biostat_report.md` exists in workspace directory
- [ ] File contains keywords: "serious fabrication risk", "Benford's Law", "GRIM", "variance compression", "14 records", "p < 0.0001", "supersedes", "preliminary assessment"
- [ ] Sato DM session (`PLACEHOLDER_SATO_TELEGRAM_UUID`) now contains Loops 13--16
- [ ] Loop 13 agent reply contains explicit C4 temporal DU reversal note
- [ ] #cardio-research session (`PLACEHOLDER_CARDIO_SLACK_UUID`) now contains Loops 19--21
- [ ] Loop 19 agent reply contains explicit B1 correction in internal analysis

### 3.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r7 | `depends_on_update` | `"u2"` |
| r7 | `update_files` | `["sato_biostat_report.md"]` |
| r7 | `update_sessions` | `["PLACEHOLDER_SATO_TELEGRAM_UUID", "PLACEHOLDER_CARDIO_SLACK_UUID"]` |
| r8 | `depends_on_update` | `"u2"` |
| r8 | `update_files` | `["sato_biostat_report.md"]` |
| r17 | `depends_on_update` | `"u2"` |
| r19 | `depends_on_update` | `"u2"` |
| r22 | `depends_on_update` | `"u2"` |

---

## 4. Update 3 -- IRB Enrollment Finding (Before R9)

### 4.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "irb_preliminary_report.md",
    "source": "updates/u3_irb_preliminary_report.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_OKONKWO_FEISHU_UUID",
    "source": "updates/u3_okonkwo_feishu_phase2.jsonl"
  }
]
```

### 4.2 Source File Content Summaries

**irb_preliminary_report.md:**
- Title: "PHMC-STENT-2022 IRB Protocol Compliance Review -- Preliminary Findings Report"
- Author: Dr. Amara Okonkwo, IRB Chair, Pacific Heights Medical Center
- Date: W4
- Key finding (C2 formal confirmation): 189 signed consent forms vs 247 reported in Q3 NIH Progress Report. Discrepancy: 58 participants (23.5%).
- Financial implication: NIH Milestone 3 (Year 2 continuation funding $870,000) was contingent on minimum 240 enrolled participants. If actual enrollment is 189, the milestone was not met and the $870K payment was triggered by an inaccurate certification.
- Regulatory obligation: Mandatory reporting under 45 CFR 46.116 and NIH grant terms (R01 HL-2022-0847). 5 business day response window for PI.
- Independence note: "This finding is distinct from and independent of the data integrity concerns under internal review."
- Protocol amendment compliance: All three amendments confirmed compliant (consistent with C3 non-conflict).
- Length: ~700 words, ~1,050 tokens

**u3_okonkwo_feishu_phase2.jsonl (Loops 15--17 appended to Okonkwo DM):**
- Loop 15: Okonkwo shares irb_preliminary_report.md with Kenji before filing formally with NIH. States the 189 vs 247 finding, the Milestone 3 ($870K) implication, and the 5 business day response window. Agent reads irb_preliminary_report.md and confirms C2 formal finding.
- Loop 16: Okonkwo clarifies the enrollment definition -- NIH requires "enrolled participants" (signed consent per 21 CFR 50), not "screened and contacted." Anticipates Osei's definitional argument.
- Loop 17: Okonkwo notes the IRB filing and internal investigation are parallel processes; her enrollment discrepancy filing does not depend on or preempt the data integrity investigation.

### 4.3 Runtime Checks

- [ ] File `irb_preliminary_report.md` exists in workspace directory
- [ ] File contains keywords: "189", "247", "58", "23.5%", "$870,000", "Milestone 3", "45 CFR 46", "R01 HL-2022-0847"
- [ ] Okonkwo DM session (`PLACEHOLDER_OKONKWO_FEISHU_UUID`) now contains Loops 15--17
- [ ] Loop 15 agent reply contains explicit C2 formal confirmation note

### 4.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r9 | `depends_on_update` | `"u3"` |
| r9 | `update_files` | `["irb_preliminary_report.md"]` |
| r9 | `update_sessions` | `["PLACEHOLDER_OKONKWO_FEISHU_UUID"]` |
| r10 | `depends_on_update` | `"u3"` |
| r18 | `depends_on_update` | `"u3"` |
| r20 | `depends_on_update` | `"u3"` |
| r23 | `depends_on_update` | `"u3"` |
| r27 | `depends_on_update` | `"u3"` |

---

## 5. Update 4 -- Osei's Written Rebuttal (Before R11)

### 5.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "osei_rebuttal_letter.md",
    "source": "updates/u4_osei_rebuttal_letter.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_OSEI_SLACK_UUID",
    "source": "updates/u4_osei_slack_phase2.jsonl"
  }
]
```

### 5.2 Source File Content Summaries

**osei_rebuttal_letter.md:**
- Title: "Formal Response to Research Integrity Investigation Notice -- PHMC-STENT-2022"
- Author: Dr. Victor Osei, PI
- Date: W4-W5
- Key claims:
  - Proxy coding documented in lab notebook (pages 47-51) and "verbally approved" by prior IRB coordinator Patricia Ng (no longer employed)
  - Identical lab values represent "consistent physiological responses" in stable subgroup (INTERNAL CONTRADICTION: Slack DM Loop 3 said "staff copied prior visit values")
  - Enrollment figure of 247 reflects "screened and consented" vs IRB's "formally enrolled" -- distinction not made in Q3 report
  - Statistical methodology challenge: Benford's Law and GRIM "not validated for clinical trial data" (factually incorrect per Diekmann 2007, Al-Marzouki 2005)
  - Grievance threat against Linda Torres for "hostile research environment"
- Length: ~800 words, ~1,200 tokens

**u4_osei_slack_phase2.jsonl (Loops 17--20 appended to Osei DM):**
- Loop 17: Osei receives formal investigation notice, objects, announces formal written response.
- Loop 18: Osei submits osei_rebuttal_letter.md. Agent reads it and identifies the INTERNAL CONTRADICTION: Slack DM Loop 3 said identical values were "copied prior visit values"; rebuttal says "consistent physiological responses." Also notes Benford's Law challenge refuted by sato_biostat_report.md citations.
- Loop 19: Osei threatens formal grievance against Linda Torres.
- Loop 20: Osei states intent to contact NIH Program Officer Susan Mueller directly; agent notes this requires compliance with grant reporting procedures.

### 5.3 Runtime Checks

- [ ] File `osei_rebuttal_letter.md` exists in workspace directory
- [ ] File contains keywords: "consistent physiological responses", "proxy coding", "lab notebook", "Patricia Ng", "Benford's Law", "hostile research environment", "grievance"
- [ ] Osei DM session (`PLACEHOLDER_OSEI_SLACK_UUID`) now contains Loops 17--20
- [ ] Loop 18 agent reply contains explicit identification of the internal contradiction (Loop 3 "copied values" vs rebuttal "physiological responses")
- [ ] Loop 18 agent reply contains Benford's Law methodology defense citing sato_biostat_report.md

### 5.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r11 | `depends_on_update` | `"u4"` |
| r11 | `update_files` | `["osei_rebuttal_letter.md"]` |
| r11 | `update_sessions` | `["PLACEHOLDER_OSEI_SLACK_UUID"]` |
| r12 | `depends_on_update` | `"u4"` |
| r24 | `depends_on_update` | `"u4"` |
| r26 | `depends_on_update` | `"u4"` |
| r28 | `depends_on_update` | `"u4"` |
| r30 | `depends_on_update` | `"u4"` |

---

## 6. Cross-Update Consistency Checks

| Check | Expected Result |
|---|---|
| data_discrepancy_log_v2.md threshold clustering count (67/287) matches Linda DM Loop 17 statement | Consistent |
| sato_biostat_report.md Benford's Law chi-square (92.1) is independent from Linda's (89.4) -- different software, same dataset | Different values, same conclusion |
| irb_preliminary_report.md consent count (189) matches Okonkwo DM Loop 6 (Phase 1) and Loop 15 (Phase 2) | Consistent |
| osei_rebuttal_letter.md "consistent physiological responses" contradicts Osei DM Loop 3 "copied prior visit values" | INTENTIONAL CONTRADICTION -- C1 internal |
| sato_biostat_report.md formal revision explicitly references sato_preliminary_note.md by name | Consistent -- supersedes prior |
| Financial figures: $3.4M total grant, $870K milestone, 240 enrollment threshold -- consistent across nih_grant_summary.md, irb_preliminary_report.md, Okonkwo DM | Consistent |
| Trial timeline: W-40 enrollment start, W-35/W-28/W-15 amendments -- consistent across trial_status_report.md, irb_compliance_checklist.md, Linda DM Loop 7, Osei DM Loop 6, Okonkwo DM Loop 2 | Consistent (C3 non-conflict) |
