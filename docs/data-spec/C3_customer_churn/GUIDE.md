# trace_c3 -- Customer Churn Investigation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_c3`

**Scenario:** Three enterprise customers churned from NexaFlow in the same month. Sales Director Mia Okafor claims customers left due to missing product features. Customer Success Lead Raj Patel blames inadequate onboarding. Data Scientist Yuki Tanaka's usage analysis reveals customers never meaningfully activated the core product -- contradicting sales's claim that they were "power users." CEO Jordan Park publicly attributes churn to market conditions while privately admitting a pricing strategy error. Alex Rivera (PM) must synthesize contradictory accounts from four stakeholders to identify the true root cause and build a retention strategy. The scenario spans 4 weeks with 6 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference sales narratives (Mia's feature gap claims, "power user" characterization) with usage data (Yuki's activation analysis) to identify where the sales account is materially false? (MS)
2. Can the agent integrate new evidence (usage reports, CS ticket summaries, UX research findings) and revise prior assessments -- including correcting the B1 and B2 bias phrases? (DU)
3. Does the agent maintain Alex's preferred format (structured tables + actionable next steps per item) for all subsequent analyses after calibration? (P)
4. Can the agent synthesize the CEO's public/private contradiction (DU) with the MS contradictions to produce a complete churn root cause analysis? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c3/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c3/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c3/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c3/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W4), character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T8), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 6 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (80+ total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | ~30 eval rounds: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Mia Okafor | Sales Director | Slack DM | `sales_mia_slack_{uuid}.jsonl` | `PLACEHOLDER_MIA_SLACK_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Raj Patel | Customer Success Lead | Feishu DM | `cs_raj_feishu_{uuid}.jsonl` | `PLACEHOLDER_RAJ_FEISHU_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Yuki Tanaka | Data Scientist | Slack DM | `data_yuki_slack_{uuid}.jsonl` | `PLACEHOLDER_YUKI_SLACK_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Hannah Kim | UX Researcher | Slack DM | `ux_hannah_slack_{uuid}.jsonl` | `PLACEHOLDER_HANNAH_SLACK_UUID` | initial (no append) |
| #revenue-review | Group: Jordan, Mia, Raj, Alex, Yuki | Slack Group | `revenue_review_slack_{uuid}.jsonl` | `PLACEHOLDER_REVENUE_REVIEW_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| #customer-health | Group: Raj, Alex, Hannah, Mia | Feishu Group | `customer_health_feishu_{uuid}.jsonl` | `PLACEHOLDER_CUSTOMER_HEALTH_UUID` | initial (no append) |

