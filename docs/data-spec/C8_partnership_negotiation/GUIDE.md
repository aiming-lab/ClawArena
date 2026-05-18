# trace_c8 -- Partnership Negotiation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_c8`
**Scenario:** Alex must choose between two integration partners -- DataSync (favored by CEO Jordan for undisclosed investor reasons) and CloudMerge (technically superior per engineering evaluation) -- while navigating a CEO who frames a strategic preference as technical, inflated revenue projections, and a vendor who privately reveals the investor connection.
**Core evaluation goals:**
1. MS: Detect CEO strategic framing vs technical evaluation (C1), revenue projection vs customer survey conflict (C2), and investor connection vs "purely technical" claim (C4)
2. DU: Track incremental evidence from API benchmarks, customer survey, Carmen's investor disclosure, and Marcus Webb's churn warning
3. P: Learn Alex's preference for structured comparison tables and explicit probability estimates for all option evaluations
4. Synthesis: Rank Sana/Leo/Raj/Marcus Webb as most reliable, recognize Jordan's advocacy as financially motivated, reframe DataSync vs CloudMerge with accurate financial impact

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c8/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c8/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c8/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c8/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: vendor_api_comparison.md, api_benchmark_report.md, customer_survey_report.md, revenue_projection_datasync.md, partnership_eval_criteria.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (API benchmark results, Carmen investor disclosure + customer survey, Marcus Webb churn warning + Jordan escalation) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Jordan Park | CEO / Co-founder | slack | `ceo_jordan_slack_{uuid}.jsonl` | `PLACEHOLDER_JORDAN_SLACK_UUID` | initial + Update 3 append |
| Carmen Diaz | DataSync Partnership Lead | feishu | `partner_carmen_feishu_{uuid}.jsonl` | `PLACEHOLDER_CARMEN_FEISHU_UUID` | initial + Update 2 append |
| Raj Patel | Customer Success Lead | feishu | `cs_raj_feishu_{uuid}.jsonl` | `PLACEHOLDER_RAJ_FEISHU_UUID` | initial + Update 2 append |
| Marcus Webb | TechCorp VP Engineering | slack | `customer_marcus_slack_{uuid}.jsonl` | `PLACEHOLDER_MARCUS_SLACK_UUID` | initial + Update 3 append |
| Jordan, Alex, Carmen, Sana | #partnerships | feishu | `partnerships_feishu_{uuid}.jsonl` | `PLACEHOLDER_PARTNERSHIPS_FEISHU_UUID` | initial |
| Sana, Leo, Alex, Raj | #integration-eval | slack | `integration_eval_slack_{uuid}.jsonl` | `PLACEHOLDER_INTEGRATION_EVAL_SLACK_UUID` | initial + Update 1 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Jordan's "DataSync is technically aligned" vs Sana/Leo benchmark: CloudMerge far superior | R2 | R2->R4 |
| C2 | Mia's $2.1M DataSync ARR projection vs Raj's 73% customer preference for CloudMerge | R3 | R3->R5 |
| C3 | API performance evaluation consistent across all sources (NON-CONFLICT) | R1 | None |
| C4 | Jordan's "purely technical" framing vs Carmen reveals Dave Reyes warrant/investor connection | R9 | R9->R10 |
| B1 | Agent accepts DataSync strategic fit in #partnerships Loop 3 | R4 | R6 |
| B2 | Agent trusts DataSync vendor docs (sub-200ms) in Carmen DM Loop 4 | R4 | R6 |

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
