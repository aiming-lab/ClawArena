# 渠道 GMV 口径重新核算备忘（Update 2 附件）

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

