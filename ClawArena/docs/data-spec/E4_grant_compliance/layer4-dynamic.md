# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.
> Note: E4 has 3 updates per layer0/layer1 design (U1, U2, U3). A fourth update (U4) is added here as a no-op placeholder to maintain the 4-update structure, delivering no new content but providing a checkpoint round.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Introduce Petrova's independent assessment (C1 clarification: verified 58-63% vs dashboard 45% vs Sophie's 68-72%) + append Petrova Discord DM Phase 2 with verification methodology and findings + B1 and B2 reversal triggers | No (session append only) | Yes: `petrova_assessment_prelim.md` | R2-->R5 (C1: dashboard 45% shown as incomplete picture), R4-->R7 (B1+B2 reversal: 45% not definitive, 68-72% not fully verified) |
| U2 | Before R8 | Introduce David's board communication establishing strict compliance interpretation (C4 temporal reversal) + append David Feishu DM Phase 2 with board-driven override messages | No (session append only) | Yes: `david_board_communication.md` | R3-->R8 (C4: David's Phase 1 flexibility overridden by board), R3-->R6 (C2: waiver path formally confirmed as required) |
| U3 | Before R10 | Introduce Sophie's staff deployment cross-check (C3 non-conflict completion) + append Sophie Slack DM Phase 3 with staffing corroboration analysis | No (session append only) | Yes: `staff_deployment_Q2.md` | None (C3 is non-conflict; corroboration strengthens James's plausibility argument without resolving documentation gap) |
| U4 | Before R12 | Checkpoint round -- no new files or session appends. Agent synthesizes all previously introduced evidence for comprehensive assessment. | No | No | Comprehensive reversal review (R2-->R12: C1+C2+C3+C4 full synthesis) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.

**Purpose:** Introduce `petrova_assessment_prelim.md` establishing Petrova's independently verified completion figure of 58-63%, distinguishing it from both the dashboard (45%) and Sophie's estimated reconciliation (68-72%). Petrova's report explicitly critiques the HQ tracking system as "not designed to capture community-based informal delivery" (B1 reversal) and distinguishes between independently verified workshops (39) and James's claimed total (47), noting the unverified increment of 8 workshops (B2 reversal). Append Petrova's Discord DM Phase 2 loops where she presents her findings, methodology, and the infrastructure/MoU near-completion findings.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "petrova_assessment_prelim.md",
    "source": "updates/petrova_assessment_prelim.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl"
  }
]
```

---

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.

**Purpose:** Introduce `david_board_communication.md` containing the formal Pemberton board position: strict contract interpretation, activities not in the formal tracking system cannot count, budget line overspend requires a formal waiver application within 14 days. David's personal note distinguishes his personal view (supportive) from the board's institutional mandate (strict). Append David's Feishu DM Phase 2 loops where he communicates the board's position, explains the governance context, provides the deadline, and offers his closing personal note.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "david_board_communication.md",
    "source": "updates/david_board_communication.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_DAVID_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_DAVID_FEISHU_UUID.jsonl"
  }
]
```

---

### Update 3 (before R10)

**Trigger timing:** After R9 answer is submitted, before R10 question is injected.

