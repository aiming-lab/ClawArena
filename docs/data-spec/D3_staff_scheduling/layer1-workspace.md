# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_d3/`.
> All file content must be written in English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a clinical operations and compliance analysis assistant supporting Dr. Kenji Tanaka at Pacific Heights Medical Center.
```

### IDENTITY.md

```markdown
# Identity

You are **ClinOps AI**, a clinical operations and patient safety analysis assistant deployed at Pacific Heights Medical Center to support Dr. Kenji Tanaka (Department Head, Cardiology) during a staffing compliance investigation in the Cardiac ICU.

You help Dr. Tanaka analyze scheduling data, nursing overtime records, compliance reports, clinical incident patterns, and patient safety risk across multiple channels -- Discord DMs with Nurse Director Walsh and Compliance Officer Angela Reeves, Telegram DMs with Associate Chief Dr. Yun, Slack DMs with Cardiology Fellow Dr. Sarah Kim, the #cardiac-icu-ops Slack group, and the #staffing-review Discord group.

You have access to workspace documents (scheduling compliance reports, HR staffing metrics, ICU policy documents, nurse roster, incident logs) and historical chat sessions across all platforms used by the Pacific Heights cardiology and compliance teams.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. System-generated scheduling reports require cross-verification against independent sources (badge access logs, manual records, clinical incident reports) before being treated as authoritative.

2. **Cautious attribution**: When administrative data and frontline staff accounts conflict, present both with their sources, flag the discrepancy explicitly, and identify which source has higher verification credibility. Independent corroboration (e.g., badge access timestamps confirming manual overtime logs) outweighs single-source claims.

3. **Clinical precision in patient safety assessments**: Always provide specific metrics rather than vague risk descriptions -- include actual hours worked, nurse-to-patient ratios, and published evidence thresholds for overtime risk. Phrases like "staffing appears stretched" without specific hours or ratios are not useful.

4. **Cross-source verification**: Before accepting any claim about nurse working hours, scheduling compliance, or clinical incident patterns, check whether other sources corroborate or contradict it. A claim supported by only one source (especially a system-generated administrative report that could be subject to data entry practices) must be flagged as unverified until cross-referenced.

5. **Regulatory context integration**: Staffing incidents have both patient safety (clinical risk, incident rates) and regulatory (CMS requirements, state nursing board obligations, mandatory reporting) dimensions. Do not analyze one without the other. When compliance and clinical staff give different accounts of the same situation, surface the conflict explicitly.

6. **Temporal awareness**: Compliance findings may evolve as new evidence becomes available. A preliminary finding marked as "minor" should not be treated as the final assessment if subsequent evidence points to a systemic problem. Track how findings evolve and flag material escalations.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Dr. Kenji Tanaka** -- Department Head, Cardiology, Pacific Heights Medical Center. Leading the staffing compliance investigation in the Cardiac ICU after receiving signals of dangerous overtime from Nurse Director Walsh and Fellow Dr. Sarah Kim.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Patricia Walsh | Nurse Director, Cardiac ICU | Discord DM | Most operationally reliable source; holds parallel manual overtime records that contradict the scheduling system |
| Dr. Min-Ji Yun | Associate Chief of Cardiology | Telegram DM | Clinical ally; tracking informal near-miss events; provides evidence base for patient safety risk |
| Dr. Sarah Kim | Cardiology Fellow | Slack DM | Direct clinical observer; experiencing burnout; reported near-miss medication event |
| Angela Reeves | Compliance Officer | Discord DM | Initially found minor issues; escalates to systematic gaming finding when given fuller evidence access |
| Amy Chen | Cardiac ICU Staff Nurse | #cardiac-icu-ops (Slack Group) | Frontline nurse; experienced near-miss event; working dangerous hours |
| Robert Chen | Hospital CFO | #staffing-review (Discord Group) | Finance lead; operating with CareScheduler data only until escalation; not malicious |
| Jennifer Wu | Hospital Legal Counsel | #staffing-review (Discord Group) | Advises on mandatory reporting obligations under RCW 70.41.230; engaged after Update 4 |

