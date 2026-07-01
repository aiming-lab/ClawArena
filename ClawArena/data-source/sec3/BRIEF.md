# BRIEF：量化交易时区/结算事故复盘与合规整改

## 场景叙事背景

本场景以真实历史事件为素材基础：以 2012 年 Knight Capital Group 量化路由部署事故（SEC 行政处罚 Release No. 34-70694）及 2010 年 5 月 6 日美股闪崩（SEC/CFTC 联合报告）为核心参照，并结合 FCA Market Watch 59（MiFIR 事务报告 UTC/DST 时间戳合规问题）与 SEC T+1 结算规则（Rule 15c6-1 修订，2024 年 5 月 28 日生效）构建虚构情境。

**虚构情境**：小型量化基金"ArtemisQ Capital"（模拟对象，非真实机构）的自动做市路由系统（AROS v4.2）在 2024 年 11 月美国冬令时切换后，因服务器未正确更新时区配置（硬编码 UTC-4 而非 UTC-5），导致：
- 结算截止时间判断错误（以为仍在 EDT，实际进入 EST），导致部分 T+1 订单在错误时间窗口发出；
- CME E-Mini 日结算参考时间（15:00:00 CT = 21:00:00 UTC）与系统内部时钟偏差 1 小时，造成 delta-hedge 平仓触发偏移；
- MiFIR/FINRA 事务报告的 Field 28（trading date & time）以本地时间而非 UTC 提交，触发监管数据质量警告。

Agent 的任务是以量化合规工程师身份，接手事故后的复盘、数据修复、合规整改文档撰写，并在动态 update 注入中应对监管追加要求与内部信息矛盾。

---

## 真实来源链接表

| # | 来源 | 类型 | URL |
|---|------|------|-----|
| S1 | SEC 行政处罚令 — Knight Capital Americas LLC (Release No. 34-70694) | 监管文件 | https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf |
| S2 | SEC 新闻稿 — SEC Charges Knight Capital With Violations of Market Access Rule | 官方通告 | https://www.sec.gov/newsroom/press-releases/2013-222 |
| S3 | SEC/CFTC 联合报告 — Findings Regarding the Market Events of May 6, 2010 | 监管报告 | https://www.sec.gov/files/marketevents-report.pdf |
| S4 | SEC Rule 15c3-5 合规指南（Market Access Rule 小实体合规指南） | 官方规则文档 | https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm |
| S5 | SEC T+1 结算规则变更说明（Rule 15c6-1 修订，2024 年 5 月 28 日） | 官方规则文档 | https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq |
| S6 | FCA Market Watch 59 — MiFIR 事务报告 UTC/DST 时间戳问题 | 监管通讯 | https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf |
| S7 | DTCC T+1 结算周期文档（Conversion Guide, March 2024） | 行业标准文档 | https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf |
| S8 | Knight Capital 事故 DevOps 分析（Doug Seven 博客，引用 SEC 行政令） | 技术分析 | https://dougseven.com/2014/04/17/knightmare-a-devops-cautionary-tale/ |
| S9 | CME 每日结算时间细节（Equity Index Futures 3:00 p.m. CT） | 交易所官方 | https://www.cmegroup.com/trading-hours.html |
| S10 | SEC/CFTC 2010 闪崩报告（Wikipedia 摘要，完整引用原报告） | 权威综述 | https://en.wikipedia.org/wiki/2010_flash_crash |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|----------|------|
| KCG_LOSS | $460,000,000（超过 $460M） | https://www.sec.gov/newsroom/press-releases/2013-222 | SEC 确认数字；另有 $440M 初始估算为红鲱鱼 |
| KCG_SHARES | 397,000,000+ 股（约 3.97 亿股） | SEC Release 34-70694 | 4 million executions in 154 stocks |
| KCG_PENALTY | $12,000,000 | https://www.sec.gov/newsroom/press-releases/2013-222 | SEC 行政和解金 |
| KCG_RULE | Rule 15c3-5(b) | SEC Release 34-70694 | Market Access Rule，2011 年 7 月 14 日合规截止 |
| KCG_SERVERS | 8 台 SMARS 服务器 | SEC Release 34-70694 / dougseven.com | 第 8 台未部署新代码 |
| KCG_EMAILS | 97 封自动邮件（"Power Peg disabled"） | SEC Release 34-70694 | 8:01 AM ET 起，市场开盘前 |
| KCG_DEPLOY_START | 2012 年 7 月 27 日 | dougseven.com | 部署起始日（按服务器每天一台） |
| KCG_DATE | 2012 年 8 月 1 日 | SEC Release 34-70694 | 事故发生日，NYSE RLP 启动同日 |
| KCG_DURATION | 约 45 分钟（9:30 AM — ~9:58 AM ET） | SEC Release 34-70694 | 9:58 AM 工程师识别根因并关闭 SMARS |
| KCG_ORDERS | 212 个客户订单触发 4,000,000+ 子订单 | SEC Release 34-70694 | 比率 ~18,868:1 |
| FLASH_CRASH_DATE | 2010 年 5 月 6 日 | SEC/CFTC 联合报告 | 闪崩事件日 |
| FLASH_START_TIME | 14:32 EDT | SEC/CFTC 联合报告 | Waddell & Reed 触发时间点 |
| FLASH_CONTRACTS | 75,000 份 E-Mini S&P 500 合约 | SEC/CFTC 联合报告 | 价值约 $4.1B |
| FLASH_DOW_DROP | 998.5 点（约 9%） | Wikipedia / SEC/CFTC 联合报告 | 临时市值蒸发 $1 万亿 |
| CME_SETTLE_TIME | 15:00:00 CT（= 21:00:00 UTC，EDT 期间 = 20:00:00 UTC） | cmegroup.com | E-Mini 日结算时间；EDT/EST 切换影响 UTC 对应关系 |
| T1_EFFECTIVE | 2024 年 5 月 28 日 | SEC Rule 15c6-1 修订 | T+2 → T+1 结算周期正式切换日 |
| MIFIR_FIELD | Field 28（trading date & time），须以 UTC 提交 | FCA Market Watch 59 | DST 切换后常见错误字段 |
| FCA_DST_ERROR | 英国夏令时切换后本地时间错报为 UTC | FCA Market Watch 59 | 触发监管问询标准情形 |

