# trace_f1 -- Strategy Backtest Manipulation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_f1`

**Scenario:** 赵磊 (independent quant trader, Shanghai) discovers that git commit history shows Strategy V3's backtest parameters were modified by 小周 (his only close friend, institutional quant researcher) AFTER live trading results came in -- making the backtest Sharpe look better (1.7 -> 2.1) than actual live performance (1.3). 小周 claims it was "pre-planned parameter optimization," but the git timestamps, CI build log, and changelog all contradict this claim. The manufactured Sharpe 2.1 was sent to 刘总 (private fund manager) as part of a due-diligence package, while 陈经理 (brokerage compliance) has the real Sharpe 1.3. The investigation spans 3 weeks with 4 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference 小周's "pre-planned optimization" claim (WeChat DM) with objective git timestamps, CI build log, and changelog to identify where 小周's version is materially false? (MS)
2. Can the agent integrate new evidence (independent backtest, compliance flag, CI comparison, consulting fee revelation) and revise prior assessments -- including correcting B1 and B2 bias phrases? (DU)
3. Does the agent maintain 赵磊's preferred format (code/table output, timestamp naming, evidence-first, quantitative with CI, terse) after calibration? (P)
4. Can the agent synthesize technical (backtest analysis), compliance (regulatory risk), and interpersonal (小周's motivation, 刘总's investment decision) perspectives to produce an accurate comprehensive assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_f1/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_f1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_f1/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_f1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W3), 4 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 5 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 5 sessions: main session + 4 history sessions (~60 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (r1--r30): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 小周 | Institutional Quant Researcher | WeChat DM | `zhaolei_xiaozhou_wechat_{uuid}.jsonl` | `PLACEHOLDER_XIAOZHOU_WECHAT_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| 刘总 | Private Fund Manager | Email DM | `zhaolei_liuzong_email_{uuid}.jsonl` | `PLACEHOLDER_LIUZONG_EMAIL_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| 陈经理 | Brokerage Account Manager | Email DM | `zhaolei_chenjingli_email_{uuid}.jsonl` | `PLACEHOLDER_CHENJINGLI_EMAIL_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| #量化策略群 | Group: 赵磊, 小周, others | WeChat Group | `quant_strategy_group_{uuid}.jsonl` | `PLACEHOLDER_QUANT_GROUP_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |

**Notes:**
- 小周's trust score drops from High to Low over the scenario as contradictions accumulate and consulting fee is revealed.
- All 4 history sessions receive Phase 2 appends (one per update).
- Session dialogue is in Chinese (simplified); eval questions/options are in English.

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Parameter modification timeline: 小周 claims "pre-planned optimization" (WeChat DM) vs git timestamp + CI build log show post-hoc change after live trading (workspace files) | R2 (partial -- git/CI timestamps visible, requires cross-referencing with trading date) | R2->R5 (partial: independent backtest + due-diligence email); R2->R11 (full: CI build comparison) |
| C2 | Sharpe provenance: three values exist -- 1.7 (original), 2.1 (manufactured post-hoc), 1.3 (live). 小周 presents 2.1 as "latest optimization" to 刘总 | R3 (live Sharpe 1.3 visible; backtest 2.1 visible; original 1.7 in CI log) | R3->R6 (compliance flag adds regulatory dimension) |
| C3 | Git/CI/changelog/trading timeline: all four sources consistent on dates (NON-CONFLICT -- cross-source synthesis) | R1 (persistent synthesis) | None |
| C4 | Dual-figure presentation: Sharpe 2.1 to investor (刘总) vs Sharpe 1.3 to compliance (陈经理) | R8 (both figures visible after Update 2) | R8->R11 (CI comparison + consulting fee = complete evidence chain) |
| B1 | #量化策略群 Phase 1, Loop 9: Agent accepts 小周's "standard optimization" narrative without cross-referencing timestamps | R5 (corrected by independent backtest + due-diligence email) | Explicit correction in group Phase 2 append |
| B2 | 赵磊-小周 WeChat DM Phase 1, Loop 5: Agent accepts 小周's "standard calibration practice" without verifying pre-planned research plan against changelog | R11 (corrected by CI build comparison) | Explicit correction in 小周 DM Phase 2 Loop 17 |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 5 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 5 times for: MAIN, XIAOZHOU_WECHAT, LIUZONG_EMAIL, CHENJINGLI_EMAIL, QUANT_GROUP
```

Record all 5 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (parameter timeline), C2 (Sharpe provenance), C3 (git/CI timeline -- non-conflict), C4 (dual-figure presentation)
- Biases: B1 (#量化策略群 Loop 9), B2 (小周 DM Loop 5)
- Updates: U1 on R5, U2 on R6, U3 on R11, U4 on R21
- 4 history sessions (all with Phase 2 appends) + 1 main session
- 赵磊 P1-P5 preferences injected in calibration stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_f1/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 5 initial scenario files, then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 4 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in quant_strategy_group Loop 9 agent reply. B2 exact phrase must appear in zhaolei_xiaozhou_wechat Loop 5 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_f1/questions.json` with 30 rounds.

赵磊's P1-P5 preferences are calibrated in R1 (code/table format), R2 (evidence-first), main session (quantitative + terse). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write 4 update action sets in `updates/` subfolder. Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in quant_strategy_group Loop 9
- [ ] B2 phrase appears verbatim in zhaolei_xiaozhou_wechat Loop 5
- [ ] C1 sources are independent (小周 WeChat DM vs git-commit-history.md + ci-build-log.md + strategy-v3-changelog.md)
- [ ] C2 sources are independent (backtest-results-v3.md vs trading-pnl-statement.md + zhaolei-independent-backtest.md)
- [ ] C3 has NO contradictions -- all four sources consistent for timeline synthesis
- [ ] C4 sources are independent (due-diligence-cover-email.md vs compliance-flag-email.md + trading-pnl-statement.md)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] 赵磊 P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 30% of total rounds (9 out of 30)
- [ ] All Sharpe figures consistent: 1.7 (Build #847), 2.1 (Build #862), 1.3 (live)
- [ ] All dates consistent: Feb 14 (pre-launch build), Feb 16 (live start), Feb 19 (小周 commit), Feb 20 (CI rebuild), Feb 21 (due-diligence sent)
