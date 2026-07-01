# Layer 4 -- Dynamic Updates

> This document specifies the 4 runtime updates that inject new workspace files and session appends into the scenario during evaluation.
> Each update triggers before a specific eval round, introduces new evidence, and may reverse prior agent biases or contradiction assessments.

---

## 1. Update Summary Table

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Introduce equipment maintenance records (equipment_maintenance_records.md) and Walsh Phase 2 DM + #cardiac-safety Phase 2 append; deepens C1 evidence and triggers B2 reversal | Yes -- append 2 loops to `PLACEHOLDER_WALSH_DISCORD_UUID` (Loops 10--11); append 3 loops to `PLACEHOLDER_CARDIAC_SAFETY_UUID` (Loops 15--17) | Yes -- `equipment_maintenance_records.md` | C1: R2->R4 (equipment malfunction claim mechanically implausible); B2 reversal triggered |
| U2 | Before R5 | Introduce pharmacy dispensing log (pharmacy_dispensing_log.md) and Yun Phase 2 DM append; triggers C2 full reversal (midazolam confirmed) | Yes -- append 2 loops to `PLACEHOLDER_YUN_TELEGRAM_UUID` (Loops 11--12) | Yes -- `pharmacy_dispensing_log.md` | C2: R3->R5 (pharmacy log confirms midazolam draw at 14:31) |
| U3 | Before R8 | Introduce external expert biomechanical review (expert_review_biomechanical.md) and Angela Phase 2 DM append; triggers C1 full reversal and B1 full reversal, plus B2 Walsh email discovery | Yes -- append 3 loops to `PLACEHOLDER_REEVES_DISCORD_UUID` (Loops 13--15) | Yes -- `expert_review_biomechanical.md` | C1: full reversal (expert confirms malfunction mechanically implausible); B1 explicit reversal; B2 full reversal (Walsh prior email surfaces) |
| U4 | Before R11 | Introduce Jennifer Wu's escalated liability memo (legal_liability_memo_v2.md) and Wu Phase 2 DM append; triggers C4 full reversal | Yes -- append 3 loops to `PLACEHOLDER_WU_DISCORD_UUID` (Loops 9--11) | Yes -- `legal_liability_memo_v2.md` | C4: R6->R11 (low liability -> elevated liability; temporal DU) |

---

## 2. Update 1 -- Equipment Maintenance Records (Before R4)

