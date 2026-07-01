# BRIEF: eng3 — SRE 生产事故复盘（Postmortem）

## 场景叙事背景

某中型 SaaS 公司（化名 "ArcNode"）的 SRE 团队负责维护一套边缘代理服务，其架构与技术栈与 Cloudflare 高度相似。2024 年 6 月 20 日，该团队经历了一次由两个独立事件交织引发的严重生产事故：一条新部署的 DDoS 缓解规则触发了速率限制器中的潜在 Lua 代码缺陷，导致大量边缘节点进程中毒，同期一次骨干网拥塞事件触发了流量管理器（Traffic Manager）的二次故障。事故持续 114 分钟，峰值时段 2.1% 的 CDN HTTP 请求收到错误响应，99 百分位 TTFB 延迟上升至正常值的 3 倍。

Agent 扮演此次事故的 **主责 SRE**，需要：
- 整理并维护事故时间线（含两条独立因果链）
- 计算 SLA 积分影响
- 编写符合公司模板的 postmortem 报告
- 管理多渠道（Slack / 飞书 / Email）对外通报
- 跟踪并更新 corrective action 列表

整个过程跨越 2 个 update（含 1 次 supersede），共 17 个 exec_check 轮次，考察信息整合、数值闭合、preference 遵守及真实锚点引用能力。

---

## 真实来源链接表