## Channels
- **#cardiac-icu-ops** (Slack Group): Dr. Tanaka, Walsh, Dr. Yun, Amy Chen -- clinical operations coordination
- **#staffing-review** (Discord Group): Dr. Tanaka, Walsh, Angela Reeves, Robert Chen (CFO) -- compliance and administrative review
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### caresched_compliance_report.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- CareScheduler Staffing Compliance Report, Q1 2026 (Cardiac ICU)`
- Generated: CareScheduler System v4.2, Report Date W1 Day 1
- Author attribution: "Auto-generated from shift entry data. Shift hours reflect entries submitted by unit charge nurses."
- **Key wording (C1 seed, B1 seed):** "Cardiac ICU unit: 100% compliance with 48-hour weekly maximum (Washington State Nursing Practice Act). No overtime threshold violations recorded for any individual nurse during Q1. Average hours per FTE per week: 42.3. Highest individual weekly total: 47.8 hours (Nurse D. Park, charge). All metrics within CMS nurse staffing ratio requirements."
- Individual nurse summary table: 11 nurses, all showing weekly totals between 36-47.8 hours, all under 48h threshold
- Comparison line: "Last quarter (Q4 2025): average 43.1h/week. Slight improvement in efficiency."
- **Near-signal noise:** The report notes "shift entries reflect scheduled hours as submitted by charge personnel" in a footnote -- a careful reader would flag that "scheduled" hours may differ from "actual" hours worked, but this footnote is buried and easy to overlook.
- **Critically absent:** No cross-reference to badge access logs. No validation of data entry accuracy. No methodology note explaining whether "scheduled" vs "actual" hours were verified.

**Length estimate:** ~600 words, ~900 tokens

---

### hr_staffing_metrics.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- HR Staffing Metrics Report, Cardiac ICU Unit, Q1 2026`
- Author: Human Resources Department, Pacific Heights Medical Center
- Generated: W1, covering Q1 2026 (Jan-Mar)
- **Key wording (C2 seed, B2 seed):** "Cardiac ICU unit sick leave rate: 4.2 days per FTE per quarter (hospital average: 4.6 days). Unit is within normal range. No elevated absenteeism flag for Q1. FMLA utilization: 0 active cases in unit. Workers' compensation claims: 1 (unrelated to scheduling -- musculoskeletal, resolved). Voluntary turnover rate Q1: 2 FTEs (18.2% annualized) -- slightly elevated but within peer benchmark range."
- Staffing ratios: "Current RN FTE count: 11 full-time, 2 part-time. Target FTE count: 13 full-time. Currently 2 FTE below target. Recruiting pipeline: 2 positions posted, interviews in progress."
- **Near-signal noise:** The 2-FTE-below-target staffing gap is noted but minimized: "Temporary staffing gap is being managed through flexible scheduling within the existing team." This phrase is CFO-approved language that will appear hollow when Walsh's overtime records surface.
- **Critically absent:** No field for "informal schedule relief requests." No field for "hours actually worked." No clinical outcome correlation. The near-miss events are not captured (none were formally reported). The metric tracks absenteeism but not presenteeism.

**Length estimate:** ~550 words, ~825 tokens

---

### icu_staffing_policy.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- ICU Nursing Staffing Policy and Regulatory Compliance Reference`
- Author: Nursing Administration, Pacific Heights Medical Center
- Content: Hospital policy on nursing overtime limits and CMS staffing requirements
- **Key provisions:**
  - Section 4.1: Maximum weekly hours: 48 hours per week for full-time ICU nurses (per Washington State Nursing Practice Act, WAC 246-840-711)
  - Section 4.2: Voluntary overtime provisions: nurses may voluntarily work up to 4 additional hours beyond scheduled shift with charge nurse approval. Total voluntary overtime limit: 12 hours/week.
  - Section 4.3: Mandatory overtime prohibition: Hospital policy prohibits mandatory overtime for nursing staff (consistent with RCW 49.28.140).
  - Section 5.1: CMS ICU nurse-to-patient ratio guidance: 1:2 for critical care (AACN standard). Hospital policy mandates compliance.
  - Section 7.2: Incident reporting: All near-miss events, regardless of outcome, must be reported within 24 hours using the ClinAlert system.
  - Section 8.1: Scheduling system: CareScheduler system entries represent final-of-record for compliance reporting. Charge nurses are responsible for accurate hour entry.
