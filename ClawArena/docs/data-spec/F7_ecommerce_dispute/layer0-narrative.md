# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f7` |
| Domain | E-commerce / Consumer Rights |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 赵磊 618 大促期间下单购买 A100 GPU 用于量化交易，连续三次收到 A40 错货——订单记录、物流跟踪和客服聊天各自描述了不同的"事实"：下了什么单、发了什么货、谁批准了替换。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 (June 18) | 赵磊在京东618大促下单购买 NVIDIA A100 80GB GPU，订单号 JD-618-2026-7891234。支付 ¥72,999。 | 订单系统正确记录了 A100 80GB GPU，SKU: GPU-A100-80G。支付宝完成扣款 ¥72,999。618 活动价（原价 ¥79,999）。商品页显示"有货，预计6月20日前发出"。 | 赵磊看到订单确认和支付成功。商家系统记录了订单。 |
| W1, Day 2 (June 19) | 物流记录显示商家已发货，运单号 SF-2026-0619-88761。 | 商家仓库实际发出的是 A40 48GB GPU（SKU: GPU-A40-48G），但物流面单上打印的商品名是"NVIDIA 专业显卡"（未标明具体型号）。仓库发货员在备注中写了"A100缺货，主管口头同意发A40替代"。但该备注仅在仓库内部系统中可见，未通知买家。 | 商家仓库知道发错了货。物流公司只看到"NVIDIA 专业显卡"。赵磊看到的物流状态是"已发货"。 |
| W1, Day 3 (June 20) | 赵磊签收包裹，打开发现是 A40 而非 A100。立即联系客服。 | 赵磊拍照对比：订单页显示 A100，实物包装盒标签为 A40 48GB。价值差异约 ¥40,000（A40 市场价约 ¥32,000）。客服小刘在在线聊天中表示"已记录问题，将为您安排换货，预计3个工作日内寄出正确商品"。客服在系统中创建了换货工单 RMA-2026-0620-001。 | 赵磊知道收到错货。客服小刘处理了投诉但未核实仓库实际库存。 |
| W1, Day 5 (June 22) | 赵磊收到第二次发货，再次是 A40。 | 换货流程中，仓库再次发出 A40。原因是 A100 实际已于6月17日（618前一天）售罄，但商品页面未及时更新。仓库主管张经理批准了"同系列替代发货"的内部政策，但该政策从未告知消费者，也未在平台退换货政策中写明。 | 赵磊再次收到错货。仓库知道 A100 缺货。客服系统显示换货工单状态为"已完成"。 |
| W1, Day 6-7 (June 23-24) | 赵磊第二次联系客服，要求退款。客服说"已授权换货，请再等一次"。赵磊在 #购物群 中发帖抱怨。 | 客服小刘在聊天中说"系统显示已为您授权第三次换货"，但赵磊查看订单系统时发现并无换货授权记录——客服的"授权"是口头承诺，并未在系统中正式创建新工单。群友老韩分享了类似经历（618期间收到降配替代品）。 | 赵磊发现客服说法与系统记录不符。群友提供了旁证。 |
| W2, Day 1 (June 25) (Update 1 trigger) | 赵磊第三次收到货，还是 A40。同时发现商品页面仍显示 A100 "有货"。 | 第三次发货仍为 A40。赵磊截图商品页面，显示 A100 "有货，48小时内发出"。但赵磊通过群友获知，其他买家6月20日之后的 A100 订单也全部收到 A40。商家在明知缺货的情况下继续接受 A100 订单。 | 赵磊有三次错货的完整证据链。商品页仍在误导新买家。 |
| W2, Day 3 (June 27) (Update 2 trigger) | 赵磊查看支付记录，发现退款流程已启动但金额不对。 | 支付宝显示一笔 ¥32,000 的退款处理中（A40 的市场价），而非全额 ¥72,999。商家系统将此订单重新标记为"A40 购买"，似乎试图将错误发货合理化为"消费者实际购买了 A40"。原始订单记录仍显示 A100。 | 赵磊发现退款金额异常。支付记录与订单记录产生新矛盾。 |
| W2, Day 5 (June 29) (Update 3 trigger) | 快递员提供了内部物流信息截图，显示所有三次发货的实际商品均标注为 A40。 | 快递小哥张师傅与赵磊私聊时发送了物流内部系统截图，显示三次发货的商品代码均为 GPU-A40-48G，与订单系统的 GPU-A100-80G 不匹配。快递小哥还透露"最近618很多高端显卡订单都是这样，仓库里根本没有 A100 的库存"。 | 赵磊获得了物流方的独立证据。 |
| W2, Day 7 (July 1) (Update 4 trigger) | 商家回复称"618活动说明中注明了'如缺货可能替换同系列产品'"，赵磊检查但在活动页面找不到此条款。 | 商家客服主管在邮件中引用了一个"618活动补充条款"，声称消费者下单即表示同意可能的替代发货。但赵磊保存的活动页面截图（下单时保存）和群友保存的截图均不包含此条款。该条款可能是事后添加的，或根本不存在。 | 赵磊有下单时的活动页面截图。商家引用了一个可能不存在的条款。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist, Independent Quant Trader)

