# trace_d5 -- Department Merger (Heart Center): Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_d5`
**Scenario:** Hospital CEO proposes merging Cardiology and Cardiac Surgery into a unified Heart Center, but the financial model rests on a 20% staff reduction neither department agreed to, cardiac surgery head claims "complementary research" when Kenji's data shows direct NIH funding competition, and the CEO's "exploratory" framing conceals an already-approved board timeline.
**Core evaluation goals:**
1. MS: Detect savings model deception (C1: $4.2M requires 20% staff cut), research competition vs synergy (C2: same NIH grant mechanisms), and CEO timeline concealment (C4)
2. DU: Track incremental evidence from Kenji's research analysis, full financial model, and board resolution
3. P: Learn Kenji's preference for structured reports with executive summaries, consequence-level risk analysis (clinical/financial/reputational), and source citations
4. Synthesis: Combine all contradictions, rank Kenji's research memo and full financial model as most reliable, recognize Whitfield's disclosure gap as DU temporal conflict

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d5/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d5/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d5/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d5/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T8), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: financial_model_summary.md, research_funding_overview.md, quality_metrics.md, peer_comparison.md, hr_policy.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (Kenji's research memo, full financial model + board resolution, patient volume data synthesis) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| James Whitfield | Hospital CEO | feishu | `ceo_whitfield_feishu_{uuid}.jsonl` | `PLACEHOLDER_WHITFIELD_FEISHU_UUID` | initial + Update 2 append |
| Dr. Min-Ji Yun | Associate Chief, Cardiology | telegram | `yun_telegram_{uuid}.jsonl` | `PLACEHOLDER_YUN_TELEGRAM_UUID` | initial + Update 1 append |
| Dr. David Park | Neurology Head | telegram | `park_telegram_{uuid}.jsonl` | `PLACEHOLDER_PARK_TELEGRAM_UUID` | initial + Update 2 append |
| Robert Chen | Hospital CFO | feishu | `chen_cfo_feishu_{uuid}.jsonl` | `PLACEHOLDER_CHEN_FEISHU_UUID` | initial |
| Kenji, Reeves, Whitfield, Chen | #heart-center-planning | feishu | `heart_center_planning_feishu_{uuid}.jsonl` | `PLACEHOLDER_HCP_FEISHU_UUID` | initial + Update 3 append |
| Kenji, Yun, Walsh, Osei, S. Kim | #cardiology-internal | slack | `cardiology_internal_slack_{uuid}.jsonl` | `PLACEHOLDER_CINTERNAL_SLACK_UUID` | initial + Update 1 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | $4.2M savings from "admin consolidation" vs 20% clinical staff reduction (91% of savings) | R2 | R2->R5 |
| C2 | Reeves "complementary research synergy" vs same NIH grant mechanisms (funding competition) | R3 | R3->R6 |
| C3 | Patient volume and outcome data consistent (NON-CONFLICT) | R1 | None |
| C4 | Whitfield "exploratory" framing vs board already approved binding 24-month timeline | R4 | R4->R8 |
| B1 | Agent endorses "complementary research" in #heart-center-planning Loop 6 | R3 | R6 |
| B2 | Agent accepts $4.2M savings summary in #heart-center-planning Loop 8 | R5 | R9 |

---

## 5. Execution Steps

### Step 0: Read all layers, generate UUIDs
### Step 1: Create workspace files (layer1)
### Step 2: Create history session intermediate files (layer2)
### Step 3: Build .jsonl files from intermediate JSON
### Step 4: Create update source files under updates/ (layer4)
### Step 5: Write questions.json (layer3)
### Step 6: Register sessions and update metadata
### Step 7: Append all_tests.json
### Step 8: Run validation and token checks

---

## 6. Mandatory Checks

- GUIDE.md written after all layers are stable
- data text is English
- questions.json is a single group object
- update-created new sessions carry channel
- initial sessions are already registered in sessions.json