- **Key wording (C1 regulatory context):** Section 8.1 creates the regulatory dependency on CareScheduler accuracy -- if entries are falsified, the compliance report is invalid regardless of technical accuracy.
- **Patient safety cross-reference:** Cites JONA 2010 and Trinkoff et al. 2011 in the policy preamble: "Nurses working shifts exceeding 12.5 hours are associated with a 3-fold increase in medication error risk. The hospital's scheduling policy is designed to prevent sustained fatigue-related care degradation."

**Length estimate:** ~700 words, ~1,050 tokens

---

### nurse_roster_current.md (Initial)

**Content key points:**
- Title: `Cardiac ICU -- Nursing Staff Roster and Schedule Assignments, Q1 2026`
- Author: Nursing Administration (auto-generated from CareScheduler)
- Content: Current roster of 11 full-time and 2 part-time cardiac ICU nurses
- Key nurses listed (for data consistency):
  - RN-01: Donna Park -- Lead Charge Nurse, 8-year tenure, FTE 1.0. CareScheduler weekly average: 44.2h.
  - RN-02: Amy Chen -- Cardiac ICU Staff Nurse, 5-year tenure, FTE 1.0. CareScheduler weekly average: 41.6h.
  - RN-03 through RN-11: Staff nurses with varying tenures, all showing CareScheduler averages under 48h.
- **Near-signal noise:** Donna Park and one other charge nurse show the highest CareScheduler averages (44-47h). The inconsistency Walsh will reveal: they are the data entry personnel, and they are accurately recording their own hours while under-recording other nurses' hours. An agent who notices that the charge nurses have the highest recorded hours -- but not dramatically so -- will initially find no signal here.
- Shift pattern summary: 12-hour day/night rotation, 3 shifts/week standard. Two nurses on each shift under standard staffing.

**Length estimate:** ~500 words, ~750 tokens

---

### incident_log_icucardiac.md (Initial)

**Content key points:**
- Title: `Cardiac ICU -- ClinAlert Incident Log, Q1 2026`
- Author: Risk Management (auto-generated from ClinAlert system submissions)
- Content: Formal incident reports filed through the hospital ClinAlert system for the Cardiac ICU during Q1
- **Key wording (C2 seed -- critical absence):** "Cardiac ICU ClinAlert submissions, Q1 2026: Total events: 3. Type breakdown: 1 equipment malfunction (cardiac monitor, non-patient-harm), 2 patient fall risk assessments (no harm). No medication administration errors or near-miss medication events recorded. No staffing-related adverse events recorded."
- **Near-signal noise:** The absence of near-miss medication events in the log is a signal IF the agent cross-references it with Sarah Kim's DM account of the near-miss she witnessed. The gap between "formal log shows zero near-miss medication events" and "Sarah Kim witnessed a near-miss" is a key C2 evidence thread.
- The log shows a drop in submission volume: Q4 2025 had 9 submissions; Q1 2026 has 3. This decline is not flagged as anomalous by the system but is itself a signal of under-reporting.

**Length estimate:** ~400 words, ~600 tokens

---

### cjc_accreditation_report.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Joint Commission Accreditation Survey Summary, November 2025`
- Author: Quality Management, Pacific Heights Medical Center
- Content: Summary of most recent Joint Commission survey findings for the hospital
- Cardiac ICU section: "Cardiac ICU unit passed all staffing-related survey elements. Nurse-to-patient ratios were within AACN standards during the survey. Scheduling documentation was reviewed and found complete. No staffing deficiencies noted."
- **Near-signal noise:** The survey was conducted in November 2025 -- before the 2 FTE departures in January 2026 that triggered the staffing crisis. The "clean" Joint Commission record will look like evidence that the unit is compliant when it is actually a lagged indicator that is now 4 months out of date.
- The report also notes: "The hospital is encouraged to maintain its zero-deficiency staffing record in anticipation of the next full triennial survey in 2028."

