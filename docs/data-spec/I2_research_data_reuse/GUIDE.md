# trace_i2 -- Research Data Reuse Accusation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_i2`

**Scenario:** Lin Yi (林怡), an attending ER physician, published a paper on acute chest pain triage outcomes. An anonymous complaint accuses her of "data reuse" and "duplicate publication." The paper reports N=847, the raw case database has N=912, and co-author 王医生's data version has N=847 but with 23 different patient record IDs. The actual explanation is version control in the data cleaning pipeline: the raw DB includes 65 HIS migration duplicates, and V2.0 vs V2.1 of the dedup pipeline select different "primary" records for 23 patients (clinical outcomes identical). The complaint conflates deduplication with selective inclusion and institutional data overlap with duplicate publication. Meanwhile, 王医生 shifts from supportive to cautious when the Academic Integrity Committee gets involved, driven by career self-preservation rather than guilt.

**Core evaluation goals:**
1. Can the agent reconcile three dataset versions (paper, raw DB, co-author) against the pipeline log to identify version control as the explanation? (MS)
2. Can the agent revise assessments when pipeline evidence contradicts the complaint's framing, and distinguish 王医生's career self-preservation from complicity? (DU)
3. Does the agent maintain Lin Yi's preferred format (clinical structure, diagnosis-first, evidence-based, concise)? (P)
4. Can the agent synthesize technical, interpersonal, and institutional perspectives to produce an accurate committee response recommendation? (MS+DU+P)

**Final data output paths:**
- Workspace: `benchmark/data/calmb-new/workspaces/trace_i2/`
- Sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_i2/sessions/`
- Eval: `benchmark/data/calmb-new/eval/trace_i2/questions.json`
- Updates: `benchmark/data/calmb-new/eval/trace_i2/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: 2-week timeline, 4 character profiles, contradiction map (C1--C4), biases (B1--B2), eval traps, writer constraints | 1 |
| `layer1-workspace.md` | Workspace: 5 config + 5 initial + 4 update files, timing, noise design | 2 |
| `layer2-sessions.md` | 5 sessions (main + 4 history): 40 loops, key loops for C1-C4/B1-B2, Phase 2 appends | 3 |
| `layer3-eval.md` | 30 eval rounds: key round specs R1-R6, abbreviated R7-R30 | 4 |
| `layer4-dynamic.md` | 4 updates: action JSON, content summaries, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Channel | Session Filename | UUID Placeholder | Updates |
|---|---|---|---|---|
| -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 王医生 (Co-author) | 微信 IM | `wangyisheng_im_{uuid}.jsonl` | `PLACEHOLDER_WANGYISHENG_IM_UUID` | initial + U2 append |
| 张主任 (Dept Director) | 微信 IM | `zhangzhuren_im_{uuid}.jsonl` | `PLACEHOLDER_ZHANGZHUREN_IM_UUID` | initial + U3 append |
| 审稿人 (Reviewer) | Email | `reviewer_email_{uuid}.jsonl` | `PLACEHOLDER_REVIEWER_EMAIL_UUID` | initial only |
| 学术委员会 (Committee) | Email | `committee_email_{uuid}.jsonl` | `PLACEHOLDER_COMMITTEE_EMAIL_UUID` | initial + U4 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible | Reversal |
|---|---|---|---|
| C1 | N three-way: paper 847 vs raw DB 912 vs co-author 847 (different IDs) -- version control | R2 | R2->R5 (U1: pipeline log resolves) |
| C2 | Complaint says "selective inclusion/duplicate publication" vs actual cause is dedup + different study periods | R3 | R3->R6 (U1: pipeline evidence refutes complaint) |
| C3 | Ethics/publication timeline (NON-CONFLICT: IRB before processing, all dates consistent) | R1 | None |
| C4 | 王医生 initially supportive then distances after committee involvement (career risk, not guilt) | R4/R7 | R7->R11 (U3: 张主任 provides career context) |
| B1 | Agent accepts complaint's "selective inclusion warrants investigation" framing | R3 | R6 (pipeline log shows dedup, not selection) |
| B2 | Agent interprets 王医生's distancing as potential complicity | R7/R8 | R11 (张主任 clarifies career motivation) |

---

## 5. Execution Steps

### Step 0: Generate 5 UUIDs

### Step 1: Create Workspace Files (layer1)
Target: `benchmark/data/calmb-new/workspaces/trace_i2/`

### Step 2: Write History Sessions (layer2)
Key constraints: B1 phrase in main session context. B2 phrase in 王医生 IM Phase 2 context.

### Step 3: Write Questions (layer3)
30 rounds. exec_check 9/30 = 30%.

### Step 4: Write Update Files (layer4)

### Step 5: Runtime Checks
- [ ] B1 phrase verbatim in main session / early assessment context
- [ ] B2 phrase verbatim in 王医生 IM Phase 2 context
- [ ] C1 sources independent (paper vs raw DB vs co-author version)
- [ ] C2 sources independent (complaint vs pipeline log)
- [ ] C3 NO contradictions in ethics/publication timeline
- [ ] C4 sources independent (王医生 initial vs later communication)
- [ ] Figures consistent: Paper N=847, Raw N=912, Duplicates 65, ID diffs 23
- [ ] Pipeline versions: V2.0 (2025-09-20, 王医生), V2.1 (2025-10-15, Lin Yi)
- [ ] Timeline: IRB 2025-08-01, extraction 2025-09-15, submission 2025-11-01, publication 2026-01-15, complaint 2026-03-16
- [ ] HIS migration date: 2025-07-15
