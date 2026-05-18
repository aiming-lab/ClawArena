# trace_i1 -- ER Patient Handoff Information Gap: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_i1`

**Scenario:** A chest-pain patient (Zhang Guoqiang, 58M, NSTEMI) is handed off during a night shift change. Three documentation sources -- HIS electronic medical record, nursing handoff sheet, and doctor verbal handoff notes -- contain inconsistent information about nitroglycerin dosage, symptom onset time, and penicillin allergy status. Lin Yi (ER attending, incoming shift) must cross-reference the sources, identify discrepancies, determine which source is most reliable for each data point, and produce a formal incident analysis. The most safety-critical finding is that the penicillin allergy is documented in HIS but missing from both the nursing handoff sheet (paper form design flaw) and doctor verbal notes (fatigue omission).

**Core evaluation goals:**
1. Can the agent cross-reference medication dosages across HIS, nursing handoff, verbal notes, and MAR to identify where each source is correct or incorrect? (MS)
2. Can the agent integrate new evidence (third troponin, nurse callback, full MAR, morning rounds) and revise prior assessments -- including correcting B1 (physician verbal trust bias) and B2 (allergy minimization)? (DU)
3. Does the agent maintain Lin Yi's preferred format (structured case format, date+patientID naming, diagnosis first, evidence-based medicine, concise professional) after calibration? (P)
4. Can the agent synthesize clinical data (troponin trend, onset time), documentation analysis (three-source comparison), and patient safety assessment (allergy omission systemic risk) to produce a comprehensive incident analysis? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_i1/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_i1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_i1/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_i1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (20:00--08:00), 7 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 6 sessions: main session + 5 history sessions (~61 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (R1--R30) spread across 12 question types: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Wang Yifan (王一凡) | Outgoing Attending | 科室微信 IM | `colleague_wangdoc_im_{uuid}.jsonl` | `PLACEHOLDER_WANGDOC_IM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Nurse Head Li (李护士长) | Nursing Head | 科室微信 IM | `nursehead_li_im_{uuid}.jsonl` | `PLACEHOLDER_NURSEHEAD_LI_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Dr. Zhang (张主任) | Department Chief | 科室微信 IM | `chief_zhang_im_{uuid}.jsonl` | `PLACEHOLDER_CHIEF_ZHANG_IM_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| Dr. Sun (孙医生) | PGY-2 Resident | 科室微信 IM | `resident_sun_im_{uuid}.jsonl` | `PLACEHOLDER_RESIDENT_SUN_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| #急诊科群 | Department Group | 科室微信群 | `er_group_im_{uuid}.jsonl` | `PLACEHOLDER_ER_GROUP_IM_UUID` | initial (Phase 1 only) |

**Notes:**
- Patient Zhang Guoqiang does NOT have a dedicated session. His clinical data is in workspace documents (HIS, nursing handoff, labs, MAR).
- Nurse Li Mei (outgoing triage nurse) does NOT have a dedicated session. Her input comes through the nursing handoff sheet (initial) and callback transcript (Update 2).
- Nurse Chen Hong (incoming night nurse) appears in the #急诊科群 but does not have a dedicated DM session.
- 4 of 5 history sessions receive Phase 2 appends through updates. #急诊科群 has no Phase 2 append.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Drug dosage discrepancy: HIS shows NTG 0.5mg x2 (total 1mg), nursing handoff says "1mg" (total), verbal notes say "0.5mg x1" (missed second dose). Heparin: HIS 4500u vs nursing 4000u vs verbal 4500u. | R2 (three-source NTG discrepancy visible) | R2->R6 (full resolution after Update 3: MAR confirms two NTG doses + heparin 4500u) |
| C2 | Onset time differs: HIS "约18:00" vs nursing "20:30左右" (arrival/onset confusion) vs verbal "约19:00" (fatigue misremembering) | R3 (three-source onset discrepancy visible) | R3->R7 (full resolution after Update 2: nurse callback confirms ~18:30 onset) |
| C3 | Lab result timeline (NON-CONFLICT): troponin 0.08 -> 0.45 -> 0.89, ECG findings, vital signs all consistent across all sources | R1 (persistent synthesis) | None |
| C4 | Penicillin allergy: present in HIS, absent from nursing handoff (form design flaw -- allergy on back page), absent from verbal notes (fatigue omission) | R4 (allergy absent from 2 of 3 sources) | R4->R8 (full reversal after Updates 3+4: systemic safety gap identified by Nurse Head Li + Dr. Zhang) |
| B1 | Wang Doctor IM Phase 1, Loop 4: Agent trusts physician verbal notes over nursing handoff as more reliable (physician-to-physician communication bias) | R5 (bias visible from Wang IM) | Full reversal when MAR shows nursing total was correct and verbal notes missed a dose (Update 3) |
| B2 | Nurse Head Li IM Phase 1, Loop 3: Agent dismisses allergy omission as "minor documentation gap" since cardiac treatment doesn't involve penicillin | R8 (bias visible from Li IM) | Full reversal when near-miss precedent + Dr. Zhang's assessment shows systemic safety risk (Updates 3+4) |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 6 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 6 times for: MAIN, WANGDOC_IM, NURSEHEAD_LI_IM, CHIEF_ZHANG_IM, RESIDENT_SUN_IM, ER_GROUP_IM
```

Record all 6 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (drug dosage), C2 (onset time), C3 (lab timeline -- non-conflict), C4 (allergy omission)
- Biases: B1 (Wang IM Loop 4), B2 (Li Nurse Head IM Loop 3)
- Updates: U1 on R5, U2 on R7, U3 on R11, U4 on R21
- 5 history sessions (4 with Phase 2 appends, 1 group chat without append) + 1 main session
- Lin Yi P1-P5 preferences injected in 4 stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_i1/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 5 initial scenario files, then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 5 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in colleague_wangdoc_im Loop 4 agent reply. B2 exact phrase must appear in nursehead_li_im Loop 3 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_i1/questions.json` with 30 rounds.

Lin Yi's P1-P5 preferences are calibrated in R1 (structured case format), R2 (diagnosis first), main session messages (EBM, concise professional). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write 4 update workspace files and 4 session append files in `updates/` subfolder. Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in colleague_wangdoc_im Loop 4
- [ ] B2 phrase appears verbatim in nursehead_li_im Loop 3
- [ ] C1 sources are independent (his-patient-record.md vs nursing-handoff-sheet.md vs doctor-verbal-notes.md vs medication-administration-record.md)
- [ ] C2 sources are independent (HIS onset vs nursing onset vs verbal onset vs nurse-callback-transcript.md)
- [ ] C3 has NO contradictions -- all lab values consistent across all sources
- [ ] C4 sources show allergy present in HIS, absent from nursing handoff and verbal notes
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Lin Yi P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 20-40% of total rounds (9/30 = 30%)
- [ ] Factual figures consistent: NTG (0.5mg x2 = 1mg total), heparin (4500u), troponin (0.08, 0.45, 0.89), onset (~18:00-18:30), allergy (penicillin), vitals (BP 165/95, HR 98, SpO2 96%), patient (58M, 75kg, NSTEMI)
- [ ] Medical content clinically plausible: NSTEMI management per ACS guidelines, troponin kinetics realistic, heparin dosing weight-based, NTG sublingual protocol standard
