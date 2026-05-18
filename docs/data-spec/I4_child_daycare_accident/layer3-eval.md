# Layer 3 -- Eval Questions Spec

> 30 rounds, multi_choice. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Medical timeline synthesis (C3, non-conflict) | No | No |
| r2 | MS-I | Wound-mechanism analysis -- slide vs edge impact (C1) | No | Yes (R2->R6) |
| r3 | MS-R | Teacher claim "I was watching" assessment (C2) | No | Yes (R3->R7) |
| r4 | MS-I | Child witness testimony evaluation (C4) | No | Yes (R4->R8) |
| r5 | DU-R | Reassess after Lin Yi's wound analysis (B1 visible) | Yes (U1) | Yes (R5->R9) |
| r6 | DU-R, exec_check | Reassess after CCTV -- location confirmed (C1 reversal) | Yes (U3) | Yes (R2->R6) |
| r7 | DU-R | Reassess teacher claim after CCTV -- phone confirmed (C2 reversal) | Yes (U3) | Yes (R3->R7) |
| r8 | DU-I | Reassess child testimony after CCTV + confession (C4 reversal) | Yes (U3+U4) | Yes (R4->R8) |
| r9 | DU-I, exec_check | B1 full reversal -- wound analysis was correct | Yes (U3+U4) | Yes |
| r10 | P-R | Preference identification | No | No |
| r11 | DU-I | B2 reversal -- child testimony corroborated | Yes (U3+U4) | No |
| r12 | MD-R, exec_check | Source reliability ranking | No | No |
| r13 | MS-R | Safety policy violation analysis | No | No |
| r14 | MD-R, exec_check | Teacher Zhao credibility analysis | No | No |
| r15 | MS-I | Wound forensics -- what wound pattern indicates | Yes (U1) | No |
| r16 | P-I | Format findings in Lin Yi's clinical style | Yes (U3) | No |
| r17 | DP-I, exec_check | B1 identification | Yes (U3) | No |
| r18 | MD-I | Kindergarten institutional response analysis | No | No |
| r19 | MP-I | Negligence vs cover-up analysis | Yes (U3+U4) | No |
| r20 | P-R | Preference compliance | No | No |
| r21 | MDP-I, exec_check | Comprehensive assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict -- medical timeline confirmed | No | No |
| r23 | DU-R | B2 identification -- child testimony dismissal | Yes (U3+U4) | No |
| r24 | MS-I, exec_check | Complete evidence chain | Yes (all) | No |
| r25 | P-I | Formal incident analysis report | Yes (all) | No |
| r26 | MD-I | Supervision failure analysis | Yes (all) | No |
| r27 | DP-I, exec_check | CCTV as corroborating evidence | Yes (U3) | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Recommendations for kindergarten | Yes (all) | No |
| r30 | MDP-I | Final comprehensive | Yes (all) | Comprehensive |

exec_check: 9/30 = 30%

---

## 2. Key Round Specs

### R1: Medical Timeline (MS-R, exec_check) -- Calibration

**exec_check:** `read medical-examination-report.md`

**Question:** "Which statements about the medical timeline are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | Incident at ~10:15, first aid by 10:20, parent called 10:30, clinic at 11:00 |
| B | YES | Clinic applied 3 stitches for 2cm forehead laceration |
| C | YES | Timeline is internally consistent across kindergarten report and medical record |
| D | YES | Wound documented as "创缘整齐" (clean wound edges) |
| E | NO | Le Le was unconscious for 10 minutes (no evidence of prolonged LOC) |
| F | YES | No vitals abnormalities noted at clinic visit |
| G | NO | The clinic doctor noted the wound was inconsistent with a slide fall |
| H | YES | The time between incident (10:15) and medical treatment (11:00) was ~45 minutes |

**answer:** `["A", "B", "C", "D", "F", "H"]`

### R2: Wound-Mechanism Analysis (MS-I) -- C1

**Question:** "Which statements about the wound and its reported mechanism are supported?"

| Option | Correct? | Content |
|---|---|---|
| A | YES | The laceration has clean, defined edges typical of impact against a hard straight edge |
| B | YES | Slide falls typically produce abrasion or friction marks, not clean lacerations |
| C | YES | The wound location (right lateral forehead) is more consistent with a lateral/backward fall than forward slide motion |
| D | YES | No sliding abrasion or friction marks are documented around the wound |
| E | YES | The kindergarten report states "fell from slide" but the medical findings suggest a different mechanism |
| F | NO | The clinic doctor explicitly stated the wound was caused by a non-slide mechanism |
| G | YES | A fall from a climbing structure (~80cm) against a metal edge would produce this type of wound |
| H | NO | Clean linear lacerations are the most common injury from slide falls |

**answer:** `["A", "B", "C", "D", "E", "G"]`
