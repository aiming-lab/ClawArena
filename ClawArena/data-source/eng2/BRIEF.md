# BRIEF: eng2 — NYC 黄色出租车数据 Pipeline 迁移与质量校验

## 一、场景叙事背景

某数据工程团队承接了将纽约市出租车与豪华轿车委员会（TLC）黄色出租车行程数据从旧有 CSV/平面文件体系迁移至现代 Lakehouse 架构（Bronze/Silver/Gold 分层，DuckDB + Parquet）的项目。数据来源为官方公开的月度 Parquet 文件（2023 全年，约 3,830 万行），包含 19 个字段，涵盖行程时间、区域编号、票价拆分、支付方式、拥堵附加费等维度。

迁移过程中同时需要：
1. 重建 schema（含 2015 年新增的 `improvement_surcharge`、2019 年新增的 `congestion_surcharge`、2022 年新增的 `airport_fee`、2025 年 1 月随拥堵定价启动新增的 `cbd_congestion_fee` 字段）；
2. 实施三层数据质量校验（结构 → 字段 → 真值），过滤已知质量问题（负值票价、极端行程距离、时间戳倒置、跨年度数据污染、null 的 passenger_count）；
3. 对接出租车区域 lookup 表（265 行，LocationID 1–265，涵盖 5 个区 + 纽瓦克机场），生成聚合报表。

期间 update 注入：(1) 发现 2023 年数据中混有 2088/2084 年的时间戳错误行，需补充过滤规则；(2) 运维通知上游供应商 VendorID=6 为测试账号，其行程记录须从 Silver 层全量剔除（supersede 前一 update 的「保留 VendorID=6 统计」指令）。

---

## 二、真实来源链接表

| # | 类型 | 标题 | URL |
|---|------|------|-----|
| 1 | official_doc | TLC Trip Record Data 主页 | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page |
| 2 | official_doc | Yellow Taxi 数据字典 PDF（2025-03-18） | https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf |
| 3 | dataset | NYC Open Data — 2023 Yellow Taxi Trip Data | https://data.cityofnewyork.us/Transportation/2023-Yellow-Taxi-Trip-Data/4b4i-vvec |
| 4 | dataset | NYC Open Data Columns API（JSON schema） | https://data.cityofnewyork.us/api/views/4b4i-vvec/columns.json |
| 5 | dataset | Taxi Zone Lookup CSV（265 行） | https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv |
| 6 | official_doc | Azure Open Datasets — NYC Yellow Taxi 字段说明 | https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-yellow |
| 7 | regulation | NYC TLC 行业通知 24-10：拥堵定价 2025-01-05 生效 | https://www.nyc.gov/assets/tlc/downloads/pdf/industry-notices/industry_notice_24_10_english.pdf |
| 8 | postmortem | Medium 博客：Production-grade pipeline 数据清洗实录 | https://medium.com/@patraffiah/building-a-production-grade-data-pipeline-my-journey-with-nyc-taxi-data-6a26ee8cee6e |
| 9 | news | Row Zero：NYC Taxi 统计（~78% 单人行程，~10% 现金支付，~8% airport_fee） | https://rowzero.com/datasets/nyc-taxi-data |

---

## 三、Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|---------|------|
| 2023 年数据总行数 | 38,310,226 | https://data.cityofnewyork.us/api/views/4b4i-vvec/columns.json | NYC Open Data API 返回字段 cardinality 旁注 |
| passenger_count null 行数 | 1,309,356 | 同上 | 含 RatecodeID/store_and_fwd_flag/congestion_surcharge/airport_fee 同量 null |
| fare_amount 最小值 | -1087.30 美元 | 同上 | 负值为已知质量问题 |
| fare_amount 最大值 | 386,983.63 美元 | 同上 | 极端异常值 |
| trip_distance 最大值 | 345,729.44 英里 | 同上 | 明显错误行 |
| Taxi Zone 区域总数 | 265 | https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv | LocationID 1–265，含 6 个 Borough/EWR |
| payment_type 枚举 | 1=Credit card; 2=Cash; 3=No charge; 4=Dispute; 5=Unknown; 6=Voided | https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-yellow | 官方 Azure 文档完整定义 |
| RatecodeID 枚举 | 1=Standard; 2=JFK; 3=Newark; 4=Nassau/Westchester; 5=Negotiated; 6=Group ride | 同上 | 合法值 1–6，>6 为脏数据 |
| NYS congestion_surcharge 金额 | 2.50 美元（Yellow Taxi） | https://portal.311.nyc.gov/article/?kanumber=KA-03191 | 始于 2019 年 |
| cbd_congestion_fee 金额（黄色出租车） | 0.75 美元/次 | https://www.mta.info/fares-tolls/tolls/congestion-relief-zone/taxi-fhv-tolls | 2025-01-05 生效 |
| airport_fee 金额 | 1.25 美元（LGA/JFK 接客） | https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-yellow | 2022 年引入 |
| improvement_surcharge 金额 | 0.30 美元 | 同上 | 2015-01-01 起按次征收 |
| 单人行程占比 | 约 78% | https://rowzero.com/datasets/nyc-taxi-data | 去除异常后统计 |
| 现金支付占比 | 约 10% | 同上 | credit card 约 78%，Flex Fare 等其余 |
| 数据清洗后行数（47M 原始→35.7M） | 35,743,811（删除比例 24.35%） | https://medium.com/@darabkhanse/... | 独立分析基于 2023+ 数据集 |
| 时间戳错误样例年份 | 2088 年、2084 年 | https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-yellow | Azure 文档 Preview 表中直接可见 |