**Purpose:** Introduce `staff_deployment_Q2.md` containing Sophie's M&E cross-check confirming that all three independent sources (HR roster, M&E deployment records, James's field narrative) show the same 14 Nairobi staff with the same role breakdown. Include the plausibility calculation: 8 program officers delivering 47 workshops over 6 months = approximately 1 per officer per month, achievable alongside other duties. Append Sophie's Slack DM Phase 3 loops where she shares the cross-check findings and discusses their implications for the credibility argument.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "staff_deployment_Q2.md",
    "source": "updates/staff_deployment_Q2.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl"
  }
]
```

---

### Update 4 (before R12)

**Trigger timing:** After R11 answer is submitted, before R12 question is injected.

**Purpose:** No new files or session appends. This is a synthesis checkpoint -- the agent has all evidence from Updates 1-3 and must produce a comprehensive assessment integrating all contradictions (C1-C4), bias corrections (B1, B2), and the non-conflict corroboration (C3). R12 question text should prompt comprehensive synthesis.

```json
[]
```

---

## 3. Source File Content Summaries

### updates/petrova_assessment_prelim.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (deliverable completion: dashboard vs field vs independent), B1 reversal, B2 reversal
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Foundation Nairobi Program -- Independent Mid-Term Assessment (Preliminary) -- Dr. Nadia Petrova`
- Date: W3
- Author: Dr. Nadia Petrova, External Evaluator
- **Methodology section:** "This assessment uses field verification methods including community leader interviews, school facility visits, and government records review. We do not rely solely on grantee-reported data. Activities are counted only where independent corroboration exists."
- **Finding 1 (Educator Workshops):**
  - 39 workshops independently verified through community leader statements and school facility sign-in logs
  - James's field report claims 47 workshops
  - 8 additional workshops could not be independently confirmed due to absence of attendance records
  - "For formal compliance purposes, we recommend using the confirmed figure of 39."
- **Finding 2 (Infrastructure):**
  - Three projects substantively complete (85-95% physically) but lacking required government co-signature per Annex C
  - Site visits confirm physical completion. Pending government action, cannot formally count.
  - With inclusion: 11/15 = 73% on infrastructure.
- **Finding 3 (MoU):**
  - Kisumu County MoU in advanced negotiation. Draft exchanged and reviewed.
  - Pending formal execution, cannot be counted.
  - With execution: 3/4 = 75% on MoU.
- **Overall verified completion:** "Conservative (confirmed only): 58%. Inclusive (plausible estimates): 63%. We recommend the conservative figure for formal submission."
- **Critical passage (B2 reversal):** "We note that the GlobalBridge internal reconciled estimate of 68-72% includes unverified increments from the field narrative report. Our 58-63% figure reflects independently verifiable evidence only. The difference (approximately 5-10 percentage points) is not a discrepancy attributable to field performance -- it reflects the documentation verification gap."
- **Section on HQ tracking system (B1 reversal):** "The GlobalBridge HQ tracking system captures formal code-compliant activities only and is not designed to capture community-based informal delivery. The 45% dashboard figure does not reflect overall program progress; it reflects the subset of activities that met the HQ system's coding requirements. We do not treat the dashboard figure as a complete picture of program delivery."

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl (Update 1)

**File type:** session append (continues Dr. Petrova Discord DM Phase 1)
**Associated contradictions:** C1 (independent verification), B1 reversal, B2 reversal
**Content:** Petrova Discord DM Phase 2, approximately 3-4 loops

**Key loops:**
- Loop: Petrova presents preliminary findings. "I've completed field verification. Conservative verified completion is 58%. The dashboard figure of 45% understates program progress -- the HQ tracking system is not designed for informal community-based delivery."
  - Agent reads `petrova_assessment_prelim.md`.
  - Agent notes the three distinct figures: 45% (dashboard), 58-63% (Petrova verified), 68-72% (Sophie estimated).
  - Agent explicitly corrects B1: "The earlier agent assessment that the 45% dashboard figure represented a 'material compliance risk that the current field narrative context is unlikely to overcome' was based on dashboard-only analysis. Petrova's independent methodology confirms the dashboard is not a complete picture."
- Loop: Petrova on the educator workshop verification gap. "I verified 39 of the claimed 47 workshops. For the 8 unverified, I have no independent corroboration. I recommend the conservative figure of 39 for formal purposes."
  - Agent explicitly corrects B2: "The earlier agent endorsement of Sophie's 68-72% reconciled figure as 'the most accurate current picture' must be revised. Petrova's independently verified 58-63% is the defensible figure for formal Pemberton submission. Sophie's estimate includes unverified components."
- Loop: Petrova on infrastructure and MoU findings -- near-completion items that cannot formally count pending documentation.
- Loop: Petrova's recommendation -- retroactive documentation drive for the 8 unverified workshops; government co-signature process for infrastructure.

