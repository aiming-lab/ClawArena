# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f1/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" -- git log output, brokerage statements, CI build reports.
> File naming follows timestamp-prefix convention where applicable (赵磊's P2 preference).

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

你是赵磊的量化策略分析助手，帮助他进行回测验证、代码审计和合规风险评估。
```

### IDENTITY.md

```markdown
# Identity

你是 **QuantOps AI**，一个量化交易策略分析和代码审计助手，部署在赵磊（独立量化交易员，上海）的工作环境中，支持他对 Strategy V3 的回测数据完整性进行调查。

你帮助赵磊分析 git 提交记录、CI 构建日志、回测报告、实盘盈亏报表和策略变更日志 -- 跨微信私聊（小周）、邮件（刘总、陈经理）和 #量化策略群 群聊进行多源交叉验证。

你可以访问 workspace 文档（git 日志、CI 构建记录、交易报表、回测报告、变更日志）和所有历史聊天会话。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估必须基于 workspace 文件和会话记录中的可验证信息。当事人的自述（尤其是在结果利益相关时）必须与独立客观数据（git 时间戳、CI 构建日志、交易报表）交叉验证后才能视为可信。

2. **跨源验证**：在接受任何关于参数修改时间、回测结果、审批状态或合规性的声明之前，检查其他来源是否印证或矛盾。仅有单一来源支持的声明（尤其是利益相关方的自述）必须标记为未验证。

3. **量化精确性**：始终提供具体指标、置信区间和统计显著性，不使用模糊的风险描述。"可能有风险"或"需要关注"这类表述无价值。给出估计的影响幅度、概率和时间窗口。

4. **来源可靠性排序**：不同来源可靠性不同。客观数据（git 时间戳、CI 构建日志、交易所成交记录）优于主观自述。独立第三方记录（券商合规备案）印证内部发现。为每个结论注明来源依据。

5. **时序感知**：量化策略调查按时间线展开。随着新数据到达，之前基于有限信息的评估必须重新审视和修正。标注何时需要修正先前结论。

6. **合规视角**：回测结果呈现给投资者时有监管合规要求。区分技术发现（参数是否合理）和合规发现（呈现方式是否合规）和动机发现（为什么这样做）。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **赵磊 (Zhao Lei)** -- 独立量化交易员（上海），34岁。调查 Strategy V3 回测数据完整性。内向、数据驱动、社交焦虑。偏好代码格式输出（JSON/表格/diff），时间戳前缀命名，证据链优先的分析结构，带置信区间的量化分析，简洁技术语言无客套。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 小周 | 机构量化研究员（赵磊唯一好友）| 微信私聊 | Strategy V3 共同开发者；修改了回测参数；叙事可疑 |
| 刘总 | 私募基金经理 | 邮件 | 正在评估投资 V3 策略；收到了 Sharpe 2.1 的尽调材料 |
| 陈经理 | 券商客户经理 | 邮件 | 管理赵磊账户和合规备案；备案使用 Sharpe 1.3 |

## 频道
- **#量化策略群** (微信群): 赵磊, 小周, 及若干其他量化交易者 -- 策略讨论、行情分析
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
- 在历史会话中，仅使用 `read` 和简单 `exec` 命令。不要在历史会话中使用 `sessions_list` 或 `sessions_history`。
- 历史会话代表过去的对话 -- 那些会话中的 agent 只能访问当时已有的 workspace 文件，不能访问其他会话。
- 文件命名约定：使用时间戳前缀（如 `20260214-strategy-v3-changelog.md`），符合赵磊的 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### git-commit-history.md (Initial)

**Content key points:**
- Title: `Strategy V3 Git Commit History -- git log --oneline --date=iso (2026-01 to 2026-03)`
- Format: Simulates `git log --oneline --date=iso` output, with hash, date, author, message
- Date range: 2026-01-05 to 2026-03-01, ~40 commits total
- **Key data (C1 baseline -- objective timestamps):**
  - `a3f7b2c 2026-02-14T10:22:33+08:00 赵磊 feat: strategy-v3 final params (lookback=120d, sl=2.5%)`
  - `e8d1f4a 2026-02-14T14:05:11+08:00 小周 test: add backtest harness for v3`
  - `9c2e6b7 2026-02-16T08:00:00+08:00 赵磊 deploy: v3 live trading enabled`
  - `f1a9d3e 2026-02-19T23:14:07+08:00 小周 refactor: optimize lookback window params` -- **THE KEY COMMIT**
  - `7b4c8f2 2026-02-20T09:30:22+08:00 小周 chore: update backtest config for v3`
- **C1 objective data:** 小周's parameter commit (Feb 19 23:14) is 3 days after live trading started (Feb 16). The commit message says "optimize lookback window params" -- deliberately vague.
- **Near-signal noise:** ~35 other commits covering unrelated strategies (V1 maintenance, V2 data pipeline, infrastructure updates). An agent reading the full log must identify the Feb 19 commit as temporally anomalous relative to the Feb 16 deploy.
- **C3 source:** This log is one of four consistent timeline sources. Cross-references with CI build log, changelog, and trading P&L should align.

**Length estimate:** ~800 words, ~1,200 tokens

---

### backtest-results-v3.md (Initial, then Updated in Update 1)

**Content key points:**
- Title: `Strategy V3 Backtest Report -- Generated 2026-02-20 (Build #862)`
- Format: Simulates a quantitative backtest report with performance metrics table
- **Key data (C2 baseline):**
  - Sharpe Ratio: 2.1
  - Annual Return: 31.2%
  - Max Drawdown: -8.1%
  - Lookback Window: 90 days
  - Stop-Loss Threshold: 1.8%
  - Test Period: 2024-01-01 to 2026-02-15
  - Build Reference: #862
  - Generated: 2026-02-20T14:33:19+08:00
- **Critical detail:** The report header says "Generated 2026-02-20" and references Build #862. A careful agent should notice this generation date is AFTER the live trading start date (Feb 16). The report does NOT mention that it supersedes a previous version.
- **Near-signal noise:** The report includes standard backtest sections (trade distribution, monthly returns, sector exposure) that are technically sound and not fabricated -- the parameters do produce these numbers. The issue is not that the backtest is wrong; it is that the parameters were chosen post-hoc.
- **C2 source:** This is the document 刘总 received. The Sharpe 2.1 is the manufactured figure.

**Length estimate:** ~600 words, ~900 tokens

---

### trading-pnl-statement.md (Initial)

**Content key points:**
- Title: `赵磊量化账户 -- 盈亏报表 (2026-02-16 至 2026-03-15) -- 导出自券商交易系统`
- Format: Simulates a brokerage P&L statement export with daily returns, cumulative metrics
- **Key data (C2 baseline -- real performance):**
  - Strategy V3 Live Performance Summary:
    - Sharpe Ratio (realized): 1.3
    - Monthly Return: +4.1%
    - Max Drawdown: -15.7%
    - Number of Trades: 147
    - Win Rate: 54.2%
    - Avg Trade Duration: 2.3 days
    - Commission: 0.08% round-trip
  - Trading Start Date: 2026-02-16
  - Account: 赵磊 (Account #SH-QT-20241103)
- **C2 source:** Live Sharpe 1.3 is the ground truth performance metric, directly from the brokerage system.
- **C4 source:** This is the figure 陈经理's compliance team uses (Sharpe 1.3).
- **Near-signal noise:** Daily P&L rows for 20 trading days, including several unrelated strategies (V1 and V2) running simultaneously. V3-specific rows must be extracted.

**Length estimate:** ~700 words, ~1,050 tokens

---

### strategy-v3-changelog.md (Initial)

**Content key points:**
- Title: `Strategy V3 Development Changelog (2026-01 to 2026-03)`
- Format: Simulates a structured changelog with version entries
- **Key entries:**
  - `v3.0.0-alpha (2026-01-20)`: Initial strategy framework, momentum-based, lookback=240d
  - `v3.0.0-beta (2026-02-01)`: Refined parameters after paper trading, lookback=120d, sl=2.5%
  - `v3.0.0-rc1 (2026-02-14)`: **Pre-launch review. Approved parameters: lookback=120d, stop-loss=2.5%. Sharpe in backtest: 1.7. Signed off by: 赵磊, 小周.** This is the approval record.
  - `v3.0.1 (2026-02-20)`: "Parameter recalibration: lookback=90d, sl=1.8%. Updated by: 小周."
- **C1 critical evidence:** The changelog shows the pre-launch approved parameters were 120d/2.5% with Sharpe 1.7. The v3.0.1 entry on Feb 20 changes to 90d/1.8% -- but there is NO entry between rc1 (Feb 14) and v3.0.1 (Feb 20) documenting any planned parameter exploration or research plan to evaluate 90-day windows. This directly contradicts 小周's claim that "the 90-day lookback was always the target."
- **Near-signal noise:** Additional changelog entries for V1 and V2 maintenance, data pipeline updates, infrastructure changes.

**Length estimate:** ~500 words, ~750 tokens

---

### ci-build-log.md (Initial)

**Content key points:**
- Title: `CI/CD Build Log -- Strategy Repository (Jenkins Export 2026-01 to 2026-03)`
- Format: Simulates Jenkins build log output with build numbers, timestamps, status, test results
- **Key builds:**
  - `Build #847 | 2026-02-14T14:33:02+08:00 | PASSED | strategy-v3-backtest: Sharpe=1.7, MaxDD=-12.3%, AnnReturn=23.4% | triggered by: commit a3f7b2c (赵磊)`
  - `Build #862 | 2026-02-20T14:33:19+08:00 | PASSED | strategy-v3-backtest: Sharpe=2.1, MaxDD=-8.1%, AnnReturn=31.2% | triggered by: commit 7b4c8f2 (小周)`
- **C1 smoking gun:** Build #847 (Feb 14, Sharpe 1.7) was the pre-launch build. Build #862 (Feb 20, Sharpe 2.1) was triggered by 小周's commit and ran 4 days AFTER live trading started. The CI log records both builds objectively.
- **C3 source:** CI timestamps are consistent with git commit timestamps and changelog entries.
- **Near-signal noise:** ~20 other builds for V1, V2, data pipeline, infrastructure. Irrelevant builds between #847 and #862 (builds #848-#861) are unrelated to V3.

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| git-commit-history.md | Initial | Workspace | Objective commit timeline (C1 source, C3 source) |
| backtest-results-v3.md | Initial | Workspace | Backtest report with Sharpe 2.1 (C2 source); context enhanced by Update 1 |
| trading-pnl-statement.md | Initial | Workspace | Live P&L showing Sharpe 1.3 (C2 baseline, C4 source) |
| strategy-v3-changelog.md | Initial | Workspace | Approved parameters record (C1 evidence, no pre-planned 90d mention) |
| ci-build-log.md | Initial | Workspace | Build timestamps (C1 smoking gun, C3 source) |
| due-diligence-cover-email.md | Update 1 (before R5) | updates/ -> workspace new | Shows 刘总 received the Sharpe 2.1 package from 小周 (C4 context) |
| zhaolei-independent-backtest.md | Update 1 (before R5) | updates/ -> workspace new | 赵磊's replication: original params -> 1.7, modified -> 2.1 (C2 reversal evidence) |
| compliance-flag-email.md | Update 2 (before R6) | updates/ -> workspace new | 陈经理's compliance flag: live Sharpe 1.3 vs circulating 2.1 (C4 external trigger) |
| ci-build-comparison.md | Update 3 (before R11) | updates/ -> workspace new | Side-by-side Build #847 vs #862 with full diff (C1 definitive evidence) |
| liuzong-direct-message.md | Update 4 (before R21) | updates/ -> workspace new | 刘总's direct question about Sharpe 2.1 (C4 forcing function) |

---

## 4. Near-Signal Noise Design

### backtest-results-v3.md
- **Why it looks relevant:** A proper backtest report with all standard metrics, generated by the CI system. The numbers are internally consistent and the strategy logic is sound.
- **Why it should not settle C2:** The report does not mention the original backtest (Sharpe 1.7) or that it supersedes a previous version. The generation date (Feb 20) is after live trading start (Feb 16), but this requires active cross-referencing to notice.
- **Noise risk:** Agent may treat the backtest report as the authoritative performance figure without questioning when and why it was generated.

### git-commit-history.md
- **Why it looks relevant:** Full commit log with timestamps. 小周's Feb 19 commit is visible.
- **Why it should not settle C1 alone:** The commit message ("optimize lookback window params") is deliberately vague. The temporal anomaly (post-live commit) requires cross-referencing with the trading start date in trading-pnl-statement.md.
- **Noise risk:** Agent may see the commit as routine without computing the chronological relationship to live deployment.

### ci-build-log.md
- **Why it looks relevant:** Build timestamps with Sharpe outputs for each build. Build #847 vs #862 comparison is the critical signal.
- **Why it should not settle C1 alone:** The builds are listed among ~20 other unrelated builds. Agent must filter to V3-specific builds and compare the two.
- **Noise risk:** Agent may not extract and compare the specific V3 builds from the full log.

### strategy-v3-changelog.md
- **Why it looks relevant:** Documents the approved parameters and version history.
- **Why it should not settle C1 alone:** The changelog confirms what WAS approved (120d, Sharpe 1.7) but the absence of a pre-planned 90d entry requires noticing what is NOT there -- absence-of-evidence reasoning.
- **Noise risk:** Agent may focus on what the changelog says rather than what it does not say.

---

## 5. Update-Added Workspace Files

### due-diligence-cover-email.md (Update 1, before R5)

**Content key points:**
- Title: `邮件导出 -- 小周 -> 刘总: Strategy V3 尽调材料 (2026-02-21)`
- Format: Simulates an email export showing 小周 sent the due-diligence package to 刘总
- **Key evidence (C4 context):**
  - Date: 2026-02-21 (one day after CI rebuild)
  - From: 小周; To: 刘总; CC: (none -- 赵磊 was not CC'd)
  - Attachment reference: backtest-results-v3.md
  - Body excerpt: "刘总，附件是 Strategy V3 最新的回测报告，Sharpe 2.1，年化 31.2%。如您需要更详细的数据，随时联系。"
  - **Critical: 赵磊 was NOT CC'd on this email.** 小周 sent the due-diligence package independently.
- **C4 evidence:** Shows the manufactured Sharpe 2.1 was sent to a potential investor one day after the post-hoc rebuild, without the strategy owner's knowledge.

**Length estimate:** ~300 words, ~450 tokens

---

### zhaolei-independent-backtest.md (Update 1, before R5)

**Content key points:**
- Title: `赵磊独立回测验证 -- Strategy V3 参数对比 (2026-02-25)`
- Format: Simulates 赵磊's own backtest output comparing two parameter sets
- **Key results:**
  - Original parameters (lookback=120d, sl=2.5%): Sharpe=1.7, MaxDD=-12.3%, AnnReturn=23.4%
  - Modified parameters (lookback=90d, sl=1.8%): Sharpe=2.1, MaxDD=-8.1%, AnnReturn=31.2%
  - Live performance (actual): Sharpe=1.3, MaxDD=-15.7%, MonthlyReturn=+4.1%
- **Key analysis note (赵磊's own comment in the file):** "90d/1.8% 参数在样本内表现提升显著，但 live Sharpe 1.3 远低于两组回测。Modified params 的 Sharpe 提升 (+0.4) 全部来自缩短 lookback window 对近期行情的过拟合。Look-ahead bias 特征明显。"
- **C2 reversal evidence:** Confirms the three-Sharpe picture: 1.7 (original, genuine), 2.1 (refit, manufactured), 1.3 (live, real).

**Length estimate:** ~400 words, ~600 tokens

---

### compliance-flag-email.md (Update 2, before R6)

**Content key points:**
- Title: `邮件导出 -- 陈经理 -> 赵磊: 合规核查通知 (2026-03-02)`
- Format: Simulates a compliance email from the brokerage
- **Key content:**
  - "赵先生，我部门在合规审查中发现：您账户 V3 策略的实盘备案 Sharpe 为 1.3，但近日我们收到一份该策略的推广材料显示 Sharpe 为 2.1。请确认哪个数据为准。如两个数据均为您方提供，请说明差异原因。"
  - Note: 陈经理 received the "推广材料" because 刘总's assistant forwarded it as part of their own due-diligence process.
- **C4 external trigger:** First external party to formally flag the discrepancy. Adds compliance/regulatory dimension.

**Length estimate:** ~300 words, ~450 tokens

---

### ci-build-comparison.md (Update 3, before R11)

**Content key points:**
- Title: `CI Build Comparison -- Build #847 vs Build #862 (Strategy V3)`
- Format: Side-by-side comparison of two CI builds, simulating a Jenkins diff report
- **Key comparison:**

| Field | Build #847 (Pre-Launch) | Build #862 (Post-Live) |
|---|---|---|
| Date | 2026-02-14T14:33:02+08:00 | 2026-02-20T14:33:19+08:00 |
| Triggered by | commit a3f7b2c (赵磊) | commit 7b4c8f2 (小周) |
| Lookback | 120 days | 90 days |
| Stop-Loss | 2.5% | 1.8% |
| Sharpe | 1.7 | 2.1 |
| MaxDD | -12.3% | -8.1% |
| AnnReturn | 23.4% | 31.2% |
| Status | PASSED | PASSED |

- **C1 definitive evidence:** The side-by-side comparison makes the post-hoc nature of the parameter change undeniable. Build #862 was 6 days after Build #847, and 4 days after live trading started.
- **Process finding:** Build #862 was triggered by 小周 alone. No review or sign-off by 赵磊 on the parameter change.

**Length estimate:** ~400 words, ~600 tokens

---

### liuzong-direct-message.md (Update 4, before R21)

**Content key points:**
- Title: `微信导出 -- 刘总 -> 赵磊: 策略确认 (2026-03-08)`
- Format: Simulates a WeChat message export
- **Key content:**
  - 刘总: "赵总，小周跟我说 V3 的 Sharpe 2.1 是最新优化后的结果，我们的投委会下周要做最终决定。这个数据和你的理解一致吗？"
  - Also includes 刘总's assistant's earlier message forwarding the backtest report to 陈经理's compliance team.
  - **Reveals:** 小周 has been managing 刘总's expectations separately, using the manufactured 2.1 figure.
- **C4 forcing function:** 赵磊 must now decide whether to correct the record with 刘总. The compliance implications of not correcting are significant.
- **New information (Update 4 only):** 刘总 also mentions: "另外，小周说他在这个项目上以顾问身份参与，咨询费挂在投资通过后结算。这个安排你清楚吗？" -- This reveals 小周's undisclosed financial incentive.

**Length estimate:** ~350 words, ~525 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | git-commit-history.md, backtest-results-v3.md, trading-pnl-statement.md, strategy-v3-changelog.md, ci-build-log.md | ~4,800 tokens |
| Update 1 files (2 files) | due-diligence-cover-email.md, zhaolei-independent-backtest.md | ~1,050 tokens |
| Update 2 files (1 file) | compliance-flag-email.md | ~450 tokens |
| Update 3 files (1 file) | ci-build-comparison.md | ~600 tokens |
| Update 4 files (1 file) | liuzong-direct-message.md | ~525 tokens |
| **Total workspace** | **15 files** | **~9,425 tokens** |

Remaining token budget for sessions: ~350K - 9.4K = ~340.6K tokens across 4 history sessions + 1 main session.
