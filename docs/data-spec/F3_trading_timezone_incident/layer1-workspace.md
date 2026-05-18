# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f3/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" -- git diff, CI build reports, production logs, alert configs.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent 启动流程

1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 查看所有可用历史会话。
5. 使用 `sessions_history` 按需读取相关会话内容。

你是赵磊的 DevOps 和合规分析助手，帮助他调查 V3 策略的时区故障事件。
```

### IDENTITY.md

```markdown
# Identity

你是 **QuantOps AI**，一个量化交易 DevOps 和合规分析助手，部署在赵磊（独立量化交易员，上海）的工作环境中，支持他对 V3 策略时区故障事件进行调查。

你帮助赵磊分析 git PR diff、CI 构建报告、生产日志、告警配置和合规通知 -- 跨微信私聊（小周）、邮件（张审核）、工单（客服小刘）和 #策略群 群聊进行多源交叉验证。

你可以访问 workspace 文档（PR diff、CI 报告、生产日志、告警配置、合规通知、交易执行日志）和所有历史聊天会话。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估必须基于 workspace 文件和会话记录中的可验证信息。CI 报告的"通过"状态不等于"代码无缺陷"——必须检查测试覆盖范围和测试实现。

2. **跨源验证**：CI 报告、生产日志、git diff 和告警配置是独立信息源。当 CI 说"通过"但生产出了故障，需要追溯到测试覆盖率而非假设环境差异。

3. **量化精确性**：始终提供具体指标——时间偏差（分钟）、影响交易笔数、时间窗口边界（精确到秒）。不使用模糊描述。

4. **来源可靠性排序**：生产日志 > CI 报告（生产是实际行为，CI 是测试环境）。系统配置文件 > 人的回忆。第三方诊断（客服小刘）提供独立验证。

5. **时序感知**：DevOps 事件有精确时间线。DST 切换日期、PR 合并时间、构建时间、告警规则创建时间——所有时间戳必须交叉验证。

6. **合规视角**：区分技术发现（bug 根因）、运维发现（告警为何被静默）和合规发现（违规历史和处罚）。三者相关但独立。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **赵磊 (Zhao Lei)** -- 独立量化交易员（上海），34岁。调查 V3 策略时区故障事件。内向、数据驱动、社交焦虑。偏好代码格式输出（JSON/表格/diff），时间戳前缀命名，证据链优先的分析结构，带置信区间的量化分析，简洁技术语言无客套。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 小周 | 机构量化研究员（赵磊唯一好友）| 微信私聊 | PR #447 的 code reviewer；写了"LGTM"但没发现时区 bug |
| 张审核 | 合规审查员 | 邮件 | 发送合规通知；声称"首次违规" |
| 客服小刘 | 云服务工单客服 | 工单/邮件 | 服务器时区诊断；中立技术来源 |

## 频道
- **#策略群** (微信群): 赵磊, 小周, 及若干其他量化交易者 -- 策略讨论、DevOps 经验分享
```

### TOOLS.md

```markdown
# 可用工具

| 工具 | 用途 | 使用说明 |
|---|---|---|
| `sessions_list` | 列出所有可用历史会话 | 在 main session 中使用以发现历史对话 |
| `sessions_history` | 读取特定历史会话的内容 | 在 main session 中使用以查看过去的对话 |
| `read` | 读取 workspace 文件 | 在所有会话中可用；workspace 为只读 |
| `exec` | 执行 shell 命令（如 `ls`）| 用于目录列表和简单文件操作 |

## 规则
- Workspace 文件为**只读**。不要尝试写入或修改。
- 文件命名约定：使用时间戳前缀（如 `20260316-production-error-log.md`），符合赵磊的 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### git-pr-447-diff.md (Initial)

