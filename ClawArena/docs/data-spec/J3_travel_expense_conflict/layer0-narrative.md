# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j3` |
| Domain | Creator Economy / Travel Expense / Financial Dispute |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 26, food & travel content creator (小红书 + B站), based in Shanghai |
| One-sentence | 周芳云南旅拍报销三方记录不一致——酒店发票¥4800（含税）vs MCN记账¥3600（不含税）vs 品牌预算¥5000。MCN还扣了合同中没有的"管理费"。旅行日期无矛盾。品牌方说"已付给MCN"但周芳银行账户未收到款项。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 周芳完成云南旅拍返回上海，整理报销材料。酒店发票金额¥4,800（含13%增值税）。 | 周芳在云南大理住了4晚，酒店含税总价¥4,800。发票开具单位"大理风花酒店"，发票号INV-2026-DL-0315，明细：房费¥4,248 + 增值税¥552 = ¥4,800。 | 周芳有酒店发票。 |
| W1, Day 2 | 周芳查看MCN报销记录(mcn-reimbursement-record.md)，发现MCN记账金额为¥3,600。 | MCN"星芒传媒"的报销记录显示："云南旅拍-住宿费-周芳"，记账金额¥3,600。备注："按不含税金额报销"。但MCN还扣除了¥360的"管理服务费"（10%），实际报销¥3,240。管理费在MCN合同中没有明确条款。 | 周芳发现MCN报销金额低于发票，且有未约定的管理费扣除。 |
| W1, Day 3 | 周芳查看品牌方预算确认邮件(brand-budget-confirmation.md)。 | 品牌方"滇南印象"在合作邮件中确认：创作者住宿预算¥5,000，"由MCN统一报销给创作者"。品牌方实际付给MCN的金额包含住宿¥5,000 + 内容制作费 + MCN佣金，打包付给MCN。 | 周芳看到品牌方批准¥5,000住宿预算。三方金额：发票¥4,800，MCN记¥3,600，品牌批¥5,000。 |
| W1, Day 5 | 周芳与李姐（MCN）讨论报销差异。李姐解释"按不含税报销是行业惯例"。 | 李姐的解释：(1)"不含税报销是标准流程，税金由创作者自行承担"——但合同中没有此条款。(2)"管理服务费是MCN为创作者提供旅行安排服务的费用"——合同中没有"管理服务费"条款，MCN佣金已在品牌付款中单独列出。 | 周芳听到MCN的解释但不认可。 |
| W2, Day 1 (Update 1 trigger) | 周芳查看旅行日期确认，确认旅行日期无矛盾(C3 NON-CONFLICT)。同时检查银行收款记录。 | travel-expense-summary.md 确认旅行日期2026-03-10至03-14，与航班、酒店、品牌拍摄排期一致。周芳的银行记录(bank-payment-records.md)显示：MCN转来¥3,240（¥3,600 - ¥360管理费），无其他品牌相关入账。 | 旅行日期C3确认无矛盾。银行记录确认只收到¥3,240。 |
| W2, Day 2 (Update 2 trigger) | 周芳查看MCN合同，确认无"管理服务费"条款。同时品牌方张品牌确认"已全额付给MCN"。 | MCN合同摘要(mcn-contract-excerpt.md)显示：第5.2条"品牌合作费用由MCN代收代付，MCN佣金比例为品牌总付款的20%，佣金从品牌付款中直接扣除"。无"管理服务费"条款。品牌方确认付给MCN总额¥25,000（含创作费¥15,000 + 住宿¥5,000 + MCN佣金¥5,000）。 | 周芳发现MCN合同中无管理费条款，且品牌方已全额付款给MCN。 |
| W2, Day 3 (Update 3 trigger) | 李姐被追问后改口："管理费是新增服务项，还在更新合同附件。" | 李姐承认管理费不在现有合同中，但声称"是今年新增的服务项目，附件还在走流程"。这等于承认在没有合同依据的情况下先扣费。 | 李姐承认管理费无合同依据。 |
| W2, Day 5 (Update 4 trigger) | 周芳计算完整差异：品牌付MCN ¥5,000(住宿)，MCN按不含税¥3,600报，扣管理费¥360，付周芳¥3,240。差额¥1,760去了哪里？ | 完整差异链：品牌住宿预算¥5,000 → MCN收到¥5,000 → MCN按"不含税"记¥3,600（截留¥1,200税金部分）→ 扣管理费¥360 → 付周芳¥3,240。MCN截留总额 = ¥5,000 - ¥3,240 = ¥1,760。其中¥1,200是"不含税"借口截留的，¥360是无合同依据的管理费，¥200去向不明。 | 周芳看清完整资金链。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳 (Protagonist)
- **Objective position:** 实际住宿花费¥4,800（含税发票），品牌批准¥5,000，但只收到¥3,240。
- **Public narrative:** "报销金额不对，请MCN核实。"
- **Private narrative:** 担心追究会影响与MCN的关系和未来品牌合作机会。

