# trace_g5 -- Recruitment Agency Invoice Fraud: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_g5`

**Scenario:** A headhunter consultant (Zhang Lin, 张琳) from RuiCai Agency (锐才猎头) billed for 8 candidates but only 5 were legitimately sourced through the agency. Three candidates (王建国, 李小红, 赵明) applied directly through the company website but were falsely included in the agency's invoice. Additionally, the finance director (Zhao Lin, 赵琳) approved the ¥386,000 invoice after emailing Chen Jing for confirmation -- but Chen Jing never received the email due to a spam filter issue during a company mail migration. The investigation reveals: (1) CRM auto-tags show the 3 candidates as direct applicants with timestamps predating the agency's referral email; (2) the invoice also falsely claims 2 of the 3 candidates were "successfully onboarded" when they were never hired; (3) a peer company experienced identical tactics from RuiCai; (4) the company's informal invoice approval process lacks a confirmation receipt mechanism.

**Core evaluation goals:**
1. Can the agent cross-reference candidate source attributions across CRM, agency invoices, candidate emails, and bank records to identify where each source agrees or conflicts? (MS)
2. Can the agent integrate new evidence (Zhang Lin's defense, spam filter discovery, external pattern evidence, VP escalation) and revise prior assessments -- including correcting B1 (contractual defense trust) and B2 (approval process normalization)? (DU)
3. Does the agent maintain Chen Jing's preferred format (bullet points + headings, executive summary first, qualitative + quantitative, professional + warm) after calibration? (P)
4. Can the agent synthesize financial data (¥386K invoice, ¥136K fraud, fee calculations), operational evidence (CRM timestamps, email chronology), and process analysis (approval gap, prevention measures) to produce a comprehensive investigation report? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_g5/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_g5/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_g5/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_g5/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (2026-01-15 to 2026-03-08), 5 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 5 sessions: main session + 4 history sessions (~42 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (R1--R30) spread across 12 question types: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Zhang Lin (张琳) | Headhunter Consultant | 工作邮箱 | `vendor_zhanglin_email_{uuid}.jsonl` | `PLACEHOLDER_ZHANGLIN_EMAIL_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Liu Yang (刘洋) | Recruitment Specialist | 飞书 IM | `team_liuyang_im_{uuid}.jsonl` | `PLACEHOLDER_LIUYANG_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Zhao Lin (赵琳) | Finance Director | 工作邮箱 | `finance_zhaolin_email_{uuid}.jsonl` | `PLACEHOLDER_ZHAOLIN_EMAIL_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| #HR内部群 | HR Team Group | 飞书群 | `hr_group_im_{uuid}.jsonl` | `PLACEHOLDER_HR_GROUP_IM_UUID` | initial (Phase 1 only) |

**Notes:**
- Zhang Wei (张薇, HR VP) does NOT have a dedicated session. Her directives are captured in vp-escalation-summary.md (Update 4).
- 3 of 4 history sessions receive Phase 2 appends through updates. #HR内部群 has no Phase 2 append.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Candidate source attribution: CRM auto-tags show 3 candidates as "官网自主投递" (direct application) vs invoice/Zhang Lin claims all 8 as "锐才推荐" (agency referral). CRM timestamps predate agency email by 5-7 days. | R2 (CRM vs invoice discrepancy visible) | R2->R6 (full resolution after Update 1: timeline debunks "verbal recommendation" defense) |
| C2 | Candidate count: Invoice lists 8 "successfully placed" candidates vs CRM tracks only 5 from agency; additionally, 2 of the 8 (李小红, 赵明) were never hired. | R3 (count discrepancy visible) | R3->R7 (full financial impact after Update 2: ¥136,000 overbilled) |
| C3 | Payment timeline (NON-CONFLICT): Invoice submitted 2026-02-20, payment 2026-02-25, amount ¥386,000 -- all consistent across bank records, invoice, and budget tracker. Timing is not the issue; amount/eligibility is. | R1 (persistent synthesis) | None |
| C4 | Approval gap: Finance director's approval log says "HR已确认" vs Chen Jing never received the confirmation email. Root cause: company mail migration (2026-02-21) caused spam filter misclassification. | R4 (approval gap visible) | R4->R8 (full resolution after Update 2: spam filter + mail migration root cause; systemic process gap identified) |
| B1 | Zhang Lin Email Phase 1, Loop 4: Agent accepts "talent pool" / "contractual referral definition" defense before checking timeline evidence | R5 (bias visible from Zhang Lin Email) | Full reversal when CRM timestamps + email chronology debunk the defense (Update 1) |
| B2 | Zhao Lin Email Phase 1, Loop 3: Agent normalizes approval gap as "standard vendor payment workflow" rather than identifying it as a control failure | R8 (bias visible from Zhao Lin Email) | Full reversal when spam filter discovery + fraud evidence shows the "standard" process enabled ¥136K in fraudulent payments (Update 2) |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 5 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 5 times for: MAIN, ZHANGLIN_EMAIL, LIUYANG_IM, ZHAOLIN_EMAIL, HR_GROUP_IM
```

Record all 5 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (source attribution), C2 (candidate count), C3 (payment timeline -- non-conflict), C4 (approval gap)
- Biases: B1 (Zhang Lin Email Loop 4), B2 (Zhao Lin Email Loop 3)
- Updates: U1 on R6, U2 on R8, U3 on R11, U4 on R21
- 4 history sessions (3 with Phase 2 appends, 1 group chat without append) + 1 main session
- Chen Jing P1-P5 preferences injected in 4 stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_g5/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 5 initial scenario files, then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 4 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in vendor_zhanglin_email Loop 4 agent reply. B2 exact phrase must appear in finance_zhaolin_email Loop 3 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_g5/questions.json` with 30 rounds.

Chen Jing's P1-P5 preferences are calibrated in R1 (bullet points + headings), R2 (qualitative + quantitative), main session messages (executive summary, professional + warm). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write 4 update workspace files and 3 session append files in `updates/` subfolder. Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in vendor_zhanglin_email Loop 4
- [ ] B2 phrase appears verbatim in finance_zhaolin_email Loop 3
- [ ] C1 sources are independent (crm-candidate-pipeline.md vs agency-invoices.md vs candidate-application-emails.md vs zhang-lin-defense-email.md)
- [ ] C2 sources are independent (invoice count vs CRM count vs budget variance vs pattern evidence)
- [ ] C3 has NO contradictions -- payment date, amount, and reference consistent across all sources
- [ ] C4 sources show "HR已确认" in bank records vs blank sign-off in budget tracker vs spam folder evidence
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Chen Jing P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 20-40% of total rounds (9/30 = 30%)
- [ ] Financial figures consistent: Invoice ¥386,000 = ¥250,000 legit + ¥136,000 fraud. Individual fees: 陈磊 52K, 黄丽 48K, 周杰 56K, 马超 44K, 吴涛 50K, 王建国 52K, 李小红 42K, 赵明 42K. Fee rate 20%.
- [ ] Timeline consistent: postings 01-15, direct apps 01-18 to 01-20, agency email 01-25, interviews 02-01 to 02-15, invoice 02-20, approval email 02-22, payment 02-25, discovery 03-01, confrontation 03-05, spam discovery 03-06, pattern evidence 03-07, VP escalation 03-08.
