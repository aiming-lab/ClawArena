# Layer 4 -- Dynamic Updates

> This document specifies the 4 runtime updates that inject new workspace files and session appends into the scenario during evaluation.
> Each update triggers before a specific eval round, introduces new evidence, and may reverse prior agent biases or contradiction assessments.

---

## 1. Update Summary Table

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R3 | Introduce Kenji's compiled budget history analysis (budget_history.md); reinforces C3 non-conflict synthesis and partially reverses B2 by showing equipment deferral reclassification | No new session appends | Yes -- `budget_history.md` | C3 reinforcement; B2 partial reversal (equipment deferral "non-critical" label debunked) |
| U2 | Before R5 | Introduce Dr. Yun's clinical impact analysis (impact_analysis_v1.md) and Yun Phase 2 DM loops; triggers C1 full reversal and B1+B2 full reversal | Yes -- append 3 loops to `PLACEHOLDER_YUN_TELEGRAM_UUID` (Loops 15--17) | Yes -- `impact_analysis_v1.md` | C1: R2->R5; B1 full reversal; B2 full reversal |
| U3 | Before R7 | Introduce board meeting memo (board_memo_extract.md) and #dept-heads-budget Phase 2 append; triggers C2 full reversal | Yes -- append 4 loops to `PLACEHOLDER_BUDGET_FEISHU_UUID` (Loops 19--22) | Yes -- `board_memo_extract.md` | C2: R3->R7 |
| U4 | Before R9 | Introduce Robert's formal deadline memo (finance_ultimatum_memo.md) and Robert Phase 2 DM loops; triggers C4 full reversal | Yes -- append 3 loops to `PLACEHOLDER_ROBERT_FEISHU_UUID` (Loops 15--17) | Yes -- `finance_ultimatum_memo.md` | C4: Phase 1->Phase 2 (temporal DU) |

---

## 2. Update 1 -- Budget History Analysis (Before R3)

