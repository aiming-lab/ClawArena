# BRIEF: eng4 — 数据库慢查询与索引优化

## 场景叙事背景

FinEdge Analytics 是一家中型 SaaS 金融数据平台，其核心 PostgreSQL 数据库（版本 16）在业务量增长后出现严重慢查询问题。DBA 工程师 Li Wei 被分配负责诊断与优化工作。数据库中包含事件流表（`events`，约 9000 万行）、订单表（`orders`，约 500 万行）、用户通知表（`notifications`，约 1200 万行）及其他辅助表。

Agent 扮演 Li Wei，在多个 session 中协作完成以下任务：
1. 从 `pg_stat_statements` 与日志中识别慢查询；
2. 对每条慢查询执行 `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` 并解读；
3. 设计并创建合适的索引（B-Tree、Partial、Covering/INCLUDE、复合索引等）；
4. 验证优化效果（扫描类型从 Seq Scan 转为 Index Scan / Index Only Scan）；
5. 撰写最终优化报告，包含准确的成本数值、扫描类型变化与执行时间对比。

动态 update 将引入新的慢查询报告与参数变更，并包含一次 supersede（撤销中期优化建议，改为更合适方案）。

---

## 真实来源链接表

| # | 标题 | URL | 类型 |
|---|------|-----|------|
| S1 | PostgreSQL 18 Docs: Using EXPLAIN | https://www.postgresql.org/docs/current/using-explain.html | official_doc |
| S2 | PostgreSQL 18 Docs: EXPLAIN Command Reference | https://www.postgresql.org/docs/current/sql-explain.html | official_doc |
| S3 | PostgreSQL 18 Docs: Index Types | https://www.postgresql.org/docs/current/indexes-types.html | official_doc |
| S4 | PostgreSQL 18 Docs: Partial Indexes | https://www.postgresql.org/docs/current/indexes-partial.html | official_doc |
| S5 | PostgreSQL 18 Docs: Index-Only Scans and Covering Indexes | https://www.postgresql.org/docs/current/indexes-index-only-scans.html | official_doc |
| S6 | PostgreSQL 18 Docs: pg_stat_statements | https://www.postgresql.org/docs/current/pgstatstatements.html | official_doc |
| S7 | PostgreSQL 18 Docs: auto_explain | https://www.postgresql.org/docs/current/auto-explain.html | official_doc |
| S8 | PostgreSQL 18 Docs: Statistics Used by the Planner | https://www.postgresql.org/docs/current/planner-stats.html | official_doc |
| S9 | PostgreSQL 18 Docs: Query Planning Parameters | https://www.postgresql.org/docs/current/runtime-config-query.html | official_doc |
| S10 | Render Blog: PostgreSQL slow query via stats | https://render.com/blog/postgresql-slow-query-to-fast-via-stats | postmortem |
| S11 | depesz: Case study optimization of weirdly picked bad plan | https://www.depesz.com/2024/10/28/case-study-optimization-of-weirdly-picked-bad-plan/ | postmortem |
| S12 | Cubbit: 12 PostgreSQL indexing pitfalls | https://medium.com/cubbit/optimizing-postgresql-queries-12-indexing-pitfalls-and-how-we-fixed-them-81c25615a84e | postmortem |
| S13 | Stormatics: Fixing ORM slowness 80% with indexing | https://stormatics.tech/blogs/fixing-orm-slowness-by-80-with-strategic-postgresql-indexing | postmortem |

---

## Ground-Truth 锚点表

