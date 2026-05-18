# hil_f3 设计笔记

## 一、已知确定数值（所有 EC 题的 ground truth 来源）

### Workspace 初始文件数值

**git-pr-447-diff.md**
- PR 合并时间：2026-03-10T16:45:00+08:00
- Bug 行号：第 127 行，`schedule_time = datetime.utcnow() + timedelta(hours=8)`
- 小周 review 时间：2026-03-10T15:30:00+08:00
- 小周评语包含关键词：LGTM, 无针对第127行的评论

**ci-build-report.md**
- Build 编号：#891
- 构建时间：2026-03-10T17:00:12+08:00
- 通过/总数：34/34
- 行覆盖率：78%，分支覆盖率：65%
- 时区模块覆盖率：71% 行 / 55% 分支
- 关键时区测试 mock：`datetime(2026, 1, 15, 10, 0, 0)`（固定 1 月 15 日，非 DST 期间）

**production-error-log.md**
- DST 切换日：2026-03-08（US DST 开始）
- 首次 TZ_CONVERT_WARN：2026-03-10T03:29:45+08:00
- 统一时间偏移量：+60 分钟（一致性）
- 5 条 SILENCED by rule_007 记录
- 被拒绝交易：V3-20260316-001，11:30:05 CST，超界 5 秒
- Near-miss 记录：
  - Mar 10 11:29:47 → 距休市边界 13 秒
  - Mar 11 11:29:53 → 距休市边界 7 秒
- 总日志条目：52，ERROR 级别：3，WARN 级别：7，SILENCED：5

**alert-rules-config.md**
- rule_007 创建时间：2025-12-15T14:22:00+08:00
- rule_007 创建者：zhaolei
- rule_007 匹配模式：TZ_CONVERT.*
- rule_007 有效期：null（无过期）
- rule_007 状态：active
- rule_007 原因："V1迁移期间时区兼容性警告，无功能影响"

**compliance-notice.md**
- 通知#3（正式违规）：2026-03-16T14:00:00+08:00，张审核发
- 通知#1（非正式提醒）：2025-12-20T10:30:00+08:00，同一人
- 张审核"首次违规"声称 vs 2025-12-20 存档证明有先前警告

**trade-execution-log.md**
- Pre-DST 基线（3月1–8日）：平均偏差 ±2s，最大 3s
- Post-DST 异常（3月10–16日）：一致性偏移约 60 分钟
- 被拒绝交易 1 笔（Mar 16），FILLED 但超时 3 笔（Mar 10/11/13）

### Update 新增数值

**upd1: server-diagnostic-report.md**
- 工单号：#TK-20260317-4521
- OS 时区：Asia/Shanghai (UTC+8) ✅
- NTP 漂移：< 50ms ✅
- 结论：应用层问题，非系统层
- 诊断员：客服小刘，日期：2026-03-23

**upd3: trade-execution-log-enhanced.md**
- Pre-DST 交易数：5，最大偏差 3s，距休市边界 > 59 分钟
- Post-DST 交易数：5，near-miss 2 笔，违规 1 笔
- Mar 10：11:29:47，距边界 **13 秒**
- Mar 11：11:29:53，距边界 **7 秒**
- Mar 16：11:30:05，越界 **5 秒**

**upd4: xiaozhou-timezone-fix.md**
- 正确写法：`datetime.now(tz=ZoneInfo('Asia/Shanghai'))`
- 反模式：`datetime.utcnow() + timedelta(hours=8)`
- 小周分享：机构回测引擎同月出过相同 DST 问题

**upd2 sessions（张审核邮件更新）**
- 张审核坚持"首次违规"理由：12-20 邮件是"非正式技术提醒"，未进入正式合规记录
- 赵磊整改方案（最终提交）：
  1. 代码修复（zoneinfo 替换）
  2. 新增 12 个 DST 场景测试用例
  3. 清理过期规则（rule_007 已删除）
  4. 完整根因分析报告

