# trace_f6 -- Fund Due Diligence Sharpe Inflation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_f6`

**Scenario:** 赵磊's close friend 小周 prepared a due-diligence package for PE fund manager 刘总 that inflates Strategy V3's Sharpe ratio from actual 1.3 to 2.1 by omitting 3 months of drawdown data. Meeting notes (drafted by 小周) report Sharpe 2.1, 刘总's email misremembers it as 1.8, and actual code tracking shows 1.3. 小周 defends the inflation as "methodology choice" while the spreadsheet formula reveals 3-month omission. Meanwhile, 刘总's "verbal commitment" to invest is contradicted by his assistant's official email saying they are "still evaluating." The scenario spans 2 weeks with 3 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference Sharpe ratios across multiple sources (DD package, meeting notes, email, actual returns, brokerage records) to identify the three-way discrepancy and its cause? (MS)
2. Can the agent integrate new evidence (independent calculation, spreadsheet formula, brokerage confirmation, assistant email) and revise prior assessments -- including correcting B1 (methodology acceptance) and B2 (verbal commitment) bias phrases? (DU)
3. Does the agent maintain 赵磊's preferred format (code/table format, timestamp naming, evidence-first, quantitative with CI, concise) after calibration? (P)
4. Can the agent synthesize financial, interpersonal, and compliance perspectives to produce an accurate assessment with actionable recommendations? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_f6/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_f6/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_f6/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_f6/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W2), 5 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 4 sessions: main session + 3 history sessions (~38 total loops + Phase 2 appends), detailed loop designs, noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (R1--R30) spread across 12 question types: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 小周 (Xiao Zhou) | Quant Researcher | 微信 IM | `xiaozhou_im_{uuid}.jsonl` | `PLACEHOLDER_XIAOZHOU_IM_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| 刘总 (Liu Zong) | PE Fund Manager | Email | `liuzong_email_{uuid}.jsonl` | `PLACEHOLDER_LIUZONG_EMAIL_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| 陈经理 (Chen Jingli) | Broker Client Manager | 微信 IM | `chenjingli_im_{uuid}.jsonl` | `PLACEHOLDER_CHENJINGLI_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Sharpe three-way discrepancy: DD package 2.1 vs 刘总 email 1.8 vs actual 1.3 (three sources, each different) | R2 (partial -- 2.1 vs 1.8 visible) | R2->R5 (full reversal after Update 1: actual 1.3 revealed) |
| C2 | 小周 says "methodology choice" vs spreadsheet formula shows 3-month omission; methodology ~0.1, omission ~0.8 | R3 (小周's explanation visible) | R3->R6 (full reversal after spreadsheet formula analysis) |
| C3 | Meeting timeline: date, time, attendees (NON-CONFLICT -- calendar, CRM, meeting notes, email all agree) | R1 (persistent synthesis) | None |
| C4 | 刘总 "verbal commitment" vs 张秘书 "still evaluating, no commitments" | R4 (verbal commitment visible) | R4->R8 (full reversal after Update 2: 张秘书 email) |
| B1 | 小周 IM Phase 1, Loop 5: Agent accepts "methodology choice" as sufficient explanation for Sharpe gap | R5 (corrected by independent calculation) | Full reversal when spreadsheet formula + quantified decomposition shows omission is primary driver |
| B2 | Main session / 小周 IM Phase 1, Loop 4: Agent treats 刘总's verbal enthusiasm as near-commitment | R8 (corrected by 张秘书 email) | Full reversal when official firm communication contradicts verbal statement |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 4 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 4 times for: MAIN, XIAOZHOU_IM, LIUZONG_EMAIL, CHENJINGLI_IM
```

**Checklist:**
- Contradictions: C1 (Sharpe three-way), C2 (methodology vs omission), C3 (timeline non-conflict), C4 (verbal vs official)
- Biases: B1 (小周 IM Loop 5), B2 (main/小周 IM Loop 4)
- Updates: U1 on R5, U2 on R7, U3 on R11, U4 on R21
- 3 history sessions (all with Phase 2 appends) + 1 main session
- 赵磊 P1-P5 preferences injected via calibration messages

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_f6/`

### Step 2: Write History Sessions (layer2)

Write 3 history session files. Phase 1 content for all sessions. Phase 2 appends in `updates/`.

Key constraint: B1 exact phrase in xiaozhou_im Loop 5. B2 exact phrase in xiaozhou_im Loop 4 / main session.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_f6/questions.json` with 30 rounds.

### Step 4: Write Update Source Files (layer4)

Write update workspace files and session append files in `updates/`.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in xiaozhou_im Loop 5
- [ ] B2 phrase appears verbatim in xiaozhou_im Loop 4 / main session
- [ ] C1 sources independent (DD package vs email vs actual returns)
- [ ] C2 sources independent (小周 IM explanation vs spreadsheet formula)
- [ ] C3 has NO contradictions -- all timeline sources consistent
- [ ] C4 sources independent (meeting notes/IM vs 张秘书 email)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] 赵磊 P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds 20-40% (9/30 = 30%)
- [ ] Factual figures consistent: Sharpe (2.1/1.8/1.3), omitted months (Jul-Sep 2025), returns (-4.2%/-3.1%/-2.8%), annualized (18% vs 31%), max DD (14% vs 8%), methodology ~0.1 vs omission ~0.8
