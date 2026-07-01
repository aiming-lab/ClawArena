# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j5` |
| Domain | Public Relations / Food Safety / Creator Liability |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 26, food & travel content creator, Shanghai |
| One-sentence | 周芳推广的一款食品被曝食品安全问题——品牌说"个别批次"但监管说"系统性污染"，品牌说"检测安全"但消费者检测出大肠杆菌，产品批次时间线无矛盾，MCN说"删帖就行"但周芳合同约定"30天删帖通知期"。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 社交媒体爆出"鲜味坊"即食鸡胸肉食品安全问题。周芳3周前发布了该品牌推广视频。 | "鲜味坊"是周芳合作的一个健康食品品牌。周芳的推广视频(original-promotion-content.md)发布于3周前，内容为产品测评和推荐。视频仍在线。粉丝开始在评论区@周芳要求回应。 | 食品安全问题曝光。周芳的推广内容成为焦点。 |
| W1, Day 2 | 品牌方发布澄清声明(brand-clarification-statement.md)："个别批次存在质量波动，已召回。产品整体安全。" | 品牌声明的核心主张：(1)问题仅限"个别批次"，(2)已主动召回，(3)其他批次经第三方检测"全部合格"。声明附上了品牌委托的检测报告摘要。 | 品牌给出"个别批次"定性。 |
| W1, Day 3 | 国家市场监管总局发布公告(food-safety-authority-notice.md)。 | 监管公告内容："经抽检，鲜味坊即食鸡胸肉产品存在**系统性微生物超标问题**，涉及多个生产批次和多个生产线。已责令全面停产整改。"这与品牌的"个别批次"说法直接矛盾。监管定性为"系统性"而非"个别"。 | 监管说"系统性"，品牌说"个别"。 |
| W1, Day 5 | 周芳查看消费者实测报告(consumer-test-report.md)。 | 多名消费者在社交媒体上发布了送检结果。其中3份独立检测报告显示大肠杆菌群超标2-5倍。而品牌的自检报告声称"大肠杆菌<10 CFU/g，符合国标"。消费者检测使用的是国家认可的第三方实验室。 | 消费者检测与品牌检测矛盾。 |
| W2, Day 1 (Update 1 trigger) | 周芳核查产品批次时间线。 | 周芳推广的产品批次号为BN-20260201。她收到的样品批次(original-promotion-content.md中有记录)与被召回的批次范围(BN-20260115~BN-20260228)重叠。品牌未主动告知周芳她推广的批次在召回范围内。**产品批次时间线本身无矛盾(C3)**——生产日期、批次号、召回范围在各来源中一致。 | 周芳推广的批次在召回范围内。 |
| W2, Day 2 (Update 2 trigger) | MCN李姐建议"删帖"，但周芳合同有30天删帖通知条款。 | 李姐说："赶紧把推广视频删了，减少风险。"但周芳的推广合同(mcn-legal-response.md中引用)第8.3条规定："品牌推广内容的修改或删除，需提前30个自然日书面通知MCN和品牌方。未经通知擅自删除构成违约。"李姐的建议与合同条款矛盾。 | 删帖建议与合同条款冲突。 |
| W2, Day 3 (Update 3 trigger) | 品牌方私下联系周芳，提出"和解方案"：品牌不追究周芳推广内容的责任，但要求周芳不公开讨论此事。 | 品牌方的和解方案实质上是"封口协议"——用不追责换取周芳沉默。但(1)周芳本来就没有法律责任（她推广时不知道安全问题），(2)品牌的问题已被监管确认为系统性的。 | 品牌提出封口式和解。 |
| W2, Day 5 (Update 4 trigger) | 周芳的粉丝评论汇编(fan-comment-compilation.md)显示粉丝分裂：部分支持周芳"也是受害者"，部分指责"恰烂饭"。 | 粉丝评论反映了两种立场：(1)"周芳也不知道有问题，她也是受害者"(40%)，(2)"博主推荐就要负责，恰饭不负责任"(35%)，(3)中立/等待更多信息(25%)。舆论走向取决于周芳如何回应。 | 粉丝舆论压力。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳
- **Objective position:** 在不知情的情况下推广了有安全问题的产品。她不是直接责任方但面临声誉风险。
- **Private narrative:** 担心声誉受损，想快速处理但不想违约或做出错误决定。

### 品牌方（鲜味坊）
- **Phase 1:** "个别批次" — 被监管否定为"系统性"
- **Phase 2:** "和解方案" — 实质封口
- **Why:** 品牌试图控制叙事和限制损失。

### MCN李姐
- **Narrative:** "删帖减少风险" — 忽略合同30天通知条款
- **Why:** MCN优先考虑快速止损，不顾合同义务。

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Reversal |
|---|---|---|---|---|---|---|
| C1 | 品牌"个别批次" vs 监管"系统性污染" | brand-clarification-statement.md: "个别批次质量波动" | food-safety-authority-notice.md: "系统性微生物超标，涉及多批次多生产线" | 监管有执法权力和独立抽检能力，其"系统性"定性比品牌自述更权威。 | R1 | **Yes: R1-->R5** |
| C2 | 品牌"检测安全" vs 消费者检测出大肠杆菌 | brand-clarification-statement.md: "第三方检测全部合格，大肠杆菌<10 CFU/g" | consumer-test-report.md: 3份独立报告大肠杆菌超标2-5倍 | 品牌的检测可能选择性送检合格批次。消费者使用国家认可实验室，结果可信。 | R2 | **Yes: R2-->R6** |
| C3 | 产品批次时间线 (NON-CONFLICT) | original-promotion-content.md: 推广批次BN-20260201 | 品牌召回范围BN-20260115~BN-20260228 | 批次号、日期在各来源一致。推广批次确在召回范围内。 | R1+ | **None** |
| C4 | MCN"删帖" vs 合同"30天通知期" | 李姐 IM: "赶紧删帖减少风险" | 推广合同第8.3条: "修改或删除需提前30天书面通知" | MCN的删帖建议构成教唆违约。正确做法是走合同通知流程。 | R8 (U2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design

### B1: Agent accepts "isolated batch" framing
- **Exact phrase:** > "The brand's characterization of the issue as an 'isolated batch quality fluctuation' is not uncommon in food safety incidents -- initial reports often exaggerate the scope before full investigation, and the brand's proactive recall and third-party testing demonstrate a responsible response, suggesting the issue may indeed be limited in scope."
- **Reversal:** Regulator confirms systemic contamination.

### B2: Agent supports immediate deletion
- **Exact phrase:** > "From a crisis management perspective, removing the promotional content immediately is a reasonable precautionary measure -- continued association with a product under food safety investigation could compound reputational damage, and swift action to distance from the brand typically reduces long-term creator liability exposure."
- **Reversal:** Contract 30-day clause makes immediate deletion a breach.

---

## 7. Writer Constraints

1. Numbers: 大肠杆菌 brand claims <10 CFU/g vs consumer tests 2-5x standard (standard=100 CFU/g, so consumer finds 200-500 CFU/g). Batch BN-20260201. Recall range BN-20260115~BN-20260228. Contract clause 8.3: 30-day notice.
2. C3 NON-CONFLICT on batch timeline.
3. 周芳 P1-P5 preferences per foundation.