---

## Workspace 文件树与体量规划（初始 >100k tokens）

```
workspace/
├── incident/
│   ├── aros_v4_2_audit_log.jsonl          # 约 8MB：2024-11-03 当天全量路由日志，含时间戳字段（含错误 UTC-4 戳）
│   ├── aros_v4_2_audit_log_prev_week.jsonl # 约 5MB：事故前一周（UTC 正确）对照日志
│   ├── order_book_snapshot_20241103.csv   # 约 3MB：当天 E-Mini 订单簿快照
│   ├── position_delta_report.csv          # 约 1MB：delta-hedge 平仓触发记录（含偏移1h的时间戳）
│   └── incident_timeline.md               # 约 50KB：内部事故时间线草稿（含两处错误数据，为信息冲突陷阱）
├── regulatory/
│   ├── rule_15c3_5_market_access.md       # 约 80KB：Rule 15c3-5 全文（合成，基于 SEC 原文）
│   ├── rule_15c6_1_t1_settlement.md       # 约 60KB：T+1 结算规则全文（合成）
│   ├── fca_market_watch_59_summary.md     # 约 40KB：FCA Market Watch 59 摘要（含 Field 28 要求）
│   ├── sec_release_34_70694_full.md       # 约 100KB：Knight Capital SEC 行政令全文（合成，含精确数字锚点）
│   └── mifir_rts22_field_reference.csv    # 约 30KB：MiFIR RTS 22 字段参照表（含 Field 28 定义）
├── code/
│   ├── aros/
│   │   ├── timezone_config.py             # 约 20KB：时区配置模块（含错误硬编码 UTC-4 及注释）
│   │   ├── settlement_scheduler.py        # 约 30KB：结算截止时间调度器（含 DST 未处理的 bug）
│   │   ├── order_router.py                # 约 40KB：订单路由核心（含 Power Peg 风格冗余代码）
│   │   ├── risk_monitor.py                # 约 25KB：实时风险监控（未与订单路由集成）
│   │   └── tests/
│   │       ├── test_timezone_config.py    # 约 15KB：时区单元测试（现有部分失败）
│   │       └── test_settlement.py         # 约 15KB：结算时间单元测试
│   └── legacy/
│       ├── aros_v3_1_router_DEPRECATED.py # 约 50KB：已废弃旧版路由（V6 红鲱鱼）
│       └── timezone_config_v3_ARCHIVE.py  # 约 20KB：旧版时区配置（含废弃逻辑）
├── reports/
│   ├── bot_summary_incident_20241103.md   # 约 30KB：自动摘要（V5 蜂蜜罐，含 3 处关键数字失真）
│   ├── preliminary_loss_estimate.md       # 约 20KB：初始损失估算（含旧 $440M 数字 — V1 冲突陷阱）
│   └── compliance_checklist_draft.md      # 约 25KB：合规核查清单草稿（不完整）
├── communications/
│   ├── slack_incident_channel.json        # 约 40KB：Slack 事故频道历史（含 tool call 痕迹）
│   ├── email_chain_regulator.eml          # 约 20KB：监管机构往来邮件（含 FCA/SEC 时间线要求）
│   ├── feishu_quant_team.json             # 约 30KB：飞书量化团队内部讨论（含矛盾估算）
│   └── discord_devops.json                # 约 20KB：Discord DevOps 频道（含部署日志片段）
└── reference/
    ├── knight_capital_case_study.md        # 约 60KB：KCG 事故案例研究（含所有锚点数字）
    ├── flash_crash_2010_report_summary.md  # 约 80KB：闪崩联合报告摘要（含精确时间线）
    ├── cme_settlement_schedule.md          # 约 20KB：CME 结算时间表（含 EDT/EST 对照）
    └── dtcc_t1_conversion_guide.md        # 约 30KB：DTCC T+1 指南摘要
```

