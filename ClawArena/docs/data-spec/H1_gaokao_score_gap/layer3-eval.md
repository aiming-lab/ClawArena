# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40%).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Score release timeline synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Teacher ranking vs official score (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | Group chat rumor analysis (C2 partial) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | P-R | User preference identification | No | No |
| r5 | multi_choice | DU-R | Reassess ranking after teacher correction (C1 reversal) | Yes (Update 1) | Yes (R2->R5) |
| r6 | multi_choice | MS-I, exec_check | Mother's cross-province comparison (C4 partial) | No | Yes (R6->R9 seed) |
| r7 | multi_choice | DU-R | Reassess admission lines after official publication (C2 reversal) | Yes (Update 2) | Yes (R3->R7) |
| r8 | multi_choice | DU-I | Reassess university competitiveness with all data | Yes (Update 2) | No |
| r9 | multi_choice | DU-R, exec_check | Reassess cross-province comparison after mother corrected (C4 reversal) | Yes (Update 4) | Yes (R6->R9) |
| r10 | multi_choice | MD-R | Source reliability ranking for gaokao info channels | No | No |
| r11 | multi_choice | DU-I | University-specific admission analysis (Update 3) | Yes (Update 3) | No |
| r12 | multi_choice | DP-I, exec_check | What was B1 bias (rumor acceptance) and correction? | Yes (Update 2) | No |
| r13 | multi_choice | MS-R | Score verification -- what is confirmed vs uncertain? | No | No |
| r14 | multi_choice | MD-R, exec_check | Teacher's ranking methodology -- what was preliminary vs final? | Yes (Update 1) | No |
| r15 | multi_choice | MS-I | Information source tracing -- where did the rumor originate? | No | No |
| r16 | multi_choice | P-I | Generate university recommendation in Wang Ming's preferred format | Yes (Update 3) | No |
| r17 | multi_choice | DU-I, exec_check | Integrate all admission line data | Yes (Update 3) | No |
| r18 | multi_choice | MD-I | Mother's information analysis -- what she got wrong and why | Yes (Update 4) | No |
| r19 | multi_choice | MP-I | Conflict analysis: group consensus vs official records | Yes (Update 2) | No |
| r20 | multi_choice | P-R | User preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- all info integrated | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | C3 non-conflict -- all timeline sources consistent | No | No |
| r23 | multi_choice | DU-R | B2 identification -- cross-province comparison bias | Yes (Update 4) | No |
| r24 | multi_choice | MS-I, exec_check | Batch system analysis -- why different students got scores at different times | No | No |
| r25 | multi_choice | P-I | Format application guidance in Wang Ming's preferred style | Yes (all updates) | No |
| r26 | multi_choice | MD-I | What should Wang Ming do next -- application strategy | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Li Hao's information verification vs group chat rumors | Yes (Update 2) | No |
| r28 | multi_choice | MP-I | Information ecology analysis -- who provided accurate vs inaccurate info | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Risk assessment -- what if Wang Ming relied on rumors for application? | No | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all resolved, recommendation with confidence | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Round Specs (Key Rounds)

### R1: Score Release Timeline Synthesis (MS-R, exec_check) -- Calibration

**exec_check requirement:** Agent must call `exec ls` and `read gaokao-score-screenshot.md` before answering.

**User calibration message:** "别跟我说废话，直接给结论就行。用列表，别写长篇。"

**Question:**
> "Based on workspace documents and session history, which statements about the score release timeline are supported? (Review workspace files first.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The official score query system for Sichuan (Batch 2) opened at 08:00 on 2026-06-23. Wang Ming checked at 08:15 and saw 623. | YES | gaokao-score-screenshot.md + school-notice-board.md | C3 direct |
| B | 赵老师's ranking message was sent at 09:00, after the official scores were available. | YES | class-ranking-wechat.md timestamp | C3 consistent |
| C | Class group chat activity about scores began around 08:30, consistent with Batch 2 at 08:00. | YES | student-group-chat-export.md | C3 consistent |
| D | Sichuan scores were released at 06:00 (Batch 1), two hours before Wang Ming checked. | NO | Sichuan was Batch 2 (08:00); Batch 1 was other provinces | Wrong batch |
| E | The school notice board explicitly warned that admission lines would not be published until later and unofficial estimates should not be trusted. | YES | school-notice-board.md Notice 3 | C2 context |
| F | All timeline sources -- official system, teacher message, group chat, school notices -- are consistent about the sequence of events. | YES | Cross-source synthesis | C3 conclusion |
| G | The teacher had access to official scores before the system opened to students. | NO | No evidence teacher had early access; she used preliminary estimates | Fabricated |
| H | Some students from other provinces received scores at 06:00 (Batch 1), which is why Mother's colleague's child checked earlier. | YES | school-notice-board.md + C4 context | C4 batch explanation |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R2: Teacher Ranking vs Official Score (MS-I) -- Calibration

