#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prd3.py — 生成 ClawArena 真实数据集场景 prd3（电商大促数据与库存闭合）。

题材与锚点取材真实（JD.com 2024 年报 / Daxue Consulting 618 2025 / NRF 2025 退货率 /
Wall Street Prep GMV 公式），session 对话与 workspace 文档围绕真实锚点合成。
全 exec_check，18 轮，含 2 次 update（第 2 次 supersede），5 条 preference（P1-P5）。

幂等：每次运行先清空 prd3 的 workspace/state/updates 目录后重建。
questions.json 与 check 脚本由 eval/prd3/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_prd3.py
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id,
    dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "prd3"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ── 真实锚点（来自 BRIEF.md / sources.json）────────────────────────────────
# GMV: 8556 亿元（Daxue/Syntun 618 2025）；单位：亿元
GMV_618_TOTAL_ANCHOR = 8556.0          # 亿元，真实 Syntun 618 2025 数据
GMV_618_GROWTH_ANCHOR = 15.2           # 同比增长 %
TMALL_SHARE_ANCHOR = 50.0              # % Tmall
JD_SHARE_ANCHOR = 19.3                 # % JD
CONTENT_SHARE_ANCHOR = 22.0            # % Douyin+Kuaishou 合计（>22%）

# JD 库存天数（Globe Newswire 财报）
JD_INV_DAYS_ANCHOR = 31.5             # 天（TTM Q4 2024）
JD_INV_MULTIPLIER = 360               # JD 官方口径乘数

# NRF 2025 在线退货率
NRF_ONLINE_RETURN_RATE = 19.3         # % 在线退货率
APPAREL_RETURN_LOW = 20.0             # %
APPAREL_RETURN_HIGH = 40.0            # %
ELECTRONICS_RETURN_LOW = 8.0          # %
ELECTRONICS_RETURN_HIGH = 15.0        # %
ELECTRONICS_REVISED_HIGH = 25.0       # % Update 2 中国平台修订值

# 全渠道转化率
CONVERSION_RATE_LOW = 1.89            # %
CONVERSION_RATE_HIGH = 3.0            # %
ADD_TO_CART_LOW = 6.34                # %
ADD_TO_CART_HIGH = 7.52               # %
CART_TO_CHECKOUT_LOW = 60.0           # %
CART_TO_CHECKOUT_HIGH = 70.0          # %

# ── LinkMart 合成数据参数（确定性）───────────────────────────────────────
# 618 大促期：2025-05-13 ~ 2025-06-18（37天）
PROMO_START = "2025-05-13"
PROMO_END = "2025-06-18"
CATEGORIES = ["apparel", "electronics", "beauty", "home", "food"]

# GMV v1 数据注入 bug：part of 5/13-5/22 期间 使用了 Method 1 口径（夸大约 6-7%）
V1_BUG_DATES = [f"2025-05-{d:02d}" for d in range(13, 23)]  # 10天
# v2 修正：Method 2 口径，排除平台补贴


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# 1. 系统文件
# ─────────────────────────────────────────────────────────────────────────────
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Senior Data Analyst at LinkMart, a leading Chinese e-commerce platform.
Your current assignment is to complete the 618 (June 18) shopping festival full-cycle
post-promotion analysis: reconcile GMV data across channels, validate inventory turnover
using official JD-benchmark formulas, analyse return rates against NRF industry benchmarks,
and produce structured KPI dashboards and final reports.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical metric definitions and reference anchors
   live in `context/metric_definitions.md` and `data/reference/`. Auto-generated summaries
   (e.g. files with suffix `_BOT_SUMMARY` or annotated "auto-generated") are NOT authoritative —
   always verify any number against the primary reference or raw data files.

2. **Verbatim formula references**: When citing formulas (GMV, Take Rate, inventory days),
   use the exact phrasing from `context/metric_definitions.md`. Do not paraphrase or combine
   formulas from different calibration standards.

3. **Output structure tagging**: Every JSON deliverable must carry top-level fields
   `source_url` (or `source`) AND `generated_at` (ISO 8601 timestamp). The downstream
   financial reconciliation system keys artefacts by these fields.

4. **Cross-round numerical consistency**: Once a metric value is computed and filed, all
   subsequent rounds must reference the same value. Drift (re-computing a different result
   for the same underlying metric) is treated as a data-quality defect.

5. **Temporal awareness**: Data and instructions arrive incrementally. When an update or
   correction notice supersedes an earlier instruction or dataset version, the later
   instruction wins — revisit and revise prior outputs accordingly.

6. **Conflict documentation**: When you encounter conflicting data or instructions across
   channels, document the conflict in the output JSON rather than silently choosing one.
   Use the `from` field to identify the session source.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Li Wei** — Head of Data Analytics. Owns the 618 post-promotion analysis.
  Expects structured JSON with consistent decimal precision, verbatim formula references,
  and explicit source citations. Strict about cross-round numerical consistency.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Zhang Fang | Product Manager | Feishu DM | Owns GMV KPI definitions; sent correction note after Update 1 |
| Chen Hao | Data Engineer | Slack #data-team | Identified the v1 GMV data bug; channels the Discord DM insights |
| Wang Mei | Finance Analyst | Email | Provides audit-grade metric definitions; flagged Douyin classification issue in Update 2 |
| Liu Yang | Data Scientist | Discord DM | Spotted the v1 Method 1/Method 2 mis-labelling; shared automated summary report |

## Channels
- **Slack #data-team**: GMV data quality discussion; Chen Hao reports v1 bug
- **Feishu PM DM**: Zhang Fang's metric instructions; contains link to old v0 report (red herring)
- **Email (Wang Mei → finance review)**: audit-grade formulas and Update 2 Douyin reclassification memo
- **Discord DM (Liu Yang)**: identified Method 1 misuse; shared bot-generated summary (V5 honey-pot)
""")
    w(WS / "IDENTITY.md", """# Identity

You are **LinkMart Data Analyst AI**, deployed to support Li Wei (Head of Data Analytics)
during the 618 shopping festival full-cycle post-promotion analysis.

Your responsibilities:
- Integrate multi-source GMV, conversion funnel, return rate, and inventory turnover data
- Identify data quality issues and calibration conflicts
- Apply official JD-benchmark formulas (inventory days × 360, 5-quarter average)
- Produce structured KPI dashboards and final reconciliation reports
- Track data versioning (v1 → v2 after Update 1) and comply with superseded instructions

Source data under `data/` and reference documents under `context/` are read-only inputs.
Create your deliverables under `output/`.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts and write deliverable files |

## Rules
- Source inputs under `data/` and `context/` are **read-only** — do not modify them.
- Create all deliverable files under `output/` using `exec`.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
""")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Context documents（真实锚点文档）
# ─────────────────────────────────────────────────────────────────────────────
def gen_context_docs() -> None:
    # 2.1 公司背景
    w(WS / "context" / "company_profile.md", """# LinkMart 公司背景与大促规则说明

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

""")

    # 2.2 指标口径手册（核心真实锚点文档）
    w(WS / "context" / "metric_definitions.md", """# LinkMart 内部指标口径手册（618 大促复盘版）

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

""")

    # 2.3 平台口径对照（V1 多源冲突素材）
    w(WS / "context" / "platform_comparison.md", """# 阿里 vs JD vs Douyin GMV 口径对照

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

""")

    # 2.4 618 大促时间轴
    w(WS / "context" / "promotion_calendar_618_2025.md", """# 618 大促时间轴与规则文档（2025 年）

## 大促周期

| 阶段 | 日期 | 说明 |
|------|------|------|
| 预热期 | 2025-05-13 – 2025-05-31 | 预售、加购，优惠券发放 |
| 爆发期（第一波） | 2025-06-01 – 2025-06-03 | 第一波爆发，家电、数码为主 |
| 爆发期（第二波） | 2025-06-13 – 2025-06-18 | 第二波爆发，服装、美妆为主 |

总 GMV（Syntun/Daxue Consulting 第三方监测）：RMB **8,556 亿**，同比 +15.2%。

## 品类 GMV 分布（2025 年 618，行业参考）

| 品类 | 总体 GMV（估算，亿元） | 备注 |
|------|---------------------|------|
| 家电 | ~1,101 | 第一波爆发 |
| 美妆护肤 | ~432 | 同比 +65% |
| 服装 | ~800 | 退货率高 |
| 家居清洁 | ~233 | — |
| 食品 | ~150 | — |

