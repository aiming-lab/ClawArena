# Layer 3 -- Eval Questions Spec

> 30 rounds, multi_choice, 8-10 options. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Guideline timeline synthesis (C3, non-conflict) | No | No |
| r2 | MS-I | Prescription spike analysis -- 300% increase vs guideline (C1) | No | Yes (R2->R6) |
| r3 | MS-R | Pharma visit correlation -- temporal pattern (C2) | No | Yes (R3->R7) |
| r4 | MS-I | Dr. Wang "following guidelines" vs pre-guideline timing (C4) | No | Yes (R4->R8) |
| r5 | DU-R | Reassess after physician breakdown (B1 visible) | Yes (U1) | Yes (R5->R9) |
| r6 | DU-R, exec_check | Reassess after guideline detail analysis (C1 reversal) | Yes (U2) | Yes (R2->R6) |
| r7 | DU-R | Reassess after external comparison (C2 strengthened) | Yes (U3) | Yes (R3->R7) |
| r8 | DU-I | Reassess after financial trail (C4 reversal) | Yes (U4) | Yes (R4->R8) |
| r9 | DU-I, exec_check | B1 full reversal | Yes (U2+U4) | Yes |
| r10 | P-R | User preference identification | No | No |
| r11 | DU-I | B2 reversal -- correlation + pre-guideline timing = stronger than coincidental | Yes (U1+U4) | No |
| r12 | MD-R, exec_check | Source reliability ranking | No | No |
| r13 | MS-R | Price comparison -- injection vs oral | No | No |
| r14 | MD-R, exec_check | Dr. Wang's claims analysis | No | No |
| r15 | MS-I | Guideline text vs actual prescribing pattern | Yes (U2) | No |
| r16 | P-I | Format analysis in Lin Yi's clinical style | Yes (U2) | No |
| r17 | DP-I, exec_check | B1 identification | Yes (U2) | No |
| r18 | MD-I | Pharma influence mechanism analysis | No | No |
| r19 | MP-I | Systemic vs individual prescribing analysis | Yes (U3+U4) | No |
| r20 | P-R | Preference compliance | No | No |
| r21 | MDP-I, exec_check | Comprehensive assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict -- guideline date confirmed | No | No |
| r23 | DU-R | B2 identification and correction | Yes (U1+U4) | No |
| r24 | MS-I, exec_check | Complete evidence chain | Yes (all) | No |
| r25 | P-I | Format compliance report in Lin Yi's style | Yes (all) | No |
| r26 | MD-I | Financial influence analysis | Yes (U4) | No |
| r27 | DP-I, exec_check | Temporal evidence as key differentiator | Yes (U1) | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Recommendations for department | Yes (all) | No |
| r30 | MDP-I | Final comprehensive | Yes (all) | Comprehensive |

exec_check: R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Key Round Specs

### R1: Guideline Timeline (MS-R, exec_check) -- Calibration

**exec_check:** `read clinical-guideline-update.md`

**Question:** "Which statements about the guideline timeline are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | Guideline published Feb 15, 2026 |
| B | YES | Guideline recommends PPI class (omeprazole, pantoprazole, esomeprazole) |
| C | YES | Guideline states "口服优先" (oral preferred) for stable patients |
| D | YES | First pharma dinner (Feb 1) occurred 14 days before guideline publication |
| E | NO | Guideline specifically recommends AnZe brand omeprazole injection |
| F | YES | Dr. Wang's prescription increase started Feb 10, 5 days before guideline |
| G | NO | Guideline was published in January 2026 |
| H | YES | Guideline recommends cost-effectiveness as a consideration |

**answer:** `["A", "B", "C", "D", "F", "H"]`

### R2: Prescription Spike (MS-I) -- C1

**Question:** "Which statements about the prescription increase are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | Overall increase from 20/month to 80/month (300%) |
| B | YES | Injection form accounts for majority of increase (15->70) while oral stayed flat (5->10) |
| C | YES | Dr. Wang is the highest prescriber |
| D | YES | A new guideline recommends PPI use, providing a legitimate clinical basis for some increase |
| E | NO | The guideline specifically recommends a 300% increase in omeprazole prescriptions |
| F | YES | The increase is disproportionately in injection form, not oral |
| G | NO | All physicians increased prescribing at the same rate |
| H | YES | The magnitude and form preference of the increase go beyond what the guideline recommends |

**answer:** `["A", "B", "C", "D", "F", "H"]`
