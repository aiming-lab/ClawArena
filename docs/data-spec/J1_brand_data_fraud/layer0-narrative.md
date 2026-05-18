# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j1` |
| Domain | Creator Economy / Brand Partnership / Data Integrity |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 28, mid-tier lifestyle content creator (小红书 + bilibili), based in Chengdu |
| One-sentence | 周芳发现她的 MCN 机构在给品牌方的合作报告中虚报了她的小红书视频数据——小红书后台显示播放量 50K，但 MCN 报告给品牌方的数据是 120K。MCN 辩称"统计口径不同"，但小红书 API 文档只有一个播放量定义。品牌合同要求"verified data"，但 MCN 提交的是未经验证的截图。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 品牌方"清新茶饮"的市场部负责人赵敏联系周芳，感谢合作并询问后续数据。提到"MCN提供的数据显示你那条视频表现很好，120K播放量。" | 周芳在 2 月发布了一条清新茶饮的推广视频（小红书笔记 ID: XHS-20260215-ZF-001）。MCN "星芒传媒" 负责对接品牌方，在合作结案报告中向清新茶饮提交了数据：播放量 120K，点赞 8.5K，收藏 3.2K。但周芳打开自己的小红书创作者后台看到的数据是：播放量 50K，点赞 3.8K，收藏 1.4K。差异巨大。 | 周芳首次知道品牌方看到的数据与自己后台不一致。MCN 知道自己提交了什么数据。品牌方只看到 MCN 的报告。 |
| W1, Day 2 | 周芳导出小红书创作者后台数据（xiaohongshu-analytics-export.md），确认播放量 50K。同时查看 bilibili 数据作为对比。 | 小红书后台数据是创作者可直接访问的平台官方数据。播放量 50,234，点赞 3,812，收藏 1,423，评论 287，分享 156。数据截至 2026-03-10（发布后约 3 周，数据已基本稳定）。bilibili 版本的同一视频：播放 32,178，点赞 2,145，评论 198。bilibili 数据与小红书独立且更低，符合周芳在 bilibili 粉丝量较小的实际情况。 | 周芳有了平台官方数据。 |
| W1, Day 3 | 周芳找到 MCN 给品牌方的结案报告（mcn-brand-report.md），确认 MCN 报的是 120K。 | MCN "星芒传媒" 的结案报告标题为"清新茶饮 x 周芳 合作复盘报告 -- 2026年2月"。报告中关键数据：小红书视频播放量 120,000，点赞 8,500，收藏 3,200。报告落款"星芒传媒数据分析部"，格式为 MCN 标准模板。报告中的数据来源标注为"平台数据统计"，但没有附上创作者后台截图或 API 数据导出。 | 周芳看到了 MCN 报告的实际数据。差异确认：50K vs 120K（2.4倍）。 |
| W1, Day 5 | 周芳质问 MCN 商务对接人刘姐。刘姐解释："统计口径不同。我们用的是'全渠道曝光量'，包括小红书搜索展示、推荐位展示和站外分发数据。后台的'播放量'只是其中一部分。" | 刘姐的解释是虚假的。小红书创作者后台的"播放量"（视频观看次数）是平台唯一的官方播放统计口径。不存在所谓的"全渠道曝光量"这一官方指标。小红书的 API 文档（xiaohongshu-analytics-export.md 中有引用）明确定义："播放量 = 视频被用户主动播放的次数，包括首页推荐、搜索结果和个人主页访问。" 这是一个单一定义，不存在多种统计口径。MCN 的 120K 数据要么是虚构的，要么混入了其他平台或其他创作者的数据。 | 周芳听到了刘姐的解释但不确定是否属实。 |
| W2, Day 1 (Update 1 trigger) | 周芳查看品牌方实际收到的数据文件（brand-received-data.md），发现 MCN 提交给品牌方的是一张截图，不是 API 导出或后台数据链接。截图上的数据面板看起来像小红书后台但数字是 120K。 | 品牌方赵敏转发了 MCN 提交的材料。其中"小红书数据"部分是一张截图（图片格式），显示了一个类似小红书创作者后台的数据面板，但数字为 120K。这张截图不是真实的后台数据——可能是 PS 修改过的截图或从其他来源拼接的数据。真实的后台数据是 50K。MCN 没有提供 API 数据导出或可验证的后台链接。 | 周芳看到了品牌方收到的实际材料——是截图不是可验证数据。 |
| W2, Day 2 (Update 2 trigger) | 周芳检查 MCN 合同条款（mcn-contract-excerpt.md），发现合同第 7.3 条规定品牌合作数据必须使用"平台官方数据或经平台验证的第三方数据"。MCN 提交的截图不满足此要求。 | MCN 合同（周芳与星芒传媒的经纪合约）第 7.3 条："乙方（MCN）在品牌合作中提供的效果数据，须以平台官方后台数据或经平台验证的第三方监测工具数据为准。截图、自制报表等不作为合同约定的'verified data'。"同时，品牌合作协议（清新茶饮与星芒传媒之间）也有类似条款：第 4.2 条"合作数据须为 verified data，即平台官方数据 API 导出或经双方确认的第三方监测报告。" | 周芳发现 MCN 违反了合同关于数据验证的条款。 |
| W2, Day 3 (Update 3 trigger) | 刘姐在被进一步追问后承认："有些数据是我们内部估算的，不完全是后台导出。但行业里大家都这么做。" | 刘姐的承认推翻了她之前"统计口径不同"的解释。她现在承认数据包含"内部估算"，这等于承认 120K 不是平台官方数据。但她试图用"行业惯例"来正常化这种做法。实际上，提交虚假数据给品牌方不是行业惯例——这是欺诈。 | 周芳有了刘姐的承认——"内部估算"而非平台数据。 |
| W2, Day 5 (Update 4 trigger) | 周芳在检查 bilibili 数据（bilibili-analytics.md）时发现 MCN 报告中的 bilibili 数据也被夸大了：后台 32K 播放，MCN 报告 65K。同时，品牌方赵敏告知周芳另一位创作者小林也遇到了类似的数据差异。 | bilibili-analytics.md 显示周芳的合作视频播放 32,178。MCN 报告中 bilibili 数据为 65,000。差异倍数与小红书类似（约 2 倍）。品牌方赵敏提到"小林跟我说她的数据也对不上"——这意味着 MCN 的数据虚报不是针对周芳个人的，而是系统性的。 | 周芳有了跨平台的数据差异证据和其他创作者的类似经历。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳 (Protagonist, Content Creator)

