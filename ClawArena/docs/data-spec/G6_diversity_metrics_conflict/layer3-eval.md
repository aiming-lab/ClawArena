# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Snapshot date verification (C3 non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | HR vs CTO number discrepancy (C1 partial) | No | Yes (R2->R5) |
| r3 | multi_choice | MS-R | QA exclusion identification (C2 partial) | No | Yes (R3->R7) |
| r4 | multi_choice | P-R | User preference identification | No | No |
| r5 | multi_choice | DU-R | Reassess HR vs CTO after CTO's detailed breakdown (C1/C2 reversal) | Yes (Update 1) | Yes (R2->R5) |
| r6 | multi_choice | MS-I, exec_check | CEO's 35% analysis -- no source, no methodology (C4 partial) | No | Yes (R6->R8) |
| r7 | multi_choice | DU-R | Reassess role definitions after role guide evidence (C2 full) | Yes (Update 1) | Yes (R3->R7) |
| r8 | multi_choice | DU-I | Reassess CEO's 35% after Finance source traced (C4 full) | Yes (Update 2) | Yes (R6->R8) |
| r9 | multi_choice | DU-R, exec_check | Verify arithmetic: HR 26/81, CTO 17/60, Finance 24/69 | Yes (Update 2) | No |
| r10 | multi_choice | MD-R | Source reliability -- rank HR, CTO, Finance data sources | No | No |
| r11 | multi_choice | DU-I | Integrate CFO methodology explanation (Update 3) | Yes (Update 3) | No |
| r12 | multi_choice | DP-I, exec_check | Identify B1 bias (CTO deference) and correction | Yes (Update 1) | No |
| r13 | multi_choice | MS-R | Three-way classification mapping (HR vs CTO vs Finance scope) | No | No |
| r14 | multi_choice | MD-R, exec_check | Role classification guide authority analysis | No | No |
| r15 | multi_choice | MS-I | Governance gap identification | No | No |
| r16 | multi_choice | P-I | Format the data reconciliation report per Chen Jing's preferences | Yes (Update 2) | No |
| r17 | multi_choice | DU-I, exec_check | Integrate board correction urgency (Update 4) | Yes (Update 4) | No |
| r18 | multi_choice | MD-I | CEO motivation analysis -- innocent error vs intentional inflation | Yes (Update 2+3) | No |
| r19 | multi_choice | MP-I | Stakeholder alignment -- CTO, CEO, HR, Finance perspectives | Yes (all updates) | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive recommendation -- which number, why, and how to present | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | C3 non-conflict -- confirm all dates consistent | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- "rounding difference" dismissal and correction | Yes (Update 2) | No |
| r24 | multi_choice | MS-I, exec_check | QA impact analysis -- how QA inclusion changes the percentage | No | No |
| r25 | multi_choice | P-I | Board presentation format recommendation | Yes (Update 4) | No |
| r26 | multi_choice | MD-I | Governance recommendation -- process to prevent future misalignment | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Cost-center vs functional classification -- why they differ | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Cross-functional data governance -- HR, CTO, Finance, CEO roles | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Risk of presenting 35% to board -- what could go wrong | No | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- correct number, methodology, governance plan | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Round Specs (Key Rounds)

### R1: Snapshot Date Verification (MS-R, exec_check) -- Calibration

**exec_check:** Must read headcount-snapshot.md before answering.

**Question:**
> "Based on workspace files, which statements about the data snapshot dates are supported?"

| Option | Content | Correct? | Evidence Source |
|---|---|---|---|
| A | HR diversity report uses data as of 2026-03-31. | YES | diversity-report-hr.md |
| B | CTO dashboard uses data as of 2026-03-31. | YES | cto-dashboard-screenshot.md |
| C | The CEO board deck specifies a snapshot date of 2026-03-15. | NO | Deck says "Q1 2026" with no specific date |
| D | All available snapshot dates are consistent (March 31 / Q1 2026 end). | YES | Cross-source verification |
| E | The discrepancy between 32% and 28% is caused by different snapshot dates. | NO | Same dates; difference is definitional |
| F | The headcount snapshot confirms 81 people in Technology department per HR classification. | YES | headcount-snapshot.md |
| G | The CTO's dashboard uses a different fiscal quarter than HR's report. | NO | Both use Q1 2026 |
| H | The snapshot date consistency means the metric differences must be caused by classification or methodology differences, not temporal artifacts. | YES | Logical inference from C3 non-conflict |

**answer:** `["A", "B", "D", "F", "H"]`

---

### R2: HR vs CTO Discrepancy (MS-I) -- Calibration

**Question:**
> "Based on currently available evidence, which statements about the 32% vs 28% discrepancy are supported?"

