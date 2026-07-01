# hil_f3 子计划

## 一、场景概要

**场景**：量化交易系统时区事件（赵磊 V3 策略，A 股午间休市违规）  
**核心矛盾**：C1 CI通过 vs 生产报错 / C2 告警静默掩盖 / C3 review LGTM vs 知识盲点 / C4 "首次违规"声称 vs 历史档案  
**偏好用户**：赵磊（P1 ISO时间 / P2 日期前缀命名 / P3 含TL;DR的五章节结构 / P4 代码引用含文件名+行号 / P5 结论量化精确）

## 二、Update 时机重新定位

原始 questions.json 中 update 触发位置为 q5/q8/q11/q17（按30轮纯MC设计）。  
重新设计后拉长间距，在各 update 之间留足 EC 空间：

| Update | 触发轮次 | 触发后首轮 EC | 本 Phase 总轮 |
|--------|---------|-------------|-------------|
| upd1（服务器诊断 + 小周认错） | q8 | q9 | Phase 0: q1–q7（7轮）|
| upd2（张审核正式调查） | q15 | q16 | Phase 1: q8–q14（7轮）|
| upd3（增强交易日志） | q21 | q22 | Phase 2: q15–q20（6轮）|
| upd4（小周修复方案） | q27 | q28 | Phase 3: q21–q26（6轮）|
| —— | —— | —— | Phase 4: q27–q32（6轮）|

总计：32 轮

## 三、题目序列

### Phase 0（q1–q7，基线，所有 update 前）

| ID | Type | 主题 | pref |
|----|------|------|------|
| q1 | MC | C1：CI Build #891 全通过 vs production-error-log TZ_CONVERT_ERROR，矛盾识别 | |
| q2 | MC | C2+C3：alert-rules-config rule_007 静默链 + git-pr-447-diff 第127行 review 缺失 | |
| q3 | EC/L2 | 生成 `docs/ci_test_gap_analysis.md`：CI 时区测试缺陷分析（mock 日期 2026-01-15 = 非DST期，缺失三类覆盖：DST边界/休市窗口/多日累积偏移） | |
| q4 | MC | 偏好引入（P1–P5 规则呈现轮） | |
| q5 | EC/L2 | [pref] 生成 `docs/YYYY-MM-DD_initial_analysis.md`：综合已有证据初步分析（须含 TL;DR + 时间线 + rule_007 创建背景 + 三个关键数值：127行/60分钟偏移/7天静默） | P1,P2,P3 |
| q6 | EC/L2 | 生成 `docs/incident_timeline.json`：bug 生命周期关键节点（5个字段：pr_merged / dst_switched / first_warn_silenced / near_miss_dates / violation），时间戳严格 ISO 8601 含+08:00 | |
| q7 | EC/L3 | 创建 `src/timezone_fix.py`：依据 git-pr-447-diff.md 第127行 bug 定位，自行实现 `get_cst_now()` 函数（使用 zoneinfo.ZoneInfo('Asia/Shanghai')），通过 `scripts/tests/test_timezone_fix.py` | |

### Phase 1（q8–q14，upd1 后：服务器诊断确认应用层问题，小周坦承知识盲点）

| ID | Type | 主题 | pref |
|----|------|------|------|
| q8 | MC | **[update_ids: upd1_sessions, upd1_workspace]** C1 反转：服务器诊断 OS/NTP 正常 → bug 在应用层；小周坦承"以为+8就是CST"→ 知识盲点而非范围问题 | |
| q9 | EC/L2 | [pref] 生成 `docs/review_quality_assessment.md`：评估小周 review 三维度（交易逻辑 ✓ / 时区处理 ✗ / 测试覆盖意识 ✗），须含：review 时间戳 2026-03-10T15:30 / "LGTM" 引文 / 第127行未评论的证据 | P4 |
| q10 | EC/L2 | 生成 `docs/alert_silence_impact_report.md`：量化 rule_007 影响（静默期 2026-03-10–2026-03-16，7条 TZ_CONVERT_WARN 被抑制，对应 near-miss×2 + 违规×1），说明若无静默则最早可在 2026-03-10 发现 | |
| q11 | EC/L3 | 创建 `scripts/trade_window_checker.py`：读取 `trade-execution-log.md`（agent 需解析 MD 表格），检测所有执行时间在 11:00–13:00 CST 范围内的条目（含 near-miss），输出 `analysis/trade_window_violations.json`（字段：order_id / actual_time / delta_to_close_secs / status），运行后通过 `scripts/tests/test_trade_window_checker.py` | |
| q12 | EC/L2 | 生成 `docs/server_diagnostic_interpretation.md`：解读工单 #TK-20260317-4521 的技术意义（NTP漂移<50ms + OS时区正确 → 排除环境假设，聚焦应用层），须与 production-error-log 中的 "DST offset not accounted for in schedule_trade() line 127" 互相印证 | |
| q13 | EC/L2 | 生成 `docs/two_phase_review_analysis.md`：对比小周两阶段表述（Phase 1 微信："review不是逐行深读，+8看起来没问题" → Phase 2 微信更新："以为+8就是CST，确实知识盲点"），明确区分"有意范围限定"与"知识缺失"的责任性质差异 | |
| q14 | EC/L2 | 更新 workspace 文件 `alert-rules-config.md`（在 agent workspace 中修改）：为 rule_007 添加 `expires: "2025-12-25T00:00:00+08:00"`，同时生成 `docs/rule_007_postmortem.md`（分析：原因合理但缺过期机制 → 迁移完成后未清理 → 7天延误） | |