| # | 来源 | URL | 类型 |
|---|------|-----|------|
| S1 | Cloudflare Incident June 20 2024 | https://blog.cloudflare.com/cloudflare-incident-on-june-20-2024/ | official postmortem |
| S2 | Cloudflare Incident October 30 2023 | https://blog.cloudflare.com/cloudflare-incident-on-october-30-2023/ | official postmortem |
| S3 | Cloudflare Thanksgiving 2023 Security Incident | https://blog.cloudflare.com/thanksgiving-2023-security-incident/ | official postmortem |
| S4 | Cloudflare November 14 2024 Log Loss | https://blog.cloudflare.com/cloudflare-incident-on-november-14-2024-resulting-in-lost-logs/ | official postmortem |
| S5 | Cloudflare Business SLA | https://www.cloudflare.com/business-sla/ | official SLA doc |
| S6 | GitHub Availability Report April 2024 | https://github.blog/news-insights/company-news/github-availability-report-april-2024/ | official postmortem |
| S7 | GitHub Availability Report August 2024 | https://github.blog/news-insights/company-news/github-availability-report-august-2024/ | official postmortem |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|----------|------|
| incident_start_utc | 2024-06-20T17:47:00Z | S1 | 首个进程中毒时刻 |
| incident_end_utc | 2024-06-20T19:27:00Z | S1 | 错误率回归基线 |
| duration_minutes | 100 | S1 | 17:47→19:27 = 100 min（场景内取整，允许 ±2） |
| ddos_rule_deploy_start_utc | 2024-06-20T14:14:00Z | S1 | DDoS 规则开始渐进部署 |
| ddos_rule_deploy_end_utc | 2024-06-20T17:06:00Z | S1 | DDoS 规则全局部署完成 |
| peak_error_rate_cdn_pct | 2.1 | S1 | CDN HTTP 请求错误峰值百分比 |
| peak_5xx_pct | 3.45 | S1 | 含源站错误的总 5xx 峰值百分比 |
| ttfb_p99_multiplier | 3 | S1 | 99 百分位 TTFB 相对正常值倍数 |
| europe_west_capacity_loss_pct | 10 | S1 | 西欧 HTTP 处理能力损失百分比 |
| europe_east_capacity_loss_pct | 4 | S1 | 东欧 HTTP 处理能力损失百分比 |
| backbone_congestion_window_utc | 2024-06-20T17:33:00Z / 2024-06-20T17:50:00Z | S1 | 骨干网拥塞起止 |
| traffic_manager_bug_trigger_utc | 2024-06-20T18:17:00Z | S1 | Traffic Manager 潜在 bug 首次触发 |
| ddos_rule_disabled_utc | 2024-06-20T19:34:00Z | S1 | DDoS 规则全局禁用 |
| lua_buggy_func_1 | get_cookie_key | S1 | 含无限递归的 Lua 函数名 |
| lua_buggy_func_2 | has_valid_cookie_broken | S1 | 与前序校验不一致的 cookie 验证函数名 |
| lua_recursive_func | parent_key_generator | S1 | 自引用导致无限 tail-call 的生成器函数 |
| sla_credit_formula | (Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes | S5 | Cloudflare Business SLA 积分计算公式 |
| sla_claim_deadline_days | 5 | S5 | 事故后提交 SLA 申领的最大工作日数 |
| oct30_incident_start_utc | 2023-10-30T19:54:00Z | S2 | Oct 30 事故对比参考：影响开始 |
| oct30_duration_minutes | 37 | S2 | Oct 30 事故持续时长 |
| oct30_root_cause_component | Workers KV deployment tool | S2 | Oct 30 事故根因组件 |
| github_apr_incident1_start_utc | 2024-04-05T08:11:00Z | S6 | GitHub Apr 事故对比参考 |
| github_apr_incident1_actions_failed | 100000 | S6 | GitHub Apr 事故失败 Actions workflow 数量 |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── postmortem/
│   ├── TEMPLATE.md              # 公司 postmortem 模板，含所有必填章节（~3k tokens）
│   ├── DRAFT_v0.md              # 初始草稿（部分填充，含刻意失真的 bot 摘要区块，~8k tokens）
│   └── FINAL.md                 # Agent 最终产出（不预填）
├── timeline/
│   ├── raw_alerts.jsonl         # 原始告警日志 250 条（JSONL，时间戳+组件+message，~15k tokens）
│   ├── backbone_events.jsonl    # 骨干网拥塞事件日志 80 条（~5k tokens）
│   └── traffic_manager_log.jsonl # Traffic Manager 路由操作日志 120 条（~8k tokens）
├── metrics/
│   ├── cdn_error_rates.csv      # 每分钟 CDN 错误率（17:00-21:00，240 行，~6k tokens）
│   ├── ttfb_p99.csv             # 每分钟 99pct TTFB（~5k tokens）
│   ├── region_capacity.csv      # 各区域容量损失百分比（~3k tokens）
│   └── 5xx_breakdown.csv        # 5xx 错误分类明细（~4k tokens）
├── code/
│   ├── rate_limit/
│   │   ├── rule_engine_v1.lua   # 旧版速率限制引擎（含 bug 函数，~3k tokens）
│   │   ├── rule_engine_v2.lua   # 新版引擎（update 后注入，~3k tokens）
│   │   └── ddos_rule_20240620.yaml  # 触发事故的 DDoS 规则配置（~1k tokens）
│   └── traffic_manager/
│       ├── router.go            # Traffic Manager 路由逻辑（~5k tokens）
│       └── router_fix.patch     # 修复 patch（update 后注入，~2k tokens）
├── sla/
│   ├── business_sla.md          # 公司 SLA 条款（基于 Cloudflare Business SLA 合成，~4k tokens）
│   ├── affected_customers.csv   # 受影响客户列表（1000 行，含 plan/region/impact，~15k tokens）
│   └── credit_calculation.py    # SLA 积分计算脚本模板（~2k tokens）
├── runbook/
│   ├── incident_response.md     # 事故响应 runbook（~5k tokens）
│   ├── escalation_matrix.md     # 升级矩阵（~2k tokens）
│   └── break_glass.md           # 紧急操作手册（~2k tokens）
├── corrective_actions/
│   ├── action_items_v1.json     # 初始 corrective actions（7 条，含截止日期/负责人，~3k tokens）
│   └── action_items_v2.json     # Update 后修订版（update_2 注入，~3k tokens）
├── communications/
│   ├── slack_history.jsonl      # #incidents 频道完整消息历史（300 条，~20k tokens）
│   ├── feishu_dm.jsonl          # 飞书 DM 记录（主责 SRE 与 EM 对话，150 条，~8k tokens）
│   ├── feishu_group.jsonl       # 飞书事故群消息（200 条，~12k tokens）
│   ├── email_thread.eml         # 对外客户通报邮件线程（~5k tokens）
│   └── discord_sre_channel.jsonl # SRE 内部 Discord 频道（100 条，~5k tokens）
├── comparison/
│   ├── oct30_2023_postmortem.md # Oct 30 2023 参考 postmortem（真实事故改写，~8k tokens）
│   └── similar_incidents.md     # 行业类似事故对比分析（~4k tokens）
└── archive/
    ├── LEGACY_rate_limit_v0.lua # 废弃旧版引擎（V6 红鲱鱼，标注废弃但内容与当前事故无关）
    └── DRAFT_postmortem_bot_summary.md  # V5 失真 bot 自动摘要（刻意错误：把 2.1% 写成 0.21%，把 100 min 写成 37 min）
```

**体量估算合计：** ~150k tokens（远超 100k 要求）
- 日志类文件（alerts + backbone + TM + slack + feishu）：约 70k tokens
- CSV 指标数据：约 18k tokens
- 文档与代码：约 35k tokens
- 通信历史：约 27k tokens

---

## Session 清单（4-6 个 Session）

| Session ID | 类型 | 参与者 | 内容概要 |
|-----------|------|--------|----------|
| session_main | 主会话 | Agent（SRE on-call）| 执行全部 17 轮任务，操作 workspace 文件 |
| session_slack_incidents | Slack #incidents 频道 | SRE团队 + EM + Platform Eng | 事故实时响应消息，含 tool call 痕迹（/page oncall、bot alert 推送） |
| session_feishu_dm | 飞书 DM | SRE（Agent）+ EM（张磊） | EM 私信催进度、注入 preference（"postmortem 必须用中英双语小标题"） |
| session_feishu_group | 飞书「事故复盘群」| SRE团队全员 | 初始摘要发布、数据讨论，含一条故意失真的 bot 自动摘要（V5 诱饵） |
| session_email | Email 线程 | SRE + Customer Success + 外部客户 | 对外通报模板，含 SLA 积分申请截止日期信息 |
| session_discord | Discord #sre-internal | SRE + Infra Eng | 技术讨论，含 corrective action 分配争议（update_2 撤销部分内容的来源） |

---

## 15-17 轮 exec_check 概要

> 格式：**Q{N}** | 目标意图 | 产物文件 | check 锚点 | 难度向量 | 涉及 update/preference

**Q1** | 解析 raw_alerts.jsonl，识别首个进程中毒事件，写出事故开始时间戳 |
产物：`output/q01_incident_start.json` { "incident_start_utc": "...", "component": "..." } |
check：字段 incident_start_utc == "2024-06-20T17:47:00Z" ±60s，component 含 "rate-limit" 或 "lua" |
向量：V4（后续轮次闭合基础）| preference P1

**Q2** | 从 backbone_events.jsonl 提取骨干网拥塞时间窗口，写入时间轴文件 |
产物：`output/q02_backbone_window.json` { "start": "...", "end": "...", "duration_seconds": N } |
check：start == "2024-06-20T17:33:00Z" ±60s，end == "2024-06-20T17:50:00Z" ±60s，duration_seconds ∈ [900, 1100] |
向量：V4 | preference P1

**Q3** | 分析 cdn_error_rates.csv，找出峰值错误率及发生时间，写入指标摘要 |
产物：`output/q03_peak_metrics.json` { "peak_cdn_error_pct": F, "peak_5xx_pct": F, "peak_time_utc": "...", "ttfb_p99_multiplier": N } |
check：peak_cdn_error_pct ∈ [2.0, 2.2]，peak_5xx_pct ∈ [3.4, 3.5]，ttfb_p99_multiplier == 3 |
向量：V8（schema-by-shape 精确值）| preference P2

**Q4** | 对比 DRAFT_postmortem_bot_summary.md 与原始日志，标出失真项并记录 |
产物：`output/q04_honeybot_discrepancies.json` { "discrepancies": [{ "field": "...", "bot_value": "...", "correct_value": "...", "source": "..." }] } |
check：discrepancies 中必须含 error_rate 失真（0.21 vs 2.1）和 duration 失真（37 vs 100），各附正确来源字段 |
向量：V5（失真摘要诱饵）

**Q5** | 识别并拒绝使用 archive/LEGACY_rate_limit_v0.lua，从 rate_limit/rule_engine_v1.lua 提取两个 bug 函数名 |
产物：`output/q05_buggy_functions.json` { "functions": ["...", "..."], "source_file": "...", "rejected_file": "..." } |
check：functions 包含 "get_cookie_key" 和 "has_valid_cookie_broken"，source_file 路径含 "rule_engine_v1"，rejected_file 路径含 "LEGACY" |
向量：V6（废弃副本红鲱鱼）| V9（真实字段 verbatim 引用）

**Q6** | 计算事故总持续时长（分钟），写入分析文件，需与 Q1 输出时间戳闭合 |
产物：`output/q06_duration.json` { "start_utc": "...", "end_utc": "...", "duration_minutes": N } |
check：duration_minutes ∈ [98, 102]，start_utc 与 q01 一致（±0 偏差），end_utc == "2024-06-20T19:27:00Z" ±60s |
向量：V4（跨轮闭合 Q1→Q6）

**Q7** | 基于 region_capacity.csv 提取各区域容量损失，写区域影响摘要 |
产物：`output/q07_region_impact.json` { "western_europe_loss_pct": F, "eastern_europe_loss_pct": F } |
check：western_europe_loss_pct == 10.0 ±0.1，eastern_europe_loss_pct == 4.0 ±0.1 |
向量：V8 | preference P2

**Q8** | 填写 postmortem DRAFT，完成 Root Cause 章节（须精确引用 Lua 函数名和 DDoS 规则部署时间戳）|
产物：`postmortem/DRAFT_v1.md`（在 DRAFT_v0 基础上编辑）|
check：文件含 "get_cookie_key"、"has_valid_cookie_broken"、"parent_key_generator"，含 "14:14" 和 "17:06" 时间戳，含 "tail call" 或 "tail-call" 关键词 |
向量：V9（verbatim 引用）| preference P3（中英双语小标题）

**Q9** | 使用 SLA 公式计算当月积分额度，写入计算结果文件（*Update 1 注入客户数量数据后方可执行*）|
产物：`output/q09_sla_credit.json` { "formula": "...", "outage_minutes": N, "affected_customer_ratio": F, "scheduled_minutes": N, "credit_ratio": F } |
check：formula 字段逐字包含 "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"，credit_ratio 数值与 (outage_minutes * affected_customer_ratio / scheduled_minutes) 误差 <0.001 |
向量：V9（SLA 条款 verbatim）| V8（精确计算验证）| UPDATE_1

**Q10** | 整理两条独立故障链（DDoS 规则链 vs. 骨干网拥塞链），写因果链 JSON |
产物：`output/q10_causal_chains.json` { "chain_1": { "trigger": "...", "mechanism": "...", "impact": "..." }, "chain_2": { ... } } |
check：chain_1.trigger 含 "DDoS rule"，mechanism 含 "Lua" 或 "tail call"，chain_2.trigger 含 "backbone" 或 "congestion"，chain_2 对应 17:33-17:50 时间窗 |
向量：V1（多源信息冲突综合，需区分两条链）

**Q11** | 从 corrective_actions/action_items_v1.json 提取所有行动项，按优先级排序并写入跟踪表（*Update 1 后*）|
产物：`output/q11_actions_tracker.csv`（columns: id, priority, owner, deadline, status, source_doc）|
check：行数 >= 7，包含 "rate-limit modernization"、"staging rollout"、"execution time limit" 三项，deadline 格式 YYYY-MM-DD |
向量：V3（隐式 preference：deadline 格式）| UPDATE_1

**Q12** | 起草对外客户通报邮件（使用 email_thread.eml 模板）|
产物：`communications/customer_notice_draft.md` |
check：含 "2024-06-20"，含 "100 minutes" 或 "1 hour 40 minutes"，不含 bot 摘要的错误数值（0.21%），含 SLA 申领截止说明（5 business days）|
向量：V5（排斥失真 bot 数据）| V4（与 Q6 时长一致）| preference P4

**Q13** | 基于 update_2 修订后的 action_items_v2.json，更新跟踪表，并标记被 supersede 的行动项（*Update 2 注入后*）|
产物：`output/q13_actions_tracker_v2.csv`（新增 superseded_by 列）|
check：存在 superseded_by 非空的行（对应 update_2 中被撤销的 "manual-restart" 行动项），新增项包含 "automated-restart-watchdog"，总行数正确 |
向量：V10（supersede 辨别）| UPDATE_2

**Q14** | 撰写 Timeline 章节（须与 Q1/Q2/Q6 输出数值零漂移），插入 DRAFT_v1.md 的对应章节 |
产物：`postmortem/DRAFT_v2.md` |
check：文件含 "17:47"、"17:33"、"17:50"、"18:04"、"19:27"、"19:34" 六个时间点，每个时间点前后有对应事件描述；检查与 q01/q02/q06 JSON 数值一致（脚本读取 JSON 交叉验证）|
向量：V4（跨轮数值闭合，5 轮闭合链路）

**Q15** | 从 slack_history.jsonl 和 feishu_group.jsonl 中识别并提取所有 on-call 升级操作记录 |
产物：`output/q15_escalations.json` { "escalations": [{ "channel": "...", "time_utc": "...", "from": "...", "to": "...", "method": "..." }] } |
check：escalations 数组长度 >= 3，包含至少 1 条 slack 和 1 条 feishu 来源，method 字段须为 "page"/"dm"/"alert" 之一 |
向量：V1（多渠道信息综合）| preference P5

**Q16** | 运行 sign-off 校验脚本，将最终版 postmortem DRAFT 内容 sha256 摘要写入 sign-off 文件 |
产物：`output/q16_signoff.txt` 内容格式：`VERIFIED:<sha256sum of postmortem/FINAL.md>` |
check：文件以 "VERIFIED:" 开头，冒号后为 64 字符小写十六进制，且与 `sha256sum postmortem/FINAL.md` 实际输出一致 |
向量：V7（Bash-sha256 sign-off token，必须实际运行）

**Q17** | 将 postmortem DRAFT_v2.md 升级为 FINAL.md，补全 Lessons Learned 和 Corrective Actions 章节，确保与 Q13 跟踪表一致 |
产物：`postmortem/FINAL.md` |
check：文件行数 >= 80，含 "get_cookie_key"、"parent_key_generator"、"2024-06-20T17:47"、SLA 公式精确文本、"2024-06-20T19:27"；superseded 行动项在 FINAL 中标注 "~~" 删除线 |
向量：V9（verbatim 引用）| V4（终轮闭合）| preference P3

---

## Update 设计

### Update 1（注入时机：Q8 完成后，Q9 执行前）
**触发时机：** 主会话第 9 轮前注入。

**内容组成（>30k tokens）：**
1. `sla/affected_customers.csv`（更新版，1200 行，含 plan/region/impact/unique_visitor_flag，~18k tokens）—— 提供受影响客户比率计算所需数据
2. `corrective_actions/action_items_v1.json`（完整版，7 条行动项，含 deadline/owner，~3k tokens）
3. `communications/customer_success_brief.md`（CS 团队要求更新对外通报的说明，~2k tokens）
4. Slack 补充消息 30 条（含 SLA 申领流程讨论，~5k tokens）
5. 飞书群补充消息 20 条（EM 明确 postmortem 要求中英双语小标题 preference，~4k tokens）

**对后续轮次的影响：**
- Q9 必须使用新注入的 affected_customers.csv 中的 affected_customer_ratio 才能正确计算 SLA 积分
- Q11 可以拿到完整 corrective actions 列表
- preference P3（中英双语小标题）从此轮飞书消息中明确注入

---

### Update 2（注入时机：Q12 完成后，Q13 执行前）—— 含 Supersede
**触发时机：** 主会话第 13 轮前注入。

**内容组成（>30k tokens）：**
1. `corrective_actions/action_items_v2.json`（修订版，~3k tokens）—— **Supersede 核心**：将 Update 1 中的行动项 CA-003 "手动重启受影响节点（manual-restart-procedure）"废弃，替换为 CA-003-revised "自动重启 watchdog 服务（automated-restart-watchdog）"，并将截止日期从 2024-07-15 改为 2024-07-31
2. `code/rate_limit/rule_engine_v2.lua`（新版引擎，修复了 bug 函数，~3k tokens）
3. `code/traffic_manager/router_fix.patch`（Traffic Manager 修复 patch，~2k tokens）
4. Discord #sre-internal 补充消息 60 条（含 CA-003 废弃讨论，~8k tokens）
5. 飞书群补充消息 30 条（~5k tokens）
6. 新的指标数据 `metrics/post_incident_metrics.csv`（事故后 48 小时监控，~10k tokens）

**Supersede 考察：**
- Agent 必须识别 action_items_v2.json 中的 superseded_by 字段（CA-003 → CA-003-revised）
- Q13 的 actions_tracker_v2.csv 必须正确标注 CA-003 被废弃，而非叠加
- Q17 的 FINAL.md 必须使用 CA-003-revised 的描述，CA-003 加删除线

---

## 4-5 条 Preference

| ID | 内容 | 注入方式 | 考察轮次 |
|----|------|----------|----------|
| P1 | 所有时间戳统一使用 ISO 8601 UTC 格式（`YYYY-MM-DDTHH:MM:SSZ`），不接受其他格式 | Q1 任务说明显式注入 | Q1-Q2-Q6-Q14 静默考察 |
| P2 | 数值字段保留两位小数（如 2.10 而非 2.1），percentage 字段单位注释为 `"unit": "percent"` | Q3 feedback 注入 | Q3-Q7-Q9 静默考察 |
| P3 | Postmortem 文档小标题格式：`## Section Name / 章节名称`（中英双语，斜杠分隔） | Update 1 飞书群消息明确注入 | Q8-Q14-Q17 考察 |
| P4 | 对外通报邮件正文须包含 `[ArcNode Status]` 前缀标签，正文结尾固定引用 SLA 申领链接 | session_email 模板中隐含，Q12 首次显式考察 | Q12 |
| P5 | JSON 输出文件须包含顶层 `"generated_at"` 字段（ISO 8601 UTC），且文件名后缀用 snake_case | session_slack 隐含（bot 输出示例），Q11 feedback 注入 | Q11-Q13-Q15 静默考察 |

---

## 难度向量绑定汇总

| 向量 | 描述 | 绑定轮次 |
|------|------|----------|
| V1 | 多源信息冲突综合 | Q10（两条因果链区分）、Q15（多渠道升级记录） |
| V2 | 动态 update 反转 | Q9（update_1 注入后正确 affected_ratio 改变）、Q13（update_2 撤销 CA-003） |
| V3 | 隐式 preference 静默考察 | Q11（deadline 格式）、Q15（JSON 字段格式） |
| V4 | 跨轮数值/事实闭合 | Q1→Q6→Q14（时间戳链）、Q3→Q12（错误率一致）、Q6→Q17（终轮闭合） |
| V5 | 失真自动摘要诱饵 | Q4（识别失真）、Q12（排斥失真数据） |
| V6 | 废弃副本红鲱鱼 | Q5（必须使用 rule_engine_v1 而非 LEGACY） |
| V7 | Bash-sha256 sign-off | Q16（终轮必须实际运行 sha256sum） |
| V8 | schema-by-shape 严格 check | Q3（精确数值）、Q7（容差校验）、Q9（计算核验） |
| V9 | 真实来源字段 verbatim 引用 | Q5（Lua 函数名）、Q8（时间戳+函数名）、Q9（SLA 公式）、Q17（终轮综合） |
| V10 | supersede 辨别 | Q13（CA-003 废弃标注）、Q17（FINAL 中删除线处理） |

---

## 拆分建议

素材已非常丰富，可拆分为两个独立场景：
- **eng3-a（主场景）**：Cloudflare June 20 2024 事故复盘，侧重双因果链分析 + postmortem 撰写 + SLA 计算（如上方案）
- **eng3-b（备选）**：SRE 多事故对比分析（Oct 30 2023 + Nov 14 2024 + GitHub Apr 2024），侧重跨事故 pattern 识别 + 预防措施优先级排序

当前选择保留 eng3 为单一场景，素材体量已超过 150k tokens，无需强制拆分。