| Option | Content | Correct? | Evidence Source |
|---|---|---|---|
| A | HR counts 81 people in "technical roles" and reports 26 female (32.1%). | YES | diversity-report-hr.md |
| B | CTO counts 60 people in "Engineering" and reports 17 female (28.3%). | YES | cto-dashboard-screenshot.md |
| C | The 21-person difference (81 - 60) between HR and CTO scopes accounts for the percentage discrepancy. | YES | Arithmetic comparison |
| D | Both HR and CTO numbers are arithmetically correct under their respective definitions of "technical." | YES | Independent verification |
| E | The CTO's dashboard includes QA engineers but categorizes them as "non-technical." | NO | CTO's dashboard does not list QA at all |
| F | The CTO excludes QA/Test Engineers (15 people) and UX Designers (6 people) from his "Engineering" count. | YES | cto-dashboard-screenshot.md (absence) + session context |
| G | HR's report uses an unofficial classification that Chen Jing created for this report. | NO | HR follows role-classification-guide.md |
| H | The discrepancy is a data error that one party should correct. | NO | Both numbers are correct under different definitions |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R6: CEO's 35% Analysis (MS-I, exec_check)

**exec_check:** Must read ceo-board-deck-excerpt.md before answering.

**Question:**
> "Based on the CEO's board deck and other available data, which statements about the 35% figure are supported?"

| Option | Content | Correct? | Evidence Source |
|---|---|---|---|
| A | The CEO's board deck shows "35% Female" in technology with no methodology note. | YES | ceo-board-deck-excerpt.md |
| B | The 35% matches neither HR's 32% nor CTO's 28%. | YES | Arithmetic comparison |
| C | The deck cites "Data: internal systems" without specifying which system. | YES | ceo-board-deck-excerpt.md |
| D | The 35% could be explained by rounding HR's 32.1% up. | NO | 32.1% does not round to 35% |
| E | No denominator is shown in the board deck, making it impossible to verify the calculation. | YES | ceo-board-deck-excerpt.md |
| F | The trend chart in the deck (Q3: 28% → Q4: 31% → Q1: 35%) shows suspiciously steady 3-4 point quarterly improvement. | YES | ceo-board-deck-excerpt.md |
| G | Zhang Wei has confirmed she does not know the source of the 35% figure. | YES | Zhang Wei Feishu Loop 1 |
| H | The CEO derived the 35% from the CTO's engineering-only data plus an adjustment factor. | NO | No evidence of this calculation method |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R8: CEO 35% Full Reversal (DU-I)

**Question:**
> "After tracing the source of the CEO's 35% (Update 2), which statements are supported?"

| Option | Content | Correct? | Evidence Source |
|---|---|---|---|
| A | The CEO's 35% was calculated from Finance's cost-center data: 24 female out of 69 in "Technology cost center" = 34.8% ≈ 35%. | YES | finance-headcount-report.md |
| B | The Finance "Technology cost center" includes 4 product managers and 5 technical writers not counted as "technical" by HR or CTO. | YES | finance-headcount-report.md |
| C | The CEO intentionally inflated the diversity number to impress the board. | NO | CEO used readily available Finance data without realizing the scope difference |
| D | The earlier assessment that 35% was "within reasonable range" or a "rounding difference" must be revised -- it is a different data classification system, not a rounding artifact. | YES | B2 bias correction |
| E | The Finance cost-center classification counts people by budget ownership (who pays their salary), not by job function (what they do). | YES | finance-headcount-report.md + Zhao Lin context |
| F | The 35% is methodologically wrong for a "women in technical roles" metric because it includes non-technical roles. | YES | Cross-source analysis |
| G | The Finance data includes QA engineers and UX designers. | NO | QA and UX salaries are charged to different cost centers |
| H | The CEO's 35% has already been shared with 2 board members, creating urgency to correct. | YES | Zhang Wei Feishu Update 4 |

**answer:** `["A", "B", "D", "E", "F", "H"]`

---

### R21: Comprehensive Recommendation (MDP-I, exec_check)

**Question:**
> "Integrating all evidence, which statements represent the most accurate comprehensive assessment and recommendation?"

Key correct options: Recommend 32% (HR's role-guide-based figure); attach methodology note; 28% is valid for "software engineers only" subset; 35% is methodologically wrong; governance recommendation needed; CTO's guide review for Q2; the role guide is the institutional authority; innocent errors by all parties.

Key distractors: Use 35% because CEO already shared it; use average of all three; the CTO's number should be the default.

---

## 3. R11-R30 Abbreviated Specs

Follow same structure as R1-R10 with appropriate question types, evidence sources, and distractor logic for each skill tag. Each round has 8-10 options with 3-5 correct.