### Phase 2（q15–q20，upd2 后：张审核坚持"首次违规"，合规追踪机制缺陷暴露）

| ID | Type | 主题 | pref |
|----|------|------|------|
| q15 | MC | **[update_ids: upd2_sessions]** C4 核实：张审核"首次违规"（正式记录始于立案）vs 2025-12-20 通知#1（存档中有，同一发件人），合规追踪机制漏洞 | |
| q16 | EC/L2 | 生成 `docs/compliance_history_comparison.md`：并排对比表（列：日期/来源/内容/正式性/系统记录状态），含通知#1（2025-12-20，非正式）和通知#3（2026-03-16，正式），论证两者关联性 | |
| q17 | EC/L3 | 创建 `scripts/compliance_timeline_builder.py`：读取 `compliance-notice.md`，提取所有通知条目，输出 `analysis/compliance_events.json`（字段：notice_id / date / sender / formal_status / related_strategy），运行后通过 `scripts/tests/test_compliance_timeline.py` | |
| q18 | EC/L2 | 生成 `docs/system_accountability_gaps.md`：识别两处系统性追踪漏洞（①非正式警告不入档 → 允许同类问题重演；②告警静默规则无过期机制 → 迁移后风险遗留），每处含：现象描述 + 根因 + 本次事件中的体现 + 改进建议 | |
| q19 | EC/L2 | 生成 `docs/compliance_response_draft.md`：赵磊整改方案草稿（对应 upd2 session 中最终提交内容：①代码修复②12个DST测试③清理rule_007④根因报告），格式符合张审核要求（含事件时间线/根因/影响范围/整改措施四节），须量化：12个测试用例 / rule_007删除 / PR#447修复 | |
| q20 | EC/L2 | 生成 `analysis/risk_window_stats.json`：统计 trade-execution-log 中 post-DST 区间（2026-03-10–2026-03-16）的风险数据（字段：total_trades / filled_but_anomalous / near_miss_count / rejected_count / min_margin_to_close_secs），须与 production-error-log 数值吻合 | |

### Phase 3（q21–q26，upd3 后：增强交易日志，near-miss 渐进模式）

| ID | Type | 主题 | pref |
|----|------|------|------|
| q21 | MC | **[update_ids: upd3_workspace]** Near-miss 渐进收窄（Mar 10: 13s → Mar 11: 7s → Mar 16: 越界5s），"如何从增强日志中看出风险递进" | |
| q22 | EC/L2 | 生成 `docs/near_miss_risk_report.md`：量化3笔post-DST异常（含精确秒数：13s/7s/5s + 各自日期），分析收窄趋势，计算如无rule_007静默可提前多少天发现（答案：7天，即2026-03-10） | |
| q23 | EC/L3 | 创建 `scripts/generate_audit_summary.py`：综合读取 `production-error-log.md` + `trade-execution-log-enhanced.md`（均为 MD 格式，需解析），输出 `analysis/audit_summary.json`（字段：total_trades / silenced_warnings / near_miss_count / violation_count / max_delta_seconds / first_anomaly_date），通过 `scripts/tests/test_audit_summary.py`（验证 near_miss_count=2, violation_count=1, silenced_warnings=5） | |
| q24 | EC/L2 | 生成 `docs/root_cause_analysis.md`：六维根因分析（①代码缺陷 line 127 ②测试覆盖 mock 2026-01-15 ③告警静默 rule_007 ④review 知识盲点 ⑤合规追踪漏洞 ⑥风险递进未识别），每维度含：现象/证据/影响/修复建议，须含数值 127 / 2026-01-15 / 7天 / 60分钟 | |
| q25 | EC/L2 | 生成 `docs/ci_remediation_tests.md`：设计三类补充测试方案（DST边界 / 休市窗口 / 多日累积），每类含：测试场景描述 + 具体 mock 日期（须覆盖 2026-03-10 即 DST后期） + 预期行为，须参照 ci-build-report.md 中现有 test_utc_to_cst_basic 的格式 | |
| q26 | EC/L2 | 创建 `tests/test_ci_edge_cases.py`：基于 q25 的方案编写实际测试代码，至少包含 3 个参数化测试用例（非DST/DST/休市边界各一个），注意此时 src/timezone_fix.py 由 q7 已创建，测试须对该文件写的函数进行验证，运行 `pytest tests/test_ci_edge_cases.py -q` 全部通过 | |

