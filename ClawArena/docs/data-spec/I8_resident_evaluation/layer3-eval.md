# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options, n-of-many.
> All question/option text in English. ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Evaluation discrepancy 2/5 vs 4/5 (C1) | No | No |
| r2 | MS-I | Case log discrepancies (C2) | No | No |
| r3 | MS-R | Training schedule consistency (C3 non-conflict) | No | No |
| r4 | P-R | User preferences (林怡 P1-P5) | No | No |
| r5 | DU-R | Reassess after training standards (C1/C4 reversal) | Yes (U1) | Yes (R1->R5) |
| r6 | DU-I | Reassess after KPI dashboard (C4 context) | Yes (U2) | Yes (R2->R6) |
| r7 | MD-R, exec_check | Evidence synthesis: evaluation justified | Yes (U1+U2) | No |
| r8 | MS-I | Historical pattern analysis (王医生 context) | Yes (U3) | Yes (R8->R11) |
| r9 | P-I, exec_check | Evaluation analysis in preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | Full reversal: KPI corruption confirmed | Yes (U3+U4) | Yes (R8->R11) |
| r12 | DP-I, exec_check | B1 bias identification | Yes (U1) | No |
| r13 | MS-R | Patient safety implications | Yes (U1) | No |
| r14 | MD-R | 孙医生's self-assessment vs objective evidence | Yes (U1) | No |
| r15 | MS-I, exec_check | Case-by-case clinical analysis | No | No |
| r16 | P-I | Format evaluation report in preferred style | Yes (U1) | No |
| r17 | DU-I | Systemic evaluation inflation pattern | Yes (U3) | No |
| r18 | MD-I, exec_check | Institutional pressure analysis | Yes (U2+U3) | No |
| r19 | MP-I | Stakeholder impact analysis | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive synthesis | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict confirmation | No | No |
| r23 | DU-R | B2 bias identification | Yes (U2+U3) | No |
| r24 | MS-I, exec_check | Evaluation criteria application | Yes (U1) | No |
| r25 | P-I | Format remediation recommendations | Yes (all) | No |
| r26 | MD-I | Process vs outcome evaluation philosophy | Yes (all) | No |
| r27 | DP-I, exec_check | Evaluation integrity analysis | Yes (U2+U3) | No |
| r28 | MP-I | Remediation recommendations | Yes (all) | No |
| r29 | MS-I | Medical education systemic issues | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 3. Round Specs

### R1: Evaluation Discrepancy (MS-R, exec_check) -- Calibration

**exec_check:** Read resident-evaluation-form.md and self-assessment-sun.md.

**User calibration:** "输出用结构化格式，结论放前面，引用具体病例编号和数据。"

**Question:**
> "Based on workspace documents, which statements about the evaluation discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | resident-evaluation-form.md rates 孙医生's procedural skills at 2/5, with overall "Below Expectations." | YES | Evaluation form | Direct fact |
| B | self-assessment-sun.md rates procedural skills at 4/5, with overall "Meeting Expectations." | YES | Self-assessment | Direct fact, C1 |
| C | The procedural skills gap is 2 points (2/5 vs 4/5) -- the largest discrepancy among all evaluation dimensions. | YES | Comparison | Quantitative |
| D | 林怡 cites three specific cases: Case A (thoracentesis off-target 1.5cm), Case B (guidewire 18cm vs standard 15cm), Case C (suture tension uneven). | YES | Evaluation form | Direct evidence |
| E | 孙医生's self-assessment notes training completion: rotations ✓, skills exam 82/100 ✓, case discussions 10 sessions ✓. | YES | Self-assessment | C3 data |
| F | 孙医生's rationale is outcome-focused: "所有操作遵循标准流程，结果良好，没有严重不良事件." | YES | Self-assessment | C1 framing |
| G | The self-assessment score of 4/5 is supported by the case log, which shows all procedures had acceptable outcomes. | NO | Outcomes were acceptable but process had deviations; 4/5 requires "操作规范，偶有小偏差" per standards | Conflates outcome with process |
| H | Team collaboration (4/5 from both evaluators) and professional attitude (4/5 from 林怡, 5/5 from 孙医生) show relative agreement on non-procedural dimensions. | YES | Both forms | Consistency observation |
| I | 林怡's evaluation is arbitrary and lacks supporting evidence. | NO | Evaluation cites 3 specific cases with objective findings | Fabricated |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R2: Case Log Discrepancies (MS-I)

