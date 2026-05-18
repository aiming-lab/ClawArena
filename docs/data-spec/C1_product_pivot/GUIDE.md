# trace_c1 -- Product Pivot Crisis: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_c1`
**Scenario:** Alex Rivera, PM at NexaFlow, navigates a product pivot crisis where the CEO's verbal Q2 enterprise dashboard promise conflicts with engineering feasibility, customer research contradicts the sales narrative, and a hidden acquisition strategy is driving the roadmap.
**Core evaluation goals:**
1. MS: Detect conflicting claims about timeline feasibility (C1) and customer demand (C2), plus non-conflict feature prioritization synthesis (C3)
2. DU: Track incremental evidence accumulation (Leo's tech debt, Hannah's research) and temporal revelation of the acquisition driver (C4)
3. P: Learn Alex's preference for tables, quantitative metrics, kebab-case file naming, TL;DR-first structure, and informal tone with [URGENT] flags
4. Synthesis: Combine all four contradictions with both biases to produce a comprehensive product strategy assessment ranking source reliability

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c1/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c1/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: product_roadmap_v2.md, customer_feedback_summary.md, engineering_capacity_tracker.md, board_deck_q2_draft.md, decision_log_alex.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content design | 3 |
| `layer3-eval.md` | Eval round plan: question design, round sequencing, cross-round reversal triggers | 4 |
| `layer4-dynamic.md` | Update plan: 4 updates (Hannah's research, Leo's tech debt, acquisition reveal, TechCorp ultimatum) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Jordan Park | CEO / Co-founder | slack | `ceo_jordan_slack_{uuid}.jsonl` | `PLACEHOLDER_JORDAN_SLACK_UUID` | initial + Update 3 append |
| Sana Mehta | CTO / Co-founder | discord | `cto_sana_discord_{uuid}.jsonl` | `PLACEHOLDER_SANA_DISCORD_UUID` | initial + Update 2 append |
| Mia Okafor | Sales Director | slack | `sales_mia_slack_{uuid}.jsonl` | `PLACEHOLDER_MIA_SLACK_UUID` | initial |
| Hannah Kim | UX Researcher | slack | `ux_hannah_slack_{uuid}.jsonl` | `PLACEHOLDER_HANNAH_SLACK_UUID` | initial + Update 1 append |
| Jordan, Sana, Mia, Alex, Hannah, Leo | #product-planning | slack | `product_planning_slack_{uuid}.jsonl` | `PLACEHOLDER_PRODUCT_PLANNING_UUID` | initial + Update 1 append |
| Mia, Alex, Marcus Webb, Raj Patel | #enterprise-deals | feishu | `enterprise_deals_feishu_{uuid}.jsonl` | `PLACEHOLDER_ENTERPRISE_DEALS_UUID` | initial + Update 4 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Q2 promise vs 14-16 wk (18-20 wk real) engineering timeline | R2 | R2->R5 |
| C2 | Mia's "enterprise demand" vs Hannah's 7/8 alerting data | R3 | R3->R6 |
| C3 | Feature prioritization timeline reconstruction (NON-CONFLICT) | R1 | None |
| C4 | Public roadmap customer-demand framing vs private CloudWave acquisition driver | R2 | Phase 1->Phase 2 (R20->R25) |
| B1 | Agent endorses enterprise dashboard demand in #product-planning Loop 8 | R6 | R8 |
| B2 | Agent accepts Q2 as achievable in Jordan DM Loop 5 | R5 | R9 |

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
