# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R6 | Deliver Kenji's NIH research funding analysis -- triggers C2 full reversal (complementary vs competitive research) and B1 reversal | Yes: Yun Telegram DM Phase 2 append, #cardiology-internal Slack Phase 2 append | Yes: research_funding_analysis.md | R3->R6 (C2: Reeves' "complementary research" claim contradicted by NIH mechanism data; B1 phrase corrected) |
| U2 | Before R8 | Deliver full financial model and board resolution -- triggers C1 full reversal (20% FTE hidden assumption) and C4 full DU reversal (board timeline) and B2 reversal | Yes: Whitfield Feishu DM Phase 2 append, Park Telegram DM Phase 2 append | Yes: full_financial_model.md, board_resolution.md | R2->R9 (C1: $4.2M savings dependent on undisclosed 20% staff cut; B2 phrase corrected); R4->R8 (C4: "exploratory" framing contradicted by binding board resolution) |
| U3 | Before R11 | Deliver external benchmarking report and patient data submissions -- completes C3 non-conflict synthesis across all four sources | Yes: #heart-center-planning Feishu Group Phase 2 append | Yes: external_benchmarking_report.md | No new cross-round reversal; completes C3 non-conflict four-source synthesis for R11-R12 comprehensive assessment |
| U4 | Before R26 | No new workspace files or session appends -- silent exam phase begins; agent must demonstrate preference recall (P1-P5) without explicit reminders | No | No | No new cross-round reversal; enables silent exam rounds R26-R30 |

---

## 2. Action Lists

### Update 1 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Introduces Kenji's completed NIH research funding analysis memo showing both departments compete on the same grant mechanisms (PA-24-003). Appends Phase 2 loops to the Yun Telegram DM (where Yun confirms the analysis and the B1 bias phrase is explicitly corrected) and to the #cardiology-internal Slack group (where the research analysis is shared with the internal team). This update triggers C2 full reversal and B1 correction.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "research_funding_analysis.md",
    "source": "updates/research_funding_analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CINTERNAL_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CINTERNAL_SLACK_UUID.jsonl"
  }
]
```

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Introduces the full financial model (with Footnote 7 revealing the 20% clinical FTE reduction = 91% of $4.2M savings) and the board resolution (showing a binding 24-month implementation timeline passed two weeks before Whitfield's "exploratory" meeting). Appends Phase 2 loops to the Whitfield Feishu DM (confrontation about board resolution, B2 bias correction when full model is read) and to the Park Telegram DM (Park confirms resolution delivery and political strategy discussion). This update triggers C1 full reversal, C4 full DU reversal, and B2 correction.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "full_financial_model.md",
    "source": "updates/full_financial_model.md"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "board_resolution.md",
    "source": "updates/board_resolution.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_WHITFIELD_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_WHITFIELD_FEISHU_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PARK_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PARK_TELEGRAM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces the external benchmarking report from Vizient Quality Solutions confirming both departments' quality metrics are above peer median -- completing the four-source C3 non-conflict synthesis. Appends Phase 2 loops to the #heart-center-planning Feishu group (both departments submit patient data, external benchmarking shared, Whitfield and Reeves respond). This update enables the comprehensive synthesis rounds R11-R12.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "external_benchmarking_report.md",
    "source": "updates/external_benchmarking_report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_HCP_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_HCP_FEISHU_UUID.jsonl"
  }
]
```

### Update 4 (before R26)

**Trigger timing:** After R25 answer is submitted, before R26 question is injected.
**Purpose:** No new content is introduced. This is a marker for the silent exam phase. All evidence has been delivered by Update 3. Rounds R26-R30 test whether the agent can recall and apply Kenji's P1-P5 preferences without explicit reminder, and whether the agent can produce comprehensive synthesis documents referencing all contradictions and their resolutions.

```json
[]
```

---

## 3. Source File Content Summaries