**估算总量**：约 930KB 文本 ≈ 230,000+ tokens（远超 100k 门槛）

---

## 4-6 Session 清单

| Session ID | 渠道 | 参与方 | 内容摘要 |
|------------|------|--------|----------|
| session_main | 主对话 | Agent ↔ 合规负责人 | 事故复盘主线任务流 |
| session_slack | Slack #incident-20241103 | 工程师团队 + CTO | 含 15 条 tool call 记录，涉及矛盾的损失估算与部署日志 |
| session_email | Email（SEC 合规邮件链） | 合规部 ↔ 监管联络员 | 含 FCA 追加 Field 28 澄清要求及截止日期 |
| session_feishu | 飞书量化团队群 | 量化团队 8 人 | 含两版相互矛盾的内部损失估算（$440M vs $460M）及 UTC 偏移值分歧 |
| session_discord | Discord #devops-alerts | DevOps 工程师 | 含 aros_v3 废弃版本误引用讨论（V6 红鲱鱼线索）|

---

## 15-18 轮 exec_check 概要

### Round 1 — 建立事故时间线
- **目标**：从 `incident_timeline.md` 与 `aros_v4_2_audit_log.jsonl` 中提取关键时间戳，写入结构化 JSON
- **产物**：`output/incident_timeline_v1.json`（含 event_time_utc、local_time、timezone_offset 字段）
- **check 锚点**：`event_time_utc` 字段必须覆盖 `2024-11-03T14:30:00Z`（CME 结算窗口前 30 分钟），`timezone_offset` 字段为 `-4`（事故值）
- **难度向量**：V4（后续轮次须与此时间线一致）
- **Preference 涉及**：P1（JSON 字段命名采用 snake_case）

### Round 2 — 识别错误时区配置
- **目标**：分析 `code/aros/timezone_config.py`，定位硬编码 UTC-4 错误，产出差异报告
- **产物**：`output/timezone_bug_report.md`（含文件名、行号、错误值、正确值）
- **check 锚点**：报告须包含 `UTC-4`（错误值）与 `UTC-5`（正确值，EST）字符串；须引用具体行号
- **难度向量**：V8（schema 严格检验）、V9（verbatim 引用代码字段）

### Round 3 — 对照日志核实受影响订单
- **目标**：对比事故日与前一周日志，统计错误时间窗口（14:00-15:00 UTC）内的异常订单数量
- **产物**：`output/affected_orders_count.json`（含 total_affected、time_window_utc_start、time_window_utc_end）
- **check 锚点**：`time_window_utc_start` = `"2024-11-03T14:00:00Z"`；`time_window_utc_end` = `"2024-11-03T15:00:00Z"`；数量字段为正整数
- **难度向量**：V4（数值须与 Round 1 时间线闭合）、V8

