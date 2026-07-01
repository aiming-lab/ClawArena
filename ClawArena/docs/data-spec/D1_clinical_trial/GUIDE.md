# trace_d1 -- Clinical Trial Irregularity: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_d1`

**Scenario:** A research integrity investigation at Pacific Heights Medical Center unfolds after research coordinator Linda Torres notices systematic data discrepancies in Dr. Victor Osei's NIH-funded cardiac stent trial (PHMC-STENT-2022). Dr. Osei claims the discrepancies are data entry errors, but Linda's documentation reveals a systematic pattern inconsistent with random error. Co-PI Dr. Hiroshi Sato conducts an independent biostatistical analysis whose conclusion shifts from "minor concern" to "serious fabrication risk" as evidence accumulates. The IRB, meanwhile, focuses on enrollment count discrepancies that suggest a different category of irregularity than Linda's data-pattern findings. Department Head Dr. Kenji Tanaka must navigate all four sources -- Osei's defense, Linda's documentation, Sato's evolving analysis, and the IRB's parallel review -- while protecting $3.4M in NIH funding and the department's research reputation. The scenario spans 5 weeks with 6 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference Dr. Osei's "data entry error" defense with Linda's systematic pattern documentation to identify where the explanation is materially insufficient? (MS)
2. Can the agent track Dr. Sato's evolving analysis from initial "minor concern" to "serious fabrication" as successive evidence triggers update that confidence? (DU)
3. Does the agent maintain Dr. Tanaka's preferred format (structured reports with executive summaries, formal citations, evidence hierarchy, systematic review format, measured/precise tone) throughout? (P)
4. Can the agent synthesize the IRB's enrollment discrepancy findings, Linda's data pattern evidence, and Sato's statistical analysis to produce an accurate, risk-stratified comprehensive assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d1/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d1/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W5), 9 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (90 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 12 eval rounds (r1--r12): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Dr. Victor Osei | Research PI | Slack DM | `pi_osei_slack_{uuid}.jsonl` | `PLACEHOLDER_OSEI_SLACK_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| Linda Torres | Research Coordinator | Slack DM | `coord_linda_slack_{uuid}.jsonl` | `PLACEHOLDER_LINDA_SLACK_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Dr. Hiroshi Sato | Co-PI (Stanford) | Telegram DM | `copi_sato_telegram_{uuid}.jsonl` | `PLACEHOLDER_SATO_TELEGRAM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Dr. Amara Okonkwo | IRB Chair | Feishu DM | `irb_okonkwo_feishu_{uuid}.jsonl` | `PLACEHOLDER_OKONKWO_FEISHU_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| #cardio-research | Group: Kenji, Osei, Sarah Kim, Linda, Sato (remote) | Slack Group | `cardio_research_slack_{uuid}.jsonl` | `PLACEHOLDER_CARDIO_SLACK_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| #trial-review | Group: Kenji, Osei, Okonkwo, Jennifer Wu | Discord Group | `trial_review_discord_{uuid}.jsonl` | `PLACEHOLDER_TRIAL_DISCORD_UUID` | initial (no append) |

**Notes:**
- Dr. Sarah Kim and Jennifer Wu do NOT have dedicated DM sessions. Their evidence is delivered via group channels.
- Dr. Sato's full opinion evolution (from "minor concern" to "serious fabrication risk") occurs across his Phase 1 and Phase 2 DM sessions -- the Phase 2 append (Update 2) is the key DU reversal trigger.
- The IRB session (Okonkwo Feishu DM) receives a Phase 2 append in Update 3 only.
- Dr. Osei's Phase 2 adversarial shift (denial to formal grievance threat) occurs in Update 4.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Data discrepancy explanation: Osei claims "data entry errors" (Slack DM) vs Linda's documentation showing systematic pattern impossible under random error (Slack DM + data_discrepancy_log.md) | R2 (partial -- Linda's pattern summary visible) | R2->R4 (full reversal after Update 1: statistical improbability analysis) |
| C2 | Enrollment numbers: Osei's stated enrollment of 247 participants vs IRB records showing 189 documented consents (MS-conflict) | R3 (both positions visible) | R3->R5 (IRB formal finding confirms discrepancy after Update 3) |
| C3 | Trial timeline -- enrollment dates, protocol amendments, data collection points: NON-CONFLICT -- all sources consistent when synthesized | R1 (persistent synthesis) | None |
| C4 | Dr. Sato's evolving assessment: initial "minor concern -- likely administrative" (Telegram DM Phase 1) shifting to "serious fabrication risk" (Telegram DM Phase 2 after Update 2) | R6 (Phase 1 "minor concern" visible) | R6->R9 (full reversal after Update 2: Sato's biostatistical re-analysis) |
| B1 | #cardio-research Loop 10: Agent endorses Osei's "data entry error" explanation based on his co-authorship record and prior publication history | R4 (corrected by data_discrepancy_log_v2.md showing statistical impossibility of random error) | Explicit reversal in Linda DM Phase 2 Loop 17 agent reply |
| B2 | Kenji-Osei DM Loop 8: Agent accepts Osei's methodology defense regarding non-standard data coding without cross-checking the trial protocol | R4 (corrected by trial_protocol_excerpt.md showing standard coding required) | Explicit reversal when Sato's biostatistical analysis is reviewed |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, OSEI_SLACK, LINDA_SLACK, SATO_TELEGRAM, OKONKWO_FEISHU, CARDIO_SLACK, TRIAL_DISCORD
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (data entry error vs systematic pattern), C2 (enrollment numbers -- MS-conflict), C3 (trial timeline -- non-conflict), C4 (Sato's evolving assessment -- DU-conflict)
- Biases: B1 (#cardio-research Loop 10), B2 (Kenji-Osei DM Loop 8)
- Updates: U1 on R4, U2 on R6 (Sato Phase 2 append), U3 on R9 (IRB formal finding), U4 on R11 (Osei escalation)
- 6 history sessions (4 with Phase 2 appends) + 1 main session