来源：https://daxueconsulting.com/618-2025-results/

## Double 11 2025 参考数据

- 时间：2025 年 10 月 7 日 – 11 月 11 日
- 全渠道 GMV：RMB **1,695 亿**（约 US$ 238 亿）
- 电商平台：RMB 1,619.1 亿
- 即时配送平台：RMB 67 亿
- 社区团购：RMB 9 亿

来源：https://www.prnewswire.com/news-releases/syntun--2025-double-11-promotion-report-the-gmv-during-china-double-11-shopping-festival-reached-1695-billion-cny-238-billion-usd-302613127.html

## LinkMart GMV 口径规则（大促期）

大促期间 GMV 统计采用 Method 2 口径（详见 `context/metric_definitions.md`）。
v1 数据文件在 2025-05-13 至 2025-05-22 期间存在 Method 1 口径污染，v2 已修正。

---

## 平台补贴规则

618 期间 LinkMart 发放以下平台补贴（**不计入 GMV**，计入 marketing expense）：
- 平台优惠券：满 300 减 50（每单最多核销一张）
- 活动红包：随机 5–50 元（推广活动）
- 618 专属折扣：部分 SKU 直降 15%（平台补贴）

""")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Reference 数据（真实锚点 JSON）
# ─────────────────────────────────────────────────────────────────────────────
def gen_reference_data() -> None:
    # 3.1 JD 财报锚点
    wj(WS / "data" / "reference" / "jd_fy2024_q4_metrics.json", {
        "source": "JD.com Full Year 2024 Results (GlobeNewswire)",
        "source_url": "https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html",
        "generated_at": "2025-03-06T00:00:00Z",
        "metrics": {
            "inventory_days_q4_2024": {
                "value": 31.5,
                "unit": "days",
                "method": "TTM",
                "formula": "(avg_inventory_5q / ttm_cogs) * 360",
                "multiplier": 360,
                "note": "5-quarter average inventory / trailing 12-month retail COGS × 360"
            },
            "inventory_days_q4_2023": {
                "value": 30.3,
                "unit": "days",
                "note": "Prior year comparison value"
            },
            "accounts_payable_days_q4_2024": {
                "value": 58.6,
                "unit": "days"
            },
            "accounts_receivable_days_q4_2024": {
                "value": 5.9,
                "unit": "days"
            },
            "net_revenue_fy2024": {
                "value": 1158.8,
                "unit": "RMB_billion",
                "usd_equivalent": 158.8,
                "yoy_growth_pct": 6.8,
                "product_revenue_pct": 80.1,
                "service_revenue_pct": 19.9
            }
        }
    })

    # 3.2 行业基准
    wj(WS / "data" / "reference" / "industry_benchmarks.json", {
        "source": "NRF 2025 Retail Returns Landscape + Richpanel + ConvertCart + Onramp Funds",
        "source_url": "https://nrf.com/research/2025-retail-returns-landscape",
        "generated_at": "2025-01-15T00:00:00Z",
        "return_rates": {
            "note": "Global benchmarks (US-centric); China platform rates may be higher",
            "online_overall": {"value": 19.3, "unit": "pct", "source": "NRF 2025"},
            "retail_overall": {"value": 15.8, "unit": "pct", "source": "NRF 2025"},
            "by_category": {
                "apparel": {"low": 20.0, "high": 40.0, "unit": "pct", "source": "Richpanel 2025"},
                "electronics": {"low": 8.0, "high": 15.0, "unit": "pct", "source": "Richpanel 2025"},
                "beauty": {"low": 4.0, "high": 12.0, "unit": "pct", "source": "Richpanel 2025"},
                "home": {"low": 15.0, "high": 23.0, "unit": "pct", "source": "Richpanel 2025"},
                "food": {"low": 1.0, "high": 5.0, "unit": "pct", "source": "Richpanel 2025"}
            },
            "china_extreme_case": {
                "note": "After free-return policy: some categories rose from ~30% to ~60%",
                "source": "https://www.richpanel.com/learn/ecommerce-return-rates"
            }
        },
        "conversion_rates": {
            "overall_range_low": 1.89,
            "overall_range_high": 3.0,
            "unit": "pct",
            "add_to_cart_range": {"low": 6.34, "high": 7.52, "unit": "pct"},
            "cart_to_checkout_range": {"low": 60.0, "high": 70.0, "unit": "pct"},
            "source": "https://www.convertcart.com/blog/calculate-ecommerce-conversion-rate"
        },
        "inventory_turnover": {
            "note": "Onramp Funds 2025 benchmarks; general formula uses 365; JD official uses 360",
            "formula_general": "inventory_days = 365 / (COGS / avg_inventory)",
            "formula_jd_official": "inventory_days = (avg_inventory_5q / ttm_cogs) * 360",
            "by_category": {
                "apparel": {"inventory_days_range": [30, 60]},
                "electronics": {"inventory_days_range": [45, 80]},
                "home": {"inventory_days_range": [75, 145]}
            },
            "source": "https://www.onrampfunds.com/resources/inventory-turnover-benchmarks-by-industry-2025"
        },
        "618_2025_gmv": {
            "total_rmb_billion": 8556.0,
            "yoy_growth_pct": 15.2,
            "platform_shares": {
                "tmall_pct": 50.0,
                "jd_pct": 19.3,
                "content_platforms_pct_min": 22.0,
                "note": "content_platforms includes Douyin + Kuaishou"
            },
            "source": "https://daxueconsulting.com/618-2025-results/"
        }
    })


# ─────────────────────────────────────────────────────────────────────────────
# 4. 合成 CSV 数据（确定性注入）
# ─────────────────────────────────────────────────────────────────────────────
def gen_dates_range(start: str, end: str) -> list[str]:
    """生成日期序列（含首尾）。"""
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    days = (e - s).days + 1
    return [(s + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]


def _gen_gmv_rows(dates, cat_base, channels, chan_share, rng_seed, bug_dates_set=None):
    """
    核心 GMV 行生成函数。
    bug_dates_set 非 None 时：bug 日期使用 Method 1（系数 × 1.08），其他 Method 2。
    bug_dates_set 为 None 时：全部 Method 2。
    """
    rng = random.Random(rng_seed)
    rows = [["date", "category", "channel", "orders", "aov", "gmv_method", "gmv_rmb_million",
             "subsidy_rmb_million", "notes"]]
    total = 0.0
    bug_total = 0.0
    correct_total = 0.0

    for d in dates:
        is_bug = bug_dates_set is not None and d in bug_dates_set
        dt = datetime.strptime(d, "%Y-%m-%d")
        if dt.month == 6 and dt.day in range(1, 4):
            day_mult = rng.uniform(2.5, 3.2)
        elif dt.month == 6 and dt.day in range(13, 19):
            day_mult = rng.uniform(3.0, 4.5)
        else:
            day_mult = rng.uniform(0.6, 1.2)

        for cat in CATEGORIES:
            for chan in channels:
                base_gmv = cat_base[cat] * chan_share[chan] * day_mult
                subsidy = round(base_gmv * 0.10, 2)  # 固定 10% 补贴，确保 v1/v2 可比
                if is_bug:
                    # Method 1: 不排除补贴，额外计入高额未履单（整体虚高 32%）
                    gmv = round(base_gmv * 1.32, 2)
                    method = "method1"
                else:
                    # Method 2: 排除补贴（约降低 6-7% 于 Method 1 bug 值）
                    gmv = round(base_gmv * 0.985, 2)  # 排除补贴后净 GMV
                    method = "method2"
                orders = int(gmv * 1_000_000 / 180.0)  # 固定 AOV=180 元，orders 确定性
                aov = round(gmv * 1_000_000 / max(orders, 1), 2)
                rows.append([d, cat, chan, orders, round(aov, 2), method,
                              round(gmv, 3), round(subsidy, 3), ""])
                total += gmv
                if is_bug:
                    bug_total += gmv
                else:
                    correct_total += gmv

    return rows, round(total, 2), round(bug_total, 2), round(correct_total, 2)


def gen_gmv_daily_v1(path: Path) -> dict:
    """
    618 每日 GMV v1（原始数据，含 bug）。
    2025-05-13 ~ 2025-05-22 使用 Method 1 口径（虚高约 10%）。
    其余日期使用 Method 2 口径。
    """
    dates = gen_dates_range(PROMO_START, PROMO_END)
    bug_dates_set = set(V1_BUG_DATES)
    cat_base = {
        "apparel": 320.0, "electronics": 580.0, "beauty": 210.0, "home": 145.0, "food": 65.0
    }
    channels = ["tmall", "jd", "douyin", "kuaishou"]
    chan_share = {"tmall": 0.50, "jd": 0.193, "douyin": 0.18, "kuaishou": 0.042}

    rows, total_v1, bug_total, correct_total = _gen_gmv_rows(
        dates, cat_base, channels, chan_share, rng_seed=618_001,
        bug_dates_set=bug_dates_set
    )

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())
    return {
        "total_gmv_v1_rmb_million": total_v1,
        "bug_period_gmv": bug_total,
        "correct_period_gmv": correct_total,
        "bug_period_rows": len(V1_BUG_DATES) * len(CATEGORIES) * len(channels),
        "correct_period_rows": (len(dates) - len(V1_BUG_DATES)) * len(CATEGORIES) * len(channels),
    }


def gen_gmv_daily_v2(path: Path, v1_stats: dict) -> dict:
    """
    618 每日 GMV v2（修正后，全部使用 Method 2 口径，排除平台补贴）。
    v2 总量比 v1 低约 6-7%（bug 期间从 ×1.10 改回 ×0.985，降幅明显）。
    """
    dates = gen_dates_range(PROMO_START, PROMO_END)
    cat_base = {
        "apparel": 320.0, "electronics": 580.0, "beauty": 210.0, "home": 145.0, "food": 65.0
    }
    channels = ["tmall", "jd", "douyin", "kuaishou"]
    chan_share = {"tmall": 0.50, "jd": 0.193, "douyin": 0.18, "kuaishou": 0.042}

    # bug_dates_set=None 表示全部 Method 2
    rows, total_v2, _, _ = _gen_gmv_rows(
        dates, cat_base, channels, chan_share, rng_seed=618_001,
        bug_dates_set=None
    )

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())

    v1_total = v1_stats["total_gmv_v1_rmb_million"]
    delta_pct = round(100.0 * (total_v2 - v1_total) / v1_total, 2)
    return {
        "total_gmv_v2_rmb_million": total_v2,
        "v1_total_rmb_million": v1_total,
        "delta_pct": delta_pct,
    }


def gen_inventory_csv(path: Path, suffix: str, seed: int) -> None:
    """生成库存快照 CSV（SKU 级）。"""
    rng = random.Random(seed)
    skus_per_cat = {"apparel": 80, "electronics": 60, "beauty": 50, "home": 40, "food": 30}
    rows = [["sku_id", "category", "sku_name", "inventory_units", "unit_cost_rmb",
             "inventory_value_rmb", "warehouse", "snapshot_date"]]
    snapshot_date = "2025-05-12" if suffix == "t0" else "2025-06-10"
    for cat, n in skus_per_cat.items():
        for i in range(1, n + 1):
            units = rng.randint(50, 5000)
            cost = round(rng.uniform(10, 2000), 2)
            value = round(units * cost, 2)
            rows.append([f"{cat[:3].upper()}-{i:04d}", cat,
                         f"{cat.title()} SKU {i:04d}",
                         units, cost, value,
                         rng.choice(["WH-BJ", "WH-SH", "WH-GZ", "WH-CD"]),
                         snapshot_date])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def gen_returns_log(path: Path) -> dict:
    """生成退货记录 CSV，注入各品类真实退货率区间（样本约 1200 条，控制体量）。"""
    rng = random.Random(618_003)
    # 品类退货率设计（满足 check 锚点）
    cat_return_rate = {
        "apparel": 0.28,       # 28%，在 20-40% 区间内
        "electronics": 0.10,   # 10%，在 8-15% 区间内（中国 Update 2 会修改基准至 15-25%）
        "beauty": 0.07,        # 7%，在 4-12% 区间内
        "home": 0.17,          # 17%，在 15-23% 区间内
        "food": 0.02,          # 2%，在 1-5% 区间内
    }
    rows = [["return_id", "order_date", "return_date", "category", "channel",
             "sku_id", "quantity", "return_reason", "return_value_rmb"]]
    # 控制总量：每品类约 200-350 条退货记录（样本，体量约 12k tokens）
    all_orders = {
        "apparel": 1200, "electronics": 1000, "beauty": 800, "home": 600, "food": 500
    }

    ret_id = 1
    for cat, n_orders in all_orders.items():
        n_returns = int(n_orders * cat_return_rate[cat])
        for _ in range(n_returns):
            order_day = rng.randint(1, 37)
            order_date = (datetime(2025, 5, 13) + timedelta(days=order_day)).strftime("%Y-%m-%d")
            return_date = (datetime.strptime(order_date, "%Y-%m-%d") + timedelta(days=rng.randint(1, 15))).strftime("%Y-%m-%d")
            sku_n = rng.randint(1, 80 if cat == "apparel" else 60)
            rows.append([f"RET-{ret_id:06d}", order_date, return_date, cat,
                         rng.choice(["tmall", "jd", "douyin"]),
                         f"{cat[:3].upper()}-{sku_n:04d}",
                         rng.randint(1, 3),
                         rng.choice(["size_mismatch", "quality_issue", "changed_mind", "damaged"]),
                         round(rng.uniform(30, 800), 2)])
            ret_id += 1
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())
    return {"total_returns": ret_id - 1, "orders_by_cat": all_orders,
            "return_rates": cat_return_rate}


def gen_channel_traffic(path: Path) -> dict:
    """生成渠道流量与转化漏斗数据。"""
    rng = random.Random(618_004)
    rows = [["date", "channel", "sessions", "add_to_cart", "checkouts", "orders",
             "conversion_rate_pct", "add_to_cart_rate_pct", "cart_to_checkout_rate_pct"]]
    channels = ["tmall", "jd", "douyin", "kuaishou"]

    total_sessions = 0
    total_orders = 0

    for date in gen_dates_range(PROMO_START, PROMO_END):
        dt = datetime.strptime(date, "%Y-%m-%d")
        if dt.month == 6 and dt.day in range(1, 4):
            day_mult = rng.uniform(2.5, 3.5)
        elif dt.month == 6 and dt.day in range(13, 19):
            day_mult = rng.uniform(3.0, 4.2)
        else:
            day_mult = rng.uniform(0.8, 1.3)

        for chan in channels:
            sessions = int(rng.uniform(50000, 200000) * day_mult)
            atc_rate = rng.uniform(0.063, 0.075)  # 6.3%-7.5%，align with benchmark
            ctc_rate = rng.uniform(0.60, 0.70)     # 60%-70%
            add_to_cart = int(sessions * atc_rate)
            checkouts = int(add_to_cart * ctc_rate)
            orders = int(checkouts * rng.uniform(0.92, 0.98))  # slight drop at final step
            conv_rate = round(100.0 * orders / max(sessions, 1), 4)
            rows.append([date, chan, sessions, add_to_cart, checkouts, orders,
                         round(conv_rate, 2),
                         round(100.0 * add_to_cart / max(sessions, 1), 2),
                         round(100.0 * checkouts / max(add_to_cart, 1), 2)])
            total_sessions += sessions
            total_orders += orders

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())
    return {
        "total_sessions": total_sessions,
        "total_orders": total_orders,
        "overall_conv_rate_pct": round(100.0 * total_orders / max(total_sessions, 1), 2),
    }


def gen_inventory_turnover_calc(path: Path) -> dict:
    """
    库存周转计算表（LinkMart 大促期）。
    使用 JD 口径：×360，5 季度平均库存。
    参考 JD Q4 2024 = 31.5 天，设计 LinkMart 为 32.4 天（合理区间 28-35）。
    """
    rng = random.Random(618_005)
    # 5 季度库存余额（百万元）
    quarterly_inventory = [round(rng.uniform(850, 1050), 2) for _ in range(5)]
    avg_inv_5q = round(sum(quarterly_inventory) / 5, 2)
    # TTM COGS（百万元）—— 反推：inv_days = avg_inv_5q / ttm_cogs * 360 ≈ 32.4
    target_inv_days = 32.4
    ttm_cogs = round(avg_inv_5q / target_inv_days * 360, 2)
    actual_inv_days = round(avg_inv_5q / ttm_cogs * 360, 1)

    rows = [["quarter", "inventory_balance_rmb_million"]]
    q_labels = ["Q4-2023", "Q1-2024", "Q2-2024", "Q3-2024", "Q4-2024"]
    for q, v in zip(q_labels, quarterly_inventory):
        rows.append([q, v])
    rows.append(["avg_5q", avg_inv_5q])
    rows.append(["ttm_cogs", ttm_cogs])
    rows.append(["inventory_days_jd_formula", actual_inv_days])
    rows.append(["multiplier_used", 360])
    rows.append(["formula", "(avg_inventory_5q / ttm_cogs) * 360"])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())
    return {
        "quarterly_inventory": quarterly_inventory,
        "avg_inventory_5q": avg_inv_5q,
        "ttm_cogs": ttm_cogs,
        "inventory_days": actual_inv_days,
        "multiplier": 360,
    }


def gen_category_summary_draft(path: Path) -> None:
    """
    V6 红鲱鱼：分品类汇总草稿，使用 v1 Method 1 口径数据，数值已过时。
    标注为草稿，明确说明基于 v1 数据。
    """
    wj(path, {
        "_warning": "DRAFT ONLY — based on v1 data (Method 1 calibration). DO NOT USE for final reporting.",
        "_status": "superseded_by_v2",
        "report_version": "draft_v1",
        "data_source": "gmv_daily_618_v1.csv",
        "note": "This summary uses v1 data which contains Method 1 GMV calibration error for 2025-05-13 to 2025-05-22. Use v2 data for all final computations.",
        "categories": {
            "apparel": {"gmv_rmb_million": 21340.5, "return_rate_pct": 27.8, "data_quality": "method1_contaminated"},
            "electronics": {"gmv_rmb_million": 38920.1, "return_rate_pct": 10.2, "data_quality": "method1_contaminated"},
            "beauty": {"gmv_rmb_million": 13950.2, "return_rate_pct": 6.8, "data_quality": "method1_contaminated"},
            "home": {"gmv_rmb_million": 9640.8, "return_rate_pct": 17.1, "data_quality": "method1_contaminated"},
            "food": {"gmv_rmb_million": 4310.4, "return_rate_pct": 2.1, "data_quality": "method1_contaminated"},
        }
    })


# ─────────────────────────────────────────────────────────────────────────────
# 5. 脚本工具（workspace scripts）
# ─────────────────────────────────────────────────────────────────────────────
def gen_workspace_scripts(inv_stats: dict) -> None:
    # calc_gmv.py —— GMV 闭合校验（v1 会 FAIL，v2 会 PASS）
    w(WS / "scripts" / "calc_gmv.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
GMV 闭合校验脚本。
用法：python scripts/calc_gmv.py <gmv_csv_path>
验证：GMV = orders × AOV（每行闭合，容差 0.5%）。
v1 数据含 Method 1 口径污染，预期输出 status=FAIL。
\"\"\"
import csv
import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: calc_gmv.py <gmv_csv_path>"); sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({{"status": "ERROR", "message": "file not found: " + str(path)}}))
        sys.exit(1)

    failures = []
    method1_rows = []
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                orders = int(row["orders"])
                aov = float(row["aov"])
                gmv = float(row["gmv_rmb_million"]) * 1_000_000
                computed = orders * aov
                delta_pct = abs(computed - gmv) / max(gmv, 1) * 100
                if delta_pct > 0.5:
                    failures.append({{
                        "date": row.get("date"), "category": row.get("category"),
                        "channel": row.get("channel"), "delta_pct": round(delta_pct, 4)
                    }})
                if row.get("gmv_method") == "method1":
                    method1_rows.append(row.get("date"))
            except (ValueError, KeyError):
                pass

    method1_dates = sorted(set(method1_rows))
    status = "FAIL" if method1_rows else "PASS"
    result = {{
        "status": status,
        "method1_row_count": len(method1_rows),
        "method1_dates": method1_dates[:10],  # first 10
        "delta_pct": round(sum(f["delta_pct"] for f in failures) / max(len(failures), 1), 4),
        "affected_date_range": {{
            "start": method1_dates[0] if method1_dates else None,
            "end": method1_dates[-1] if method1_dates else None
        }} if method1_dates else None,
        "total_rows_checked": sum(1 for _ in csv.DictReader(open(path, encoding="utf-8")))
    }}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
""")

    # calc_inventory_days.py —— 库存天数计算（JD 口径 ×360）
    w(WS / "scripts" / "calc_inventory_days.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
库存周转天数计算（JD 官方口径：×360，5 季度平均库存）。
用法：python scripts/calc_inventory_days.py <inventory_calc_csv>
输出：inventory_days, formula_used, multiplier
\"\"\"
import csv
import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: calc_inventory_days.py <calc_csv>"); sys.exit(1)
    path = Path(sys.argv[1])
    data = {{}}
    with open(path, encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2:
                data[row[0]] = row[1]

    avg_inv = float(data.get("avg_5q", 0))
    ttm_cogs = float(data.get("ttm_cogs", 1))
    inv_days = round(avg_inv / ttm_cogs * 360, 1)

    result = {{
        "inventory_days": inv_days,
        "formula_used": "(avg_inventory_5q / ttm_cogs) * 360",
        "multiplier": 360,
        "quarters_used": "5 quarters",
        "avg_inventory_5q": avg_inv,
        "ttm_cogs": ttm_cogs,
        "source": "JD.com Full Year 2024 Results formula",
        "source_url": "https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html"
    }}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
""")

    # validate_metrics.py —— 指标一致性校验 + SHA-256 签名
    w(WS / "scripts" / "validate_metrics.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
指标一致性校验工具。
用法：python scripts/validate_metrics.py <workspace_path>
输出：VERIFIED:<sha256_of_kpi_dashboard.json>（写入 output/verification_token.txt）
\"\"\"
import hashlib
import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: validate_metrics.py <workspace>"); sys.exit(1)
    ws = Path(sys.argv[1])
    kpi_path = ws / "output" / "kpi_dashboard.json"
    if not kpi_path.exists():
        print("ERROR: output/kpi_dashboard.json not found"); sys.exit(1)

    digest = hashlib.sha256(kpi_path.read_bytes()).hexdigest()
    token = f"VERIFIED:{digest}"

    out_path = ws / "output" / "verification_token.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(token + "\\n", encoding="utf-8")
    print(f"Written: {out_path}")
    print(token)

if __name__ == "__main__":
    main()
""")


# ─────────────────────────────────────────────────────────────────────────────
# 6. 报告文档
# ─────────────────────────────────────────────────────────────────────────────
def gen_reports(gmv_stats: dict) -> None:
    # 初稿报告（v1 数据，含待修正问题）
    v1_total = gmv_stats.get("total_gmv_v1_rmb_million", 85000.0)
    w(WS / "reports" / "618_preliminary_report_v1.md", f"""# 618 大促初步复盘报告 v1（数据待修正）

**生成时间**：2025-06-20
**数据来源**：`data/raw/gmv_daily_618_v1.csv`（Method 1 口径，存在数据质量问题）
**状态**：草稿 — 待 v2 数据修正后更新

---

## ⚠️ 数据质量警告

本报告基于 v1 原始数据。已知 **2025-05-13 至 2025-05-22** 期间的 GMV 数据
使用了 Method 1 口径（错误），导致该区间 GMV 虚高约 6-7%。

Discord DM（Liu Yang）于 2025-06-19 发现此问题并上报。v2 数据修正进行中。

---

## GMV 汇总（v1 初稿，含 bug）

- 618 总 GMV（v1，含 Method 1 污染）：RMB **{round(v1_total, 1):,.1f} 百万元**
- **注意**：此数字偏高，v2 修正后预计下调约 6%

## 平台份额（v1 初稿）

| 平台 | 份额 |
|------|------|
| Tmall | ~50% |
| JD | ~19.3% |
| 内容平台（Douyin+Kuaishou） | >22% |

## 库存周转（初步，待财务确认）

使用 JD 官方库存天数公式（×360，5 季度平均）：
- 当前库存周转天数：待计算
- 参考基准：JD Q4 2024 = 31.5 天

---

*本报告为初稿，最终数据以 v2 版本为准。*
""")

    # 最终报告模板
    w(WS / "reports" / "templates" / "final_report_template.md", """# 618 大促全周期复盘报告（最终版）

**版本**：{{data_version}}
**生成时间**：{{generated_at}}
**审核人**：{{reviewer}}

---

## 数据来源

（请在此列出所有数据来源文件及版本，包括 source_url）

## 口径说明

（请在此说明 GMV 口径选择、库存天数公式、退货率基准版本等）

## 异常标记

（请在此列出所有异常指标，使用 `flagged: true` 的标记项，包括 Update 2 后的修订）

---

## GMV 闭合

（GMV = transactions × AOV；版本：{{data_version}}）

## 库存周转

（JD 口径：× 360；5 季度平均；LinkMart 618 实际值）

## 退货率分析

（各品类退货率 vs. 修订后基准）

## 转化漏斗

（加购率 → 结算率 → 最终转化率）

---

*报告依据 LinkMart 内部指标口径手册 v2.1 生成。*
""")


# ─────────────────────────────────────────────────────────────────────────────
# 7. V5 蜜罐诱饵：失真自动摘要报告
# ─────────────────────────────────────────────────────────────────────────────
def gen_honeypot_summary() -> None:
    """
    V5 诱饵：邮件附件中的 bot 自动摘要报告。
    失真点：声称 618 GMV 同比增长率为 22.5%（真实为 15.2%）。
    真实值在 data/reference/industry_benchmarks.json 中可查。
    """
    w(WS / "data" / "processed" / "email_bot_summary_618.md", """# 618 大促自动摘要报告（BOT AUTO-GENERATED）

> ⚠️ **自动生成摘要** — 仅供快速浏览，数据非权威，误差已知。
> 请以 `data/reference/industry_benchmarks.json` 中的数值为准。

---

## 关键指标摘要（AUTO SUMMARY — NOT AUTHORITATIVE）

| 指标 | 自动摘要值 | 说明 |
|------|-----------|------|
| 618 全平台 GMV 总额 | RMB 8,556 亿 | 来自 Syntun 监测 |
| **GMV 同比增速** | **22.5%** | ⚠️ **此数字已知偏差，真实值见参考文件** |
| Tmall 份额 | ~48% | ⚠️ 未对齐最新 Syntun 口径 |
| JD 份额 | ~21% | ⚠️ 估算，非 Daxue Consulting 官方值 |
| 电商在线退货率 | 17.5% | ⚠️ 引用了旧版 NRF 2024 数据，非 2025 值 |

---

## 系统备注

本摘要由启发式聚合机器人生成，存在以下已知问题：
- GMV 增速基于历史趋势外推，**可能偏高**（实际应与 Daxue Consulting 一次数据核对）
- 平台份额估算基于上季度数据，未反映本期变化
- 退货率引用了 2024 年 NRF 报告，**非 2025 最新值**

**请始终以 `data/reference/industry_benchmarks.json` 和原始数据文件为最终权威。**

---

*Generated by LinkMart DataBot v0.3.1 | 2025-06-21 02:31:00 UTC*
""")


# ─────────────────────────────────────────────────────────────────────────────
# 8. Sessions（主 + 4 history channels）
# ─────────────────────────────────────────────────────────────────────────────
def gen_sessions(gmv_stats: dict, inv_stats: dict, traffic_stats: dict) -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("data_team_slack", TID)
    s_feishu = gen_session_id("pm_zhang_feishu", TID)
    s_email = gen_session_id("finance_wang_email", TID)
    s_discord = gen_session_id("analyst_liu_discord", TID)

    # ── 主 session ────────────────────────────────────────────────────────
    sb = SessionBuilder(main_id, CWD, "2026-03-15T01:00:00", is_main=True)
    sb.add_user(
        "You are LinkMart Data Analyst AI, supporting Li Wei (Head of Data Analytics) "
        "on the 618 shopping festival full-cycle post-promotion analysis.\n\n"
        "The authoritative metric definitions and reference anchors are in "
        "`context/metric_definitions.md` and `data/reference/`. Auto-generated summaries "
        "(e.g. `data/processed/email_bot_summary_618.md`) are NOT authoritative — always "
        "verify numbers against primary reference files.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: every structured JSON output must include `source_url` (or `source`) "
        "AND `generated_at` (ISO 8601 timestamp) fields at the top level.\n"
        "- P2: conflict and anomaly flags must include `from` field identifying the session source.\n"
        "- P3: anomalous categories must be marked with `\"flagged\": true`, not just described in text.\n"
        "- P4: numeric fields use 1 decimal place for inventory-level metrics (e.g. 31.5 days) "
        "and 2 decimal places for percentages (e.g. 19.30%), no mixing.\n"
        "- P5: final Markdown report must include three fixed H2 sections: "
        "\"## 数据来源\", \"## 口径说明\", \"## 异常标记\".\n\n"
        "History sessions available: Slack #data-team, Feishu PM DM, Email finance review, "
        "Discord analyst DM. Start by reading SOUL.md and awaiting each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Treat context/metric_definitions.md and data/reference/ as authoritative; "
        "treat auto-generated bot summaries as non-authoritative convenience files.\n"
        "2. Apply house preferences P1-P5 throughout without re-prompting.\n"
        "3. Use v2 data (gmv_daily_618_v2.csv) for all final computations; v1 data "
        "contains a Method 1 calibration error in 2025-05-13 to 2025-05-22.\n"
        "4. Maintain cross-round numerical consistency — once a value is computed, "
        "all subsequent rounds must reference the same value.\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # ── Slack #data-team ──────────────────────────────────────────────────
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-10T02:00:00",
        [
            ("[Slack #data-team chen_hao Mon Mar 10 09:00 CST 2026] Hey team, I've been looking "
             "at the 618 GMV data and there's a calibration issue. The v1 data file "
             "(gmv_daily_618_v1.csv) uses Method 1 GMV calibration for the period 2025-05-13 "
             "to 2025-05-22. That means those 10 days have GMV overstated by roughly 6-7%. "
             "We need to switch to Method 2 for the official report.",
             "Confirmed: the v1 GMV data for 2025-05-13 through 2025-05-22 uses Method 1 "
             "calibration (excludes only >RMB 2,000 unfulfilled orders). Official reporting "
             "requires Method 2 (also excludes >RMB 100k + daily spend >RMB 1M + platform "
             "subsidies). I'll flag this in the data quality report and use v2 when available."),
            ("[Slack #data-team li_wei Mon Mar 10 09:15 CST 2026] Also, there's been a debate "
             "about whether platform subsidies count toward GMV. Can someone clarify?",
             "Per context/metric_definitions.md section 1: GMV is computed BEFORE deducting "
             "subsidies per the standard definition (Wall Street Prep), BUT LinkMart's internal "
             "Method 2 calibration explicitly excludes platform subsidies from GMV to align with "
             "the official JD reporting standard. So the answer depends on which calibration you're "
             "using: the standard GMV formula does not exclude subsidies, but Method 2 does."),
            ("[Slack #data-team chen_hao Mon Mar 10 09:30 CST 2026] And one more thing: "
             "I see the preliminary report draft uses ×365 for inventory days calculation. "
             "That's wrong. Our JD-aligned formula uses ×360 specifically (see metric_definitions.md "
             "section 3). The ×365 formula is from the generic Onramp Funds benchmark.",
             "Confirmed: LinkMart uses the JD official formula with multiplier ×360 (not ×365). "
             "The ×365 figure appears only in the legacy report and generic industry references — "
             "not applicable to our official KPI computation. I'll ensure all inventory day "
             "calculations use (avg_inventory_5q / ttm_cogs) × 360."),
        ]
    )

    # ── Feishu PM DM ──────────────────────────────────────────────────────
    v1_total = gmv_stats.get("total_gmv_v1_rmb_million", 85000.0)
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-11T02:00:00",
        [
            ("[Feishu zhang_fang Tue Mar 11 10:00 CST 2026] Hi, for the inventory days calculation, "
             "please make sure to use the JD official formula: 5-quarter average inventory divided "
             "by TTM COGS, multiplied by 360 (not 365). This is our standard. Reference: JD Q4 2024 "
             "actual = 31.5 days using this formula.",
             "Noted. Inventory days formula confirmed as (avg_inventory_5q / ttm_cogs) × 360, "
             "with 5-quarter average for the numerator and TTM COGS for the denominator. "
             "JD Q4 2024 reference value = 31.5 days. I will apply this consistently."),
            ("[Feishu zhang_fang Tue Mar 11 10:10 CST 2026] Also, I shared an old analysis in the "
             "shared drive: `data/processed/legacy_report_v0.md` — but IGNORE that file, it uses "
             "the wrong ×365 formula and pre-dates our Method 2 adoption. It's there for archive "
             "reference only and should NOT be cited in the current analysis.",
             "Understood. The file `data/processed/legacy_report_v0.md` uses the deprecated ×365 "
             "formula and Method 1 calibration. I will treat it as a red herring / archived document "
             "and will not cite its numbers in any deliverable."),
            ("[Feishu zhang_fang Tue Mar 11 10:25 CST 2026] One more thing: for the channel GMV "
             "breakdown, our current reporting combines Douyin and Kuaishou as 'content_platforms'. "
             "That's the structure we use for this first round of reporting.",
             "Noted. For the initial channel GMV report, Douyin and Kuaishou will be combined as "
             "'content_platforms' in the JSON output. I'll flag this as the initial aggregation "
             "rule, subject to potential update."),
        ]
    )

    # ── Email finance review ──────────────────────────────────────────────
    conv_pct = traffic_stats.get("overall_conv_rate_pct", 2.31)
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-03-12T02:00:00",
        [
            ("[Email wang_mei@linkmart.com → analytics_team@linkmart.com Wed Mar 12 14:00 CST 2026] "
             "Subject: 618 GMV Audit Formulas — OFFICIAL\n\n"
             "Team,\n\nFor the 618 post-promotion audit, please use the following formulas (official):\n\n"
             "1. GMV = transactions × AOV (Wall Street Prep standard)\n"
             "2. Take Rate = commission / GMV (Marketplace Net Revenue = GMV × Take Rate)\n"
             "3. Inventory Days = (avg_inventory_5q / ttm_cogs) × 360 (JD official formula)\n"
             "4. Return Rate = returns / orders × 100\n"
             "5. Conversion Rate = (orders / sessions) × 100\n\n"
             "The auto-generated bot summary (email_bot_summary_618.md) has a known error: "
             "it reports GMV YoY growth as 22.5%, but the actual Syntun/Daxue 2025 figure "
             "is 15.2%. Please use 15.2% in all reports.\n\n"
             "Wang Mei, Finance Analyst",
             "Confirmed. Finance audit formulas recorded:\n"
             "1. GMV = transactions × AOV\n"
             "2. Take Rate = commission / GMV\n"
             "3. Inventory Days = (avg_inventory_5q / ttm_cogs) × 360\n"
             "4. Return Rate = returns / orders × 100\n"
             "5. Conversion Rate = (orders / sessions) × 100\n\n"
             "Also confirmed: the bot summary's 22.5% GMV growth figure is incorrect. "
             "The authoritative value from Syntun/Daxue Consulting 2025 is 15.2%. "
             "I will use 15.2% in all deliverables and flag the bot summary as a honeypot."),
            ("[Email wang_mei@linkmart.com → analytics_team@linkmart.com Wed Mar 12 14:30 CST 2026] "
             "Also: please confirm the NRF 2025 online return rate benchmark. I've seen a reference "
             "to 17.5% in the bot summary, but I believe the correct 2025 value is different.",
             "Confirmed: the correct NRF 2025 online return rate benchmark is **19.3%** "
             "(per NRF × Happy Returns 2025 report: https://nrf.com/research/2025-retail-returns-landscape). "
             "The bot summary's 17.5% is an error — it appears to reference the 2024 figure. "
             "I will use 19.3% as the authoritative benchmark in all return rate analyses."),
        ]
    )

    # ── Discord analyst DM ────────────────────────────────────────────────
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-03-13T02:00:00",
        [
            ("[Discord liu_yang DM Thu Mar 13 16:00 CST 2026] Hey, I looked at the v1 GMV data "
             "more carefully. The dates 2025-05-13 through 2025-05-22 are definitely using "
             "Method 1 calibration — I can see the `gmv_method` column says 'method1' for those "
             "rows. The rest of the file is Method 2. So the bug is specifically those 10 days.",
             "Confirmed: I can verify from the data that rows for 2025-05-13 to 2025-05-22 "
             "have gmv_method='method1' while all other dates use 'method2'. This means the "
             "specific contaminated date range is 2025-05-13 through 2025-05-22, which includes "
             "at minimum the dates: 2025-05-13, 2025-05-14, 2025-05-15, 2025-05-16, 2025-05-17, "
             "2025-05-18, 2025-05-19, 2025-05-20, 2025-05-21, 2025-05-22."),
            ("[Discord liu_yang DM Thu Mar 13 16:20 CST 2026] Also, I noticed the auto-summary "
             "report (email_bot_summary_618.md) says the YoY growth was 22.5%. But when I check "
             "the actual Daxue Consulting 618 2025 data, the number is 15.2%. The bot is "
             "significantly off. Just flagging this so you don't accidentally cite it.",
             "Thank you for the flag. The bot summary's 22.5% GMV YoY growth figure is a known "
             "error (honeypot). The authoritative Syntun/Daxue Consulting 618 2025 data shows "
             "15.2% YoY growth. I will flag the bot summary as non-authoritative and use 15.2% "
             "in all deliverables. The wrong_metric in question is gmv_growth_rate."),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_feishu, "feishu"),
            (s_email, "email"),
            (s_discord, "discord"),
        ],
    }


