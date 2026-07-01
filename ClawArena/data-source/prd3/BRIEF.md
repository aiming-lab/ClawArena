# BRIEF：prd3 — 电商大促数据与库存闭合

## 场景叙事背景

某头部电商平台（综合 Taobao/Tmall/JD.com 口径，虚构公司名「LinkMart」）的数据分析团队，正在完成一场大促（618 购物节）的全周期复盘。Agent 扮演高级数据分析师，需要在跨渠道协作环境中：整合来自多个数据源的 GMV、转化率、退货率、库存周转数据；识别各 session 与文件之间的口径冲突；按照严格的财务口径公式进行数据闭合校验；输出符合内部规范的结构化报表。

核心挑战：不同数据源对同一指标的口径存在真实差异（如阿里 vs. JD 的 GMV 排除规则不同）；大促进行中数据会更新，后续 update 会撤销或修订前期结论；agent 需要在保持数值跨轮一致性的同时，准确辨别 supersede 信息。

---

## 真实来源链接表

| # | 来源名称 | URL | 类型 |
|---|---------|-----|------|
| S1 | JD.com Q3 2024 Form 6-K (SEC) | https://www.sec.gov/Archives/edgar/data/0001549802/000119312524257928/d815449dex991.htm | official_doc |
| S2 | JD.com Full Year 2024 Results (GlobeNewswire) | https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html | official_doc |
| S3 | Alibaba FY2025 Results (BusinessWire) | https://www.businesswire.com/news/home/20250514856295/en/Alibaba-Group-Announces-March-Quarter-2025-and-Fiscal-Year-2025-Results | official_doc |
| S4 | Syntun 2025 Double 11 Report (PR Newswire) | https://www.prnewswire.com/news-releases/syntun--2025-double-11-promotion-report-the-gmv-during-china-double-11-shopping-festival-reached-1695-billion-cny-238-billion-usd-302613127.html | dataset |
| S5 | Daxue Consulting 618 2025 Results | https://daxueconsulting.com/618-2025-results/ | dataset |
| S6 | Wall Street Prep: GMV Formula & Calculator | https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/ | official_doc |
| S7 | Wall Street Prep: Take Rate Formula & Calculator | https://www.wallstreetprep.com/knowledge/take-rate/ | official_doc |
| S8 | NRF 2025 Retail Returns Landscape | https://nrf.com/research/2025-retail-returns-landscape | regulation |
| S9 | Onramp Funds: Inventory Turnover Benchmarks 2025 | https://www.onrampfunds.com/resources/inventory-turnover-benchmarks-by-industry-2025 | dataset |
| S10 | Speedwell Memos: Alibaba vs JD GMV Accounting | https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and | postmortem |
| S11 | Wikipedia: Gross merchandise volume | https://en.wikipedia.org/wiki/Gross_merchandise_volume | official_doc |
| S12 | ConvertCart: eCommerce Conversion Rate Formula | https://www.convertcart.com/blog/calculate-ecommerce-conversion-rate | official_doc |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|---|---------|------|
| GMV 基础公式 | GMV = 交易笔数 × 平均客单价（AOV） | https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/ | 亦等价于 销售单价 × 销售件数 |
| Take Rate 公式 | Take Rate (%) = 平台佣金收入 ÷ GMV | https://www.wallstreetprep.com/knowledge/take-rate/ | 产品类平台典型区间 5%–25%，均值约 15% |
| 净收入 vs GMV 关系 | 净收入 ≈ GMV × Take Rate（marketplace 模式）；直营模式净收入 = GMV – 退货 – 折扣 | https://www.wallstreetprep.com/knowledge/take-rate/ | 两种模式口径不可混用 |
| JD 库存周转天数公式 | 库存周转天数 = (过去 5 季度平均库存 ÷ 过去 12 个月零售业务成本) × 360 | https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html | TTM 口径，乘数为 360 而非 365 |
| JD 库存天数 Q4 2024 | 31.5 天（TTM） | https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html | Q4 2023 对比值为 30.3 天 |
| JD 应付账款周转天数 Q4 2024 | 58.6 天 | https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html | — |
| JD 应收账款周转天数 Q4 2024 | 5.9 天 | https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html | — |
| JD 2024 全年净收入 | RMB 1,158.8 亿（US$ 158.8 亿） | https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html | 同比增长 6.8%；产品收入 80.1%，服务收入 19.9% |
| JD GMV 口径差异 | JD Method 1（排除 2k 以上未履单）vs Method 2（排除 100k+）导致 GMV 差幅约 40% | https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and | 2016 年数据：Method 1 为 RMB 658bn，Method 2 为 RMB 939bn |
| Alibaba GMV 刷单调整估算 | 若按更严格口径排除虚假交易，Alibaba 中国零售 GMV 可能虚高约 30%（约 $330bn） | https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and | 调整后 Take Rate 约 6–9%，而非名义 4% |
| 618 2025 总 GMV | RMB 8,556 亿（约 8.6 万亿，存版本分歧：另一口径为 856 亿） | https://daxueconsulting.com/618-2025-results/ | 同比增长 15.2%；Syntun 数据 |
| 618 2025 平台份额 | Tmall 约 50%，JD 约 19.3%，Douyin 约 22%（含 Kuaishou） | https://daxueconsulting.com/618-2025-results/ | Douyin GMV 增速 15.2%，最快 |
| Double 11 2025 总 GMV | RMB 1,695 亿（约 238 亿美元），电商平台占 1,619.1 亿 | https://www.prnewswire.com/news-releases/syntun--2025-double-11-promotion-report-the-gmv-during-china-double-11-shopping-festival-reached-1695-billion-cny-238-billion-usd-302613127.html | 2025 年 10 月 7 日至 11 月 11 日 |
| 电商全渠道退货率（美国 2025） | 19.3%（在线）；整体零售 15.8% | https://nrf.com/research/2025-retail-returns-landscape | NRF × Happy Returns 联合报告 |
| 服装类退货率 | 20%–40% | https://www.richpanel.com/learn/ecommerce-return-rates | 电子产品 8%–15%，美妆 4%–12% |
| 中国平台退货率极端案例 | 免费退货后部分品类退货率从约 30% 升至约 60% | https://www.richpanel.com/learn/ecommerce-return-rates | 与美国基准明显不同 |
| 库存周转天数公式（通用） | 库存天数 = 365 ÷ 库存周转率；库存周转率 = COGS ÷ 平均库存 | https://www.onrampfunds.com/resources/inventory-turnover-benchmarks-by-industry-2025 | 电商综合基准：服装 30–60 天，电子产品 45–80 天 |
| 电商转化率公式 | 转化率 = (成交订单数 ÷ 访客总次数) × 100 | https://www.convertcart.com/blog/calculate-ecommerce-conversion-rate | 全行业均值约 1.89%–3%；Shopify 平均 1.4% |
| 加购率（Add-to-Cart Rate） | 全球均值约 6.34%–7.52% | https://www.convertcart.com/blog/calculate-ecommerce-conversion-rate | 加购后结算率约 60%–70% |