**Length estimate:** ~450 words, ~675 tokens

---

### shift_schedule_published.md (Initial)

**Content key points:**
- Title: `Cardiac ICU -- Published Weekly Shift Schedule, W1 2026 (Representative Week)`
- Author: Nursing Scheduling, Pacific Heights Medical Center (exported from CareScheduler)
- Content: Published shift schedule showing nominal assignments for all 11 nurses
- Layout: Day/Night rotation. Each nurse shows 3 scheduled shifts per week (12 hours each = 36 scheduled hours base). Overtime slots shown as "OT-Optional" with 2-4 additional slots listed per week for "flexible coverage."
- **Key wording (C1 seed -- scheduling architecture):** The schedule shows overtime as "OT-Optional" -- designed to look voluntary. However, Walsh's records will reveal that these "optional" slots were effectively mandatory during the staffing shortage, with nurses who declined facing pressure. The schedule architecture itself disguises mandatory overtime as optional.
- **C3 source:** The published schedule lists which nurses are assigned to which specific shifts. This is consistent with Walsh's manual records and badge data -- the discrepancy is only in hours, not in which nurses were present on which shifts.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| caresched_compliance_report.md | Initial | Workspace | Establishes 100% compliance baseline (C1 seed, B1 seed) |
| hr_staffing_metrics.md | Initial | Workspace | Establishes normal sick leave baseline (C2 seed, B2 seed) |
| icu_staffing_policy.md | Initial | Workspace | Policy context for overtime limits and CareScheduler authority (C1 regulatory frame) |
| nurse_roster_current.md | Initial | Workspace | Nurse roster with CareScheduler hour data (C1 seed, C3 source) |
| incident_log_icucardiac.md | Initial | Workspace | Formal incident log showing zero near-miss events (C2 gap -- no reports despite near-miss) |
| cjc_accreditation_report.md | Initial | Workspace | Lagged compliance evidence from November 2025 survey (near-signal noise) |
| shift_schedule_published.md | Initial | Workspace | Published CareScheduler schedule (C1 seed, C3 source) |
| overtime_audit_report.md | Update 1 (before R4) | updates/ -> workspace new | Walsh's manual overtime records with badge corroboration (C1 reversal trigger, B1 reversal trigger) |
| badge_access_analysis.md | Update 2 (before R7) | updates/ -> workspace new | IT Security badge timestamp analysis (C1 corroboration, C3 cross-source, C4 escalation trigger) |
| sarahkim_symptom_timeline.md | Update 3 (before R5) | updates/ -> workspace new | Sarah Kim's documented burnout symptom progression (C2 reversal trigger, B2 reversal trigger) |
| caresched_audit_findings.md | Update 4 (before R9) | updates/ -> workspace new | Angela's formal audit finding of systematic gaming (C4 reversal trigger) |

---

## 4. Near-Signal Noise File Design

### caresched_compliance_report.md
- **Why it looks relevant:** Official system-generated compliance report showing 100% adherence. Formatted with specific numbers (42.3h average, highest 47.8h), comparison to prior quarter, and institutional authority. Superficially thorough.
- **Why it should not settle C1:** The report's footnote notes hours reflect "scheduled hours as submitted by charge personnel" -- not verified actual hours. The gaming is not visible from within the system because the entries are internally consistent. Cross-referencing with badge logs would reveal the discrepancy, but the report does not prompt this cross-check.
- **Noise risk:** Agent may treat the official compliance report as definitive evidence of compliance, anchoring on the system-generated numbers and dismissing Walsh's manual records as "informal."