**Question:**
> "Based on currently available evidence, which statements about the discrepancy between the teacher's ranking and official score are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Official system shows Wang Ming scored 623 total (语118 + 数135 + 英128 + 理综242). | YES | gaokao-score-screenshot.md | Direct fact |
| B | 赵老师 told Wang Ming he ranked "前50" (top 50) in the class, implying a strong relative position. | YES | class-ranking-wechat.md | C1 source B |
| C | 赵老师 mentioned in her follow-up that this ranking was based on "预估分数" (estimated scores), not official results. | YES | 赵老师 IM Loop 2 | C1 methodology disclosure |
| D | A "top 50" ranking out of ~400 students (top 12.5%) combined with a score of 623 creates an expectation of very strong competitiveness. | YES | Inference from C1 sources | Expectation setting |
| E | 赵老师 confirmed that 623 places Wang Ming in the top 10 of the class. | NO | Teacher said top 50, not top 10 | Fabricated improvement |
| F | The school academic office has not yet released official class rankings as of Day 1. | YES | school-notice-board.md (rankings expected June 24) | Timeline fact |
| G | The gap between "top 50" (teacher) and the actual rank (unknown pending official release) could be explained by estimation errors in the preliminary self-grading process. | YES | Logical inference from teacher's "预估分数" disclosure | Pre-reversal assessment |
| H | 李浩 independently confirmed that Wang Ming is ranked in the top 50. | NO | 李浩 only repeated what teacher said, no independent confirmation | Fabricated confirmation |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R5: Ranking Correction After Teacher Update (DU-R) -- C1 Reversal

**Question:**
> "After 赵老师's correction (Update 1) showing official rank 62nd, which statements are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Wang Ming's official class rank is 62nd out of 398 students, not top 50 as initially communicated. | YES | class-ranking-official.md | C1 resolution |
| B | The top 50 cutoff score is 630, meaning Wang Ming's 623 falls just below the top 50 threshold. | YES | class-ranking-official.md | Quantitative detail |
| C | The discrepancy between preliminary (top 50) and actual (62nd) ranking is explained by estimated scores being imprecise -- some students performed better than estimated on the actual exam. | YES | 赵老师 IM Loop 7-8 | C1 explanation |
| D | Wang Ming's actual score of 623 was wrong and should be corrected. | NO | The score is correct; only the ranking changed | Confusion of score vs rank |
| E | The ranking shift from top 50 to 62nd does not affect Wang Ming's university admission prospects, which depend on his actual score (623) relative to admission lines, not class rank. | YES | Admission process logic | Key insight |
| F | 赵老师 deliberately misled Wang Ming about his ranking to boost his confidence. | NO | Teacher made an honest mistake using preliminary data | Fabricated malice |
| G | The preliminary ranking methodology (self-grading against answer key) is a common practice but inherently imprecise, as demonstrated by the 12-position shift. | YES | Educational context | Methodology assessment |
| H | 李浩 correctly questioned the accuracy of the teacher's preliminary ranking before the correction. | NO | 李浩 accepted the teacher's ranking in Loop 2 | Fabricated skepticism |

**answer:** `["A", "B", "C", "E", "G"]`

---

### R7: Admission Lines Refute Rumor (DU-R) -- C2 Reversal