---

## Workspace 文件树与体量规划（目标 >100k tokens，约 400KB+）

```
workspace/
├── context/
│   ├── company_profile.md              # LinkMart 公司背景与大促规则说明（~8k tokens）
│   ├── metric_definitions.md           # 内部指标口径手册（GMV/转化率/退货率/库存天数）（~15k tokens）
│   ├── platform_comparison.md          # 阿里 vs JD vs Douyin 口径对照（含真实差异）（~10k tokens）
│   └── promotion_calendar_618_2025.md  # 618 大促时间轴与规则文档（~8k tokens）
├── data/
│   ├── raw/
│   │   ├── gmv_daily_618_v1.csv        # 618 每日 GMV 原始数据（50 天 × 5 品类 × 多维度）（~30k tokens）
│   │   ├── gmv_daily_618_v2.csv        # update1 后更新版（数据口径修正）（~30k tokens）
│   │   ├── inventory_snapshot_t0.csv   # 大促前库存快照（SKU 级，~15k tokens）
│   │   ├── inventory_snapshot_t1.csv   # 大促中库存快照（~15k tokens）
│   │   ├── returns_log_618.csv         # 退货记录（~12k tokens）
│   │   └── channel_traffic_metrics.csv # 渠道流量 & 转化漏斗数据（~12k tokens）
│   ├── processed/
│   │   ├── category_summary_draft.json # 分品类汇总草稿（含口径问题，作为红鲱鱼诱饵）（~8k tokens）
│   │   └── inventory_turnover_calc.xlsx.csv # 库存周转计算表（csv 格式）（~10k tokens）
│   └── reference/
│       ├── jd_fy2024_q4_metrics.json   # JD 公开财报锚点数据（~5k tokens）
│       └── industry_benchmarks.json    # 行业基准数据（NRF、Onramp Funds）（~5k tokens）
├── reports/
│   ├── 618_preliminary_report_v1.md    # 初稿报告（含待修正数据，update 前）（~15k tokens）
│   └── templates/
│       └── final_report_template.md    # 最终报告模板（~5k tokens）
├── scripts/
│   ├── calc_gmv.py                     # GMV 闭合校验脚本（~3k tokens）
│   ├── calc_inventory_days.py          # 库存天数计算（JD 口径）（~3k tokens）
│   └── validate_metrics.py             # 指标一致性校验工具（~3k tokens）
└── sessions/
    ├── main_session.md                 # 主 session 任务描述（~5k tokens）
    ├── slack_data_team_channel.md      # Slack 数据组群聊（~20k tokens）
    ├── feishu_pm_dm.md                 # 飞书 PM DM 历史（~15k tokens）
    ├── email_finance_review.md         # 邮件往来：财务口径审查（~12k tokens）
    └── discord_analyst_dm.md           # Discord 个人消息（~10k tokens）
```