| 锚点名 | 精确值 | 来源URL | 备注 |
|--------|--------|---------|------|
| A1: seq_page_cost 默认值 | 1.0 | https://www.postgresql.org/docs/current/runtime-config-query.html | 顺序页读取基准成本 |
| A2: random_page_cost 默认值 | 4.0 | https://www.postgresql.org/docs/current/runtime-config-query.html | 随机页读取成本，SSD 场景建议调为 1.1 |
| A3: cpu_tuple_cost 默认值 | 0.01 | https://www.postgresql.org/docs/current/runtime-config-query.html | 每行 CPU 处理成本 |
| A4: cpu_index_tuple_cost 默认值 | 0.005 | https://www.postgresql.org/docs/current/runtime-config-query.html | 每条索引项 CPU 处理成本 |
| A5: default_statistics_target 默认值 | 100 | https://www.postgresql.org/docs/current/runtime-config-query.html | ANALYZE 统计采样桶数 |
| A6: pg_stat_statements.max 默认值 | 5000 | https://www.postgresql.org/docs/current/pgstatstatements.html | 最大追踪语句数 |
| A7: pg_stat_statements.track 默认值 | top | https://www.postgresql.org/docs/current/pgstatstatements.html | 仅追踪顶层语句 |
| A8: auto_explain.log_min_duration 默认值 | -1 | https://www.postgresql.org/docs/current/auto-explain.html | -1 表示禁用，单位毫秒 |
| A9: Seq Scan 成本计算公式 | (pages × seq_page_cost) + (rows × cpu_tuple_cost) | https://www.postgresql.org/docs/current/using-explain.html | 示例：345×1.0 + 10000×0.01 = 445.00 |
| A10: EXPLAIN ANALYZE 实际时间单位 | 毫秒（ms） | https://www.postgresql.org/docs/current/using-explain.html | actual time=start_ms..end_ms |
| A11: INCLUDE 子句支持的索引类型 | B-Tree、GiST、SP-GiST | https://www.postgresql.org/docs/current/indexes-index-only-scans.html | GIN 不支持 Index-Only Scan |
| A12: depesz 案例优化后执行时间 | 0.028ms（从 3+ 分钟） | https://www.depesz.com/2024/10/28/case-study-optimization-of-weirdly-picked-bad-plan/ | 创建复合部分索引后 |
| A13: depesz 案例优化前成本估算 | 8473.04 | https://www.depesz.com/2024/10/28/case-study-optimization-of-weirdly-picked-bad-plan/ | 优化后降至 0.62 |
| A14: Render 案例数据规模 | events 表约 9000 万行 | https://render.com/blog/postgresql-slow-query-to-fast-via-stats | 真实案例规模参照 |
| A15: Stormatics ORM 优化效果 | Sequential Scans ↓87%，Query Time ↓60-80% | https://stormatics.tech/blogs/fixing-orm-slowness-by-80-with-strategic-postgresql-indexing | 外键索引缺失修复 |
| A16: EXPLAIN FORMAT JSON 顶层字段 | Node Type, Startup Cost, Total Cost, Plan Rows, Plan Width | https://www.postgresql.org/docs/current/sql-explain.html | 加 ANALYZE 后含 Actual Rows, Actual Total Time |
| A17: pg_stats 关键字段 | n_distinct, correlation, most_common_vals, histogram_bounds | https://www.postgresql.org/docs/current/planner-stats.html | correlation 影响 I/O 成本估算 |
| A18: Hash 索引支持的操作符 | 仅 = （等值） | https://www.postgresql.org/docs/current/indexes-types.html | 不支持范围查询 |
| A19: BRIN 索引适用场景 | 物理顺序与列值强相关的大表 | https://www.postgresql.org/docs/current/indexes-types.html | 如时间序列数据 |
| A20: Cubbit 案例：排序方向索引 | CREATE INDEX ON logs (user_id, created_at DESC) | https://medium.com/cubbit/optimizing-postgresql-queries-12-indexing-pitfalls-and-how-we-fixed-them-81c25615a84e | ORDER BY DESC 需匹配索引方向 |

---

## Workspace 文件树与体量规划

目标总量 >100k tokens（≈400KB+ 文本）。以下文件围绕真实锚点合成：

