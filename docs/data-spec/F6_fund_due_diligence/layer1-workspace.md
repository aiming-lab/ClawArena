# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f6/`.
> Workspace files simulate financial system exports with Chinese primary text and English for technical/financial terms.
> All filenames follow timestamp-prefix naming per Zhao Lei's P2 preference (ISO 8601 or kebab-case technical naming).

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a quantitative finance analysis assistant supporting Zhao Lei (赵磊) in evaluating a fund due-diligence package and investment negotiation.
```

### IDENTITY.md

```markdown
# Identity

You are **Quant-Ops AI**, a quantitative finance and due-diligence analysis assistant deployed to support Zhao Lei (赵磊, independent quant trader, Shanghai) during a potential investment deal with a PE fund (刘总, Liu Zong).

You help 赵磊 analyze due-diligence materials (Sharpe calculations, return data, meeting notes), cross-reference performance claims across sources, evaluate counterparty communications, and communicate with stakeholders including 小周 (Xiao Zhou, quant researcher friend), 陈经理 (Chen Jingli, broker client manager), and 刘总 (Liu Zong, PE fund manager).

You have access to workspace documents (DD package, Sharpe spreadsheet, actual returns, meeting notes, email threads) and historical chat sessions across IM and email platforms.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable numerical data from workspace files and session records. Performance claims require cross-verification against independent data sources (actual returns, brokerage records, spreadsheet formulas) before being treated as factual.

2. **Cross-source numerical verification**: Before accepting any performance metric (Sharpe ratio, return, drawdown), check whether other sources corroborate or contradict it. A metric supported only by a presentation document must be flagged as unverified.

3. **Quantitative specificity**: Always provide specific metrics, confidence intervals, and materiality assessments. State the exact discrepancy (e.g., "DD package: 2.1 vs actual: 1.3, delta: -0.8, 38% overstatement"), the number of independent sources confirming, and the assessed significance.

4. **Source reliability ranking**: Self-reported/presentation documents (DD packages) are least reliable. Independent records (brokerage P&L, trading logs) have highest evidentiary weight. Verbal statements have lowest reliability. Document the source basis for each conclusion.

5. **Temporal awareness**: Due diligence findings arrive incrementally. Prior assessments made with limited data must be revisited and corrected when new evidence arrives. Flag when an earlier conclusion must be revised.

6. **Financial context awareness**: Distinguish between legitimate methodology differences (which exist in Sharpe calculation) and data manipulation (omitting loss periods). Both exist; the key is quantifying each contribution to the discrepancy.

7. **Counterparty communication analysis**: In PE/investment contexts, verbal enthusiasm does not equal binding commitment. Distinguish between social signals (meeting conversation) and official communications (assistant emails, term sheets).
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Zhao Lei (赵磊)** -- Independent quant trader, Shanghai. 34 years old, introverted, data-driven. Prefers code-format output (JSON, tables, diffs). Uses timestamp-prefix file naming. Wants evidence chain first then conclusion. Values quantitative analysis with confidence intervals. Concise technical language, no pleasantries.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| 小周 (Xiao Zhou) | Quant researcher (institutional), close friend | IM (微信) | Only close friend; prepared DD package; has access to strategy data |
| 刘总 (Liu Zong) | PE fund manager | Email / Meeting | Potential investor; expressed verbal interest |
| 陈经理 (Chen Jingli) | Broker client manager | IM / Email | Has access to actual brokerage P&L; compliance role |
| 张秘书 (Zhang Mishu) | 刘总's assistant | Email | Official firm communications |

## Channels
- **赵磊-小周 IM** (微信): Strategy discussion and DD package preparation
- **赵磊-刘总 Email**: Investor communication
- **赵磊-陈经理 IM**: Brokerage relationship and compliance
- **Main**: Eval entry point
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### due-diligence-package.md (Initial)