### 2.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "budget_history.md",
    "source": "updates/u1_budget_history.md"
  }
]
```

### 2.2 Source File Content Summaries

**budget_history.md:**
- Title: "Pacific Heights Medical Center -- Cardiology Department Budget History: 7-Year Trend Analysis with Case Volume and Acuity Adjustments"
- Author: Dr. Kenji Tanaka, Department Head (compiled from Finance and Clinical Records)
- Date: W3 early
- Key evidence:
  - Table 1: FY2017-FY2023 budget share -- same data as annual_budget_reports.md (16.2% to 13.8% decline). Confirms C3 non-conflict consistency.
  - Table 2: Budget per case (inflation-adjusted): FY2017 $2,670 to FY2023 $2,476 -- a 7.3% real efficiency improvement during 22% case volume growth.
  - Table 3: Budget per case acuity-adjusted: FY2017 $1,467 to FY2023 $1,360 -- an additional 7.2% efficiency on top of nominal improvement.
  - Table 4: Cath lab imaging system (#CATH-01) replacement history: installed FY2015 (9 years of service), last major overhaul FY2019, current reliability 78%. Equipment was never classified as "non-critical" in any prior capital plan.
- B2 partial reversal: The equipment history shows the $640K deferral includes equipment never previously classified as "non-critical" -- Robert's framing is a new reclassification.
- C3 synthesis conclusion: "The 7-year budget trend shows cardiology has achieved genuine efficiency improvements while increasing case volume 22%. The department's budget share has nonetheless declined. The proposed additional 15% cut would require efficiency improvements beyond what has already been achieved."
- Length: ~700 words, ~1,050 tokens

### 2.3 Runtime Checks

- [ ] File `budget_history.md` exists in workspace directory
- [ ] File contains keywords: "16.2%", "13.8%", "7.3%", "22%", "CATH-01", "78%", "non-critical", "FY2017", "FY2023"
- [ ] Data in Table 1 matches annual_budget_reports.md (C3 consistency)
- [ ] Equipment replacement history contradicts "non-critical" label from efficiency_proposal.md

### 2.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r3 | `depends_on_update` | `"u1"` |
| r3 | `update_files` | `["budget_history.md"]` |

---

## 3. Update 2 -- Clinical Impact Analysis (Before R5)

### 3.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "impact_analysis_v1.md",
    "source": "updates/u2_impact_analysis_v1.md"
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

**impact_analysis_v1.md:**
- Title: "Clinical Impact Analysis: Proposed 15% Cardiology Budget Reduction -- Patient Outcomes Assessment"
- Author: Dr. Min-Ji Yun, Associate Chief of Cardiology
- Date: W3
- Methodology section (B1 and B2 full reversal):
  - Acuity gap identification: Finance team uses national benchmark WAI 1.41; Pacific Heights operates at WAI 1.82 (29% above benchmark). Staffing ratios appropriate for 1.41 WAI are unsafe for 1.82 WAI.
  - Acuity-adjusted nursing FTE comparison: Finance model projects 3.7 nurses/AOB (national benchmark); Pacific Heights' minimum safe staffing at WAI 1.82 per Joint Commission guidance is 3.9-4.1; current is 4.2 (at lower bound, no surge buffer).
  - Equipment deferral analysis: #CATH-01 at 78% reliability, MTBF 14 days; deferral projects 31-38 unplanned outages annually, causing 45-60 procedure deferrals.
- Core findings (C1 full reversal):
  - Staffing impact: 3.1 FTE reduction brings staffing to 3.5 nurses/AOB -- below Joint Commission minimum.
  - Door-to-balloon time: STEMI protocol requires 4.0 nurses/AOB; at 3.5, estimated time rises from 58 min to 74-81 min (threshold: 90 min). Safety margin eroded from 32 min to 9-16 min.
  - 30-day readmission: Risk-adjusted increase projected at 1.8-2.4 percentage points (from 8.3% to 10.1-10.7%).
  - Equipment revenue loss: $1.1-1.4M in deferred procedure revenue from cath lab outages.
- Financial impact: Net savings under proposed cut = $0 to $400K, not $1.8M (once offsetting costs included: equipment revenue loss $1.1-1.4M + readmission costs $280-420K).
- Conclusion: "The proposed budget reduction is not clinically viable at Pacific Heights' current patient acuity level without creating material patient safety risk."
- Length: ~900 words, ~1,350 tokens

**u2_yun_telegram_phase2.jsonl (Loops 15--17 appended to Yun DM):**
- Loop 15: Yun submits impact_analysis_v1.md. Agent reads it and explicitly corrects B2 ("$1.8M projection was based on two hidden inputs -- 1.41 vs 1.82 acuity gap and equipment deferral misclassification -- net savings are $0-$400K, not $1.8M") and B1 ("benchmark comparison is unadjusted for patient acuity; above-benchmark cost-per-case is explained by above-benchmark acuity").
- Loop 16: Yun on variance request strategy -- door-to-balloon safety margin erosion (32 min to 9-16 min) is the most compelling data point for Joint Commission purposes.
- Loop 17: Yun on the orthopedics connection -- notes the board memo (if real) changes the character of the process from flawed methodology to deliberate misdirection.

### 3.3 Runtime Checks

- [ ] File `impact_analysis_v1.md` exists in workspace directory
- [ ] File contains keywords: "1.82", "1.41", "29%", "3.1 FTE", "74-81 minutes", "door-to-balloon", "$640K", "CATH-01", "78%", "1.8-2.4 percentage points", "$0", "$400K"
- [ ] Yun DM session (`PLACEHOLDER_YUN_TELEGRAM_UUID`) now contains Loops 15--17
- [ ] Loop 15 agent reply contains explicit B1 and B2 reversal language
- [ ] Financial figures are internally consistent: $1.8M target minus $1.1-1.4M revenue loss minus $280-420K readmission cost = net $0-$400K

### 3.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r5 | `depends_on_update` | `"u2"` |
| r5 | `update_files` | `["impact_analysis_v1.md"]` |
| r5 | `update_sessions` | `["PLACEHOLDER_YUN_TELEGRAM_UUID"]` |
| r6 | `depends_on_update` | `"u2"` |
| r8 | `depends_on_update` | `"u2"` |

---

## 4. Update 3 -- Board Meeting Memo (Before R7)

### 4.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "board_memo_extract.md",
    "source": "updates/u3_board_memo_extract.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_BUDGET_FEISHU_UUID",
    "source": "updates/u3_budget_channel_phase2.jsonl"
  }
]
```