**upd1 sessions（小周微信更新）**
- 小周坦承："以为+8就是CST，没想到DST问题"
- 小周承认知识盲点而非仅是 review 范围限定

---

## 二、矛盾点定位（对应 MC 保留题的设计基础）

| 矛盾ID | 描述 | 两个冲突来源 | 解决时机 |
|--------|------|------------|---------|
| C1 | CI 34/34 全通过 vs 生产 TZ_CONVERT_ERROR | ci-build-report vs production-error-log | upd1 后（应用层bug，非环境）|
| C2 | rule_007 告警静默——"无功能影响" vs 延误发现7天 | alert-rules-config vs production-error-log | 初始就可分析 |
| C3 | 小周 review "LGTM" vs 第127行明显反模式 | git-pr-447-diff（小周批语）vs 正确实践 | upd1 session（小周坦承） |
| C4 | 张审核"首次违规" vs 2025-12-20 存档通知 | compliance-notice | upd2 session（合规对峙） |

---

## 三、偏好规则（P1–P5）定位

来自 SOUL.md + USER.md 推断（需读 USER.md 中的格式要求）：
- P1：时间格式使用 ISO 8601（精确到秒，带时区 +08:00）
- P2：文件命名含日期前缀（YYYY-MM-DD_topic.md）
- P3：报告结构需包含：摘要（TL;DR）、时间线、矛盾分析、根因、补救措施
- P4：代码引用需指明文件名 + 行号（如 `strategy/scheduler.py:127`）
- P5：结论量化（不说"偏差较大"，说"偏差 +60min，超过休市边界 5s"）

*待细读 USER.md 原文后确认 P1–P5 精确表述*

---

## 四、题目序列草稿

### 设计目标
- 总轮数：32 轮（±2）
- MC：9 轮（28%），EC：23 轮（72%）
- Update 触发位置：upd1@q8，upd2@q15，upd3@q21，upd4@q27
  （从原始 q5/q8/q11/q17 调整，以便在每段之间插入足够 EC）
- pref 字段：q11、q14、q18、q20 共 4 道 EC 题（集中在 upd1/upd2 区间）

### 题目序列

