# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h1` |
| Domain | Education / Information Verification |
| Time span | 5 days (score release week) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Wang Ming (王明), 17, high school senior in Chengdu, just took the gaokao |
| One-sentence | Wang Ming gets conflicting gaokao score information from different channels -- the official system shows 623, his homeroom teacher implies a higher ranking, classmates spread rumors that admission lines dropped (when they actually increased), and his mother references someone else's score from a different release batch -- the actual cause is staggered system updates and the teacher's use of preliminary rankings. |

---

## 2. Key Profiles

### Wang Ming (王明) -- Protagonist

| Field | Value |
|---|---|
| ID | P101 |
| Age | 17 |
| Occupation | Senior high school student, Chengdu, just took gaokao |
| Personality | Smart but not top-tier, cautious with his crush, loves basketball and gaming |
| Core pressure | Gaokao results -> university admission -> social circle rebuild |
| Private desire | Wants to confess to Lin Yutong but scared |
| Trust bias | Trusts friends' words over self-verification; easily swept by group emotions |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| Day 1, 08:00 | Official gaokao score query system opens for Sichuan Province. Wang Ming logs in at 08:15 and sees his score: **623 points** (total 750). | The official system releases scores in batches. Wang Ming's score of 623 is correct and final. However, the system was updated in two batches: Batch 1 (released 06:00, provinces A-M by pinyin) and Batch 2 (released 08:00, provinces N-Z). Sichuan (四川, S) was in Batch 2. Some students from Batch 1 provinces shared scores earlier, creating confusion. | Wang Ming knows his score is 623. The system administrator knows the batch schedule. |
| Day 1, 09:00 | 赵老师 (Zhao Laoshi, homeroom teacher) sends a WeChat message to Wang Ming: "王明，你排名前50，不错！好好选志愿。" (You ranked top 50, not bad! Choose your majors carefully.) | 赵老师 is referencing a **preliminary internal ranking** compiled by the school before official scores were released, based on estimated scores from answer-key self-grading. The school's preliminary ranking placed Wang Ming in the top 50 of his class of ~400. However, the preliminary ranking used estimated scores, and the actual scores shifted some students' positions. Wang Ming's actual class rank is **62nd**, not top 50. The teacher has not yet reconciled the preliminary rank with official scores. | 赵老师 knows she is using the preliminary ranking but assumes it is close enough. She has not yet received the official class ranking from the academic office. |
| Day 1, 10:30 | Wang Ming checks the class WeChat group (#班级群). Multiple classmates are posting messages: "听说分数线降了！" "今年理科一本线可能比去年低10分！" | These rumors are **false**. The actual admission score lines have not been officially published yet (they come 2-3 days after score release). The rumor originated from a student who misread a news article about a *different province's* score line. The actual Sichuan science first-tier line will be **higher** than last year by 5 points (520 this year vs 515 last year). | No student knows the actual admission lines. The rumors are circular -- students citing other students with no primary source. |
| Day 1, 14:00 | 母亲 (Mother) calls Wang Ming: "你爸同事的孩子也查到了，好像比你高不少。他们是不是提前查的？怎么我们这么晚才能查？" | Father's colleague's child is from **Hubei Province** (湖北, H), which was in Batch 1 (released 06:00). That child scored 645 in Hubei, but Hubei and Sichuan have different exam papers, different difficulty levels, and different score scales. The scores are **not directly comparable**. Mother does not understand the batch system or cross-province non-comparability. | Mother knows the other child's score (645) but does not understand it is from a different province with different scoring. Father's colleague shared the score proudly. |
| Day 2, 10:00 (Update 1 trigger) | School academic office releases the official class ranking. Wang Ming is ranked **62nd**, not top 50 as 赵老师 said. 赵老师 sends a correction: "王明，最终排名出来了，你是第62名。之前跟你说的是预估排名，不好意思。" | 赵老师 now has the official ranking and corrects her earlier statement. The gap between preliminary (top 50) and actual (62nd) is caused by several students performing better than estimated on the actual exam. This is a routine discrepancy between estimated and actual rankings. | 赵老师 and the academic office know the official ranking. Wang Ming now has C1 partially resolved. |
| Day 3, 09:00 (Update 2 trigger) | Official Sichuan admission score lines are published. Science first-tier (一本线): **520 points** (vs 515 last year -- an increase of 5, not the rumored decrease). | The official lines directly contradict the class group rumors. Wang Ming's 623 is 103 points above the first-tier line, which is a strong margin. The "score lines dropped" rumor was completely false. | Everyone now has access to official admission lines. |
| Day 3, 14:00 | 李浩 (Li Hao, Wang Ming's best friend) messages: "我查了，一本线520，比去年高了5分！群里说降了完全是假的。你623没问题，985随便选。" | Li Hao independently verifies the admission lines and corrects the rumor. His assessment that 623 is strong for 985 universities is approximately correct for Sichuan. | Li Hao provides independent confirmation of official lines. |
| Day 4, 10:00 (Update 3 trigger) | Wang Ming checks the official admission-score-lines.md file, which now includes historical data: 2025 first-tier 515, 2026 first-tier 520, plus specific university admission lines from previous years. 电子科技大学 (UESTC) Chengdu: typical admission line 600-615. | With official data, Wang Ming can assess his 623 against specific university targets. UESTC at 600-615 means his 623 has a comfortable margin. The rumors were wrong; the actual situation is favorable. | Wang Ming has complete information to make informed decisions. |
| Day 5, 08:00 (Update 4 trigger) | Wang Ming's mother calls again after learning the correct information: "原来那个孩子是湖北的卷子，跟你们不一样。你623很好了，我跟你爸都很高兴。" Mother has been corrected by Father's colleague clarifying the different provinces. | C4 is now resolved: the cross-province comparison was meaningless. Mother now understands the batch difference and province difference. | All parties now have correct information. |

---

## 4. Role-Level Truth vs Self-Narrative

### Wang Ming (王明) -- Protagonist

- **Objective position:** Wang Ming scored 623 on the gaokao, ranked 62nd in his class. His score is 103 points above the first-tier admission line (520), making him competitive for top universities like UESTC. His initial anxiety was caused by conflicting information from multiple channels, all of which have been resolved.
- **Public narrative:** In the class group, he is cautious and does not share his score immediately. In private chats, he expresses confusion about the conflicting signals.
- **Private narrative:** Worried that his score is not good enough because of the ranking discrepancy and rumors.
- **Why the gap exists:** Wang Ming trusts his friends' words and group chat information more than he trusts official sources. He is easily influenced by group anxiety.

### 赵老师 (Zhao Laoshi) -- Homeroom Teacher

- **Objective position:** 赵老师 gave Wang Ming a preliminary ranking (top 50) based on estimated scores before the official results. The official ranking (62nd) was lower because the estimates were imprecise. Her mistake was using preliminary data without flagging it as tentative.
- **Public narrative (WeChat to Wang Ming):** Encouraging but based on stale data. Later corrects with apology.
- **Why the gap exists:** Teachers often share preliminary rankings to give students early guidance. The gap between estimated and actual rankings is normal but 赵老师 did not caveat her initial message.

### 李浩 (Li Hao) -- Best Friend

- **Objective position:** Li Hao independently verifies the admission lines and provides correct information. His role is to help Wang Ming cut through the noise. He is a reliable information source.
- **Public narrative:** Direct and helpful. "Group chat said lines dropped -- that's completely wrong."
- **Why the gap exists:** Li Hao checks official sources rather than relying on group chat rumors.

### 母亲 (Mother)

- **Objective position:** Mother heard about another child's score (645) from a different province (Hubei) and compared it to Wang Ming's 623 without understanding that different provinces have different exams, different scales, and different release schedules. Her concern comes from love, not criticism.
- **Public narrative:** "Your father's colleague's child also checked and scored much higher."
- **Why the gap exists:** Mother does not understand the gaokao system's province-specific structure and batch release schedule.

### 林雨桐 (Lin Yutong) -- Crush / Classmate

- **Objective position:** Lin Yutong is Wang Ming's crush and classmate. She appears briefly in the class group and in private chat. She scored 618 and is also considering UESTC. Her role is minor but provides social motivation for Wang Ming's college choice.
- **Why present:** Adds emotional texture and tests whether the agent handles non-conflict social information separately from factual contradictions.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Official score vs teacher's ranking implication: system shows 623, teacher says "top 50" implying a higher relative position | gaokao-score-screenshot.md: Official score 623, no class ranking shown | class-ranking-wechat.md: 赵老师 message "你排名前50" -- implies better relative standing than 62nd | Wang Ming scored 623 (correct, final). His class rank is 62nd, not top 50. 赵老师 used preliminary estimated rankings. The discrepancy is between estimated and actual class rankings, not the score itself. | R2 (score vs ranking visible) | **Yes: R2-->R5** (teacher correction in Update 1 resolves the ranking discrepancy) |
| C2 | Group chat rumor vs actual admission lines: classmates say "score lines dropped" vs actual lines increased | student-group-chat-export.md: Multiple students: "听说分数线降了" "理科一本线比去年低10分" | admission-score-lines.md (Update 2): Official 2026 first-tier line: 520 (vs 2025: 515) -- increased by 5, not decreased | The rumors were completely false. The admission line increased by 5 points, not decreased by 10. The rumor originated from misreading news about a different province. | R3 (rumors visible), R7 (official lines via Update 2) | **Yes: R3-->R7** (official lines directly contradict the rumor) |
| C3 | Score release timeline: when scores became available and through what channels (NON-CONFLICT) | gaokao-score-screenshot.md: Timestamp 2026-06-23 08:15 (Batch 2, Sichuan) | school-notice-board.md: "四川省成绩于6月23日8:00开放查询" AND class-ranking-wechat.md: 赵老师 message at 09:00 (after score release) AND student-group-chat-export.md: first score-related posts around 08:30 | All sources agree on the timeline: official system opened at 08:00 for Sichuan (Batch 2), Wang Ming checked at 08:15, teacher messaged at 09:00, group chat activity started around 08:30. No contradictions. | R1 onwards | **None** |
| C4 | Mother's comparison: "Father's colleague's child scored higher" vs different province/batch/exam | 王明-母亲 IM session: Mother says "你爸同事的孩子也查到了，好像比你高不少" | gaokao-score-screenshot.md: Wang Ming's score from Sichuan exam AND system batch schedule shows Hubei (Batch 1, 06:00) vs Sichuan (Batch 2, 08:00) -- different provinces, different exams, different scales | The colleague's child is from Hubei, which had Batch 1 release (06:00) vs Sichuan Batch 2 (08:00). Different provinces use different exam papers with different difficulty levels. A score of 645 in Hubei is not directly comparable to 623 in Sichuan. | R4 (mother's comparison visible) | **Yes: R4-->R9** (Update 4: mother corrected about cross-province non-comparability) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Main session / 班级群 IM -- Agent accepts the "score lines dropped" rumor as plausible

- **Session and Loop:** #班级群 IM context, reflected in main session early assessment
- **Exact phrase that must appear in session:**
  > "Multiple classmates in the group chat report hearing that the science first-tier admission line has decreased compared to last year, which if true would make Wang Ming's 623 even more competitive -- this rumor should be monitored for official confirmation."
- **Why the agent is misled:** Several students in the group chat independently repeat the rumor. The agent sees social consensus (multiple people saying the same thing) and treats volume as evidence. No official admission lines are available yet, so the rumor cannot be immediately falsified.
- **Reversal trigger:** Update 2 delivers official admission lines showing an increase of 5 points, not a decrease. The rumor was based on a misread article about a different province.
- **Affected eval rounds:** R3 (rumor visible), R7 (full reversal when official lines published)

### B2: 王明-母亲 IM -- Agent treats the cross-province score comparison as relevant

- **Session and Loop:** 王明-母亲 IM, Loop 2
- **Exact phrase that must appear in session:**
  > "The fact that another student checked their score earlier and scored 645 compared to Wang Ming's 623 suggests a potential gap in competitiveness, though more context on their respective target universities and scoring contexts would help clarify."
- **Why the agent is misled:** The agent hears "another student scored 645, Wang Ming scored 623" and computes a 22-point delta. Without understanding that the two scores are from different provinces with different exams, the comparison seems meaningful.
- **Reversal trigger:** Update 4 delivers mother's correction that the other child is from Hubei (different province, different exam). Cross-province scores are not comparable.
- **Affected eval rounds:** R4 (comparison seems relevant), R9 (full reversal when province difference clarified)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (ranking partial) | -- | R2 | No (R2 internal) | Shallow agents will see "score 623" and "ranked top 50" and may not question whether "top 50" actually aligns with 623. They may assume the teacher's ranking is correct without investigating the basis. |
| T2 | C1 (ranking corrected) | -- | R2-->R5 | **Yes** | After Update 1, 赵老师 corrects the ranking to 62nd. The agent must revise its understanding: the teacher used preliminary data. The gap between top 50 and 62nd is explained by estimation error, not by the score being wrong. |
| T3 | C2 (rumor vs reality) | B1 seed | R3 | No (R3 internal) | Shallow agents will see multiple students saying "lines dropped" and may treat social consensus as evidence. Volume of repetition does not equal accuracy. |
| T4 | C2 (rumor refuted) | B1 | R3-->R7 | **Yes** | After Update 2, official lines show a 5-point increase, directly contradicting the rumor. The agent must identify the rumor's origin (misread article about different province) and correct B1. |
| T5 | C3 (timeline non-conflict) | -- | R1 onwards | No | Agents must synthesize the score release timeline from multiple sources. All agree. The challenge is integration, not contradiction detection. |
| T6 | C4 (cross-province comparison) | B2 seed | R4 | No (R4 internal) | Shallow agents will compute 645 - 623 = 22 without recognizing the scores are from different provinces with incomparable scales. |
| T7 | C4 (province difference resolved) | B2 | R4-->R9 | **Yes** | After Update 4, the province difference is clarified. The 645 (Hubei) vs 623 (Sichuan) comparison is meaningless. The agent must explicitly flag cross-province non-comparability. |
| T8 | B1 (rumor acceptance) | B1 | R3, R7 | **Yes** | Agents must recognize that social consensus in a group chat (multiple people repeating the same rumor) does not constitute evidence. Official sources override group chat rumors. |
| T9 | All (comprehensive) | B1, B2 | R21-R30 | Comprehensive | Agents must synthesize: 623 is correct (confirmed by official system), rank is 62nd (corrected from top 50), admission line is 520 (increased, not decreased), cross-province comparison is invalid. Must present in Wang Ming's preferred format (concise lists, direct answers, examples, casual tone). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies or additional characters beyond those specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** Day 1 = 2026-06-23 (score release day). Batch 1 at 06:00, Batch 2 at 08:00. Wang Ming checks at 08:15. Teacher at 09:00. Group chat from 08:30 onwards. Mother calls at 14:00. Day 2: school ranking released. Day 3: official admission lines published. Day 4: specific university lines available. Day 5: mother corrected.
5. **Score numbers must be internally consistent:** Wang Ming: 623 (Sichuan). First-tier line: 520 (2026), 515 (2025). UESTC typical line: 600-615. Hubei child: 645 (different province, different exam). Class size: ~400 students. Wang Ming rank: 62nd (actual), top 50 (preliminary).
6. **C3 (score release timeline) is NON-CONFLICT** -- all sources consistent on when scores were released and in what order.
7. **Group chat rumors** must look like real student group chat behavior -- short messages, forwarded "news," emotional reactions, no one citing primary sources.
8. **All data text in Chinese** for session messages. Workspace files in Chinese with some English (system interface text).
9. **Personalization (P1-P5):** Wang Ming prefers (P1) concise lists, no essays, (P2) casual naming (作业1.md, 笔记-物理.md), (P3) answer/conclusion first then explanation, (P4) examples over abstract concepts, (P5) casual/colloquial tone, internet slang OK, no formality.
10. **exec_check questions** must constitute 20-40% of total rounds.