**总估算体量：约 274k tokens（远超 100k 要求）**

每次 update 新增/修改文件体量约 40–60k tokens（超过 30k 要求）。

---

## Session 清单（4-6 个）

| Session ID | 渠道 | 类型 | 关键信息 |
|-----------|------|------|---------|
| S-main | 主任务 | 独立 session | 完整任务背景；内部指标口径手册；v1 原始数据 |
| S-slack | Slack #data-team | 群聊历史 | 同事讨论口径分歧（GMV 是否含税？退货率分子口径）；包含 tool call 痕迹（查询数据库）|
| S-feishu | 飞书 PM DM | 私信历史 | PM 要求用「JD 口径」计算库存天数（×360 而非 ×365）；含 V6 旧版报告链接 |
| S-email | 邮件 | 往来邮件 | 财务团队提供审计口径；含 V5 失真自动摘要作为附件 |
| S-discord | Discord 个人 DM | 私信历史 | 数据工程师告知 v1 GMV 数据有 bug（部分日期使用了 Method 1 而非 Method 2 口径）|
| S-update1 | 系统注入 | update session | 注入修正后的 gmv_daily_618_v2.csv 与 pm_correction_note.md |

---

## 15–18 轮 exec_check 概要

### 前置：大促第 1 周数据整合期

**Q1（第 1 轮）**
- 目标：解析内部指标口径手册，提取核心公式并输出结构化 JSON
- 产物：`output/metric_glossary.json`
- Check 锚点：`gmv_formula` 字段须为 `"GMV = transactions × AOV"`；`inventory_days_multiplier` 字段须为 `360`（非 365，依 JD 口径）；`take_rate_formula` 须含 `"commission / GMV"`
- 难度向量：V9（verbatim 引用真实锚点）
- Preference：P1（JSON 输出必须含 `source_url` 字段）

