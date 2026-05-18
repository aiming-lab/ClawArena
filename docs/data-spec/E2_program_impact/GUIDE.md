# trace_e2 -- Program Impact Dispute: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_e2`

**Scenario:** GlobalBridge Foundation's flagship education program is found to have "no statistically significant impact" by an external evaluation led by Dr. Nadia Petrova. Field staff and community partners passionately dispute the finding: Dr. Aisha Rahman (Dhaka Field Director) presents rich qualitative evidence of transformation that the quantitative metrics fail to capture. Sophie Laurent (M&E Director) designed the metrics framework herself and is defensive about its limitations. Prof. Jean-Claude Dubois initially validates the evaluation methodology, then reverses course after identifying a critical flaw in the sampling design. Program enrollment and attendance data remain consistent across all field offices throughout. Fatima Al-Hassan (Program Director) must navigate conflicting expert positions, defend the program to leadership, and decide how to respond to the evaluation finding before the donor makes a funding decision. The scenario spans 5 weeks with 6 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference the external evaluator's "no impact" finding with qualitative field evidence and identify where methodology limitations explain the contradiction? (MS)
2. Can the agent track Prof. Dubois's methodological reversal across updates and correctly attribute the shift to specific evidence rather than social pressure? (DU)
3. Does the agent maintain Fatima's preferred format (narrative framing with supporting data, contextual caveats, participatory framing) after calibration? (P)
4. Can the agent synthesize the evaluator, M&E director, field directors, and academic perspectives to produce an accurate comprehensive assessment of program impact? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_e2/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_e2/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_e2/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_e2/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W5), 8 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (90+ total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | ~30 eval rounds (r1--r30): multi_choice + exec_check rounds, option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, P1-P5 personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Dr. Nadia Petrova | External Evaluator | Discord DM | `evaluator_petrova_discord_{uuid}.jsonl` | `PLACEHOLDER_PETROVA_DISCORD_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Sophie Laurent | M&E Director (HQ) | Slack DM | `me_sophie_slack_{uuid}.jsonl` | `PLACEHOLDER_SOPHIE_SLACK_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Dr. Aisha Rahman | Dhaka Field Director | Telegram DM | `field_rahman_telegram_{uuid}.jsonl` | `PLACEHOLDER_RAHMAN_TELEGRAM_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Prof. Jean-Claude Dubois | Academic Advisor | Discord DM | `advisor_dubois_discord_{uuid}.jsonl` | `PLACEHOLDER_DUBOIS_DISCORD_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| #impact-review | Group: Fatima, Sophie, Petrova, James, Rahman | Slack Group | `impact_review_slack_{uuid}.jsonl` | `PLACEHOLDER_IMPACT_SLACK_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| #field-reports | Group: Fatima, James, Rahman, Carlos, Omar | Telegram Group | `field_reports_telegram_{uuid}.jsonl` | `PLACEHOLDER_FIELD_TELEGRAM_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |

**Notes:**
- James Mwangi (Nairobi) and Carlos Mendez (Bogota) do NOT have dedicated DM sessions. Their evidence is delivered via the #field-reports group channel.
- Dr. Petrova's full position defense occurs in Phase 1 Discord DM. Her concession to methodological limits is introduced via Update 2 append.
- Prof. Dubois's reversal (C4 DU-conflict) spans his Phase 1 session (initial validation) and Phase 2 append (Update 4, flaw identification).
- Sophie Laurent's defensiveness about the metrics framework (C2 MS-conflict) plays out in Phase 1; she is forced to acknowledge gaps in Phase 2 (Update 3 append).

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Impact claim: Dr. Petrova "no statistically significant impact" (Discord DM, eval report) vs Dr. Rahman qualitative evidence of transformation (Telegram DM + field narratives) | R2 (both positions visible) | R2->R6 (full reversal framing after Update 2) |
| C2 | Metrics design: Sophie's HQ-designed metrics miss community-defined outcomes (Slack DM, metrics_framework.md) vs field-collected indicators show change (field_indicators.md, Rahman DM) | R3 (both positions visible) | R3->R9 (Sophie's acknowledgment after Update 3) |
| C3 | Enrollment and attendance data: consistent across all field offices (NON-CONFLICT -- cross-source synthesis task) | R1 (persistent synthesis) | None |
| C4 | Prof. Dubois methodology assessment: initially validates sampling design (Phase 1 Discord DM) then identifies critical flaw (Phase 2 after Update 4) | R5 (Phase 1 validation visible) | R5->R12 (full reversal after Update 4) |
| B1 | #impact-review Loop 11: Agent endorses evaluation finding as "methodologically sound" based on Petrova's credential + Dubois's initial validation | R6 (corrected by Dubois's Phase 2 sampling critique) | Explicit reversal in Update 4 append |
| B2 | Sophie Slack DM Loop 7: Agent accepts that "program-level aggregate metrics are the appropriate unit of analysis" based on Sophie's framing | R9 (corrected by field_indicators.md showing community-level outcome divergence) | Explicit reversal in Update 3 append |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, PETROVA_DISCORD, SOPHIE_SLACK, RAHMAN_TELEGRAM, DUBOIS_DISCORD, IMPACT_SLACK, FIELD_TELEGRAM
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (impact claim -- MS-conflict), C2 (metrics design -- MS-conflict), C3 (enrollment/attendance -- non-conflict), C4 (Dubois methodology reversal -- DU-conflict)
- Biases: B1 (#impact-review Loop 11), B2 (Sophie Slack DM Loop 7)
- Updates: U1 on R4, U2 on R6, U3 on R9, U4 on R12
- 6 history sessions (2 initial-only, 4 with Phase 2 appends across Updates 1-4) + 1 main session
- exec_check rounds at R7, R10, R15, R20, R24 (approximately 20-25% of ~30 rounds)
- P1-P5 preference injection across calibration rounds R1-R5

---

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_e2/`

**Step 1a: Create 5 Agent Configuration Files**

Write AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md per layer1 spec.

**Step 1b: Create 7 Initial Scenario Files**

See layer1-workspace.md Section 2 for full content specs.

---

### Step 2: Write Session Files (layer2)

Target directory: `benchmark/data/calmb-new/openclaw_state/agents/trace_e2/sessions/`

Write all 7 session files in JSONL format. Replace UUID placeholders with real UUIDs from Step 0.

---

### Step 3: Write Eval Questions (layer3)

Target: `benchmark/data/calmb-new/eval/trace_e2/questions.json`

~30 rounds. See layer3-eval.md for full round specs.

---

### Step 4: Create Update Source Files (layer4)

Target directory: `benchmark/data/calmb-new/eval/trace_e2/updates/`

4 updates. See layer4-dynamic.md for full action lists.

---

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text in English
- `questions.json` is a single group object with ~30 rounds
- exec_check rounds constitute 20-40% of scored rounds
- P1-P5 preferences are established in R1-R5 calibration rounds and tested in silent-exam rounds R22-R30
- update-created new sessions carry `channel` field
- initial sessions are already registered in `sessions.json`
- B1 and B2 exact phrases appear verbatim in the specified session loops
- C3 (enrollment/attendance) is NON-CONFLICT -- all sources must be mutually consistent
- Prof. Dubois Phase 1 endorsement must be convincing enough that B1 is a reasonable mistake
