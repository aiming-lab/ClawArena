# trace_g7 -- Employee Wellness Benefit Misuse (SPA Reimbursement): Execution Guide

> This file is the complete entry point for a fresh window.

---

## 1. Task Overview

**Task ID:** `trace_g7`

**Scenario:** 陈静 (HR Manager, Beijing tech company) discovers that 5 employees across 3 departments submitted wellness benefit claims labeled "gym membership" (¥28,500 total) but the vendor invoices are from "悦享水疗会所" (a high-end SPA). The company wellness policy (section 2.1) explicitly lists reimbursable items (gym, equipment, checkups, counseling) and section 3.2 states unlisted items cannot be reimbursed -- SPA is not listed. Finance Director 赵琳 claims "we follow policy" and mentions "flexible interpretation," but there is no written basis for this. Employee 小李 says VP 张薇 orally approved SPA as part of "employee wellbeing" at a department meeting, but no meeting minutes or email confirm this. VP 张薇 later acknowledges "maybe mentioning wellbeing in general" but denies specifically authorizing SPA reimbursement.

**Core evaluation goals:**
1. Can the agent identify the mismatch between expense claim categories ("gym") and actual invoices ("SPA"), and recognize the policy explicitly excludes unlisted items? (MS)
2. Can the agent trace the "authorization" chain from employee claim -> finance "flexibility" -> VP oral comment, and assess credibility at each level? (DU)
3. Does the agent maintain 陈静's preferred format (bullet points, executive summary, warmth)? (P)
4. Can the agent distinguish between policy gaps, process failures, and employee misconduct? (MS+DU+P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: timeline, character tables, C1--C4, B1--B2, traps, constraints | 1 |
| `layer1-workspace.md` | Workspace spec: 5 config + 5 initial + 2 update files | 2 |
| `layer2-sessions.md` | 4 sessions: main + 3 history (~24 loops + Phase 2 appends) | 3 |
| `layer3-eval.md` | 30 eval rounds | 4 |
| `layer4-dynamic.md` | 4 updates: action lists, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 赵琳 | Finance Director | Email | `chenjing_zhaolin_email_{uuid}.jsonl` | `PLACEHOLDER_ZHAOLIN_EMAIL_UUID` | initial + Update 2 append |
| 员工小李 | Employee | IM | `chenjing_employee_im_{uuid}.jsonl` | `PLACEHOLDER_EMPLOYEE_IM_UUID` | initial + Update 2 append |
| 张薇 | HR VP | Feishu | `chenjing_zhangwei_feishu_{uuid}.jsonl` | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | initial + Update 4 append |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Expense "gym" vs invoice "spa" | R1 (baseline) | None (persistent fact) |
| C2 | Finance "follows policy" vs policy has no SPA mention | R2 (partial) | R2->R7 (employee reveals VP oral source) |
| C3 | Claim timeline (NON-CONFLICT) | R1 (persistent) | None |
| C4 | VP approved verbally vs no written record | R6 (partial) | R6->R9->R11 (no record + VP ambiguous denial) |
| B1 | Email Loop 5: Agent accepts finance "follows policy" | R5 (correction) | R7 (full reversal) |
| B2 | Employee IM Loop 3: Agent treats as "categorization error" | R5 (correction via health data) | R8 (full reversal) |

---

## 5. Execution Steps

### Step 0: Generate 4 UUIDs (MAIN, ZHAOLIN_EMAIL, EMPLOYEE_IM, ZHANGWEI_FEISHU)
### Step 1: Create Workspace Files (layer1)
### Step 2: Write History Sessions (layer2) -- B1 in zhaolin_email Loop 5, B2 in employee_im Loop 3
### Step 3: Write Questions File (layer3) -- 30 rounds, 30% exec_check
### Step 4: Write Update Source Files (layer4)
### Step 5: Runtime Checks