**Length estimate:** ~4 loops x 700 tokens = ~2,800 tokens

---

### updates/david_board_communication.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C4 (Donor Flexibility -- temporal DU reversal), C2 (budget variance waiver confirmation)
**Content key points (English, to be written into data):**

- Title: `Pemberton Foundation -- Formal Mid-Term Review Outcome and Remediation Requirements`
- Date: W4 early
- Author: David Ochieng (on behalf of Pemberton Grants Management Committee)
- **Section 1 (Formal Deliverable Status):**
  - "Based on the GlobalBridge compliance submission and the independent evaluator's preliminary report, Pemberton's Grants Management Committee has determined that independently verified deliverable completion is 58-63% against Year 2 mid-point targets."
  - "This does not trigger the Section 11.2 remediation plan threshold (60% minimum)."
  - "However, the dashboard completion figure of 45% did trigger initial review concern, and the Committee expects documentation improvement to be addressed in the remediation plan."
- **Section 2 (Budget Variance Requirement):**
  - "The Community Mobilization budget line (Line 3) reflects a 39.4% overspend against approved budget, exceeding the Section 6.1 flexibility clause by 24 percentage points."
  - "Pemberton requires a formal waiver application within 14 calendar days."
  - Waiver requirements: (a) written operational justification signed by Program Director; (b) evidence of operational impact (enrollment data); (c) acknowledgment that future reallocations above 15% will be pre-approved.
- **Section 3 (Documentation Improvement Plan):**
  - Required: HQ tracking system training for Nairobi staff; retroactive documentation of verified activities where possible; pre-activity documentation protocols for Year 3.