**Q2（第 2 轮）**
- 目标：识别 Slack 历史中的口径分歧，输出冲突清单
- 产物：`output/conflicts.json`
- Check 锚点：`conflict_count >= 2`；其中一个冲突须涉及「GMV 是否含平台补贴」；另一个涉及「库存天数分母是 360 还是 365」
- 难度向量：V1（多源信息冲突综合）
- Preference：P2（冲突条目须附 session 来源标识）

**Q3（第 3 轮）**
- 目标：用 calc_gmv.py 校验 v1 原始数据的 GMV 总量是否与产品/客单价数据闭合
- 产物：`output/gmv_validation_v1.json`；脚本须实际运行
- Check 锚点：`status` 字段须为 `"FAIL"`；`delta_pct` 须 > 2%（因为 v1 数据有 bug）；`affected_date_range` 须记录具体日期
- 难度向量：V7（须运行 Bash 脚本得到真实输出）、V4（数值闭合）

**Q4（第 4 轮）**
- 目标：根据 Discord DM 提示，识别 v1 中使用了错误 GMV 口径的日期范围，并写入报告
- 产物：`output/data_quality_report.json`
- Check 锚点：`jd_method1_dates` 须包含至少 3 个具体日期；`correct_method` 须为 `"Method 2"`
- 难度向量：V1（多源冲突）、V6（旧口径即红鲱鱼）

### 大促数据处理期（update 前）

**Q5（第 5 轮）**
- 目标：计算各品类的退货率，与 NRF 行业基准对比，标记异常品类
- 产物：`output/return_rate_analysis.json`
- Check 锚点：`apparel_return_rate` 须在 20–40% 区间；`electronics_return_rate` 须在 8–15% 区间；标记出超基准品类（若中国平台退货率达 60% 须特别标注）
- 难度向量：V9（引用 NRF 真实锚点）、V8（schema 严格校验）
- Preference：P3（异常品类须用 `"flagged": true` 标记）

**Q6（第 6 轮）**
- 目标：用 JD 官方口径公式（×360，5 季度平均库存）计算 LinkMart 大促期库存周转天数
- 产物：`output/inventory_days_618.json`
- Check 锚点：`formula_used` 须包含 `"360"` 和 `"5 quarters"`；`inventory_days` 数值须在 28–35 天合理区间（参照 JD Q4 2024: 31.5 天）；`multiplier` 字段须为 `360`
- 难度向量：V4（跨轮数值闭合，Q11 须引用此值）、V9（精确引用 JD 公式）
- Preference：P4（数值保留 1 位小数）

**Q7（第 7 轮）**
- 目标：阅读邮件附件中的「自动摘要报告」，识别其中的失真数据，标记蜜罐
- 产物：`output/honeypot_flags.json`
- Check 锚点：`honeypot_identified` 须为 `true`；`wrong_metric` 须为具体失真字段名（如 `"gmv_growth_rate"`）；`correct_value_source` 须指向原始数据文件
- 难度向量：V5（失真自动摘要诱饵）
- Preference：P2（须附反证来源）

**Q8（第 8 轮）**
- 目标：生成 618 大促分渠道 GMV 汇总表（Tmall、JD、Douyin 份额），与 Syntun/Daxue 基准对标
- 产物：`output/platform_gmv_share.json`
- Check 锚点：`tmall_share_pct` 在 45–55%；`jd_share_pct` 在 15–25%；`content_platforms_share_pct` > 20%
- 难度向量：V9（真实来源数值引用）、V8（schema 校验）

---

### Update 1（注入时机：Q8 完成后）

**Update 内容：**
1. 注入 `gmv_daily_618_v2.csv`（修正后 GMV 数据，重新计算后总量下调约 6%）
2. 注入 `pm_correction_note.md`（PM 发来的修正说明：v2 已切换至 Method 2 口径，且排除了平台补贴金额）
3. 注入 `update_slack_thread.md`（后续 Slack 讨论，含对 v1 数据的批评）

**体量：** v2 数据文件约 30k tokens + 2 个 md 文件约 8k tokens = 38k tokens（>30k 要求）

**对后续轮次的影响：** Q9–Q12 须使用 v2 数据，v1 数据所有结论须修正。