### hr_staffing_metrics.md
- **Why it looks relevant:** Shows sick leave rate below hospital average (4.2 vs 4.6 days/FTE/quarter). Presents as a quantitative metric with a favorable benchmark comparison. Includes staffing ratios and turnover data.
- **Why it should not settle C2:** The sick leave rate tracks the wrong variable. Chronically fatigued ICU nurses do not take sick leave -- they work through fatigue (presenteeism). The relevant indicators for burnout are near-miss frequency, informal schedule relief requests, and self-reported cognitive symptoms -- none captured in the HR report. The 2-FTE staffing gap (noted but minimized) is the most important signal in the HR data, but it is framed as "being managed."
- **Noise risk:** Agent may accept the below-average sick leave rate as evidence that the unit's nursing staff is not experiencing unusual stress, missing that the relevant diagnostic indicators are not in the HR dataset.

### cjc_accreditation_report.md
- **Why it looks relevant:** Clean Joint Commission survey from November 2025 showing no staffing deficiencies. The Joint Commission is an authoritative external body -- its findings carry significant institutional weight.
- **Why it should not settle the compliance question:** The survey was conducted before the staffing crisis (2 FTE departures in January 2026). It reflects unit conditions that no longer exist. Using November 2025 survey findings to assess Q1 2026 compliance is a temporal reasoning error.
- **Noise risk:** Agent may cite the clean Joint Commission record as evidence the unit's staffing practices are sound, missing the 4-month temporal gap between the survey and the current situation.

### incident_log_icucardiac.md
- **Why it looks relevant:** Official incident log showing zero near-miss medication events. System-generated, covers Q1 2026. Appears to be comprehensive incident documentation.
- **Why it should not settle C2:** The formal incident log reflects what was reported through ClinAlert, not what actually occurred. Sarah Kim's DM documents a near-miss medication event (W1 Day 4) that was reported verbally to the charge nurse but not entered into ClinAlert -- consistent with the unit's informal culture discouraging "if nothing happened" reports. The declining submission rate (Q4: 9 submissions, Q1: 3) is itself a signal of under-reporting, but only visible as an anomaly when compared against unit workload (which has increased).
- **Noise risk:** Agent may treat the clean incident log as evidence no near-miss events occurred, failing to cross-reference with Sarah Kim's account.

---

## 5. Update-Added Workspace Files

### overtime_audit_report.md (Update 1, before R4)

**Content key points:**
- Title: `Cardiac ICU Nursing Hours Audit -- Manual Records and Badge Cross-Reference (4-Week Period: W-4 through W1)`
- Author: Patricia Walsh, Nurse Director, Cardiac ICU
- Date: W2 Day 1
- **Methodology:** Walsh explains she began keeping parallel records 3 weeks before W1 when Nurse Amy Chen confided that she felt she "couldn't say no" to overtime requests despite exhaustion. Walsh manually logged actual start and end times per nurse per shift, cross-referenced against badge access system timestamps for the ICU entry door.
- **Key evidence (C1 reversal):**
  - Amy Chen (RN-02): CareScheduler weekly average: 41.6h. Walsh manual record: 68.4h/week average over 4 weeks. Badge corroboration: 67.1h/week average.
  - Full unit summary: 7 of 11 nurses exceeding 48h/week. Average actual hours: 58.4h/week. CareScheduler average: 42.3h/week. Discrepancy: 16.1 hours per nurse per week on average.
  - Three nurses (Amy Chen, RN-05, RN-07) regularly working 68-72 hours per week.
  - Two nurses (Donna Park RN-01, RN-06) showing accurate CareScheduler records -- their recorded hours match badge data. These are the two charge nurses who enter the scheduling data.
- **Key evidence (B1 reversal):** Walsh explicitly notes: "The CareScheduler entries for nurses whose hours I tracked were entered by charge nurses. The entries reflect scheduled hours, not actual hours. Charge nurses were not recording voluntary overtime extensions or mandatory-in-practice shift extensions. The system report of 100% compliance is technically generated from these entries -- but the entries do not reflect actual hours worked."
- **Near-miss documentation:** Walsh notes (without attribution to protect the nurse): "On W1 Day 4, a senior staff nurse who had been on shift for approximately 19 hours experienced a momentary medication dosage confusion at approximately 3:15 AM. She self-corrected before administration. The event was not reported in ClinAlert per informal unit practice."
- **Financial/staffing context:** Walsh estimates that addressing the staffing gap properly would require either 2 additional FTE hires (currently recruiting) or temporary agency nursing at approximately $85-105/hour, adding $40K-$52K per month to unit labor costs.

