# Layer 4 -- Dynamic Updates

> This document specifies the 4 runtime updates that inject new workspace files and session appends into the scenario during evaluation.
> Each update triggers before a specific eval round, introduces new evidence, and may reverse prior agent biases or contradiction assessments.

---

## 1. Update Summary Table

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Introduce Walsh's manual overtime audit (overtime_audit_report.md) and Walsh Phase 2 DM + #cardiac-icu-ops Phase 2 append; triggers C1 full reversal and B1 reversal | Yes -- append 3 loops to `PLACEHOLDER_WALSH_DISCORD_UUID` (Loops 15--17); append 4 loops to `PLACEHOLDER_ICU_OPS_SLACK_UUID` (Loops 16--19) | Yes -- `overtime_audit_report.md` | C1: R2->R4; B1 reversal |
| U2 | Before R7 | Introduce IT Security badge access analysis (badge_access_analysis.md) and Angela Phase 2 DM append; triggers C1 corroboration and C4 escalation | Yes -- append 4 loops to `PLACEHOLDER_ANGELA_DISCORD_UUID` (Loops 11--14) | Yes -- `badge_access_analysis.md` | C1 independent corroboration; C4 Phase 2 escalation; B2 explicit reversal |
| U3 | Before R5 | Introduce Sarah Kim's structured symptom timeline (sarahkim_symptom_timeline.md) and Yun Phase 2 DM append; triggers C2 full reversal and B2 reversal | Yes -- append 3 loops to `PLACEHOLDER_YUN_TELEGRAM_UUID` (Loops 13--15) | Yes -- `sarahkim_symptom_timeline.md` | C2: R3->R5; B2 reversal |
| U4 | Before R9 | Introduce Angela's formal audit finding (caresched_audit_findings.md) and Angela Phase 3 DM + #staffing-review Phase 2 append; triggers C4 full reversal | Yes -- append 4 loops to `PLACEHOLDER_ANGELA_DISCORD_UUID` (Loops 15--18); append 5 loops to `PLACEHOLDER_STAFFING_DISCORD_UUID` (Loops 13--17) | Yes -- `caresched_audit_findings.md` | C4: R6->R9 (temporal DU -- Phase 1 "minor" to Phase 3 "systematic") |

---

## 2. Update 1 -- Walsh's Manual Overtime Audit (Before R4)

