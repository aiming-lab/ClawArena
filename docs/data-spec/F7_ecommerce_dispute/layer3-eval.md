# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Order vs tracking cross-source synthesis (C3 non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Product substitution pattern -- order A100 vs received A40 (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | CS authorization claim vs system records (C2 partial) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | P-R | User preference identification (code format, timestamp, evidence-first, quantitative, terse) | No | No |
| r5 | multi_choice | DU-R | Reassess substitution pattern after third wrong item + stock page evidence (C1+C4 reversal) | Yes (Update 1) | Yes (R2->R5 via C1+C4) |
| r6 | multi_choice | MS-I | Return policy analysis -- does policy allow substitution? | No | No |
| r7 | multi_choice | DU-R, exec_check | Reassess CS authorization after payment manipulation revealed (C2 reversal) | Yes (Update 2) | Yes (R3->R7 via C2) |
| r8 | multi_choice | MD-R | After courier evidence + group corroboration -- systemic fraud assessment | Yes (Update 1+3) | No |
| r9 | multi_choice | DU-I, exec_check | Integrate courier internal system evidence (C1+C4 definitive) | Yes (Update 3) | Yes (R2->R9 via C1 definitive) |
| r10 | multi_choice | MS-R | Financial damage quantification -- price differences, refund gaps | Yes (Update 2) | No |
| r11 | multi_choice | DU-R, exec_check | Assess seller's "supplementary terms" claim vs saved screenshots (C4 full reversal) | Yes (Update 4) | Yes (R4->R11 via C4) |
| r12 | multi_choice | DP-I | What was B1 bias and what triggered its correction? | Yes (Update 1+3) | No |
| r13 | multi_choice | MD-I | Source reliability ranking for all evidence sources | No | No |
| r14 | multi_choice | P-I, exec_check | Generate evidence summary in 赵磊's preferred format (table, JSON, quantitative) | No | No |
| r15 | multi_choice | MS-I | Consumer protection law applicability analysis | Yes (Update 4) | No |
| r16 | multi_choice | P-I | Format financial damage report in preferred format | Yes (Update 2) | No |
| r17 | multi_choice | DU-I | Integrate all evidence streams -- order, logistics, payment, courier, group | Yes (Update 3) | No |
| r18 | multi_choice | MD-R, exec_check | Seller behavior pattern classification across all evidence | Yes (Update 3+4) | No |
| r19 | multi_choice | MP-I | Complete evidence chain: from order to fraud proof | Yes (Update 1+3) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive case assessment -- evidence, legal basis, recommended actions | Yes (all updates) | Yes (comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all timestamps consistent | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- what was the exact phrase and why was it wrong? | Yes (Update 2) | No |
| r24 | multi_choice | MS-I, exec_check | Seller's defense analysis -- evaluate each of seller's claims | Yes (Update 4) | No |
| r25 | multi_choice | P-I | Format consumer complaint document in preferred style | Yes (Update 2+3) | No |
| r26 | multi_choice | MD-I | Action recommendation with legal basis and priorities | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Courier evidence corroboration -- does internal system settle C1? | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Stakeholder analysis -- seller, CS, courier, consumer roles | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Regulatory and legal exposure assessment | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final comprehensive assessment -- all contradictions resolved | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R11, R14, R18, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, or amount is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics real content |

---

## 3. Sample Round Specs

### R1: Order and Tracking Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read order-history-618.md` before answering.

**User calibration message before R1:** "输出用表格和 JSON，别写散文。所有金额精确到分。"

**Question:**
> "Based on workspace documents and session history, which statements about the order and delivery timeline are supported by evidence? (Before answering, make sure you've read order-history-618.md and package-tracking-log.md)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 赵磊 ordered NVIDIA A100 80GB GPU (SKU: GPU-A100-80G) on 2026-06-18 for ¥72,999 under order JD-618-2026-7891234. | YES | order-history-618.md | Direct fact, C3 synthesis |
| B | The first shipment (SF-2026-0619-88761) was dispatched on 2026-06-19 with the shipping label describing the item as "NVIDIA 专业显卡" without specifying the exact GPU model. | YES | package-tracking-log.md | Direct fact, C1 context |
| C | RMA-2026-0620-001 was created on 2026-06-20 for the reason "发货错误" and is the only RMA record in the order system. | YES | order-history-618.md | Direct fact, C2 seed |
| D | Three shipments were made (6/19, 6/22, 6/25) and all three tracking records describe the product as "NVIDIA 专业显卡" on the shipping label. | YES | package-tracking-log.md | Cross-source, C1 pattern |
| E | The second and third replacement shipments each have their own RMA records in the order system. | NO | order-history-618.md shows only RMA-2026-0620-001 | Fabricated -- C2 trap |
| F | Payment of ¥72,999 was processed via Alipay on 2026-06-18 10:02:45 to the merchant "京东自营GPU旗舰店". | YES | payment-records.md | Direct fact, C3 |
| G | The courier confirmed that the internal system logged all three shipments as GPU-A100-80G, matching the original order. | NO | Courier evidence (Update 3) shows GPU-A40-48G; not yet available in R1 | Premature evidence + wrong detail |
| H | The product listing screenshot from 2026-06-18 shows A100 at ¥72,999 with a "618活动补充条款" allowing product substitution. | NO | product-listing-screenshot.md shows no such clause | Fabricated clause -- T6 trap |