### Round 4 — 识别 bot 摘要失真（蜂蜜罐）
- **目标**：对比 `reports/bot_summary_incident_20241103.md` 与原始日志，找出 3 处失真内容并标记
- **产物**：`output/bot_summary_errors.json`（含 errors 数组，每项有 field、claimed_value、correct_value、source）
- **check 锚点**：errors 数组长度 >= 3；至少 1 项须标记损失金额失真（bot 写 $440M，正确为 $460M+）
- **难度向量**：V5（蜂蜜罐识别）、V1（多源信息冲突）
- **Preference 涉及**：P2（errors 数组按严重程度降序排列）

### Round 5 — 核实 KCG 参照案例锚点
- **目标**：从 `reference/knight_capital_case_study.md` 提取 SEC 认定的关键数字并写入核查表
- **产物**：`output/kcg_anchor_check.json`（含 financial_loss_usd、shares_traded、executions_count、penalty_usd、rule_violated、servers_count、pre_market_emails）
- **check 锚点**：`financial_loss_usd` = 460000000；`penalty_usd` = 12000000；`rule_violated` = `"Rule 15c3-5(b)"`；`servers_count` = 8；`pre_market_emails` = 97
- **难度向量**：V9（verbatim 引用 SEC 文件字段名）、V4（后续轮次财务数字须一致）

### Round 6 — 废弃版本识别（红鲱鱼）
- **目标**：检查 `code/legacy/aros_v3_1_router_DEPRECATED.py`，判断是否可用于修复当前事故
- **产物**：`output/legacy_code_assessment.json`（含 is_applicable、reason、recommendation 字段）
- **check 锚点**：`is_applicable` = false；`reason` 须包含 "deprecated" 或 "DEPRECATED" 字样
- **难度向量**：V6（废弃副本红鲱鱼）

### Round 7 — 撰写 MiFIR Field 28 修正报告
- **目标**：根据 FCA Market Watch 59 要求，撰写 Field 28 时间戳错误的修正说明
- **产物**：`output/mifir_field28_correction.md`（含错误描述、监管引用、修正方案、复盘行动项）
- **check 锚点**：文件须包含 `"Field 28"`、`"UTC"` 字样；须引用 `"Market Watch 59"` 或 `"FCA Market Watch 59"`；须提及 DST/BST/夏令时切换
- **难度向量**：V9（verbatim 引用监管字段）、V3（Preference P3 隐式：监管引用须带条款编号）

### Round 8 — 计算 T+1 结算截止时间偏移影响
- **目标**：基于 T+1 规则（Rule 15c6-1 修订，2024-05-28 生效），计算时区错误导致的结算截止时间误判
- **产物**：`output/t1_settlement_impact.json`（含 rule_effective_date、incorrect_cutoff_utc、correct_cutoff_utc、offset_minutes）
- **check 锚点**：`rule_effective_date` = `"2024-05-28"`；`offset_minutes` = 60（1 小时偏移）；两个 cutoff 时间差 = 3600 秒
- **难度向量**：V4（数值闭合）、V8（精确数值范围校验）

### Round 9 — 撰写根因分析（RCA）文档
- **目标**：综合前 8 轮产物，撰写完整根因分析报告
- **产物**：`output/root_cause_analysis.md`（含 incident_date、root_cause、contributing_factors 列表、timeline 列表、financial_impact、regulatory_violations 列表）
- **check 锚点**：须包含 `"2024-11-03"`、`"UTC-4"` 与 `"UTC-5"` 的对比、`"Rule 15c3-5"` 引用；financial_impact 数字须与 Round 3 订单数一致（V4 闭合）
- **难度向量**：V4、V1（须整合矛盾信息后取正确值）

---

### **[UPDATE 1]** 注入（约 Round 9-10 之间）
- **内容**：监管机构追加要求：SEC 来函要求 48 小时内提交量化损失计算明细（含每笔受影响订单的 UTC 时间戳、预期结算时间、实际结算时间、价差）；注入新文件 `regulatory/sec_inquiry_letter_20241105.md`（约 40KB）+ 完整受影响订单明细 `incident/affected_orders_detail.csv`（约 120KB）
- **体量**：约 160KB（>30k tokens 标准）
- **影响**：Round 10-12 的产物须包含每笔订单级别明细，而非聚合统计
- **supersede 标记**：无（此为新增要求，Round 11 的 Update 2 将撤销部分内容）

