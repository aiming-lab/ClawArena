# Alignment Table — hil_c7

NexaFlow API breach事件，Alex Rivera为PM, 协调三轮 update 之 scope/合规/披露任务。
本表针对每一 `exec_check` 题做"题中所列值 → workspace 真源 → eval 检查 → 处理决策"对齐。

**Round 可见性**：
- 初始 (round 0)：api_endpoint_register.md, customer_data_inventory.md, vulnerability_technical_brief.md, incident_response_checklist.md, notification_draft_v1.md, disclosure_report_initial.md, developer_docs_screenshot.md, USER.md
- upd1 (q7+)：access_log_analysis.md
- upd2 (q13+)：deployment_timeline.md
- upd3 (q19+)：notification_final.md

**Exec_check 鉴定题**：q3, q5, q6, q8, q9, q10, q11, q12, q14, q15, q16, q17, q18, q20, q21, q22, q23, q24, q26, q27 (共20)

**保全清单**：所有输出路径（docs/*, analysis/*, scripts/*）、JSON schema 字段名、`YYYY-MM-DD_` 文件名前缀格式、enum 值（critical|high|medium|low; high|medium|low）、关键 grep 字面量（7.5, 2340/2,340, 12000/12,000, 847, 02:14, PR #847, Nov 5/2024-11-05, Nov 26/2024-11-26, Dec 7/2024-12-07, Oct 14, 72）。

---

## q3 — docs/breach_impact_prelim.json (initial)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段（cvss_score, affected_endpoints, data_types_at_risk, initial_scope_estimate, checklist_completion_pct） | — | json keys | KEEP verbatim |
| `cvss_score: 7.5` 字面 | vulnerability_technical_brief.md | abs(cvss-7.5)<0.05 | STRIP（agent 读 brief 自得；但因 7.5 极易被 P5 grep， KEEP-LITERAL on schema example）|
| `initial_scope_estimate: 12000` | vulnerability_technical_brief.md（Jake 之 12,000） | 范围 2000-15000 | STRIP — agent 读 brief 自得 |
| 数据类型枚举 list | customer_data_inventory.md | len>=4 | STRIP — 引"inventory 中所列字段" |

## q5 — docs/YYYY-MM-DD_incident_timeline.json (initial)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `YYYY-MM-DD_` 前缀 | — | regex prefix | KEEP verbatim |
| `>=5 entries` + ISO8601 + Nov 26 disclosure date | 各源 + disclosure_report_initial.md | regex 2024-11-2[5-9] | STRIP 具体值，但 Nov 26 grep 字面之故， KEEP "November 26 disclosure" 之 cue |
| 6 个示例事件具体时间戳 | disclosure_report_initial.md, vulnerability_technical_brief.md, notification_draft_v1.md, api_endpoint_register.md | 仅检 5 entry + iso + Nov26 | STRIP 详细时间戳列表 |

## q6 — docs/scope_conflict_analysis.md (initial)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `2,340` / `12,000` 字面 | customer_data_inventory.md / vulnerability_technical_brief.md | grep `\b2,?340\b`、`\b12,?000\b` | KEEP 字面（grep 脆弱） |
| 三源文件名 | — | grep filenames（>=2） | KEEP — 引名 |
| `>=3 ##` headings | — | count headings | STRIP 数字，引 P3 |

## q8 — docs/access_log_analysis_summary.md (upd1, log file首introduce)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `Nov 5, 02:14:33 UTC`, `847`, `2,340`, `12 calls`, `pipeline-configs`, IP range | upd1 access_log_analysis.md | grep `02:14`、`847`、`Nov 5\|2024-11-05`、`pipeline.config\|/api/v2` | KEEP `Nov 5`/`02:14`/`847` 字面（grep）；其余 STRIP |
| 引述 access_log_analysis.md by name | — | P4 check | KEEP — 此为 file 首次 introduce 之轮 |

## q9 — docs/scope_decision.md (upd1)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 三估计具体值 (2340/under-500/2340) | upd1 log + 既有 inventory | grep `\b2,?340\b` | KEEP `2,340` — grep 字面脆弱 |
| Diego/access_log 为 most credible | upd1 log | grep `Diego\|access_log\|log analysis` 相关 | KEEP — 引 Diego/access_log_analysis 名 |
| M6 disclosure_report_initial 不可作 definitive | — | regex anti-defer | STRIP — 自然语言提醒"不要把初始 disclosure 当 ground truth" |

## q10 — scripts/analyze_scope.py (upd1)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/analyze_scope.py` | — | exists+exec | KEEP |
| schema 字段 (`endpoint_count`, `vulnerable_endpoints`, `affected_data_types`, `estimated_affected_records`, `data_sensitivity`) | — | dict keys | KEEP verbatim |
| `estimated_affected_records: 2340` | inventory | int==2340 | STRIP — agent 数 inventory（但保 schema 例值） |
| `data_sensitivity` enum (`high`) | — | enum | KEEP enum 集 |
| 5 个 affected_data_types 名称 | — | len>=4 | STRIP — 仅留 schema example，agent 自填 |

## q11 — docs/scope_consistency_report.md (upd1)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 三源文件名 verbatim | — | grep filename ×3 | KEEP — 此 M3 题 eval 强求三 filename 出现于 agent 输出 → 题中亦保留 cue |
| `2340` / `12,000` 具体值对比 | — | grep `\b2,?340\b` | KEEP `2,340` |
| 不一致语 | — | grep `inconsisten\|conflict` | STRIP（agent 自然会写出） |

## q12 — docs/checklist_audit_report.md (upd1)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `incident_response_checklist.md` 名 | — | grep filename | KEEP |
| 4 个示例 checklist item 描述 | incident_response_checklist.md | grep ≥2 of {access log, 72 hour/GDPR, rotate, disable, root cause/PR, notification} | STRIP 具体例，引"checklist 内项" |
| 完成状态评估 | — | grep complete/incomplete | STRIP |
| `- [ ]` 字面 | — | 无强检 | STRIP |

## q14 — docs/vulnerability_introduction_trace.md (upd2, deployment_timeline首introduce)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `PR #847` | upd2 deployment_timeline.md | grep `PR\s*#?\s*847` | KEEP 字面 |
| `Oct 14, 14:32:18 UTC` | upd2 timeline | grep `Oct\w*\s+14\|2024-10-14`，`14:32` | KEEP `Oct 14` 字面 |
| 22 / 43 days | — 可推 | grep `\b22\b\|\b43\b\|\b21\b` | STRIP — agent 算 |
| `deployment_timeline.md` cite | — | grep filename | KEEP — 此轮首次引入此文件，称名 |
| `>=3 ##` | — | count | STRIP 数字 |

## q15 — analysis/compliance_timing.json (upd2)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema fields verbatim | — | json keys | KEEP |
| `2024-11-05T02:14:33Z` 示例 | upd1 log | regex `2024-11-05` | KEEP（schema 中已存） |
| `2024-11-26T16:52:00Z` | initial disclosure_report 之 11:52 EST + log | 仅检 exposure_window 480-550 | KEEP（schema 中已存） |
| `exposure_window_hours` 范围 480-550 | 计算所得 | numeric range | STRIP 具体值，agent 自计 |
| `regulatory_notification_deadline_ts` | first_exploited+72h | regex Nov 7-9 / Dec 4-6 | STRIP 数值 |
| `notification_sent_ts: TBD - upd3 pending` | — | nst 检 lenient | KEEP `TBD - upd3 pending` 字面（schema example） |
| `compliant_72h: null` | — | lenient | KEEP |

## q16 — scripts/analyze_timeline.py (upd2)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 + schema fields | — | run + dict keys | KEEP |
| 时间戳示例 (`2024-11-05T02:14:33Z`, `2024-10-14T14:32:18Z`, `2024-11-26T16:52:00Z`) | upd1 log + upd2 timeline + initial | regex `2024-11-05`, `2024-10-14`, exposure 480-550, deadline `2024-11-0[78]` | KEEP（schema example 字面） |
| `regulatory_window_hours: 72` | — | int==72 | KEEP |
| 各源文件名 | — | 无强检（仅指点） | STRIP，引"latest log 文件 + deployment 时间表" |

## q17 — docs/notification_comparison.md (upd2)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `notification_draft_v1.md` 名 | initial | grep filename | KEEP |
| 4 项缺漏（timeline, scope 2,340, framing, GDPR） | — | grep 至少 2 difference markers | STRIP 详细 enum，引"compare draft v1 vs 当前已知证据" |
| `2 specific differences` | — | count | STRIP |

## q18 — docs/YYYY-MM-DD_midterm_breach_report.md (upd2)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| YYYY-MM-DD_ prefix | — | regex | KEEP |
| `7.5` | brief | grep `\b7\.5\b` | KEEP（grep 字面） |
| `2,340` | inventory + log | grep `\b2,?340\b\|\b891\b` | KEEP |
| `891` 顾客数 | inventory | 同上 | OPTIONAL — 提到 inventory 即可，agent 自查 |
| 72h regulatory window | — | grep `72\s*hour\|72h\|GDPR` | KEEP `72` 数 |
| Nov 5..Nov 26 计算 | — | grep `\d+\s*hours\|days` | STRIP — agent 算 |
| `>=4 ##` | — | count | STRIP 具体数 |

## q20 — analysis/72h_compliance_final.json (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema fields | — | keys | KEEP |
| `2024-11-05T02:14:33Z`, `2024-12-07` 示例 | upd1 log + upd3 notification_final | regex `2024-11-05`, `2024-12-07` | KEEP（schema example） |
| `72h_limit: 72.0` | — | abs-72<0.5 | KEEP |
| `compliant: bool`, `hours_margin: float` | — | type check | KEEP type |
| 法律确认 vs 数学不一致提示 | upd3 notification_final.md | 无强检 | STRIP — 微提一笔 |

## q21 — scripts/generate_breach_summary.py (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 + JSON shape `breach_summary.{...}` | — | run + dict | KEEP `breach_summary` 键 |
| schema fields verbatim | — | dict keys | KEEP |
| 三时间戳示例 | upd 1/3 | regex `2024-11-05`, `2024-12-07`, exposure 480-550 | KEEP |
| `cvss_score: 7.5` | brief | abs-7.5<0.05 | KEEP（schema example） |
| `affected_endpoints: 1` | — | int>=1 | KEEP（schema example） |

## q22 — docs/root_cause_analysis.md (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `7.5` | brief | grep `\b7\.5\b` | KEEP |
| `GET /api/v2/pipeline-configs/{uuid}` | api_endpoint_register | grep `pipeline.config\|/api/v2` | STRIP 全字符，KEEP `pipeline-configs` 短串 |
| `PR #847` + `Oct 14` | upd2 timeline | grep `PR\s*#?\s*847\|#847\|Oct\w*\s+14` | KEEP `PR #847` 字面 |
| `@require_auth` | brief | grep `require_auth\|authentication` | KEEP `@require_auth` 字面 |
| 二重失败原因（auth gap + ?list=true） | — | 无强检（仅 auth keyword） | STRIP — 留语义 |
| `>=3 ##` | — | count | STRIP |

## q23 — analysis/breach_impact_final.json (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema verbatim | — | keys | KEEP |
| `cvss_score: 7.5`, `total_affected_records: 2340`, `exposure_hours` 范围 | 推算 | 严格 enum + 数 | KEEP example values |
| `affected_endpoints: ["GET /api/v2/pipeline-configs/{uuid}"]` | — | non-empty list | KEEP |
| enum 集 (`critical/high/medium/low`, `high/medium/low`) | — | 严格 enum | KEEP verbatim |

## q24 — docs/stakeholder_action_timeline.md (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 5 名 stakeholder 名 | USER.md | grep ≥3 of names | STRIP — 仅引"USER.md 中之核心团队"，agent 自查（但 grep 检 ≥3 names → 此 strip 风险，KEEP 至少 3 names 提示）|
| Nov 26 + Dec 7 dates | — | grep `Nov\s+26\|2024-11-26` | KEEP `Nov 26` 字面 |
| 具体动作（disabled/rotated/...） | — | grep ≥3 action verbs | STRIP — agent 自然写 |

## q26 — docs/remediation_plan.json (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema verbatim | — | keys | KEEP |
| `>=5 actions` + 5 examples | — | len>=5, fields non-empty | STRIP 具体5 examples（仅 strict schema 检 fields 非空），引"≥5 actions" |
| `estimated_completion_days: int` | — | positive int | KEEP |

## q27 — docs/YYYY-MM-DD_final_breach_report.md (upd3)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| YYYY-MM-DD_ prefix | — | regex | KEEP |
| `7.5`, `2,340`, exposure hours, `Nov 5`, `Dec 7`, `pipeline-configs` | — | 各 grep | KEEP 这些 grep 字面 |
| `>=5 ##` | — | count | STRIP 数 |
| 各 source citation | — | 无显式 grep（P-rule 之 P4 适用） | STRIP — 引"惯例 cite sources" |

---

## 总体处理总结

- **完全 STRIP 具体值之题**：q3 部分, q5 例事件, q8 12 calls/IP, q12 例 items, q14 22/43 days, q15 计算值, q17 4 缺漏, q18 计算 hours, q20 数学/法律调和, q26 5 example actions
- **保留具体值（grep 字面脆弱）**：q6 之 `2,340`/`12,000`、q8 之 `Nov 5`/`02:14`/`847`、q9/q11 之 `2,340`、q14 之 `PR #847`/`Oct 14`、q18 之 `7.5`/`2,340`/`72`、q22 之 `7.5`/`PR #847`/`@require_auth`、q24 之 `Nov 26`/`Dec 7`、q27 之 `7.5`/`2,340`/`Nov 5`/`Dec 7`/`pipeline-configs`
- **schema 字段名 verbatim 留**：q3, q10, q15, q16, q20, q21, q23, q26
- **文件名 pattern verbatim 留**：q5, q18, q27（YYYY-MM-DD_）
- **enum 值 verbatim 留**：q10 (data_sensitivity), q23 (data_sensitivity, regulatory_risk)

## 角色分配（USER.md persona casting）

- **q3, q5**：Alex 自言自语 / 给自己列单（PM 起步）— 简洁 Slack/笔记体
- **q6, q9, q11**：scope 争议 — Alex 在 #security-response 之 Discord 群 ping 的语气
- **q8**：Diego 在 Telegram 给的 log 分析后，Alex 整理 — Discord 写给团队
- **q10, q16, q21**：脚本类 — engineering Discord ("pls add", "heads up:")
- **q12**：审 checklist — Alex 自查清单口吻
- **q14, q17, q22**：技术写作 — 给 Sana/Jake 之 Discord
- **q15, q20, q23**：合规 JSON — 较 spec-style，因外部法律会读
- **q18, q27**：正式 report — PM Telegram 给 Jordan/exec
- **q24**：复盘 timeline — 内部回顾
- **q26**：remediation plan — 给 Sana/Leo 之 #security-response

## RISK 标记

- q24 grep ≥3 stakeholder names — 题中虽 STRIP 具体5名，但保留"参 USER.md 中之 4-5 名团队成员"提示，agent 当无虞
- q22 之 `pipeline-configs` 短串保留，`/api/v2/...{uuid}` 全形仅作引用，eval 已 lenient 接收

---

## v2 hardening notes

V1 在 gpt-5.4 上 ec 通过率约 95%（仅 q9 失利），过松。v2 旨在压至 ~55%。逐题应用 lever：

- **q3** (B+D)：schema JSON block 改为散文（"endpoints list, customer-data fields list, Jake's CVSS, prelim headcount, completion ratio"），逐字段名仅靠惯例 snake_case 推断。`data_types_at_risk` / `checklist_completion_pct` / `initial_scope_estimate` 名称不复出题面，agent 须自命名。Maya 之 30% 完成率为 hedged-wrong distractor。
- **q5** (C+D)：`November 26` 字面去除，植入 hedged-wrong "Jordan said maybe Nov 24-25" distractor；ISO 8601 表述软化为"machine-readable date strings"。
- **q6** (D+C)：`2,340` 与 `12,000` 字面全去（grep 字面险），引"the actual figures from the inventory and the brief"；植入 Maya 之 8K hedged-wrong 提示。
- **q8** (D)：`Nov 5` / `02:14` / `847` 全去；引 Raj 之"config-pipeline"误称作 distractor，强逼 agent 读 access_log_analysis.md。
- **q9** (D+C)：`2,340` 字面去除，`Diego` 字面去除（仅留 access_log_analysis.md 文件名）；植入 Sana 之 1,800 hedged-wrong distractor。
- **q10** (B)：schema JSON block 改散文，仅留 enum 集 verbatim。`endpoint_count` 等字段名全去出题面。
- **q11** (D+C)：`2,340` 字面去除（保 3 文件名以满 grep ≥3）；Leo 之 2,400 hedged-wrong。
- **q12** (C)：保 v1 大体；植入 Raj 之"half done"hedged distractor。
- **q14** (D+C)：`PR #847` / `Oct 14` 字面全去（agent 读 timeline 自得）；Sana 之"mid-October, 16th"hedged-wrong 误导。
- **q15** (B)：JSON block 改 bullet-list 散文，schema fields 字面均保（unconventional + 检验严）。
- **q16** (B+D)：JSON block 改散文，去除三 timestamp 示例（`2024-11-05T02:14:33Z` 等），仅留字段名。
- **q17** (C)：植入 Jake 之"draft mostly fine"hedged-wrong distractor；GDPR Article 33 名删除（仅"EU breach-notification regime"）。
- **q18** (D+A)：`7.5` / `2,340` / `72` 字面全去；P-rule 名删除；Maya 之 ~1,200 customer hedged-wrong distractor。
- **q20** (B+C)：JSON block 改 bullet 散文；保 schema 字段名 verbatim；强化 legal vs math 之困境（"两读皆可"）。
- **q21** (B)：JSON block 改 bullet 散文；schema 字段名全保（验证强）。
- **q22** (D)：`7.5` / `PR #847` / `Oct 14` 字面去除（保 `pipeline-configs` 与 `@require_auth`）；Leo 之"late-summer deploy"hedged 误导。
- **q23** (B+C)：JSON block 改散文；保字段名与 enum verbatim；植入 Maya 之 600h hedged-wrong distractor。
- **q24** (D+C)：`Nov 26` 与 `Dec 7` 字面全去；Leo 之 Nov 24 hedged-wrong 误导；强逼读 USER.md/disclosure_report。
- **q26** (C)：strict schema 全保（验证严）；植入 Priya 之"three actions enough"hedged-wrong（验证 ≥5）。
- **q27** (A+D)：P1-P5 显式标签全去（A）；`7.5` / `2,340` / `Nov 5` / `Dec 7` 字面全去（D）；保 `pipeline-configs`、`YYYY-MM-DD_`。

**预期失利目标题**（agent grep 失配概率高）：q3（schema 自命名易错→ `data_types_at_risk` 写成 `at_risk_data_types`）、q5（Nov 26 漏写）、q6（数值漏读）、q8（Nov 5/02:14/847 三 grep 任一漏即败）、q14（PR #847/Oct 14 双 grep）、q18（7.5/2,340/72 任一漏）、q22（7.5 漏）、q24（Nov 26 / 3 stakeholders）、q27（5 grep 字面 + ≥5 ##）、q3 之 hedged 30% 误导。约 9-12 题有可能失利，符合 ~55% 通过率目标。

**未触动**：无 — 二十题悉作调整（q12、q15、q26 仅轻改，因验证已严或本身够难）。

**BROKEN 风险**：低。所有 v2 删除的字面值均 workspace 可读；schema 字段（q15/q16/q20/q21/q23/q26）仍以 bullet 列示，agent 严格遵循无虞。enum 集（critical/high/medium/low）字面保留。q23/q26 strict schema 全字段名 verbatim 保留。

## v3 super-harden notes

v2 实测 ec 仅 q3、q9 失利（18/20 通过 ≈ 90%），未达预期。v3 选定 5 题（q15/q16/q21/q23/q26），重叠加杠杆 H（深度 schema obfuscation）+ C++（多重 hedged distractor）+ D++（再删字面 token），逼 agent 自创字段名。

- **q15** (H)：原 6 字段（`vulnerability_first_exploited_ts` 等）字面全删，转语义散文；`72h` / `TBD - upd3 pending` 亦删；preserved_tokens 仅余输出路径。验证脚本严验 `vulnerability_first_exploited_ts` / `exposure_window_hours` / `regulatory_notification_deadline_ts` 之 `data.get(...)`，agent 易猜成 `first_exploited_ts` / `exposure_hours` / `notification_deadline_ts` 等近义键 → 必失。植入 Sana "intake form 容忍" + Maya "field 名按规则命名" 双 hedged 诱导。
- **q16** (H+C++)：6 字段字面悉删（`exploit_first_ts` / `vulnerability_introduced_ts` / `fix_deployed_ts` / `exposure_hours` / `regulatory_window_hours` / `regulatory_deadline_ts`）转散文；植入 Leo "CI 不 pin key 名" + Priya "或许 pin 一两个" 矛盾 hedged。验证严验五字段 + `re.search` 日期，agent 极易写 `exploit_ts` / `vuln_introduced_ts` 之类 → 失。
- **q21** (H+C++)：去除 `breach_summary` 顶层 wrapper 字面 + 8 字段名（`exploit_ts` / `notify_ts` / `exposure_hours` / `compliant_72h` / `affected_endpoints` / `cvss_score` / `fix_ts` / `notification_hours`）。验证用 `data.get("breach_summary")`，agent 若用 `summary` / `breach` / `report` 顶层名则获 `None` 后 fallback to top-level，然各 field 名亦未保 → 多重 miss。Sana/Priya 矛盾 hedged 加成。
- **q23** (H+C++)：去除 7 字段名（`cvss_score` / `affected_endpoints` / `notification_compliant` / `exposure_hours` / `total_affected_records` / `data_sensitivity` / `regulatory_risk`）转散文；保 enum 字面（`critical` / `high` / `medium` / `low` 验证脚本对值非键，故仍需保字面以引导值）。植入 Maya 1,800 + Leo 3,200 双 hedged-wrong 干扰 records 数。agent 易写 `cvss` / `total_records` / `notification_complies` → 失。
- **q26** (H+C++)：去除 `remediation_actions` 顶层 + 5 子字段名（`action_id` / `description` / `owner` / `deadline` / `acceptance_criteria`）+ `estimated_completion_days`。验证脚本严验 `data.get("remediation_actions")` 与每条 action 必含五字段名，agent 极易用 `actions` / `id` / `task` / `due` / `criteria` → 失。Leo "schema 历来 loose" hedged 加诱导。

**预期增量失利**：5 题中至少 3-5 题应失（agent 字段名命名一致性与脚本验证之 strict literal-match 鸿沟难弥）。q23 留 enum 字面或 q26 因 5 行 must-have 提示仍可能蒙对部分 → 保守估计 +3 失利，激进估计 +5 失利。

**BROKEN 风险评估**：中低。
- workspace 数据完整可推（agent 若读全文档可得全数值）。
- enum 词汇 `critical/high/medium/low` 字面保留 → q23 `data_sensitivity` 值不会败于词汇。
- 所有输出路径完整保留 → `test -f` 类检查不影响。
- 唯一风险：若 agent 对 schema 字段命名极保守（如总猜 `id` / `description` 之"业界默认"），q26 命中率反偏高；但 q15/q16/q21 之多 timestamp 字段难以全猜中 → 失利近确定。
