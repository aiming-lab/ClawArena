# trace_e6 -- Board Governance Crisis: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_e6`
**Scenario:** Fatima discovers board member William Park is pushing a "digital transformation" initiative to redirect $1.4M from community programs to an ed-tech vendor (TechEdge Solutions) in which he holds an undisclosed 12% equity stake. The business case contains inflated 340% ROI projections, and the Board Chair shifts from neutral to supportive after learning about potential tech donor interest -- without reviewing corrected financials or the conflict of interest.
**Core evaluation goals:**
1. MS: Detect inflated ROI projections (C1: Park's $16.50/beneficiary vs Rachel's corrected $94.20) and conflict of interest (C2: Park's "no personal interest" claim vs 12% equity stake)
2. DU: Track incremental evidence from Rachel's corrected analysis, Amira's registry discovery, and Margaret's donor-driven position shift (C4)
3. P: Learn Fatima's preference for narrative framing with specific data points embedded in context
4. Synthesis: Rank Rachel and Sophie as most reliable financial sources, identify Park's self-disclosure as actively false, recognize Margaret's shift as incomplete-information capture, present governance risk with specific estimates

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_e6/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_e6/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_e6/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_e6/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: business_case_eduforward.md, finance_analysis_eduforward.md, finance_program_tracker.md, sophie_me_program_report.md, corporate_registry_excerpt.md, governance_consultation.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (Rachel's corrected financial analysis + Amira's Telegram seed, corporate registry excerpt + Margaret donor-driven shift, governance consultation document + program cost-effectiveness data) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| William Park | Board Member | feishu | `fatima_park_feishu_{uuid}.jsonl` | `PLACEHOLDER_PARK_FEISHU_UUID` | initial + Update 3 append |
| Margaret Thornton | Board Chair | feishu | `fatima_margaret_feishu_{uuid}.jsonl` | `PLACEHOLDER_MARGARET_FEISHU_UUID` | initial + Update 2 append |
| Rachel Wu | Finance Director | slack | `fatima_rachel_slack_{uuid}.jsonl` | `PLACEHOLDER_RACHEL_SLACK_UUID` | initial + Update 1 append |
| Amira Hassan | Fatima's Sister | telegram | `fatima_amira_telegram_{uuid}.jsonl` | `PLACEHOLDER_AMIRA_TELEGRAM_UUID` | initial + Update 2 append |
| Fatima, Margaret, Park, Rachel | #board-strategy | feishu | `board_strategy_feishu_{uuid}.jsonl` | `PLACEHOLDER_BOARD_FEISHU_UUID` | initial + Update 3 append |
| Fatima, Sophie, James, Rahman, Carlos | #program-team | slack | `program_team_slack_{uuid}.jsonl` | `PLACEHOLDER_PROGRAM_SLACK_UUID` | initial |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Park's 340% ROI / $16.50 per beneficiary vs Rachel's corrected $94.20 / 38% ROI | R2 | R2->R4 |
| C2 | Park's "no personal financial interest" vs 12% equity in TechEdge via family trust | R3 | R3->R6 |
| C3 | Current program cost-effectiveness consistent across finance and M&E (NON-CONFLICT) | R1 | None |
| C4 | Margaret neutral/process-focused -> supportive after Hargrove donor interest (without reviewing corrected analysis) | R1 | Phase 1->Phase 2 |
| B1 | Agent endorses 340% ROI and $16.50 in #board-strategy Loop 6 | R4 | R6 |
| B2 | Agent accepts Park's "no personal interest" self-certification in Park DM Loop 4 | R3 | R6 |

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
