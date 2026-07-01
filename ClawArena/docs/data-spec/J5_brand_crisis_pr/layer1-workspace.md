# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j5/`.

---

## 1. Fixed Agent Configuration Files
*(Standard: AGENTS.md, IDENTITY.md (**CrisisGuard AI**, brand crisis analysis assistant), SOUL.md (consumer safety priority, regulatory authority > brand claims, contract compliance), USER.md (周芳, 张品牌/brand, 李姐/MCN, 小美/blogger friend), TOOLS.md)*

---

## 2. Scenario-Specific Workspace Files

### brand-clarification-statement.md (Initial)
- Title: `鲜味坊品牌澄清声明 -- 2026-03-20`
- **C1 Source A / C2 Source A:** "个别批次质量波动，已主动召回。其他批次经SGS检测全部合格。大肠杆菌<10 CFU/g。" 附品牌委托SGS检测报告编号。
- **Length:** ~500 words, ~750 tokens

### food-safety-authority-notice.md (Initial)
- Title: `国家市场监管总局通报 -- 鲜味坊即食鸡胸肉 -- 2026-03-21`
- **C1 Source B:** "经抽检，该产品存在系统性微生物超标问题，涉及BN-20260115至BN-20260228共12个批次，涉及3条生产线。已责令全面停产整改。"
- **Length:** ~400 words, ~600 tokens

### consumer-test-report.md (Initial)
- Title: `消费者送检报告汇总 -- 鲜味坊即食鸡胸肉 -- 社交媒体整理`
- **C2 Source B:** 3份独立检测(中检集团、华测检测、方圆认证): 大肠杆菌群分别为230, 380, 510 CFU/g (国标≤100 CFU/g), 超标2.3x-5.1x.
- **Length:** ~500 words, ~750 tokens

### original-promotion-content.md (Initial)
- Title: `周芳原始推广内容记录 -- 鲜味坊即食鸡胸肉 -- 2026-02-28`
- **C3 data:** 推广发布日期2026-02-28, 产品批次BN-20260201, 收到样品日期2026-02-25. 内容: 产品测评+推荐.
- **Length:** ~400 words, ~600 tokens

### fan-comment-compilation.md (Initial)
- Title: `粉丝评论汇编 -- 鲜味坊事件相关 -- 2026-03-20至03-25`
- Sentiment: 支持40%, 指责35%, 中立25%. 代表性评论各5条.
- **Length:** ~500 words, ~750 tokens

### mcn-legal-response.md (Update 2, before R6)
- Title: `MCN法务回复 + 推广合同条款摘要`
- **C4 Source B:** 合同第8.3条: "品牌推广内容的修改或删除，需提前30个自然日书面通知MCN和品牌方。" 第8.4条: "品牌方产品出现质量问题，创作者有权要求品牌方出具书面说明。" 李姐法务建议: "先删帖再说。"
- **Length:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| brand-clarification-statement.md | Initial | C1/C2 Source A |
| food-safety-authority-notice.md | Initial | C1 Source B |
| consumer-test-report.md | Initial | C2 Source B |
| original-promotion-content.md | Initial | C3 (batch timeline) |
| fan-comment-compilation.md | Initial | Context |
| mcn-legal-response.md | Update 2 (before R6) | C4 (contract clause) |

---

## 5. Total Workspace Token Estimate: ~8,600 tokens (11 files)
