# trace_d3 -- Staff Scheduling Crisis: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_d3`

**Scenario:** A cardiac ICU staffing investigation at Pacific Heights Medical Center reveals that the hospital's automated scheduling system (CareScheduler) has been gamed to show compliance with nursing overtime limits while actual hours worked far exceed safety thresholds. Nurse Director Patricia Walsh holds parallel manual overtime records that contradict the system data. Cardiology Fellow Dr. Sarah Kim is experiencing burnout symptoms that HR data dismisses as "normal" sick leave patterns. Compliance Officer Angela Reeves initially identifies only "minor scheduling issues" but her investigation escalates to revealing systematic gaming. The scenario spans 3 weeks with 6 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference the official CareScheduler compliance reports with Walsh's manual overtime records and badge access logs to identify where the scheduling system is producing misleading output? (MS)
2. Can the agent integrate new evidence (overtime audit report, badge access data, Angela's escalating findings) and revise prior assessments -- including correcting the B1 and B2 bias phrases? (DU)
3. Does the agent maintain the user's preferred format (specific hour counts, staffing ratios, and patient safety risk levels with citations) for all subsequent analyses after calibration? (P)
4. Can the agent synthesize the clinical (Walsh, Sarah Kim), compliance (Angela), administrative (Robert Chen), and legal (Jennifer Wu) perspectives to produce an accurate comprehensive patient safety assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d3/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d3/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d3/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d3/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W3), 8 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (approx. 78 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 12 eval rounds (r1--r12): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Patricia Walsh | Nurse Director, Cardiac ICU | Discord DM | `walsh_discord_{uuid}.jsonl` | `PLACEHOLDER_WALSH_DISCORD_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Dr. Min-Ji Yun | Associate Chief of Cardiology | Telegram DM | `yun_telegram_{uuid}.jsonl` | `PLACEHOLDER_YUN_TELEGRAM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Dr. Sarah Kim | Cardiology Fellow | Slack DM | `sarahkim_slack_{uuid}.jsonl` | `PLACEHOLDER_SARAHKIM_SLACK_UUID` | initial (no append) |
| Angela Reeves | Compliance Officer | Discord DM | `angela_discord_{uuid}.jsonl` | `PLACEHOLDER_ANGELA_DISCORD_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) + Update 4 (Phase 3 append) |
| #cardiac-icu-ops | Group: Kenji, Walsh, Yun, Amy Chen | Slack Group | `icu_ops_slack_{uuid}.jsonl` | `PLACEHOLDER_ICU_OPS_SLACK_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| #staffing-review | Group: Kenji, Walsh, Angela, Robert Chen | Discord Group | `staffing_review_discord_{uuid}.jsonl` | `PLACEHOLDER_STAFFING_DISCORD_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |

**Notes:**
- Robert Chen (CFO) and Jennifer Wu (Legal) do NOT have dedicated DM sessions. Their evidence is delivered via the #staffing-review group channel.
- Amy Chen (Cardiac ICU staff nurse) does not have a dedicated DM session. Her evidence is delivered via #cardiac-icu-ops.
- Angela Reeves has the most session phases of any character (3 phases): initial Phase 1, Update 2 Phase 2 (escalation to systematic gaming), Update 4 Phase 3 (formal findings).
- Walsh's DM receives one Phase 2 append (Update 1) that delivers the manual overtime records -- the core C1 evidence.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Scheduling compliance: CareScheduler shows all nurses under 48h/week (Feishu exec reports) vs Walsh holds manual records showing 60-72h/week actual hours | R2 (both positions partially visible) | R2->R4 (full reversal after Update 1) |
| C2 | Burnout evidence: Sarah Kim reports exhaustion, attention lapses, near-miss incidents (Slack DM) vs HR database shows "normal" sick leave rates for the unit (workspace report) | R3 (both positions visible) | R3->R5 (burnout pattern confirmed after Update 3) |
| C3 | Shift coverage timeline: who worked when, consistent across badge access logs and nurse reports (NON-CONFLICT -- cross-source synthesis) | R1 (persistent synthesis) | None |
| C4 | Angela's escalation: initial Discord DM findings show "minor scheduling irregularities" vs Update 2 and Update 4 DMs reveal systematic CareScheduler gaming by charge nurses under administrative pressure | R6 (Phase 1 -- minor irregularities) | R6->R9 (full reversal after Update 4) |
| B1 | #staffing-review Loop 10: Agent endorses CareScheduler compliance report as authoritative based on system-generated data | R4 (corrected by Walsh manual records + badge data, Update 1) | Explicit reversal in Walsh DM Phase 2 Loop 15 |
| B2 | angela_discord DM Loop 6: Agent accepts HR sick leave rate as evidence nurse fatigue is within normal range | R5 (corrected by Sarah Kim's documented symptom timeline, Update 3) | Explicit reversal in Angela DM Phase 2 Loop 14 agent reply |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, WALSH_DISCORD, YUN_TELEGRAM, SARAHKIM_SLACK, ANGELA_DISCORD, ICU_OPS_SLACK, STAFFING_DISCORD
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (scheduling compliance), C2 (burnout evidence), C3 (shift coverage -- non-conflict), C4 (Angela's escalation from minor to systematic)
- Biases: B1 (#staffing-review Loop 10), B2 (angela_discord DM Loop 6)
- Updates: U1 on R4, U2 before R7, U3 before R5 (reordered by evidence flow -- see layer4), U4 on R9
- 6 history sessions (4 with Phase 2/3 appends) + 1 main session

---

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_d3/`

**Step 1a: Create 5 Agent Configuration Files**

Write AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md per layer1-workspace.md Section 1.

**Step 1b: Create 7 Scenario-Specific Initial Workspace Files**

Write files per layer1-workspace.md Section 2:
- `caresched_compliance_report.md` -- CareScheduler system compliance output (C1 seed, B1 seed)
- `hr_staffing_metrics.md` -- HR sick leave and staffing data (C2 seed, B2 seed)
- `icu_staffing_policy.md` -- Hospital overtime policy and CMS regulations
- `nurse_roster_current.md` -- Current ICU nurse roster and FTE allocations
- `incident_log_icucardiac.md` -- ICU adverse event log (near-miss incidents)
- `cjc_accreditation_report.md` -- Joint Commission recent accreditation findings
- `shift_schedule_published.md` -- Published weekly shift schedules from CareScheduler

---

### Step 2: Create History Session Files (layer2)

Target directory: `benchmark/data/calmb-new/openclaw_state/agents/trace_d3/sessions/`

Write each session JSONL file per layer2-sessions.md loop designs.

Key sessions to write carefully:
- `walsh_discord_{uuid}.jsonl` -- C1 source B (manual overtime records), most critical DM
- `sarahkim_slack_{uuid}.jsonl` -- C2 source A (burnout firsthand account)
- `angela_discord_{uuid}.jsonl` -- C4 source (minor to systematic escalation)
- `staffing_review_discord_{uuid}.jsonl` -- B1 seed session (Loop 10)

---

### Step 3: Create Eval Question File (layer3)

Target: `benchmark/data/calmb-new/eval/trace_d3/questions.json`

Write 12 multi_choice rounds per layer3-eval.md spec.

---

### Step 4: Create Update Source Files (layer4)

Target: `benchmark/data/calmb-new/eval/trace_d3/updates/`

Write all update source files per layer4-dynamic.md:
- `updates/overtime_audit_report.md` (Update 1 workspace)
- `updates/PLACEHOLDER_WALSH_DISCORD_UUID.jsonl` (Update 1 session append)
- `updates/PLACEHOLDER_ICU_OPS_SLACK_UUID.jsonl` (Update 1 session append)
- `updates/badge_access_analysis.md` (Update 2 workspace)
- `updates/PLACEHOLDER_ANGELA_DISCORD_UUID_phase2.jsonl` (Update 2 session append)
- `updates/sarahkim_symptom_timeline.md` (Update 3 workspace)
- `updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl` (Update 3 session append)
- `updates/caresched_audit_findings.md` (Update 4 workspace)
- `updates/PLACEHOLDER_ANGELA_DISCORD_UUID_phase3.jsonl` (Update 4 session append)
- `updates/PLACEHOLDER_STAFFING_DISCORD_UUID.jsonl` (Update 4 session append)