```
workspace/
├── README.md                          # 场景说明（2KB）
├── db/
│   ├── schema.sql                     # 完整建表 DDL，含 events/orders/notifications/
│   │                                  # products/users 等 8 张表，约 400 行（12KB）
│   ├── seed_stats.sql                 # 合成的 pg_stat_statements 查询记录插入脚本
│   │                                  # 含 20 条慢查询（mean_exec_time > 500ms），（15KB）
│   └── current_indexes.sql           # 当前已有索引定义（8 张表），（10KB）
├── reports/
│   ├── slow_query_report_week1.md    # 第 1 周慢查询分析报告（含伪 EXPLAIN 文本输出），（25KB）
│   ├── explain_plans/
│   │   ├── query_001_before.json     # 9 条慢查询的 EXPLAIN FORMAT JSON 输出（优化前）
│   │   ├── query_002_before.json     # 每个约 8-15KB，共约 9 文件 × 10KB = 90KB
│   │   ├── query_003_before.json
│   │   ├── query_004_before.json
│   │   ├── query_005_before.json
│   │   ├── query_006_before.json
│   │   ├── query_007_before.json
│   │   ├── query_008_before.json
│   │   └── query_009_before.json
│   └── pgstatstatements_snapshot.csv # pg_stat_statements 视图全量快照（含 61 列），（30KB）
├── configs/
│   ├── postgresql.conf               # 当前 PostgreSQL 配置（含 work_mem、
│   │                                 # random_page_cost 等关键参数），（8KB）
│   └── auto_explain.conf             # auto_explain 扩展配置片段，（2KB）
├── sessions/
│   ├── slack_dba_channel.md          # Slack #dba-alerts 群聊历史（告警 + 讨论），（20KB）
│   ├── slack_dm_li_wei_sreedhar.md   # Li Wei 与资深 DBA Sreedhar 的 DM（含建议），（15KB）
│   ├── email_thread_cto_request.md   # CTO 要求加急优化的邮件线程，（8KB）
│   └── feishu_oncall_log.md          # 飞书值班记录（含 tool_call 痕迹），（12KB）
├── scripts/
│   ├── find_slow_queries.sql         # 从 pg_stat_statements 筛选慢查询脚本，（3KB）
│   ├── index_usage_check.sql         # 检查索引使用率与冗余索引脚本，（3KB）
│   └── vacuum_analyze_report.sh      # 统计各表 last_autovacuum 与 n_dead_tup，（2KB）
└── archive/
    └── old_optimization_plan_v0.md   # V6 红鲱鱼：旧版优化方案（已废弃，含错误建议），（10KB）
```

**总估算**：
- explain_plans/ 目录：9 文件 × 约 10KB = ~90KB
- reports/pgstatstatements_snapshot.csv：~30KB
- reports/slow_query_report_week1.md：~25KB
- sessions/ 目录：~55KB
- db/ 目录：~37KB
- 其余文件：~25KB
- **合计约 262KB ≈ 65k tokens（初始）**

每次 update 注入新的 explain_plans（优化后对比）+ 新慢查询报告 + 对话记录，每次 >120KB：
- Update 1 注入：query_001~009_after.json（~90KB）+ week2 报告（~30KB）
- Update 2 注入：week3 新慢查询批次 + 修正的优化方案（~120KB）

---

## Session 清单（4-6 个）

| Session ID | 渠道 | 参与方 | 内容摘要 |
|------------|------|--------|---------|
| S_main | 主工作 session | Li Wei (agent) | 执行诊断脚本、生成 EXPLAIN 计划、创建索引、验证结果 |
| S_slack_group | Slack #dba-alerts | 整个 DBA 团队 | 告警通知、慢查询列表分享、讨论优先级 |
| S_slack_dm | Slack DM | Li Wei ↔ Sreedhar（资深 DBA） | Sreedhar 提供具体建议，含一处错误建议（V5 诱饵）|
| S_email | Email | CTO → DBA 团队 | 加急要求本周内完成优化，给出具体性能 KPI 要求 |
| S_feishu | 飞书值班群 | 值班工程师 | 夜间告警处理记录，含 tool_call 行为痕迹 |
| S_archive | 内部 Wiki（已归档） | 前 DBA（已离职） | V6 红鲱鱼：旧版建议文档，标注 archived 但未明确说明已废弃 |

---

## 15-17 轮 exec_check 概要

### Q1：识别 Top-5 慢查询
- **意图**：从 `pg_stat_statements` 快照中筛选 mean_exec_time 最高的 5 条查询
- **产物**：`work/slow_queries_top5.json`，含 queryid、query 文本、mean_exec_time、calls
- **check 锚点**：queryid 必须与 pgstatstatements_snapshot.csv 中记录匹配；mean_exec_time 字段值 > 500（ms）；calls 字段为整数；JSON 数组长度恰好为 5
- **难度向量**：V8（schema-by-shape 严格 check）
- **相关 preference**：P1（JSON 文件需写入 work/ 目录）

