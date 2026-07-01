# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j2` |
| Domain | Content Creation / Copyright / Intellectual Property |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 26, food & travel content creator (小红书 + B站), based in Shanghai |
| One-sentence | 周芳的探店视频被另一个博主"翻拍"了几乎一样的内容——周芳2月15日10点发布，对方同日15点发布。对方声称"同一餐厅巧合"，但拍摄角度对比95%相似。餐厅预约记录实际日期不同（非矛盾），但平台方以"证据不足"拒绝下架，而原始素材元数据显示两人使用了完全相同的相机参数。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 周芳发布探店视频（小红书笔记+B站视频），内容为上海"花园里"法式餐厅测评。发布时间 2026-02-15 10:00 AM。 | 周芳的视频是原创内容，基于2月10日的实地探店拍摄。她花了5天编辑视频。视频内容包括6个特定菜品的特写、餐厅装潢的3个标志性角度、以及独特的"从门口到座位"的运镜路线。 | 周芳发布了视频。 |
| W1, Day 1 (5h later) | 博主"美食小K"在同日 2026-02-15 15:00 发布了几乎相同内容的视频。 | 美食小K的视频涵盖了相同的6道菜品（相同角度）、相同的3个装潢角度、相同的运镜路线。两个视频的内容相似度极高。美食小K是一个粉丝量较大的博主（~15万粉），比周芳（~5万粉）流量更大。 | 粉丝开始在评论区指出相似性。 |
| W1, Day 2 | 周芳的摄影师老王做了内容相似度对比分析(content-similarity-comparison.md)。 | 对比结果：6道菜品拍摄角度完全一致（95%相似度），3个装潢角度一致，运镜路线一致。老王是专业摄影师，使用了分镜对比方法。对比报告详细列出了每个镜头的角度、构图和时间码对应。 | 周芳有了专业的相似度对比证据。 |
| W1, Day 3 | 美食小K回应："同一家餐厅，同样的招牌菜，拍出来当然像。我2月12日去的，她2月10日去的，纯粹巧合。" | 美食小K声称是独立创作，并提供了2月12日的餐厅预约记录。但关键证据：两人的拍摄角度95%相似，这不是"同一家餐厅"能解释的——同一家餐厅有无数种拍摄角度。 | 美食小K给出"巧合"辩护。 |
| W1, Day 5 | 周芳查看餐厅预约记录(restaurant-reservation-log.md)。 | 预约记录显示：周芳2月10日预约并就餐，美食小K 2月12日预约并就餐。日期不同，不存在同一天就餐的问题。这是C3——NON-CONFLICT。但预约日期不同反而增加了巧合的可疑性：如果不是同一天去的，为什么拍摄角度如此一致？ | 预约记录确认不同日期就餐。 |
| W2, Day 1 (Update 1 trigger) | 周芳向平台提交侵权投诉，平台回复"证据不足以支持下架"。 | 平台举报记录(platform-report-record.md)显示：平台的审核回复为"经审核，两条内容存在相似之处，但无法认定为直接抄袭。相似可能源于同一拍摄场所。建议双方协商解决。"平台的标准是"直接复制或明显抄袭"才会下架。 | 平台拒绝下架。周芳需要更强的证据。 |
| W2, Day 2 (Update 2 trigger) | 周芳检查原始素材元数据(original-footage-metadata.md)，发现关键证据。 | 元数据对比发现：两人的视频使用了**完全相同的相机设置**——Sony A7IV, 24-70mm f/2.8 GM, ISO 800, 1/60s, 24fps, S-Log3。不仅如此，连白平衡色温都一样（5200K）。这种参数完全一致的概率极低——说明美食小K极有可能是参考了周芳的视频设置后复制拍摄。 | 周芳有了元数据证据。 |
| W2, Day 3 (Update 3 trigger) | 摄影师老王提供进一步分析：美食小K的视频有2个镜头包含周芳视频中独有的构图元素（花瓶位置、餐巾折法）。 | 老王发现美食小K视频的第3镜头和第7镜头中，餐桌上的花瓶位置和餐巾折法与周芳视频完全一致。但餐厅服务员确认"每桌的花瓶和餐巾摆设每天不同"。这意味着美食小K要么是看了周芳的视频后重新摆设复原，要么是直接盗用了周芳的素材片段。 | 有了"场景复原"的证据。 |
| W2, Day 5 (Update 4 trigger) | 周芳的大学室友发现美食小K 3个月前也被另一位博主指控过类似行为。 | 大学室友截图了一个微博讨论帖，另一位美食博主"吃货阿明"3个月前发帖指控美食小K翻拍了他的一条日料店视频。帖子有角度对比截图但最终被删除（可能被美食小K公关处理）。这说明美食小K有"翻拍"的前科。 | 周芳有了对方的前科证据。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳 (Protagonist, Original Creator)

