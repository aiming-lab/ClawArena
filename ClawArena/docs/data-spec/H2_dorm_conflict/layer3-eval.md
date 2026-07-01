# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | CCTV + access log cross-reference (C3 non-conflict) | No | No |
| r2 | MS-I | Access log vs canteen timestamp impossibility (C1 partial) | No | Yes (R2->R5) |
| r3 | MS-R | Package pickup log anomaly (C2 partial) | No | Yes (R3->R7) |
| r4 | P-R | Wang Ming's preferences | No | No |
| r5 | DU-R | Reassess C1 after Li Hao's statement (card was borrowed) | Yes (U1) | Yes (R2->R5) |
| r6 | MS-I, exec_check | Physical impossibility analysis (10-min walk vs 5-min gap) | No | No |
| r7 | DU-R | Reassess C2 after package station camera (Zhang Wei mistake) | Yes (U2) | Yes (R3->R7) |
| r8 | DU-I | Full timeline reconstruction after U1+U2 | Yes (U1+U2) | Yes (B1 reversal) |
| r9 | DU-R, exec_check | Reassess C4 after bookstore receipt + lost-and-found (amount + resolution) | Yes (U3+U4) | Yes (R4->R9) |
| r10 | MD-R | Evidence hierarchy -- system logs vs testimony vs camera | No | No |
| r11 | DU-I | Integrate bookstore receipt correcting ¥500 to ¥200 (U3) | Yes (U3) | No |
| r12 | DP-I, exec_check | Identify B1 (access log = person) and what corrected it | Yes (U1) | No |
| r13 | MS-R | Alibi reconstruction -- Wang Ming's actual timeline | No | No |
| r14 | MD-R, exec_check | Card ≠ person principle -- when is a card swipe unreliable? | No | No |
| r15 | MS-I | Elimination analysis -- who could have taken the money? | No | No |
| r16 | P-I | Present findings in Wang Ming's preferred format | Yes (U2) | No |
| r17 | DU-I, exec_check | Integrate lost-and-found resolution (U4) | Yes (U4) | No |
| r18 | MD-I | Why Liu Chen's memory of ¥500 was wrong | Yes (U3) | No |
| r19 | MP-I | Multi-party analysis: Wang Ming, Liu Chen, Li Hao, Zhang Wei | Yes (all) | No |
| r20 | P-R | Preference compliance | No | No |
| r21 | MDP-I, exec_check | Comprehensive resolution -- no theft, complete explanation | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict -- CCTV confirms all timestamps | No | No |
| r23 | DU-R | B2 identification -- amount acceptance and correction | Yes (U3) | No |
| r24 | MS-I, exec_check | Adjacent pickup code analysis | No | No |
| r25 | P-I | Explain the resolution to Liu Chen in appropriate tone | Yes (all) | No |
| r26 | MD-I | Root cause -- door draft + unsecured drawer | Yes (U4) | No |
| r27 | DP-I, exec_check | What evidence would have cleared Wang Ming earlier? | Yes (U1) | No |
| r28 | MP-I | Lessons learned for all parties | Yes (all) | No |
| r29 | MS-I | What if Li Hao had not come forward? | No | No |
| r30 | MDP-I | Final comprehensive -- all evidence synthesized | Yes (all) | Comprehensive |

**exec_check:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Key Round Specs

### R1: CCTV + Access Log Synthesis (MS-R, exec_check) -- Calibration

**exec_check:** Must read dorm-access-log.md and dorm-cctv-summary.md.