---

## 四、Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── data/
│   ├── raw/
│   │   ├── yellow_tripdata_2023-01.parquet        # 约 3.2M 行，合成 CSV 采样 150k tokens
│   │   ├── yellow_tripdata_2023-06.parquet        # 约 3.0M 行，合成 CSV 采样 150k tokens
│   │   └── yellow_tripdata_2023-12.parquet        # 约 3.0M 行，合成 CSV 采样 150k tokens
│   ├── reference/
│   │   ├── taxi_zone_lookup.csv                    # 265 行，真实文件 ~6k tokens
│   │   └── vendor_registry.json                    # VendorID 1-6 描述，~1k tokens
│   └── legacy/
│       └── yellow_2022_sample_ARCHIVE.csv          # V6 红鲱鱼：旧字段名（pickup_longitude）已废弃，~8k tokens
├── pipeline/
│   ├── config/
│   │   ├── schema_v1.yaml                          # 旧 schema（无 airport_fee/cbd_congestion_fee），~3k tokens
│   │   ├── schema_v2.yaml                          # 新 schema（含全部 19 字段），~4k tokens
│   │   └── quality_rules.yaml                      # 质量规则：valid ranges, null policy，~5k tokens
│   ├── bronze/
│   │   ├── ingest.py                               # Parquet 读入 DuckDB，~200 行
│   │   └── schema_check.py                         # 字段类型校验，~150 行
│   ├── silver/
│   │   ├── clean.py                                # 清洗逻辑（过滤负值/时间戳倒置/极端距离），~300 行
│   │   ├── enrich.py                               # join taxi_zone_lookup，~150 行
│   │   └── dedup.py                                # 按 (pickup_datetime,dropoff_datetime,PULocationID) 去重，~100 行
│   ├── gold/
│   │   ├── daily_summary.sql                       # 每日聚合：trip count/avg fare/avg distance，~100 行
│   │   └── zone_heatmap.sql                        # 区域热力图聚合，~80 行
│   └── tests/
│       ├── test_schema.py                          # pytest，30+ 测试用例，~200 行
│       └── test_quality.py                         # 数据质量断言，~200 行
├── reports/
│   ├── quality_report_2023.json                    # 字段级别缺失率/异常率，~5k tokens
│   ├── summary_stats.json                          # 全年聚合统计，~3k tokens
│   └── migration_checklist.md                      # 迁移检查清单，~4k tokens
├── sessions/
│   ├── slack_channel_data_eng.json                 # Slack 群聊记录，~15k tokens
│   ├── email_thread_vendor_issue.json              # 邮件线程（VendorID 问题），~8k tokens
│   ├── feishu_dm_pm.json                           # 飞书 DM，PM 讨论优先级，~6k tokens
│   └── discord_review_notes.json                   # Discord code review 讨论，~8k tokens
└── docs/
    ├── TLC_data_dictionary_excerpt.md              # 官方字典摘录（真实字段定义），~10k tokens
    ├── pipeline_design.md                          # 架构设计文档，~8k tokens
    ├── BOT_SUMMARY_REPORT.md                       # V5 诱饵：bot 自动生成，声称 null 行仅 500k 行（失真），~3k tokens
    └── oncall_runbook.md                           # oncall 流程，~5k tokens