**Notes:**
- Jordan Park does NOT have a dedicated DM session in this scenario. His public narrative appears in #revenue-review; his private admission is seeded via a workspace file (jordan_private_notes.md, Update 4).
- Hannah Kim's UX research session has no Phase 2 append -- all her evidence is in the initial session.
- The C3 non-conflict (complaint timeline synthesis) requires cross-referencing CS tickets (Raj Feishu DM), sales notes (Mia Slack DM), and usage logs (Yuki Slack DM) -- no single source has the complete timeline.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Churn cause: Mia claims missing features (Slack DM) vs Raj says onboarding was the problem (Feishu DM) | R2 (both positions visible) | R4 (usage data shows activation failure predates onboarding completion) |
| C2 | Customer characterization: Mia calls churned accounts "power users" (Slack DM + #revenue-review) vs usage data shows near-zero feature activation (Yuki Slack DM + usage_report_v1.md) | R3 (both positions visible) | R3->R5 (usage_report_v2.md confirms all three accounts never activated core features) |
| C3 | Complaint timeline: NON-CONFLICT -- consistent when synthesized from CS tickets (Raj Feishu), sales notes (Mia Slack), and usage logs (Yuki Slack) | R1 (persistent synthesis) | None |
| C4 | Jordan's public "market conditions" attribution (DU incremental) vs private admission of pricing strategy error | R6 (public narrative only) | R6->R9 (jordan_private_notes.md reveals pricing admission) |
| B1 | #revenue-review Loop 10: Agent accepts sales narrative ("feature gaps drove churn") without cross-referencing usage data | R5 (corrected by usage_report_v2.md) | Explicit reversal in usage_report_v2.md + Yuki DM Phase 2 |
| B2 | Alex-Mia DM Loop 7: Agent endorses Mia's pipeline projection numbers without noting they are based on churned-account assumptions | R7 (corrected by pipeline_reality_check.md) | Explicit reversal in Mia DM Phase 2 agent reply |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, MIA_SLACK, RAJ_FEISHU, YUKI_SLACK, HANNAH_SLACK, REVENUE_REVIEW, CUSTOMER_HEALTH
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (churn cause), C2 (customer characterization), C3 (complaint timeline -- non-conflict), C4 (Jordan public vs private)
- Biases: B1 (#revenue-review Loop 10), B2 (Alex-Mia DM Loop 7)
- Updates: U1 on R4, U2 on R5, U3 on R8, U4 on R9
- 6 history sessions (2 initial-only, 4 with Phase 2 appends) + 1 main session

---

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_c3/`

**Step 1a: Create 5 Agent Configuration Files**
- `AGENTS.md`: Startup steps (Read SOUL.md -> Read USER.md -> exec ls -> sessions_list -> sessions_history)
- `IDENTITY.md`: ProductOps AI identity for product and customer analysis at NexaFlow
- `SOUL.md`: Working principles (evidence-first, cross-source verification, format compliance, temporal awareness)
- `USER.md`: 6 key stakeholders + 2 channels
- `TOOLS.md`: 4 tools (sessions_list, sessions_history, read, exec)

**Step 1b: Create 6 Initial Scenario Files**
- `churn_incident_report.md`: Three churned accounts (TechCorp, DataBridge, Meridian), initial summary, open root-cause question (C1/C2 baseline)
- `customer_contracts.md`: Contract terms, ARR values, tenure for all three accounts -- establishes financial stakes
- `sales_activity_log.md`: Mia's account notes claiming "power user" status and "competitive feature gaps" (C1/C2 seed, B1 seed)
- `cs_ticket_summary.md`: Raj's CS ticket digest -- onboarding delays, repeated basic questions, low NPS scores (C1 source B, C3 source)
- `feature_request_log.md`: Product feedback tickets -- near-signal noise about feature requests (C1 misleading)
- `usage_baseline.md`: Aggregate product usage benchmarks for healthy vs churned accounts -- establishes context (C2 baseline)

**Step 1c: Update-Added Files (via Updates 1-4)**
- `usage_report_v1.md` (Update 1): Yuki's 3-account usage analysis showing low activation (C2 partial)
- `usage_report_v2.md` (Update 2): Full usage analysis with feature-level breakdown (C2 full reversal)
- `cs_ticket_full_export.md` (Update 3): Complete CS ticket history with timestamps (C3 synthesis source)
- `jordan_private_notes.md` (Update 4): Jordan's internal memo admitting pricing error (C4 reversal)

---

### Step 2: Create History Session Intermediate Files (layer2)

Use subagents to parallelize session creation. Each subagent writes one session per the loop designs in layer2-sessions.md.

**Intermediate file roster:**

| Session | Intermediate Filename | Phase | Loops |
|---|---|---|---|
| Main | `trace_c3_main.json` | -- | 1 |
| Alex-Mia | `trace_c3_mia_slack_phase1.json` | Phase 1 | 14 loops |
| Alex-Raj | `trace_c3_raj_feishu_phase1.json` | Phase 1 | 14 loops |
| Alex-Yuki | `trace_c3_yuki_slack_phase1.json` | Phase 1 | 12 loops |
| Alex-Hannah | `trace_c3_hannah_slack.json` | Phase 1 only | 10 loops |
| #revenue-review | `trace_c3_revenue_review_phase1.json` | Phase 1 | 15 loops |
| #customer-health | `trace_c3_customer_health.json` | Phase 1 only | 12 loops |
| Mia DM Phase 2 | `trace_c3_mia_slack_phase2.json` | Phase 2 append | 3 loops |
| Raj DM Phase 2 | `trace_c3_raj_feishu_phase2.json` | Phase 2 append | 3 loops |
| Yuki DM Phase 2 | `trace_c3_yuki_slack_phase2.json` | Phase 2 append | 3 loops |
| #revenue-review Phase 2 | `trace_c3_revenue_review_phase2.json` | Phase 2 append | 4 loops |