- **Objective position:** 周芳2月10日探店拍摄，2月15日10点发布。她是原创作者，有完整的素材元数据、拍摄日期和编辑时间线。
- **Public narrative:** "我的视频被抄袭了，请平台和公众关注。"
- **Private narrative:** 担心与粉丝量更大的博主对抗会被反噬（"小博主碰瓷大博主"的舆论风险）。
- **Why the gap exists:** 创作者生态中，粉丝量小的创作者维权成本高，容易被舆论翻转。

### 美食小K (Alleged Copier)

- **Objective position:** 美食小K在周芳视频发布5小时后发布了几乎相同的内容。相机参数完全一致，拍摄角度95%相似。
- **Narrative:** "同一家餐厅，巧合。我2月12日去的。"
- **Why the gap exists:** 美食小K利用"同一地点"的合理性来掩盖有意复制。粉丝量优势使她更容易获得舆论支持。

### 摄影师老王 (Professional Photographer)

- **Objective position:** 提供专业的相似度对比分析，是周芳这边最重要的技术证据来源。
- **Narrative:** 客观专业分析，支持周芳。

### 平台审核

- **Objective position:** 平台的审核标准侧重于"直接复制"，对"翻拍/模仿"的认定标准模糊。
- **Narrative:** "证据不足" — 但实际上是审核标准不适用于这种情况。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | 周芳2/15 10:00发布 vs 美食小K 2/15 15:00发布（同日，5h差） | video-publish-timeline.md (initial): 周芳发布时间 2026-02-15 10:00, 笔记ID XHS-20260215-ZF-FLR | video-publish-timeline.md (initial): 美食小K发布时间 2026-02-15 15:00, 笔记ID XHS-20260215-MK-FLR | 周芳先发布5小时。5小时足够观看视频、前往同一餐厅或参考拍摄方案。但美食小K声称2月12日已经拍好。时间线本身不能证明抄袭，但结合其他证据（角度、参数）形成证据链。 | R1 (initial) | **Yes: R1-->R5** |
| C2 | 美食小K"巧合" vs 拍摄角度95%相似 | 美食小K response (IM/公开): "同一家餐厅，同样的招牌菜，拍出来当然像。纯粹巧合。" | content-similarity-comparison.md (initial): 6道菜品角度完全一致(95%), 3个装潢角度一致, 运镜路线一致。专业摄影师分析。 | "同一餐厅"可以解释食物种类相同，但不能解释拍摄角度、构图、运镜路线95%一致。同一餐厅有无限种拍法。 | R2 (comparison initial) | **Yes: R2-->R6** |
| C3 | 餐厅预约记录 (NON-CONFLICT) | restaurant-reservation-log.md (initial): 周芳 2026-02-10 预约，19:00就餐，2人 | restaurant-reservation-log.md (initial): 美食小K 2026-02-12 预约，12:00就餐，1人 | 两人在不同日期就餐。C3为非矛盾数据。但不同日期反而削弱"巧合"说法——如果不是同一天同一桌，为什么场景元素（花瓶、餐巾）也一致？ | R1 onwards | **None** |
| C4 | 平台"证据不足" vs 元数据显示相同相机设置 | platform-report-record.md (Update 1): "无法认定为直接抄袭。相似可能源于同一拍摄场所。" | original-footage-metadata.md (Update 2): 完全相同的相机参数(Sony A7IV, 24-70mm f/2.8, ISO 800, 1/60s, 24fps, S-Log3, WB 5200K) | 平台的"同一场所"解释无法涵盖相机参数完全一致的事实。两个独立创作者使用完全相同的相机型号+镜头+ISO+快门+帧率+色彩模式+白平衡的概率极低。元数据是比视觉对比更强的证据。 | R8 (Update 1+2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 周芳-摄影师老王 IM -- Agent accepts "same restaurant" as partial explanation

- **Session and Loop:** 周芳-摄影师老王 IM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "The 95% angle similarity is notable but not conclusive on its own -- when two creators visit the same restaurant featuring the same signature dishes and architectural highlights, a high degree of visual similarity in their content is expected, and the 5-hour publication gap could reflect independent parallel creation rather than copying."
- **Why the agent is misled:** Restaurant review videos of the same venue do inherently share visual elements. Without metadata evidence, the agent may treat high similarity as environmentally driven.
- **Reversal trigger:** Metadata (Update 2) shows identical camera settings, and scene elements (Update 3) show props that change daily were identical.
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal)