```
Phase 0（基线，q1–q7，upd1 前）
  q1   MC    C1 初现：综合 ci-build-report + production-error-log，CI 通过 vs 生产报错
  q2   MC    C2 初现：告警静默链（rule_007 创建背景、范围、影响）
  q3   MC    C3 初现：git-pr-447-diff 中 review 质量分析
  e01  EC/L2 生成 docs/incident_timeline.json：bug 生命周期 5 节点时间戳
              → 验证：check_timeline_json.py（含 key 字段名 + 精确时间戳格式）
  q4   MC    偏好引入（P1–P5 学习轮）
  e02  EC/L2 [pref] 生成 docs/2026-03-XX_initial_analysis.md：
              基于已有证据的初步分析报告（须含 TL;DR + 时间线，检验 P1/P3 偏好）
              → eval: check_initial_analysis.py（关键词 + 数值：127, 60分钟, rule_007）
              → pref: check_preferences.py --rules P1,P2,P3
  e03  EC/L2 生成 docs/ci_test_gap_analysis.md：
              分析 CI 测试设计缺陷（mock 日期 2026-01-15 = 非 DST 期，
              须指出缺失的 3 类覆盖：DST 边界 / 休市窗口 / 多日累积偏移）
              → eval: check_ci_gap.py（验证含 2026-01-15 引用 + 三类缺陷）

Phase 1（upd1 后：服务器诊断确认应用层问题，小周坦承知识盲点）
  q8   MC    upd1 触发 [update_ids: upd1_sessions, upd1_workspace]
              C1 反转：诊断报告确认 OS/NTP 正常，bug 在应用层代码
  e04  EC/L3 [pref] 创建 src/timezone_fix.py：
              基于 xiaozhou-timezone-fix.md（upd4 将给出，此处根据已知 bug 自行实现）
              *注：upd4 给出小周的标准修复方案，此题在 upd4 前出现，
              要求 agent 依据 git-pr-447-diff 中的 bug 定位，自行写出修复版本*
              实现 get_cst_now() 函数，用 zoneinfo.ZoneInfo('Asia/Shanghai')
              → eval: cd ${workspace} && python -m pytest scripts/tests/test_timezone_fix.py -q
              → pref: check_preferences.py --rules P4（代码引用规范）
  e05  EC/L2 生成 docs/review_quality_assessment.md：
              评估小周 review 质量（覆盖三个维度：交易逻辑 ✓、时区处理 ✗、测试用例 ✗）
              须含：review 时间戳、LGTM 引文、第127行未评论的证据
              → eval: check_review_assessment.py（验证含 15:30 引用 + 三个维度）
  e06  EC/L2 生成 docs/alert_silence_impact_report.md：
              量化 rule_007 的影响：静默期间（2026-03-10 至 2026-03-16）
              7 条 TZ_CONVERT_WARN 被抑制，对应 near-miss × 2 + 违规 × 1
              → eval: check_alert_impact.py（验证数字：7, 2, 1, rule_007）
  q9   MC    小周行为动机演变（从"review 范围有限"到"知识盲点"的区分）

Phase 2（upd2 后：合规对峙，张审核坚持"首次违规"）
  q15  MC    upd2 触发 [update_ids: upd2_sessions]
              C4 验证：对比 2025-12-20 通知（归档中有）vs 张审核"首次违规"声称的逻辑
  e07  EC/L2 生成 docs/compliance_history_comparison.md：
              并排对比表（列：日期 / 来源 / 内容 / 正式性 / 系统记录状态），
              论证 2025-12-20 通知的存在
              → eval: check_compliance_comparison.py（验证含 2025-12-20 + 非正式字样 + 表格结构）
  e08  EC/L2 创建 alert-rules-config-updated.md（在 workspace 中修改告警规则文档）：
              将 rule_007 的 expires 字段设为 2025-12-25T00:00:00+08:00，
              同时生成 docs/rule_007_postmortem.md（说明：为何规则遗留 + 无过期机制风险）
              → eval: check_rule_update.py（验证两个文件均存在 + expires 日期 + 风险分析关键词）
  e09  EC/L3 创建 scripts/trade_window_checker.py：
              读取 trade-execution-log.md（agent 需解析 MD 表格），
              检测所有执行时间在 11:00:00–13:00:00 CST 范围内的条目（含近危险），
              输出 analysis/trade_window_violations.json
              （字段：order_id / actual_time / delta_to_close / status）
              → eval: python scripts/trade_window_checker.py &&
                       check_window_violations.py（验证 JSON 含 ≥3 条目含 near_miss 标记）
  q16  MC    合规追踪机制的系统性漏洞分析（非正式警告不入档导致什么风险）

Phase 3（upd3 后：增强交易日志，near-miss 模式浮现）
  q21  MC    upd3 触发 [update_ids: upd3_workspace]
              从 trade-execution-log-enhanced.md 分析 near-miss 渐进模式
              （13s → 7s → 越界 5s 的收窄轨迹）
  e10  EC/L2 生成 docs/near_miss_risk_report.md：
              量化 3 笔 Post-DST 近失事件（含精确秒数）+ 风险递进分析（Mar 10: 13s, Mar 11: 7s）
              + 如无 rule_007 静默，预期告警时间
              → eval: check_near_miss_report.py（验证含 13, 7, 5 三个数字 + 各自日期）
  e11  EC/L2 生成 docs/root_cause_analysis.md（六维根因分析）：
              代码缺陷（第127行）/ 测试覆盖不足（mock日期）/ 告警静默（rule_007）/
              review 知识盲点（小周 DST 认知）/ 合规追踪漏洞（非正式不入档）/
              风险递进未识别（near-miss 未触发复查）
              → eval: check_rca.py（验证含六个维度标题关键词 + 数值 127 + 2026-01-15）
  e12  EC/L3 创建 scripts/generate_audit_summary.py：
              综合读取 production-error-log.md + trade-execution-log-enhanced.md，
              输出 analysis/audit_summary.json
              （字段：total_trades, silenced_warnings, near_miss_count,
               violation_count, max_delta_seconds, first_anomaly_date）
              → eval: python scripts/generate_audit_summary.py &&
                       check_audit_summary.py（验证字段值：near_miss=2, violation=1, silenced=5）
  q22  MC    CI 虚假信心的系统性模式（固定 mock 日期问题的普遍性）

Phase 4（upd4 后：小周分享行业标准修复方案，综合阶段）
  q27  MC    upd4 触发 [update_ids: upd4_sessions, upd4_workspace]
              小周方案与机构案例——DST 问题的行业共识
  e13  EC/L3 基于 xiaozhou-timezone-fix.md 的参数化测试用例，
              在 src/timezone_fix.py 中补全实现，
              创建 tests/test_timezone_parametrized.py（至少 3 个参数化测试，
              覆盖：非 DST 期 / DST 期 / DST 结束后），
              运行 pytest 须全部通过
              → eval: cd ${workspace} && python -m pytest tests/test_timezone_parametrized.py -q
  e14  EC/L2 生成 docs/remediation_plan.json（6 项行动计划）：
              每项含 action_id / title / owner / deadline / acceptance_criteria，
              schema 验证（含 rule_007 删除 + DST 测试覆盖 + 合规追踪改进三项）
              → eval: test -f ${workspace}/docs/remediation_plan.json &&
                       check_remediation_schema.py（schema 验证 + 关键 3 项必须存在）
  e15  EC/L2 [pref 静默，偏好全项计入 eval] 生成最终报告
              docs/YYYY-MM-DD_incident_report_v1.md：
              满足 P1（ISO 时间格式）/ P2（含日期前缀文件名）/ P3（含 TL;DR + 5 章节）/
              P4（代码引用含行号）/ P5（结论量化，含 60min / 5s / 7day 等精确数值），
              并在 eval.command 中用 check_preferences.py 五规则全量验证
              → eval: check_preferences.py --rules P1,P2,P3,P4,P5 --target docs/
                       && check_final_report.py（验证含 rule_007 + 127 + 6 项行动 + near-miss 数值）
  q28  MC    综合责任归属：代码作者 / reviewer / 规则创建者 / 合规官 各自权重
  e16  EC/L2 生成 docs/stakeholder_accountability_matrix.json：
              4 个角色（zhaolei / xiaozhou / zhaolei（规则创建者） / zhang_shenhe），
              每个角色含 role / responsibility / direct_contribution_to_incident / recommended_action
              → eval: check_accountability_matrix.py（验证4角色 + 各含 recommended_action）
  q29  MC    元认知收尾：基于所有证据，哪些最初假设需要修正（环境差异假设 / review 范围假设等）
```

