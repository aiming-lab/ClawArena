# trace_d4 -- Patient Safety Incident: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_d4`

**Scenario:** An adverse cardiac event during a routine cardiac catheterization at Pacific Heights Medical Center produces three irreconcilable accounts: the attending physician Dr. Marcus Webb attributes the complication to equipment malfunction, but the cath lab equipment logs show all devices operated within normal parameters throughout the procedure. Nurse Amy Chen's contemporaneous notes document verbal orders the attending never entered into the chart. Legal Counsel Jennifer Wu initially assesses "low liability" but escalates after reviewing all three primary accounts. Dr. Kenji Tanaka (Department Head, Cardiology) must reconcile these diverging narratives for the incident investigation, a potential malpractice defense, and an imminent Joint Commission review. The scenario spans 3 weeks with 6 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference the attending's incident report (equipment malfunction claim) with equipment logs (normal operation) and nursing notes (undocumented verbal orders) to identify where accounts materially conflict? (MS)
2. Can the agent integrate new evidence (equipment maintenance records, pharmacy log, patient vitals flowsheet, expert review) and revise prior risk assessments -- including correcting the B1 and B2 bias phrases? (DU)
3. Does the agent maintain Dr. Tanaka's preferred format (structured reports with confidence intervals and probability ranges) for all subsequent analyses after calibration? (P)
4. Can the agent synthesize the clinical (Dr. Yun), legal (Jennifer Wu), compliance (Angela Reeves), and frontline-nursing (Amy Chen / Patricia Walsh) perspectives to produce an accurate comprehensive assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d4/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d4/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d4/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d4/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W3), 8 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (~30 total rounds + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 12 eval rounds (r1--r12): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Dr. Min-Ji Yun | Associate Chief of Cardiology | Telegram DM | `yun_telegram_{uuid}.jsonl` | `PLACEHOLDER_YUN_TELEGRAM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Patricia Walsh | Nurse Director, Cardiac ICU | Discord DM | `walsh_discord_{uuid}.jsonl` | `PLACEHOLDER_WALSH_DISCORD_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Angela Reeves | Compliance Officer | Discord DM | `reeves_discord_{uuid}.jsonl` | `PLACEHOLDER_REEVES_DISCORD_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Jennifer Wu | Hospital Legal Counsel | Discord DM | `wu_discord_{uuid}.jsonl` | `PLACEHOLDER_WU_DISCORD_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| #cardiac-safety | Group: Kenji, Walsh, Angela, Amy Chen, Yun | Discord Group | `cardiac_safety_discord_{uuid}.jsonl` | `PLACEHOLDER_CARDIAC_SAFETY_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| #risk-management | Group: Kenji, Angela, Jennifer Wu, Whitfield | Feishu Group | `risk_mgmt_feishu_{uuid}.jsonl` | `PLACEHOLDER_RISK_MGMT_UUID` | initial (Phase 1) |

**Notes:**
- Dr. Marcus Webb (attending) and Nurse Amy Chen do NOT have dedicated DM sessions with Kenji. Their accounts are delivered through workspace documents (Webb's incident report, Chen's nursing notes) and group channels.
- Angela Reeves's Phase 2 append (Update 3) delivers the external expert biomechanical review that rebuts the equipment-malfunction claim.
- Jennifer Wu's Phase 2 append (Update 4) captures her liability re-assessment escalation after all three primary accounts have been reviewed.
- The #risk-management Feishu group has no Phase 2 append; escalation occurs implicitly through Jennifer Wu's Phase 2 DM.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Equipment status: Webb's report claims "catheter guide-wire manipulator unit showed intermittent pressure feedback failure" vs equipment logs show all devices within normal operating parameters throughout procedure | R2 (partial -- equipment logs vs Webb's report) | R2->R4 (full reversal after Update 2: maintenance records confirm no prior faults) |
| C2 | Verbal orders: Webb's chart has no record of midazolam 2mg IV push at 14:32 vs Amy Chen's nursing notes document the verbal order and her administration of it | R3 (both positions visible) | R3->R5 (pharmacy log confirms midazolam draw at 14:31, corroborating Chen's notes) |
| C3 | Procedure timeline (NON-CONFLICT): vitals trend, drug administration sequence, equipment readings, and door-entry log are all consistent when synthesized across sources | R1 (persistent synthesis) | None |
| C4 | Legal liability: Jennifer Wu initially assesses "low liability -- equipment-malfunction narrative is defensible" vs escalates to "elevated liability" after reviewing all three primary accounts together | R6 (initial low-liability position) | R6->R11 (full escalation after Update 4) |
| B1 | #cardiac-safety Loop 10: Agent accepts Webb's incident report framing at face value -- "equipment malfunction appears to be the proximate cause of the adverse event based on the attending's official report" | R4 (corrected by equipment logs and Update 2 maintenance records) | Explicit correction in reeves_discord Phase 2 Loop 14 agent reply |
| B2 | walsh_discord Loop 6: Agent treats "no formal complaint filed by nursing staff before the event" as evidence the care environment was normal -- missing that Walsh had raised informal concerns about Webb's sedation practices two weeks earlier | R5 (corrected by Update 3: Walsh's prior informal escalation email surfaces in compliance review) | Explicit reversal when Update 3 reveals Walsh's email |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, YUN_TELEGRAM, WALSH_DISCORD, REEVES_DISCORD, WU_DISCORD, CARDIAC_SAFETY, RISK_MGMT
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (equipment status), C2 (verbal orders / chart gap), C3 (procedure timeline -- non-conflict), C4 (legal liability escalation)
- Biases: B1 (#cardiac-safety Loop 10), B2 (walsh_discord Loop 6)
- Updates: U1 on R4, U2 on R5, U3 on R8, U4 on R11
- 6 history sessions + 1 main session; 4 sessions receive Phase 2 appends

---

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_d4/`

**Step 1a: Create 5 Agent Configuration Files**
- AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md

**Step 1b: Create 7 Initial Scenario Files**
- incident_report_webb.md (attending's official incident report)
- nursing_notes_chen.md (Amy Chen's contemporaneous nursing notes)
- equipment_log_cathlab.md (cath lab equipment operating log)
- patient_chart_excerpt.md (official procedure chart -- Webb's documentation)
- cath_lab_protocol.md (standard operating protocol for cardiac catheterization)
- staffing_roster_d4.md (procedure suite staffing on day of incident)
- incident_response_log.md (immediate post-incident response actions)

**Step 1c: Create Update-Added Files (under `updates/`)**
- updates/equipment_maintenance_records.md (U1: maintenance history showing no prior faults -- C1 context)
- updates/pharmacy_dispensing_log.md (U2: midazolam draw confirmed at 14:31 -- C2 reversal trigger)
- updates/expert_review_biomechanical.md (U3: external expert review rebutting equipment-malfunction claim)
- updates/legal_liability_memo_v2.md (U4: Jennifer Wu's escalated liability assessment)

---

### Step 2--8: Standard Build Sequence

Follow the same pattern as trace_a5 steps 2--8, replacing all placeholder UUIDs with D4 values, all file paths with `trace_d4`, and all medical domain references as specified in layer0--layer4.

---

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text is in English
- `questions.json` is a single group object for `trace_d4`
- Update-created new sessions carry `channel`
- All 6 initial history sessions are registered in `sessions.json` before eval runs
- B1 exact phrase appears in #cardiac-safety Loop 10
- B2 exact phrase appears in walsh_discord Loop 6
- C1 contradiction is traceable to two independent sources (incident_report_webb.md vs equipment_log_cathlab.md)
- C2 contradiction is traceable to two independent sources (patient_chart_excerpt.md vs nursing_notes_chen.md)
- C3 (timeline) is NON-CONFLICT -- all sources must be internally consistent
- C4 escalation spans two Jennifer Wu DM phases (initial low-liability + Update 4 escalation)
- exec_check questions appear in rounds R3, R6, R9, R12 (~27% of rounds -- within 20-40% target)
- P1-P5 preference injections occur across calibration R2, R5, R8, R11 (4 injection stages)