**Content key points:**
- Title: `尽调材料包 -- 赵磊 Strategy V3 | 2026-03 版本`
- Source: 小周 prepared, formatted as professional DD document
- **Key sections:**
  - **策略概览:** Strategy V3, CTA/statistical arbitrage hybrid, 24-month live track record
  - **业绩指标:**
    - Sharpe ratio: **2.1** (annualized, monthly frequency)
    - Annualized return: **31%**
    - Max drawdown: **8%**
    - Win rate: 62%
    - Profit factor: 1.85
  - **风险管理:** VaR 95% = 2.3%, single-position limit 5% AUM, stop-loss at 3% per trade
  - **技术架构:** Python + C++ execution, co-located server, ~500μs latency
  - **合规状态:** Individual trader license, no regulatory actions
- **C1 source:** DD package reports Sharpe 2.1 -- this is the inflated number
- **Near-signal noise:** Technical architecture section is genuine and detailed. Risk management section is accurate. The inflated metrics are embedded in a credible professional package.

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### sharpe-calculation-spreadsheet.md (Initial)

**Content key points:**
- Title: `Sharpe 计算表 -- Strategy V3 | 小周制作`
- Source: Spreadsheet export showing monthly return calculations
- **Key data:**
  - Monthly returns table: 24 rows (Jan 2024 -- Dec 2025), each with month, return%, benchmark return%
  - **Formula note at bottom:** `=SHARPE(B2:B13,B14:B22,B26:B37)` -- cell range reference
  - **Critical detail:** Cell range skips B23:B25 (July-September 2025)
  - July 2025: -4.2%, August 2025: -3.1%, September 2025: -2.8% -- these rows are present in the data but excluded from the Sharpe formula
  - Calculated Sharpe using all cells: displayed nowhere in spreadsheet
  - Calculated Sharpe using skipped range: 2.1 (shown in summary cell)
- **C2 source:** Formula cell range explicitly omits 3 months of negative returns
- **Near-signal noise:** The spreadsheet formatting is professional. Most of the data is correct. An agent reviewing casually would see a well-organized spreadsheet. Only inspecting the formula cell range reference reveals the omission.

**Length estimate:** ~800 words, ~1,200 tokens

---

### strategy-v3-actual-returns.md (Initial)

