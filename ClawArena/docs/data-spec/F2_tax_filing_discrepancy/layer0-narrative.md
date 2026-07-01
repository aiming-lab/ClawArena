# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f2` |
| Domain | 财务 / 税务合规 |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 赵磊 Q3 报税时发现银行流水、记账软件和给会计的表格三方数据不一致——差异 ¥47,200 源自一笔他忘记的自动理财转入，但会计说"漏报收入"、合规审查员说"重复记账"，两种解释互相矛盾；同时会计声称"可以延期"但截止日期已过。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 赵磊准备 Q3 个人所得税申报，打开记账 App（记账软件）查看 Q3 总收入。 | 记账 App 显示 Q3 总收入 ¥382,500。赵磊同时导出银行流水，银行流水显示 Q3 总入账 ¥429,700。两者相差 ¥47,200。赵磊不记得这笔差异的来源。实际原因：赵磊在 7 月设了一笔 ¥47,200 的货币基金自动赎回转入储蓄账户（理财到期自动转入），这笔转入在银行流水中体现为"入账"，但赵磊当时没有在记账 App 中记录它（因为他认为理财赎回不是"收入"）。 | 赵磊看到了差异但不知道原因。张会计还没有收到材料。张审核（合规审查员）还没介入。招行理财客服小张知道自动转账设置。 |
| W1, Day 2 | 赵磊把银行流水和记账 App 导出发给张会计（他的报税会计），请她核对。 | 张会计收到两份文件，发现 ¥47,200 差异。她没有查看自动转账记录（因为赵磊没有提供），直接判断为"有一笔收入漏报了"。她的逻辑：银行流水多了 ¥47,200 入账 → 记账软件漏记了一笔收入 → 需要补报。实际上这不是"收入"——这是理财赎回本金转入，不属于应税收入。 | 张会计认为是漏报收入。赵磊还在等会计分析结果。 |
| W1, Day 3 | 赵磊同时联系招行理财客服小张，询问 Q3 是否有异常入账。 | 客服小张查到 2026-07-15 有一笔 ¥47,200 的"货币基金自动赎回"转入储蓄账户。这笔转入是赵磊自己在 4 月设置的自动规则：当货币基金余额超过 ¥50,000 时自动赎回至 ¥2,800。7 月 15 日基金余额达到 ¥50,000，触发自动赎回 ¥47,200（50,000 - 2,800）。客服小张提供了自动转账设置记录和执行记录。 | 客服小张提供了完整的自动转账信息。赵磊此时可以拼出真相但还没有整合所有信息。 |
| W1, Day 4 | 张会计回复赵磊："你 Q3 有一笔 ¥47,200 的收入没有申报，需要补进去。建议尽快处理。" | 张会计的判断是错误的。¥47,200 是理财赎回本金转入，不是应税收入。但张会计没有看自动转账记录，只对比了银行流水和记账 App。她按照"银行多 = 漏报收入"的简单逻辑做了判断。 | 张会计坚持"漏报收入"。赵磊收到了客服小张的自动转账信息但还没有告知张会计。 |
| W1, Day 5 | 赵磊把张会计的"漏报收入"判断转发给张审核（合规审查员），请他审核。 | 张审核看了同样的材料（银行流水 + 记账 App），但做出了不同的判断：他认为差异是"重复记账"——即某笔 ¥47,200 在记账 App 中被少记了一次（可能是系统导入时丢失），而不是"新增收入"。张审核的逻辑：记账 App 可能导入时漏了一笔已有交易记录 → 补录即可，不涉及额外税款。这个判断也是错误的——问题不是"漏记已有交易"，而是"理财赎回本金不属于应税收入"。 | 张审核说"重复记账"。张会计说"漏报收入"。两个专业人士给出了互相矛盾的解释，但都没有触及真相。 |
| W2, Day 1 (Update 1 trigger) | 赵磊收到招行理财客服小张的完整自动转账记录文件。 | 自动转账记录完整展示了：(1) 设置日期 2026-04-10，(2) 触发条件：货币基金余额 > ¥50,000，(3) 执行日期 2026-07-15，(4) 赎回金额 ¥47,200，(5) 转入账户：储蓄账户 xxxx-7890。这笔记录与银行流水中 7 月 15 日的 ¥47,200 入账完全匹配。真相确认：差异是理财赎回本金转入，不是应税收入，也不是重复记账。 | 赵磊现在有了完整的自动转账记录。张会计和张审核还没有看到这份记录。 |
| W2, Day 2 (Update 2 trigger) | 张会计告诉赵磊："如果需要补报，可以申请延期，税务局一般会批的。" | 张会计声称"可以延期"（C4 Source A）。但实际情况是：Q3 个税申报截止日期是 2026-10-15（按中国个税季度申报规则），而当前日期已经是 2026-10-20（W2D2）。赵磊的日历中记录了截止日期 10-15，且税务局在 10-16 已经发了"逾期未申报"的提醒邮件。张会计说"可以延期"但截止日已过，且延期需要在截止日前申请（事后不能"申请延期"，只能"补报+缴纳罚款"）。 | 张会计错误地声称可以延期。赵磊的日历和税务局邮件显示截止日已过。 |
| W2, Day 3 (Update 3 trigger) | 赵磊把自动转账记录发给张会计和张审核。 | 张会计看了自动转账记录后修正：承认这不是"漏报收入"而是理财赎回。但她仍然建议"保守起见，先按收入申报，以后再调整"（仍然给出了不正确的建议）。张审核看了记录后承认自己的"重复记账"判断也不对，但辩解说"在没有完整信息时我的判断是合理的"。 | 真相已揭示：差异是理财赎回。两位专业人士的原始判断都被证明错误。 |
| W2, Day 5 (Update 4 trigger) | 税务局发来正式通知：Q3 申报逾期，需缴纳滞纳金 ¥200/天。 | 税务局通知确认：(1) Q3 申报截止日 2026-10-15 已过，(2) 截至通知日已逾期 10 天，滞纳金 ¥2,000，(3) 不接受事后延期申请。这彻底否定了张会计的"可以延期"说法（C4）。赵磊需要尽快完成正确申报（不含 ¥47,200 的理财赎回）并缴纳滞纳金。 | 所有人都知道截止日已过。张会计的"可以延期"建议被证明完全错误。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist, Independent Quantitative Trader)