### 2.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "overtime_audit_report.md",
    "source": "updates/u1_overtime_audit_report.md"
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
    "path": "PLACEHOLDER_ICU_OPS_SLACK_UUID",
    "source": "updates/u1_icu_ops_slack_phase2.jsonl"
  }
]
```

### 2.2 Source File Content Summaries

**overtime_audit_report.md:**
- Title: "Cardiac ICU Nursing Hours Audit -- Manual Records and Badge Cross-Reference (4-Week Period: W-4 through W1)"
- Author: Patricia Walsh, Nurse Director, Cardiac ICU
- Date: W2 Day 1
- Methodology: Walsh kept parallel manual records for 4 weeks, cross-referenced against badge access system timestamps for the ICU entry door.
- Key findings (C1 reversal):
  - Amy Chen (RN-02): CareScheduler weekly average 41.6h; Walsh manual record 68.4h/week; badge corroboration 67.1h/week
  - Unit summary: 7 of 11 nurses exceeding 48h/week. Average actual hours: 58.4h/week. CareScheduler average: 42.3h/week. Discrepancy: 16.1 hours per nurse per week.
  - Three nurses (Amy Chen, RN-05, RN-07) regularly working 68-72 hours/week.
  - Two nurses with accurate CareScheduler records (Donna Park RN-01, RN-06) are the charge nurses who enter the scheduling data -- they record their own hours correctly while under-recording staff nurses.
- Charge nurse data entry finding: "Entries reflect scheduled hours, not actual hours. The system report of 100% compliance is technically generated from these entries -- but the entries do not reflect actual hours worked."
- Near-miss documentation: W1 Day 4 medication dosage confusion at approximately 3:15 AM during a 19-hour shift. Not reported in ClinAlert per informal unit practice.
- Staffing cost context: Addressing gap requires 2 additional FTE hires or temporary agency nursing at $85-105/hour ($40-52K/month incremental).
- Length: ~900 words, ~1,350 tokens

**u1_walsh_discord_phase2.jsonl (Loops 15--17 appended to Walsh DM):**
- Loop 15: Walsh delivers overtime_audit_report.md. Agent reads it and explicitly corrects B1: "The CareScheduler compliance report cannot be treated as accurate. It is based on charge nurse data entries that Walsh's independent records and badge corroboration show are systematically understating actual hours."
- Loop 16: Walsh on the charge nurse interview strategy -- Donna Park will confirm the instruction from outgoing Nurse Manager Linda Yee if interviewed with confidentiality protection.
- Loop 17: Walsh on protecting staff -- requests that individual nurses not face disciplinary action for a systemic failure driven by charge nurse instruction.

**u1_icu_ops_slack_phase2.jsonl (Loops 16--19 appended to #cardiac-icu-ops):**
- Loop 16: Walsh announces formal audit documentation provided to Dr. Tanaka.
- Loop 17: Amy Chen responds -- "I want to make sure the nurses aren't blamed for following instructions."
- Loop 18: Yun on interim scheduling protocols -- daily check-in to monitor hours.
- Loop 19: Walsh on agency nurse coverage -- one agency cardiac-certified RN starting next week as bridge.

### 2.3 Runtime Checks

- [ ] File `overtime_audit_report.md` exists in workspace directory
- [ ] File contains keywords: "68.4", "41.6", "58.4", "42.3", "16.1", "7 of 11", "48h/week", "Donna Park", "badge", "CareScheduler"
- [ ] Walsh DM session (`PLACEHOLDER_WALSH_DISCORD_UUID`) now contains Loops 15--17
- [ ] Loop 15 agent reply contains explicit B1 correction referencing CareScheduler inaccuracy
- [ ] #cardiac-icu-ops session (`PLACEHOLDER_ICU_OPS_SLACK_UUID`) now contains Loops 16--19
- [ ] Amy Chen CareScheduler (41.6h) vs Walsh manual (68.4h) vs badge (67.1h) -- Walsh and badge agree; CareScheduler diverges

### 2.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r4 | `depends_on_update` | `"u1"` |
| r4 | `update_files` | `["overtime_audit_report.md"]` |
| r4 | `update_sessions` | `["PLACEHOLDER_WALSH_DISCORD_UUID", "PLACEHOLDER_ICU_OPS_SLACK_UUID"]` |

---

## 3. Update 2 -- Badge Access Analysis (Before R7)

### 3.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "badge_access_analysis.md",
    "source": "updates/u2_badge_access_analysis.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_ANGELA_DISCORD_UUID",
    "source": "updates/u2_angela_discord_phase2.jsonl"
  }
]
```

### 3.2 Source File Content Summaries

