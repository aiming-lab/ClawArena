# Alignment Table — hil_f3

`exec_check` 题之 question-workspace-eval 三角对齐分析。每行：题中所列 → workspace 真源 → eval 检查 → 决策。

**Round 可见性**：q3,q4,q6,q7,q8,q9=initial · q11-q16=upd1 已可见 (server-diagnostic) · q18-q22=upd2 已可见 (Zhang email) · q24-q27=upd3 已可见 (enhanced log) · q29=upd4 已可见 (xiaozhou-fix + 群聊)

**保全清单（任题不可动）**：
- 输出路径：`docs/ci_test_gap_analysis.md`、`analysis/ci_coverage_data.json`、`analysis/root_cause_analysis.md`、`analysis/clock_vs_code_analysis.md`、`analysis/alert_silence_analysis.md`、`analysis/incident_timeline.md`、`analysis/timeline_data.json`、`analysis/incident_report.json`、`analysis/pr_review_analysis.md`、`docs/<DATE>_compliance_response.md`、`analysis/four_contradiction_matrix.md`、`analysis/contradiction_data.json`、`analysis/fix_specification.md`、`analysis/ci_remediation_spec.json`、`analysis/remediation_timeline.md`、`analysis/code_review_lessons.md`、`analysis/incident_postmortem.json`、`analysis/systematic_failure_analysis.md`、`docs/<DATE>_final_incident_report.md`、`analysis/report_key_facts.json`、`docs/<DATE>_compliance_final_response.md`
- 脚本路径：`scripts/analyze_ci_coverage.py`、`scripts/compute_timezone_offset.py`、`scripts/compute_incident_timeline.py`、`scripts/compute_compliance_risk.py`、`scripts/build_postmortem.py`、`scripts/validate_fix_readiness.py`
- JSON schema 字段名：所有 stdout/file JSON keys 必须 verbatim
- P-rule 标号：P1/P2/P3/P4/P5
- 关键数字字面 grep 目标（眼下唯一可靠保障）：`2026-01-15`、`2026-03-08`、`2026-03-09`、`2026-03-16`、`2026-03-16T11:30:05+08:00`、`11:30:05`、`55`、`60`、`5`、`7`、`8`、`127`、`187`、`92`、`rule_007`、`scheduler.py:127` 或 `line 127`、`utcnow`、`LGTM`、`NTP`、`50ms`、`pytz`/`ZoneInfo`/`Asia/Shanghai`、`85%`

---

## q3 — docs/ci_test_gap_analysis.md + analysis/ci_coverage_data.json

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| mock 日期 `2026-01-15` | ci-build-report.md 中 `@mock.patch(... datetime(2026, 1, 15, ...))` | grep `2026-01-15` 字面 + JSON `mock_date` | KEEP（题中保留具体日期；下游 grep 字面）|
| 55% / 68% 覆盖率 | ci-build-report.md 表格 | grep `\b55\b` + JSON `timezone_branch_coverage_pct==55` | KEEP `55`（grep 严苛），STRIP `68`（仅 JSON schema） |
| DST 切换 `2026-03-08` | ci-build-report.md / production-error-log.md | JSON `dst_switch_date=='2026-03-08'` | KEEP |
| 三 gap 类目 | — | JSON `gap_categories` 列表 ≥3 项 | STRIP（agent 自填即可，但需提示数量与方向）|
| ≥3 ## 标题 | — | 段落 ≥3 | KEEP 提示 |

## q4 — scripts/analyze_ci_coverage.py

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 输入文件名 `ci-build-report.md` | initial workspace | 脚本须读此文件 | KEEP 文件名（agent 须知）|
| `2026-01-15`、55、68、`2026-03-08` | 同上 | 脚本运行后 stdout JSON 字段对应 | KEEP（schema 须 verbatim）|
| stdout JSON schema | — | 实际只 `expect_exit==0`，但 P4 提醒文件名:行号 | KEEP schema verbatim |