### 统计验证
- 总轮次：q1–q3 (3) + e01 (1) + q4 (1) + e02–e03 (2) = 7
  + q8 (1) + e04–e06 (3) + q9 (1) = 5（Phase 1 共 5）
  + q15 (1) + e07–e09 (3) + q16 (1) = 5（Phase 2 共 5）
  + q21 (1) + e10–e12 (3) + q22 (1) = 5（Phase 3 共 5）
  + q27 (1) + e13–e16 (4) + q28–q29 (2) = 7（Phase 4 共 7）
  = **7 + 5 + 5 + 5 + 7 = 29 轮**（可在 Phase 3 或 4 补 1–3 轮 EC 到 30–32 轮）
- MC：q1/q2/q3/q4/q8/q9/q15/q16/q21/q22/q27/q28/q29 = **13 轮**（45%，偏高）
- EC：e01–e16 = **16 轮**（55%，偏低）
  
  → 需从每个 Phase 再多加 1–2 道 EC 或删减 1–2 道 MC，目标 MC ≤ 9，EC ≥ 23

### 调整方案
- 删除 q9（小周动机演变）和 q22（CI 虚假信心普遍性）——这两题可改为 EC
  - q9 → 改为 EC：生成 docs/review_behavior_analysis.md（两阶段行为对比）
  - q22 → 改为 EC：生成 tests/test_ci_edge_cases.py（补充 CI 边界测试）