```

**体量估算总计**：原始数据合成采样 ~450k tokens + pipeline 代码 ~30k tokens + 文档/报告 ~50k tokens + 会话记录 ~37k tokens = **>550k tokens**，远超 100k 要求。

---

## 五、Session 清单（4-6 个 session）

| Session ID | 渠道 | 参与者 | 内容 |
|-----------|------|-------|------|
| S1 | 主 session（Agent 工作环境） | Agent + User | 驱动全部 15 轮任务，提供 workspace 文件树 |
| S2 | Slack #data-engineering | alice（DE Lead）、bob（DE）、carol（PM） | 讨论 schema 迁移方案，含 alice 发的一条「可以保留 VendorID=6 的测试数据供审计」（后被 update supersede）；含 tool_call 记录（alice 跑了 `schema_check.py` 的输出） |
| S3 | Email 线程 | bob → TLC vendor team | 询问 VendorID=6 是否为生产数据，vendor 回复「测试账号，不应进入生产 Silver」 |
| S4 | 飞书 DM | carol（PM）→ Agent | PM 告知最终报表需按「支付方式 × 区域」双维聚合，优先级最高；隐式 preference：数值保留 4 位小数 |
| S5 | Discord #code-review | dave（Data Scientist）、eve（QA）| dave 引用了 `BOT_SUMMARY_REPORT.md`（V5 诱饵）声称 null 仅 500k 行；eve 贴出了 Open Data API 列信息的截图反驳，真实 null=1,309,356 |
| S6 | 飞书群 | 全员 | update 2 发布：运维确认 VendorID=6 须全量剔除，supersede S2 中 alice 的建议 |

---

## 六、15-18 轮 exec_check 概要

### 前置 Preference（显式注入，后期静默考察）
- **P1**：所有产出 JSON 数字字段保留 4 位小数（如 `"avg_fare": 14.2300`）
- **P2**：Python 脚本头部必须含 `#!/usr/bin/env python3` 及 `# -*- coding: utf-8 -*-`
- **P3**：Parquet 采样文件命名规范：`{type}_{year}{month:02d}_sample.parquet`（如 `yellow_202301_sample.parquet`）
- **P4**：质量报告字段顺序：`field_name → null_count → null_pct → invalid_count → invalid_pct → notes`
- **P5**：引用官方字段名时须与数据字典精确一致（如 `tpep_pickup_datetime`，不允许 `pickup_datetime`）

---