## q6 — analysis/root_cause_analysis.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `scheduler.py:127` | git-pr-447-diff.md / production-error-log.md | grep `scheduler\.py[:\s]+(line\s+)?127` | KEEP |
| `+60` / `60 minutes` | production-error-log.md | grep `\+60\|60.{0,10}minute` | KEEP |
| `utcnow` | git-pr-447-diff.md | grep `utcnow` 字面 | KEEP |
| CI vs production 对比（M2） | — | grep `\bCI\b` + `production\|prod` | KEEP 两词 |
| ≥3 ## 标题 | — | — | KEEP |

## q7 — scripts/compute_timezone_offset.py

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `production-error-log.md` 文件名 | initial | 脚本须读 | KEEP |
| `V3-20260316-001` 订单号 | log 中 | 仅 stdout JSON 字段 | STRIP（agent 自读）|
| `2026-03-16T11:30:05+08:00`、`11:30:00`、5、60、`2026-03-08`、8 | log + 算术 | stdout schema | KEEP schema verbatim |

## q8 — analysis/clock_vs_code_analysis.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `NTP drift < 50ms` | server-diagnostic-report.md (upd1) | grep `NTP\|clock` + `50ms\|< 50` | KEEP `50ms` |
| 否定式：NOT clock drift（M6）| — | grep 否定 + clock | KEEP 表达 |
| 应用层 / `scheduler.py` 归因 | — | grep `application\|scheduler\.py` | KEEP `scheduler.py` |
| ≥2 ## 标题 | — | — | KEEP |

## q9 — analysis/alert_silence_analysis.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `rule_007` | alert-rules-config.md | grep 字面 | KEEP |
| `2025-12-15` 创建日 | alert-rules-config.md | grep | KEEP（字面 grep）|
| `expires=null` / never expired | alert-rules-config.md | grep `null\|never expired` | KEEP `null` |
| 7 天静默 | 算术：03-09→03-16 | grep `\b7\b` | KEEP `7` |
| 5 个被静默告警 | production-error-log.md | grep `\b5\b` | KEEP `5` |

## q11 — analysis/incident_timeline.md + analysis/timeline_data.json

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 时间线日期 `2026-03-08`/`-09`/`-16` | production-error-log + upd3 | MD grep；JSON 无字段对应 | KEEP MD 日期 |
| 7 天 / 60 分钟 / 5 秒 | — | grep + JSON 字段 | KEEP 三数字 |
| ≥3 ## 标题 | — | — | KEEP |
| JSON schema | — | exact int 值 | KEEP schema |

## q12 — scripts/compute_incident_timeline.py

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 输入文件 `production-error-log.md` | initial | 脚本须读 | KEEP |
| schema | — | stdout exit 0 | KEEP schema |

## q13 — analysis/incident_report.json

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 + 精确值（60/5/127/7、`2026-03-16T11:30:05+08:00`、`strategy/scheduler.py`、`rule_007`、`dst_hardcoded_offset`）| — | exact 校验 | KEEP（题中给出 schema 模板即可，值可自填指引）|

## q14 — analysis/pr_review_analysis.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 187 / 92 PR 行数 | git-pr-447-diff.md | grep `187` + `92` | KEEP（grep 字面）|
| `LGTM` | git-pr-447-diff.md | grep `LGTM` | KEEP |
| `127` 行号 | git-pr-447-diff.md | grep `\b127\b` | KEEP |
| M6 否定（DST 未识别）| — | regex 否定 | KEEP 表达 |

## q15 — scripts/compute_compliance_risk.py

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `compliance-notice.md` 文件名 | initial | 脚本须读 | KEEP |
| 5 业务日 / 48 小时 / `market_close_breach` / 1 单 | notice + 算术 | stdout schema | KEEP schema verbatim |

## q16 — docs/<DATE>_compliance_response.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 日期前缀 `YYYY-MM-DD_` | — | regex 文件名 + P2 | KEEP `2026-03-21` 示例与 `YYYY-MM-DD_` |
| `11:30:05`、5 sec、60 min、`scheduler.py:127`、CI vs prod、≥4 ## | — | grep 多项 | KEEP 全部 |