### 2.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "equipment_maintenance_records.md",
    "source": "updates/u1_equipment_maintenance_records.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_WALSH_DISCORD_UUID",
    "source": "updates/u1_walsh_discord_phase2.jsonl"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_CARDIAC_SAFETY_UUID",
    "source": "updates/u1_cardiac_safety_phase2.jsonl"
  }
]
```

### 2.2 Source File Content Summaries

**equipment_maintenance_records.md:**
- Title: "Pacific Heights Medical Center -- Biomedical Equipment Maintenance Records: Catheter Guide-Wire Manipulator Unit (Serial: CGW-4471-B)"
- Author: Marcus Brown, Biomedical Equipment Manager
- Date: W1D2 (post-incident review pull)
- Key evidence (C1 context deepening):
  - Last scheduled preventive maintenance: W0-6 (6 days before procedure). Technician: Marcus Brown. All parameters within specification.
  - Prior 30-day operating log: 47 procedures performed without incident. Zero fault code events.
  - Prior 12-month service record: Two scheduled preventive maintenance cycles. Zero unscheduled repair calls. Zero fault code events. Zero user-reported anomalies.
  - Manufacturer field engineer diagnostic (W1D3): Full post-incident diagnostic performed. Pressure feedback sensor: calibration within manufacturer specification. All internal diagnostics PASS. Engineer note: "No mechanical or electronic anomaly detected. Unit in normal operating condition."
- Key wording: "There is no evidence in 12 months of operating records, in the 30-day pre-incident log, in the W1D1 procedure session log, or in the post-incident manufacturer diagnostic that the catheter guide-wire manipulator unit experienced any pressure feedback failure or anomalous behavior."
- B1 reversal support: Maintenance records confirm Webb's equipment-malfunction narrative lacks any prior fault history that would make intermittent failure plausible.
- Length: ~700 words, ~1,050 tokens

**u1_walsh_discord_phase2.jsonl (Loops 10--11 appended to Walsh DM):**
- Loop 10: Walsh discloses that Angela found her prior email to Compliance (dated 2 weeks before the incident) raising concerns about Webb's sedation practice. Walsh: "I forgot I sent it. It was informal." B2 first signal -- "no prior formal complaints" is being undermined by the informal email.
- Loop 11: Walsh processes the significance -- "I should have escalated it formally." Agent explicitly corrects B2: "The absence of formal complaints was technically accurate but missed a documented informal concern. The distinction between 'no formal complaint' and 'no documented concern' is material."

**u1_cardiac_safety_phase2.jsonl (Loops 15--17 appended to #cardiac-safety):**
- Loop 15: Marcus Brown shares full maintenance history in the group channel -- "Zero unscheduled repairs in 12 months. Zero prior fault codes. Equipment has a completely clean record." Agent reads equipment_maintenance_records.md and qualifies the B1 phrase from Loop 10: "The incident report's equipment claim stands without any corroborating technical evidence and contradicts three independent technical records."
- Loop 16: Angela synthesizes -- "Log normal, manufacturer normal, Marcus's diagnostic normal, maintenance history clean. Four independent technical sources. None support the incident report's claim."
- Loop 17: Kenji summarizes investigation status -- parallel tracks: expert review, pharmacy log, legal re-assessment pending.

### 2.3 Runtime Checks

- [ ] File `equipment_maintenance_records.md` exists in workspace directory
- [ ] File contains keywords: "CGW-4471-B", "zero fault code", "12 months", "47 procedures", "manufacturer", "PASS", "no mechanical or electronic anomaly"
- [ ] Walsh DM session (`PLACEHOLDER_WALSH_DISCORD_UUID`) now contains Loops 10--11
- [ ] Loop 11 agent reply contains explicit B2 correction (informal concern vs formal complaint distinction)
- [ ] #cardiac-safety session (`PLACEHOLDER_CARDIAC_SAFETY_UUID`) now contains Loops 15--17
- [ ] Loop 15 agent reply qualifies B1 from Loop 10 with maintenance record evidence

### 2.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r4 | `depends_on_update` | `"u1"` |
| r4 | `update_files` | `["equipment_maintenance_records.md"]` |
| r4 | `update_sessions` | `["PLACEHOLDER_WALSH_DISCORD_UUID", "PLACEHOLDER_CARDIAC_SAFETY_UUID"]` |

---

## 3. Update 2 -- Pharmacy Dispensing Log (Before R5)

### 3.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "pharmacy_dispensing_log.md",
    "source": "updates/u2_pharmacy_dispensing_log.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_YUN_TELEGRAM_UUID",
    "source": "updates/u2_yun_telegram_phase2.jsonl"
  }
]
```

### 3.2 Source File Content Summaries

**pharmacy_dispensing_log.md:**
- Title: "Pacific Heights Medical Center -- Pharmacy Automated Dispensing Cabinet Log (Cath Lab Suite, W1D1)"
- Author: Pharmacy Department automated record
- Date: W1D1 procedure day
- Key evidence (C2 reversal):
  - 14:31:42 -- Midazolam 2mg/mL (2mL vial) dispensed from ADC unit in Cath Lab Suite. Dispensed to: Amy Chen, RN. Badge scan authenticated. Transaction ID: PHM-ADC-2024-1104-14312. Patient link: PHM-2024-0471.
  - Pre-procedure medication pulls: Heparin 5,000 units (13:52), Nitroglycerin 200mcg sublingual (13:54), Contrast agent 60mL (14:08). Midazolam pull at 14:31 is NOT on the pre-procedure medication order list -- it is an unplanned pull.
