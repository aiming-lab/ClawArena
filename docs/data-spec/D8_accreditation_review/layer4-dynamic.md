# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Deliver full text of 5 substantive incident reports -- triggers C1 full reversal (98.4% dashboard vs real clinical deviations) and B1+B2 reversal; confirms C2 partial reversal (documentation issue vs substantive deviations) | Yes: Walsh Discord DM Phase 2 append | Yes: incident_reports_substantive.md | R2->R4 (C1: dashboard checkbox compliance contradicted by documented substantive protocol deviations; B1 corrected); R3->R5 (C2: Angela's "documentation issue" framing refuted for 5 of 12 incidents; B2 corrected) |
| U2 | Before R6 | Deliver Amy Chen's 3 unreported incidents -- expands deviation scope and confirms real practice gaps beyond documentation timing; triggers scope expansion context | Yes: Angela Discord DM Phase 2 append, #cardiac-icu-ops Slack Phase 2 append | Yes: amy_chen_unreported_incidents.md | No new cross-round reversal; extends C2 evidence (15 total incidents, all on understaffed shifts) and contextualizes C4 scope expansion |
| U3 | Before R9 | Deliver Yun's staffing analysis -- transforms the picture from scattered incidents to systemic administration-driven failure; all 15 incidents on unauthorized understaffed shifts (p < 0.001) | Yes: Jennifer Wu Discord DM Phase 3 append, Yun Telegram DM Phase 3 append | Yes: staffing_incident_analysis.md | R2->R9 (C1+C2 comprehensive: compliance gaps reattributed from nursing performance to structural understaffing; Jennifer Wu's legal posture reverses to proactive disclosure) |
| U4 | Before R11 | No new workspace files or session appends -- marker for comprehensive synthesis assessment; all evidence delivered by Update 3 | No | No | No new cross-round reversal; enables comprehensive R11-R12 synthesis incorporating all contradictions, staffing causation, and disclosure strategy |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.
**Purpose:** Introduces the full text of the 5 substantive incident reports from Walsh's 12-incident summary. These reports describe protocol steps that were not performed per specification -- not checkbox timing errors. The reports directly show the compliance checkbox was completed on the same shifts as documented deviations, establishing that the 98.4% dashboard figure fails to capture real clinical practice gaps. Appends Phase 2 loops to the Walsh Discord DM (Walsh provides full texts; Walsh's precise 7/12 timing + 5/12 substantive breakdown). This update triggers C1 full reversal and B1+B2 corrections.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "incident_reports_substantive.md",
    "source": "updates/incident_reports_substantive.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_WALSH_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_WALSH_DISCORD_UUID.jsonl"
  }
]
```

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Introduces Amy Chen's 3 unreported incidents from the #cardiac-icu-ops channel, expanding the documented deviation count from 12 to 15. Amy explicitly states these were not documentation errors but situations where "something I should have done per protocol, I didn't do, because of workload." Appends Phase 2 loops to the Angela Discord DM (scope expansion reaction; Angela acknowledges the limitation of her "documentation issue" framing for the 5 substantive cases) and to the #cardiac-icu-ops Slack group (Amy's disclosure, Walsh's supportive response, Kenji's measured acknowledgment). This update extends C2 evidence and contextualizes the C4 scope expansion.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "amy_chen_unreported_incidents.md",
    "source": "updates/amy_chen_unreported_incidents.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ANGELA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ANGELA_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ICU_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ICU_SLACK_UUID.jsonl"
  }
]
```