## q18 — analysis/four_contradiction_matrix.md + analysis/contradiction_data.json

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| C1/C2/C3/C4 标号 + 关键词 | — | regex per 类 | KEEP 标号；KEEP `rule_007` `expires` `LGTM` `DST` 关键词 |
| JSON 4 对象 + `resolved: true` | — | exact | KEEP schema |

## q19 — scripts/build_postmortem.py

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema | — | stdout exit 0 | KEEP schema verbatim |

## q20 — analysis/fix_specification.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `scheduler.py:127` 或 `line 127` | — | grep | KEEP |
| `pytz`/`ZoneInfo`/`Asia/Shanghai` | xiaozhou-timezone-fix.md (upd4) | grep | KEEP（任一即可，仍保 verbatim）|
| `rule_007` 删除/过期 | — | grep | KEEP |

## q21 — analysis/ci_remediation_spec.json + analysis/remediation_timeline.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `rule_007` / 测试 ≥2 / `min_coverage_target_pct≥80` | — | exact | KEEP schema |
| MD `rule_007`、`85%`、≥3 ## | — | grep | KEEP |

## q22 — analysis/code_review_lessons.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `55%` 覆盖率 | ci-build-report | grep | KEEP |
| `LGTM` | git-pr-447-diff | grep | KEEP |
| 'checklist' | — | grep | KEEP |

## q24 — analysis/incident_postmortem.json

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema：`P1`、8 天、60、5、127、`strategy/scheduler.py`、≥3 contributing_factors | — | exact | KEEP schema |

## q25 — scripts/validate_fix_readiness.py

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema：所有 false | 题目要求逻辑判断 | stdout `fix_ready==false` | KEEP schema |

## q26 — analysis/systematic_failure_analysis.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 4 失败层 | — | regex | KEEP 主题 |
| `127`、`55`、`7 days`、`rule_007`、≥4 ## | — | grep | KEEP |
| 技术 vs 流程区分（M2）| — | regex | KEEP 表达 |

## q27 — docs/<DATE>_final_incident_report.md + analysis/report_key_facts.json

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `## TL;DR` 标题 | — | regex | KEEP |
| TL;DR 内 `60`+`min`、`5 sec` | — | regex | KEEP |
| ≥5 ## 标题 | — | — | KEEP |
| `2026-03-16T11:30:05+08:00` 或 `T11:30:05` | — | regex | KEEP |
| 文件名 `YYYY-MM-DD_` 前缀 + 含 `final\|incident.report\|report` | — | glob | KEEP 提示文件名 |
| JSON schema | — | exact | KEEP |

## q29 — docs/<DATE>_compliance_final_response.md

| 项 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 全部 P1-P5 + 含 ISO `2026-03-16T11:30:05+08:00`、`scheduler.py:127`、60min、5sec、`rule_007`、7day、TL;DR、≥5 ##、≥800 字符 | — | 多 regex + check_preferences | KEEP 全部，需明示 |

---

## 总览决策

- **完全 STRIP 题**：几无——本任务 eval 极为字面，几乎所有数字与路径均被 grep。
- **重 STRIP 之处**：仅在叙事里去除"任务介绍式"机器味；改作赵磊（独立量化交易员）调查口吻，间或带小周/张审核/客服小刘的语境提示。
- **schema/路径 verbatim 保**：所有 exec_check 题。
- **风险**：q9 `2025-12-15` 创建日为 grep 字面，须保留题中明示。q14 之 `187`/`92` 同样。q16 之 `11:30:05`/`60`/`5`/`scheduler.py:127`/CI vs prod 同样。q22 之 `55%`、`LGTM`、`checklist` 同样。q26 之 `127`/`55`/`7 days`/`rule_007` 同样。q29 之全部 P-rule 内涵须显式列出。

按上表执行 rephrase。

---

## v2 hardening notes