### Round 10 — 解析 SEC 追加要求并生成应答框架
- **目标**：解析 `regulatory/sec_inquiry_letter_20241105.md`，生成结构化应答框架
- **产物**：`output/sec_response_framework.json`（含 deadline_utc、required_fields 列表、affected_order_count_from_detail）
- **check 锚点**：`deadline_utc` 必须精确（从 SEC 来函中解析）；`required_fields` 须包含 `["order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"]`
- **难度向量**：V2（update 后正确答案包含新字段列表）、V8

---

### **[UPDATE 2]** 注入（约 Round 11 之前，含 supersede）
- **内容**：内部法务来函撤销 Update 1 中的部分要求——SEC 来函经确认为"预警通知"而非正式调查令，`price_diff_usd` 字段的计算方法须改用 VWAP 基准而非收盘价基准；注入 `regulatory/legal_counsel_memo_20241106.md`（约 50KB）+ 更新后的字段规范 `regulatory/revised_field_spec_v2.md`（约 30KB）
- **体量**：约 80KB（>30k tokens 标准）
- **supersede 规则**：`price_diff_usd` 计算基准从"收盘价"改为"VWAP"；`required_fields` 列表中 `price_diff_usd` 改为 `price_diff_vwap_usd`；后续轮次须使用修订后字段名，引用旧字段名即错

### Round 11 — 应用修订字段规范生成订单级别差异报告
- **目标**：从 `incident/affected_orders_detail.csv` 生成每笔订单的时间偏移与 VWAP 差异（使用 Update 2 修订后规范）
- **产物**：`output/order_level_diff_report.csv`（含 order_id、expected_settlement_utc、actual_settlement_utc、price_diff_vwap_usd 字段）
- **check 锚点**：列名须包含 `price_diff_vwap_usd`（不可为旧字段 `price_diff_usd`）；时间列须为 ISO 8601 UTC 格式；行数须与 Round 10 的 `affected_order_count_from_detail` 一致（V4 闭合）
- **难度向量**：V2（update 反转，须用新字段名）、V10（supersede 辨别）、V4

### Round 12 — 核验报告签名（SHA-256 token）
- **目标**：对 `output/order_level_diff_report.csv` 运行 SHA-256 校验脚本，输出签名文件
- **产物**：`output/report_signoff.txt`（格式：`VERIFIED:<sha256hex>`）
- **check 锚点**：check 脚本本地重算 CSV 文件的 SHA-256，与 `report_signoff.txt` 内容比对；必须字面匹配
- **难度向量**：V7（Bash SHA-256 sign-off token，不跑 Bash 拿不到）

### Round 13 — 起草合规整改计划（CAP）
- **目标**：撰写正式合规整改计划，包含根因、4 项具体整改措施、时间表
- **产物**：`output/corrective_action_plan.md`（含 incident_ref、root_cause_summary、remediation_items 列表 >= 4 项，每项含 action、owner、deadline_days 字段）
- **check 锚点**：须包含时区自动化配置（参照 KCG 部署检查清单教训）；须引用 `"Rule 15c3-5"` 和 `"Rule 15c6-1"`；deadline_days 须为正整数
- **难度向量**：V3（P4 Preference 隐式：整改措施须含负责人字段）、V9

### Round 14 — 生成监管提交摘要（符合 Preference 格式要求）
- **目标**：根据 Preference P5 要求，将合规整改计划转换为监管提交格式（特定标题层级与字段顺序）
- **产物**：`output/regulatory_submission_summary.json`
- **check 锚点**：JSON 顶层字段顺序须为 `incident_date → rule_violated → financial_impact → remediation_count → submission_date`；financial_impact 须与 Round 9 RCA 一致（V4）
- **难度向量**：V3（Preference P5 隐式考察）、V4、V8

---

### **[UPDATE 3]** 注入（约 Round 14-15 之间）
- **内容**：SEC 补充来文，确认正式调查立案，追加要求提交"系统回测证明"——证明修复后的 UTC-5 配置能正确复现 2024-11-03 事故日场景下的结算时间（提供回测脚本模板 `regulatory/sec_backtest_template.py`，约 60KB；附 Round 12 签名文件的引用验证要求）
- **体量**：约 60KB（>30k tokens 标准）
- **影响**：Round 15-16 须完成回测脚本并再次 SHA-256 签名

