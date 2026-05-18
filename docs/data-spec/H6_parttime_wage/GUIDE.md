# trace_h6 -- Part-time Tutoring Wage Dispute: Execution Guide

> This file is the complete entry point for a fresh window.

---

## 1. Task Overview

**Task ID:** `trace_h6`

**Scenario:** 王明 (UESTC CS freshman, 17) tutors high school math through the "学霸家教" platform. He agreed on ¥3,000/month with the parent 张女士, but received only ¥2,400 via WeChat. C1: The ¥600 gap comes from the platform's 20% service fee, but the job posting said 10% (should have been ¥300 deducted, not ¥600). C2: The posting says "10%" but the contract says "20%" -- the platform raised fees in January 2026 but didn't update all postings; a contract footnote mentions the rate change. C3: Tutoring schedule and payment dates are consistent (NON-CONFLICT). C4: Parent says "paid full ¥3,000" and platform shows ¥2,400 to tutor -- both are true; the contradiction is the platform's intermediary extraction, not between parent and tutor. The platform later modified the posting from "10%" to "15-20%" after 王明 raised the issue, suggesting awareness of the deceptive practice.

**Core evaluation goals:**
1. Can the agent trace the three-party payment flow (parent -> platform -> tutor) and identify where the money goes? (MS)
2. Can the agent identify the posting/contract fee rate discrepancy and assess its legal significance? (DU)
3. Can the agent recognize that both parent and tutor are truthful, and the platform is the source of the discrepancy? (MD)
4. Does the agent use 王明's casual, conclusion-first format? (P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible, C1--C4, B1--B2, traps | 1 |
| `layer1-workspace.md` | 5 config + 5 initial + 1 update file | 2 |
| `layer2-sessions.md` | 4 sessions: main + 3 history | 3 |
| `layer3-eval.md` | 30 rounds | 4 |
| `layer4-dynamic.md` | 4 updates | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | UUID Placeholder | Initial or Update |
|---|---|---|---|---|
| -- | main | main | `PLACEHOLDER_MAIN_UUID` | initial |
| 张女士 | Parent | IM | `PLACEHOLDER_PARENT_IM_UUID` | initial + Update 2 |
| 平台客服 | Platform CS | IM | `PLACEHOLDER_PLATFORM_IM_UUID` | initial + Update 1 + Update 4 |
| 周姐姐 | Former Tutor | IM | `PLACEHOLDER_ZHOUJIEJIE_IM_UUID` | initial + Update 3 |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible | Reversal Round |
|---|---|---|---|
| C1 | WeChat ¥2,400 vs agreed ¥3,000 (platform fee gap) | R1 | None (baseline) |
| C2 | Platform "20% fee" (contract) vs "10%" (posting) | R2 | R2->R6->R9->R10 |
| C3 | Tutoring schedule NON-CONFLICT | R1 | None |
| C4 | Parent "paid full" vs tutor "received partial" (both true) | R3 | R3->R7 |
| B1 | Platform IM Loop 4: accepts "contract governs" | R5 | R8+R10 |
| B2 | Main Loop 3: normalizes 20% deduction as "standard" | R3 | R6 |

---

## 5. Execution Steps

### Step 0: Generate 4 UUIDs
### Step 1: Create Workspace Files
### Step 2: Write Sessions -- B1 in platform_im Loop 4, B2 in main Loop 3
### Step 3: Write Questions -- 30 rounds, 30% exec_check
### Step 4: Write Updates
### Step 5: Runtime Checks