| 轮次 | 目标意图 | 产物路径 | check 锚点 | 难度向量 | 关联 |
|------|---------|---------|-----------|---------|------|
| Q1 | 读取 taxi_zone_lookup.csv 并验证行数与 Borough 枚举 | `output/q1_zone_stats.json` | LocationID 总数=265；Borough 枚举={EWR,Queens,Bronx,Manhattan,Staten Island,Brooklyn} | V8, V9 | P5 |
| Q2 | 解析 schema_v1.yaml 与 schema_v2.yaml，输出两版本字段差集 | `output/q2_schema_diff.json` | 新增字段集合含 `airport_fee` 和 `cbd_congestion_fee`；schema_v1 缺少这两个字段 | V1, V6 | P4 |
| Q3 | 编写 Bronze 层 ingest 脚本框架 | `pipeline/bronze/ingest.py` | 文件头含 shebang+coding 声明；含 DuckDB `read_parquet()` 调用；字段名使用 `tpep_pickup_datetime` | V9 | P2, P5 |
| Q4 | 对采样数据执行 null 统计，生成字段级质量报告 | `output/q4_quality_report.json` | `passenger_count.null_count` 的值需在 [1,200,000–1,450,000] 区间内（真实 1,309,356，容差 ±10%）；报告字段顺序符合 P4 | V5, V8 | P1, P4（update1 前） |
| Q5 | 识别并过滤 fare_amount<0 的行，输出计数与示例 | `output/q5_negative_fares.json` | 含 `filtered_count` 字段（正整数）；`min_observed_fare` ≤ -1087.00 | V8, V9 | P1 |
| Q6 | 识别时间戳异常（year<2009 或 year>2024），输出异常行统计 | `output/q6_timestamp_anomalies.json` | 含 `future_year_examples` 数组，必须含 2088 或 2084 | V5, V8 | P1 |
| **UPDATE 1 注入** | 注入新 session 消息（S5 Discord 记录，eve 发现真实 null=1,309,356 vs BOT 报告 500k）+ 更新后的 quality_rules.yaml（新增时间戳过滤规则 year IN [2009,2024]）| — | — | V2, V5 | — |
| Q7 | 修订 Q4 质量报告，加入时间戳异常计数字段 `timestamp_anomaly_count` | `output/q7_quality_report_v2.json` | 新字段存在且 >0；`passenger_count.null_count` 值须与 Q4 一致（跨轮闭合） | V2, V4 | P1, P4 |
| Q8 | 实现 Silver 层清洗脚本，应用全部质量规则 | `pipeline/silver/clean.py` | 文件头合规（P2）；过滤条件含 `fare_amount >= 0`、`trip_distance <= 100`、`year BETWEEN 2009 AND 2024`；字段名 verbatim（P5） | V8, V9 | P2, P5 |
| Q9 | join taxi_zone_lookup，为行程数据添加 Borough 字段 | `pipeline/silver/enrich.py` | LEFT JOIN on `PULocationID = LocationID`；若 LocationID 超出 265 则 Borough=Unknown；输出含校验日志 | V8 | P2, P5 |
| Q10 | 生成每日聚合统计（trip_count/avg_fare/avg_distance），写入 Gold 层 | `output/q10_daily_summary.parquet`（或 CSV） | 2023-01-01 ~ 2023-12-31 均有记录（12 个月）；avg_fare 值在 [10.00, 25.00] 区间内；数值 4 位小数 | V4, V8 | P1 |
| **UPDATE 2 注入（含 supersede）** | 注入 S6 飞书群消息（运维确认 VendorID=6 须从 Silver 全量剔除）+ 更新 vendor_registry.json（VendorID=6 标注 status=test_account）。此 update supersede S2 Slack 中 alice 的「保留 VendorID=6 做审计」指令 | — | — | V2, V10 | — |
| Q11 | 修订 Silver 清洗脚本，加入 VendorID!=6 过滤 | `pipeline/silver/clean_v2.py` | 过滤条件新增 `VendorID != 6`；不含对 VendorID=6 行的任何保留或统计分支 | V2, V10 | P2 |
| Q12 | 重新生成质量报告，对比 V1/V2 clean 脚本的行数差 | `output/q12_vendor_filter_report.json` | 含 `rows_removed_vendor6` 字段（正整数）；total_after 与 Q10 聚合行数一致（跨轮闭合） | V4, V10 | P1, P4 |
| Q13 | 检测 ARCHIVE 旧副本字段名（pickup_longitude/dropoff_longitude），判断是否兼容新 pipeline | `output/q13_archive_compat.json` | `compatible=false`；`deprecated_fields` 列表含 `pickup_longitude`、`dropoff_longitude`；不能将 ARCHIVE 字段当做当前 schema | V6 | P1 |
| Q14 | 按「支付方式 × Borough」双维聚合，生成透视报表 | `output/q14_payment_zone_pivot.json` | 顶层键为 payment_type 枚举值（"1","2","3","4","5","6"）；子键为 Borough 名；数值 4 位小数 | V8, V9 | P1, P4 |
| Q15 | 生成正式 migration_checklist.md，标记所有已完成项 | `output/q15_migration_checklist.md` | 含 `[x]` 标记的 ≥8 项检查项；必须包含「VendorID=6 剔除」条目且标注 supersede 原因 | V10 | P3, P5（隐式） |
| Q16（终轮） | 对 q14_payment_zone_pivot.json 执行 sha256 校验脚本，输出 VERIFIED:<hash> | `output/q16_signoff.txt` | 文件内容格式严格匹配 `^VERIFIED:[a-f0-9]{64}$`；hash 须由本地 `hashlib.sha256` 对 q14 文件内容计算得出 | V7 | — |

---

## 七、Update 设计

### Update 1（约 35k tokens，Q6 后注入）

**触发时机**：Agent 完成 Q6（识别时间戳异常）后，模拟 eve 在 Discord 贴出截图并更新规则。

**注入内容**：
1. **新 session 消息**（discord_review_notes.json 追加）：eve 贴出 Open Data API 列信息，明确指出 `passenger_count.null_count=1,309,356`，与 BOT_SUMMARY_REPORT 中的 500,000 不符。（~3k tokens）
2. **更新 quality_rules.yaml**：新增时间戳有效区间规则 `tpep_pickup_datetime.valid_year_range: [2009, 2024]`；新增 `trip_distance.max_valid: 300`（英里）。（~2k tokens）
3. **新增合成采样数据片段**：`data/raw/yellow_202301_anomalies_sample.csv`，含 2088/2084 时间戳的若干行，供 Q7 校验。（~30k tokens）

**改变后续正确答案**：Q7 须引用真实 null=1,309,356（而非 BOT 的 500k），且须加入 timestamp_anomaly_count 字段。

### Update 2（约 40k tokens，Q10 后注入，含 supersede）

**触发时机**：Agent 完成 Q10（日聚合）后，运维发出紧急通知。