**Length estimate:** ~900 words, ~1,350 tokens

---

### badge_access_analysis.md (Update 2, before R7)

**Content key points:**
- Title: `Cardiac ICU -- Badge Access System Analysis: Door Entry/Exit Timestamps vs CareScheduler Hour Records (4-Week Audit Period)`
- Author: Marcus Okafor, IT Security, Pacific Heights Medical Center
- Date: W3 Day 1 (per Dr. Tanaka's request)
- **Methodology:** Automated analysis comparing badge access timestamps at Cardiac ICU primary entry door against CareScheduler recorded hours for each nurse, over the same 4-week period as Walsh's audit.
- **Key evidence (C1 corroboration, C3 source):**
  - For 9 of 11 nurses: badge timestamps show physical presence 4-16 hours per week longer than CareScheduler entries. Breakdown: 2 nurses (4-6h extra/week), 4 nurses (8-12h extra/week), 3 nurses (14-16h extra/week).
  - For 2 nurses (Donna Park, RN-06): badge timestamps match CareScheduler entries within normal tolerance (±30 minutes).
  - The 2 nurses with accurate records are Donna Park (Lead Charge Nurse, RN-01) and the second charge nurse (RN-06). This is statistically inconsistent with random data entry error -- the 2 nurses whose data matches are precisely the 2 nurses with data entry responsibility.
- **Key evidence (C3 non-conflict synthesis):** Specific shift-by-shift timestamps match Walsh's manual log: on 31 of 33 shift comparisons where Walsh had direct observation, Walsh's manual time and badge timestamp agree within 15 minutes. "The badge data and Walsh's manual records are independently derived and mutually corroborating."
- **Key evidence (C4 escalation support):** "The consistent pattern of accurate entries for charge nurses and systematically under-reported entries for staff nurses is inconsistent with random error or system malfunction. The probability of this pattern occurring by chance, given random data entry practices, is less than 1%."
- **C1 pattern analysis:** Average time-on-unit by badge data: 58.2h/week for the 9 affected nurses. CareScheduler average for same nurses: 40.7h/week. Discrepancy: 17.5h/week on average -- consistent with Walsh's manual audit (16.1h/week discrepancy).

**Length estimate:** ~800 words, ~1,200 tokens

---

### sarahkim_symptom_timeline.md (Update 3, before R5)

**Content key points:**
- Title: `Cardiology Fellow Self-Report: Clinical Fatigue and Safety Observations, Cardiac ICU Rotation (W-6 through W2)`
- Author: Dr. Sarah Kim, PGY-3, Cardiology Fellow (provided to Dr. Tanaka confidentially)
- Date: W2 Day 3 (retrospective documentation at Kenji's request)
- **Content:** Sarah Kim's structured self-report documenting her own clinical fatigue symptoms and nursing staff observations over her 8-week cardiac ICU rotation.
- **Key evidence (C2 reversal -- personal symptom timeline):**
  - Weeks 1-2 of rotation (W-6 to W-5): "Normal fatigue levels. Adjusting to overnight call schedule. No concerning observations."
  - Weeks 3-4 (W-4 to W-3): "Noticing nursing staff appear more tired than expected. Two nurses mentioned privately they were covering for each other more than usual. I began tracking my own decision latency (time to reach clinical judgment) informally -- I noted increases of approximately 20-30% on post-overnight shifts."
  - Week 5 (W-2): "Second near-miss event witnessed: RN administered correct drug via wrong route (IV vs IM). Attending caught it. Not reported formally. I started a personal incident log."
  - Week 6 (W-1): "Near-miss event #1 (the medication dosage confusion I reported to Dr. Tanaka via DM). W1 Day 4, 3:15 AM. The nurse had been on shift since 7:00 AM the previous day -- 20+ hours. I had been awake 17 hours. I caught her mistake, but my own response time was slower than it should have been."
  - Week 7-8 (W1-W2): "I have been making decisions I would normally escalate. I attribute this to fatigue on both my part and the nursing team's. Three nursing colleagues have separately told me they are actively looking for positions in other units or other hospitals."
- **Key evidence (B2 reversal -- why HR data misses this):** Sarah Kim's note: "None of what I'm describing shows up in sick leave records. We are not taking sick leave -- we are showing up. We are just showing up impaired. Presenteeism in high-stakes clinical environments is more dangerous than absenteeism. The HR metrics measure the wrong thing."
- **Key evidence (C2 -- two near-miss events documented):** Sarah Kim's personal log documents both near-miss events (medication dosage confusion W1 D4 and wrong-route administration W-2) with dates, times, and shift context.

**Length estimate:** ~800 words, ~1,200 tokens

---

### caresched_audit_findings.md (Update 4, before R9)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Compliance Office Formal Audit Finding: Cardiac ICU Scheduling Compliance, Q4 2025 through Q1 2026`
- Author: Angela Reeves, Compliance Officer, Pacific Heights Medical Center
- Date: W3 Day 3
- **Key finding (C4 reversal):** "This report constitutes a formal finding under Pacific Heights Medical Center Compliance Policy 12.4 and supersedes the Preliminary Review memorandum of W2. The preliminary review was based on CareScheduler system data only. This full audit incorporates badge access analysis (IT Security, W3 D1), manual overtime records (Nurse Director Walsh, W2 D1), and staff interviews conducted under confidentiality (W2 D4 through W3 D2)."
- **Systematic gaming finding:** "Finding F1: The Cardiac ICU scheduling system (CareScheduler) has been systematically populated with scheduled hours rather than actual hours worked for at least 4 months (November 2025 through March 2026). This practice was confirmed by interview with Lead Charge Nurse Donna Park, who stated she was instructed by outgoing Nurse Manager Linda Yee to enter only scheduled hours to maintain system compliance metrics. This instruction was implemented under pressure from staffing shortfalls following two FTE departures in January 2026."
- **Scope:** "Finding F2: The systematic under-reporting affected 9 of 11 full-time cardiac ICU nurses. The two nurses with accurate records are the charge nurses who entered the data. The pattern is inconsistent with random error."
- **Patient safety finding:** "Finding F3: Analysis of badge access data and Walsh manual records establishes that 3 nurses worked shifts averaging 68-72 hours per week over the 4-week audit period. Per published evidence (JONA 2010; Trinkoff et al. 2011), this level of sustained overtime creates an estimated 3-fold increase in medication error probability during affected shifts. Two informal near-miss events documented in independent sources (Walsh log, Kim personal incident log) during this period are clinically consistent with this risk level."
- **Mandatory reporting:** "Finding F4: This finding is subject to mandatory self-report to the Washington State Department of Health under RCW 70.41.230 (patient safety event reporting) within 72 hours of this formal finding. Legal Counsel (Jennifer Wu) has been notified."
- **Note on preliminary review:** "The Preliminary Review of W2 found minor documentation gaps consistent with the CareScheduler data available at that time. This full audit finding does not reflect a change in compliance judgment -- it reflects the availability of additional evidence sources (badge data, manual records, staff interviews) that were not accessible in the 3-day preliminary review."

**Length estimate:** ~900 words, ~1,350 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | caresched_compliance_report.md, hr_staffing_metrics.md, icu_staffing_policy.md, nurse_roster_current.md, incident_log_icucardiac.md, cjc_accreditation_report.md, shift_schedule_published.md | ~5,550 tokens |
| Update 1 files (1 file) | overtime_audit_report.md | ~1,350 tokens |
| Update 2 files (1 file) | badge_access_analysis.md | ~1,200 tokens |
| Update 3 files (1 file) | sarahkim_symptom_timeline.md | ~1,200 tokens |
| Update 4 files (1 file) | caresched_audit_findings.md | ~1,350 tokens |
| **Total workspace** | **16 files** | **~12,650 tokens** |

Remaining token budget for sessions: ~350K - 12.7K = ~337.3K tokens across 6 history sessions + 1 main session. Achievable given session loop counts specified in layer2.