### B2: 周芳-平台客服 邮件 -- Agent normalizes platform's "insufficient evidence" standard

- **Session and Loop:** 周芳-平台客服 邮件, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The platform's assessment that visual similarity alone is insufficient to establish copyright infringement has a reasonable basis -- content platforms must balance creator protection with the risk of false takedowns, and without clear evidence of direct copying (such as identical audio, watermarks, or frame-by-frame matches), similarity in restaurant review content may not meet the threshold for actionable infringement."
- **Why the agent is misled:** Platform copyright standards are generally cautious. The agent applies a reasonable legal framework but doesn't account for the strength of metadata evidence.
- **Reversal trigger:** Metadata (Update 2) provides the "clear evidence" the platform says it lacks. Prior complaints against 美食小K (Update 4) show a pattern.
- **Affected eval rounds:** R6 (bias visible), R11 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (timeline, partial) | B1 seed | R1, R2 | No | Timeline alone doesn't prove copying. Need combined evidence. |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After metadata, the timeline + angles + parameters = strong evidence chain. |
| T3 | C2 (angle similarity) | -- | R2 | No | 95% similarity is unusual but agents may accept "same restaurant." |
| T4 | C2 (full reversal) | -- | R2-->R6 | **Yes** | Metadata + scene elements make "coincidence" implausible. |
| T5 | C3 (reservation, non-conflict) | -- | R1 onwards | No | Different dates actually weakens "coincidence" defense. |
| T6 | C4 (platform vs metadata) | B2 | R8, R9 | No | Platform's standard doesn't account for metadata evidence. |
| T7 | C4 (full reversal) | B2 | R8-->R11 | **Yes** | Metadata + scene props + prior complaints = comprehensive case. |
| T8 | B2 ("insufficient evidence") | B2 | R6, R11 | **Yes** | Platform standard is outdated for this type of evidence. |
| T9 | Comprehensive | B1, B2 | R21-R30 | Comprehensive | Full: timeline + angles + metadata + scene props + prior history. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.** No additional copyright disputes.
2. **B1 and B2 exact phrases** must appear verbatim in specified session loops.
3. **Each contradiction traceable to at least two independent sources.**
4. **Camera parameters must be exact:** Sony A7IV, FE 24-70mm f/2.8 GM, ISO 800, 1/60s, 24fps, S-Log3, WB 5200K. Both creators use identical settings.
5. **Similarity metrics consistent:** 95% angle similarity, 6 dishes matched, 3 decor angles matched, 1 camera movement path matched.
6. **C3 (reservation) is NON-CONFLICT.** 周芳: Feb 10, 19:00. 美食小K: Feb 12, 12:00. Different dates.
7. **Publication timeline:** 周芳 2026-02-15 10:00, 美食小K 2026-02-15 15:00. 5-hour gap.
8. **Flower vase and napkin detail:** Restaurant confirms these change daily. Identical arrangement = staging or direct copying.
9. **周芳's personality:** Enthusiastic, creative, socially active. Concerned about reputation damage from public confrontation.
10. **All data text in Chinese (simplified).** Eval questions in English.
11. **Personalization (P1-P5):** 周芳 prefers (P1) visual descriptions and emoji-separated sections, (P2) topic-date naming (探店对比-0215.md), (P3) conclusion/recommendation first, (P4) data + story combined, (P5) lively and approachable tone.
12. **exec_check 20-40% of rounds.**