### Update 3 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.
**Purpose:** Introduces Dr. Yun's staffing analysis showing all 15 incidents (12 formal + 3 Amy) clustered on unauthorized understaffed shifts (48 of 487 shifts), with zero incidents on adequately staffed or authorized surge shifts (p < 0.001). This transforms the deviation pattern from a nursing performance narrative to a systemic administration-driven failure narrative. Appends Phase 3 loops to the Jennifer Wu Discord DM (Wu reverses legal posture from "don't volunteer" to proactive disclosure; identifies administrative causation chain) and to the Yun Telegram DM (Yun presents analysis results, administrative causation, and strategic narrative reframe). This update enables the comprehensive synthesis and disclosure strategy rounds.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "staffing_incident_analysis.md",
    "source": "updates/staffing_incident_analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JENNIFER_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JENNIFER_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** No new content is introduced. This is a logical marker for the comprehensive synthesis phase. All evidence has been delivered by Update 3. Rounds R11-R12 test whether the agent can produce a complete synthesis incorporating all four contradictions, the staffing causation analysis, source reliability rankings, and the disclosure strategy, in the structured format Kenji prefers.

```json
[]
```

---

## 3. Source File Content Summaries

### updates/incident_reports_substantive.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), C2 (partial reversal), B1 (reversal trigger), B2 (reversal trigger)
**Content key points:**
- Title: "Cardiac ICU Incident Reports -- Full Text, Five Substantive Protocol Deviation Cases"
- Author: Patricia Walsh, Nurse Director (compiled from original nurse-authored reports)
- Incident 1 (dual-nurse verification): Code blue; IV epinephrine administered by single nurse without second verification; only other nurse managing active deterioration; EHR checkbox completed 3 minutes post-administration; deviation is missing second nurse, not timing
- Incident 2 (heparin co-sign): Attending unavailable overnight; dose adjustment at 03:45; co-sign checkbox marked; attending retrospective co-sign at 08:22 (4.5 hours later)
- Incident 3 (vitals monitoring): Managing 4 patients (3 post-surgical) with no backup nurse 0100-0500; extended monitoring interval from 15 to 45 minutes for 2 stable patients; CheckComplete entry at shift end
- Incident 4 (cardiac rhythm escalation): Multi-patient deterioration; rhythm alert acknowledged but not escalated per protocol for 22 minutes while managing active code for adjacent patient
- Incident 5 (defibrillator verification): Patient deteriorated before pre-use checklist could be initiated; emergency defibrillation without verification; checklist completed retrospectively
- Walsh cover note: "In all five cases, the EHR CheckComplete entry was made after the care event, not before -- so these are not early-checkbox timing errors. Protocol steps were either not performed, performed by one nurse instead of two, or performed outside the specified timeframe."

**Length estimate:** ~950 words, ~1,425 tokens

---

### updates/amy_chen_unreported_incidents.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (scope expansion), confirms real practice gaps
**Content key points:**
- Title: "Cardiac ICU -- Three Unreported Protocol Deviations (Staff Account, Nurse Amy Chen)"
- Source: Amy Chen's #cardiac-icu-ops message, W4+1
- Incident A (cardiac monitoring lead verification): Shift with 4 patients, no charge nurse; skipped lead placement verification for 2 stable patients; undetected arrhythmia for 22 minutes until next assessment; no patient harm
- Incident B (anticoagulation monitoring): Lab queue 5-hour backlog; administered warfarin without current INR results; used 6-hour-old results in range; documented as "administered per previous results" which is not protocol
- Incident C (code blue delay): Managing 3 patients alone 0300-0530; monitor alarm indicated possible arrest; called code from doorway without completing bedside assessment per protocol; approximately 3 minutes after alarm; patient survived
- Amy's framing: "not documentation errors -- things I couldn't do the way the protocol says because of the situation I was in"
- Context: incidents not filed because Amy was uncertain whether they were "errors" or "judgment calls under resource constraints"

**Length estimate:** ~750 words, ~1,125 tokens

---