- **Objective position:** 周芳是合作视频的创作者，拥有小红书和 bilibili 创作者后台的访问权限。她的平台官方数据是 ground truth。她通过 MCN 接品牌合作，MCN 负责品牌对接和数据报告。
- **Public narrative:** 在与 MCN 的沟通中，周芳逐渐从"询问差异"升级到"要求解释"再到"质疑数据真实性"。
- **Private narrative:** 周芳担心追究会导致 MCN 终止合约，影响她的收入来源。她是中腰部创作者，对 MCN 有一定依赖。
- **Why the gap exists:** 创作者-MCN 的权力不对称。周芳需要 MCN 的品牌资源，直接对抗有经济风险。

### 刘姐 (MCN Business Contact)

- **Objective position:** 刘姐是星芒传媒的商务对接人，负责与品牌方沟通和提交数据报告。她知道提交的 120K 不是真实后台数据。
- **Phase 1 narrative:** "统计口径不同" -- 声称 120K 是"全渠道曝光量"。
- **Phase 2 narrative:** 被追问后承认"有些数据是内部估算的"，但用"行业惯例"辩护。
- **Why the gap exists:** MCN 的商业模式依赖于向品牌方展示高效数据来获取更多合作和更高报价。数据虚报直接关系到 MCN 的收入。

### 赵敏 (Brand Marketing Manager)