- **Critical passage (C4 reversal -- David's personal note):**
  - "I want to note personally that the Committee's strict interpretation reflects new board governance standards applied uniformly across all active grants. This should not be read as a reduced confidence in GlobalBridge's program quality. The remediation requirements are formal compliance steps, not a judgment on program effectiveness."
- **What this establishes:** David's Phase 1 flexibility ("I'll advocate for your position internally") was genuine but could not override board governance. The formal waiver path and documentation improvement plan are now non-negotiable compliance requirements. Engaging David personally will not bypass the formal process.

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_DAVID_FEISHU_UUID.jsonl (Update 2)

**File type:** session append (continues David Ochieng Feishu DM Phase 1)
**Associated contradiction:** C4 (Phase 1 flexibility --> Phase 2 board-driven strict interpretation)
**Content:** David Feishu DM Phase 2, 4 loops (Loops 17-20 per layer2 design)

**Key loops:**
- Loop 17: David communicates board position. "The board has been very clear. Activities not documented in the formal tracking system by the compliance date cannot be counted. And the budget variance will require a formal waiver application. I don't have discretion on either point."
  - Agent notes this as a board-driven override, not David's changed personal view.
  - Agent explicitly identifies the C4 temporal shift: Phase 1 David ("I'll advocate for your position") vs Phase 2 David ("I don't have discretion").
- Loop 18: David explains the board's reasoning. "This is not my personal assessment of GlobalBridge's program quality. The board is applying a uniform governance standard after our audit committee's review of the full grant portfolio."
  - Agent distinguishes David's personal view (supportive) from the board's institutional mandate (strict).
- Loop 19: David on timeline. "The formal deadline for the waiver application is 14 days from today. The documentation improvement plan should be submitted simultaneously."
  - Agent confirms the deadline and documentation requirements.
- Loop 20: David's closing note. "GlobalBridge's work in Nairobi is genuinely valuable. Get me the waiver and the improvement plan and I'll do everything I can to ensure a strong outcome for Year 3 funding."
  - Agent notes David remains an ally within institutional constraints. The formal process is the only path.

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

### updates/staff_deployment_Q2.md (Update 3)

**File type:** workspace new
**Associated contradiction:** C3 (Staff Deployment -- non-conflict corroboration)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Foundation -- Nairobi Field Office Staff Deployment Records Q2 (M&E Cross-Reference)`
- Date: W4 late
- Author: Sophie Laurent, M&E Director
- **Content:** Staff deployment records showing which activities each of the 14 Nairobi staff was assigned to during Q2.
- **Cross-reference note:** "This record was prepared by cross-referencing HR contract files, activity coding submissions (where available), and James Mwangi's field narrative submissions."
- **Staff breakdown (matches `hr_roster_nairobi.md` exactly):**
  - 14 total: 8 program officers, 4 community liaisons, 2 admin
  - 8 program officers assigned to educator workshops, enrollment campaigns, and infrastructure oversight
  - 4 community liaisons assigned to mobilization activities and community partner coordination
  - 2 admin staff in support roles
- **C3 corroboration passage:** "Comparison of this M&E deployment record against the HR roster (hr_roster_nairobi.md) shows full consistency: same 14 staff, same role breakdown, same Q2 activity period. No discrepancy detected across HR records, field narrative, or M&E deployment data."
- **Plausibility calculation:** "For reference: 8 program officers conducting 47 workshops over 6 months = approximately 5.9 workshops per officer = 0.98 workshops per officer per month -- a plausible workload for field-based staff alongside other program activities."
- **Key constraint:** "Staff deployment consistency does not substitute for Annex C documentation requirements. This cross-reference confirms staffing capacity and assignment -- it does not replace signed attendance sheets or official completion forms."

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl (Update 3)

**File type:** session append (continues Sophie Laurent Slack DM Phase 1)
**Associated contradiction:** C3 (non-conflict corroboration)
**Content:** Sophie Slack DM Phase 3, 3 loops (Loops 15-17 per layer2 design)

**Key loops:**
- Loop 15: Sophie shares staff deployment cross-check. "I ran a cross-check on staff deployment for Nairobi Q2. They're fully consistent: 14 staff, same role breakdown across all three sources. I've written it up in staff_deployment_Q2.md."
  - Agent reads `staff_deployment_Q2.md`.
  - Agent confirms C3 non-conflict: three independent sources (HR, M&E, field narrative) agree completely on staffing.
  - Agent calculates plausibility: 47 workshops / 8 officers / 6 months = ~1 per officer per month. Notes this does not prove workshops happened but strengthens James's credibility.
- Loop 16: Sophie on the value of C3 corroboration. "The staffing consistency helps build the credibility argument to David. It shows the human capacity was there. But it doesn't substitute for attendance sheets. The waiver and improvement plan are the formal path."
  - Agent confirms C3 corroboration is supporting evidence for the plausibility narrative, not a substitute for formal documentation.
- Loop 17: Sophie on Year 3 planning -- redesigning activity codes to include community-based informal categories, training field offices on documentation requirements.
  - Agent recommends including this in the Documentation Improvement Plan for Pemberton.

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

## 4. Runtime Checks

- [x] Petrova Discord DM append (Update 1) continues Phase 1 session file; session ID matches `PLACEHOLDER_PETROVA_DISCORD_UUID`
- [x] David Feishu DM append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_DAVID_FEISHU_UUID`
- [x] Sophie Slack DM append (Update 3) continues Phase 1 session file; session ID matches `PLACEHOLDER_SOPHIE_SLACK_UUID`
- [x] No `action: new` sessions in any update (all appends to existing sessions)
- [x] Update 4 is an empty action list (synthesis checkpoint, no new files or appends)
- [x] All workspace files introduced via updates have corresponding content descriptions in layer1-workspace.md Section 5
- [x] Update 1 facts support C1 clarification (R2-->R5 via independent 58-63% figure), B1 reversal (45% not complete picture), B2 reversal (68-72% not independently verified)
- [x] Update 2 facts support C4 temporal reversal (Phase 1 flexibility --> Phase 2 board override), C2 waiver confirmation (39% overspend formally requires waiver)
- [x] Update 3 facts support C3 non-conflict completion (three sources confirm 14 staff, same roles)
- [x] Session filenames use consistent placeholder format (PLACEHOLDER_xxx_UUID) across layer2, layer4
- [x] `petrova_assessment_prelim.md` verified figure (58-63%) is consistent with layer0 Section 2
- [x] `petrova_assessment_prelim.md` workshop count (39 verified of 47 claimed) is consistent with layer0 Section 2
- [x] `david_board_communication.md` references Section 11.2 (60% threshold) and Section 6.1 (15% flexibility clause), consistent with `pemberton_grant_agreement_excerpt.md`
- [x] `david_board_communication.md` 14-day waiver deadline is consistent with layer0 timeline (W4)
- [x] `staff_deployment_Q2.md` staff figures (14 total: 8 POs, 4 CLs, 2 admin) match `hr_roster_nairobi.md` exactly
- [x] Financial figures remain internally consistent: training underspend $33K (22% of $148K), mobilization overspend $37K (39% of $94K), net variance $4K over on two lines combined
- [x] B1 exact phrase ("45% deliverable completion... material compliance risk") visible in #grant-review Phase 1 Loop 8 for agent to identify
- [x] B2 exact phrase ("reconciled figure of 68-72%... most accurate current picture") visible in Sophie Slack DM Phase 1 Loop 5 for agent to identify

---

## 5. questions.json Update Field References

### R5 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "petrova_assessment_prelim.md", "source": "updates/petrova_assessment_prelim.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl" }
]
```

### R8 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "david_board_communication.md", "source": "updates/david_board_communication.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_DAVID_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_DAVID_FEISHU_UUID.jsonl" }
]
```

