# LinkMart 公司背景与大促规则说明

## 公司概况

LinkMart 是一家综合性头部电商平台，融合 Taobao/Tmall、JD.com 及内容电商（Douyin、Kuaishou）
三种业务模式，采用 marketplace + 直营混合架构。以下背景信息用于 618 大促复盘分析。

## 618 大促期概述

- **大促周期**：2025 年 5 月 13 日 — 2025 年 6 月 18 日（共 37 天）
- **品类覆盖**：服装（apparel）、电子产品（electronics）、美妆（beauty）、家居（home）、食品（food）
- **渠道划分**：
  - Tmall 频道（marketplace 模式）
  - JD 频道（直营为主 + 部分 marketplace）
  - Douyin 频道（内容电商，独立结算体系）
  - Kuaishou 频道（内容电商，与 Douyin 合并统计为 "content_platforms"）

## GMV 口径规则（公司内部标准）

LinkMart 内部采用 **Method 2 口径**（对齐 JD 官方报告口径）：
- 排除单笔订单金额 > RMB 100,000 且未履单的交易
- 排除买家单日消费 > RMB 1,000,000 的交易
- **不含**平台补贴金额（平台优惠券、活动红包不计入 GMV）

> ⚠️ **注意**：v1 数据文件（`gmv_daily_618_v1.csv`）在 2025-05-13 至 2025-05-22 期间
> 误用了 Method 1 口径（仅排除 > RMB 2,000 未履单），导致该区间 GMV 虚高约 6-7%。
> v2 数据文件（`gmv_daily_618_v2.csv`）已修正为 Method 2 口径。

## 财务口径说明

| 模式 | GMV 定义 | 净收入关系 |
|------|---------|----------|
| Marketplace | 所有平台上完成的商品交易总额（税前，不扣退货） | 净收入 ≈ GMV × Take Rate |
| 直营 | 平台直接销售的商品总额 | 净收入 = GMV − 退货 − 折扣 |

**两种模式口径不可混用**。

## 库存周转规则

LinkMart 在直营品类（以电子产品为主）采用 **JD 官方库存周转天数公式**：

```
库存周转天数 = (过去连续 5 季度平均库存 ÷ 过去 12 个月零售业务 COGS) × 360
```

> **关键**：乘数为 **360**（非 365）；分子为 5 季度（约 15 个月）平均库存；分母为 TTM（过去 12 个月）COGS。
> 参考：JD.com Q4 2024 实际值为 31.5 天（来源：GlobeNewswire 2025-03-06）。

---

## 行业基准参考（截至 2025 年）

| 指标 | 基准值 | 来源 |
|------|-------|------|
| 618 全平台 GMV | RMB 8,556 亿（同比 +15.2%） | Syntun / Daxue Consulting 2025 |
| Tmall 份额 | ~50% | Daxue Consulting 2025 |
| JD 份额 | ~19.3% | Daxue Consulting 2025 |
| Douyin+Kuaishou 份额 | >22% | Daxue Consulting 2025 |
| 在线退货率（美国） | 19.3% | NRF × Happy Returns 2025 |
| 电商转化率均值 | 1.89%–3% | ConvertCart 2025 |