**Question:**
> "Based on workspace files, which statements about the Building 7 entrance activity on March 20 are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | CCTV shows a male in black hoodie entering Building 7 at ~10:00 without swiping a card, after Ma Qiang exits. | YES | dorm-cctv-summary.md |
| B | The access log shows Wang Ming's card (WM-2026-CS-0042) swiped at 10:15:23. | YES | dorm-access-log.md |
| C | CCTV shows a male in gray jacket with glasses swiping a card at ~10:14:30. | YES | dorm-cctv-summary.md |
| D | The CCTV description of the 10:00 entrant (black hoodie, ~175cm) and the 10:14 entrant (gray jacket, glasses, ~180cm) are clearly two different people. | YES | dorm-cctv-summary.md |
| E | The access log records both entry and exit swipes, showing Wang Ming left at 10:10. | NO | System note says entry only |
| F | CCTV and access log timestamps are consistent -- the 10:14-10:15 card swipe matches the gray-jacket person on camera. | YES | Cross-source alignment |
| G | The access log shows Ma Qiang leaving Building 7 at 09:55. | NO | Access log only records entries |
| H | Liu Chen's card swipe at 11:02 is consistent with his claim of returning to discover missing money. | YES | dorm-access-log.md + session context |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R2: Access Log vs Canteen Impossibility (MS-I) -- Calibration

**Question:**
> "Based on the access log and canteen payment records, which statements about the 10:15-10:20 time window are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | Wang Ming's card was swiped at Building 7 entrance at 10:15:23 and used at Canteen #2 at 10:20:15 -- a 5-minute gap. | YES | Both logs |
| B | Building 7 to Canteen #2 is approximately a 10-minute walk, making it physically impossible to be at both locations within 5 minutes. | YES | Campus geography context |
| C | This physical impossibility suggests the card was used by two different people, or the timestamps are wrong. | YES | Logical inference |
| D | The most likely explanation is that Wang Ming ran to the canteen. | NO | 10 min walk cannot be done in 5 min even running |
| E | The canteen payment system timestamps could be inaccurate by up to 10 minutes. | NO | No evidence of timestamp inaccuracy |
| F | If the card was not with Wang Ming at 10:15, then the access log does NOT prove Wang Ming entered Building 7 at that time. | YES | Card ≠ person principle |
| G | CCTV shows the person who swiped at 10:14-10:15 was wearing a gray jacket, while Wang Ming typically wears a black hoodie. | YES | dorm-cctv-summary.md |
| H | This evidence alone is sufficient to clear Wang Ming of suspicion. | NO | Still need to confirm who had the card |

**answer:** `["A", "B", "C", "F", "G"]`

---

### R5: C1 Resolution After Li Hao's Statement (DU-R)

**Question:**
> "After Li Hao's statement (Update 1), which statements about the access log and canteen evidence are now supported?"

| Option | Content | Correct? |
|---|---|---|
| A | Li Hao confirms he borrowed Wang Ming's card and swiped at Building 7 at ~10:15 to visit Room 208 on floor 2. | YES |
| B | Li Hao confirms he used the card at Canteen #2 at 10:20 for ¥12. | YES |
| C | The 10:15 building swipe and 10:20 canteen payment are both explained by Li Hao using the card. | YES |
| D | CCTV's gray-jacket male at 10:14 is consistent with Li Hao's description (glasses, ~180cm). | YES |
| E | Wang Ming entered Building 7 at ~10:00 through the unlocked door (CCTV: black hoodie, no card swipe). | YES |
| F | Li Hao went to Room 312 and could have seen whether the money was there. | NO |
| G | The access log is no longer evidence against Wang Ming -- it records Li Hao's entry, not Wang Ming's. | YES |
| H | Wang Ming was in the dorm from ~10:00 to ~10:10 (CCTV confirms entry and exit). | YES |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

## 3. R6-R30 Abbreviated Specs

Each round follows the same 8-10 option format with 3-5 correct answers, evidence-based reasoning, and appropriate distractors. Key rounds:

- **R7:** Package resolved -- Zhang Wei from 314, adjacent codes
- **R8:** Full timeline with all corrections applied
- **R9:** Amount corrected to ¥200, found in lost-and-found
- **R11:** Bookstore receipt analysis
- **R17:** Lost-and-found ¥200 matches the missing amount
- **R21:** Comprehensive: no theft, door draft explanation, all evidence aligned
- **R30:** Final complete resolution with lessons learned
