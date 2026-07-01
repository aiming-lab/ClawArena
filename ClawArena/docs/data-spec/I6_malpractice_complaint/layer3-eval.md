# Layer 3 -- Eval Questions Spec

> 30 rounds. exec_check 20-40%.

---

## Round Inventory

| Round | Tags | Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Nursing log cross-verification (C3) | No | No |
| r2 | MS-I | Arrival time discrepancy -- triage 10:15 vs family 9:30 (C1) | No | Yes (R2->R6) |
| r3 | MS-R | 40-min wait vs 30-min policy (C2) | No | Yes (R3->R7) |
| r4 | MS-I | Family "2 hours" vs records <1 hour (C4) | No | Yes (R4->R8) |
| r5 | DU-R | After triage context -- two Level I patients (B1 visible) | Yes (U1) | Yes (R5->R9) |
| r6 | DU-R, exec_check | After security footage -- ER arrival at 10:08 (C1 reversal) | Yes (U4) | Yes (R2->R6) |
| r7 | DU-R | After Lin Yi's response -- contextualized delay (C2 reversal) | Yes (U2) | Yes (R3->R7) |
| r8 | DU-I | After all evidence -- family claims refuted (C4 reversal) | Yes (U4) | Yes (R4->R8) |
| r9 | DU-I, exec_check | B1 full reversal -- 10-min overshoot in context | Yes (U1+U2) | Yes |
| r10 | P-R | Preference identification | No | No |
| r11 | DU-I | B2 reversal -- family timeline explained by wrong building | Yes (U4) | No |
| r12 | MD-R, exec_check | Source reliability ranking | No | No |
| r13 | MS-R | ER response time policy analysis | No | No |
| r14 | MD-R, exec_check | Complaint claims vs documented evidence | No | No |
| r15 | MS-I | Multi-patient triage reasoning | Yes (U1) | No |
| r16 | P-I | Format timeline in Lin Yi's style | Yes (U2) | No |
| r17 | DP-I, exec_check | B1 identification | Yes (U1) | No |
| r18 | MD-I | Family perception vs system reality | No | No |
| r19 | MP-I | Policy breach contextualization | Yes (U1+U2) | No |
| r20 | P-R | Preference compliance | No | No |
| r21 | MDP-I, exec_check | Comprehensive assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict confirmed | No | No |
| r23 | DU-R | B2 identification -- family timeline | Yes (U4) | No |
| r24 | MS-I, exec_check | Complete timeline reconstruction | Yes (all) | No |
| r25 | P-I | Formal complaint response draft | Yes (all) | No |
| r26 | MD-I | ER workflow analysis | Yes (all) | No |
| r27 | DP-I, exec_check | Security footage as definitive evidence | Yes (U4) | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Recommendations for ER process | Yes (all) | No |
| r30 | MDP-I | Final comprehensive | Yes (all) | Comprehensive |

exec_check: R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## Key Round Specs

### R1: Nursing Log Cross-Verification (MS-R, exec_check) -- Calibration

**exec_check:** `read nursing-station-log.md`

**Question:** "Which statements about the nursing station log are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | Nursing log records bed assignment at 10:20, consistent with triage at 10:15 |
| B | YES | ECG was performed at 10:30, 15 min after triage |
| C | YES | Vitals were rechecked at 10:40, showing patient was stable |
| D | YES | Nursing log confirms Lin Yi assessed the patient at 10:55 |
| E | YES | Nursing log shows continuous patient monitoring during the 35-min gap before physician assessment |
| F | NO | Nursing log shows a 20-minute gap where no one checked on the patient |
| G | YES | Nursing log documents Lin Yi was with the trauma patient (Bed 1) when ECG was ready at 10:30 |
| H | NO | Nursing log contradicts the triage log about the arrival time |

**answer:** `["A", "B", "C", "D", "E", "G"]`

### R2: Arrival Time Discrepancy (MS-I) -- C1

**Question:** "Which statements about the arrival time discrepancy are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | Triage log records patient arrival at 10:15 |
| B | YES | Patient's family claims arrival at 9:30, creating a 45-minute discrepancy |
| C | YES | No ER system record (triage, nursing, queue) shows any 9:30 entry for Zhao Damin |
| D | YES | The discrepancy could be explained by the family arriving at a different location (e.g., outpatient building) before reaching the ER |
| E | NO | The triage nurse admitted she may have recorded the wrong arrival time |
| F | YES | Nurse Head Li confirmed that 9:30 does not appear in any ER log for this patient |
| G | YES | The family's emotional distress during a chest pain emergency could affect time perception |
| H | NO | Multiple ER staff confirmed seeing the patient at 9:30 |

**answer:** `["A", "B", "C", "D", "F", "G"]`