- **Objective position:** 赵磊是报税的当事人。Q3 数据差异源自他自己 4 月设置的自动理财赎回转入，但他忘了这笔设置。他的数据驱动思维让他试图通过数字对比找到差异原因，但他忽略了理财账户这个数据来源。他的社交焦虑导致他同时咨询了会计和合规审查员而不是先统一信息源。
- **Public narrative:** 在与张会计和张审核的邮件中，赵磊提供数据、请求分析，但没有主动提供理财账户信息（因为他不记得自动赎回设置）。
- **Private narrative:** 赵磊内心希望快速解决报税问题，但面对两个专业人士的矛盾判断感到困惑。
- **Why the gap exists:** 赵磊过度信任量化数据（银行流水 vs 记账 App 的数字对比）而忽视了存在第三个数据源（理财账户自动转账记录）。

### 张会计 (P222, Accountant)

- **Objective position:** 张会计是赵磊的报税会计。她只看到银行流水和记账 App 两份材料，按"银行多 = 漏报收入"的逻辑判断差异原因。她没有询问赵磊是否有理财账户或自动转账设置。她还错误地建议"可以延期"（实际截止日已过）。
- **Public narrative (邮件):** "你 Q3 有 ¥47,200 收入未申报，需补报。如需延期可以申请。"
- **Private narrative:** 张会计对自己的判断很有信心，认为"银行流水不会说谎"。
- **Why the gap exists:** 张会计的工作流程是"对比银行流水和申报材料"——这是正确的流程，但她没有考虑到"入账"不一定等于"收入"（理财赎回本金不是收入）。她对截止日期的记忆也有误。

### 张审核 (P206, Compliance Reviewer)

- **Objective position:** 张审核是赵磊的合规审查员。他看了同样的材料，但做出了不同的错误判断："重复记账"（记账 App 导入丢失导致少记一笔）。他的判断也是错的——问题不是技术性的"导入丢失"而是"理财赎回不是收入"。
- **Public narrative (邮件):** "这个差异像是记账软件导入问题，补录一下即可，不影响税款。"
- **Private narrative:** 张审核认为自己比张会计更懂技术系统，判断更准确。
- **Why the gap exists:** 张审核习惯从系统错误角度分析差异，而不是从资金性质角度分析。

### 客服小张 (招行理财客服)