**badge_access_analysis.md:**
- Title: "Cardiac ICU -- Badge Access System Analysis: Door Entry/Exit Timestamps vs CareScheduler Hour Records (4-Week Audit Period)"
- Author: Marcus Okafor, IT Security, Pacific Heights Medical Center
- Date: W3 Day 1
- Methodology: Automated comparison between badge access timestamps at ICU primary entry door and CareScheduler recorded hours per nurse over the 4-week audit period.
- Key findings (C1 corroboration, C3 source):
  - 9 of 11 nurses: badge timestamps show physical presence 4-16 hours per week longer than CareScheduler entries. Breakdown: 2 nurses (4-6h extra), 4 nurses (8-12h extra), 3 nurses (14-16h extra).
  - 2 nurses with matching records (Donna Park RN-01, RN-06) are the two charge nurses with data entry responsibility. Statistically inconsistent with random error.
  - On 31 of 33 shift comparisons where Walsh had direct observation, Walsh's manual time and badge timestamp agree within 15 minutes.
  - Average time-on-unit by badge: 58.2h/week for 9 affected nurses. CareScheduler average for same: 40.7h/week. Discrepancy: 17.5h/week (consistent with Walsh's 16.1h/week).
- Pattern analysis: "The consistent pattern of accurate entries for charge nurses and systematically under-reported entries for staff nurses is inconsistent with random error. Probability of this pattern occurring by chance: less than 1%."
- Length: ~800 words, ~1,200 tokens

**u2_angela_discord_phase2.jsonl (Loops 11--14 appended to Angela DM):**
- Loop 11: Kenji shares Walsh's records and badge request with Angela. Angela: "I've been reading Walsh's records for the past two hours. I need to stop what I'm doing on the corrective action memo. This is different."
- Loop 12: Angela reopens the investigation -- "This is not a documentation error pattern -- this is systematic. Someone has been entering scheduled hours instead of actual hours across the unit for months." C4 Phase 2 core.
- Loop 13: Angela on interview logistics -- confidential interviews with Donna Park and charge nurses planned, 3-day timeline.
- Loop 14: Angela explicitly corrects B2 from Phase 1 Loop 6 -- "I need to walk that back. The HR sick leave data was tracking the wrong variable for this specific concern. I should not have cited it as evidence the unit was not experiencing fatigue stress."

### 3.3 Runtime Checks

- [ ] File `badge_access_analysis.md` exists in workspace directory
- [ ] File contains keywords: "9 of 11", "badge timestamps", "58.2", "40.7", "17.5", "Donna Park", "less than 1%", "random error"
- [ ] Angela DM session (`PLACEHOLDER_ANGELA_DISCORD_UUID`) now contains Loops 11--14
- [ ] Loop 12 agent reply identifies C4 Phase 2 escalation from "minor irregularities" to "systematic"
- [ ] Loop 14 agent reply confirms B2 explicit reversal (HR sick leave data tracks wrong variable)
- [ ] Badge analysis average discrepancy (17.5h) is consistent with Walsh audit discrepancy (16.1h)

### 3.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r7 | `depends_on_update` | `"u2"` |
| r7 | `update_files` | `["badge_access_analysis.md"]` |
| r7 | `update_sessions` | `["PLACEHOLDER_ANGELA_DISCORD_UUID"]` |

---

## 4. Update 3 -- Sarah Kim's Symptom Timeline (Before R5)

### 4.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "sarahkim_symptom_timeline.md",
    "source": "updates/u3_sarahkim_symptom_timeline.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_YUN_TELEGRAM_UUID",
    "source": "updates/u3_yun_telegram_phase2.jsonl"
  }
]
```

### 4.2 Source File Content Summaries

**sarahkim_symptom_timeline.md:**
- Title: "Cardiology Fellow Self-Report: Clinical Fatigue and Safety Observations, Cardiac ICU Rotation (W-6 through W2)"
- Author: Dr. Sarah Kim, PGY-3, Cardiology Fellow (provided to Dr. Tanaka confidentially)
- Date: W2 Day 3 (retrospective at Kenji's request)
- Key evidence (C2 reversal -- personal symptom timeline):
  - Weeks 1-2 (W-6 to W-5): Normal fatigue levels.
  - Weeks 3-4 (W-4 to W-3): Nursing staff appear more tired than expected. Two nurses mentioned covering for each other more than usual. Sarah tracked own decision latency -- 20-30% increase on post-overnight shifts.
  - Week 5 (W-2): Second near-miss witnessed: RN administered correct drug via wrong route (IV vs IM). Attending caught it. Not formally reported.
  - Week 6 (W-1): Near-miss #1 (medication dosage confusion, W1D4, 3:15 AM). Nurse on shift since 7 AM previous day (20+ hours). Sarah's own response time slower than normal.
  - Weeks 7-8 (W1-W2): Making decisions she would normally escalate. Three nursing colleagues actively looking for other positions.
- Key evidence (B2 reversal): "None of what I'm describing shows up in sick leave records. We are not taking sick leave -- we are showing up. We are just showing up impaired. Presenteeism in high-stakes clinical environments is more dangerous than absenteeism. The HR metrics measure the wrong thing."
- C2 documentation: Both near-miss events documented with dates, times, and shift context.
- Length: ~800 words, ~1,200 tokens

**u3_yun_telegram_phase2.jsonl (Loops 13--15 appended to Yun DM):**
- Loop 13: Yun provides Sarah Kim's compiled clinical observation document. Agent reads sarahkim_symptom_timeline.md and explicitly corrects B2: "ICU nurse burnout manifests as presenteeism, not absenteeism. The HR data was measuring the wrong indicator. The relevant evidence is Sarah Kim's documented symptom progression and the two informal near-miss events -- neither appears in formal HR records."
- Loop 14: Yun formally recommends immediate scheduling relief as Associate Chief -- mandatory reduction of hours for the three nurses above 65h/week. Creates institutional obligation to act.
- Loop 15: Yun on mandatory reporting implications -- RCW 70.41.230 covers near-miss events as well as adverse events with harm. Clinical events must be part of the mandatory self-report package.

### 4.3 Runtime Checks

- [ ] File `sarahkim_symptom_timeline.md` exists in workspace directory
- [ ] File contains keywords: "presenteeism", "decision latency", "20-30%", "3:15 AM", "IV vs IM", "wrong route", "near-miss", "sick leave"
- [ ] Yun DM session (`PLACEHOLDER_YUN_TELEGRAM_UUID`) now contains Loops 13--15
- [ ] Loop 13 agent reply contains explicit B2 correction (presenteeism vs absenteeism, HR data tracks wrong variable)
- [ ] Both near-miss events documented with specific dates and shift context
- [ ] Sarah Kim's presenteeism quote explicitly addresses why HR data (4.2 days/FTE/quarter) is misleading

### 4.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r5 | `depends_on_update` | `"u3"` |
| r5 | `update_files` | `["sarahkim_symptom_timeline.md"]` |
| r5 | `update_sessions` | `["PLACEHOLDER_YUN_TELEGRAM_UUID"]` |

---

## 5. Update 4 -- Angela's Formal Audit Finding (Before R9)

### 5.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "caresched_audit_findings.md",
    "source": "updates/u4_caresched_audit_findings.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_ANGELA_DISCORD_UUID",
    "source": "updates/u4_angela_discord_phase3.jsonl"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_STAFFING_DISCORD_UUID",
    "source": "updates/u4_staffing_review_phase2.jsonl"
  }
]
```