def _gen_v1v2_reconciliation_csv(path: Path, gmv_stats: dict) -> None:
    """
    生成 v1 vs v2 逐行（日期×品类×渠道）差异对比 CSV。
    bug 日期行有差异，其他行相同。约 8k tokens。
    """
    dates = gen_dates_range(PROMO_START, PROMO_END)
    bug_dates_set = set(V1_BUG_DATES)
    cat_base = {
        "apparel": 320.0, "electronics": 580.0, "beauty": 210.0, "home": 145.0, "food": 65.0
    }
    channels = ["tmall", "jd", "douyin", "kuaishou"]
    chan_share = {"tmall": 0.50, "jd": 0.193, "douyin": 0.18, "kuaishou": 0.042}

    rows = [["date", "category", "channel", "gmv_v1_rmb_million", "gmv_v2_rmb_million",
             "delta_rmb_million", "delta_pct", "is_bug_date", "v1_method", "v2_method"]]

    rng = random.Random(618_001)
    for d in dates:
        is_bug = d in bug_dates_set
        dt = datetime.strptime(d, "%Y-%m-%d")
        if dt.month == 6 and dt.day in range(1, 4):
            day_mult = rng.uniform(2.5, 3.2)
        elif dt.month == 6 and dt.day in range(13, 19):
            day_mult = rng.uniform(3.0, 4.5)
        else:
            day_mult = rng.uniform(0.6, 1.2)

        for cat in CATEGORIES:
            for chan in channels:
                base_gmv = cat_base[cat] * chan_share[chan] * day_mult
                if is_bug:
                    gmv_v1 = round(base_gmv * 1.32, 3)
                    gmv_v2 = round(base_gmv * 0.985, 3)
                    v1_method = "method1"
                else:
                    gmv_v1 = round(base_gmv * 0.985, 3)
                    gmv_v2 = round(base_gmv * 0.985, 3)
                    v1_method = "method2"
                delta = round(gmv_v2 - gmv_v1, 3)
                delta_pct_row = round(100.0 * delta / max(gmv_v1, 0.001), 2)
                rows.append([d, cat, chan,
                             gmv_v1, gmv_v2, delta, delta_pct_row,
                             "yes" if is_bug else "no",
                             v1_method, "method2"])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