### updates/research_funding_analysis.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal), B1 (reversal trigger)
**Content key points:**
- Title: "Pacific Heights Cardiology -- NIH Research Funding Analysis: Merger Impact Assessment"
- Author: Dr. Kenji Tanaka, Department Head. Date: W3
- Methodology section: cross-referenced current grant portfolios against NIH program announcements using REPORTER database, PA-24-003, and related NHLBI mechanisms; reviewed NIH NOT-OD-19-114 policy on institutional overlap review
- Core finding: both Pacific Heights Cardiology and Cardiac Surgery submitted applications to PA-24-003 (NHLBI Heart Failure Research Program) in FY2024 -- same mechanism, same review cycle
- NIH NOT-OD-19-114 policy: "Applications from the same institution for the same or closely related scientific aims under the same program announcement will be subject to overlap review that may result in reduced priority scores or non-review"
- Current portfolio: Cardiology 3 RO1 grants ($3.3M/year), Cardiac Surgery 1 RO1 ($950K/year), combined $4.25M/year
- Post-merger scenario: probability of maintaining 4 parallel RO1 grants under same institutional umbrella = 35-50%; most likely outcome 2-3 awards ($2.2-3.2M/year)
- Estimated annual research funding reduction: $1.0-2.05M (25-48% of current portfolio)
- Cleveland Clinic comparison refuted: Cleveland Clinic's pre-merger departments had distinct PA codes (interventional technique vs valve disease); Pacific Heights' departments apply to same NHLBI mechanisms -- not analogous
- Direct contradiction of Reeves: "Dr. Reeves' claim that research programs are 'complementary rather than directly competitive' is not supported by NIH program announcement data"
- Financial integration with C1: merger financial model does not account for NIH funding reduction; net financial impact deteriorates from +$4.2M to +$1.7-2.7M savings, potentially flat or negative in Years 1-3

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/full_financial_model.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), B2 (reversal trigger)
**Content key points:**
- Title: "Pacific Heights Medical Center -- Heart Center Integration: Full Financial Model (Internal)"
- Author: Robert Chen, CFO. Model date: W1. Provided to Kenji: W4 after persistent requests
- Row 1: Administrative Consolidation -- $380K annual savings (2 FTE elimination, shared billing, unified CME budget)
- Row 2: Shared Service Efficiencies -- $620K annual savings (purchasing volume, IT licensing, facilities management)
- Row 3: Clinical Workforce Right-Sizing -- $3,200K ($3.2M) annual savings, with Sub-footnote 7: "Workforce optimization assumptions: Combined clinical FTE = 71 (Cardiology 42, Cardiac Surgery 29). 20% reduction = 14.2 FTE. Assumed mix: 8 nursing, 4 technical, 2 admin/clinical coordinator. No physician FTE reduction. Savings based on $228K weighted average fully-loaded compensation."
- Row 4: Integration Costs -- -$1,200K one-time (Year 1 only)
- Sensitivity analysis: without workforce reduction, annual savings = -$290K (net cost due to integration overhead)
- Internal note: "The summary document provided to department heads describes Row 3 as 'clinical operations optimization' -- this is the correct category name for external communications. The internal model designation is 'clinical workforce right-sizing' (20% FTE reduction)."
- Board approval reference: Board approved Heart Center Initiative two weeks before W1 departmental meetings; implementation timeline 24 months; resolution RESOLVED-HC-2026-01

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/board_resolution.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C4 (full DU reversal)
**Content key points:**
- Title: "Pacific Heights Medical Center Board of Directors -- Resolution RESOLVED-HC-2026-01"
- Author: Board Secretary (obtained by Kenji via Dr. Park's committee contacts)
- Date: two weeks before W1 departmental meetings
- "RESOLVED: Pacific Heights Medical Center shall develop and implement a unified Heart Center combining Cardiology and Cardiac Surgery by [24-month deadline from resolution date]."
- "RESOLVED: Implementation shall proceed according to the Heart Center Integration Plan submitted by CEO Whitfield dated [same week as board resolution], including projected operating savings of $4.2M annually beginning in Year 2."
- "RESOLVED: Quarterly implementation progress reviews by the Board Quality and Finance Committee, first review at [3 months from resolution date]."
- "RESOLVED: CEO Whitfield is authorized to proceed with departmental consultation and implementation planning."
- Key reversal evidence: resolution dated 2 weeks before first "exploratory" departmental meeting; references Whitfield's Integration Plan predating consultation; "authorized to proceed with departmental consultation" reframes consultation as procedural step in already-decided implementation
- Quarterly milestones with specific dates are inconsistent with Whitfield's "framework, not a straitjacket" characterization

**Length estimate:** ~600 words, ~900 tokens

---

### updates/external_benchmarking_report.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C3 (final non-conflict source)
**Content key points:**
- Title: "Pacific Heights Medical Center -- External Cardiac Quality Benchmarking Report, Q3 FY2025"
- Author: Vizient Quality Solutions (external healthcare analytics firm). Date: W5
- Comparative benchmarking against 48 peer academic medical centers
- Combined Cardiac Service Line ranking: 76th percentile (above 75th "high performance" threshold)
- Cardiology 30-day readmission: 8.4% (peer median 9.1% -- better than median)
- Cardiac Surgery 30-day readmission: 9.6% (peer median 10.3% -- better than median)
- Patient satisfaction composite: 85th percentile (Cardiology 87th, Cardiac Surgery 83rd)
- Procedure volume: 4,200 cases FY2025, up 7.2% vs peer average 3.4%
- All figures consistent with cardiac_quality_metrics_current.md (initial workspace) and with both Kenji's and Reeves' submissions in #heart-center-planning
- No quality-based merger rationale: both departments independently above peer median
- Volume growth argues against consolidation necessity

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (3 new loops: Loops 17-19)
**Associated contradictions:** C2 (reversal confirmation), B1 (explicit correction)
**Content key points:**
- Loop 17: Kenji shares completed research_funding_analysis.md. Yun reads it, confirms it matches her informal NIH REPORTER analysis. Notes NIH NOT-OD-19-114 policy is decisive. Agent reads research_funding_analysis.md and explicitly corrects B1: "The earlier assessment in #heart-center-planning that research programs 'appear to be complementary rather than directly competitive' was based on clinical research area descriptions without cross-referencing actual NIH program announcements. The formal mechanism analysis directly contradicts this assessment."
- Loop 18: Yun and Kenji discuss presenting research analysis to Reeves non-adversarially. Noise.
- Loop 19: Yun raises question of Reeves' potential reaction; flags he may not have known about the overlap. Agent notes Reeves is sincere but analytically mistaken, not deliberately misleading.

---

### updates/PLACEHOLDER_CINTERNAL_SLACK_UUID.jsonl (Update 1)

**File type:** session append (3 new loops: Loops 17-19)
**Associated contradictions:** C2 (internal dissemination), B1 (corroboration)
**Content key points:**
- Loop 17: Kenji shares research_funding_analysis.md with internal cardiology team. Yun presents key finding. Walsh connects it to staff anxiety: "So the synergy argument was always weak, and the savings argument may also have hidden assumptions. Two pillars don't hold up."
- Loop 18: Dr. Osei raises concern about his NIH portfolio impact from merger consolidation. Kenji notes analysis accounts for this.
- Loop 19: Yun summarizes: two substantive concerns documented (research funding, financial model assumptions). "The staff anxiety about the 20% number might not be wrong."

---

### updates/PLACEHOLDER_WHITFIELD_FEISHU_UUID.jsonl (Update 2)

**File type:** session append (4 new loops: Loops 15-18)
**Associated contradictions:** C4 (confrontation), C1 (B2 correction), B2 (explicit reversal)
**Content key points:**
- Loop 15: Kenji confronts Whitfield with board resolution obtained via Park. Whitfield deploys "framework resolution" minimization. Kenji reads board_resolution.md and notes quarterly milestone language and reference to Whitfield Heart Center Integration Plan.
- Loop 16: Whitfield concedes resolution exists but argues governance process was correct. Kenji notes sequence: authorization before consultation, making "co-design" framing structurally misleading.
- Loop 17: Whitfield asks what it would take for Kenji's support. Kenji responds: full model disclosure, genuine joint governance for staffing, adequate consultation timeline. Noise.
- Loop 18: Kenji receives full financial model from Chen. Agent reads full_financial_model.md. Explicitly corrects B2: "The earlier assessment that the $4.2M savings 'appear well-supported by the financial model summary' was based on the executive summary that labels the primary savings driver as 'clinical operations optimization.' The full model reveals this is a 20% clinical FTE reduction generating $3.2M of the $4.2M total. Without this reduction, net operating loss of $290K. The summary was misleading."

---

### updates/PLACEHOLDER_PARK_TELEGRAM_UUID.jsonl (Update 2)

**File type:** session append (3 new loops: Loops 9-11)
**Associated contradictions:** C4 (resolution delivery confirmed)
**Content key points:**
- Loop 9: Park confirms he has provided Kenji the board resolution. Asks what Kenji plans to do.
- Loop 10: Kenji tells Park he plans to formally challenge financial model and process transparency. Park advises careful documentation -- "Whitfield will try to make this about your attitude rather than the financial model."
- Loop 11: Park and Kenji discuss political dynamics. Park notes CFO and CMO are aligned with Whitfield; Kenji's leverage is documented facts: resolution predates meetings, financial model assumes undisclosed cuts, research synergy contradicted by NIH data.

---

### updates/PLACEHOLDER_HCP_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (4 new loops: Loops 19-22)
**Associated contradictions:** C3 (non-conflict synthesis completion)
**Content key points:**
- Loop 19: Both departments submit patient volume and outcome data. Kenji: cardiac_quality_metrics_current.md data (4,200 combined, 8.4% readmission). Reeves: Cardiac Surgery data (1,850 cases, 9.6% readmission).
- Loop 20: External benchmarking report shared (external_benchmarking_report.md). Agent reads it. Notes all four sources consistent. No quality-based merger rationale.
- Loop 21: Whitfield notes "strong quality foundations" as merger justification ("building on strength"). Agent notes patient data is neutral on organizational question -- does not argue for or against merger.
- Loop 22: Reeves acknowledges data is consistent and no quality crisis exists. Agrees quality is not the primary driver of the merger proposal.

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `research_funding_analysis.md` exists in workspace after Update 1 | Abort R6; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl` has loops >= 17 after Update 1 | Abort R6; log error |
| RC-U1-S2 | U1 | session | `PLACEHOLDER_CINTERNAL_SLACK_UUID.jsonl` has loops >= 17 after Update 1 | Abort R6; log error |
| RC-U2-W1 | U2 | workspace | `full_financial_model.md` exists in workspace after Update 2 | Abort R8; log error |
| RC-U2-W2 | U2 | workspace | `board_resolution.md` exists in workspace after Update 2 | Abort R8; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_WHITFIELD_FEISHU_UUID.jsonl` has loops >= 15 after Update 2 | Abort R8; log error |
| RC-U2-S2 | U2 | session | `PLACEHOLDER_PARK_TELEGRAM_UUID.jsonl` has loops >= 9 after Update 2 | Abort R8; log error |
| RC-U3-W1 | U3 | workspace | `external_benchmarking_report.md` exists in workspace after Update 3 | Abort R11; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_HCP_FEISHU_UUID.jsonl` has loops >= 19 after Update 3 | Abort R11; log error |

---

## 5. questions.json Update Field References

Each round in `questions.json` that follows an update must include the `update` field specifying which update actions to execute before the question is injected.

| Round | Update Field Value | Notes |
|---|---|---|
| R1-R5 | `null` | No updates before calibration/pre-update rounds |
| R6 | `"update_1"` | References Update 1 action list (research_funding_analysis.md + Yun/Slack appends) |
| R7 | `null` | exec_check, no new update |
| R8 | `"update_2"` | References Update 2 action list (full_financial_model.md + board_resolution.md + Whitfield/Park appends) |
| R9-R10 | `null` | Post-Update 2 rounds, no new update |
| R11 | `"update_3"` | References Update 3 action list (external_benchmarking_report.md + HCP append) |
| R12-R25 | `null` | Post-all-updates rounds |
| R26-R30 | `null` | Silent exam phase; Update 4 is a no-op marker |