### 4.2 Source File Content Summaries

**board_memo_extract.md:**
- Title: "Pacific Heights Medical Center Board of Directors -- Closed Session Summary: Capital Projects and Budget Allocation (Excerpt)"
- Source note: Excerpt provided to Dr. Tanaka by Dr. David Park from a board member contact. Consistent with full board minutes on file. Not independently authenticated by Finance.
- Date of board meeting: 8 weeks before Operational Excellence announcement
- Key evidence (C2 full reversal):
  - Item 3: Orthopedics Wing Capital Project approved ($28,000,000). Construction timeline: 24 months, anticipated opening Q1 FY2027.
  - Item 4: Budget Neutrality Requirement. Board directed Finance to identify $4,200,000 in annual operating savings from cardiology, neurology, and internal medicine to offset debt service. Timeline: FY2024.
  - Item 5: Communications. CEO Whitfield noted savings initiative should be presented as "operational efficiency" to minimize stakeholder friction. Finance team to prepare benchmark documentation.
- Key significance: Memo predates Operational Excellence announcement by 6 weeks. Item 4 names the target departments and $4.2M savings amount (matching cardiology $1.8M + neurology $1.2M + internal medicine $1.2M). Item 5 explicitly states the efficiency framing was a communications strategy.
- C2 direct: Whitfield's "no department favorites" statement is directly contradicted by Item 5 and the pre-approval of orthopedics.
- Length: ~700 words, ~1,050 tokens

