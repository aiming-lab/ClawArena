# 财务审计备忘录（Update 2）

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