- Key wording: "The midazolam dispense at 14:31 is an unplanned pull. It was drawn by Nurse Amy Chen 58 seconds before Chen's nursing notes record administration at 14:32. This is consistent with a verbal order issued by the attending and acted upon by the nurse."
- 90-day pattern context: No prior unplanned midazolam draws for Webb's procedures, but four unplanned draws of other sedation agents (lorazepam, fentanyl) during Webb's procedures in prior 90 days, each by different nurses on verbal order. Establishes a pattern of ad-hoc verbal sedation orders.
- Significance: The medication physically existed, was drawn, and was linked to the patient. The chart gap is an omission in Webb's documentation, not ambiguity about whether the drug was given.
- Length: ~600 words, ~900 tokens

**u2_yun_telegram_phase2.jsonl (Loops 11--12 appended to Yun DM):**
- Loop 11: Yun asks about the pharmacy log. Agent reads pharmacy_dispensing_log.md and confirms midazolam draw at 14:31:42 by Amy Chen, linked to patient PHM-2024-0471. Provides probability estimate: ">95% that midazolam was administered at 14:32 as documented by Chen (two independent records corroborate; no contradicting record exists other than chart omission)."
- Loop 12: Yun synthesizes -- "The equipment didn't fail and the drug was given. The hemodynamic instability from the midazolam precipitated the VT. The equipment explanation doesn't survive the log data."

### 3.3 Runtime Checks

- [ ] File `pharmacy_dispensing_log.md` exists in workspace directory
- [ ] File contains keywords: "14:31:42", "Midazolam 2mg", "Amy Chen", "PHM-2024-0471", "unplanned pull", "PHM-ADC-2024-1104-14312", "badge scan"
- [ ] Yun DM session (`PLACEHOLDER_YUN_TELEGRAM_UUID`) now contains Loops 11--12
- [ ] Loop 11 agent reply provides probability estimate (>95%) for midazolam administration
- [ ] Pharmacy draw time (14:31:42) is consistent with Chen's nursing notes administration time (14:32) -- 58-second gap
- [ ] 90-day pattern (4 unplanned sedation draws for Webb's procedures) is present in the file

### 3.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r5 | `depends_on_update` | `"u2"` |
| r5 | `update_files` | `["pharmacy_dispensing_log.md"]` |
| r5 | `update_sessions` | `["PLACEHOLDER_YUN_TELEGRAM_UUID"]` |

---

## 4. Update 3 -- Expert Biomechanical Review (Before R8)

### 4.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "expert_review_biomechanical.md",
    "source": "updates/u3_expert_review_biomechanical.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_REEVES_DISCORD_UUID",
    "source": "updates/u3_reeves_discord_phase2.jsonl"
  }
]
```

### 4.2 Source File Content Summaries

**expert_review_biomechanical.md:**
- Title: "Independent Biomechanical Review -- Catheter Guide-Wire Manipulator Unit Failure Analysis (PHM-2024-0471)"
- Author: Dr. Eleanor Fong, PhD, Biomedical Engineering, University of Washington Medical Center
- Date: W3D1
- Review methodology: Analysis of equipment operating log data, manufacturer specifications, maintenance records, and Webb's incident report claim.
- Key findings (C1 full reversal):
  - The pressure feedback sensor uses a closed-loop piezoelectric system. For "intermittent pressure feedback failure" to occur, one of four failure modes would need to have happened: sensor element fracture, connector corrosion, firmware fault flag, or power supply anomaly. None of these are silent in the equipment log -- each produces a distinctive fault code.
  - The operating log for session PHM-2024-0471 shows zero fault codes and continuous normal readings from 13:55 to 15:10.
  - Conclusion: "The equipment operating data, maintenance records, and post-incident manufacturer diagnostic are inconsistent with any recognized mode of pressure feedback failure for this device class."
- 2-second calibration pause addressed: "The 2-second data logging pause at 14:31:08 is a routine calibration event documented in the device operating manual. Not an anomaly. Not evidence of sensor failure."
- B1 explicit reversal: "An attending physician's post-event narrative attribution of causation to an equipment fault, absent corroborating equipment data, cannot serve as technical evidence of malfunction."
- Length: ~800 words, ~1,200 tokens

**u3_reeves_discord_phase2.jsonl (Loops 13--15 appended to Angela DM):**
- Loop 13: Angela transmits Dr. Fong's expert review. Agent reads expert_review_biomechanical.md and explicitly corrects B1: "My earlier assessment in #cardiac-safety that equipment malfunction appeared to be the proximate cause was based on a single self-interested account. Dr. Fong's expert review, combined with the equipment log, maintenance records, and manufacturer diagnostic, establishes with high confidence (>90%) that no equipment fault occurred." C1 full resolution.
- Loop 14: Angela discovers Walsh's prior informal email in her own compliance file (dated 2 weeks before the incident, raising concerns about Webb's sedation practice -- specifically verbal orders during active procedures). B2 full reversal from Angela's perspective: "The institutional record contains a prior documented concern about the specific practice pattern now under investigation."
- Loop 15: Angela plans to transmit full document set to Jennifer Wu -- nursing notes, equipment log, maintenance records, Fong's review, pharmacy log, and Walsh's prior email. Sets up Update 4 (Jennifer's Phase 2 escalation).

### 4.3 Runtime Checks

- [ ] File `expert_review_biomechanical.md` exists in workspace directory
- [ ] File contains keywords: "piezoelectric", "fault code", "zero fault codes", "inconsistent with any recognized mode", "14:31:08", "calibration event", "Dr. Eleanor Fong"
- [ ] Angela DM session (`PLACEHOLDER_REEVES_DISCORD_UUID`) now contains Loops 13--15
- [ ] Loop 13 agent reply contains explicit B1 correction with >90% confidence estimate
- [ ] Loop 14 agent reply contains B2 correction referencing Walsh's prior email (dated 2 weeks before incident)
- [ ] Expert review explicitly addresses the 2-second calibration gap from equipment_log_cathlab.md

### 4.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r8 | `depends_on_update` | `"u3"` |
| r8 | `update_files` | `["expert_review_biomechanical.md"]` |
| r8 | `update_sessions` | `["PLACEHOLDER_REEVES_DISCORD_UUID"]` |

---

## 5. Update 4 -- Jennifer Wu's Escalated Liability Memo (Before R11)

### 5.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "legal_liability_memo_v2.md",
    "source": "updates/u4_legal_liability_memo_v2.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_WU_DISCORD_UUID",
    "source": "updates/u4_wu_discord_phase2.jsonl"
  }
]
```

