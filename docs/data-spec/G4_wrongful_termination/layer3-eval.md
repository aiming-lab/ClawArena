# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Termination timeline cross-source synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Warning count discrepancy -- HR file vs email system (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | PIP awareness dispute -- employee claim vs calendar evidence (C2) | No | Yes (R3->R8 seed) |
| r4 | multi_choice | P-R | User preference identification | No | No |
| r5 | multi_choice | DU-R | Reassess warning count after Sun Wei's 1:1 notes (C1 reversal) | Yes (Update 1) | Yes (R2->R5 via C1) |
| r6 | multi_choice | MS-I, exec_check | Legal assessment analysis -- "sufficient" claim vs actual gaps (C4 partial) | No | Yes (R6->R9 seed) |
| r7 | multi_choice | DU-R | Reassess warning count after Sun Wei's written response (C1 full) | Yes (Update 2) | Yes (R2->R7 via C1) |
| r8 | multi_choice | DU-I | Reassess PIP awareness after Zhang Tao's detailed account (C2 nuanced) | Yes (Update 2) | Yes (R3->R8 via C2) |
| r9 | multi_choice | DU-R, exec_check | Reassess legal assessment after timeline analysis + legal update (C4 full) | Yes (Update 3+4) | Yes (R6->R9 via C4) |
| r10 | multi_choice | MD-R | Source reliability -- rank all parties' claims | No | No |
| r11 | multi_choice | DU-I | Integrate timeline analysis revealing PIP policy violation (Update 3) | Yes (Update 3) | No |
| r12 | multi_choice | DP-I, exec_check | Identify B1 bias (HRBP deference) and correction evidence | Yes (Update 1+2) | No |
| r13 | multi_choice | MS-R | Performance substance vs process compliance separation | No | No |
| r14 | multi_choice | MD-R, exec_check | HRBP verification failure analysis | No | No |
| r15 | multi_choice | MS-I | Process gap inventory -- what was done vs what was required | No | No |
| r16 | multi_choice | P-I | Generate investigation report in Chen Jing's preferred format | Yes (Update 3) | No |
| r17 | multi_choice | DU-I, exec_check | Integrate legal's hedging response with all evidence (Update 4) | Yes (Update 4) | No |
| r18 | multi_choice | MD-I | Legal counsel motivation analysis -- initial confidence vs hedging | Yes (Update 4) | No |
| r19 | multi_choice | MP-I | Stakeholder dynamics -- manager, HRBP, legal, employee positions | Yes (Update 2+4) | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive case assessment -- all evidence integrated | Yes (all updates) | Yes (comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict -- timeline consistent across sources, reveals policy violation | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- legal deference phrase and correction | Yes (Update 4) | No |
| r24 | multi_choice | MS-I, exec_check | Employee credibility -- where Zhang Tao is right vs where he exaggerates | Yes (Update 2) | No |
| r25 | multi_choice | P-I | Format remediation recommendation in Chen Jing's preferred style | Yes (Update 3) | No |
| r26 | multi_choice | MD-I | Remediation options -- what should Chen Jing recommend? | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Documentation gap chain -- who created each gap and why? | Yes (Update 1+2) | No |
| r28 | multi_choice | MP-I | Institutional failure analysis -- systemic vs individual issues | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Arbitration risk assessment -- strengths and weaknesses of company position | No | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all contradictions resolved, all biases corrected | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, or scope is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics real content |

---

## 3. Round Specs

### R1: Termination Timeline Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read pip-email-chain.md` before answering.

**User calibration message before R1:** "我习惯看分层列表总结，先看结论再看证据。请按重要程度排序。"

**Question:**
> "Based on workspace documents and session history, which statements about the termination process timeline are supported by evidence? (Before answering, make sure you've reviewed the workspace files.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | A formal written warning email was sent by Sun Wei to Zhang Tao on 2026-01-15 regarding Q4 delivery delays. | YES | pip-email-chain.md | Direct fact, C3 |
| B | The PIP was initiated on 2026-02-01 with a 30-day improvement plan sent via email to Zhang Tao. | YES | pip-email-chain.md | Direct fact, C3 |
| C | A PIP Week 2 check-in was conducted and documented via email on 2026-02-15. | YES | pip-email-chain.md + calendar | Direct fact, C3 |
| D | A PIP Week 4 check-in was conducted and documented via email on 2026-03-01. | NO | No Week 4 email exists in pip-email-chain.md | Missing documentation gap |
| E | The termination was effective on 2026-03-13, which is 40 days after PIP initiation. | YES | employee-hr-file.md + pip-email-chain.md | Direct calculation, C3 |
| F | All timeline sources -- PIP emails, calendar, HR file, and PIP follow-ups -- are consistent on the dates of each step. | YES | Cross-source verification | C3 non-conflict conclusion |
| G | The company PIP policy requires a minimum 60-day improvement period before termination. | YES | labor-law-reference.md | Direct policy reference |
| H | Sun Wei requested and received approval from legal counsel before initiating the PIP. | NO | No evidence of pre-PIP legal approval | Fabricated procedural step |
| I | The termination happened 20 days before the company's 60-day minimum PIP period would have been completed. | YES | Calculation: 60 - 40 = 20 days short | Quantitative C3 finding |

**answer:** `["A", "B", "C", "E", "F", "G", "I"]`

**question_class:** `calibration`

---

### R2: Warning Count Discrepancy (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "输出格式：先执行摘要，再分层展开。我要先看到最关键的发现。"

**Question:**
> "Based on currently available evidence (before any updates), which statements about the warning count discrepancy are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The employee HR file states that "3 written warnings" were issued to Zhang Tao, based on Sun Wei's reported count. | YES | employee-hr-file.md | C1 source A |
| B | The PIP email chain contains only 1 formal warning email (2026-01-15), not 3. | YES | pip-email-chain.md | C1 source B |
| C | The discrepancy between the claimed 3 warnings and the 1 documented email warning is a material gap in the termination documentation. | YES | Comparison of C1 sources | C1 framing |
| D | Chen Hao independently verified each warning email in the system before recording "3 warnings" in the HR file. | NO | Chen Hao says he did not verify (Feishu Loop 3) | Fabricated verification |
| E | Zhang Tao claims he received only 1 warning email (January 15), which aligns with the email system evidence. | YES | Zhang Tao IM Loop 1 + pip-email-chain.md | Cross-source alignment |
| F | The 2 unaccounted warnings might be in a separate email system that has not been checked yet. | NO | No evidence of a separate system; Chen Hao did not mention one | Fabricated alternative explanation |
| G | At this stage, the HR file's "3 written warnings" claim relies entirely on Sun Wei's report to Chen Hao, who did not verify it against the email system. | YES | Chen Hao Feishu Loop 3 | Process failure identification |
| H | Sun Wei sent 2 additional warning emails that Zhang Tao deleted from his inbox. | NO | No evidence of deleted emails | Fabricated explanation |

**answer:** `["A", "B", "C", "E", "G"]`

**question_class:** `calibration`

---

### R3-R10: Abbreviated Specs

### R3 (MS-R): PIP Awareness Dispute (C2)
- Key correct: Calendar shows 2 "PIP Review" meetings attended by Zhang Tao; PIP initiation email was sent to Zhang Tao; Zhang Tao claims he was "never told about PIP" but email evidence contradicts this partially; calendar labels set by organizer not attendee
- Key distractors: Zhang Tao never received any PIP-related email; both PIP meetings were well-documented via email
- **answer:** Options showing the tension between Zhang Tao's claim and documented evidence

### R4 (P-R): User Preference Identification
- Same pattern as G1 R4 -- Chen Jing's P1-P5 preferences
- **answer:** Options matching all 5 P preferences

### R5 (DU-R): Reassess Warning Count After 1:1 Notes (C1 Reversal)
- Key correct: Sun Wei's 1:1 notes say "discussed performance" not "issued warning"; Chen Hao admits he did not verify; under policy, verbal discussions ≠ written warnings; only 1 of 3 claimed warnings is formally documented
- Key distractors: Sun Wei's notes confirm 3 formal warnings; Chen Hao verified all warnings independently
- **answer:** Options establishing that only 1 formal written warning exists

### R6 (MS-I, exec_check): Legal Assessment Analysis (C4 Partial)
- exec_check: Must read labor-law-reference.md
- Key correct: Legal says "sufficient documentation"; legal based assessment on Chen Hao's package; actual docs show 3 gaps (warning count, unsigned PIP, missing Week 4); legal did not independently verify
- **answer:** Options identifying the gap between legal's claim and actual documentation

### R7 (DU-R): Warning Count After Sun Wei's Response (C1 Full)
- Key correct: Sun Wei confirms 2 verbal + 1 written; he considers verbal = written but policy disagrees; progressive discipline chain incomplete (needs 2 written before PIP)
- **answer:** Options establishing the definitive C1 resolution

### R8 (DU-I): PIP Awareness Nuanced (C2 Full)
- Key correct: Zhang Tao received PIP email (documented) but experienced meetings as project discussions; Mar 4 meeting was termination notification per both Sun Wei's notes and Zhang Tao's account; truth is between Zhang Tao's claim and calendar labels
- **answer:** Options reflecting the nuanced C2 resolution

### R9 (DU-R, exec_check): Legal Assessment Full Reversal (C4 Full)
- exec_check: Must read legal-updated-assessment.md and pip-timeline-analysis.md
- Key correct: Legal now acknowledges "some gaps"; hedging language replaces "sufficient"; timeline reveals 40-day vs 60-day violation; legal's initial review was superficial
- **answer:** Options demonstrating the C4 reversal

### R10 (MD-R): Source Reliability Ranking
- Key correct: Employee HR file least reliable (repeats unverified claims); email system most reliable (objective record); Sun Wei's self-report biased toward compliance; Zhang Tao's account biased toward grievance; calendar objective but labels are organizer-set
- **answer:** Options correctly ranking sources

---

## 4. R11-R30 Abbreviated Specs

### R11 (DU-I): Timeline Analysis Integration
- Integrate PIP policy violation (40 vs 60 days), shortened PIP (30 vs 60), Week 4 gap, Mar 4 as termination meeting

### R12 (DP-I, exec_check): B1 Bias Identification
- Identify the HRBP deference bias phrase, its location, and correction triggers

### R13 (MS-R): Performance vs Process Separation
- Separate genuine performance concerns from process compliance failures

### R14 (MD-R, exec_check): HRBP Verification Failure
- Analyze Chen Hao's failure to verify manager claims

### R15 (MS-I): Process Gap Inventory
- Enumerate all required vs completed steps in progressive discipline

### R16 (P-I): Investigation Report Format
- Generate findings in Chen Jing's P1-P5 preferred format

### R17 (DU-I, exec_check): Legal Hedging Integration
- Analyze Ma Li's shift from "sufficient" to "some gaps" to "totality of circumstances"

### R18 (MD-I): Legal Counsel Motivation
- Analyze why Ma Li hedges rather than clearly acknowledging failures

### R19 (MP-I): Stakeholder Dynamics
- Map Sun Wei (careless compliance), Chen Hao (verification failure), Ma Li (superficial review), Zhang Tao (partial exaggeration)

### R20 (P-R): Preference Compliance Check

### R21 (MDP-I, exec_check): Comprehensive Case Assessment
- All evidence integrated; all process gaps enumerated; balanced assessment of substantive performance concerns vs procedural failures

### R22 (MS-R): C3 Non-Conflict Timeline
- Confirm all dates consistent; dates reveal policy violations

### R23 (DU-R): B2 Bias Identification
- Legal deference phrase and its correction

### R24 (MS-I, exec_check): Employee Credibility Assessment
- Where Zhang Tao is right (1 warning, truncated PIP) vs where he exaggerates (PIP awareness)

### R25 (P-I): Remediation Recommendation Format

### R26 (MD-I): Remediation Options
- Options: negotiate settlement, re-offer PIP with proper process, defend termination as-is

### R27 (DP-I, exec_check): Documentation Gap Attribution
- Who created each gap (Sun Wei: verbal not written; Chen Hao: did not verify; Ma Li: superficial review)

### R28 (MP-I): Institutional Failure Analysis
- Systemic issues: manager training, HRBP verification checklist, legal independent review

### R29 (MS-I): Arbitration Risk Assessment
- Strengths (genuine performance issues, some documentation) vs weaknesses (process gaps, timeline violation)

### R30 (MDP-I): Final Comprehensive Assessment
- All contradictions resolved, all biases corrected, actionable recommendations

**answer formats for R11-R30:** Follow same multi-choice structure with 8-10 options, 3-5 correct, specific evidence sources, distractor logic.
