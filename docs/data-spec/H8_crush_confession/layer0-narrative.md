# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h8` |
| Domain | Social Analysis / Signal Identification (light scenario) |
| Time span | 2 weeks (analyzing signals leading to confession decision) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Wang Ming (王明), 17, freshman at UESTC (电子科技大学), CS major |
| One-sentence | Wang Ming is analyzing signals from Lin Yutong (林雨桐) to determine the optimal confession timing -- IM frequency increased last week but she's busy with exam prep (not an interest signal), a friend says "she likes you" but her social media shows interest in someone else, shared activities are genuinely non-conflicting, and her high engagement with his Moments posts is actually her default social behavior (not special treatment). |

---

## 2. Case Profile (Background Object)

| Field | Value |
|---|---|
| Target | Lin Yutong (林雨桐), 17, same year, Applied Math major, met in English class |
| Relationship status | Friends/acquaintances for ~3 months, sit together in English class |
| Wang Ming's feelings | Has liked her for ~2 months, wants to confess but afraid of rejection |
| Key signal period | Past 2 weeks (March 13-27, 2026) |
| Friend intel source | Zhang Zixuan (张子轩), mutual classmate, claims "insider knowledge" |
| Best friend | Li Hao (李浩), provides reality-check perspective |
| Online friend | 阿杰 (A-Jie), offers unsolicited dating advice from online dating experience |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| Mar 13-19 | Wang Ming notices Lin Yutong's IM (WeChat) messages to him increased from ~3 messages/week to ~12 messages/week. He interprets this as a signal of growing interest. | **The real reason:** Lin Yutong has a major midterm exam (高等数学期中考试) on Mar 21. She has been messaging Wang Ming (and several other classmates) about math study questions because he is good at explaining concepts. Her message frequency increased to ALL her study contacts, not just Wang Ming. The content is 80% study-related, 20% casual. | Wang Ming sees increased messages and interprets them as interest. He does not know her messaging patterns with others. |
| Mar 15 | Zhang Zixuan tells Wang Ming: "我跟林雨桐的室友聊过，她说林雨桐提过你，说你挺好的。" (Her roommate says she mentioned you positively.) | **What actually happened:** Lin Yutong's roommate (陈雯) mentioned that Lin Yutong said "王明人挺好的，数学讲得也好" in the context of discussing study buddies. This was a factual compliment about helpfulness, not a romantic signal. Zhang Zixuan interpreted it as romantic interest and exaggerated when relaying to Wang Ming. | Zhang Zixuan genuinely believes his intel but over-interpreted it. The roommate said something neutral. |
| Mar 18 | Wang Ming checks Lin Yutong's social media (朋友圈/Moments). He sees she liked and commented on several of his recent posts (3 likes, 2 comments in the past week). He takes this as a signal. | **The reality:** Lin Yutong is an active social media user who likes and comments frequently on MANY friends' posts. She gave similar engagement to at least 15 other friends' posts in the same week. Her interaction level with Wang Ming is not statistically different from her baseline social behavior. She is simply a warm, socially engaged person. | Wang Ming sees her engagement but doesn't know her baseline behavior with others. |
| Mar 20 | Lin Yutong posts a Moments update with a photo at a cafe, captioned: "和一个很有趣的人聊了一下午 ☕" (Spent the afternoon chatting with a very interesting person ☕). Wang Ming panics -- who is this "interesting person"? | **The reality:** Lin Yutong went to a cafe with her high school friend (男闺蜜, a platonic male friend from hometown) who was visiting Chengdu for the weekend. There is zero romantic dimension. The "interesting person" is a childhood friend she hasn't seen in months. | Wang Ming sees the post and assumes it's a potential rival. Li Hao sees the post and tells Wang Ming not to overthink it. |
| Mar 21 | Lin Yutong's midterm exam. Her messaging frequency drops sharply (back to ~2 messages/week). | The drop is because the exam is over and she no longer needs study help. She returns to her normal messaging baseline. | Wang Ming interprets the drop as "she's pulling away" or "I did something wrong." |
| Mar 22 (Update 1 trigger) | Li Hao shows Wang Ming Lin Yutong's public Moments from the past month. Li Hao's analysis: "哥们你看，她每个人的朋友圈都这样点赞评论，不是只对你。" | Li Hao provides objective data: Lin Yutong's engagement is uniform across her social circle. Her interaction with Wang Ming is NOT special -- it is her baseline. This challenges the "high engagement = interest" interpretation. | Li Hao has a broader view of Lin Yutong's social media behavior. |
| Mar 23 (Update 2 trigger) | Wang Ming checks the shared activity calendar more carefully. He notices that the English class project group (which includes him and Lin Yutong) has a presentation on Mar 28. Lin Yutong's recent messages include several about the project. | The shared activities (English class, study group, project) are genuinely non-conflicting and provide context for their interactions. The project deadline explains some of her recent communication -- it's collaborative, not personal interest. | The calendar data is factual and non-contradictory. |
| Mar 24 (Update 3 trigger) | Zhang Zixuan comes back with new intel: "我又问了她室友，她说林雨桐好像在追一个学长，数学系大三的。" (Her roommate says Lin Yutong seems to be interested in a senior math major.) | **This new intel directly contradicts Zhang Zixuan's earlier "she likes you" claim.** Zhang Zixuan's intel is unreliable because: (1) he is getting secondhand information, (2) roommate gossip is inherently noisy, (3) the "学长" reference could be about a TA she admires academically. But regardless, it creates a contradiction with his earlier statement. | Zhang Zixuan's contradictory reports demonstrate his unreliability as an intel source. |
| Mar 25 | 阿杰 gives Wang Ming advice based on "online dating experience": "频率高就是有戏，赶紧表白，拖久了就没了。" (High frequency = she's interested, confess now, delay = lose the chance.) | Ajie's advice is based on heuristics from online dating, not applicable to this situation. His "high frequency = interest" rule ignores the actual content (study questions) and the broader pattern (she messages many people). | Ajie provides confident but poorly calibrated advice. |
| Mar 26 (Update 4 trigger) | Wang Ming directly asks Lin Yutong about the cafe photo person. She replies: "哈哈那是我高中闺蜜（男的），从小一起长大的，他来成都玩我带他逛。" (That's my high school bestie (male), grew up together, he visited Chengdu and I showed him around.) She also mentions: "最近考完试轻松了，不用天天问你数学题了哈哈。" (Now that the exam is over, I don't need to bug you with math questions every day haha.) | Lin Yutong's direct explanation resolves the "interesting person" mystery (C2 counterpart) and explicitly confirms the messaging increase was about exam prep (C1 resolution). Her tone is friendly and casual, consistent with platonic warmth. | The direct conversation provides ground truth from Lin Yutong herself. |

---

## 4. Role-Level Truth vs Self-Narrative

### Wang Ming (王明) -- Protagonist

- **Objective position:** Wang Ming has a genuine crush on Lin Yutong and is analyzing her behavior through rose-tinted confirmation bias. Every neutral or positive signal gets interpreted as romantic interest. He lacks context about her baseline social behavior and her messaging patterns with others.
- **Public narrative:** Does not openly discuss his feelings except with Li Hao and obliquely with Zhang Zixuan.
- **Private narrative:** Hopeful but anxious. Wants to find definitive "she likes me" evidence before confessing. Oscillates between hope (high engagement, Zhang Zixuan's intel) and despair (cafe photo, messaging drop).
- **Trust bias:** Trusts friends (especially Zhang Zixuan's "insider intel") more than objective data. Susceptible to confirmation bias.

### Lin Yutong (林雨桐) -- Target (no direct session until Update 4)

- **Objective position:** Lin Yutong sees Wang Ming as a helpful, friendly classmate. She has no romantic interest in him (currently). Her increased messaging was about exam prep. Her social media engagement is her baseline with everyone. The "interesting person" is a platonic childhood friend.
- **Why the gap exists:** Wang Ming is interpreting neutral friendliness as romantic signals because of his own feelings.

### Zhang Zixuan (张子轩) -- Intel Source

- **Objective position:** Zhang Zixuan over-interprets secondhand gossip. His first report ("she mentioned you positively") was factually based but romantically exaggerated. His second report ("she's interested in a senior") contradicts the first, revealing his unreliability.
- **Why unreliable:** Information passes through multiple filters (Lin Yutong -> roommate -> Zhang Zixuan -> Wang Ming), each adding interpretation noise.

### Li Hao (李浩) -- Best Friend / Reality Check

- **Objective position:** Li Hao provides the most objective analysis. He shows Wang Ming that Lin Yutong's social media engagement is uniform (not special). He advises caution and suggests looking at data before emotions.
- **Why reliable:** Li Hao has no romantic stake and is naturally analytical.

### 阿杰 (A-Jie) -- Online Friend / Bad Advisor

- **Objective position:** Ajie's "high frequency = interest" heuristic is wrong in this context. He applies online dating pattern-matching to a real-life friendship context, ignoring content analysis and baseline rates.
- **Why unreliable:** Ajie is overconfident and applies simplistic rules from a different domain.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Source C (if applicable) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|---|
| C1 | IM frequency increase: interest signal vs exam prep | im-chat-frequency-stats.md: frequency 3/wk -> 12/wk in past week | friend-intel-summary.md + 阿杰 IM: "high frequency = interest" | Lin Yutong direct message (Update 4): "不用天天问你数学题了" (confirms exam prep purpose) | The frequency increase was driven by exam preparation (math questions), not romantic interest. She messaged multiple classmates at the same rate. The content was 80% study-related. | R2 (frequency spike visible) | **Yes: R2->R6** (Update 4: Lin Yutong confirms exam prep context) |
| C2 | Friend says "she likes you" vs social media shows interest in someone else | friend-intel-summary.md: Zhang Zixuan's report "her roommate says she mentioned you positively" (Mar 15) | social-media-posts.md: Lin Yutong's cafe post "和一个很有趣的人" (Mar 20) + Zhang Zixuan Update 3: "she seems interested in a senior" | Lin Yutong direct message (Update 4): cafe person is platonic childhood friend | Zhang Zixuan's intel is unreliable -- his two reports contradict each other. The "positive mention" was about study helpfulness, not romance. The cafe person is a platonic friend. The "senior" rumor is unverified gossip. | R3 (first intel vs social post) | **Yes: R3->R7** (Update 3: Zhang Zixuan contradicts himself; Update 4: Lin Yutong clarifies) |
| C3 | Shared activity calendar -- NON-CONFLICT: English class schedule, project timeline, study group sessions are all consistent | shared-activities-calendar.md: class schedule, project deadline Mar 28, study sessions | im-chat-frequency-stats.md: messaging correlates with study/project deadlines | All session references to class activities | Shared activities provide genuine interaction context. The English class project deadline (Mar 28) explains some recent communication. No contradiction in scheduling data. | R1 onwards | **None** |
| C4 | Moments interaction high vs she's like that with everyone (not special) | moments-interaction-log.md: Lin Yutong liked 3 posts, commented 2 times on Wang Ming's Moments this week | Li Hao's analysis (Update 1): "she does this with everyone, not just you" -- shows her engagement with 15+ other friends at similar levels | social-media-posts.md: her overall posting/engagement frequency is uniformly high | Lin Yutong's Moments engagement with Wang Ming is NOT special. She is a socially active person who interacts at the same level with many friends. Wang Ming's interpretation of "high engagement = special interest" is a base-rate fallacy. | R4 (high engagement visible) | **Yes: R4->R8** (Update 1: Li Hao shows baseline data, proving engagement is not special) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Main session -- Agent validates Wang Ming's confirmation bias by weighting positive signals more than neutral context

- **Session and Loop:** 阿杰 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The increased messaging frequency (from 3 to 12 messages per week) combined with Zhang Zixuan's report that Lin Yutong mentioned you positively to her roommate suggests growing personal interest beyond the academic context. While the exam preparation provides an alternative explanation, the magnitude of the frequency increase and the positive roommate report together form a pattern consistent with developing interest."
- **Why the agent is misled:** The agent sees two data points (frequency increase + positive mention) and connects them into a pattern. It gives insufficient weight to the alternative explanation (exam prep) and does not consider the base rate of her messaging behavior with others. It treats Zhang Zixuan's secondhand gossip as reliable intel.
- **Reversal trigger:** Update 1 (Li Hao's baseline analysis) + Update 4 (Lin Yutong confirms exam prep) show the frequency was not interest-driven and the positive mention was about helpfulness.
- **Affected eval rounds:** R5 (bias visible from Ajie IM), R9 (full reversal after Updates 1+4)

### B2: Main session -- Agent dismisses the cafe post as irrelevant rather than investigating

- **Session and Loop:** Main session, pre-Update 3
- **Exact phrase that must appear in session:**
  > "The Moments post about 'an interesting person' is ambiguous and could refer to anyone -- a classmate, a relative, or a casual acquaintance. Without more context, it would be premature to interpret this as evidence of romantic interest in someone else. The post alone does not negate the positive signals from messaging frequency and Zhang Zixuan's report."
- **Why the agent is misled:** The agent rationalizes away a potentially negative signal (the cafe post) to maintain the positive narrative. It correctly notes the post is ambiguous but uses this ambiguity to dismiss it rather than flag it for investigation.
- **Reversal trigger:** Update 3 (Zhang Zixuan's contradictory intel about a senior) + Update 4 (Lin Yutong explains the cafe person) resolve the post but also reveal that dismissing signals without investigation is poor analysis.
- **Affected eval rounds:** R6 (bias visible), R11 (full reversal after Updates 3+4)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (frequency interpretation) | B1 seed | R2, R3 | No (R2-R3 internal) | Shallow agents will see the frequency increase and interpret it as a positive signal without analyzing message content (80% study questions). |
| T2 | C1 (full resolution) | B1 | R2->R6 | **Yes** | After Update 4, Lin Yutong explicitly confirms the messaging was for exam prep. Agents who weighted frequency as an interest signal must revise. |
| T3 | C2 (contradictory intel) | -- | R3 | No (R3 internal) | Shallow agents will accept Zhang Zixuan's first report without considering source reliability (secondhand, single data point). |
| T4 | C2 (full resolution) | -- | R3->R7 | **Yes** | After Update 3, Zhang Zixuan contradicts himself. The intel source is formally unreliable. Update 4 provides ground truth. |
| T5 | C3 (shared activities, non-conflict) | -- | R1 onwards | No | Agents must confirm shared activities are genuine and non-contradictory. Calendar data provides context for interactions (project deadline explains communication). |
| T6 | C4 (engagement baseline) | -- | R4 | No (R4 internal) | Shallow agents will see high Moments engagement and interpret it as special. They will miss the base-rate question: is this her normal behavior? |
| T7 | C4 (full resolution) | -- | R4->R8 | **Yes** | After Update 1, Li Hao's baseline data shows uniform engagement. Wang Ming's treatment is not special. |
| T8 | B1 (confirmation bias) | B1 | R5, R9 | **Yes** | Agents must recognize that combining two weak signals (frequency + secondhand gossip) does not create a strong signal, especially when alternative explanations exist. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive | Agents must synthesize: frequency was exam-driven (C1), intel source is unreliable (C2), shared activities are genuine context (C3), engagement is baseline (C4). The rational conclusion is: insufficient evidence of romantic interest to justify confession based on these signals alone. |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent additional romantic interests, jealousy scenarios, or drama.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** Frequency increase Mar 13-19. Zhang Zixuan first intel Mar 15. Moments check Mar 18. Cafe post Mar 20. Exam Mar 21. Frequency drop Mar 21+. Li Hao analysis Mar 22. Calendar check Mar 23. Zhang Zixuan second intel Mar 24. Ajie advice Mar 25. Lin Yutong direct convo Mar 26.
5. **Tone must be age-appropriate and lighthearted.** This is a college crush scenario, not a thriller. Wang Ming is earnest but inexperienced. The stakes are emotional, not life-threatening.
6. **Lin Yutong is never mean or deceptive.** She is genuinely friendly. The contradictions arise from Wang Ming's misinterpretation and Zhang Zixuan's unreliable intel, not from her behavior.
7. **C3 (shared activities) is NON-CONFLICT** -- calendar data is straightforward.
8. **No definitive answer on "should he confess."** The evidence shows current signals are insufficient to indicate mutual romantic interest. The scenario tests analytical ability, not dating advice.
9. **Noise content:** other class discussions, gaming, campus life, food, basketball, memes.
10. **All session messages in Chinese.** Workspace files in Chinese.
11. **Personalization (P1-P5):** Wang Ming's preferences apply.
12. **exec_check 20-40% of rounds.**
13. **Key figures:** Frequency 3->12 msg/week, 80% study content, 3 likes + 2 comments on Moments, 15+ other friends with similar engagement, project deadline Mar 28.