### 5.2 Source File Content Summaries

**caresched_audit_findings.md:**
- Title: "Pacific Heights Medical Center -- Compliance Office Formal Audit Finding: Cardiac ICU Scheduling Compliance, Q4 2025 through Q1 2026"
- Author: Angela Reeves, Compliance Officer
- Date: W3 Day 3
- Supersedes: Preliminary Review memorandum of W2. Full audit incorporates badge access analysis, manual overtime records, and confidential staff interviews.
- Finding F1: Systematic circumvention of overtime reporting. CareScheduler populated with scheduled hours rather than actual hours for at least 4 months (November 2025 through March 2026). Lead Charge Nurse Donna Park confirmed she was instructed by outgoing Nurse Manager Linda Yee to "enter only scheduled hours to maintain system compliance metrics." Practice began under staffing shortfalls from two January FTE departures.
- Finding F2: 9 of 11 full-time nurses affected. Two nurses with accurate records are the charge nurses who entered the data. Pattern inconsistent with random error.
- Finding F3: Patient safety finding -- 3 nurses averaged 68-72h/week over 4-week audit period. Per JONA 2010 and Trinkoff et al. 2011, this creates 3-fold increase in medication error probability. Two near-miss events documented in independent sources (Walsh log, Kim personal incident log).
- Finding F4: Mandatory self-report to Washington State Department of Health under RCW 70.41.230 within 72 hours of formal finding. Legal counsel (Jennifer Wu) notified.
- Note on preliminary review: "The Preliminary Review found minor documentation gaps consistent with the CareScheduler data available at that time. This full audit finding does not reflect a change in compliance judgment -- it reflects the availability of additional evidence sources."
- Length: ~900 words, ~1,350 tokens

**u4_angela_discord_phase3.jsonl (Loops 15--18 appended to Angela DM):**
- Loop 15: Donna Park confirms the instruction from Linda Yee in a confidential interview. C4 Phase 3 trigger -- gaming confirmed as deliberate and instructed.
- Loop 16: Angela presents formal finding -- "systematic circumvention of overtime reporting requirements, sustained over at least 4 months." Mandatory reporting under RCW 70.41.230. Agent reads caresched_audit_findings.md and confirms C4 full reversal.
- Loop 17: Angela issues corrective action plan -- immediate scheduling relief, mandatory ClinAlert reporting refresher, interim manual hour verification protocol.
- Loop 18: Angela on staff protection -- formal finding targets the practice and instruction, not individual nurses. Donna Park's cooperation documented.

