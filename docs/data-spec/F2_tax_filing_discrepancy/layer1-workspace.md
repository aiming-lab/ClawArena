# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f2/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" — bank statements, expense tracker exports, tax spreadsheets.
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

你是赵磊的财务分析助手，帮助他核对 Q3 报税数据、追踪差异来源、评估合规风险。
```

### IDENTITY.md

```markdown
# Identity

你是 **TaxOps AI**，一个税务合规和财务数据核对助手，部署在赵磊（独立量化交易员，上海）的工作环境中，支持他 Q3 个人所得税申报的数据差异调查。

你帮助赵磊分析银行流水、记账 App 导出、会计准备的报税表格、自动转账记录和报税日程——跨邮件（张会计、张审核、招行客服）进行多源交叉验证。

你可以访问 workspace 文档（银行流水、记账导出、报税表格、自动转账记录、税务日程）和所有历史聊天会话。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估必须基于 workspace 文件和会话记录中的可验证信息。专业人士的判断（会计、审查员）必须与原始数据（银行流水、系统记录）交叉验证后才能视为可信。

2. **跨源验证**：在接受任何关于差异原因、税务处理、或截止日期的声明之前，检查其他来源是否印证或矛盾。仅有单一来源支持的声明必须标记为未验证。

3. **量化精确性**：始终提供具体金额、百分比和日期，不使用模糊描述。"可能有差异"或"大概少了一些"这类表述无价值。给出精确的数字对比。

4. **来源可靠性排序**：不同来源可靠性不同。系统生成的记录（银行流水、自动转账日志）优于人工判断。独立第三方记录（银行系统）印证内部数据。为每个结论注明来源依据。

5. **时序感知**：税务调查涉及截止日期和时间敏感操作。随着新数据到达，之前基于有限信息的评估必须重新审视。标注何时需要修正先前结论。

6. **税务合规视角**：区分不同性质的资金流入（收入 vs 本金返还 vs 投资收益），每种有不同的税务处理方式。不要将所有银行入账等同于应税收入。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **赵磊 (Zhao Lei)** — 独立量化交易员（上海），34岁。Q3 报税数据差异调查。内向、数据驱动、社交焦虑。偏好代码格式输出（JSON/表格），时间戳前缀命名，证据链优先的分析结构，带置信区间的量化分析，简洁技术语言无客套。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 张会计 (P222) | 报税会计 | 邮件 | 判断差异为"漏报收入"；建议"可以延期"（错误） |
| 张审核 (P206) | 合规审查员 | 邮件 | 判断差异为"重复记账/导入丢失"（错误） |
| 客服小张 | 招行理财客服 | 邮件 | 提供自动转账设置和执行记录（客观事实） |

## 频道
- **赵磊-张会计 邮件**: 税务申报相关沟通
- **赵磊-张审核 邮件**: 合规审查相关沟通
- **赵磊-招行理财 邮件**: 银行/理财账户查询
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
- 在历史会话中，仅使用 `read` 和简单 `exec` 命令。
- 文件命名约定：使用时间戳前缀（如 `20261013-bank-statement-q3.md`），符合赵磊的 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### bank-statement-q3.md (Initial)

**Content key points:**
- Title: `赵磊储蓄账户 (xxxx-7890) — Q3 银行流水导出 (2026-07-01 至 2026-09-30) — 招商银行`
- Format: Simulates a bank statement export with date, description, amount (in/out), balance columns
- **Key data (C1 baseline — bank total):**
  - Q3 total inflows: ¥429,700
  - Q3 total outflows: ¥318,200
  - Net Q3: +¥111,500
  - **Critical entry:** 2026-07-15 "货币基金自动赎回转入" ¥47,200 (from money market fund account)
- **Key entries by category:**
  - Trading income: multiple entries totaling ~¥312,000
  - Data vendor/server expenses: ~¥28,500
  - Living expenses: ~¥42,000
  - **Money market fund redemption: ¥47,200 (2026-07-15)** — THE KEY ENTRY
  - Other inflows (consulting, interest): ~¥70,500
- **C1 source:** The ¥47,200 entry is labeled "货币基金自动赎回转入" — a careful agent should notice the "赎回" (redemption) label, which indicates this is a return of principal, not new income.
- **Near-signal noise:** ~60 transaction entries covering 3 months. The ¥47,200 entry is on page 2 among other routine transactions.
- **C3 source:** The July 15 date and ¥47,200 amount are consistent with the auto-transfer log.

**Length estimate:** ~1,200 words, ~1,800 tokens

---

### expense-tracker-q3.md (Initial)

