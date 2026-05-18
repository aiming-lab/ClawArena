# Layer 3 -- Eval Questions Spec

> 30 rounds. exec_check 20-40%.

---

## Round Inventory

| Round | Tags | Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Overtime records cross-verification (C3) | No | No |
| r2 | MS-I | Schedule vs policy max (C1) | No | Yes (R2->R6) |
| r3 | MS-R | Fair rotation claim vs statistics (C2) | No | Yes (R3->R7) |
| r4 | MS-I | Algorithm changelog vs chief denial (C4) | No | Yes (R4->R8) |
| r5 | DU-R | After HR detailed data (B1 visible) | Yes (U1) | Yes (R5->R9) |
| r6 | DU-R, exec_check | After algorithm analysis (C1 reversal) | Yes (U2) | Yes (R2->R6) |
| r7 | DU-R | After IT deployment confirmation (C2 strengthened) | Yes (U3) | Yes (R3->R7) |
| r8 | DU-I | After bug report (C4 full) | Yes (U4) | Yes (R4->R8) |
| r9 | DU-I, exec_check | B1 full reversal | Yes (U1+U2) | Yes |
| r10 | P-R | Preference identification | No | No |
| r11 | DU-I | B2 reversal -- algorithm update not routine | Yes (U3+U4) | No |
| r12 | MD-R, exec_check | Source reliability | No | No |
| r13 | MS-R | Policy article analysis | No | No |
| r14 | MD-R, exec_check | Zhang's credibility | No | No |
| r15 | MS-I | Seniority-nights correlation | Yes (U2) | No |
| r16 | P-I | Format analysis in Lin Yi's style | Yes (U2) | No |
| r17 | DP-I, exec_check | B1 identification | Yes (U2) | No |
| r18 | MD-I | Zhang management failure analysis | No | No |
| r19 | MP-I | Systemic vs individual | Yes (U3+U4) | No |
| r20 | P-R | Preference compliance | No | No |
| r21 | MDP-I, exec_check | Comprehensive | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict | No | No |
| r23 | DU-R | B2 identification | Yes (U3+U4) | No |
| r24 | MS-I, exec_check | Complete evidence chain | Yes (all) | No |
| r25 | P-I | Format formal complaint | Yes (all) | No |
| r26 | MD-I | Algorithm fairness analysis | Yes (U4) | No |
| r27 | DP-I, exec_check | Changelog as evidence | Yes (U2) | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Recommendations | Yes (all) | No |
| r30 | MDP-I | Final comprehensive | Yes (all) | Comprehensive |

exec_check: R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## Key Round Specs

### R1: Overtime Cross-Verification (MS-R, exec_check) -- Calibration

**exec_check:** `read hr-overtime-records.md`

**Question:** "Which statements about the overtime records are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | HR records confirm Lin Yi worked 11, 12, 12 night shifts in Oct, Nov, Dec |
| B | YES | HR overtime records independently verify the shift schedule data |
| C | YES | Lin Yi's total overtime hours are the highest in the department for Q4 |
| D | YES | The two data sources (schedule + HR) agree on shift counts (C3 non-conflict) |
| E | NO | HR records show Lin Yi worked only 8 night shifts per month |
| F | YES | The department average from overtime records is consistent with ~7.5 nights/month |
| G | NO | HR records show the overtime was voluntarily requested by Lin Yi |
| H | YES | Dr. Wang's HR overtime records show ~7 nights/month average |

**answer:** `["A", "B", "C", "D", "F", "H"]`

### R2: Schedule vs Policy (MS-I) -- C1

**Question:** "Which statements about the scheduling-policy gap are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | Department policy Article 5 sets max 8 night shifts per attending per month |
| B | YES | Lin Yi's actual shifts (11-12) exceed the policy max by 37-50% |
| C | YES | The scheduling system did not enforce the policy maximum |
| D | YES | Other attendings' shifts (6-8/month) are within or near the policy limit |
| E | NO | The policy allows exceptions up to 15 shifts per month during staffing shortages |
| F | YES | Policy Article 15 requires chief approval for system-generated schedules |
| G | YES | Lin Yi is the only attending consistently exceeding the policy maximum |
| H | NO | The policy maximum was changed to 12 in October 2025 |

**answer:** `["A", "B", "C", "D", "F", "G"]`