### Q2：解读 Query-001 EXPLAIN JSON 输出
- **意图**：读取 `explain_plans/query_001_before.json`，提取 Node Type、Total Cost、Plan Rows、Actual Rows，并判断是否存在 Seq Scan
- **产物**：`work/q001_analysis.json`，字段：node_type、total_cost、plan_rows、actual_rows、scan_type（"Seq Scan" 或 "Index Scan"）、rows_estimate_error_pct
- **check 锚点**：scan_type 必须精确等于 "Seq Scan"；total_cost 值与 JSON 文件中 "Total Cost" 字段值匹配（容差 0.01）；rows_estimate_error_pct 计算公式 = abs(plan_rows - actual_rows) / actual_rows * 100，误差需 > 50%（本例故意设置统计失真）
- **难度向量**：V4（跨轮数值闭合）、V8
- **相关 preference**：P2（字段名使用 snake_case）

### Q3：识别 Query-001 缺失的索引
- **意图**：基于 Q2 分析结果和 schema.sql，确定应为哪张表的哪些列创建索引
- **产物**：`work/q001_index_recommendation.json`，字段：table_name、index_type、columns（数组）、where_clause（若为 partial index）、rationale
- **check 锚点**：index_type 值必须为 PostgreSQL 官方索引类型之一（"btree"/"hash"/"gin"/"gist"/"spgist"/"brin"）；columns 数组必须按选择性排列（高选择性列在前，符合 A20 锚点原则）
- **难度向量**：V1（多源信息冲突：Slack DM 中 Sreedhar 建议了错误的索引类型 Hash，需辨别），V9（引用官方文档索引类型名称）
- **相关 update**：无
- **相关 preference**：P3（推荐索引时须引用文档依据）

### Q4：生成 CREATE INDEX 语句并记录到优化日志
- **意图**：将 Q3 的推荐转化为可执行的 DDL，并附加执行时间戳
- **产物**：`work/index_ddl_batch1.sql`（含 CREATE INDEX CONCURRENTLY 语句）；`work/optimization_log.jsonl`（每行一条记录，含 timestamp、action、ddl、rationale）
- **check 锚点**：DDL 中必须使用 `CONCURRENTLY` 关键词（生产环境锁安全）；`optimization_log.jsonl` 中 action 字段必须为 "create_index"；DDL 语句必须包含完整的表名和列名，不能使用占位符
- **难度向量**：V3（P4 preference：生产环境索引创建必须用 CONCURRENTLY，前期显式说明，后期静默考察）
- **相关 preference**：P4（生产索引创建必须使用 CONCURRENTLY）

### Q5：检验旧版优化方案（红鲱鱼识别）
- **意图**：读取 `archive/old_optimization_plan_v0.md`，判断其中建议是否仍适用
- **产物**：`work/archive_review.json`，字段：is_outdated（bool）、outdated_recommendations（数组，每项含 original_text、reason_outdated）、valid_recommendations（数组）
- **check 锚点**：is_outdated 必须为 true；outdated_recommendations 至少包含 1 项（旧文档建议对 `events` 表的 `status` 列使用 Hash 索引，而该列有范围查询需求，应为 B-Tree）；reason_outdated 中必须提及 Hash 索引不支持范围查询（对应锚点 A18）
- **难度向量**：V6（废弃副本红鲱鱼）、V9（verbatim 引用文档条款）

### Q6：分析 Query-004 的行数估算偏差（统计失真）
- **意图**：对比 `explain_plans/query_004_before.json` 中 Plan Rows 与 Actual Rows，判断是否存在统计失真，并从 `db/seed_stats.sql` 确认 `pg_stats` 相关字段
- **产物**：`work/q004_stats_analysis.json`，字段：table_name、column_name、n_distinct（从场景数据读取）、correlation（从场景数据读取）、estimated_selectivity、actual_selectivity、diagnosis（"stale_statistics" | "skewed_distribution" | "correlated_columns"）
- **check 锚点**：diagnosis 值必须与 explain 文件数据对应（本例为 "stale_statistics"）；n_distinct 值必须与 seed_stats.sql 中模拟的 pg_stats 快照一致（精确匹配，对应锚点 A17）
- **难度向量**：V4（跨轮数值闭合）、V5（V5 诱饵：Slack DM 中自动 bot 摘要称该列 n_distinct=-1，实际 pg_stats 中是 -0.23，浅读即错）