---

**Q9（第 9 轮）**
- 目标：用 v2 数据重新计算总 GMV，与 v1 结果对比并写入差异报告
- 产物：`output/gmv_revision_v2.json`
- Check 锚点：`v2_total_gmv` 须比 `v1_total_gmv` 低 5%–8%；`reason` 须包含 `"Method 2"` 和 `"subsidy excluded"`
- 难度向量：V2（动态 update 反转）、V10（supersede 辨别，后续 update 2 会部分撤销）

**Q10（第 10 轮）**
- 目标：根据 v2 数据重新计算品类转化率漏斗（加购率 → 结算率 → 最终转化率）
- 产物：`output/conversion_funnel_v2.json`
- Check 锚点：`overall_conversion_rate` 在 1.5%–5% 之间；`add_to_cart_rate` 在 5%–10%；`cart_to_checkout_rate` 在 55%–75%；每个数值须有计算过程字段
- 难度向量：V4（漏斗各环节数值必须数学一致）、V8（schema 严格校验）
- Preference：P4（数值保留 2 位小数）

**Q11（第 11 轮）**
- 目标：输出综合大促 KPI dashboard（含 GMV、转化率、退货率、库存天数），引用 Q6 库存天数值
- 产物：`output/kpi_dashboard.json`
- Check 锚点：`inventory_days` 须与 Q6 输出完全一致（drift 即判错，V4）；`gmv_total` 须与 Q9 v2 数值一致；`return_rate_overall` 须在合理区间
- 难度向量：V4（严格跨轮闭合）、V8（schema 校验）
- Preference：P1（须含 `data_version` 字段，值为 `"v2"`）

---

### Update 2（注入时机：Q11 完成后）

**Update 内容（含 Supersede）：**
1. 注入 `finance_audit_memo.md`：财务审计团队发现 Douyin 渠道数据口径与 Syntun 定义不一致，要求将 Douyin GMV 从平台汇总中**单独列出**而非计入「content platforms」合计（此条 supersede Update 1 中「content platforms 合计 > 22%」的要求）
2. 注入 `revised_category_benchmarks.json`：更新品类退货率基准（中国平台基准替换 NRF 美国基准，电子产品退货率基准调整为 15%–25%）
3. 注入 `legacy_report_v0.md`：一份标注为「archive」的旧版报告（V6 红鲱鱼，使用错误的 ×365 公式）

**体量：** 3 个文件合计约 35–40k tokens（>30k 要求）

**Supersede 说明：** Update 2 的 `finance_audit_memo.md` 明确写明「撤销 Update 1 pm_correction_note.md 中关于渠道合并方式的要求」，要求 Douyin 单独呈现。

---

**Q12（第 12 轮）**
- 目标：识别 Update 2 对 Update 1 的 supersede 关系，更新渠道 GMV 报表
- 产物：`output/platform_gmv_share_v3.json`
- Check 锚点：`douyin_gmv` 须单独字段而非包含在 `content_platforms`；`superseded_rule` 须标注 `"pm_correction_note.md § channel_aggregation"`
- 难度向量：V10（supersede 辨别）、V2（update 反转）

**Q13（第 13 轮）**
- 目标：识别并拒绝 legacy_report_v0.md 中的错误公式，输出红鲱鱼标记报告
- 产物：`output/legacy_report_flags.json`
- Check 锚点：`is_legacy` 须为 `true`；`wrong_formula` 须包含 `"×365"`；`correct_formula` 须包含 `"×360"` 和 `"5 quarters"` 引用
- 难度向量：V6（废弃副本红鲱鱼）、V9（verbatim 引用正确公式）

**Q14（第 14 轮）**
- 目标：用修正后的中国平台基准（Update 2）重新标记退货率异常品类
- 产物：`output/return_rate_analysis_v2.json`
- Check 锚点：`electronics_benchmark_source` 须为 `"China platform (revised)"`；`electronics_upper_bound` 须为 `25`（非 15）；与 Q5 结论的差异须明确标注
- 难度向量：V2（update 反转），V3（隐式考察 P3 preference 的 flagged 字段使用）

