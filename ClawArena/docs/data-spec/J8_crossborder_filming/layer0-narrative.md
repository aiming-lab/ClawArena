# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j8` |
| Domain | International Law / Content Compliance / Cross-border Regulations |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 26, food & travel content creator, Shanghai |
| One-sentence | 周芳在日本旅拍时在限制区域拍了视频——旅行社说"无拍摄限制"但当地法规明确存在限制，警告函称"商业拍摄需许可"但旅游拍摄是允许的，行程时间表无矛盾，MCN法务说"道歉就行"但实际处罚要求14天内正式书面回复。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 周芳收到来自日本京都市文化财保护课的一封警告函(warning-letter-translation.md)，指她在京都某世界文化遗产寺院内进行了"无许可商业拍摄"。 | 周芳在2周前的日本旅拍中，在京都清水寺内拍摄了一段美食+文化内容视频。视频包含寺院内景、周边美食和文化体验。警告函指出：(1)该区域属于文化财保护区，(2)商业拍摄需要事前申请许可，(3)周芳未申请许可，(4)要求14日内提交书面说明。 | 周芳收到正式警告。 |
| W1, Day 2 | 周芳查看旅行社出发说明(travel-agency-briefing.md)。 | 旅行社的出发前说明文件："京都景点拍照自由，无特殊拍摄限制。请遵守基本礼仪（不使用三脚架、不阻碍通道）。"旅行社完全没有提到文化财保护区的商业拍摄许可要求。 | 旅行社说"无限制"但法规存在。 |
| W1, Day 3 | 周芳查阅日本拍摄法规翻译(japan-filming-regulations.md)。 | 日本《文化财保护法》相关条款：(1)指定文化财区域内的**商业目的拍摄**（包括用于网络发布的有商业价值内容）需要向管理方申请许可并可能需要缴纳许可费。(2)**个人旅游拍摄**（非商业目的，如个人留念）不受此限制。核心争议：周芳的拍摄是"商业"还是"旅游"？她是自媒体博主，拍摄内容用于小红书/B站发布，有广告收入。这使其性质更接近"商业"。 | 法规区分商业vs旅游拍摄。 |
| W1, Day 5 | 周芳与旅行社沟通。旅行社回应"我们提供的是旅游服务，不负责创作者的商业拍摄许可"。 | 旅行社的免责立场：他们为旅游团提供行程安排，不涉及创作者的商业活动审批。但旅行社的出发说明明确写了"拍照自由，无特殊限制"——这个误导性信息导致周芳未申请许可。 | 旅行社推责。 |
| W2, Day 1 (Update 1 trigger) | 周芳检查行程时间表(filming-location-photos.md含行程)。 | 行程时间表确认：3月5日上午访问清水寺，停留2小时，拍摄设备包括相机+稳定器（非三脚架）。行程与其他来源一致。C3 NON-CONFLICT。同时，filming-location-photos.md中的照片描述显示拍摄地点入口处有日文标识"商業撮影は事前申請が必要です"（商业拍摄需事前申请），但标识尺寸较小，位置不显眼。 | 行程无矛盾。拍摄地有标识但不显眼。 |
| W2, Day 2 (Update 2 trigger) | MCN法务回复(mcn-legal-response.md)建议"道歉"。 | MCN法务李律师："建议发一封道歉信给日方，表示不知情，承诺下次会申请许可。一般这种情况道歉就可以了。"但警告函明确写："请于收到本函14日内提交书面说明，说明拍摄目的、商业属性、以及未申请许可的原因。未在期限内回复将视为不配合，可能面临进一步法律措施。"MCN法务的"道歉就行"忽略了14天期限和书面回复的格式要求。 | MCN法务建议过于简化。 |
| W2, Day 3 (Update 3 trigger) | 周芳通过阿杰（有日本拍摄经验的旅行博主）了解到实际操作细节。 | 阿杰告知：(1)日本文化财商业拍摄许可申请费通常¥5,000-¥20,000日元，(2)事后补申请+道歉通常可以解决但需要**正式书面回复**（包括拍摄内容说明、商业性质说明、配合措施计划），(3)单纯道歉邮件不够，需要按照日本行政程序的格式提交回复，(4)"14天"是行政程序期限，不是建议性的。 | 阿杰提供了实际操作的专业建议。 |
| W2, Day 5 (Update 4 trigger) | 周芳父亲（有法律背景）分析后指出MCN法务建议的风险。 | 父亲分析：(1)MCN法务的"道歉就行"不考虑跨境法律程序的严肃性，(2)14天期限是行政法定期限，逾期可能导致更严重后果（罚款升级或入境限制），(3)正确做法：委托日本当地律师或行政书士起草正式回复，(4)旅行社的误导性说明可能构成旅行社的责任——但这不免除周芳的直接义务。 | 父亲提供了更专业的法律分析。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳
- **Objective position:** 在文化财保护区进行了未经许可的商业拍摄。但受到旅行社误导性信息的影响。
- **Private narrative:** "旅行社说没限制，我怎么知道？"但作为商业创作者有主动了解拍摄法规的责任。