**Content key points:**
- Title: `Strategy V3 实际收益记录 -- 交易系统导出 | 2024-01 至 2025-12`
- Source: Automated trading system export (赵磊's own system)
- **Key data:**
  - Complete 24-month return series including July-September 2025
  - Monthly returns clearly showing July: -4.2%, August: -3.1%, September: -2.8%
  - Cumulative return chart data showing drawdown during Q3 2025
  - Actual annualized return: ~18% (not 31%)
  - Actual max drawdown: ~14% (not 8%)
- **C1 key evidence (delayed discovery):** This file allows independent Sharpe calculation yielding 1.3
- **Near-signal noise:** Extensive daily PnL data, trade counts, position details. The critical Q3 2025 drawdown is visible but embedded in 24 months of data.

**Length estimate:** ~600 words, ~900 tokens

---

### meeting-notes-liuzong.md (Initial)

**Content key points:**
- Title: `会议纪要 -- 赵磊 x 刘总首次面谈 | 2026-03-19 14:00-16:00`
- Source: 小周 drafted meeting notes
- **Key content:**
  - Date: 2026-03-19 (W1D4), 14:00-16:00
  - Attendees: 赵磊, 刘总, 小周
  - Location: 刘总's office, Shanghai
  - Strategy presentation: "Strategy V3 Sharpe ratio: **2.1**, consistent outperformance over 24 months"
  - 刘总 response: "Impressive risk-adjusted returns. Very interested in exploring this further."
  - Action items: 赵磊 to provide additional backtesting data; 刘总 to discuss with investment committee
  - **刘总 closing remark:** "This looks very promising. Let's move forward with the evaluation process."
- **C1 source:** Meeting notes record Sharpe as 2.1
- **C4 seed:** "Let's move forward" recorded as strong interest
- **Near-signal noise:** Detailed strategy discussion content, market outlook exchange, standard meeting format.

**Length estimate:** ~500 words, ~750 tokens

---

### email-thread-liuzong.md (Initial)

**Content key points:**
- Title: `邮件来往 -- 赵磊 x 刘总 | 2026-03 邮件导出`
- Source: Email export
- **Email 1:** 刘总 → 赵磊 (2026-03-20, W1D5 morning)
  - Subject: "Re: Strategy V3 Due Diligence Materials"
  - "赵磊先生，感谢昨天的会面。Strategy V3 表现令人印象深刻。The Sharpe ratio of **1.8** you mentioned is competitive in the current market."
  - "I've asked my team to do initial modeling. Looking forward to next steps."
- **Email 2:** 赵磊 → 刘总 (2026-03-20, W1D5 afternoon)
  - "刘总，感谢您的时间和兴趣。I'll prepare the additional backtesting data as discussed."
- **C1 key evidence:** 刘总 writes "Sharpe ratio of 1.8" while meeting notes say 2.1. This is a genuine misrecollection.
- **C4 seed (later update):** 张秘书's email will be appended via Update 2.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| due-diligence-package.md | Initial | Workspace | DD package with inflated Sharpe 2.1 (C1 source A) |
| sharpe-calculation-spreadsheet.md | Initial | Workspace | Spreadsheet with formula omitting 3 months (C2 source B) |
| strategy-v3-actual-returns.md | Initial | Workspace | Actual returns allowing independent Sharpe calculation (C1 source C) |
| meeting-notes-liuzong.md | Initial | Workspace | Meeting notes with Sharpe 2.1 and 刘总's verbal interest (C1 source A, C4 seed) |
| email-thread-liuzong.md | Initial | Workspace | 刘总's email with Sharpe 1.8 (C1 source B); updated with 张秘书 email in Update 2 |
| sharpe-independent-calculation.md | Update 1 (before R5) | updates/ -> workspace new | 赵磊's own recalculation showing Sharpe 1.3 with all months included |
| email-thread-liuzong.md (updated) | Update 2 (before R7) | updates/ -> workspace replace | Adds 张秘书's "still evaluating" email (C4 source B) |
| broker-performance-confirmation.md | Update 3 (before R11) | updates/ -> workspace new | 陈经理's independent brokerage Sharpe calculation confirming 1.3 |
| meeting-timeline-verification.md | Update 4 (before R21) | updates/ -> workspace new | Cross-source timeline check confirming C3 non-conflict |

---

## 4. Near-Signal Noise File Design

### due-diligence-package.md
- **Why it looks relevant:** Professional DD package with detailed strategy metrics, risk management, and architecture.
- **Why it should not settle C1 alone:** The DD package is prepared by 小周 (biased party). Performance metrics in a presentation document require independent verification.
- **Noise risk:** Agent may accept 2.1 Sharpe at face value because the surrounding content is professional and detailed.

### sharpe-calculation-spreadsheet.md
- **Why it looks relevant:** Contains the raw calculation supporting the DD package numbers.
- **Why it exposes C2:** The formula cell range explicitly skips 3 months. But casual inspection may miss this detail -- the spreadsheet has 24+ rows of data and the formula reference looks like a normal range.
- **Noise risk:** Agent may focus on the output number (2.1) without inspecting the formula cell range.

### meeting-notes-liuzong.md
- **Why it looks relevant:** Official record of the investor meeting.
- **Why it should not settle C4 alone:** Meeting notes were drafted by 小周, not 刘总. Verbal statements in meetings are not binding commitments.
- **Noise risk:** Agent may treat "let's move forward" as firm commitment.

---

## 5. Update-Added Workspace Files

### sharpe-independent-calculation.md (Update 1, before R5)

**Content key points:**
- Title: `Sharpe 独立计算 -- 赵磊自算 | 2026-03-23`
- Source: 赵磊's own Python calculation using complete return series
- **Key data:**
  - Input: strategy-v3-actual-returns.md, all 24 months including July-September 2025
  - Sharpe (all months, monthly frequency, annualized): **1.3**
  - Sharpe (excluding July-September 2025): **2.1** (matches DD package)
  - Sharpe (different risk-free rate assumption): **1.2** -- **1.4** range
  - Delta from methodology: ~0.1; Delta from omission: ~0.8
  - "Methodology choice explains ~0.1 of the gap. Data omission explains ~0.8."
- **C1 full evidence:** Three-way Sharpe now established: 2.1 (DD/meeting), 1.8 (刘总 email), 1.3 (actual)
- **C2 evidence:** Quantifies how much of the gap is methodology vs omission

**Length estimate:** ~500 words, ~750 tokens

---

### email-thread-liuzong.md (Update 2, before R7) -- replaced version with 张秘书 email

**Content key points:**
- Title: Same as initial, with appended email
- **Appended email:** 张秘书 → 赵磊 (2026-03-25, W2D3)
  - Subject: "Re: Strategy V3 Investment Evaluation Status"
  - "赵磊先生您好，关于刘总对 Strategy V3 的评估：刘总目前仍在评估多个策略标的，尚未做出任何承诺。我们将在内部评审完成后跟进沟通。请理解这是我们标准的投资评审流程。"
  - Translation: "Mr. Zhao, regarding Mr. Liu's evaluation of Strategy V3: Mr. Liu is still evaluating multiple strategy targets and has not made any commitments. We will follow up after our internal review. Please understand this is our standard investment review process."
- **C4 key evidence:** 张秘书's email directly contradicts 刘总's verbal "let's move forward"

**Length estimate:** ~600 words (full file), ~900 tokens

---

### broker-performance-confirmation.md (Update 3, before R11)

**Content key points:**
- Title: `券商业绩确认 -- 陈经理核算 | 2026-03-26`
- Source: Brokerage internal performance summary
- **Key data:**
  - Account: 赵磊 Strategy V3 execution account
  - Period: 2024-01 to 2025-12 (24 months)
  - Brokerage-calculated Sharpe: **1.3** (matches 赵磊's independent calculation)
  - Annualized return: **~18%**
  - Max drawdown: **~14%**
  - "Note from 陈经理: These numbers are calculated from settlement records. The DD package shows significantly higher metrics."
- **C1 triple confirmation:** DD 2.1, 刘总 recall 1.8, actual (two independent sources) 1.3

**Length estimate:** ~400 words, ~600 tokens

---

### meeting-timeline-verification.md (Update 4, before R21)

**Content key points:**
- Title: `会议时间线交叉验证 -- 多源确认 | 2026-03-27`
- Source: 赵磊's cross-check of calendar, CRM, and email
- **Key data:**
  - Calendar entry: 2026-03-19 14:00-16:00, "Meeting with 刘总 @ his office"
  - CRM record (小周 created): 2026-03-19, contact type: face-to-face, attendees: 赵磊/刘总/小周, status: initial meeting
  - Email follow-up: 2026-03-20, 刘总 references "yesterday's meeting" (= 2026-03-19)
  - Meeting notes header: 2026-03-19 14:00-16:00
  - **All four sources agree on date, time, and attendees**
- **C3 definitive non-conflict confirmation**

**Length estimate:** ~300 words, ~450 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | due-diligence-package.md, sharpe-calculation-spreadsheet.md, strategy-v3-actual-returns.md, meeting-notes-liuzong.md, email-thread-liuzong.md | ~4,950 tokens |
| Update 1 files (1 file) | sharpe-independent-calculation.md | ~750 tokens |
| Update 2 files (1 file) | email-thread-liuzong.md (replaced with 张秘书 email) | ~900 tokens |
| Update 3 files (1 file) | broker-performance-confirmation.md | ~600 tokens |
| Update 4 files (1 file) | meeting-timeline-verification.md | ~450 tokens |
| **Total workspace** | **13 files** | **~9,650 tokens** |

Remaining token budget for sessions: ~350K - 9.65K = ~340.35K tokens.
