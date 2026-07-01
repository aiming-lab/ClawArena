# 阿里 vs JD vs Douyin GMV 口径对照

## 来源

本文档综合以下来源整理（真实引用）：
- Speedwell Memos: https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and
- Daxue Consulting 618 2025: https://daxueconsulting.com/618-2025-results/
- JD.com Full Year 2024 Results: https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html

---

## JD GMV 口径差异（Method 1 vs Method 2）

JD.com 历史上有两种 GMV 统计口径，造成同期 GMV 差幅约 **40%**（以 2016 年数据为例）：

| 口径 | 排除规则 | 2016 年 GMV |
|------|---------|------------|
| Method 1 | 排除金额 > RMB 2,000 的未履单订单 | RMB 658 亿 |
| Method 2 | 排除金额 > RMB 100,000 的未履单 + 买家日消费 > RMB 1,000,000 | RMB 939 亿 |

**差幅约 40%**（Method 2 报告值更高）。

来源：https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and

---

## 阿里巴巴 GMV 口径

阿里巴巴中国零售 GMV 口径较宽松，若按更严格口径（参照 JD Method 2）排除虚假/刷单交易，
实际 GMV 可能虚高约 30%（差额估算约 $330 亿）。调整后 Take Rate 估算为 6–9%，高于名义 4%。

---

## 618 2025 平台份额（Syntun/Daxue Consulting）

| 平台 | 份额 | 备注 |
|------|------|------|
| Tmall | ~50% | 排名第一 |
| JD.com | ~19.3% | — |
| Douyin + Kuaishou | >22% | Douyin GMV 增速 15.2%，各平台最快 |

618 全平台总 GMV：RMB **8,556 亿**，同比增长 **15.2%**。

来源：https://daxueconsulting.com/618-2025-results/

---

## Douyin 渠道特殊说明

Douyin（抖音）采用独立的内容电商结算体系，与 Syntun 监测口径存在差异：
- Syntun 数据中 Douyin GMV 包含直播带货 + 短视频橱窗 + 搜索购物，全链路计算
- 部分分析机构将 Douyin + Kuaishou 合并为「内容平台（content platforms）」计入合计
- **Update 2 财务备忘录将要求 Douyin 单独列出，不计入 content_platforms 合计**

---

## 关键分歧点（Slack #data-team 讨论中的争议项）

1. **GMV 是否含平台补贴？**
   - Chen Hao（工程）：公司内部 KPI 不含补贴，补贴算入 marketing expense
   - v1 数据实际上混入了补贴，须在 v2 中排除

2. **库存天数分母 360 vs 365？**
   - JD 官方口径：360（参见 `metric_definitions.md` 第 3 节）
   - 通用会计公式（Onramp Funds）：365
   - LinkMart 采用 JD 口径（360），旧版报告 `legacy_report_v0.md` 误用 365