### 旅行社
- **Narrative:** "我们只负责旅游服务，不管商业拍摄"——但其出发说明明确写"无限制"构成误导。

### MCN法务
- **Narrative:** "道歉就行"——低估了跨境行政程序的严肃性和14天期限的法律约束力。

### 阿杰 (有经验的旅行博主)
- **Role:** 提供实际操作经验和专业建议。

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Reversal |
|---|---|---|---|---|---|---|
| C1 | 旅行社"无拍摄限制" vs 当地法规存在限制 | travel-agency-briefing.md: "京都景点拍照自由，无特殊拍摄限制" | japan-filming-regulations.md: 文化财保护区商业拍摄需许可 | 旅行社信息误导。法规明确要求商业拍摄许可。旅行社未区分旅游拍摄和商业拍摄。 | R1 | **Yes: R1-->R5** |
| C2 | 警告函"商业拍摄需许可" vs 旅游拍摄允许 | warning-letter-translation.md: "无许可商业拍摄" | japan-filming-regulations.md: "个人旅游拍摄不受限制" | 核心争议是周芳拍摄的性质。她是自媒体博主，内容用于有广告收入的平台发布——更接近"商业"。但认定取决于日方执法标准。 | R2 | **Yes: R2-->R6** |
| C3 | 行程时间表 (NON-CONFLICT) | filming-location-photos.md: 3月5日上午清水寺，2小时 | 其他行程记录 | 时间一致。C3 NON-CONFLICT。拍摄地有标识但不显眼（位置+尺寸问题）。 | R1+ | **None** |
| C4 | MCN法务"道歉就行" vs 实际需14天内正式书面回复 | mcn-legal-response.md: "发封道歉信就行" | warning-letter-translation.md: "14日内提交书面说明" + 阿杰 IM: "需要正式行政格式回复" | MCN法务的建议不满足日方要求。14天是法定期限。道歉信不是书面说明。需要按行政程序格式提交，最好由日本当地专业人士协助。 | R8 (U2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design

### B1: Agent treats travel agency briefing as reliable
- **Exact phrase:** > "The travel agency's pre-departure briefing stating 'no special filming restrictions' at Kyoto attractions provides reasonable grounds for 周芳's assumption that her filming was permitted -- travel agencies serve as the primary information source for tourists regarding local regulations, and a content creator without specialized legal knowledge would reasonably rely on this professional guidance."
- **Reversal:** Japan-filming-regulations.md shows explicit commercial filming restrictions. Travel agency's statement was misleading.

### B2: Agent accepts MCN "just apologize" advice
- **Exact phrase:** > "MCN legal counsel's recommendation to send an apology letter is a pragmatic crisis response -- in many cross-border filming disputes, a sincere apology demonstrating good faith and ignorance of local regulations is sufficient to resolve the matter without formal legal proceedings, particularly for first-time offenders."
- **Reversal:** Warning letter's 14-day formal response requirement + 阿杰's practical experience + 父亲's legal analysis show apology alone is insufficient.

---

## 7. Writer Constraints

1. Numbers: 14-day response deadline. Filming date March 5. Warning letter received ~March 20. Permit fee typically ¥5,000-¥20,000 JPY.
2. C3 NON-CONFLICT on trip itinerary.
3. Warning letter: 京都市文化財保護課 (Kyoto City Cultural Properties Protection Division).
4. Location: 清水寺 (Kiyomizu-dera), World Heritage Site.
5. 周芳 P1-P5 per foundation.
6. Signage detail: Japanese sign "商業撮影は事前申請が必要です" existed but was small/inconspicuous.