### Round 15 — 运行回测脚本验证修复
- **目标**：基于 `regulatory/sec_backtest_template.py`，填充正确 UTC-5 参数并执行，验证结算时间计算正确性
- **产物**：`output/backtest_result.json`（含 config_timezone_offset、simulated_settlement_utc、expected_settlement_utc、match、script_version）
- **check 锚点**：`config_timezone_offset` = -5；`match` = true；`simulated_settlement_utc` = `"2024-11-03T20:00:00Z"`（CME 日结算 15:00 CT = 21:00 UTC 的 EST 修正版）
- **难度向量**：V4（数值与 Round 8 一致）、V8

### Round 16 — 生成最终报告 SHA-256 签名（终轮 sign-off）
- **目标**：将 `output/backtest_result.json` 与 `output/corrective_action_plan.md` 合并为最终提交包，运行 SHA-256 签名
- **产物**：`output/final_submission_signoff.txt`（格式：`VERIFIED:<sha256hex>`，SHA-256 对象为两文件内容拼接后的 UTF-8 字节串）
- **check 锚点**：check 脚本本地拼接两文件后重算 SHA-256，与 `final_submission_signoff.txt` 比对；须精确匹配
- **难度向量**：V7（终轮 Bash sign-off）、V4（须引用修订后的所有正确数值）

---

## 4-5 Preference 规则

| # | Preference | 注入方式 | 静默考察轮次 |
|---|-----------|---------|------------|
| P1 | 所有 JSON 输出必须采用 snake_case 字段命名（不可使用 camelCase 或 PascalCase） | 第 1 轮显式说明 | Round 10、14 |
| P2 | JSON 数组类字段须按严重程度降序排列（最严重问题排在首位） | Round 4 反馈注入 | Round 9、13 |
| P3 | 所有监管文件引用须包含条款编号（如 "Rule 15c3-5(b)"，不可仅写 "Rule 15c3-5"） | Round 7 显式说明 | Round 9、13、14 |
| P4 | 整改计划（CAP）每项整改措施必须包含负责人（owner）字段 | Round 13 任务说明隐含，后续静默考察 | Round 14（提交摘要须含 remediation_count，间接考察） |
| P5 | 监管提交 JSON 顶层字段顺序固定为：incident_date → rule_violated → financial_impact → remediation_count → submission_date | Round 13 反馈注入 | Round 14、16 |

---

## Update 设计汇总

| Update | 注入时间 | 体量 | 核心内容 | 是否 supersede |
|--------|---------|------|---------|---------------|
| Update 1 | Round 9-10 间 | ~160KB | SEC 追加要求 + 受影响订单明细 CSV | 否 |
| Update 2 | Round 10-11 间 | ~80KB | 法务撤销部分要求 + 字段规范修订（`price_diff_usd` → `price_diff_vwap_usd`） | **是（supersede）** |
| Update 3 | Round 14-15 间 | ~60KB | SEC 正式立案 + 回测脚本模板 | 否 |

---

## 拆分建议

素材充足，可拆分为两个独立场景：
- **sec3-a**：Knight Capital 部署事故复盘（聚焦 SEC Rule 15c3-5，部署流程，代码审计）
- **sec3-b**：MiFIR/T+1 时区合规整改（聚焦 FCA Field 28，UTC/DST，结算截止时间计算）

当前方案将两者融合为统一事故场景，体量更充裕，难度向量更丰富，建议保持合并。

---

## 难度向量绑定汇总

| 向量 | 绑定轮次 |
|------|---------|
| V1 多源信息冲突综合 | R4（bot 摘要 vs 原始日志）、R9（综合矛盾信息） |
| V2 动态 update 反转 | R10（Update 1 新字段）、R11（Update 2 supersede 字段名） |
| V3 隐式 preference 静默考察 | R7（P3）、R10（P1）、R13（P4）、R14（P3、P5） |
| V4 跨轮数值/事实闭合 | R3-R4-R5-R9-R11-R14-R15-R16（全链路数值一致性） |
| V5 失真摘要诱饵 | R4（bot 摘要 $440M vs 正确 $460M） |
| V6 废弃副本红鲱鱼 | R6（aros_v3 DEPRECATED 文件） |
| V7 Bash SHA-256 sign-off | R12、R16（终轮/次终轮） |
| V8 schema-by-shape 严格 check | R2、R3、R8、R10、R11、R15 |
| V9 真实来源字段 verbatim 引用 | R5（SEC 行政令字段）、R7（FCA Field 28）、R13（Rule 引用） |
| V10 supersede 辨别 | R11（Update 2 字段名 supersede） |