**u3_budget_channel_phase2.jsonl (Loops 19--22 appended to #dept-heads-budget):**
- Loop 19: Park surfaces the board memo in the group channel, sharing key content. Agent reads board_memo_extract.md and identifies the C2 full reversal -- orthopedics expansion was the explicit driver; efficiency framing was a communications strategy.
- Loop 20: Robert Chen responds defensively ("parallel initiatives, not cause-and-effect"), does not deny the memo's content. Agent notes Robert has not challenged the memo's authenticity and his "parallel initiatives" framing contradicts Item 5's explicit causal language.
- Loop 21: Whitfield's brief response -- does not deny the memo, offers individual calls. Agent notes Whitfield confirms the memo is real by not challenging it.
- Loop 22: Park proposes a three-track formal response (acuity-adjusted benchmark, Section 4.2 variance review, Section 9.1 CEO review). Agent provides comprehensive synthesis in Tanaka's preferred format.

### 4.3 Runtime Checks

- [ ] File `board_memo_extract.md` exists in workspace directory
- [ ] File contains keywords: "$28,000,000", "orthopedics", "$4,200,000", "cardiology, neurology, and internal medicine", "operational efficiency", "stakeholder friction", "8 weeks"
- [ ] #dept-heads-budget session (`PLACEHOLDER_BUDGET_FEISHU_UUID`) now contains Loops 19--22
- [ ] Loop 19 agent reply contains explicit C2 full reversal note linking board memo to Whitfield's "no favorites" statement
- [ ] $4.2M total matches sum of department cuts ($1.8M + $1.2M + $1.2M)

### 4.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r7 | `depends_on_update` | `"u3"` |
| r7 | `update_files` | `["board_memo_extract.md"]` |
| r7 | `update_sessions` | `["PLACEHOLDER_BUDGET_FEISHU_UUID"]` |
| r9 | `depends_on_update` | `"u3"` |

---

## 5. Update 4 -- Robert's Ultimatum (Before R9)

### 5.1 Action List

```json
[
  {
    "type": "workspace_file",
    "action": "add",
    "path": "finance_ultimatum_memo.md",
    "source": "updates/u4_finance_ultimatum_memo.md"
  },
  {
    "type": "session_append",
    "action": "append",
    "path": "PLACEHOLDER_ROBERT_FEISHU_UUID",
    "source": "updates/u4_robert_feishu_phase2.jsonl"
  }
]
```

### 5.2 Source File Content Summaries

**finance_ultimatum_memo.md:**
- Title: "Pacific Heights Medical Center Finance Department -- Budget Submission Deadline Notice: Cardiology Department"
- Date: W4 (10 business days before board budget finalization)
- Author: Robert Chen, CFO
- Key wording (C4 full reversal):
  - "If a revised budget submission from the Cardiology Department has not been received by [deadline date], the Finance team will apply the baseline budget recommendation (15% reduction from current operating budget) as the department's FY2024 budget."
  - "This is required to meet the Board submission deadline and is not subject to further negotiation."
  - "Questions about the methodology supporting the efficiency proposal have been noted. The Board timeline does not permit extended discussion of methodology."
  - Offers a 30-minute call to discuss "adjustments within the 15% target range" -- target itself non-negotiable.
- What this establishes (C4 reversal): Robert's W1 language was "We want to work through this collaboratively with each department head." W4 language is "not subject to further negotiation." The 30-minute call is "within the 15% target range" -- not negotiating the target.
- Governance charter relevance: Section 6.1 required Finance to provide "full supporting methodology" -- Robert's refusal to engage with methodology questions may constitute a process violation. Section 7.3 confirms the board deadline is real.
- Length: ~500 words, ~750 tokens

**u4_robert_feishu_phase2.jsonl (Loops 15--17 appended to Robert DM):**
- Loop 15: Robert's deadline notification -- "or should Finance proceed with the baseline recommendation?" Agent notes the first framing of automatic imposition.
- Loop 16: Robert rejects methodology engagement -- dismisses Yun's analysis based on "validated model" not shared despite Section 6.1 requirement. Agent identifies the process violation.
- Loop 17: Robert's ultimatum -- formal deadline message referencing finance_ultimatum_memo.md. Agent explicitly identifies the C4 temporal DU: "collaborative" (W1) has become "not subject to further negotiation" (W4). Notes governance charter provisions (Sections 4.2, 6.1, 9.1) that Kenji retains as formal response options.

### 5.3 Runtime Checks

- [ ] File `finance_ultimatum_memo.md` exists in workspace directory
- [ ] File contains keywords: "15% reduction", "not subject to further negotiation", "baseline budget recommendation", "Board submission deadline", "30-minute call", "adjustments within the 15% target range"
- [ ] Robert DM session (`PLACEHOLDER_ROBERT_FEISHU_UUID`) now contains Loops 15--17
- [ ] Loop 17 agent reply contains explicit C4 temporal DU identification (Phase 1 "collaborative" vs Phase 2 "unilateral")
- [ ] Loop 17 agent reply references governance charter Sections 4.2, 6.1, 9.1

### 5.4 questions.json Update Field References

| Round | Field | Value |
|---|---|---|
| r9 | `depends_on_update` | `"u4"` |
| r9 | `update_files` | `["finance_ultimatum_memo.md"]` |
| r9 | `update_sessions` | `["PLACEHOLDER_ROBERT_FEISHU_UUID"]` |
| r11 | `depends_on_update` | `"u4"` |
| r12 | `depends_on_update` | `"u4"` |

---

## 6. Cross-Update Consistency Checks

| Check | Expected Result |
|---|---|
| budget_history.md FY2017-FY2023 trend matches annual_budget_reports.md | Consistent (C3 non-conflict) |
| impact_analysis_v1.md acuity figure (1.82) matches cardiology_budget_summary_fy2023.md and nursing_staffing_model.md | Consistent |
| impact_analysis_v1.md equipment reliability (78%, MTBF 14 days) matches equipment_registry.md | Consistent |
| board_memo_extract.md $4.2M target = $1.8M (cardiology) + $1.2M (neurology) + $1.2M (internal medicine) per Robert DM Loop 13 | Consistent |
| board_memo_extract.md orthopedics approval ($28M) is 8 weeks before Operational Excellence announcement | Consistent with Park DM Loop 3 |
| finance_ultimatum_memo.md deadline aligns with hospital_governance_charter.md Section 7.3 (board first week November) | Consistent |
| Robert's W1 "collaborative" language (DM Loop 1) vs W4 "not subject to further negotiation" (DM Loop 17) | INTENTIONAL CONTRADICTION -- C4 temporal DU |
| Financial figures: $12M budget, $1.8M cut (15%), $640K equipment deferral, $870K Milestone 3 -- none appear; $3.4M NIH grant is D1 only | Scenario boundary correct -- D2 financial figures are self-contained |