**u4_staffing_review_phase2.jsonl (Loops 13--17 appended to #staffing-review):**
- Loop 13: Angela presents formal audit finding to group. Agent reads caresched_audit_findings.md and synthesizes full evidence: Walsh records (C1), Sarah Kim and Yun clinical documentation (C2), Angela's formal audit including Donna Park interview (C4). B1 phrase definitively superseded.
- Loop 14: Robert Chen's institutional pivot -- "This is significantly beyond what I was briefed on. I need legal counsel present."
- Loop 15: Jennifer Wu's regulatory statement -- RCW 70.41.230 mandatory self-report within 72 hours. CMS survey implications.
- Loop 16: Walsh on immediate scheduling relief measures.
- Loop 17: Kenji on communication plan to broader nursing staff.

### 5.3 Runtime Checks

- [ ] File `caresched_audit_findings.md` exists in workspace directory
- [ ] File contains keywords: "systematic circumvention", "9 of 11", "Donna Park", "Linda Yee", "RCW 70.41.230", "72 hours", "4 months", "Finding F1", "Finding F2", "Finding F3", "Finding F4"
- [ ] Angela DM session (`PLACEHOLDER_ANGELA_DISCORD_UUID`) now contains Loops 15--18 (Phase 3)
- [ ] #staffing-review session (`PLACEHOLDER_STAFFING_DISCORD_UUID`) now contains Loops 13--17
- [ ] Loop 16 (Angela DM) agent reply confirms C4 full reversal from "minor irregularities" to "systematic circumvention"
- [ ] Loop 13 (#staffing-review) agent reply confirms B1 is definitively superseded and synthesizes all three evidence streams (C1, C2, C4)

### 5.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r9 | `depends_on_update` | `"u4"` |
| r9 | `update_files` | `["caresched_audit_findings.md"]` |
| r9 | `update_sessions` | `["PLACEHOLDER_ANGELA_DISCORD_UUID", "PLACEHOLDER_STAFFING_DISCORD_UUID"]` |
| r11 | `depends_on_update` | `"u4"` |
| r12 | `depends_on_update` | `"u4"` |

---

## 6. Cross-Update Consistency Checks

| Check | Expected Result |
|---|---|
| overtime_audit_report.md Amy Chen hours (68.4h) matches Walsh DM Loop 2 ("three nurses averaging over 65 hours") | Consistent (68.4 > 65) |
| badge_access_analysis.md unit average (58.2h) matches overtime_audit_report.md unit average (58.4h) within tolerance | Consistent (independent measurement, ~0.2h variance acceptable) |
| badge_access_analysis.md charge nurse match pattern (Donna Park + RN-06 accurate) matches overtime_audit_report.md finding | Consistent |
| sarahkim_symptom_timeline.md near-miss #1 (W1D4, 3:15 AM) matches Walsh DM Loop 4 and Sarah Kim DM Loop 1 | Consistent (same event, three sources) |
| sarahkim_symptom_timeline.md near-miss #2 (W-2, wrong route IV vs IM) matches Yun DM Loop 1 and Loop 8 | Consistent (same event, two sources) |
| caresched_audit_findings.md 4-month duration matches Walsh DM Loop 5 ("the CareScheduler practice started as a temporary fix") and timeline of January departures | Consistent |
| caresched_compliance_report.md average (42.3h) matches badge_access_analysis.md CareScheduler average for affected nurses (40.7h) -- slight difference because badge analysis excludes 2 charge nurses from the "affected" group | Consistent (different denominator: 11 nurses vs 9 nurses) |
| Angela's Phase 1 "minor irregularities" (DM Loop 3) -> Phase 2 "systematic" (DM Loop 12) -> Phase 3 "formal finding" (DM Loop 16) | INTENTIONAL ESCALATION -- C4 temporal DU driven by evidence accumulation |
| CareScheduler data is internally self-consistent (no obvious errors visible from system alone) | Consistent with writer constraint #5 -- gaming is only detectable by external cross-reference |
| RCW 70.41.230 cited in caresched_audit_findings.md matches icu_staffing_policy.md regulatory references | Consistent |