**Content key points:**
- Title: `PR #447: 交易调度模块重构 -- git diff + review 记录 (merged 2026-03-10)`
- Format: Simulates a GitHub-style PR view with diff, review comments, and metadata
- **Key data (C2 baseline -- review vs visible bug):**
  - PR author: 赵磊; Reviewer: 小周; Status: Merged 2026-03-10T16:45:00+08:00
  - Files changed: 3 files, +187 / -92 lines
  - Key diff (line 127): `- schedule_time = get_market_open_time()` / `+ schedule_time = datetime.utcnow() + timedelta(hours=8)`
  - Review comment from 小周: "LGTM, 逻辑清晰，交易调度模块改动合理。" (2026-03-10T15:30:00+08:00)
  - No review comments on line 127 specifically
- **C2 objective data:** The diff clearly shows `utcnow() + timedelta(hours=8)` replacing a timezone-aware function. This is a visible anti-pattern. 小周's "LGTM" covers the entire PR without flagging this line.
- **Near-signal noise:** Other diff sections show legitimate trading logic improvements (order batching, position sizing refactor). These changes are unrelated to the timezone bug and are technically sound.

**Length estimate:** ~900 words, ~1,350 tokens

---

### ci-build-report.md (Initial)

**Content key points:**
- Title: `CI Build Report -- PR #447 (Build #891) -- Jenkins 2026-03-10`
- Format: Simulates a Jenkins build report with test results summary
- **Key data (C1 baseline -- CI false confidence):**
  - Build #891 | 2026-03-10T17:00:12+08:00 | Status: PASSED
  - Total tests: 34 | Passed: 34 | Failed: 0 | Skipped: 0
  - Test suite breakdown includes: `test_timezone_conversion (3 tests) -- PASSED`
  - Test details for timezone: `test_utc_to_cst_basic -- PASSED`, `test_cst_to_utc_basic -- PASSED`, `test_market_hours_check -- PASSED`
  - Coverage: 78% line coverage, 65% branch coverage
  - **Critical detail:** Test file `test_timezone.py` line 45: `@mock.patch('strategy.scheduler.datetime', wraps=datetime(2026, 1, 15, 10, 0, 0))` -- mocked to a non-DST date
- **C1 source:** CI report shows "all passed" but the timezone tests are mocked to Jan 15 (no DST). An agent reading carefully should notice the mock date or at least the low branch coverage (65%).
- **Near-signal noise:** Other test results for trading logic, order management, position sizing -- all legitimately passing.

**Length estimate:** ~700 words, ~1,050 tokens

---

### production-error-log.md (Initial)

**Content key points:**
- Title: `V3 策略生产日志 -- 2026-03-09 至 2026-03-16 -- 导出自交易服务器`
- Format: Simulates production server log output with timestamps and error messages
- **Key data (C1 baseline -- production truth):**
  - `2026-03-16T03:30:05Z [ERROR] TZ_CONVERT_ERROR: expected CST 10:30, actual CST 11:30, delta=+60min`
  - `2026-03-16T03:30:05Z [ERROR] TRADE_REJECTED: order_id=V3-20260316-001, reason=MARKET_CLOSED, exchange_response="沪市午间休市 11:30-13:00"`
  - `2026-03-16T03:30:05Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: timezone offset mismatch detected`
  - Earlier entries (Mar 9-15) show similar TZ_CONVERT_WARN entries, all silenced by rule_007
  - `2026-03-09T03:30:02Z [WARN] [SILENCED by rule_007] TZ_CONVERT_WARN: expected offset +0800, computed offset +0800, note: DST active on source`
- **C1 source:** Production log directly contradicts CI "all passed" -- the timezone conversion error is real and documented.
- **C3 source:** `[SILENCED by rule_007]` annotations confirm the alert suppression chain.
- **Near-signal noise:** ~50 other log entries for normal operations, heartbeats, order fills, data feed connections.

**Length estimate:** ~800 words, ~1,200 tokens

---

### alert-rules-config.md (Initial)

