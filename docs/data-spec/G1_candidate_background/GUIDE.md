# trace_g1 -- Candidate Background Check Discrepancy: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_g1`

**Scenario:** A senior backend engineer candidate (Wang Hao) has a resume with two material discrepancies: (1) claims to have led a team of 12 when the reference says 4, and (2) claims continuous employment when GitHub and LinkedIn both show a 6-month gap. The CTO (Li Qiang) is pushing for an expedited hire driven by board meeting optics, while the tech lead (Huang Lei) independently corroborates the discrepancies and recommends hiring at a lower level. The HR VP (Zhang Wei) supports Chen Jing's due diligence. The scenario spans 2 weeks with 4 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference the candidate's resume claims with independent sources (reference email, GitHub data, interview feedback, LinkedIn) to identify where the resume is materially misleading? (MS)
2. Can the agent integrate new evidence (Huang Lei's interview notes, LinkedIn data, detailed assessment, CTO response) and revise prior assessments -- including correcting B1 (CTO deference) and B2 (gap minimization) bias phrases? (DU)
3. Does the agent maintain Chen Jing's preferred format (bullet summaries, Chinese naming, exec summary first, quali+quanti, professional+warm) after calibration? (P)
4. Can the agent synthesize technical (Huang Lei), process (Zhang Wei), recruiter (Liu Yang), and authority (CTO) perspectives to produce an accurate comprehensive assessment with a nuanced recommendation? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_g1/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_g1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_g1/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_g1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W2), 7 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 5 sessions: main session + 4 history sessions (~57 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (R1--R30) spread across 12 question types: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Liu Yang (刘洋) | Recruiter | 企业微信 IM | `recruiter_liuyang_im_{uuid}.jsonl` | `PLACEHOLDER_LIUYANG_IM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Li Qiang (李强) | CTO | Feishu DM | `cto_liqiang_feishu_{uuid}.jsonl` | `PLACEHOLDER_LIQIANG_FEISHU_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| Huang Lei (黄磊) | Tech Team Lead | Email | `tl_huanglei_email_{uuid}.jsonl` | `PLACEHOLDER_HUANGLEI_EMAIL_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Zhang Wei (张薇) | HR VP | Feishu DM | `vp_zhangwei_feishu_{uuid}.jsonl` | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |

**Notes:**
- Wang Hao (candidate) does NOT have a dedicated session. His evidence is delivered through workspace documents (resume, GitHub, LinkedIn) and other characters' reports.
- Liu Wei (reference) does NOT have a dedicated session. His input is in reference-check-emails.md.
- All 4 history sessions receive Phase 2 appends through updates.
- CTO trust in the "hire fast" narrative erodes as evidence accumulates across updates.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Team-size inflation: resume "led team of 12" vs reference "managed about 4" vs interview "about 4-5 direct reports" (triple-source) | R2 (partial -- resume vs reference visible) | R2->R5 (full reversal after Update 1: Huang Lei interview feedback) |
| C2 | CTO pressure vs due diligence: CTO "hire immediately" (board-driven) vs background check findings + HR VP support + Huang Lei workload assessment | R3 (both positions visible) | R3->R8 (full reversal after Updates 2+4: Zhang Wei support + CTO "everyone embellishes") |
| C3 | Interview and evaluation timeline: when each step occurred (NON-CONFLICT -- cross-source synthesis across CTO email, recruiter IM, email thread, workspace files) | R1 (persistent synthesis) | None |
| C4 | Employment gap: resume claims continuous employment vs GitHub shows 6-month zero activity vs LinkedIn shows departure/return dates (dual-source) | R6 (partial -- GitHub gap visible) | R6->R9 (full reversal after Update 2: LinkedIn confirmation) |
| B1 | CTO Feishu DM Phase 1, Loop 5: Agent defers to CTO urgency and recommends parallel offer process despite emerging background check concerns | R5 (corrected by Huang Lei evidence) | Full reversal when Zhang Wei + CTO "everyone embellishes" reveal true dynamics |
| B2 | Liu Yang IM Phase 1, Loop 6: Agent minimizes GitHub employment gap as "possibly private repository work" despite resume claiming active open-source contributions | R7 (corrected by LinkedIn evidence) | Full reversal when LinkedIn shows actual employment departure |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 5 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 5 times for: MAIN, LIUYANG_IM, LIQIANG_FEISHU, HUANGLEI_EMAIL, ZHANGWEI_FEISHU
```

Record all 5 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (team-size inflation), C2 (CTO pressure vs due diligence), C3 (interview timeline -- non-conflict), C4 (employment gap)
- Biases: B1 (CTO Feishu DM Loop 5), B2 (Liu Yang IM Loop 6)
- Updates: U1 on R5, U2 on R7, U3 on R11, U4 on R21
- 4 history sessions (all with Phase 2 appends) + 1 main session
- Chen Jing P1-P5 preferences injected in 4 stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_g1/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 5 initial scenario files, then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 4 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in cto_liqiang_feishu Loop 5 agent reply. B2 exact phrase must appear in recruiter_liuyang_im Loop 6 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_g1/questions.json` with 30 rounds.

Chen Jing's P1-P5 preferences are calibrated in R1 (bullet points + headings), R2 (exec summary first), main session messages (quali+quanti, professional+warm). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write 4 update workspace files and 4 session append files in `updates/` subfolder. Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in cto_liqiang_feishu Loop 5
- [ ] B2 phrase appears verbatim in recruiter_liuyang_im Loop 6
- [ ] C1 sources are independent (resume vs reference-check-emails.md vs interview-feedback-forms.md Huang Lei notes)
- [ ] C2 sources are independent (CTO email/Feishu vs Zhang Wei Feishu + Huang Lei email workload assessment)
- [ ] C3 has NO contradictions -- all sources consistent for timeline synthesis
- [ ] C4 sources are independent (candidate-resume.md vs github-contribution-export.md vs linkedin-profile-export.md)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Chen Jing P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 20-40% of total rounds (9/30 = 30%)
- [ ] Factual figures consistent: team size (12 vs 4), gap (6 months, 2023-06 to 2023-12), technical scores (4.0-4.3/5.0), leadership score (2.8/5.0), board meeting (3 weeks from W1D1), company (~200 employees)