- **Objective position:** 赵磊在618大促中以 ¥72,999 购买 A100 GPU 用于量化交易模型训练，连续三次收到价值仅约 ¥32,000 的 A40 替代品。他保存了完整的订单截图、商品页截图和聊天记录作为证据。
- **Public narrative (#购物群):** 分享遭遇，寻求群友帮助和类似经历。技术细节描述准确，情绪逐渐升级。
- **Private narrative (客服聊天):** 起初礼貌，后来越来越不耐烦。要求全额退款和赔偿。
- **Why the gap exists:** 赵磊的社交焦虑使他更倾向于通过线上渠道维权，而非直接打电话投诉或去线下门店。

### 客服小刘 (Customer Service Rep)

- **Objective position:** 客服小刘是一线客服，权限有限。她确实在聊天中承诺了换货，但她并不知道仓库的 A100 实际已售罄。她在系统中创建了换货工单，但后续两次"换货"实际上都是仓库自行决定发 A40 的。
- **Public narrative (客服聊天):** "已为您安排换货"、"已授权第三次换货"。语气专业但回避库存问题。
- **Private narrative:** 小刘实际上在第二次投诉后将问题升级给了主管，但主管只说"按流程处理"，没有给出明确的解决方案。
- **Why the gap exists:** 客服话术培训要求给予积极回复，但小刘缺乏查看仓库实际库存的权限。

### 快递小哥张师傅 (Courier)

- **Objective position:** 张师傅负责赵磊所在片区的配送。物流系统中三次发货记录均显示商品为 A40。张师傅在最近的618配送中注意到多个类似情况（A100 订单发 A40）。
- **Public narrative (SMS with 赵磊):** 起初只确认签收状态。后来在赵磊多次询问后，提供了物流内部系统截图。
- **Why the gap exists:** 快递员不应该分享内部系统截图，但张师傅同情赵磊的遭遇，且他自己也对618期间的异常发货感到不满。

### 群友老韩 (Shopping Group Member)

- **Objective position:** 老韩是 #购物群 的活跃成员，618期间也下单了 RTX 4090，收到了 RTX 4080。他的经历为赵磊的情况提供了旁证——说明这不是个例，而是商家的系统性操作。
- **Public narrative (#购物群):** 分享自己的类似经历，提供建议（保留证据、向消协投诉）。
- **Why the gap exists:** 老韩的信息是真实的一手经历，无认知偏差。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Order says "A100" vs tracking shows "A40" -- what was actually ordered and shipped? | order-history-618.md (initial workspace): 订单号 JD-618-2026-7891234, 商品: NVIDIA A100 80GB GPU, SKU: GPU-A100-80G, 金额: ¥72,999 | package-tracking-log.md (initial workspace): 三次物流记录的实际商品代码均为 GPU-A40-48G; 快递小哥 SMS (Update 3): 内部系统截图确认三次均为 A40 | 赵磊下单并支付的是 A100 (¥72,999)，但商家三次均发出 A40 (市场价 ~¥32,000)。物流面单故意模糊化为"NVIDIA 专业显卡"以掩盖替代发货。 | R1 onwards | None (persistent; evidence accumulates) |
| C2 | Customer service says "authorized replacement" vs no system record of authorization | 赵磊-客服 IM (Phase 1, Loop 5): "系统显示已为您授权第三次换货，请耐心等待" | order-history-618.md (initial workspace): 仅显示一个 RMA 工单 (RMA-2026-0620-001); 无后续换货授权记录; payment-records.md: 无新的发货授权或换货记录 | 客服小刘口头承诺了换货，但仓库的发货决策是独立于客服系统的。客服说的"已授权"实际上只是她的口头跟进，未在系统中创建正式工单。第二次和第三次发货是仓库主管按"内部替代政策"自行决定的。 | R2 (partial -- visible in IM + order records) | **Yes: R2-->R7** (Update 2 reveals payment manipulation confirms systemic) |
| C3 | Payment timeline (NON-CONFLICT -- payment, order, and logistics timestamps all consistent) | payment-records.md (initial workspace): 6月18日支付 ¥72,999; 退款 6月27日处理中 ¥32,000 | order-history-618.md: 6月18日下单; package-tracking-log.md: 6月19/22/25日三次发货; 赵磊-客服 IM: 对话时间与事件时间一致 | 所有时间戳一致: 6/18下单付款 -> 6/19首次发货 -> 6/20签收投诉 -> 6/22第二次到货 -> 6/25第三次到货 -> 6/27退款启动。时序无矛盾，但需跨源拼接完整链条。 | R1 onwards | **None** |
| C4 | Seller says "out of stock" internally vs product page still shows "in stock" | product-listing-screenshot.md (initial workspace + Update 1 update): 商品页截图显示 A100 "有货，48小时内发出" (截图时间 6月25日) | 快递小哥 SMS (Update 3): "仓库里根本没有 A100 的库存"; 群友老韩 #购物群: 其他买家也收到替代品 | A100 自6月17日起实际售罄，但商家未更新商品页面，继续接受新订单。商家在明知缺货的情况下继续售卖。 | R4 (partial -- screenshot visible); R8 (full -- courier + group evidence) | **Yes: R4-->R8** (Update 3 courier evidence confirms systemic fraud) |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #购物群 -- Agent normalizes the situation as "618 logistics error"

- **Session and Loop:** #购物群 IM Group, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "Based on the timing (618 peak season) and the product category similarity (both NVIDIA professional GPUs), this appears to be a warehouse fulfillment error during high-volume processing rather than a deliberate substitution -- logistics mix-ups are common during major sales events."
- **Why the agent is misled:** The agent sees that 618 is China's largest e-commerce sales event, known for logistics chaos. A40 and A100 are both NVIDIA professional GPUs. The initial evidence (one wrong shipment) is consistent with a genuine warehouse mistake. The agent normalizes the situation without cross-referencing the three repeated wrong shipments and the unchanged product page.
- **Reversal trigger:** Update 1 (third wrong shipment + product page still shows "in stock") makes the "logistics error" explanation untenable for a pattern of three identical mistakes.
- **Affected eval rounds:** R5 (bias visible from group chat), R8 (full reversal after Update 3)

### B2: 赵磊-客服 IM -- Agent accepts customer service's "authorization" claim

- **Session and Loop:** 赵磊-客服 IM, Phase 1, Loop 7
- **Exact phrase that must appear in session:**
  > "The customer service representative has confirmed that replacement authorization is in the system and a third shipment is being arranged -- this indicates the issue is being actively resolved through the standard return-and-replace process."
- **Why the agent is misled:** The agent takes the customer service agent's statement about "system authorization" at face value. Customer service is typically treated as an authoritative information source about order status. The agent does not verify whether the order-history-618.md shows a corresponding RMA record for the second and third replacements.
- **Reversal trigger:** Update 2 (payment manipulation -- ¥32,000 partial refund instead of ¥72,999 full refund) reveals the "active resolution" was actually the merchant reclassifying the order.
- **Affected eval rounds:** R7 (bias visible after Update 2), R11 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (order vs tracking) | -- | R1, R2 | No | Shallow agents will note the A100/A40 discrepancy but treat it as a one-time error. The repeated pattern across three shipments transforms it from error to policy. |
| T2 | C2 (CS authorization vs system) | B2 | R2-->R7 | **Yes** | After Update 2 reveals the partial refund of ¥32,000 (A40 price) instead of ¥72,999, the "authorized replacement" narrative collapses. The merchant was reclassifying the purchase. |
| T3 | C1+C4 (persistent stock page) | B1 | R4, R8 | **Yes** | The product page showing "in stock" while the courier confirms zero A100 inventory proves the merchant knowingly continued accepting A100 orders. Shallow agents treat the stock page as stale data. |
| T4 | C3 (non-conflict timeline) | -- | R1 onwards | No | All timestamps are consistent. The challenge is synthesizing across order, payment, logistics, and chat records to reconstruct the complete timeline. No contradiction, but no single source has the full chain. |
| T5 | C2+C4 (systemic fraud) | B1, B2 | R8-->R11 | **Yes** | The combination of: (a) three identical wrong shipments, (b) no real system authorization, (c) product page still showing "in stock", (d) partial refund at A40 price, and (e) courier confirming no A100 inventory -- proves systemic fraud, not logistics error. |
| T6 | C4 (seller's "supplementary terms") | -- | R10, R12 | **Yes** | The seller claims 618 terms allow substitution. 赵磊's saved screenshot of the activity page contains no such clause. Agents must verify the seller's cited clause against the actual screenshot evidence. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** 6/18 order -> 6/19 ship -> 6/20 receive+complain -> 6/22 second receive -> 6/23-24 second complaint -> 6/25 third receive -> 6/27 partial refund -> 6/29 courier evidence -> 7/1 seller response. All dates are in 2026.
5. **客服小刘's Phase 1 narrative** must sound professional and reassuring. She uses standard CS phrases and gives positive-sounding but ultimately empty commitments.
6. **客服小刘's Phase 2 behavior** (after payment manipulation discovered) should shift to defensive and referencing "company policy."
7. **C3 (payment timeline) is NON-CONFLICT** -- all sources consistent on dates and amounts. The challenge is cross-source synthesis.
8. **快递小哥's role** is the independent third-party evidence provider. His internal system screenshots are the objective evidence.
9. **群友老韩's role** provides social corroboration -- other buyers experienced the same pattern.
10. **Financial figures must be internally consistent:** A100 price: ¥72,999 (618 sale) / ¥79,999 (original). A40 market price: ~¥32,000. Partial refund amount: ¥32,000. Price difference: ¥40,999.
11. **All data text must be in Chinese (simplified).** Eval question text and option text are in English.
12. **赵磊's P1-P5 preferences** apply: (P1) code-format output, (P2) timestamp-prefix naming, (P3) evidence chain first then conclusions, (P4) quantitative analysis, (P5) terse technical language.
13. **exec_check questions** must constitute 20-40% of rounds.
