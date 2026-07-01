# trace_h3 -- CS Assignment Plagiarism Dispute: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_h3`

**Scenario:** Wang Ming (王明), a 17-year-old CS freshman at UESTC, has his CS101 programming assignment flagged by the MOSS plagiarism detection system with 95% similarity to another student (Chen Wei). Wang Ming's git commit history shows he started coding earlier, but Chen Wei claims Wang Ming copied his publicly posted GitHub code. The truth is both students independently referenced the same Stack Overflow answer (#48291037). The scenario spans 10 days with 4 history sessions and 4 dynamic updates, covering the progression from accusation through investigation to resolution.

**Core evaluation goals:**
1. Can the agent cross-reference the plagiarism report, both git commit histories, and session conversations to correctly assess the "who copied whom" question -- and recognize the common-source hypothesis? (MS)
2. Can the agent integrate new evidence (TA git comparison, SO answer, Chen Wei's admission, TA resolution) and revise prior assessments -- including correcting B1 and B2 bias phrases? (DU)
3. Does the agent maintain Wang Ming's preferred format (lists, casual naming, answer-first, examples, colloquial) after calibration? (P)
4. Can the agent synthesize evidence from code provenance (git), automated systems (MOSS), interpersonal conflict (Chen Wei IM), procedural authority (TA email), and policy interpretation (syllabus) to produce a correct comprehensive analysis? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_h3/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_h3/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_h3/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_h3/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (D-2 through D10), 5 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 3 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 5 sessions: main session + 4 history sessions (~57 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 25 eval rounds (R1--R25) covering 12 question types: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Zhang Hao (张昊) | Course TA | Email | `ta_zhanghao_email_{uuid}.jsonl` | `PLACEHOLDER_TA_EMAIL_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| Li Hao (李浩) | Best friend | WeChat IM | `friend_lihao_im_{uuid}.jsonl` | `PLACEHOLDER_LIHAO_IM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Chen Wei (陈伟) | Opponent student | WeChat IM | `opponent_chenwei_im_{uuid}.jsonl` | `PLACEHOLDER_CHENWEI_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| #CS101群 | Group: ~60 CS101 students | WeChat Group | `cs101_group_im_{uuid}.jsonl` | `PLACEHOLDER_CS101_GROUP_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |

**Notes:**
- Professor Liu (刘教授) does NOT have a dedicated session. His role is referenced in TA communications.
- All session dialogue is in Chinese; workspace system exports mix Chinese and English naturally.
- Chen Wei's narrative shifts from aggressive (Phase 1) to deflective (Phase 2) after the SO discovery.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Plagiarism accusation: 95% similarity -- is it plagiarism or common-source reference? MOSS report + Chen Wei claims "you copied me" vs git timeline + SO answer shows common source | R1 (partial -- report + git visible) | R1->R6 (full resolution via SO discovery in Update 2) |
| C2 | Git timeline: Wang Ming commits 30h earlier vs Chen Wei claims "I posted on GitHub first" | R2 (both timelines visible) | R2->R6 (TA confirms timeline + SO makes "who first" moot) |
| C3 | Stack Overflow common source: both referenced SO #48291037 (NON-CONFLICT -- resolves C1 and C2) | R5 onwards (after Update 2) | None (NON-CONFLICT -- this IS the resolution) |
| C4 | Course policy: "zero tolerance" text vs TA's "first offense = warning" resolution | R8 (policy text visible initially; resolution after Update 4) | R8->R11 (TA resolution contradicts literal policy reading) |
| B1 | Chen Wei IM Phase 1, Loop 5: Agent concludes "timeline strongly suggests Chen Wei referenced Wang Ming's work" without considering common-source hypothesis | R6 (corrected by SO discovery) | Explicit reversal when SO answer invalidates the "one copied the other" frame |
| B2 | TA Email Phase 1, Loop 3: Agent accepts "zero tolerance = zero grade" without considering TA discretion or policy nuance | R11 (corrected by TA resolution email) | Explicit reversal when TA issues warning, not zero |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 5 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 5 times for: MAIN, TA_EMAIL, LIHAO_IM, CHENWEI_IM, CS101_GROUP
```

Record all 5 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (plagiarism accusation), C2 (git timeline claim), C3 (SO common source -- non-conflict), C4 (policy vs enforcement)
- Biases: B1 (Chen Wei IM Loop 5), B2 (TA Email Loop 3)
- Updates: U1 on R5, U2 on R6, U3 on R11, U4 on R21
- 4 history sessions (all with Phase 2 appends) + 1 main session
- Wang Ming P1-P5 preferences injected in 4 stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_h3/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 5 initial scenario files (including SO placeholder), then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 4 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in opponent_chenwei_im Loop 5 agent reply. B2 exact phrase must appear in ta_zhanghao_email Loop 3 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_h3/questions.json` with 25 rounds.

Wang Ming's P1-P5 preferences are calibrated in R1 (lists), R2 (answer-first), main session messages (examples, colloquial, casual naming). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write update files in `updates/` subfolder:
- Update 1: ta-git-comparison-notes.md
- Update 2: stackoverflow-answer-screenshot.md (full), PLACEHOLDER_LIHAO_IM_UUID.jsonl append
- Update 3: PLACEHOLDER_CHENWEI_IM_UUID.jsonl append
- Update 4: ta-resolution-email.md, PLACEHOLDER_TA_EMAIL_UUID.jsonl append, PLACEHOLDER_CS101_GROUP_UUID.jsonl append

Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in opponent_chenwei_im Loop 5
- [ ] B2 phrase appears verbatim in ta_zhanghao_email Loop 3
- [ ] C1 sources are independent (MOSS report vs git histories + SO answer)
- [ ] C2 sources are independent (Chen Wei IM claim vs git histories + TA comparison)
- [ ] C3 has NO contradictions -- SO answer, git histories, TA notes, Li Hao discovery, Chen Wei admission all consistent
- [ ] C4 sources are independent (course-syllabus-integrity-policy.md Section 4.2 vs ta-resolution-email.md + TA email)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Wang Ming P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 20-40% of total rounds (8/25 = 32%)
- [ ] All timestamps internally consistent (D-2 14:22, D-1 20:00, D1 22:30, D1 23:50, D2 01:15, D3 09:00, etc.)
- [ ] Dialogue in Chinese; workspace mixes Chinese/English naturally
- [ ] SO answer: #48291037, 847 upvotes, 2 years old -- consistent across all references