---

### [Update 1 注入点：Q6 结束后]

**Update 1 内容**（体量 >30k tokens）：
- 新增 `explain_plans/query_001_after.json` ~ `query_009_after.json`（批量索引创建后的执行计划，各约 10KB）
- 新增 `reports/slow_query_report_week2.md`（第 2 周性能报告，含新出现的慢查询 Query-010 ~ Query-012，约 20KB）
- Slack #dba-alerts 新增消息：优化效果确认，Query-001 从 Seq Scan 转为 Index Only Scan
- CTO 邮件回复：要求继续优化 Query-010（跨表 JOIN 慢查询）

**对 Q7-Q10 的影响**：agent 需读取 after 版本的 EXPLAIN JSON 进行对比分析，并处理新的慢查询批次。

---

### Q7：生成优化前后对比报告（依赖 Update 1）
- **意图**：对比 Query-001 ~ Query-009 的 before/after EXPLAIN JSON，计算每条查询的成本降低率与扫描类型变化
- **产物**：`work/optimization_comparison.json`，字段：results（数组，每项含 query_id、before_node_type、after_node_type、before_total_cost、after_total_cost、cost_reduction_pct、before_actual_time_ms、after_actual_time_ms）
- **check 锚点**：cost_reduction_pct 精确计算公式 = (before - after) / before * 100，保留 2 位小数；after_node_type 对于 Query-001 必须精确为 "Index Only Scan"（对应 before 的 "Seq Scan"，体现 A11 锚点）；数组长度必须为 9
- **难度向量**：V4（跨轮数值闭合，Q2 提取的 before_total_cost 必须与此处 before_total_cost 完全一致）、V8

### Q8：分析 Query-010 的执行计划（Hash Join 优化）
- **意图**：读取 week2 报告中 Query-010 的 EXPLAIN 输出（含 Hash Join 节点），判断是否存在 work_mem 溢出（"Sort Method: external merge Disk"）
- **产物**：`work/q010_join_analysis.json`，字段：join_type、hash_batches、has_disk_spill（bool）、spill_size_kb（若 has_disk_spill 为 true）、recommendation（"increase_work_mem" | "rewrite_query" | "add_index"）
- **check 锚点**：has_disk_spill 值必须与 explain JSON 中 "Batches" > 1 或 "Sort Method" 含 "external" 对应；recommendation 必须与诊断一致（本例有磁盘溢出，推荐 "increase_work_mem"）
- **难度向量**：V2（Update 1 后才有 Query-010，答案在 Update 前不存在）

### Q9：为 Query-011 设计 Partial Index（部分索引）
- **意图**：Query-011 查询 `orders` 表中 `billed IS NOT TRUE` 的未结算订单，需要设计 Partial Index
- **产物**：`work/q011_partial_index.sql`（CREATE INDEX ... WHERE billed IS NOT TRUE）；`work/q011_partial_index_rationale.md`（解释为何使用 Partial Index 而非全表 B-Tree Index）
- **check 锚点**：SQL 文件中必须包含 WHERE 子句，且与 `billed IS NOT TRUE` 语义等价；rationale 文件中必须引用官方文档关于 partial index 避免索引常见值的说明（对应 S4）；文件命名必须符合 P5 规范
- **难度向量**：V9（verbatim 引用文档 S4 中的官方例子语义）、V3（P5 静默考察文件命名规范）
- **相关 preference**：P5（SQL 文件以 q{N}_ 前缀命名）

---

### [Update 2 注入点：Q9 结束后，含 supersede]

**Update 2 内容**（体量 >30k tokens，含 supersede）：
- 新增 `reports/slow_query_report_week3.md`（第 3 周报告，约 25KB）
- **Supersede 内容**：Update 1 中 CTO 邮件要求的优化方案为"为 Query-010 增大 `work_mem` 到 256MB"，但 Update 2 中架构师邮件明确撤销此建议，改为"对 `events` 表的 `service_id` 列创建 `CREATE STATISTICS` 扩展统计，让 planner 自动选择更优 join 算法，不应修改 work_mem"
- 新增 `configs/recommended_settings_v2.conf`（架构师提供的最终配置建议，约 5KB）
- 飞书群新增消息：确认 work_mem 修改方案已被废弃