### Phase 4（q27–q32，upd4 后：综合收尾）

| ID | Type | 主题 | pref |
|----|------|------|------|
| q27 | MC | **[update_ids: upd4_sessions, upd4_workspace]** 小周方案与机构案例：确认 zoneinfo 为行业标准，评估 q7 中 agent 自行实现的修复与小周方案的一致性 | |
| q28 | EC/L3 | 基于 xiaozhou-timezone-fix.md，补全 `tests/test_timezone_parametrized.py`（3个参数化用例覆盖：非DST期2026-01-15 / DST期2026-03-10 / DST结束后2026-11-02），同时完善 `src/timezone_fix.py` 使其通过新测试，运行 `pytest tests/test_timezone_parametrized.py -q` 全部通过 | |
| q29 | EC/L2 | 生成 `docs/remediation_plan.json`：6项行动计划（每项含 action_id/title/owner/deadline/acceptance_criteria），三项必须包含：①rule_007删除（含验证条件：grep rule_007 在更新后配置中不存在）②DST测试覆盖（含：12个用例，覆盖三类）③合规非正式追踪改进（含：入档机制建立） | |
| q30 | EC/L2 | 生成 `docs/stakeholder_accountability_matrix.json`：4个角色（zhaolei_coder/xiaozhou_reviewer/zhaolei_rule_creator/zhang_compliance），每角色含 role/direct_contribution/indirect_contribution/recommended_action，须区分赵磊的双重角色（代码作者 vs 规则创建者） | |
| q31 | EC/L2 | 生成最终报告 `docs/YYYY-MM-DD_v3_incident_report_final.md`（YYYY-MM-DD 用实际日期），须同时满足 P1–P5 全量偏好（eval.command 直接跑 check_preferences.py --rules P1,P2,P3,P4,P5），报告须含：TL;DR / 时间线表格（含所有关键时间戳） / 矛盾点汇总（C1–C4）/ 六维根因 / 6项补救清单 | |
| q32 | MC | 元认知收尾：基于所有证据，哪些最初假设需要修正（测试环境差异假设 / review 范围有限假设 / 首次违规声称）；哪个信息源最后被证明最可靠 | |

## 四、分布统计

| 指标 | 数值 |
|------|------|
| 总轮次 | 32 |
| MC | 9 轮（q1/q2/q4/q8/q15/q21/q27/q29/q32 → 实为 q1/q2/q4/q8/q15/q21/q27/q32 = 8轮，加上 q29 共 9轮*）|
| EC | 23 轮 |
| EC 比例 | 71.9% |
| 含 pref 的 EC 题 | q5/q9 共 2 题（Phase 0–1，教学期） |
| 偏好计入 eval 的 EC 题 | q31（P1–P5 全量，计分） |
| Update 间距 | Phase 0: 7轮 / Phase 1: 7轮 / Phase 2: 6轮 / Phase 3: 6轮 / Phase 4: 6轮 |

*注：q29 是 EC 题（生成 remediation_plan.json），不是 MC，上表订正：MC = q1/q2/q4/q8/q15/q21/q27/q32 = 8轮；EC = 24轮；EC比例 = 75%。

## 五、脚本清单

