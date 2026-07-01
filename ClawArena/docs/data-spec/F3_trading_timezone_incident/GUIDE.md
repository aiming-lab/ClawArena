# trace_f3 -- Trading System Timezone Incident: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_f3`

**Scenario:** 赵磊's automated trading system executed a trade order during A-share midday break (11:30-13:00 CST) due to a timezone bug in PR #447. The bug: `datetime.utcnow() + timedelta(hours=8)` on line 127 does not handle DST. CI reported "all tests passed" but tests mocked a non-DST date. 小周 reviewed the PR with "LGTM" but missed the anti-pattern. 赵磊's own 3-month-old alert silence rule suppressed timezone warnings for 7 days before the violation. Compliance claims "first offense" but a Dec 2025 email shows a prior timezone warning. Trade execution logs reveal 4 additional near-miss trades during the post-DST week.

**Core evaluation goals:**
1. Can the agent cross-reference CI "all tests passed" with production error logs to identify the false confidence from inadequate test coverage? (MS)
2. Can the agent integrate server diagnostics, 小周's admission, and near-miss patterns to revise prior assessments? (DU)
3. Does the agent maintain 赵磊's preferred format? (P)
4. Can the agent synthesize technical (code bug), operational (alert suppression), review (小周's miss), and compliance (first offense) dimensions? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_f3/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_f3/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_f3/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_f3/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W2), 4 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config + 6 scenario files + 2 update-added files, timing table, noise design | 2 |
| `layer2-sessions.md` | All 5 sessions: main + 4 history sessions, loop designs for key loops (C1--C4, B1--B2), Phase 2 appends | 3 |
| `layer3-eval.md` | 30 eval rounds (r1--r30): option tables, answer keys, distractor logic, cross-round reversals | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 小周 | Institutional Quant Researcher | WeChat DM | `zhaolei_xiaozhou_wechat_{uuid}.jsonl` | `PLACEHOLDER_XIAOZHOU_WECHAT_UUID` | initial + Update 1 append |
| 张审核 | Compliance Officer | Email DM | `zhaolei_zhangshenhe_email_{uuid}.jsonl` | `PLACEHOLDER_ZHANGSHENHE_EMAIL_UUID` | initial + Update 2 append |
| 客服小刘 | Cloud Service Support | Ticket | `zhaolei_kefu_ticket_{uuid}.jsonl` | `PLACEHOLDER_KEFU_TICKET_UUID` | initial + Update 1 append |
| #策略群 | Group: 赵磊, 小周, others | WeChat Group | `strategy_group_{uuid}.jsonl` | `PLACEHOLDER_STRATEGY_GROUP_UUID` | initial + Update 4 append |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | CI "all tests passed" vs production timezone failure (test coverage gap) | R1 | R1->R5 (server diagnostic confirms code-level issue) |
| C2 | 小周 "LGTM" vs visible timezone anti-pattern on line 127 | R2 | R2->R6 (小周's candid admission) |
| C3 | Alert suppression timeline (NON-CONFLICT -- all sources consistent) | R1 onwards | None |
| C4 | Compliance "first offense" vs Dec 2025 prior warning | R8 | R8->R11 (near-miss pattern amplifies) |
| B1 | #策略群 Loop 8: Agent trusts CI "all passed" as sufficient validation | R5 (corrected by server diagnostic) | Explicit correction in group Phase 2 |
| B2 | 小周 DM Loop 4: Agent accepts "deliberate scope decision" for LGTM | R6 (corrected by 小周's admission) | Explicit correction in DM Phase 2 |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design
Generate 5 UUIDs for: MAIN, XIAOZHOU_WECHAT, ZHANGSHENHE_EMAIL, KEFU_TICKET, STRATEGY_GROUP.

### Step 1: Create Workspace Files (layer1)
Target: `benchmark/data/calmb-new/workspaces/trace_f3/`

### Step 2: Write History Sessions (layer2)
B1 phrase in strategy_group Loop 8. B2 phrase in zhaolei_xiaozhou_wechat Loop 4.

### Step 3: Write Questions File (layer3)
30 rounds. exec_check = 9 rounds (30%).

### Step 4: Write Update Source Files (layer4)

### Step 5: Runtime Checks
- [ ] B1 phrase verbatim in strategy_group Loop 8
- [ ] B2 phrase verbatim in zhaolei_xiaozhou_wechat Loop 4
- [ ] C1 sources independent (ci-build-report.md vs production-error-log.md + server-diagnostic-report.md)
- [ ] C2 sources in same file (git-pr-447-diff.md: review + diff)
- [ ] C3 NO contradictions (alert-rules-config.md + production-error-log.md + compliance-notice.md consistent)
- [ ] C4 sources in same file (compliance-notice.md: Dec entry vs Mar "first offense")
- [ ] All timestamps consistent: DST 2026-03-08, PR merge 2026-03-10, violation 2026-03-16T11:30:05 CST
- [ ] Near-miss trades: Mar 10 11:29:47, Mar 11 11:29:53
- [ ] exec_check rounds = 30% of total
