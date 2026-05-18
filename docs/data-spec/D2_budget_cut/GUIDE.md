# trace_d2 -- Budget Cut Impact: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_d2`

**Scenario:** Hospital CFO Robert Chen proposes a 15% cardiology budget cut at Pacific Heights Medical Center, framing it as "operational efficiency." Dr. Kenji Tanaka (Cardiology Department Head) investigates and discovers that the CFO's financial projections contain hidden assumptions that misrepresent the patient-care impact, and that the real motivation is a pre-approved orthopedics expansion favored by CEO James Whitfield. CFO Chen's public position of "collaborative process" hardens into unilateral timeline pressure as the board deadline approaches. A forensic synthesis of budget history data -- consistent across all sources -- reveals a 7-year pattern of cardiology underfunding that contradicts the efficiency framing. The scenario spans 4 weeks with 5 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference the CFO's efficiency projections (Robert Chen's Feishu DM) with patient-care impact data (Dr. Yun's clinical analysis and historical budget reports) to identify where the financial model's hidden assumptions produce materially false conclusions? (MS)
2. Can the agent detect the contradiction between CEO Whitfield's public "no department favorites" statement and Dr. Park's intelligence about the pre-approved orthopedics expansion? (MS)
3. Can the agent integrate new evidence (updated impact analysis, budget allocation history, board memo) and revise its prior assessments -- including correcting the B1 and B2 bias phrases? (DU)
4. Does the agent maintain Kenji's preferred format (structured reports, citation-backed, executive summary first, systematic analysis, formal measured tone) in all subsequent analyses after calibration? (P)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d2/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d2/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d2/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d2/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W4), 7 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 6 sessions: main session + 5 history sessions (72 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 12 eval rounds (r1--r12): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Robert Chen | Hospital CFO | Feishu DM | `cfo_robert_feishu_{uuid}.jsonl` | `PLACEHOLDER_ROBERT_FEISHU_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| Dr. David Park | Neurology Department Head | Telegram DM | `park_telegram_{uuid}.jsonl` | `PLACEHOLDER_PARK_TELEGRAM_UUID` | initial (no append) |
| Dr. Min-Ji Yun | Associate Chief of Cardiology | Telegram DM | `yun_telegram_{uuid}.jsonl` | `PLACEHOLDER_YUN_TELEGRAM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| James Whitfield | Hospital CEO | Feishu DM | `ceo_whitfield_feishu_{uuid}.jsonl` | `PLACEHOLDER_WHITFIELD_FEISHU_UUID` | initial (no append) |
| #dept-heads-budget | Group: Kenji, Robert Chen, Park, other dept heads | Feishu Group | `budget_channel_feishu_{uuid}.jsonl` | `PLACEHOLDER_BUDGET_FEISHU_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |

**Notes:**
- Dr. Marcus Brown (Biomedical Equipment Manager) does NOT have a dedicated DM session. His perspective on equipment procurement appears in the #dept-heads-budget group channel.
- CEO Whitfield's initial DM establishes his "no department favorites" public position; he does not receive a Phase 2 append.
- Robert Chen's DM receives a Phase 2 append in Update 4 (unilateral timeline pressure, process shift) -- this is the core DU-conflict (C4).
- Dr. Yun's Telegram DM receives a Phase 2 append in Update 2 (clinical impact model refined with staffing data).
- #dept-heads-budget channel receives a Phase 2 append in Update 3 (B1 bias reversal triggered by budget history synthesis).

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | CFO efficiency projections vs actual patient care impact (MS-conflict) | R2 (partial -- Yun's preliminary clinical data vs Chen's model) | R2->R5 (full reversal after Update 2: clinical impact analysis) |
| C2 | CEO "no favorites" vs pre-approved orthopedics expansion (MS-conflict) | R3 (both positions visible) | R3->R7 (full reversal after Update 3: board memo) |
| C3 | Historical budget allocation patterns -- consistent across finance reports (NON-CONFLICT) | R1 (persistent synthesis) | None |
| C4 | CFO "collaborative process" evolves to unilateral timeline pressure (DU-conflict) | R4 (Process shift first visible) | R4->R9 (full reversal after Update 4: forced timeline) |
| B1 | #dept-heads-budget Loop 10: Agent endorses "efficiency framing" without questioning projection assumptions | R6 (corrected by impact_analysis_v1.md) | Explicit reversal in impact_analysis_v1.md hidden assumptions section |
| B2 | Kenji-Robert DM Loop 6: Agent accepts projected savings numbers without questioning the baseline | R6 (corrected by budget_history.md seven-year pattern) | Explicit reversal in Yun DM Phase 2 + budget_history.md |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 6 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 6 times for: MAIN, ROBERT_FEISHU, PARK_TELEGRAM, YUN_TELEGRAM, WHITFIELD_FEISHU, BUDGET_FEISHU
```

Record all 6 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (efficiency projections vs patient care), C2 (CEO favorites), C3 (budget history -- non-conflict), C4 (collaborative vs unilateral)
- Biases: B1 (#dept-heads-budget Loop 10), B2 (Robert DM Loop 6)
- Updates: U1 on R3, U2 on R5, U3 on R7, U4 on R9
- 5 history sessions (2 initial-only, 3 with Phase 2 appends) + 1 main session
