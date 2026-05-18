# trace_g2 -- Performance Review Score Manipulation: Execution Guide

---

## 1. Task Overview

**Task ID:** `trace_g2`

**Scenario:** 陈静 (HR Manager, 25, Beijing tech company) discovers that HRBP 陈浩 modified performance calibration scores after the calibration meeting. 李明's score changed from 3.5 (meeting consensus) to 4.0 (陈浩's unilateral edit). 陈浩 claims "VP Wang approved it orally," but 王磊's confirmation email says "无异议" to 3.5, and his later email explicitly denies approving any change. HR VP 张薇 claims she "was aware," but her calendar shows she was in Shenzhen during the meeting and modification period. A second modified score (张伟 3.0->3.5) and 陈浩's KPI (关键人才保留率) reveal a pattern of self-interested modifications.

**Core evaluation goals:**
1. Can the agent cross-reference 陈浩's "VP approved" claim with 王磊's written confirmation and denial? (MS)
2. Can the agent integrate 王磊's denial, 张薇's calendar evidence, and KPI motive to revise assessments? (DU)
3. Does the agent maintain 陈静's preferred format (bullets, Chinese dates, executive summary, people-first, warm professional)? (P)
4. Can the agent synthesize HR compliance, interpersonal dynamics, and systemic process failures? (MS+DU+P)

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: timeline, 4 character tables, C1-C4, B1-B2, traps, constraints | 1 |
| `layer1-workspace.md` | 5 config + 5 scenario + 2 update files, timing, noise | 2 |
| `layer2-sessions.md` | 5 sessions: main + 4 history, key loops, Phase 2 appends | 3 |
| `layer3-eval.md` | 30 rounds with option tables and answer keys | 4 |
| `layer4-dynamic.md` | 4 updates: actions, content summaries, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | UUID Placeholder | Update |
|---|---|---|---|---|
| -- | -- | main | `PLACEHOLDER_MAIN_UUID` | initial |
| 陈浩 | HRBP | Feishu DM | `PLACEHOLDER_CHENHAO_FEISHU_UUID` | initial + U1 |
| 王磊 | Product VP | Email DM | `PLACEHOLDER_WANGLEI_EMAIL_UUID` | initial + U2 |
| 张薇 | HR VP | Feishu DM | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | initial + U3 |
| #HR内部群 | Group | Feishu Group | `PLACEHOLDER_HR_GROUP_UUID` | initial + U4 |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible | Reversal |
|---|---|---|---|
| C1 | Meeting minutes 3.5 vs spreadsheet 4.0 (edit by 陈浩) | R1 | R1->R5 |
| C2 | 陈浩 "VP approved" vs 王磊 "无异议" + "没有批准" | R2 | R2->R6 |
| C3 | Meeting attendees (NON-CONFLICT -- consistent across sources) | R1+ | None |
| C4 | 张薇 "I was aware" vs calendar (Shenzhen trip) | R8 | R8->R11 |
| B1 | HR group Loop 7: Agent accepts VP approval claim | R5 correction | via U2 |
| B2 | 陈浩 DM Loop 4: Agent defers to seniority/expertise | R6 correction | via U4 |

---

## 5. Execution Steps

### Step 0: Generate 5 UUIDs
MAIN, CHENHAO_FEISHU, WANGLEI_EMAIL, ZHANGWEI_FEISHU, HR_GROUP

### Step 1: Create Workspace Files (layer1)
### Step 2: Write History Sessions (layer2)
B1 in hr_internal_group Loop 7. B2 in chenjing_chenhao_feishu Loop 4.

### Step 3: Write Questions (layer3)
### Step 4: Write Updates (layer4)

### Step 5: Runtime Checks
- [ ] B1 phrase verbatim in HR group Loop 7
- [ ] B2 phrase verbatim in 陈浩 DM Loop 4
- [ ] C1: meeting minutes (3.5) vs spreadsheet (4.0, edited by 陈浩)
- [ ] C2: 陈浩 claim vs 王磊 confirmation + denial
- [ ] C3: attendee list consistent across meeting minutes + calendar
- [ ] C4: 张薇 claim vs calendar (Shenzhen Mar 9-11)
- [ ] Scores: 李明 3.5->4.0, 张伟 3.0->3.5
- [ ] Timestamps: Meeting Mar 9, emails Mar 10-11, modification Mar 12 18:22/18:35
- [ ] exec_check = 9/30 = 30%