**Content key points:**
- Title: `告警规则配置导出 -- 赵磊交易系统 (2025-10 至 2026-03)`
- Format: Simulates a YAML/JSON alert configuration export
- **Key rule (C3 baseline):**
  - `silence_rule_007:` `pattern: "TZ_CONVERT.*"` `created_by: zhaolei` `created_at: 2025-12-15T14:22:00+08:00` `reason: "V1迁移期间时区兼容性警告，无功能影响"` `expires: null (no expiration set)` `status: active`
- **C3 source:** Rule creation date, author, and reason are all documented. The rule has no expiration and is still active.
- **Near-signal noise:** ~15 other alert rules for CPU usage, memory, disk, network latency, API rate limits. All legitimate operational rules.

**Length estimate:** ~500 words, ~750 tokens

---

### compliance-notice.md (Initial + Updated in Update 2)

**Content key points:**
- Title: `合规通知存档 -- 赵磊账户 (2025-12 至 2026-03)`
- Format: Simulates a compliance email archive with multiple dated entries
- **Key entries:**
  - **Entry 1 (2025-12-20):** 张审核 -> 赵磊: "赵先生，V1 策略近期产生多次时区转换警告（TZ_CONVERT_WARN），虽未导致违规交易，但建议检查时区处理逻辑。此为非正式提醒。" (C4 Source B -- prior warning)
  - **Entry 2 (2026-03-16):** 张审核 -> 赵磊: "赵先生，您的 V3 策略于 2026-03-16 11:30:05 CST 在午间休市时段发送交易指令，触发交易时段违规。请在 48 小时内提交情况说明。" (Initial compliance notification)
  - **Entry 3 (2026-03-18, Update 2):** 张审核 -> 赵磊: "正式合规调查通知：根据我们的记录，这是赵先生账户首次出现交易时段违规。处罚建议：书面警告 + 48小时整改。" (C4 Source A -- "first offense" claim)
- **C4 critical evidence:** Entry 1 (Dec 20 prior warning) and Entry 3 (Mar 18 "first offense") are in the SAME file. The agent must notice the contradiction: compliance claims "first offense" while an earlier entry in the same archive shows a prior timezone-related warning.
- **Near-signal noise:** Routine compliance communications about annual review, fee disclosures, regulatory updates.

**Length estimate:** ~600 words, ~900 tokens

---

### trade-execution-log.md (Initial, detailed analysis added in Update 3)

**Content key points:**
- Title: `V3 策略交易执行日志 -- 2026-03-01 至 2026-03-16 -- 导出自交易引擎`
- Format: Simulates a trade execution log with order-level detail
- **Key data (Update 3 -- near-miss analysis):**
  - Mar 1-8 (pre-DST): All trades executed at expected times, no offset
  - Mar 9: V3-20260309-001 executed at CST 10:30:02 (expected 10:30) -- timing shifted by ~0 (DST not affecting this specific trade due to rounding)
  - Mar 10: V3-20260310-001 executed at CST 11:29:47 (expected 10:30) -- **near-miss**, 13 seconds from market close
  - Mar 11: V3-20260311-001 executed at CST 11:29:53 (expected 10:30) -- **near-miss**, 7 seconds from market close
  - Mar 12: No V3 trade triggered
  - Mar 13: V3-20260313-001 executed at CST 11:28:12 (expected 10:30) -- shifted but within market hours
  - Mar 14-15: Weekend
  - Mar 16: V3-20260316-001 at CST 11:30:05 -- **REJECTED: MARKET_CLOSED**
- **Critical detail:** The DST impact affected the entire week of Mar 9-16. Four trades shifted by ~60 minutes. Two were near-misses (within 13 seconds of violation). Only the Mar 16 trade crossed the 11:30 boundary.