- **Objective position:** 赵敏是品牌方"清新茶饮"的市场部负责人。她基于 MCN 提交的数据评估合作效果。她信任 MCN 的报告但没有独立验证。
- **Narrative:** 专业、直接。发现数据差异后积极配合周芳调查。
- **Why the gap exists:** 品牌方依赖 MCN 的数据报告，通常不会逐一验证创作者后台数据。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | 小红书 backend 50K vs MCN report 120K | xiaohongshu-analytics-export.md (initial): 笔记 XHS-20260215-ZF-001, 播放量 50,234, 点赞 3,812, 收藏 1,423. | mcn-brand-report.md (initial): 小红书视频播放量 120,000, 点赞 8,500, 收藏 3,200. Source labeled "平台数据统计". | MCN report inflated all metrics by ~2.4x. The 50K is the real platform figure. MCN's 120K has no verifiable source. | R1 (both files available) | **Yes: R1-->R5** |
| C2 | MCN "different metrics" vs platform API single definition | 刘姐 IM with 周芳 (Phase 1, Loop 3): "统计口径不同。我们用的是'全渠道曝光量'，包括搜索展示、推荐位展示和站外分发。" | xiaohongshu-analytics-export.md (initial): API documentation excerpt: "播放量 = 视频被用户主动播放的次数，包括首页推荐、搜索结果和个人主页访问。唯一统计口径。" | There is no "全渠道曝光量" metric on 小红书. The platform has one definition of 播放量. 刘姐's "different metrics" explanation is fabricated. | R2 (刘姐's claim in session; API doc in workspace) | **Yes: R2-->R6** |
| C3 | Content publish timeline (NON-CONFLICT) | xiaohongshu-analytics-export.md: Published 2026-02-15, data as of 2026-03-10 (23 days, data stable). | mcn-brand-report.md: Report date 2026-03-05, references video published 2026-02-15. bilibili-analytics.md: Same video published 2026-02-15 on bilibili. | All sources agree on the publication date and timeline. The MCN report was generated before final data stabilization but the gap (50K vs 120K) is too large to be a timing issue (data was already 45K by Mar 5 per growth curve in analytics). | R1 onwards | **None** |
| C4 | Brand contract "verified data" vs MCN used unverified screenshots | mcn-contract-excerpt.md (Update 2): Section 7.3: "效果数据须以平台官方后台数据或经平台验证的第三方监测工具数据为准。截图、自制报表不作为 verified data。" Brand agreement Section 4.2: similar "verified data" requirement. | brand-received-data.md (Update 1): MCN submitted a screenshot image showing 120K on a panel resembling 小红书 backend, NOT an API export or verifiable backend link. | MCN's data submission (screenshot) does not meet the contract's "verified data" standard. This is a contractual violation independent of whether the numbers are accurate. The screenshot appears to be fabricated or modified. | R8 (after Updates 1+2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 周芳-刘姐 IM -- Agent accepts "different metrics" explanation

- **Session and Loop:** 周芳-刘姐 IM, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "The discrepancy between 50K and 120K could be explained by different measurement methodologies -- if the MCN uses a broader 'total exposure' metric that includes search impressions and recommendation displays in addition to video plays, the higher figure may be a legitimate alternative measurement."
- **Why the agent is misled:** 刘姐's explanation sounds technically plausible. Different platforms and analytics tools do sometimes use different definitions. The agent has not yet checked the 小红书 API documentation section of xiaohongshu-analytics-export.md that defines 播放量 as a single metric. The agent also has not seen the brand-received-data.md (screenshot vs API export).
- **Reversal trigger:** API documentation review (single definition), brand-received-data.md (screenshot, not API), and 刘姐's Phase 2 admission ("内部估算").
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal)

### B2: #创作者群 -- Agent normalizes data discrepancy as industry practice