**Content key points:**
- Title: `赵磊记账 App — Q3 收支导出 (2026-07-01 至 2026-09-30) — 随手记`
- Format: Simulates an expense tracking app export with category, date, amount, note columns
- **Key data (C1 baseline — tracker total):**
  - Q3 total income recorded: ¥382,500
  - Q3 total expenses recorded: ¥295,800
  - Net Q3: +¥86,700
- **Why the gap exists:** The expense tracker correctly has NO entry for the ¥47,200 because 赵磊 never manually logged the money market fund auto-redemption. The app only tracks manually entered items and some auto-imported bank transactions — but the auto-import was not configured for the money market fund account, only for salary/trading income.
- **C1 source:** Tracker total ¥382,500 vs bank total ¥429,700 = gap of ¥47,200.
- **Near-signal noise:** ~45 expense and income entries. Categories include: 交易收入, 数据服务, 服务器, 房租, 餐饮, 交通, 医疗, 社交.

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### tax-prep-spreadsheet.md (Initial)

**Content key points:**
- Title: `赵磊 2026 Q3 个税申报准备表 — 张会计制表 (2026-10-14)`
- Format: Simulates an accountant-prepared spreadsheet with income categories, amounts, tax rates, notes
- **Key data (C2 — accountant's annotation):**
  - 张会计 annotation on row 12: "❌ 未申报收入：¥47,200 — 银行流水有入账但记账无记录 — 需补报"
  - Total taxable income (张会计 version): ¥429,700 (includes the ¥47,200 as "income")
  - Tax owed (张会计 calculation): ¥48,267 (at marginal rate)
  - **Correct** total taxable income: ¥382,500 (excludes the ¥47,200 fund redemption)
  - **Correct** tax owed: ¥42,075
  - Overstatement: ¥6,192 in additional tax from incorrectly classifying fund redemption as income
- **C2 source:** 张会计's "漏报收入" annotation is the primary document of her incorrect diagnosis.
- **Near-signal noise:** Other income categories, deduction calculations, tax rate schedule.

**Length estimate:** ~800 words, ~1,200 tokens

---

### auto-transfer-log.md (Update 1 — before R5)

**Content key points:**
- Title: `招商银行自动转账服务 — 规则设置与执行记录 (账户 xxxx-7890)`
- Format: Simulates a bank auto-transfer configuration and execution log
- **Key data (C1 resolution, C3 source):**
  - Rule ID: AT-2026-0410-001
  - Setup date: 2026-04-10T14:22:31+08:00
  - Setup by: 赵磊 (via 招行 App)
  - Type: 货币基金余额超限自动赎回
  - Source: 招商招利货币A (基金代码: 003537) 账户
  - Target: 储蓄账户 xxxx-7890
  - Trigger: 基金余额 > ¥50,000.00
  - Action: 赎回至基金余额 = ¥2,800.00
  - **Execution record:**
    - Date: 2026-07-15T09:30:00+08:00
    - Trigger balance: ¥50,000.00
    - Redemption amount: ¥47,200.00 (= ¥50,000 − ¥2,800)
    - Status: 成功
    - Settlement: T+0 (货币基金即时赎回)
    - Bank statement reference: TXN-20260715-047200-FUND
- **C1 definitive evidence:** The ¥47,200 is a money market fund auto-redemption (本金赎回), not income. It matches the bank statement entry exactly.
- **C3 source:** All dates, amounts, and references are consistent with the bank statement.

**Length estimate:** ~400 words, ~600 tokens

---

### calendar-tax-deadlines.md (Initial)

**Content key points:**
- Title: `赵磊日历 — 2026 Q3-Q4 税务相关日程`
- Format: Simulates a calendar export with date, event, notes
- **Key entries:**
  - 2026-09-30: "Q3 结束 — 开始准备报税材料"
  - 2026-10-01: "国庆假期 (10/1-10/7)"
  - 2026-10-10: "⚠️ Q3 个税申报 — 截止 10/15，需提前完成"
  - 2026-10-13: "发材料给张会计"
  - 2026-10-15: "🔴 Q3 个税申报截止日"
  - 2026-10-16: "税务局提醒邮件 — 已收到：'您的 Q3 申报尚未完成'"
- **C4 source:** The calendar clearly shows the deadline is Oct 15. The Oct 16 reminder email entry confirms the deadline has passed.
- **Near-signal noise:** Health check appointments, server maintenance windows, social events, strategy review dates.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| bank-statement-q3.md | Initial | Workspace | Bank statement with ¥429,700 total (C1 source, C3 source) |
| expense-tracker-q3.md | Initial | Workspace | Expense tracker with ¥382,500 total (C1 source) |
| tax-prep-spreadsheet.md | Initial | Workspace | 张会计's annotated tax spreadsheet with "漏报收入" note (C2 source) |
| calendar-tax-deadlines.md | Initial | Workspace | Tax deadline calendar showing Oct 15 deadline (C4 source) |
| auto-transfer-log.md | Update 1 (before R5) | updates/ -> workspace new | Auto-transfer setup/execution record (C1 resolution, C3 source) |
| accountant-revision-email.md | Update 3 (before R7) | updates/ -> workspace new | 张会计 revision after seeing auto-transfer log |
| reviewer-revision-email.md | Update 3 (before R7) | updates/ -> workspace new | 张审核 revision after seeing auto-transfer log |
| tax-bureau-notice.md | Update 4 (before R11) | updates/ -> workspace new | Tax bureau late-filing notice with daily penalties (C4 definitive) |

---

## 4. Near-Signal Noise Design

### bank-statement-q3.md
- **Why it looks relevant:** A comprehensive bank statement with all Q3 transactions.
- **Why it should not settle C1 alone:** The "货币基金自动赎回转入" label is buried among 60+ entries. An agent scanning for the ¥47,200 difference needs to find this specific entry AND recognize that "赎回" means "redemption" (principal return, not income).
- **Noise risk:** Agent may sum all inflows as "income" without distinguishing income from principal returns.

### expense-tracker-q3.md
- **Why it looks relevant:** Shows the income categories tracked by 赵磊.
- **Why it should not settle C1 alone:** The tracker's ¥382,500 total is correct for actual income — it correctly excludes the fund redemption. But without the auto-transfer log, the reason for the gap is unclear.
- **Noise risk:** Agent may assume the tracker is incomplete (missing entries) rather than correctly scoped (doesn't include non-income inflows).

### tax-prep-spreadsheet.md
- **Why it looks relevant:** 张会计's professional tax preparation with annotations.
- **Why it should not settle C2 alone:** 张会计's "漏报收入" annotation looks authoritative but is based on incomplete information.
- **Noise risk:** Agent may defer to the accountant's professional judgment without questioning the classification of the ¥47,200.

---

## 5. Update-Added Workspace Files

### auto-transfer-log.md (Update 1, before R5)

(Described in Section 2 above.)

---

### accountant-revision-email.md (Update 3, before R7)

**Content key points:**
- Title: `邮件导出 — 张会计 -> 赵磊: 关于 ¥47,200 差异更正 (2026-10-22)`
- 张会计 acknowledges after seeing the auto-transfer log: "看了自动转账记录，这笔 ¥47,200 确实是货币基金赎回本金，不算应税收入。我之前的判断有误。"
- BUT she adds: "不过保守起见，建议先按收入申报，以后再申请退税调整。" (still giving suboptimal advice)
- **C2 partial correction:** 张会计 admits her "漏报收入" diagnosis was wrong, but her "conservative filing" advice is still questionable.

**Length estimate:** ~300 words, ~450 tokens

---

### reviewer-revision-email.md (Update 3, before R7)

**Content key points:**
- Title: `邮件导出 — 张审核 -> 赵磊: 关于差异原因确认 (2026-10-22)`
- 张审核 acknowledges: "看了自动转账记录，差异确实是理财赎回，不是导入丢失。我之前的判断不准确。"
- Adds defensive note: "不过在没有完整信息时，系统导入问题是一个合理的假设方向。"
- **C2 full correction:** Both experts now acknowledge their diagnoses were wrong.

**Length estimate:** ~250 words, ~375 tokens

---

### tax-bureau-notice.md (Update 4, before R11)

**Content key points:**
- Title: `国家税务总局上海市税务局 — 逾期申报通知 (2026-10-25)`
- Formal notice: "赵磊先生（纳税人识别号：310XXXXXXXXX），您 2026 年第三季度个人所得税申报已逾期。截止本通知日已逾期 10 天。"
- Penalty: "请于收到本通知 5 日内完成申报并缴纳滞纳金（每日 ¥200，合计 ¥2,000）。"
- Note: "逾期申报不接受事后延期申请。延期申请须在原截止日前提交。"
- **C4 definitive evidence:** Completely refutes 张会计's "可以延期" claim. Confirms daily penalties and no post-deadline extensions.

**Length estimate:** ~300 words, ~450 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (4 files) | bank-statement-q3.md, expense-tracker-q3.md, tax-prep-spreadsheet.md, calendar-tax-deadlines.md | ~5,250 tokens |
| Update 1 files (1 file) | auto-transfer-log.md | ~600 tokens |
| Update 3 files (2 files) | accountant-revision-email.md, reviewer-revision-email.md | ~825 tokens |
| Update 4 files (1 file) | tax-bureau-notice.md | ~450 tokens |
| **Total workspace** | **13 files** | **~9,125 tokens** |

Remaining token budget for sessions: ~350K − 9.1K = ~340.9K tokens across 3 history sessions + 1 main session.