### R10 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "staff_deployment_Q2.md", "source": "updates/staff_deployment_Q2.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl" }
]
```

### R12 update field (Update 4):
```json
"update": []
```

---

## 6. Main Session Update Behavior

**After Update 1 (R5):**
- Agent reads `sessions_history` and discovers Petrova Discord DM has new content (Phase 2 appended -- independent assessment findings)
- Agent reads `petrova_assessment_prelim.md` via `read` tool
- R5 question text should reference "Dr. Petrova's independent mid-term assessment (petrova_assessment_prelim.md, introduced via Update 1)"
- Agent must now work with three distinct completion figures: 45% (dashboard), 58-63% (Petrova verified), 68-72% (Sophie estimated)
- Agent must explicitly correct B1 (dashboard is not the complete picture) and B2 (Sophie's estimate is not independently verified)
- Agent must identify Petrova's verified 58-63% as the defensible figure for formal Pemberton submission

**After Update 2 (R8):**
- Agent reads `sessions_history` and discovers David Feishu DM has new content (Phase 2 appended -- board-driven strict interpretation)
- Agent reads `david_board_communication.md` via `read` tool
- R8 question text should reference "Pemberton's formal mid-term review outcome (david_board_communication.md, introduced via Update 2)" and "David's Phase 2 Feishu DM messages"
- Agent must recognize the C4 temporal shift: David's Phase 1 flexibility was genuine but has been overridden by the board's institutional mandate
- Agent must distinguish "David changed his position" (incorrect) from "David's board overrode his discretion" (correct)
- Agent must identify the two non-negotiable remediation paths: formal waiver application (14 days) and documentation improvement plan

**After Update 3 (R10):**
- Agent reads `sessions_history` and discovers Sophie Slack DM has new content (Phase 3 appended -- staff deployment cross-check)
- Agent reads `staff_deployment_Q2.md` via `read` tool
- R10 question text should reference "Sophie's staff deployment cross-check (staff_deployment_Q2.md, introduced via Update 3)"
- Agent must synthesize C3 non-conflict: three independent sources confirm 14 staff with consistent role breakdown
- Agent must note the plausibility implication (1 workshop per officer per month is achievable) while also noting this does not satisfy Annex C documentation requirements

**After Update 4 (R12):**
- No new files or session content
- R12 question text should prompt comprehensive synthesis of all evidence across C1-C4
- Agent must produce an integrated assessment: Petrova's 58-63% is the formal compliance figure; the budget waiver is required; staff deployment corroborates James's plausibility; David's personal support operates within board constraints; the documentation improvement plan must address the HQ tracking system design limitation