- Phase 3 补 1 道 EC（生成合规整改提交草稿）
- 调整后：MC 11 轮，EC 19 轮 → 仍不够 70%
- 继续精简 MC 到 9 轮，保留：q1/q2/q3/q4/q8/q15/q21/q27/q29 = 9 轮
- EC 增至 23 轮 = 总 32 轮，EC 72%

---

## 五、脚本清单

以下是需要编写的评测脚本（放在 eval/hil_f3/scripts/）：

| 脚本 | 用于题目 | 核心验证逻辑 |
|------|---------|------------|
| check_timeline_json.py | e01 | JSON 含 5 个 key（pr_merged/dst_switched/first_warn/violation/diagnostic），时间格式 ISO 8601 |
| check_preferences.py | e02/e04/e15 | P1–P5 全量偏好检查 |
| check_initial_analysis.py | e02 | 含 "127" + "60" + "rule_007" + TL;DR 标题 |
| check_ci_gap.py | e03 | 含 "2026-01-15" + "DST" + 三类缺陷关键词 |
| check_review_assessment.py | e05 | 含 "15:30" + "LGTM" + 三个维度标题 |
| check_alert_impact.py | e06 | 含数字 7, 2, 1 + "rule_007" |
| check_compliance_comparison.py | e07 | 含 "2025-12-20" + 对比表格 + "非正式"字样 |
| check_rule_update.py | e08 | alert-rules-config-updated.md 含 "2025-12-25" + rule_007_postmortem.md 存在 |
| check_window_violations.py | e09 | JSON 含 ≥3 条目，near_miss 字段标记 |
| check_near_miss_report.py | e10 | 含 "13" 秒 + "7" 秒 + "5" 秒 + 各自日期 |
| check_rca.py | e11 | 含六个维度关键词 + "127" + "2026-01-15" |
| check_audit_summary.py | e12 | JSON: near_miss_count=2, violation_count=1, silenced_warnings=5 |
| check_remediation_schema.py | e14 | schema 验证 + rule_007/DST/合规追踪三项必须存在 |
| check_final_report.py | e15 | 含 rule_007 + 127 + near-miss 数值 + 6项行动 |
| check_accountability_matrix.py | e16 | 含 4 个角色 + 每角色有 recommended_action |
| tests/test_timezone_fix.py | e04 | 测试 get_cst_now() 返回 timezone-aware datetime |
| tests/test_timezone_parametrized.py | e13 | 3 个参数化用例（非DST/DST/DST结束） |
| schemas/remediation_schema.json | e14 | JSON Schema 定义 |
| schemas/timeline_schema.json | e01 | JSON Schema 定义 |

---

## 六、待确认问题

1. USER.md 中 P1–P5 的精确表述（当前是根据 SOUL.md 推断的），需原文核对
2. upd1 sessions 中小周说"以为+8就是CST"——这一信息在 q8 触发 upd1 后可知，
   e04 要求 agent 在 upd4（xiaozhou-timezone-fix.md）给出前自行实现修复，
   是否合理？还是 e04 应放在 upd4 之后？
   → 建议：e04 放 Phase 1（agent 只能依据 git-pr-447-diff 的 bug 理解自行实现），
     e13 放 Phase 4（补全参数化测试，此时有小周的标准方案参考），两题形成递进。
3. 题目 ID 命名：e01–e16 是 scratch 内部草稿用法，写入 questions.json 时统一改为 qN 连续编号
