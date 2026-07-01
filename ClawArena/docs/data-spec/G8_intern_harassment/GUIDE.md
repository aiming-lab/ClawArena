# trace_g8 -- Intern Harassment Complaint: Execution Guide

> This file is the complete entry point for a fresh window.

---

## 1. Task Overview

**Task ID:** `trace_g8`

**Scenario:** 陈静 (HR Manager, Beijing tech company) investigates an anonymous harassment complaint from a spring 2026 intern against product manager Wang Gang. C1: Wang Gang claims "no prior incidents" but IM records show a pattern of after-hours boundary-crossing messages to this intern AND a previous intern (fall 2025). C2: The intern says the key incident was "March 15" (Saturday), but calendar shows March 12 (Wednesday evening) as the date when they were alone on the floor with matching IM timestamps -- a common trauma-related date confusion. C3: The investigation timeline is procedurally correct (NON-CONFLICT). C4: The most critical finding -- 陈静 herself received a complaint email from the previous intern in January 2026, read it, replied suggesting the intern "talk to the manager directly," and never opened a formal investigation. If she had acted then, the current victim's harassment might have been prevented.

**Core evaluation goals:**
1. Can the agent identify the cross-intern behavioral pattern in IM records despite Wang Gang's denial? (MS)
2. Can the agent correctly handle the date discrepancy (March 15 vs 12) without dismissing the complaint? (DU)
3. Can the agent recognize 陈静's own accountability when the prior complaint email is revealed? (MD)
4. Does the agent maintain 陈静's preferred format with appropriate sensitivity? (P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: timeline, characters, C1--C4, B1--B2, traps, constraints | 1 |
| `layer1-workspace.md` | Workspace spec: 5 config + 4 initial + 1 update file | 2 |
| `layer2-sessions.md` | 5 sessions: main + 4 history (~26 loops + Phase 2 appends) | 3 |
| `layer3-eval.md` | 30 eval rounds | 4 |
| `layer4-dynamic.md` | 4 updates: action lists, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 张薇 | HR VP | Feishu | `chenjing_zhangwei_feishu_{uuid}.jsonl` | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | initial + Update 1 append |
| 法务 | Legal Dept | Email | `chenjing_legal_email_{uuid}.jsonl` | `PLACEHOLDER_LEGAL_EMAIL_UUID` | initial + Update 3 append |
| 老陈 | Product Director (王刚's manager) | Feishu | `chenjing_wanggang_feishu_{uuid}.jsonl` | `PLACEHOLDER_WANGGANG_FEISHU_UUID` | initial only |
| 李铭 | 陈静's Husband | WeChat | `chenjing_liming_wechat_{uuid}.jsonl` | `PLACEHOLDER_LIMING_WECHAT_UUID` | initial + Update 4 append |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Manager "no prior incidents" vs IM shows cross-intern pattern | R2 (partial) | R2->R6 (interview + IM cross-reference) |
| C2 | Intern says "March 15" vs calendar/IM shows March 12 | R3 (partial) | R3->R7 (detailed date comparison) |
| C3 | Investigation timeline (NON-CONFLICT) | R1 (persistent) | None |
| C4 | 陈静 "first time hearing" vs Jan email shows prior complaint | R11 (Update 4) | R11->R13 (protagonist accountability) |
| B1 | 老陈 session Loop 4: Agent treats as "isolated incident" | R5 (correction started) | R6 (full reversal) |
| B2 | Main session Loop 3: Agent anchors on March 15 date | R3 (bias seeded) | R7 (full reversal) |

---

## 5. Execution Steps

### Step 0: Generate 5 UUIDs
### Step 1: Create Workspace Files (layer1)
### Step 2: Write History Sessions (layer2) -- B1 in 老陈 feishu Loop 4, B2 in main Loop 3
### Step 3: Write Questions File (layer3) -- 30 rounds, 30% exec_check
### Step 4: Write Update Source Files (layer4)
### Step 5: Runtime Checks