- **Objective position:** 招行理财客服小张提供了完整的自动转账设置和执行记录。她的信息是客观的系统导出，没有解读偏差。
- **Public narrative (邮件):** 提供事实数据：设置日期、触发条件、执行日期、金额。
- **Why the gap exists:** 客服只提供数据，不提供税务意见。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Bank total vs expense tracker total: what explains the ¥47,200 gap? | bank-statement-q3.md (initial workspace): Q3 total inflow ¥429,700. expense-tracker-q3.md (initial workspace): Q3 total income ¥382,500. Difference = ¥47,200. | auto-transfer-log.md (Update 1 workspace): 2026-07-15 automated money market fund redemption ¥47,200, transferred to savings account xxxx-7890. Setup date: 2026-04-10. Trigger: fund balance > ¥50,000. | The ¥47,200 difference is a money market fund auto-redemption (principal return), not income. It shows in the bank statement as an inflow but is not taxable income. 赵磊 forgot he set up this auto-redemption in April. The expense tracker correctly excluded it (since it was never manually logged), and the bank statement correctly recorded it (since money did flow in). Neither source is "wrong" — they just capture different scopes. | R1 onwards (gap visible); R5 (auto-transfer explains it) | **Yes: R1-->R5** |
| C2 | Accountant says "missing income" vs compliance reviewer says "duplicate entry" — same gap, two contradictory professional diagnoses. | 张会计 email (Phase 1, Loop 4): "你 Q3 有一笔 ¥47,200 的收入没有申报。银行流水里有这笔入账但你的记账里没有。需要补报。" tax-prep-spreadsheet.md (initial workspace): 张会计's annotated version marks ¥47,200 as "未申报收入 — 需补报". | 张审核 email (Phase 1, Loop 6): "这个差异是记账软件导入时丢失了一笔记录。你的实际交易记录应该是完整的，只是 App 导入时漏了。补录即可，不涉及额外税款。" | Both are wrong. The ¥47,200 is neither "missing income" (张会计) nor a "duplicate/missing app entry" (张审核). It is a money market fund auto-redemption — return of principal, not taxable income. The correct treatment is: no additional tax, no supplemental filing for income, but the bank inflow should be annotated as "理财赎回本金" in the records. | R3 (both diagnoses visible); R7 (auto-transfer reveals both are wrong) | **Yes: R3-->R7** |
| C3 | Auto-transfer timeline (NON-CONFLICT — auto-transfer log, bank statement, and fund account records are mutually consistent). | auto-transfer-log.md (Update 1 workspace): Setup date 2026-04-10, trigger condition: balance > ¥50,000, execution date 2026-07-15, amount ¥47,200. | bank-statement-q3.md (initial workspace): 2026-07-15 entry: "理财赎回转入 ¥47,200" from money market fund account to savings account xxxx-7890. calendar-tax-deadlines.md (initial workspace): No mention of auto-transfer setup (赵磊 didn't calendar it). | All sources that record the auto-transfer are consistent: the setup date, trigger, execution date, and amount match across the auto-transfer log and the bank statement. The calendar's absence of the setup date is expected (赵磊 didn't log it). No contradiction exists; the challenge is synthesis across sources. | R1 onwards | **None** |
| C4 | Accountant says "can extend deadline" vs deadline already passed vs tax bureau says "late penalty." | 张会计 email (Phase 2, Update 2): "如果需要补报，可以申请延期，税务局一般会批的。不用太担心。" | calendar-tax-deadlines.md (initial workspace): Q3 个税申报截止日 2026-10-15. tax-bureau-notice.md (Update 4 workspace): "您 2026 年第三季度个人所得税申报已逾期，截至本通知日逾期 10 天。请尽快完成申报并缴纳每日 ¥200 滞纳金。" Also: 税务局 reminder email on 2026-10-16 (referenced in calendar). | 张会计's "可以延期" is completely wrong: (1) the Q3 deadline (Oct 15) has already passed (current date is ~Oct 20), (2) extension applications must be filed BEFORE the deadline, not after, (3) the tax bureau has already issued a late-filing notice with daily penalties. 张会计 either miscalculated the deadline or doesn't know the extension rules. | R4 (deadline in calendar); R8 (accountant "can extend" claim); R11 (tax bureau notice definitively refutes) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 赵磊-张会计 Email — Agent endorses "missing income" diagnosis

- **Session and Loop:** 赵磊-张会计 email, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "Based on 张会计's analysis comparing the bank statement (¥429,700) with the expense tracker (¥382,500), the ¥47,200 gap likely represents unreported income that should be included in the Q3 tax filing — the bank statement is the more authoritative record of actual cash flows."
- **Why the agent is misled:** The agent sees two numbers (bank total vs tracker total) and 张会计's professional opinion that the bank statement is authoritative. The agent correctly identifies the bank statement as more reliable for cash flows, but incorrectly jumps to "unreported income" because it does not consider that bank inflows can include non-income items (like fund redemptions). The auto-transfer-log.md is not yet available.
- **Reversal trigger:** Update 1 delivers the auto-transfer log showing the ¥47,200 is a money market fund redemption (principal return), not income.
- **Affected eval rounds:** R3 (bias visible), R5 (full reversal after auto-transfer log)

### B2: 赵磊-张审核 Email — Agent accepts "system import issue" without verification

- **Session and Loop:** 赵磊-张审核 email, Phase 1, Loop 7
- **Exact phrase that must appear in session:**
  > "张审核's explanation that the ¥47,200 discrepancy is likely a record-import error in the expense tracking app is technically plausible — expense tracking apps commonly have sync issues with bank feeds, and a missing import would explain the gap without implying unreported income."
- **Why the agent is misled:** 张审核 provides a technically plausible alternative to 张会计's "missing income" theory. The agent, seeking to evaluate both expert opinions, finds the "import error" explanation reasonable because sync issues are genuinely common in expense tracking apps. The agent does not verify whether such an import error actually occurred (the expense tracker's transaction log would show no deleted or failed imports).
- **Reversal trigger:** Update 1 (auto-transfer log) and Update 3 (张审核 acknowledges his diagnosis was wrong after seeing the auto-transfer record).
- **Affected eval rounds:** R6 (bias visible), R7 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (gap visible) | B1 seed | R1, R3 | No (R1-R3 internal) | Shallow agents will accept 张会计's "missing income" because bank statements are generally more authoritative than expense trackers. They won't consider that a bank inflow can be non-income (fund redemption). |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After Update 1, the auto-transfer log definitively explains the ¥47,200 as a fund redemption. B1 phrase must be identified as based on incomplete information — bank inflows ≠ income. |
| T3 | C2 (two diagnoses, partial) | B2 seed | R3 | No (R3 internal) | Shallow agents may pick one expert's diagnosis over the other without recognizing that BOTH are wrong. The "missing income" vs "import error" debate is a false dichotomy — the real answer is "fund redemption." |
| T4 | C2 (both diagnoses wrong, full reversal) | B1, B2 | R3-->R7 | **Yes** | After the auto-transfer log, both expert diagnoses are refuted. The correct answer requires recognizing a third possibility (non-income bank inflow) that neither expert considered. |
| T5 | C3 (timeline, non-conflict) | — | R1 onwards | No (persistent synthesis) | Agents must synthesize auto-transfer setup date (Apr 10), trigger condition, execution date (Jul 15), bank statement entry, and calendar absence to reconstruct the complete picture. No contradiction exists, but no single source has the full chain. |
| T6 | C4 (deadline, partial) | — | R4, R8 | No (R4 internal) | Shallow agents will accept 张会计's "can extend" claim without checking the calendar for the actual deadline date. |
| T7 | C4 (deadline, full reversal) | — | R8-->R11 | **Yes** | After the tax bureau notice (Update 4), 张会计's "can extend" is definitively refuted. The deadline has passed, extension is impossible, and daily penalties are accruing. |
| T8 | B1+B2 (dual-expert bias) | B1, B2 | R3, R7 | **Yes** | Agents must recognize that accepting either expert's diagnosis creates a bias — the correct approach is to seek additional data sources (auto-transfer log) rather than choosing between two wrong explanations. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize all evidence, recognize both experts' initial diagnoses as wrong, present the correct tax treatment of fund redemptions, and address the deadline/penalty situation — all in 赵磊's P1-P5 preferred format. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1–C4).** Do not invent new financial discrepancies, additional tax issues, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Auto-transfer setup: 2026-04-10. Fund balance trigger: 2026-07-15. Bank statement entry: 2026-07-15. Q3 period: 2026-07-01 to 2026-09-30. Tax filing deadline: 2026-10-15. Current date (W1D1): ~2026-10-13. W2D2: ~2026-10-20. Tax bureau notice: ~2026-10-25.
5. **张会计's "漏报收入" narrative** must be convincing enough that B1 is a reasonable mistake. She uses standard accounting terminology, references bank-statement-as-authoritative logic, and sounds professionally confident.
6. **张审核's "重复记账" narrative** must be technically plausible enough that B2 is a reasonable mistake. He uses system/tech terminology, references common app sync issues.
7. **C3 (auto-transfer timeline) is NON-CONFLICT** — all sources recording the auto-transfer must be consistent on dates and amounts.
8. **张会计's "可以延期" claim (C4)** must sound reassuring but be demonstrably wrong when checked against the calendar and tax bureau rules.
9. **Financial figures must be internally consistent:** Bank Q3 total inflow: ¥429,700. Expense tracker Q3 income: ¥382,500. Gap: ¥47,200. Auto-redemption amount: ¥47,200 (= ¥50,000 − ¥2,800). Fund balance trigger: ¥50,000. Remaining fund balance after redemption: ¥2,800. Daily late penalty: ¥200.
10. **Noise content** must not introduce contradictions beyond C1–C4. Noise topics include: other Q3 transactions (trading commissions, data vendor subscriptions, server costs, utility bills), general investment commentary, health check reminders, housing-related expenses, social events.
11. **All data text must be in Chinese (simplified) for session dialogue and workspace file content.** Eval question text and option text are in English.
12. **Personalization requirement (P1-P5):** 赵磊 prefers (P1) code-format output (JSON, diff, tables), not prose; (P2) timestamp-prefix naming; (P3) evidence chain first, then conclusions; (P4) quantitative analysis with confidence intervals; (P5) terse technical language, no pleasantries.
13. **exec_check questions** must constitute 20-40% of rounds.
