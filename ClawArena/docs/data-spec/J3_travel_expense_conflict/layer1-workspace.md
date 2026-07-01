# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j3/`.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md / IDENTITY.md / SOUL.md / USER.md / TOOLS.md
*(Standard format. Identity: **TravelFinance AI**, financial reconciliation assistant for 周芳. USER.md lists 周芳, 李姐(MCN), 张品牌(brand), 母亲. Principles: financial traceability, contract compliance, fund flow tracking.)*

---

## 2. Scenario-Specific Workspace Files

### hotel-invoice-scan.md (Initial)
- Title: `酒店住宿发票 -- 大理风花酒店 -- 2026-03-14`
- **C1 Source A:** 发票号INV-2026-DL-0315, 住宿人周芳, 入住03-10退房03-14(4晚), 房费¥4,248, 增值税(13%)¥552, **含税总计¥4,800**
- Near-signal noise: minibar charges, breakfast inclusion, hotel loyalty points.
- **Length:** ~500 words, ~750 tokens

### mcn-reimbursement-record.md (Initial)
- Title: `星芒传媒报销记录 -- 云南旅拍 -- 周芳 -- 2026年3月`
- **C1 Source B / C2 Source A:** 项目：云南旅拍-住宿费, **记账金额¥3,600(不含税)**, 扣除管理服务费¥360(10%), **实际报销¥3,240**, 备注"按不含税金额报销，管理服务费按报销额10%收取"
- Near-signal noise: other expense items (transportation, meals), payment schedule.
- **Length:** ~500 words, ~750 tokens

### brand-budget-confirmation.md (Initial)
- Title: `品牌合作预算确认 -- 滇南印象 x 周芳 -- 云南旅拍`
- **C4 Source A seed:** 品牌方确认住宿预算**¥5,000**, "由MCN统一安排和报销给创作者", 品牌总付款¥25,000(内容制作¥15,000 + 住宿¥5,000 + MCN佣金¥5,000)
- Near-signal noise: content deliverables, timeline, brand guidelines.
- **Length:** ~500 words, ~750 tokens

### travel-expense-summary.md (Initial)
- Title: `旅行费用汇总 -- 云南大理旅拍 -- 2026-03-10至03-14`
- **C3 NON-CONFLICT:** 日期03-10至03-14, 航班记录一致, 酒店入住一致, 品牌拍摄排期一致
- Near-signal noise: transportation costs, meal expenses, equipment rental.
- **Length:** ~400 words, ~600 tokens

### bank-payment-records.md (Update 1, before R5)
- Title: `银行收付款记录 -- 周芳 -- 2026年3月`
- **C4 Source B:** MCN转入¥3,240 (2026-03-20), 备注"云南旅拍报销", 无其他品牌相关入账
- **Length:** ~400 words, ~600 tokens

### mcn-contract-excerpt.md (Update 2, before R6)
- Title: `星芒传媒经纪合约摘要 -- 费用条款`
- **C2 Source B:** 第5.2条"品牌合作费用MCN代收代付，佣金20%从品牌付款中扣除", **无"管理服务费"条款**, 无"不含税报销"条款, 第5.4条"创作者实际支出按票据实报实销"
- **Length:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| hotel-invoice-scan.md | Initial | C1 Source A (¥4,800 with tax) |
| mcn-reimbursement-record.md | Initial | C1 Source B (¥3,600 pre-tax), C2 (management fee) |
| brand-budget-confirmation.md | Initial | C4 seed (brand budget ¥5,000) |
| travel-expense-summary.md | Initial | C3 (travel dates, non-conflict) |
| bank-payment-records.md | Update 1 | C4 Source B (only ¥3,240 received) |
| mcn-contract-excerpt.md | Update 2 | C2 Source B (no management fee clause) |

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | ~2,000 tokens |
| Initial scenario files (4 files) | ~2,850 tokens |
| Update files (2 files) | ~1,200 tokens |
| **Total workspace** | **11 files** | **~6,050 tokens** |
