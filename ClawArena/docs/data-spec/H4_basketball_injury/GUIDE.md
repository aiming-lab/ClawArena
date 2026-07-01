# trace_h4 -- Basketball Injury Liability Dispute: Execution Guide

> This file is the complete entry point for a fresh window.

---

## 1. Task Overview

**Task ID:** `trace_h4`

**Scenario:** 王明 (UESTC CS freshman, 17) was injured during a school basketball friendly match. C1: Video shows the defender (Zhang Qiang) was in motion during contact, but the referee ruled "no foul" -- the referee's own annotation notes "defender in motion," contradicting the ruling; coach's video analysis confirms blocking foul per CUBA rule 4.14. C2: Campus clinic diagnosed "mild sprain" but missed a "suspicious positive anterior drawer test" that should have triggered MRI; hospital MRI confirmed partial ACL tear. C3: Game timeline is consistent across all sources (NON-CONFLICT). C4: Insurance covers "sports/athletic injury" but rejected the claim as "recreational activity"; school sports department approval document classifies the match as "school-organized extracurricular sports activity."

**Core evaluation goals:**
1. Can the agent identify the referee ruling/annotation contradiction and apply basketball rules? (MS)
2. Can the agent recognize the campus clinic's diagnostic gap (suspicious positive test not followed up)? (MS)
3. Can the agent integrate coach analysis, school approval, and policy text to build an insurance appeal? (DU)
4. Does the agent use 王明's preferred casual, conclusion-first format? (P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible, C1--C4, B1--B2, traps | 1 |
| `layer1-workspace.md` | 5 config + 5 initial + 3 update files | 2 |
| `layer2-sessions.md` | 5 sessions: main + 4 history | 3 |
| `layer3-eval.md` | 30 rounds | 4 |
| `layer4-dynamic.md` | 4 updates | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | UUID Placeholder | Initial or Update |
|---|---|---|---|---|
| -- | main | main | `PLACEHOLDER_MAIN_UUID` | initial |
| 马强 | Teammate | IM | `PLACEHOLDER_MAQIANG_IM_UUID` | initial + Update 2 |
| 刘教练 | Coach | IM | `PLACEHOLDER_COACH_IM_UUID` | initial + Update 3 |
| 母亲 | Mother | WeChat | `PLACEHOLDER_MOTHER_WECHAT_UUID` | initial + Update 1 |
| 辅导员 | Counselor | IM | `PLACEHOLDER_COUNSELOR_IM_UUID` | initial + Update 4 |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible | Reversal Round |
|---|---|---|---|
| C1 | Video shows contact vs referee "no foul" (but annotation says "defender moving") | R1 | R3->R6->R9 |
| C2 | Campus "sprain" vs hospital "ACL tear" | R2 | None (baseline fact) |
| C3 | Game timeline NON-CONFLICT | R1 | None |
| C4 | Insurance "sports injury" coverage vs "recreational" rejection | R4 | R4->R7->R11 |
| B1 | Teammate IM Loop 4: accepts referee as authoritative | R5 | R6+R9 |
| B2 | Main Loop 3: accepts campus diagnosis at face value | R2 | R5 |

---

## 5. Execution Steps

### Step 0: Generate 5 UUIDs
### Step 1: Create Workspace Files
### Step 2: Write Sessions -- B1 in maqiang Loop 4, B2 in main Loop 3
### Step 3: Write Questions -- 30 rounds, 30% exec_check
### Step 4: Write Updates
### Step 5: Runtime Checks