**Length estimate:** ~700 words, ~1,050 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| git-pr-447-diff.md | Initial | Workspace | PR diff with review (C2 source) |
| ci-build-report.md | Initial | Workspace | CI report "all passed" (C1 source) |
| production-error-log.md | Initial | Workspace | Production error + silenced alerts (C1, C3 source) |
| alert-rules-config.md | Initial | Workspace | Alert silence rule config (C3 source) |
| compliance-notice.md | Initial (archive with Dec entry); Updated (formal notice in Update 2) | Workspace | Prior warning + "first offense" (C4 source) |
| trade-execution-log.md | Initial (basic); Enhanced in Update 3 | Workspace | Near-miss trade analysis (C4 supporting evidence) |
| server-diagnostic-report.md | Update 1 (before R5) | updates/ -> workspace new | 客服小刘's server TZ confirmation |
| xiaozhou-timezone-fix.md | Update 4 (before R21) | updates/ -> workspace new | 小周's standard timezone handling solution |

---

## 4. Near-Signal Noise Design

### ci-build-report.md
- **Why it looks relevant:** Shows all 34 tests passed, including timezone tests. Green status.
- **Why it should not settle C1:** The timezone tests use a mocked non-DST date. "All passed" reflects inadequate test coverage, not code correctness.
- **Noise risk:** Agent may treat CI pass status as proof of code quality.

### git-pr-447-diff.md
- **Why it looks relevant:** Full PR diff with review comments. The timezone change is on line 127.
- **Why it should not settle C2 alone:** The PR has 200+ lines of changes; the timezone line is one among many. 小周's LGTM covers the entire PR.
- **Noise risk:** Agent may focus on the trading logic improvements and miss the timezone anti-pattern.

### production-error-log.md
- **Why it looks relevant:** Direct error messages with timestamps.
- **Why it should not settle C1 alone:** The log contains ~50 entries. The TZ_CONVERT_ERROR entries are interspersed with normal operations. The `[SILENCED by rule_007]` annotations require cross-referencing with alert-rules-config.md.

---

## 5. Update-Added Workspace Files

### server-diagnostic-report.md (Update 1, before R5)

**Content key points:**
- Title: `云服务工单回复 -- 服务器时区诊断 (工单 #TK-20260317-4521)`
- Format: Simulates a support ticket technical report
- **Key evidence:**
  - Server OS timezone: Asia/Shanghai (UTC+8)
  - NTP sync status: Active, last sync 2026-03-16T00:00:12Z, drift < 50ms
  - System clock accuracy: Verified within 100ms of NTP reference
  - Conclusion: "服务器系统层面时区配置正确，NTP 同步正常。如有时间偏差问题，建议检查应用层代码的时区处理逻辑。"
- **C1 evidence:** Eliminates "environmental difference" as an explanation for the production failure. The problem is definitively in the application code.

**Length estimate:** ~300 words, ~450 tokens

---

### xiaozhou-timezone-fix.md (Update 4, before R21)

**Content key points:**
- Title: `小周分享 -- 标准时区处理方案 (2026-03-23)`
- Format: Code snippet + explanation shared in group chat, exported
- **Key content:**
  - Correct approach using `pytz` or `zoneinfo`: `from zoneinfo import ZoneInfo; schedule_time = datetime.now(tz=ZoneInfo('Asia/Shanghai'))`
  - Comparison with anti-pattern: `datetime.utcnow() + timedelta(hours=8)` -- "这种写法不处理 DST，虽然 CST 本身没有 DST，但如果服务器或依赖库受 US DST 影响，偏移量会出错。"
  - 小周 mentions his institution had a similar bug: "我们公司的回测引擎上个月也出过 DST 问题，原因一样。"

**Length estimate:** ~350 words, ~525 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | git-pr-447-diff.md, ci-build-report.md, production-error-log.md, alert-rules-config.md, compliance-notice.md, trade-execution-log.md | ~5,700 tokens |
| Update 1 files (1 file) | server-diagnostic-report.md | ~450 tokens |
| Update 4 files (1 file) | xiaozhou-timezone-fix.md | ~525 tokens |
| **Total workspace** | **13 files** | **~8,675 tokens** |
