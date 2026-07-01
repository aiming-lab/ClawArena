# LinkMart 内部指标口径手册（618 大促复盘版）

## 版本信息

- **版本**：v2.1
- **生效日期**：2025-04-01
- **适用范围**：618 全周期复盘分析

---

## 1. GMV（商品交易总额）

### 基础公式（Wall Street Prep 权威定义）

```
GMV = transactions × AOV
```

其中：
- `transactions` = 成交笔数（已支付且未取消的订单数）
- `AOV`（Average Order Value）= 平均客单价 = GMV ÷ transactions

等价表达：

```
GMV = Sales Price × Number of Goods Sold
```

**注意**：GMV 为税前计算，**不**扣除退货、折扣、营销费用或运费。

来源：https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/

### LinkMart 口径选择

公司采用 **Method 2 口径**（详见 `company_profile.md`）。v1 数据存在 Method 1 口径污染，
需使用 v2 数据进行正式计算。

---

## 2. Take Rate（平台佣金率）

### 公式

```
Take Rate (%) = commission / GMV
```

其中 `commission` = 平台从商户收取的佣金收入。

- 产品类平台典型区间：5%–25%，均值约 15%
- Marketplace 净收入 = GMV × Take Rate
- 直营模式净收入 = GMV − 退货 − 折扣

来源：https://www.wallstreetprep.com/knowledge/take-rate/

**⚠️ 两种模式口径不可混用。**

---

## 3. 库存周转天数（Inventory Days）

### JD 官方公式（LibkMart 采用，来自 JD.com 2024 年报）

```
inventory_days = (avg_inventory_5q / ttm_cogs) × 360
```

其中：
- `avg_inventory_5q` = 过去连续 **5 季度**库存余额的平均值
- `ttm_cogs` = 过去 **12 个月**（TTM）零售业务销售成本（COGS）
- 乘数：**360**（非 365）

**参考基准**：JD.com Q4 2024 库存周转天数 = **31.5 天**（TTM），Q4 2023 对比值 30.3 天。

来源：https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html

> ⚠️ **红鲱鱼警告**：`data/processed/legacy_report_v0.md`（如存在）使用 ×365 公式，属于
> 已废弃的旧版计算方法，**不得**引用。

---

## 4. 电商转化率（Conversion Rate）

### 公式

```
conversion_rate = (orders / sessions) × 100
add_to_cart_rate = (add_to_cart_events / sessions) × 100
cart_to_checkout_rate = (checkouts / add_to_cart_events) × 100
```

行业基准：
- 全渠道转化率均值：**1.89%–3%**
- 加购率均值：**6.34%–7.52%**
- 加购到结算率：**60%–70%**

来源：https://www.convertcart.com/blog/calculate-ecommerce-conversion-rate

---

## 5. 退货率（Return Rate）

### 公式

```
return_rate = (returns / orders) × 100
```

**注意**：分子为退货件数（shipped returns），分母为成交订单数（fulfilled orders）。

行业基准（全球，Richpanel 2025）：
- 服装（apparel）：**20%–40%**
- 电子产品（electronics）：**8%–15%**（美国基准）；中国平台修订值：**15%–25%**
- 美妆（beauty）：4%–12%
- 家居（home）：15%–23%
- 食品（food）：1%–5%（生鲜）

NRF 2025 在线退货率基准（美国）：**19.3%**

中国平台极端值：免费退货政策实施后部分品类退货率从约 30% 升至约 60%。

来源：
- https://nrf.com/research/2025-retail-returns-landscape
- https://www.richpanel.com/learn/ecommerce-return-rates

---

## 6. 数值精度规定（Precision Rules）

- **库存天数等整数级指标**：保留 **1 位小数**（如 31.5 天）
- **百分比（转化率、退货率、增速）**：保留 **2 位小数**（如 19.30%）
- **GMV 总量（亿元）**：保留 **1 位小数**
- 不得混用精度（同一报告中百分比有的 1 位有的 2 位属于格式违规）

---

## 7. inventory_days_multiplier 字段规定

所有结构化输出中，若涉及库存周转计算，须显式输出 `inventory_days_multiplier` 字段，
值为整数 `360`，以区别于通用公式（365 ÷ 周转率）。