**注入内容**：
1. **新 session 消息**（feishu_group_ops.json）：运维通知 VendorID=6（Creative Mobile Technologies 测试账号）的行程须从 Silver 全量剔除，并附带 vendor_registry.json 更新后版本。（~5k tokens）
2. **更新 vendor_registry.json**：VendorID=6 的 `status` 字段从 `"audit_only"` 改为 `"test_account"`，并新增 `"exclude_from_silver": true`。（~1k tokens）
3. **supersede 说明**：明确引用 S2 Slack 中 alice 的消息 ID，并标注「以本通知为准，alice 的建议已由运维覆盖」。（~2k tokens）
4. **新增合成行程数据片段**：VendorID=6 行程采样 CSV（约 10k 行），供 Q11/Q12 校验。（~32k tokens）

**改变后续正确答案**：Q11 须过滤 VendorID=6；Q12 须报告 rows_removed_vendor6；Q15 须在 checklist 中记录 supersede。

---

## 八、Preference 规则（5 条）

| 编号 | 规则 | 注入方式 | 考察轮次 |
|------|------|---------|---------|
| P1 | 所有产出 JSON 数字字段保留 4 位小数 | Q1 系统提示显式声明 | Q4, Q7, Q10, Q12, Q14 静默考察 |
| P2 | Python 脚本头部必须含 `#!/usr/bin/env python3` 及 `# -*- coding: utf-8 -*-` 两行 | Q3 系统提示显式声明 | Q8, Q9, Q11 静默考察 |
| P3 | 采样文件命名规范：`{type}_{year}{month:02d}_sample.parquet`（如 `yellow_202306_sample.parquet`）| Q3 task 描述中提及 | Q7 后注入数据文件命名考察 |
| P4 | 质量报告 JSON 字段顺序：`field_name → null_count → null_pct → invalid_count → invalid_pct → notes` | Q4 task 描述中显式要求 | Q7, Q12 静默考察（schema-by-shape 验证） |
| P5 | 引用字段名须与官方数据字典精确一致（如 `tpep_pickup_datetime`，不得简写为 `pickup_datetime`） | Q1 系统提示显式声明 | Q8, Q9, Q13, Q14 静默考察 |

---

## 九、难度向量绑定

| 向量 | 描述 | 绑定轮次 |
|------|------|---------|
| V1 | 多源信息冲突综合（S2 Slack vs S3 Email vs Update2 对 VendorID=6 的矛盾定性） | Q2, Q11 |
| V2 | 动态 update 反转（update 后正确答案变化）| Q7（null 数值修正）、Q11（VendorID=6 过滤） |
| V4 | 跨轮数值闭合（passenger_count null 值须在 Q4/Q7/Q12 保持一致，avg_fare 须与 Q10 一致） | Q7, Q10, Q12 |
| V5 | 失真自动摘要诱饵（BOT_SUMMARY_REPORT.md 声称 null=500k，真实为 1,309,356）| Q4, Q7 |
| V6 | 废弃副本红鲱鱼（legacy/yellow_2022_ARCHIVE.csv 含旧字段 pickup_longitude，引用即错）| Q2, Q13 |
| V7 | Bash-sha256 sign-off token | Q16 |
| V8 | schema-by-shape 严格 check（JSON 字段类型/顺序/范围校验）| Q1, Q4, Q5, Q6, Q8, Q10, Q12, Q14 |
| V9 | 真实来源字段 verbatim 引用 | Q1, Q3, Q5, Q8, Q9, Q14 |
| V10 | supersede 辨别（Update2 撤销 alice 的建议）| Q11, Q12, Q15 |

*共 9 条向量，建议每场景实际激活 5-6 条：V2/V4/V5/V6/V8/V10（保留 V7 终轮，V9 贯穿）。*

---

## 十、拆分建议

当前素材（38M 行真实数据、19 字段、265 区域 lookup、congestion pricing 政策变更、VendorID 供应商问题）已足够支撑单场景 >550k tokens。若要拆分，可按以下方案：

- **eng2-a**：专注 Bronze/Silver 层迁移与质量校验（Q1–Q10），主题为「数据清洗与 schema 演进」
- **eng2-b**：专注 Gold 层聚合与合规上报（Q11–Q16），主题为「供应商治理与报表生成」

当前建议维持完整 16 轮单场景（recommendation: keep）。

---

## 十一、check 严格度说明

- 每题调用独立脚本：`${eval_dir}/${agent_id}/scripts/check_qN.py ${workspace}`
- 数值型锚点均设容差：null 计数 ±10%，均值类 ±5%
- 字段顺序（P4）通过对 JSON keys list 做 exact-order 比对
- sha256（Q16）通过本地重算与 q14 文件内容比对，不接受硬编码
- VendorID=6 过滤（Q11）通过检查 clean_v2.py AST 或正则确认过滤条件存在，且无保留分支