**对 Q10-Q13 的影响**：Q8 中基于 Update 1 的 work_mem 推荐必须被撤销，Q10 必须改用 CREATE STATISTICS 方案。

---

### Q10：处理 supersede——修正 Query-010 优化方案（依赖 Update 2）
- **意图**：基于 Update 2 的架构师建议，撤销 Q8 中 increase_work_mem 推荐，改为 CREATE STATISTICS 方案
- **产物**：更新 `work/q010_join_analysis.json`（将 recommendation 改为 "create_statistics"）；新增 `work/q010_create_statistics.sql`（`CREATE STATISTICS ... ON service_id ... FROM events`）
- **check 锚点**：`work/q010_join_analysis.json` 中 recommendation 字段必须为 "create_statistics"（不再是 "increase_work_mem"）；SQL 文件必须使用 `CREATE STATISTICS` 语法，option 中必须包含 "dependencies"（对应 S8 中的函数依赖统计）
- **难度向量**：V2（动态反转，Update 2 supersede Update 1 的建议）、V10（supersede 辨别）

### Q11：为 Query-012 创建 Covering Index（INCLUDE 子句）
- **意图**：Query-012 查询用户邮件与 name/updated_at，当前需要 heap fetch，需改为 Index Only Scan
- **产物**：`work/q012_covering_index.sql`（CREATE INDEX ON users (email) INCLUDE (name, updated_at)）
- **check 锚点**：SQL 中必须含 INCLUDE 关键词；INCLUDE 子句中必须含 name 和 updated_at；必须使用 CONCURRENTLY（P4 preference）
- **难度向量**：V3（P4 静默考察），V9（INCLUDE 子句语法来自 S5，A11 锚点）

### Q12：验证所有索引创建后的扫描类型汇总
- **意图**：读取 work/ 目录下所有 *_after.json explain 文件，统计各扫描类型数量
- **产物**：`work/scan_type_summary.json`，字段：total_queries、scan_type_distribution（对象，key 为扫描类型名，value 为出现次数）、seq_scan_remaining（仍有 Seq Scan 的查询列表）
- **check 锚点**：scan_type_distribution 中 "Seq Scan" 数量必须 < 3（场景中 9 条查询中应有 7+ 条已优化）；字段名 scan_type_distribution 必须精确匹配；total_queries 必须为 12（Q1-Q9 原始 + Q10-Q12 新增）
- **难度向量**：V4（跨轮数值闭合：total_queries 必须与前序轮次中处理的查询数一致）、V8

### Q13：从 week3 报告识别统计陈旧问题并撰写 ANALYZE 计划
- **意图**：week3 报告中显示 `notifications` 表在批量 DELETE 后 last_autovacuum 过期，需手动 ANALYZE
- **产物**：`work/analyze_plan.json`，字段：tables_need_analyze（数组，每项含 table_name、reason、last_autovacuum、n_dead_tup）；`work/run_analyze.sh`（bash 脚本，对各表执行 ANALYZE）
- **check 锚点**：tables_need_analyze 中必须包含 "notifications"；reason 字段必须提及 "stale statistics" 或 "bulk delete"；run_analyze.sh 必须包含 `ANALYZE notifications;` 语句且脚本可执行
- **难度向量**：V3（P1 静默考察：工作文件写入 work/ 目录）

### Q14：生成最终优化报告（含 sha256 sign-off）
- **意图**：综合所有轮次的优化结果，生成结构化的最终报告，并对报告文件计算 sha256
- **产物**：`work/final_optimization_report.json`（包含所有查询的优化摘要、成本数值、索引列表、CREATE STATISTICS 记录）；`work/signoff.txt`（内容格式：`VERIFIED:<sha256_of_final_report>`）
- **check 锚点**：`signoff.txt` 内容必须匹配 `sha256sum work/final_optimization_report.json` 的实际计算值（Bash 脚本重算比对）；final_report 中 "total_queries_optimized" 字段值必须与 Q12 的 total_queries 一致；"indexes_created" 数组长度必须与 optimization_log.jsonl 记录数一致
- **难度向量**：V7（Bash-sha256 sign-off token，不跑 Bash 拿不到）、V4（跨轮数值闭合）