| 脚本 | 用于 | 核心逻辑 |
|------|------|---------|
| check_ci_gap.py | q3 | 含 "2026-01-15" + "DST" + 三类缺陷关键词（DST/休市/累积） |
| check_preferences.py | q5,q9,q31 | P1–P5 通用偏好检查 |
| check_initial_analysis.py | q5 | 含 "127" + "60" + "rule_007" + TL;DR 标题 |
| check_timeline_json.py | q6 | JSON 含 5 个必须字段，时间戳 ISO 8601 含+08:00 |
| check_review_assessment.py | q9 | 含 "15:30" + "LGTM" + 三维度标题 |
| check_alert_impact.py | q10 | 含数字 7 / 2 / 1 + "rule_007" |
| check_window_violations.py | q11 | JSON ≥3 条目，含 near_miss 标记字段 |
| check_diagnostic_interp.py | q12 | 含工单号 + "line 127" + "应用层"或"application" |
| check_review_phases.py | q13 | 含两段引文关键词 + "知识" 或 "知识盲点" |
| check_rule_update.py | q14 | alert-rules-config.md 含 "2025-12-25" + rule_007_postmortem.md 存在且含"过期" |
| check_compliance_comparison.py | q16 | 含 "2025-12-20" + 对比表格标记 + "非正式" |
| check_compliance_timeline.py | q17 | JSON 含 2 条目，formal_status 字段区分 |
| check_accountability_gaps.py | q18 | 含两处漏洞关键词 + 各自改进建议 |
| check_compliance_response.py | q19 | 含 "12" + "rule_007" + 四节结构标题 |
| check_risk_stats.py | q20 | JSON 字段值：near_miss_count=2 / rejected_count=1 / min_margin=7 |
| check_near_miss_report.py | q22 | 含 "13" + "7" + "5" + 三个对应日期 |
| check_audit_summary.py | q23 | JSON: near_miss_count=2 / violation_count=1 / silenced_warnings=5 |
| check_rca.py | q24 | 含六维度关键词 + "127" + "2026-01-15" + "7" |
| check_remediation_schema.py | q29 | schema 验证 + rule_007/DST/合规三项必须存在 |
| check_accountability_matrix.py | q30 | 含4角色 + 每角色 recommended_action |
| check_final_report.py | q31 | 含 rule_007 + 127 + near-miss 数值 + 6项行动标题 |
| schemas/timeline_schema.json | q6 | JSON Schema |
| schemas/remediation_schema.json | q29 | JSON Schema |
| tests/test_timezone_fix.py | q7 | 测试 get_cst_now() 返回 timezone-aware datetime，Asia/Shanghai |
| tests/test_trade_window_checker.py | q11 | 验证输出 JSON 含正确条目数和字段 |
| tests/test_compliance_timeline.py | q17 | 验证输出 JSON 结构 |
| tests/test_audit_summary.py | q23 | 验证 near_miss=2 / violation=1 / silenced=5 |
| tests/test_timezone_parametrized.py | q28 | 3个参数化用例（由 agent 编写，但 test 文件由我们预写） |

## 六、关键 ground truth 数值速查

| 数值 | 来源 | 用于脚本 |
|------|------|---------|
| 第127行 | git-pr-447-diff.md | check_ci_gap / check_rca / check_final_report |
| 2026-03-10T16:45:00+08:00（PR合并） | git-pr-447-diff.md | check_timeline_json |
| 2026-03-08（DST切换） | trade-execution-log.md | check_timeline_json |
| 2026-03-10T03:29:45（首次WARN） | production-error-log.md | check_timeline_json / check_alert_impact |
| 60分钟（统一偏移量） | production-error-log.md | check_initial_analysis / check_rca |
| rule_007 创建 2025-12-15 | alert-rules-config.md | check_rule_update |
| 5条 SILENCED / 7条 WARN | production-error-log.md | check_alert_impact / check_audit_summary |
| near-miss: 13s / 7s（Mar 10/11） | trade-execution-log-enhanced.md（upd3） | check_near_miss_report / check_risk_stats |
| 违规: 5s（Mar 16） | production-error-log.md | check_near_miss_report |
| 2025-12-20（非正式合规提醒） | compliance-notice.md | check_compliance_comparison |
| Build #891, 34/34, 78% 覆盖率 | ci-build-report.md | check_ci_gap |
| mock日期 2026-01-15 | ci-build-report.md | check_ci_gap / check_rca |
| #TK-20260317-4521（工单号） | server-diagnostic-report.md（upd1） | check_diagnostic_interp |
| 2026-03-23（诊断日期） | server-diagnostic-report.md（upd1） | check_diagnostic_interp |
| 整改方案含12个测试 | upd2 sessions | check_compliance_response |