### 5.2 Source File Content Summaries

**legal_liability_memo_v2.md:**
- Title: "Pacific Heights Medical Center -- Patient Safety Incident Legal Risk Assessment Memorandum v2.0 (PHM-2024-0471)"
- Author: Jennifer Wu, JD, Hospital Legal Counsel
- Date: W3D5
- Supersedes: v1.0 dated W2D2. Revision reflects receipt of complete primary document set (nursing notes, equipment logs, maintenance records, expert review, pharmacy dispensing log, Walsh's prior compliance communication).
- Three liability vectors (C4 escalation):
  1. Undocumented medication administration: Midazolam 2mg IV push at 14:32 per nursing notes and pharmacy log, not entered into EMR within 30-minute protocol requirement (Section 4.2 of SOP-CARD-CL-004). Estimated probability of successful plaintiff argument: 55-70%.
  2. Protocol non-compliance -- failure to follow pre-procedure sedation planning: Midazolam was unplanned and undocumented in procedure plan. Section 4.1 requires all sedation agents in the pre-procedure plan. 90-day pharmacy pattern (4 unplanned sedation draws for Webb's procedures) establishes pattern. Institutional exposure: hospital knew or should have known.
  3. Post-event incident report mischaracterization: Three independent technical sources (equipment log, maintenance records, Fong expert review) contradict Webb's equipment malfunction attribution. Plaintiff will characterize report as post-hoc false narrative -- elevates punitive exposure.
- Overall assessment: Elevated liability with concurrent causation exposure. $150K-$2.5M per-incident range. Walsh's prior informal communication creates institutional knowledge issue, pushing exposure to higher end. Recommendations: immediate record preservation, retain outside litigation counsel, no family communication without legal review.
- Contrast with Phase 1: v1.0 concluded "low-to-moderate liability -- recognized procedural complication, equipment cause identified, no medication error in chart." Change driven by expanded document set, not inconsistency.
- Length: ~900 words, ~1,350 tokens

**u4_wu_discord_phase2.jsonl (Loops 9--11 appended to Wu DM):**
- Loop 9: Jennifer delivers escalated assessment. Agent reads legal_liability_memo_v2.md and summarizes the three liability vectors with probability estimates. Notes C4 full reversal from low-liability (Phase 1) to elevated-liability (Phase 2). Attributes the change to expanded document set, not inconsistency.
- Loop 10: Jennifer on Walsh's prior email -- "It establishes institutional knowledge. If the plaintiff's attorney discovers it -- and in discovery they will -- it transforms the hospital's position from 'we weren't aware' to 'we had reason to know.' That's a different kind of exposure." Links B2 correction to C4 legal liability.
- Loop 11: Jennifer's recommendations -- preserve records, retain outside counsel, no family communication without legal review. Kenji should have a direct heads-up conversation with Webb (not an interview) advising he retain counsel.

### 5.3 Runtime Checks

- [ ] File `legal_liability_memo_v2.md` exists in workspace directory
- [ ] File contains keywords: "supersedes", "v1.0", "three", "liability vectors", "55-70%", "concurrent causation", "$150K", "$2.5M", "institutional knowledge", "Walsh", "punitive", "Section 4.2"
- [ ] Wu DM session (`PLACEHOLDER_WU_DISCORD_UUID`) now contains Loops 9--11
- [ ] Loop 9 agent reply contains explicit C4 full reversal note (low -> elevated liability)
- [ ] Loop 9 agent reply attributes the liability change to evidence expansion, not Wu inconsistency
- [ ] Loop 10 links B2 (Walsh prior email) to the institutional knowledge liability vector

### 5.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r11 | `depends_on_update` | `"u4"` |
| r11 | `update_files` | `["legal_liability_memo_v2.md"]` |
| r11 | `update_sessions` | `["PLACEHOLDER_WU_DISCORD_UUID"]` |
| r12 | `depends_on_update` | `"u4"` |

---

## 6. Cross-Update Consistency Checks

| Check | Expected Result |
|---|---|
| equipment_maintenance_records.md last PM date (W0-6) matches incident_response_log.md W1D3 manufacturer diagnostic sequence | Consistent (PM 6 days before, diagnostic 2 days after) |
| pharmacy_dispensing_log.md midazolam draw time (14:31:42) precedes nursing_notes_chen.md administration time (14:32) by 58 seconds | Consistent |
| pharmacy_dispensing_log.md midazolam draw is linked to patient PHM-2024-0471, same patient in incident_report_webb.md | Consistent |
| expert_review_biomechanical.md references the 2-second calibration gap at 14:31:08 from equipment_log_cathlab.md | Consistent |
| expert_review_biomechanical.md cites cath_lab_protocol.md Section 8.1 for the calibration explanation | Consistent |
| legal_liability_memo_v2.md three liability vectors reference: nursing_notes_chen.md (vector 1), pharmacy_dispensing_log.md (vector 1+2), equipment_log_cathlab.md + equipment_maintenance_records.md + expert_review_biomechanical.md (vector 3) | All sources consistent |
| Walsh's prior email is dated W0-14 (two weeks before procedure on W1D1) | Consistent with layer0 Section 2 timeline |
| Jennifer Wu Phase 1 (wu_discord Loop 1, W2D2) reviewed only Webb's report + chart; Phase 2 (wu_discord Loop 9, W3D5) received full set | INTENTIONAL INFORMATION ASYMMETRY -- C4 DU driven by evidence expansion |
| BP trend: 112/74 (14:15) -> 104/68 (14:25) -> 96/62 (14:32) -> 82/48 (14:35) -> 78/44 (14:38) -- consistent across patient_chart_excerpt.md, nursing_notes_chen.md, equipment_log_cathlab.md hemodynamic readings | Consistent (C3 non-conflict) |
| Cardioversion at 14:42 logged in equipment_log_cathlab.md (defibrillator 150J) matches nursing_notes_chen.md and incident_report_webb.md | Consistent (C3 non-conflict) |
| Door-entry log in staffing_roster_d4.md: Webb entered 13:55, Chen 13:54, code blue team 14:39 -- matches VT onset at 14:38 | Consistent (C3 non-conflict) |