### 闭合与签收期

**Q15（第 15 轮）**
- 目标：生成最终综合报告草稿（Markdown），须引用所有真实锚点公式
- 产物：`output/final_report_draft.md`
- Check 锚点：文件行数 > 100 行；须包含字符串 `"GMV = transactions × AOV"`；须包含 `"× 360"` 或 `"× 360 days"`；须包含 `"Method 2"`；须包含 `"data_version: v2"`
- 难度向量：V9（verbatim 引用）、V3（隐式考察 P5 报告结构 preference）
- Preference：P5（最终报告须包含「数据来源」「口径说明」「异常标记」三个固定章节）

**Q16（第 16 轮）**
- 目标：对最终报告中的所有数值进行跨轮一致性自查，输出闭合验证表
- 产物：`output/closure_check.json`
- Check 锚点：`all_consistent` 须为 `true` 或列出具体不一致项；`inventory_days_matches_q6` 须为 `true`；`gmv_version_matches_q9` 须为 `true`
- 难度向量：V4（跨轮数值闭合）

**Q17（第 17 轮）**
- 目标：运行 validate_metrics.py 脚本，生成包含 SHA-256 签名的最终验证 token
- 产物：`output/verification_token.txt`；脚本须实际运行
- Check 锚点：文件内容须匹配格式 `VERIFIED:<sha256_hex>`；sha256 须为对 `output/kpi_dashboard.json` 内容的真实计算结果
- 难度向量：V7（Bash-sha256 sign-off，不跑脚本无法获得真实哈希）

**Q18（第 18 轮）**
- 目标：生成最终提交包清单，验证所有输出文件存在且 schema 完整
- 产物：`output/submission_manifest.json`
- Check 锚点：`total_files` >= 12；每个文件条目须含 `path`、`schema_valid`（true）、`data_version` 三个字段；`verification_token` 须与 Q17 输出一致
- 难度向量：V8（schema 严格校验）、V4（终局闭合）
- Preference：P1（manifest 须含 `generated_at` ISO 8601 时间戳字段）

---

## 4-5 条 Preference 规则

| ID | Preference 内容 | 注入方式 | 考察轮次 |
|----|----------------|---------|---------|
| P1 | 所有结构化 JSON 输出须包含 `source_url`（或 `source`）字段，以及 `generated_at` ISO 8601 时间戳 | Q1 显式说明 | Q11、Q18 静默考察 |
| P2 | 冲突与异常标记须附 session 来源标识（如 `"from": "slack_data_team_channel"`） | Q2 显式说明 | Q7、Q14 静默考察 |
| P3 | 异常品类须使用 `"flagged": true` 字段标记，不得仅用文字说明 | Q5 显式说明 | Q14 静默考察 |
| P4 | 数值字段统一保留 1 位小数（库存天数等整数级指标）或 2 位小数（百分比），不得混用精度 | Q6 feedback 注入 | Q10、Q11 静默考察 |
| P5 | 最终 Markdown 报告须包含「数据来源」「口径说明」「异常标记」三个固定章节（H2 级别） | Q15 模板暗示 | Q15 静默考察 |

---

## 拆分建议

素材充足，可沿以下维度拆分为 2 个独立场景：
1. **prd3-a（GMV 与营收闭合）**：聚焦 GMV 口径冲突、take rate 计算、平台份额汇总（Q1–Q8 + Q15–Q17）
2. **prd3-b（库存与退货优化）**：聚焦库存周转天数（JD 口径 ×360）、退货率分析、品类基准对比（Q6、Q13–Q14 扩展 + 新 Q 轮）

当前保留合并方案，以充分发挥跨轮数值闭合（V4）的考察深度。

---

## 删除建议

无。素材真实性强（SEC 监管文件、NRF 行业报告、Syntun 节点数据），体量充足，锚点可查，viability 为 strong。