### updates/staffing_incident_analysis.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C1+C2 comprehensive (systemic causation reframe)
**Content key points:**
- Title: "Cardiac ICU Staffing Ratio Analysis -- Correlation with Protocol Deviation Incidents"
- Author: Dr. Min-Ji Yun, Associate Chief of Cardiology. Date: W4+3
- Data sources: official HR staffing records (8-month period) cross-referenced with all 15 documented incidents (12 formal Walsh + 3 Amy Chen)
- Total shift records: 487
- Adequately staffed shifts (1:2 or better): 425 (87.3%) -- zero incidents
- Below-threshold shifts: 62 (12.7%), comprising: 14 authorized surge (1:3 for 4 hours with documented charge nurse approval) -- zero incidents; 48 unauthorized below-threshold shifts -- 15 incidents (all of them)
- All 15 documented incidents occurred on unauthorized below-threshold shifts
- Chi-square test: p < 0.001 -- "This is not coincidence"
- Key causal finding: "Protocol deviations are a consequence of unauthorized understaffing rather than individual nursing performance failures. The 425 adequately staffed shifts produced zero documented incidents."
- Administrative implication: 48 unauthorized shifts are on the approved staffing schedule; FTE reduction approved by CFO Robert Chen's office 14 months ago; staffing model does not maintain 1:2 ratio on night shifts during high-census periods
- Financial context: 12% Cardiac ICU staffing FTE reduction authorized 14 months ago

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_WALSH_DISCORD_UUID.jsonl (Update 1)

**File type:** session append (3 new loops: Loops 15-17)
**Associated contradictions:** C1 (reversal confirmation), B2 (explicit correction)
**Content key points:**
- Loop 15: Walsh sends full incident texts (incident_reports_substantive.md). "Read them. Then tell me if Angela's documentation-timing explanation still holds." Agent reads the full texts and explicitly revises: "These five reports describe substantive deviations from protocol requirements, not documentation timing discrepancies."
- Loop 16: Walsh provides precise breakdown: 7 of 12 genuine documentation-timing issues; 5 of 12 substantive clinical deviations. "In those five, the step was either not done, done differently, or done by fewer people than required. The checkbox was eventually checked in all five, which is why the dashboard reads 98%." Agent records this precise framing.
- Loop 17: Walsh on scope expansion: "If you submit 98% compliance with 12 incident reports, any experienced reviewer will notice those two numbers don't fit." Agent notes Walsh's prediction validated; recommends discussing proactive disclosure with Jennifer Wu.

---

### updates/PLACEHOLDER_ANGELA_DISCORD_UUID.jsonl (Update 2)

**File type:** session append (2 new loops: Loops 16-17)
**Associated contradictions:** C4 (scope expansion reaction), C2 (partial acknowledgment)
**Content key points:**
- Loop 16: Angela reacts to scope expansion. Surprised: "I thought our pre-review package was strong." Agent explains the causal chain: Joint Commission reviewers identified statistical inconsistency between 98.4% dashboard and 12-incident log.
- Loop 17: Angela acknowledges limitation after reading the 5 substantive reports. Accepts documentation timing applies to most (7 of 12) but not the 5 substantive cases. Revises pre-review narrative: "dashboard captures EHR documentation compliance; incident reports capture a separate category." Agent records Angela's acceptance of methodological limitation.

---

### updates/PLACEHOLDER_ICU_SLACK_UUID.jsonl (Update 2)

**File type:** session append (3 new loops: Loops 12-14)
**Associated contradictions:** C2 (scope expansion), Amy disclosure
**Content key points:**
- Loop 12: Amy Chen discloses 3 unreported incidents in #cardiac-icu-ops. "With the expanded review scope, I want to share three situations I haven't formally reported." Agent reads amy_chen_unreported_incidents.md; notes Amy's framing distinguishes documentation errors from practice gaps.
- Loop 13: Walsh responds supportively: "What you described is situations where circumstances made full protocol adherence impossible, not situations where a nurse chose not to follow protocol. These are system-level findings, not performance findings." Recommends inclusion in Joint Commission preparation.
- Loop 14: Kenji acknowledges in group channel: "They are now part of our preparation record... these represent systemic context, not individual performance issues." Agent notes Kenji validates systemic framing publicly.

---

### updates/PLACEHOLDER_JENNIFER_DISCORD_UUID.jsonl (Update 3)

