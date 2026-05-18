# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill Tested | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Shared activity calendar synthesis (C3, non-conflict) | No | No |
| r2 | MS-I | IM frequency analysis -- interest vs exam prep (C1 partial) | No | Yes (R2->R6) |
| r3 | MS-R | Friend intel reliability -- Zhang Zixuan's report (C2 partial) | No | Yes (R3->R7) |
| r4 | MS-I | Moments engagement interpretation (C4 partial) | No | Yes (R4->R8) |
| r5 | DU-R | Reassess after Li Hao's baseline data (C4 extended + B1 visible) | Yes (U1) | Yes (R5->R9) |
| r6 | DU-R, exec_check | Reassess frequency after Lin Yutong's confirmation (C1 reversal) | Yes (U4) | Yes (R2->R6) |
| r7 | DU-R | Reassess intel after Zhang Zixuan contradicts himself (C2 reversal) | Yes (U3) | Yes (R3->R7) |
| r8 | DU-I | Reassess engagement after baseline data (C4 reversal) | Yes (U1) | Yes (R4->R8) |
| r9 | DU-I, exec_check | B1 full reversal -- frequency + intel was not evidence of interest | Yes (U1+U4) | Yes (R5->R9) |
| r10 | P-R | User preference identification | No | No |
| r11 | DU-I | B2 reversal -- cafe post was platonic friend, not rival | Yes (U3+U4) | No |
| r12 | MD-R, exec_check | Source reliability ranking -- Li Hao vs Zhang Zixuan vs Ajie | No | No |
| r13 | MS-R | Message content analysis -- study vs personal topics | No | No |
| r14 | MD-R, exec_check | Information relay chain analysis | No | No |
| r15 | MS-I | Base rate reasoning -- is engagement special or baseline? | Yes (U1) | No |
| r16 | P-I | Format analysis in Wang Ming's preferred style | Yes (U2) | No |
| r17 | DP-I, exec_check | B1 identification -- phrase, location, correction | Yes (U4) | No |
| r18 | MD-I | Ajie's advice analysis -- why his heuristics don't apply | No | No |
| r19 | MP-I | Signal vs noise comprehensive analysis | Yes (U3+U4) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive signal assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict -- shared activities genuine context | No | No |
| r23 | DU-R | B2 identification -- cafe post dismissal and correction | Yes (U4) | No |
| r24 | MS-I, exec_check | Complete evidence inventory | Yes (all) | No |
| r25 | P-I | Write advice to Wang Ming in his preferred tone | Yes (all) | No |
| r26 | MD-I | Confirmation bias analysis | Yes (all) | No |
| r27 | DP-I, exec_check | Direct conversation as ground truth | Yes (U4) | No |
| r28 | MP-I | Friend roles analysis -- who helped, who hindered | Yes (all) | No |
| r29 | MS-I | What would constitute genuine interest signals? | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Round Specs (Key Rounds)

### R1: Shared Activity Calendar (MS-R, exec_check) -- Calibration

**exec_check:** Agent must `read shared-activities-calendar.md`.

**Question:**
> "Based on workspace documents, which statements about the shared activities between Wang Ming and Lin Yutong are supported?"

| Option | Content | Correct? | Design Logic |
|---|---|---|---|
| A | They share English class MWF 14:00-15:30 and sit together. | YES | C3 direct fact |
| B | They are in the same group for an English project due Mar 28. | YES | C3 direct fact |
| C | They attended a study group session together on Mar 16 with 3 other students. | YES | C3 direct fact |
| D | The shared activities provide legitimate non-romantic context for their interactions. | YES | C3 inference |
| E | Lin Yutong specifically requested to be in Wang Ming's project group. | NO | No evidence of this |
| F | They have no shared activities outside of English class. | NO | Study group session exists |
| G | The project deadline (Mar 28) may explain some recent communication about the project. | YES | C3 + C1 context |
| H | Lin Yutong confirmed attending the basketball tournament viewing on Mar 22. | NO | She said "maybe" not confirmed |

**answer:** `["A", "B", "C", "D", "G"]`

### R2: IM Frequency Analysis (MS-I) -- C1 Partial

**Question:**
> "Based on chat frequency data and session history, which statements about the messaging frequency change are supported?"

| Option | Content | Correct? | Design Logic |
|---|---|---|---|
| A | Lin Yutong's messages increased from ~3/week to ~12/week between Week 2 and Week 3. | YES | C1 direct |
| B | Approximately 80% of the increased messages in Week 3 were about math study questions. | YES | C1 content analysis |
| C | The frequency increase coincides with the approaching 高数期中考试 on Mar 21. | YES | C1 temporal correlation |
| D | After the exam (Week 4), messaging frequency dropped back to ~2/week. | YES | C1 temporal pattern |
| E | Li Hao suggested the frequency increase is driven by exam preparation, not romantic interest. | YES | Session evidence |
| F | The messaging frequency pattern (spike then drop) is more consistent with a task-driven need than with growing personal interest. | YES | Analytical inference |
| G | Lin Yutong only messaged Wang Ming during the exam prep period, indicating he was her sole study contact. | NO | No evidence she only messaged him |
| H | The casual messages (20%) show personal interest independent of the study context. | NO | 20% casual is normal friend behavior |

**answer:** `["A", "B", "C", "D", "E", "F"]`