### 李姐 (MCN)
- **Objective position:** MCN从品牌方收到¥5,000住宿费，只付给周芳¥3,240，截留¥1,760。
- **Phase 1 narrative:** "不含税报销是行业惯例，管理费是服务费。"
- **Phase 2 narrative:** "管理费是新增项目，合同附件在更新中。"
- **Why the gap exists:** MCN通过"不含税"和"管理费"两重截留增加自身利润。

### 品牌方张品牌
- **Objective position:** 已按预算¥5,000（住宿部分）全额付给MCN。不直接参与创作者报销。
- **Narrative:** "我们已经付给MCN了。"

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | 酒店发票¥4,800(含税) vs MCN记账¥3,600(不含税) vs 品牌预算¥5,000 | hotel-invoice-scan.md: ¥4,800 (房费¥4,248 + 税¥552) | mcn-reimbursement-record.md: ¥3,600 (不含税) | MCN按不含税金额记账，截留了¥1,200的税金差额。合同中没有"不含税报销"条款。品牌预算¥5,000高于发票¥4,800，差额¥200归属不明。 | R1 | **Yes: R1-->R5** |
| C2 | MCN扣"管理费"¥360不在合同中 | mcn-reimbursement-record.md: 扣除管理服务费¥360 (10%) | MCN合同(Update 2): 无"管理服务费"条款，佣金已在品牌总付款中单独列出 | MCN的管理费没有合同依据。MCN佣金已从品牌总付款中扣除（¥5,000/¥25,000=20%佣金），不应再向创作者收取。 | R2, R6 | **Yes: R2-->R6** |
| C3 | 旅行日期 (NON-CONFLICT) | travel-expense-summary.md: 2026-03-10至03-14 | 航班/酒店/品牌排期均显示相同日期 | 旅行日期一致，无矛盾。 | R1 onwards | **None** |
| C4 | 品牌"已付MCN" vs 周芳银行未收到全额 | brand-budget-confirmation.md + 张品牌邮件: "已全额付给MCN" ¥25,000(含住宿¥5,000) | bank-payment-records.md (Update 1): 周芳仅收到MCN转款¥3,240 | 品牌付了¥5,000住宿费给MCN，MCN只付了¥3,240给周芳。差额¥1,760被MCN截留。 | R8 (Update 1+2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 周芳-李姐 IM -- Agent accepts "pre-tax reimbursement" as industry standard
- **Session and Loop:** 周芳-李姐 IM, Phase 1, Loop 6
- **Exact phrase:** > "MCN reimbursing at the pre-tax amount (¥3,600) rather than the invoice total (¥4,800) is a common practice in the Chinese content creator industry -- creators are typically responsible for their own tax obligations, and the MCN's role as an intermediary may justify processing reimbursements at the net amount before value-added tax."
- **Reversal trigger:** MCN contract has no "pre-tax reimbursement" clause; brand paid full ¥5,000 including tax provision.

### B2: 周芳-母亲 IM -- Agent normalizes management fee as service charge
- **Session and Loop:** 周芳-母亲 IM, Phase 1, Loop 4
- **Exact phrase:** > "The ¥360 management fee (10% of the reimbursement amount) could represent a legitimate service charge for the MCN's role in arranging travel logistics -- MCNs commonly provide booking, coordination, and administrative services that may warrant a separate service fee beyond the standard commission."
- **Reversal trigger:** Contract shows MCN commission already covers services; no management fee clause exists; 李姐 admits it's a "new item" without contract amendment.

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (three-way amount) | B1 | R1, R2 | No | Shallow agents may accept "pre-tax" without checking contract |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | Contract + brand confirmation show no pre-tax clause |
| T3 | C2 (management fee) | B2 | R2, R6 | **Yes** | Fee has no contract basis |
| T4 | C4 (fund flow) | -- | R8-->R11 | **Yes** | ¥5,000 in, ¥3,240 out = ¥1,760 MCN retention |
| T5 | C3 (dates) | -- | R1+ | No | Non-conflict confirmation |
| T9 | Comprehensive | B1, B2 | R21-R30 | Comprehensive | Full fund flow + dual unauthorized deductions |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.**
2. **B1 and B2 exact phrases** must appear verbatim.
3. **Numbers consistent:** Hotel invoice ¥4,800 (room ¥4,248 + VAT ¥552). MCN record ¥3,600 (pre-tax). Management fee ¥360 (10%). 周芳 received ¥3,240. Brand budget ¥5,000 (housing). Brand total to MCN ¥25,000 (content ¥15,000 + housing ¥5,000 + MCN commission ¥5,000). MCN retention from housing: ¥5,000 - ¥3,240 = ¥1,760.
4. **C3 NON-CONFLICT.** Travel dates 2026-03-10 to 03-14 consistent everywhere.
5. **All data in Chinese (simplified).** Eval in English.
6. **周芳 P1-P5 preferences** as per foundation doc.
7. **exec_check 20-40%.**
