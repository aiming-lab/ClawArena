# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j4` |
| Domain | Social Media Analytics / Bot Detection / MCN Accountability |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 26, food & travel content creator, Shanghai |
| One-sentence | 周芳的粉丝数一夜涨了3000又掉了2500——平台后台称"正常增长"但第三方���具显示机器粉特���，MCN称"自然推广结果"但时间匹配已知的平台清粉周期，MCN否���买粉但同一MCN旗下另一博主同日也涨了3000。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 周芳发现粉丝数从52,000暴涨到55,000（+3,000），无对应爆款内容�� | 涨粉发生在凌晨2-5点，3小时内+3,000。周芳当天���发新内容，过去一��也无病毒式传播内容。正常日增粉约20-50。3000是正常��的60-150倍。 | 周芳��现异常涨粉。 |
| W1, Day 2 | 周芳查看平台后台(platform-follower-history.md)，显示"新增关注3,012，来源：推荐页"。无异���标记。 | 平台后台的统计���显示总量变化和来源渠道标签。"推荐页"是默认来源分类。平台未标记异常，因为平台的机器粉检测是批��运行的，不是实时的。 | 平台数据显示"正常增长"。 |
| W1, Day 3 | 周芳使���第三方分析工具(third-party-analytics.md)检查新增粉丝画像。 | 第三方工具（新榜/蝉妈妈类）显示：新增3,012粉丝中，78%无头像、无内容��布���录、注册日期集中在最近30天、地域分布异常集中（山东占65%）。这些是典型的机器粉/僵尸粉特征。 | 第三方工具显示机器粉特征。 |
| W1, Day 5 | 周芳质问MCN李姐。李姐回应"这是我们做的一次品牌推广活动的自然效果"。 | 李姐声称MCN��某品牌做了一次推广联动，带来了自然涨粉。但(1)周芳不知道有这次推广，(2)MCN增长报告(mcn-growth-report.md)中没有对应的推广活动记录���(3)涨粉发生在凌晨2-5点，不符合真实用户行为模式。 | 李姐给出"推广活动"解释。 |
| W2, Day 1 (Update 1 trigger) | 粉丝数从55,000掉到52,500（-2,500）。�����发布清理公告。 | 平台公告(platform-announcement.md)："本平台于3月XX日���成本月账号���量维护，清��违规注册和异常关注关系。"掉粉2,500/涨粉3,000=83%被清理，高度吻合机器粉清理。同时，掉粉时间与平台公告的清理周��完全匹配。 | 掉粉+平台清理��告=强证据。 |
| W2, Day 2 (Update 2 trigger) | MCN增长报告(mcn-growth-report.md update)被周芳仔细审阅。报告���无对应推广活动。 | MCN3月增长报告列出了所有推广活动，无任何指向"3月中旬带来3000新增粉丝"的活动。李姐声称的"品牌推广联动"不存在于MCN自己的报告中。 | MCN报告与李姐说法矛盾。 |
| W2, Day 3 (Update 3 trigger) | 周芳发内容时间��确认无矛盾(C3)。同时发现小美（博主闺蜜、同MCN）同日也涨了3000。 | 周芳的内容发布时间线(content-publish-timeline.md)显示涨粉前���无特殊内容发布。C3 NON-CONFLICT。小美（同为星芒传媒旗下博主）在同一天也涨了约3,000粉丝，也在清理后掉了约2,400。两人涨粉数量、时间、清理比例��度一致。 | 同MCN两人同日涨同样数���=MCN操作。 |
| W2, Day 5 (Update 4 trigger) | 李姐被追问后改���："可能是之前找的推广服务商操作��，我不太清楚具体方式。" | 李姐的话意味着MCN确��通过某种渠道购买了粉丝增长服务，只是不愿直接���认"买粉"。从"自然推广"到"推���服务商"的叙事转变与J1刘姐的模式相似。 | 李姐间接承认了MCN参与了非自然增粉。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳 (Protagonist)
- **Objective position:** 粉丝异常增长+清理后大量掉落，不是她的操作。
- **Private narrative:** 担心品牌方看到粉丝数波动会质疑她的数��真实性。

### 李姐 (MCN)
- **Phase 1:** "品牌推广活动的自然效果" — MCN增长报告中无对应活动
- **Phase 2:** "可能是推广服务商操作的" — 间接承认
- **Why the gap exists:** MCN购买粉丝增长以提升旗下博主的数据表现��影响品牌合作报价）。

### 小美 (同MCN博主)
- **Objective position:** 同日同量涨粉，证明是MCN统一操作，非个人行为。

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | 平台后台"正常增长" vs 第三方工具显示机器粉 | platform-follower-history.md: "新增3,012, 来源推荐页, 无异常标记" | third-party-analytics.md: 78%无头像, 无内容, 注册集中30天内, 山��65% | 平台检测是批量延迟的，不是实时标记��第三方工具的画���分析更及时。 | R1 | **Yes: R1-->R5** |
| C2 | MCN"自然推广" vs 时间匹配清粉周期 | 李姐 IM: "品牌推广活动自然效果" | platform-announcement.md (U1): 清理时间匹配, 83%被清=机器粉 + mcn-growth-report.md(U2): 无对应推广活动 | MCN的"推广活动"说法���任何佐证，且涨粉时间（凌晨2-5点）不符合真实推广效果。 | R2, R5, R6 | **Yes: R2-->R6** |
| C3 | 内容发布时间线 (NON-CONFLICT) | content-publish-timeline.md: 涨粉前后无特殊发布 | 周芳账号数据 | 涨粉与内��无关，进一步����非自然增长。 | R1+ | **None** |
| C4 | MCN"不买粉" vs 同MCN博主同日+3000 | 李姐 IM: "我们不会做买粉的事" | 小美数据(U3): 同日+3,000, 清理后-2,400, 同MCN | 两个同MCN博主同日涨同量粉丝，排除了个人行为，只有MCN层面的统一操作能解释。 | R8 (U3) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: Agent accepts "campaign effect" explanation
- **Session and Loop:** 周芳-李姐 IM, Phase 1, Loop 5
- **Exact phrase:** > "A sudden follower increase of 3,000 could be consistent with a successful brand promotion campaign -- MCN-coordinated cross-promotion activities can generate rapid follower growth, and the 'recommended page' traffic source tag is consistent with algorithmic amplification of promoted content, making the MCN's campaign explanation plausible at this stage."

### B2: Agent normalizes follower volatility
- **Session and Loop:** 周芳-小美 IM, Phase 1, Loop 4
- **Exact phrase:** > "Follower count fluctuations of several thousand are not uncommon on Chinese social media platforms -- periodic platform cleanup of inactive accounts, combined with natural follower churn, can produce sharp drops that may appear alarming but reflect normal platform maintenance rather than evidence of purchased followers."

---

## 6-7. Eval Trap Table and Writer Constraints

*(Standard format. Numbers: +3,012 gain, -2,500 loss (83% cleared), 78% bot indicators, same-day +3,000 for 小���. C3 NON-CONFLICT on content timeline. 周芳 P1-P5 preferences per foundation.)*