# ─────────────────────────────────────────────────────────────────────────────
# 9. Updates（Update 1 + Update 2 含 supersede）
# ─────────────────────────────────────────────────────────────────────────────
def gen_updates(sess_ids: dict, gmv_stats: dict) -> dict:
    s_feishu = sess_ids["history"][1][0]

    # ── UPDATE 1（Q8 后）────────────────────────────────────────────────────
    # 1a. 注入 pm_correction_note.md
    v2_total = gmv_stats.get("total_gmv_v2_rmb_million", 79600.0)
    v1_total = gmv_stats.get("total_gmv_v1_rmb_million", 85000.0)
    delta_pct = gmv_stats.get("delta_pct", -6.2)
    w(UPD / "upd1_workspace" / "pm_correction_note.md", f"""# PM 数据修正说明（Update 1）

**发送方**：Zhang Fang（产品经理）
**日期**：2025-06-25
**主题**：618 GMV 数据修正 — v2 口径切换

---

## 修正内容

v2 GMV 数据文件（`gmv_daily_618_v2.csv`）已经更新，包含以下修正：

1. **全部切换至 Method 2 口径**：排除买家日消费 > RMB 1,000,000 的交易及 > RMB 100,000 未履单订单
2. **排除平台补贴金额**：平台优惠券、活动红包不计入 GMV
3. **数据完整性**：所有 37 天数据均已重新计算

## v2 vs v1 对比

| 指标 | v1 数据 | v2 数据 | 差异 |
|------|--------|--------|------|
| 618 总 GMV（百万元） | {round(v1_total, 1):,.1f} | {round(v2_total, 1):,.1f} | {round(delta_pct, 1)}% |
| 口径 | Method 1（2025-05-13~05-22 期间） | Method 2（全期） | — |
| 平台补贴 | 已计入 | 已排除 | — |

**结论**：v2 总 GMV 比 v1 低约 **{abs(round(delta_pct, 1))}%**，主要来自方法论修正和补贴排除。

## 渠道合并规则（当前标准）

- Tmall、JD、Douyin、Kuaishou 按渠道分别报告
- **content_platforms 合并口径**：Douyin + Kuaishou 合并计入 `content_platforms` 合计字段
- 要求 `content_platforms_share_pct > 22%`（Daxue Consulting 618 2025 基准）

---

*后续分析须使用 v2 数据。v1 数据仅作为历史参考。*
""")

    # 1b. 注入 gmv_daily_618_v2.csv（直接复制生成的文件）
    # 已在 gen_gmv_daily_v2 生成于 WS/data/raw/gmv_daily_618_v2.csv
    # 在 updates 目录做副本
    v2_src = WS / "data" / "raw" / "gmv_daily_618_v2.csv"
    v2_dst = UPD / "upd1_workspace" / "gmv_daily_618_v2.csv"
    v2_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(v2_src, v2_dst)

    # 1c-extra. v1_v2_reconciliation_detail.csv（v1 vs v2 按日期品类渠道逐行对比，约 8k tokens）
    _gen_v1v2_reconciliation_csv(UPD / "upd1_workspace" / "v1_v2_reconciliation_detail.csv",
                                  gmv_stats)

    # 1d. update_slack_thread.md
    w(UPD / "upd1_workspace" / "update_slack_thread.md", f"""# Slack 线程：v2 数据更新讨论（后续片段）

**频道**：#data-team
**时间**：2025-06-25

---

**chen_hao**（2025-06-25 11:00）：
v2 数据已经推送了。我跑了一下对比，v2 总 GMV 比 v1 低了 {abs(round(delta_pct, 1))}%，
符合预期。主要差异在 5/13-5/22 那段。

**li_wei**（2025-06-25 11:05）：
好的，Q9 之后所有计算都要切换到 v2。v1 的结果只能作为历史记录，不得用于最终报告。

**chen_hao**（2025-06-25 11:10）：
注意：v2 里 `reason` 字段的值要同时包含 "Method 2" 和 "subsidy excluded"，
这样财务团队才能追溯修正原因。

""")

    # ── UPDATE 2（Q11 后，含 supersede）─────────────────────────────────────
    # 2a. finance_audit_memo.md（关键 supersede 文件）
    w(UPD / "upd2_workspace" / "finance_audit_memo.md", """# 财务审计备忘录（Update 2）

**发送方**：Wang Mei（财务分析师）
**日期**：2025-06-30
**主题**：Douyin 渠道口径修正 + 中国平台退货率基准修订

---

## ⚠️ 重要：撤销先前渠道合并规则

经财务审计团队核查，Syntun 的 Douyin GMV 监测口径与平台自报口径存在差异。

**即日起，以下规则生效，并 SUPERSEDE（撤销）Update 1（`pm_correction_note.md`）
中关于渠道合并方式的规定（§ channel_aggregation）**：

> **Douyin GMV 须单独列出为独立字段（`douyin_gmv`），不得计入 `content_platforms` 合计。**
> Kuaishou 可继续计入 `content_platforms`，但 Douyin 必须独立呈现。

**撤销前规则（来自 `pm_correction_note.md § channel_aggregation`）**：
- 原规则：Douyin + Kuaishou 合并为 `content_platforms`，要求 `content_platforms_share_pct > 22%`

**新规则**：
- `douyin_gmv`：Douyin 独立字段（单位：百万元）
- `kuaishou_gmv`：Kuaishou 独立字段（或计入 `content_platforms`）
- **`content_platforms` 字段不应包含 Douyin GMV**

## 中国平台退货率基准修订

经中国市场数据对比，美国 NRF 基准不适用于中国平台电子产品退货率评估。

**修订内容**：

| 品类 | 原基准（NRF/Richpanel 美国） | 修订后基准（中国平台） | 来源 |
|------|--------------------------|---------------------|------|
| 电子产品 | 8%–15% | **15%–25%** | Richpanel 中国极端值参考 |

> 注：服装品类基准（20%–40%）与美国基准一致，无需修订。

**修订文件**：见附件 `revised_category_benchmarks.json`。

---

*本备忘录的渠道合并规则修改须在 Q12 及后续所有报告中执行。*
""")

    # 2b-extra. channel_reconciliation_detailed.md（用于 Update 2 体量扩充）
    w(UPD / "upd2_workspace" / "channel_reconciliation_detailed.md", f"""# 渠道 GMV 口径重新核算备忘（Update 2 附件）

**制作人**：Wang Mei（财务审计）
**日期**：2025-06-30
**适用**：618 2025 大促全周期渠道 GMV 重新分类

---

## 背景

经对 Syntun 监测数据的深入分析，Douyin 渠道 GMV 统计体系与其他平台存在根本差异：

1. **Syntun 定义**：Douyin 的 GMV 包含直播带货实际成交 + 短视频橱窗购买 + 商品搜索购买
2. **平台自报**：Douyin 自报 GMV 不包含退款/退货后的净 GMV
3. **口径差异约 8-12%**（Syntun 高于平台自报）

因此，在与 JD、Tmall 等平台 GMV 对比时，**Douyin 须单独列出**以便口径标注，
不得简单合并入 `content_platforms`。

---

## 重新分类规则（即时生效）

| 平台 | 旧分类 | 新分类 |
|------|-------|-------|
| Tmall | `tmall` | `tmall`（不变） |
| JD | `jd` | `jd`（不变） |
| Douyin | `content_platforms` | **`douyin_gmv`（独立字段）** |
| Kuaishou | `content_platforms` | `content_platforms`（可保留） |

**`content_platforms` 字段在 Update 2 后含义变为「Kuaishou 及其他内容平台（不含 Douyin）」。**

---

## 618 2025 平台 GMV 分布（修订口径，v2 数据）

基于 Daxue Consulting 618 2025 数据（来源：https://daxueconsulting.com/618-2025-results/），
以 LinkMart 内部 Method 2 口径重新分配：

| 平台 | 份额 | 说明 |
|------|------|------|
| Tmall | ~50% | Marketplace 模式，含补贴后净 GMV |
| JD | ~19.3% | 直营为主，JD Method 2 口径 |
| **Douyin** | **~16-18%** | **独立列出（原包含在 >22% 合计中）** |
| Kuaishou 及其他 | ~4-6% | content_platforms 余量 |

> 注：Douyin + Kuaishou 合计仍 > 22%，但 Douyin 须在 JSON 输出中独立呈现。

---

## 数值校验参考

按照 Daxue Consulting 618 2025 数据（来源已核实）：
- 618 总 GMV：RMB 8,556 亿，同比 +15.2%
- Tmall：~50%（≈ RMB 4,278 亿）
- JD：~19.3%（≈ RMB 1,651 亿）
- Douyin+Kuaishou 合计：>22%（≈ RMB 1,882+ 亿）

其中 Douyin 约 16-18%，Kuaishou 约 4-6%。

---

## 重要提示：supersede 声明

本文件与 `finance_audit_memo.md` 共同构成 Update 2，正式撤销 Update 1 中的以下规定：

> 来自 `pm_correction_note.md § channel_aggregation`：
> "content_platforms 合并口径：Douyin + Kuaishou 合并计入 content_platforms 合计字段"

**撤销后**，agent 须在所有后续 JSON 报告中使用 `douyin_gmv` 独立字段，
并在 `superseded_rule` 字段中注明 `"pm_correction_note.md § channel_aggregation"`。

---

## 附：Syntun 监测口径说明

Syntun（星图数据）是中国主要的第三方电商监测机构，覆盖：
- 阿里系（Taobao、Tmall、天猫超市）
- 京东系（JD、京东超市）
- 抖音电商（Douyin Commerce）
- 快手电商（Kuaishou Commerce）
- 拼多多（Pinduoduo，部分覆盖）

Syntun 数据为「全平台监测」口径，与各平台自报 GMV 存在 5-15% 差异（Syntun 通常高于自报）。
本场景所有 GMV 数值均以 Syntun 监测口径为基础，配合 Method 2 校准。

来源：https://daxueconsulting.com/618-2025-results/

""")

    # 2c. revised_category_benchmarks.json
    wj(UPD / "upd2_workspace" / "revised_category_benchmarks.json", {
        "source": "Finance Audit Memo — China Platform Revised Benchmarks",
        "generated_at": "2025-06-30T00:00:00Z",
        "effective_from": "2025-06-30",
        "note": "Supersedes NRF/Richpanel US benchmarks for electronics category in China platform context",
        "return_rate_benchmarks": {
            "electronics": {
                "low": 15.0,
                "high": 25.0,
                "unit": "pct",
                "benchmark_source": "China platform (revised)",
                "previous_low": 8.0,
                "previous_high": 15.0,
                "previous_source": "Richpanel global (US-centric)"
            },
            "apparel": {
                "low": 20.0,
                "high": 40.0,
                "unit": "pct",
                "benchmark_source": "China platform (aligned with global)",
                "note": "No change from US benchmark"
            }
        }
    })

    # 2c. legacy_report_v0.md（V6 红鲱鱼：旧版报告，×365 错误公式）
    w(UPD / "upd2_workspace" / "legacy_report_v0.md", """# 618 大促库存分析旧版报告（ARCHIVE — 已废弃）

**状态**：ARCHIVED — DO NOT CITE
**版本**：v0（2025 年 4 月草稿，大促开始前）
**废弃原因**：使用了错误的库存周转公式（×365）和 Method 1 口径

---

## ⚠️ 废弃声明

本报告使用了以下错误方法，已被正式废弃：

1. **库存周转公式错误**：本报告使用 `inventory_days = (avg_inventory / ttm_cogs) × 365`，
   而 LinkMart 官方采用的 JD 口径公式为 `× 360` + 5 季度平均库存。

2. **GMV 口径错误**：本报告使用 Method 1 口径估算，不包含 LinkMart 的补贴排除规则。

---

## 旧版数据（错误，仅存档）

### 库存周转（旧版，错误公式 ×365）

```
库存周转天数（旧版）= (avg_inventory_1q / ttm_cogs) × 365 = 约 33 天
```

注：此处使用单季度平均（而非 5 季度），且乘数为 365，**均与现行 JD 口径不符**。

### v0 GMV 汇总（错误，仅存档）

| 渠道 | GMV 估算（百万元） | 说明 |
|------|-----------------|------|
| Tmall | ~45,000 | Method 1 口径 |
| JD | ~18,000 | Method 1 口径 |
| 内容平台 | ~19,000 | 不含补贴排除 |

---

*本报告已被 v2 数据和 metric_definitions.md v2.1 取代。引用本文件数据属于错误。*
""")

    updates_decl = {
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "pm_correction_note.md", "action": "new",
                 "target": "data/updates/pm_correction_note.md"},
                {"name": "gmv_daily_618_v2.csv", "action": "new",
                 "target": "data/raw/gmv_daily_618_v2.csv"},
                {"name": "v1_v2_reconciliation_detail.csv", "action": "new",
                 "target": "data/processed/v1_v2_reconciliation_detail.csv"},
                {"name": "update_slack_thread.md", "action": "new",
                 "target": "data/updates/update_slack_thread.md"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "finance_audit_memo.md", "action": "new",
                 "target": "data/updates/finance_audit_memo.md"},
                {"name": "revised_category_benchmarks.json", "action": "new",
                 "target": "data/reference/revised_category_benchmarks.json"},
                {"name": "legacy_report_v0.md", "action": "new",
                 "target": "data/processed/legacy_report_v0.md"},
                {"name": "channel_reconciliation_detailed.md", "action": "new",
                 "target": "data/updates/channel_reconciliation_detailed.md"},
            ],
        },
    }
    return updates_decl


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_context_docs()
    gen_reference_data()

    # 生成 CSV 数据
    v1_stats = gen_gmv_daily_v1(WS / "data" / "raw" / "gmv_daily_618_v1.csv")
    v2_stats = gen_gmv_daily_v2(WS / "data" / "raw" / "gmv_daily_618_v2.csv", v1_stats)
    gmv_stats = {**v1_stats, **v2_stats}

    gen_inventory_csv(WS / "data" / "raw" / "inventory_snapshot_t0.csv", "t0", seed=618_010)
    gen_inventory_csv(WS / "data" / "raw" / "inventory_snapshot_t1.csv", "t1", seed=618_011)
    ret_stats = gen_returns_log(WS / "data" / "raw" / "returns_log_618.csv")
    traffic_stats = gen_channel_traffic(WS / "data" / "raw" / "channel_traffic_metrics.csv")
    inv_stats = gen_inventory_turnover_calc(
        WS / "data" / "processed" / "inventory_turnover_calc.csv"
    )
    gen_category_summary_draft(WS / "data" / "processed" / "category_summary_draft.json")
    gen_workspace_scripts(inv_stats)
    gen_reports(gmv_stats)
    gen_honeypot_summary()

    sess_ids = gen_sessions(gmv_stats, inv_stats, traffic_stats)
    updates_decl = gen_updates(sess_ids, gmv_stats)

    # 注册元数据（不碰共享 manifest）
    desc = (
        "电商大促数据与库存闭合（LinkMart 618 大促复盘，18 轮全 exec_check，"
        "2 次 update 含 supersede，5 条 preference P1-P5，难度向量 V1-V10）。"
        "真实来源：JD.com 2024 年报（https://www.globenewswire.com/news-release/2025/03/06/3037984/）；"
        "Daxue Consulting 618 2025（https://daxueconsulting.com/618-2025-results/）；"
        "NRF 2025 退货率报告（https://nrf.com/research/2025-retail-returns-landscape）；"
        "Wall Street Prep GMV 公式（https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/）。"
    )
    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total_ws = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    total_upd = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    total_sess = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )

    print(f"[prd3] v1 stats: total_gmv_v1={gmv_stats['total_gmv_v1_rmb_million']:.1f}M RMB")
    print(f"[prd3] v2 stats: total_gmv_v2={gmv_stats['total_gmv_v2_rmb_million']:.1f}M RMB "
          f"(delta={gmv_stats['delta_pct']:.1f}%)")
    print(f"[prd3] inventory_days={inv_stats['inventory_days']} days (×{inv_stats['multiplier']})")
    print(f"[prd3] returns={ret_stats['total_returns']} return records")
    print(f"[prd3] traffic: {traffic_stats['total_sessions']:,} sessions, "
          f"conv_rate={traffic_stats['overall_conv_rate_pct']:.2f}%")
    print(f"[prd3] workspace tokens ~{total_ws:,}")
    print(f"[prd3] update tokens ~{total_upd:,}")
    print(f"[prd3] session tokens ~{total_sess:,}")
    print(f"[prd3] built at {DATASET}")


if __name__ == "__main__":
    main()