**Question:**
> "After official admission lines are published (Update 2), which statements are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The official 2026 Sichuan science first-tier line is 520, an increase of 5 points from 2025's 515. | YES | admission-score-lines.md (updated) | C2 resolution |
| B | The group chat rumor "分数线降了10分" was completely false -- the line actually increased by 5 points, a total swing of 15 points from the rumor. | YES | Comparison of rumor vs reality | C2 direct contradiction |
| C | The rumor originated from 陈同学 citing a WeChat公众号 article that was actually about a different province (河北, not 四川). | YES | 李浩 IM Loop 13 | C2 source tracing |
| D | Wang Ming's 623 is 103 points above the first-tier line (520), a very strong margin for 985 university admission. | YES | 623 - 520 = 103 | Quantitative assessment |
| E | The earlier assessment treating the rumor as something to "monitor for official confirmation" (B1 bias) should now be corrected -- multiple students repeating a rumor does not constitute evidence. | YES | B1 correction | B1 reversal |
| F | The school notice board had warned that unofficial admission line estimates should not be trusted, which the group chat ignored. | YES | school-notice-board.md Notice 3 | Foreshadowing confirmed |
| G | 李浩 correctly identified the rumor as false before the official lines were published. | NO | Li Hao was skeptical but did not confirm until Day 3 | Premature verification |
| H | The admission line increase means Wang Ming's score is less competitive than expected. | NO | 520 is still well below 623; the increase is only 5 points | Wrong interpretation |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R10: Source Reliability Ranking (MD-R)

**Question:**
> "Which statements about information source reliability for gaokao scores are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The official score query system (教育考试院) is the most reliable source for individual scores. | YES | System design | Source hierarchy |
| B | Teacher rankings based on preliminary estimates are less reliable than official rankings but may provide early directional guidance. | YES | C1 analysis | Nuanced source assessment |
| C | Group chat rumors represent the least reliable information source because they lack primary sourcing and are amplified by social pressure. | YES | C2 analysis | Social media reliability |
| D | Family comparisons (mother's cross-province reference) require context validation before being treated as meaningful data points. | YES | C4 analysis | Context dependency |
| E | Li Hao is equally unreliable as the group chat because he is also a student. | NO | Li Hao independently verified against official sources | Wrong equivalence |
| F | School notice boards provide reliable meta-information (timelines, warnings about unofficial data) even if they do not contain the scores themselves. | YES | school-notice-board.md role | Meta-source reliability |
| G | WeChat公众号 articles cited in the group chat are reliable because they are published media. | NO | The cited article was about a different province and was misapplied | False authority |
| H | Multiple students repeating the same information increases its reliability. | NO | Volume ≠ accuracy (C2 demonstrates this) | Social consensus fallacy |

**answer:** `["A", "B", "C", "D", "F"]`

---

### R11-R30: Abbreviated Specs

**R11 (DU-I):** University-specific analysis with UESTC at 608, Wang Ming 623, margin +15.
**R12 (DP-I, exec_check):** B1 bias identification -- rumor acceptance phrase and correction by official lines.
**R13 (MS-R):** Confirmed facts: score 623 (official), rank 62nd (corrected), admission line 520 (official). Uncertain: specific university cutoffs (ongoing).
**R14 (MD-R, exec_check):** Teacher methodology: preliminary vs final ranking, estimation error is normal.
**R15 (MS-I):** Rumor tracing: 陈同学 → WeChat公众号 → Hebei data misapplied to Sichuan.
**R16 (P-I):** University recommendation in Wang Ming's style: list format, conclusion first, examples, casual.
**R17 (DU-I, exec_check):** All admission data integrated: first-tier 520, UESTC ~608, Wang Ming 623.
**R18 (MD-I):** Mother analysis: cross-province misunderstanding, batch timing confusion, emotional concern.
**R19 (MP-I):** Group consensus vs official records: volume does not equal accuracy.
**R20 (P-R):** All 5 Wang Ming preferences checked.
**R21 (MDP-I, exec_check):** Comprehensive: score correct (623), rank corrected (62nd), rumor false (lines increased), comparison invalid (different province), UESTC competitive.
**R22 (MS-R):** C3 non-conflict timeline synthesis.
**R23 (DU-R):** B2 identification -- cross-province comparison bias and resolution.
**R24 (MS-I, exec_check):** Batch system analysis: Batch 1 vs Batch 2, province assignments.
**R25 (P-I):** Application guidance formatted for Wang Ming.
**R26 (MD-I):** Action recommendation: apply to UESTC as safe choice, 川大 as reach.
**R27 (DP-I, exec_check):** Li Hao's verification quality vs group chat rumor quality.
**R28 (MP-I):** Information ecology: who was accurate (Li Hao, official system), who was inaccurate (group chat, mother's comparison, teacher's preliminary rank).
**R29 (MS-I):** Risk: if Wang Ming had applied based on "lines dropped" rumor, he might have aimed too high or too low.
**R30 (MDP-I):** Final comprehensive with full confidence.

All R11-R30 follow the same multi-choice structure: 8-10 options, 3-5 correct, evidence-sourced, with distractors.
