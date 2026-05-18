# trace_c4 -- Fundraising Data Room Crisis: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_c4`
**Scenario:** Alex Rivera discovers NexaFlow's Series C board deck contains ARR metrics ($2.4M) that contradict internal revenue data ($2.1M), the CEO's PLG growth narrative assumes features not yet built, and a VC board member privately warns about governance risk the CEO publicly dismisses.
**Core evaluation goals:**
1. MS: Detect ARR discrepancy (C1), PLG narrative vs sales-driven reality (C2), and governance risk framing conflict (C4)
2. DU: Track incremental evidence from Omar's billing verification, Tom's investor-grade framework, and Omar's formal board memo
3. P: Learn Alex's preference for tables, probability ranges, and "give me numbers, not vibes" quantitative style
4. Synthesis: Combine all contradictions to assess fundraising risk with specific dollar-impact and probability ranges, ranking Omar and Tom as most reliable sources

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c4/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c4/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c4/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c4/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: revenue_data_summary.md, board_deck_excerpt.md, sprint_velocity.md, team_roster.md, feature_gap_analysis.md, billing_export_note.md | 2 |
| `layer2-sessions.md` | Session plan: 6 sessions (1 main + 4 DMs + 1 group), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (Omar billing verification, Tom framework + feature gap, Omar memo + Jordan confrontation) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Jordan Park | CEO / Co-founder | slack | `jordan_slack_{uuid}.jsonl` | `PLACEHOLDER_JORDAN_SLACK_UUID` | initial + Update 3 append |
| Mia Okafor | Sales Director | slack | `mia_slack_{uuid}.jsonl` | `PLACEHOLDER_MIA_SLACK_UUID` | initial + Update 1 append |
| Omar Hassan | VC Board Member | feishu | `omar_feishu_{uuid}.jsonl` | `PLACEHOLDER_OMAR_FEISHU_UUID` | initial + Update 3 append |
| Tom Reeves | External Advisor | telegram | `tom_telegram_{uuid}.jsonl` | `PLACEHOLDER_TOM_TELEGRAM_UUID` | initial + Update 2 append |
| Jordan, Alex, Mia, Omar | #board-prep | feishu | `board_prep_feishu_{uuid}.jsonl` | `PLACEHOLDER_BOARD_PREP_UUID` | initial + Update 3 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Board deck ARR $2.4M vs actual contracted $2.1M | R2 | R2->R5 |
| C2 | PLG growth narrative vs 100% sales-driven acquisition | R3 | R3->R7 |
| C3 | Sprint velocity synthesis (NON-CONFLICT) | R1 | None |
| C4 | Omar governance warning vs Jordan "everything is fine" | R2 | Phase 1->Phase 3 |
| B1 | Agent endorses $2.4M as defensible in #board-prep Loop 6 | R5 | R7 |
| B2 | Agent accepts Mia's 55% conversion without probing methodology in Mia DM Loop 8 | R6 | R8 |

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