**File type:** session append (3 new loops: Loops 11-13)
**Associated contradictions:** C1+C2 comprehensive (legal posture reversal)
**Content key points:**
- Loop 11: Jennifer reviews Yun's staffing analysis. "All 15 incidents on unauthorized understaffed shifts. None on adequately staffed shifts. This changes my advice completely." Agent records Jennifer's posture shift.
- Loop 12: Jennifer's revised advice: proactive disclosure of Yun's staffing analysis to Joint Commission reviewers at start of review week. Reframes deviations as systemic staffing problem administration is now aware of and addressing. This is the opposite of Phase 1 "don't volunteer information" posture; reversal attributed to new causal evidence.
- Loop 13: Jennifer identifies administrative causation chain: CFO budget reduction (14 months ago) -> approved staffing schedule -> 48 unauthorized understaffed shifts -> 15 protocol incidents. Advises Kenji position himself as the person who investigated, found, and disclosed the problem.

---

### updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl (Update 3)

**File type:** session append (3 new loops: Loops 13-15)
**Associated contradictions:** C1+C2 comprehensive (systemic causation)
**Content key points:**
- Loop 13: Yun presents staffing analysis results. 487 shifts, 425 at 1:2 standard (zero incidents), 62 below-threshold: 14 authorized surge (zero incidents), 48 unauthorized (all 15 incidents). Chi-square p < 0.001.
- Loop 14: Yun identifies administrative causation chain. The 48 unauthorized shifts reflect an approved staffing model that structurally produces below-ratio conditions. "Someone looked at this schedule and approved it."
- Loop 15: Yun's strategic reframe recommendation. Present to Joint Commission as: "We identified an administrative staffing policy that created structural conditions for protocol deviation. We have analyzed the pattern, identified the cause, and are prepared to present a corrective action plan." Positions department as the people who found the problem, not the people who created it.

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `incident_reports_substantive.md` exists in workspace after Update 1 | Abort R4; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_WALSH_DISCORD_UUID.jsonl` has loops >= 15 after Update 1 | Abort R4; log error |
| RC-U2-W1 | U2 | workspace | `amy_chen_unreported_incidents.md` exists in workspace after Update 2 | Abort R6; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_ANGELA_DISCORD_UUID.jsonl` has loops >= 16 after Update 2 | Abort R6; log error |
| RC-U2-S2 | U2 | session | `PLACEHOLDER_ICU_SLACK_UUID.jsonl` has loops >= 12 after Update 2 | Abort R6; log error |
| RC-U3-W1 | U3 | workspace | `staffing_incident_analysis.md` exists in workspace after Update 3 | Abort R9; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_JENNIFER_DISCORD_UUID.jsonl` has loops >= 11 after Update 3 | Abort R9; log error |
| RC-U3-S2 | U3 | session | `PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl` has loops >= 13 after Update 3 | Abort R9; log error |

---

## 5. questions.json Update Field References

Each round in `questions.json` that follows an update must include the `update` field specifying which update actions to execute before the question is injected.

| Round | Update Field Value | Notes |
|---|---|---|
| R1-R3 | `null` | Pre-update rounds (C3 non-conflict synthesis, initial C1/C2 inference, C4 Phase 1 framing) |
| R4 | `"update_1"` | References Update 1 action list (incident_reports_substantive.md + Walsh append) |
| R5 | `null` | Post-Update 1 C2 confirmation round |
| R6 | `"update_2"` | References Update 2 action list (amy_chen_unreported_incidents.md + Angela/ICU appends) |
| R7-R8 | `null` | Post-Update 2 rounds (C4 scope expansion, preference assessment) |
| R9 | `"update_3"` | References Update 3 action list (staffing_incident_analysis.md + Jennifer/Yun appends) |
| R10 | `null` | Post-Update 3 comprehensive staffing causation assessment |
| R11-R12 | `null` | Post-all-updates comprehensive synthesis and recommendation rounds |