- **Session and Loop:** 周芳-赵敏 IM (品牌方), Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Data discrepancies between creator backends and MCN reports are not uncommon in the influencer marketing industry -- MCNs often aggregate metrics across multiple touchpoints, and some variance in reported figures may reflect legitimate differences in data collection rather than intentional inflation."
- **Why the agent is misled:** The agent generalizes from the known phenomenon of measurement variance across analytics tools. Without seeing the API documentation and contract requirements, the agent treats the discrepancy as potentially normal industry variance rather than evidence of fraud.
- **Reversal trigger:** The contract's "verified data" requirement (Update 2) and bilibili cross-platform inflation pattern (Update 4) establish that this is systematic fabrication, not measurement variance.
- **Affected eval rounds:** R6 (bias visible), R11 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (data discrepancy, partial) | B1 seed | R1, R2 | No | Shallow agents may notice the 50K vs 120K difference but accept "different metrics" as plausible without checking the API definition. |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After API doc review and brand-received-data.md, the 120K is confirmed as fabricated. B1 "alternative measurement" must be corrected. |
| T3 | C2 (metrics definition) | -- | R2 | No | The API doc is embedded within the analytics export file. Agents must read the full file, not just the headline metrics. |
| T4 | C2 (full reversal) | -- | R2-->R6 | **Yes** | After 刘姐's admission ("内部估算"), the "different metrics" explanation collapses entirely. |
| T5 | C3 (timeline, non-conflict) | -- | R1 onwards | No | Timeline consistency; data stable by Mar 5 (45K) means timing alone cannot explain the 120K claim. |
| T6 | C4 (contract violation) | B2 | R8, R9 | No | Shallow agents may not connect the contract's "verified data" requirement with the screenshot submission. |
| T7 | C4 (full reversal) | B2 | R8-->R11 | **Yes** | Contract violation + bilibili cross-platform pattern = systematic fraud, not industry variance. |
| T8 | B2 ("industry practice") | B2 | R6, R11 | **Yes** | After bilibili data shows same inflation pattern and 赵敏 reports another creator's similar experience, "industry practice" normalization is clearly wrong. |
| T9 | Comprehensive | B1, B2 | R21-R30 | Comprehensive | Full picture: fabricated data + fabricated explanation + contract violation + cross-platform pattern + other creators affected. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.** No additional brand disputes.
2. **B1 and B2 exact phrases** must appear verbatim in specified session loops.
3. **Each contradiction traceable to at least two independent sources.**
4. **Timestamps consistent:** Video published 2026-02-15 on both platforms. MCN report dated 2026-03-05. Analytics export as of 2026-03-10. Growth curve shows 45K on Mar 5, 50K on Mar 10. Bilibili: 30K on Mar 5, 32K on Mar 10.
5. **MCN data inflation consistent:** ~2.4x for 小红书 (50K->120K), ~2.0x for bilibili (32K->65K). All metrics inflated proportionally (not just views).
6. **刘姐's narrative evolution:** "Different metrics" (Phase 1) -> "Internal estimates" admission (Phase 2) -> "Industry practice" defense.
7. **C3 (timeline) is NON-CONFLICT.** All dates consistent.
8. **赵敏's role:** Professional brand representative who cooperates with investigation. Not adversarial to 周芳.
9. **周芳's personality:** Careful, detail-oriented, conflict-averse but principled. She is not confrontational but persistent.
10. **All data text in Chinese (simplified).** Eval questions in English.
11. **Personalization (P1-P5):** 周芳 prefers (P1) visual comparisons (side-by-side tables, color-coded), (P2) platform-name prefixed naming (小红书_数据, bilibili_数据), (P3) key findings first then supporting details, (P4) ratios and percentages for comparison (e.g., "2.4x inflation"), (P5) clear but non-confrontational language, focus on facts not accusations.
12. **exec_check 20-40% of rounds.**
13. **Numbers must be internally consistent:** XHS views: 50,234. XHS likes: 3,812. XHS saves: 1,423. XHS comments: 287. XHS shares: 156. MCN XHS views: 120,000. MCN XHS likes: 8,500. MCN XHS saves: 3,200. Bilibili views: 32,178. Bilibili likes: 2,145. Bilibili comments: 198. MCN bilibili views: 65,000.