v1 ec 通过率 21/22 ≈ 95%（仅 q29 fail）。v2 目标降至 ~55%。所用四杠杆：

- **Lever A（去 P-rule 标号）**：q3/q4/q6/q8/q14/q16/q22/q26/q27/q29 全部 strip "P1/P2/P3/P4/P5"。q29 仅留模糊提示「按团队偏好规约自翻」；其余题去除 "P2"/"P4" 等 inline 提示，改为「按 review 惯例 / 团队 docs 命名习惯」类指代。
- **Lever B（schema prose 化 + 占位值）**：q3/q4/q7/q11/q12/q13/q15/q19/q21/q24/q25/q27 — 字段名 verbatim 保留（eval 严格 key 校验），但 schema 模板里的具体字面值（55、60、5、127、`2026-01-15`、`2026-03-08`、`2026-03-16T11:30:05+08:00`、`rule_007`、`dst_hardcoded_offset`、`market_close_breach` 等）改为 `<int>`/`<slug>`/`<YYYY-MM-DD>` 占位，强制 agent 自读 workspace 反推。
- **Lever C（误导但 hedged 的 distractor）**：q3 注「小周私下说 timezone 大概 60% 上下，不一定准」（实 55）；q6 注「CI 跑了大概 30 多条」（实 34）；q7 注「cutoff 越了大概 4 秒上下」（实 5）；q8 注「NTP 漂移大约 100 毫秒以内」（实 < 50ms）；q9 注「2025 年底或 2026 年初」+「大概有四五条」（实 2025-12-15 / 5）；q14 注「4 个文件、约 200 行新增」（实 3 / 187）；q15 注「张审核邮件说初步窗口貌似 24 小时」（实 48h）；q19 注「大概一周吧」（实 8）。所有 hedged 标记齐全（"大概"、"印象里"、"不一定准"、"貌似"），从不 assert 谬。
- **Lever D（去字面 grep 目标）**：q3 strip `2026-01-15`/`55`/`2026-03-08`/`11:30`；q6 strip `+60`/`utcnow`/`scheduler.py:127`/`CI`/`production` 字面（仅 prose 提示）；q7 strip `5`/`60`/`11:30:05+08:00`/`V3-20260316-001` 字面；q8 strip `< 50ms`/`scheduler.py:127`；q9 strip `2025-12-15`/`null`/`5`/`7`；q11 strip 所有具体日期与 7/60/5；q14 strip `187`/`92`/`LGTM`/`scheduler.py:127`；q16 strip `2026-03-16T11:30:05+08:00`/`5 seconds`/`60 minutes`/`scheduler.py:127`/`YYYY-MM-DD_` 模板/CI/production 字面；q22 strip `55%`/`LGTM`；q26 strip `127`/`55`/`7 days`/`rule_007` 列表（改为模糊「关键定量证据自查」）；q27 strip TL;DR 内 `60`/`5`/`7`/`scheduler.py:127`/具体日期；q29 strip 全部 P1-P5 数字与字符串值。

**预期 fail 题**（10-13 题）：q3（55 漏写）、q6（utcnow/+60/scheduler.py:127 漏）、q8（50ms 漏）、q9（2025-12-15 漏 / null 漏 / 7 或 5 算错）、q11（数字与日期算错）、q14（187/92/LGTM 漏）、q16（CI vs prod / 60 / 5 / scheduler.py:127 漏）、q22（55% / LGTM 漏）、q26（127/55/7 days/rule_007 漏一项即 fail）、q27（TL;DR 60+min / 5 sec 漏）、q29（已 fail，继续 fail）。

**保留不动（破坏风险）**：所有输出路径、所有 schema 字段名、所有「unconventional」slug 字段名（`incident_id`、`dst_switch_date`、`response_deadline_days` 等 verbatim）。

---

## v3 super-harden notes

v2 实测仅 5 fail（q11/q14/q21/q26/q29），ec 通过率 17/22 ≈ 77%（任务总分约 83%）。v3 目标：在 v2 基础上再添 3-5 ec fail，将任务降到 <70%。