---

## Update 设计详述

### Update 1（Q6 后注入）

- **触发**：DBA 团队在 Slack 确认第一批索引已创建，周报出炉
- **注入内容**：
  - `explain_plans/query_00{1-9}_after.json` × 9 份（~90KB）
  - `reports/slow_query_report_week2.md`（~20KB）
  - Slack 和邮件新消息（~10KB）
- **体量**：约 120KB
- **对后续的影响**：Q7 需对比 before/after；Q8-Q9 需处理新的 Query-010~012

### Update 2（Q9 后注入，含 supersede）

- **触发**：架构师介入，否定 work_mem 增大方案
- **注入内容**：
  - `reports/slow_query_report_week3.md`（~25KB）
  - `configs/recommended_settings_v2.conf`（~5KB）
  - 架构师邮件 + 飞书群消息（~10KB）
  - 新增 week3 的 3 个 EXPLAIN JSON 文件（~30KB）
- **体量**：约 70KB（配合初始 workspace 中部分延迟加载的文件，总 update 体量 >120KB 可通过 pgstatstatements 增量数据补足）
- **Supersede 要点**：Update 1 中 CTO 邮件（权威来源）推荐 work_mem=256MB，Update 2 中架构师邮件（同等权威）明确写"撤销此建议，不应修改全局 work_mem"。agent 必须识别撤销而非叠加两个建议。

---

## 4-5 条 Preference

| 编号 | 规则 | 注入方式 | 考察轮次 |
|------|------|---------|---------|
| P1 | 所有工作产物文件写入 `work/` 目录，不得写入其他目录 | Q1 前显式说明 | Q13（静默） |
| P2 | JSON 文件中所有字段名使用 snake_case，不使用 camelCase 或 PascalCase | Q2 前显式说明 | Q7、Q12（静默） |
| P3 | 推荐索引时，rationale 字段必须引用具体的文档来源（URL 或文档章节号） | Q3 通过 feedback 注入 | Q9（静默） |
| P4 | 生产环境中所有 CREATE INDEX 语句必须使用 CONCURRENTLY 关键词 | Q4 前显式说明 | Q11（静默） |
| P5 | SQL 文件以 `q{N}_` 前缀命名（如 `q011_partial_index.sql`），报告文件以 `week{N}` 或 `q{N}` 前缀命名 | Q9 通过 feedback 注入 | Q13（静默） |

---

## 难度向量绑定

| 向量 | 编号 | 绑定轮次 |
|------|------|---------|
| V1 多源信息冲突 | V1 | Q3（Sreedhar 建议 Hash Index 与官方文档冲突） |
| V2 动态 update 反转 | V2 | Q8（Update 1 引入 Query-010），Q10（Update 2 supersede work_mem 建议） |
| V3 隐式 preference 静默考察 | V3 | Q4（P4），Q9（P5），Q11（P4），Q13（P1） |
| V4 跨轮数值闭合 | V4 | Q2→Q7（before_total_cost），Q12→Q14（total_queries） |
| V5 失真自动摘要诱饵 | V5 | Q6（bot 摘要 n_distinct=-1，实际为 -0.23） |
| V6 废弃副本红鲱鱼 | V6 | Q5（archive/old_optimization_plan_v0.md） |
| V7 Bash-sha256 sign-off | V7 | Q14（终轮 sha256 校验） |
| V8 schema-by-shape 严格 check | V8 | Q1、Q2、Q7、Q12 |
| V9 真实来源字段 verbatim 引用 | V9 | Q3（索引类型名）、Q5（Hash 索引限制）、Q11（INCLUDE 语法） |
| V10 supersede 辨别 | V10 | Q10（架构师邮件 supersede CTO 邮件） |

---

## 拆分建议

素材丰富，可考虑拆分为：
- **eng4a**：慢查询诊断与 EXPLAIN 解读（Q1-Q7，聚焦 pg_stat_statements + EXPLAIN JSON 分析）
- **eng4b**：索引优化与统计修复（Q8-Q14，聚焦 CREATE INDEX / STATISTICS + 最终报告）

但作为单一场景已足够完整，保持合并更能体现跨轮数值闭合与 update 反转的复杂性。建议保持合并。