**Question:**
> "Based on case-log-sun-doctor.md, which statements about the three cited cases are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Case A: 孙医生 recorded "穿刺顺利" but 林怡 noted puncture site 1.5cm medial to optimal location, near internal mammary artery path. | YES | Case log | Direct, C2 |
| B | Case B: 孙医生 recorded "操作顺利" but guidewire insertion depth was 18cm (3cm beyond the 15cm standard), with post-op X-ray showing catheter tip too low. | YES | Case log | Direct, C2 |
| C | Case C: 孙医生 recorded "伤口对合良好" but suture tension was uneven, requiring repair, with wider scarring noted at follow-up. | YES | Case log | Direct, C2 |
| D | In each case, 孙医生's own documentation describes the procedure as "顺利" (smooth) while objective findings (X-ray, measurements, follow-up) reveal deviations. | YES | Pattern across 3 cases | C2 pattern |
| E | The remaining 15 cases in the log show no significant procedural issues. | YES | Case log | Context |
| F | 3 out of 18 cases (16.7%) showing procedural deviations is within the expected error rate for PGY-2 residents. | NO | Depends on evaluation standards; the deviations are specific technique issues, not random errors | Premature normalization |
| G | 孙医生's self-documentation omitting deviations raises a documentation integrity concern separate from procedural skill. | YES | C2 + documentation analysis | Additional issue |
| H | None of the three cases resulted in serious adverse events requiring escalation. | YES | Case outcomes | Factual context |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R3-R30: Remaining Rounds (abbreviated)

### R3: Training Schedule (MS-R) -- C3 Non-conflict
**answer:** `["A", "B", "C", "D", "E", "G"]` -- rotations completed on time, skills exam passed (82/100), case discussions attended (10), all training milestones met, C3 confirmed as non-conflict, training completion does not equal procedural competency.

### R4: User Preference (P-R)
**answer:** `["A", "B", "C", "D", "E", "G"]` -- structured format, date+ID naming, conclusion first, evidence-based citations, concise professional, all 5 preferences.

### R5: C1 Reversal After Training Standards (DU-R) [Update 1]
**answer:** `["A", "B", "C", "D", "E", "G", "H"]` -- Section 4.2 "process compliance first," Section 4.3 "deviations without adverse events still count," scoring guide 2/5 = "technical deviations needing improvement," B1 "results matter" contradicted by standards, 林怡's evaluation aligns with formal criteria.

### R6: KPI Context (DU-I) [Update 2]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- KPI target ≥90%, current 9/10 if 孙医生 fails = 90% borderline, 张主任's pressure contextualized, Section 6.1 "clinical accuracy paramount" overrides KPI, B2 KPI concern is institutionally real but should not override evaluation standards.

### R7: Evidence Synthesis (MD-R, exec_check)
**answer:** `["A", "B", "C", "E", "F", "H"]` -- evaluation justified by standards + case evidence, B1 corrected (process > outcome), B2 weakened (standards > KPI), three independent evidence streams support 林怡's assessment, 孙医生's documentation integrity is a separate concern.

### R8: Historical Pattern (MS-I) [Update 3]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- 王医生 reveals same issues last year, previous evaluator gave "达标" under KPI pressure, pattern shows persistent skill gap, evaluation inflation prevented targeted training.

### R9-R30: Format analysis, source reliability, full reversal, bias identification, patient safety, case clinical analysis, format report, systemic pattern, institutional pressure, stakeholder impact, preferences, comprehensive synthesis, C3 confirmation, B2 identification, criteria application, remediation format, process vs outcome philosophy, evaluation integrity, remediation recommendations, medical education issues, final assessment.