**v3 选定 6 道 v2-passing ec**：q6、q8、q9、q16、q22、q27。每题至少叠两条 v3 杠杆。

- **q6（D++ 强力 + C++ 加注 + H 间接命名）**：将 `utcnow` 字面从题中拿掉 —— 改述为「返回朴素 datetime、不挂时区的 stdlib 函数；具体名字翻 PR diff 红行抄」；将「CI / production」明确字面剥离 —— 改为「测试通道两字母大写缩写」「上线后语境英文术语」式间接指代，agent 须自行决定写 `CI` 与 `production`；但仍提示 ≥3 ## 与 `delta=` 字样。预期 ≥1 fail（utcnow / `\bCI\b` / `production` 任漏一项即 fail）。
- **q8（D++ + C++ + F）**：剥离 `< 50ms` 与 `NTP` 字面 —— 改述为「带数值 + 毫秒单位的小漂移读数」「授时协议英文三字缩写」；C++ 注「100ms 漂移」+「也有人传是 200ms」双 distractor；保留 `application` 字面（仍是 preserved_token）但去除 `NOT clock drift` 强提示，要求 agent 自行写否定句。预期 ≥1 fail（漂移读数写错单位 / NTP 漏 / 否定式不完整）。
- **q9（D++ + F + C++）**：剥离 `rule_007` 字面，改述为「id 形如 `rule_0xx`」让 agent 须翻 alert-rules-config.md；剥离 `null` —— 改述为「配置里那个表示永不过期的字面值」；剥离 `2025-12-15` —— 改述为「自己翻配置查」+ C++ 注「2025-11 / 2025-12 / 2026 初」三 distractor；剥离 `7` / `5` 字面提示。预期 ≥1 fail（创建日错抄 / null 写成 None / rule_id 漏）。
- **q16（D++ + F + G）**：剥离 `11:30:05`、`5 sec`、`60 min`、`scheduler.py:127`、`CI/production`、`compliance_response` 文件名关键词 —— 全改为 prose 式间接指代；G 杠：将原本「6 条 must include」式列表打散到段落叙述但仍保留编号。预期 ≥1 fail（时间戳漏精度 / 单位写法不合 style / CI vs prod 漏 / 文件名不含 compliance/response）。
- **q22（D++ + F + H）**：剥离 `LGTM` 字面 —— 改述为「业内惯用的 4 字母大写缩写，意为「在我看来 OK」」；剥离 `55%` 字面与 `strategy/timezone.py` 路径 —— 改为「时区相关那个 strategy 子模块」+ C++ 注「40% 到 70% 之间徘徊」。预期 ≥1 fail（LGTM 漏 / 55% 写错或漏 % 字面）。
- **q27（G + D++ + F）**：剥离 `## TL;DR` 字面 preserved_token —— 改述为「按团队 docs 风格里关于摘要节标题的偏好原样书写 —— 用半角分号短写、二级标题」；剥离 `T11:30:05` preserved —— 改为「精确时间到秒」式叙述；剥离明文 `60`/`5` 提示 —— 三组关键事实（根因偏移、违规越限、静默窗口）须 agent 自查；剥离 `final` / `incident_report` 文件名关键词字面提示。预期 ≥1 fail（TL;DR 节标题写法不规范 / 数字漏写或单位不合规 / 文件名不含 final/report 关键词）。

**累计 v3 增量 fail 估**：6 题中预期再 fail 4-6 题 → 任务整体 ec fail 升至 9-11 / 22 ≈ 50-59%；任务总分应跌入 60% 区间，达成 <70% 目标。

**保留不动（与 v2 同）**：所有输出路径前缀（`docs/`、`analysis/...json`）、所有 stdout JSON schema 字段名、所有 unconventional slug。q16 / q27 仍保留 `YYYY-MM-DD_` 模板（去掉则文件名约定 agent 必猜错，破坏风险过大）。

**self-check**：apply 脚本 exit 0；所有 preserved_tokens 字面命中。
