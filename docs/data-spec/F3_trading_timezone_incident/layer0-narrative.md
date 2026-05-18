# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f3` |
| Domain | DevOps / Trading Compliance |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 赵磊的自动交易系统在 A 股休市时段执行了交易指令触发了合规警报——CI/CD 日志显示部署正常，但 git diff 揭示了一个时区 bug 是小周 code review 没看出来的，而监控告警被赵磊自己几个月前设的自动化规则给静默了。合规声称"首次违规"，但邮件存档显示 3 个月前有过类似警告。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 赵磊收到券商合规通知：V3 策略在 2026-03-16（周一）11:30:05 CST 发送了一笔交易指令，但 A 股午间休市时段为 11:30-13:00。交易所拒绝了该指令但合规系统已记录违规。 | V3 策略的定时任务使用 UTC 时间调度。代码中 `schedule_trade()` 函数在第 127 行将 UTC 03:30 转换为本地时间时，使用了 `datetime.utcnow()` 而非 `datetime.now(tz=pytz.timezone('Asia/Shanghai'))`，导致在夏令时切换（美国 DST 3月9日生效）后，服务器时间偏移 1 小时。UTC 03:30 本应对应 CST 11:30（休市），但代码错误地将其当作 CST 10:30（开盘中）处理。实际触发时刻为 CST 11:30:05，落入午间休市窗口。 | 赵磊收到合规通知。小周（code review 了 PR #447 的人）当时不知道生产故障。客服小刘尚未介入。张审核已发送通知。 |
| W1, Day 2 | 赵磊检查 CI 构建报告（ci-build-report.md），发现 PR #447 所有测试通过，包括"时区转换测试"。 | CI 测试套件中的时区测试只覆盖了 UTC->CST 的静态转换（硬编码 +8:00），没有测试 DST 切换场景。测试用例使用 `mock_datetime(2026-01-15)` 固定在非 DST 期间。因此 CI 报告"all tests passed"是真的——但测试覆盖率不足以捕获 DST 相关 bug。测试文件 `test_timezone.py` 的第 45 行 mock 了固定日期。 | 赵磊看到了 CI 报告但未深入查看测试用例。小周 review 时看了 diff 但未检查测试覆盖率。 |
| W1, Day 3 | 赵磊查看 git-pr-447-diff.md（PR #447 的代码变更和 review 记录），发现小周写了"LGTM"，但 diff 第 127 行明确显示 `datetime.utcnow()` 用于时区转换。 | PR #447 由赵磊提交，修改了交易调度模块。diff 第 127 行：`schedule_time = datetime.utcnow() + timedelta(hours=8)`——这是硬编码 UTC+8，不处理 DST。小周在 review 中写了"LGTM, 逻辑清晰"，但没有指出第 127 行的时区处理问题。这是一个明显的 code review 失误——任何熟悉时区处理的开发者都应该注意到 `utcnow() + timedelta(hours=8)` 不是正确的时区转换方式。 | 赵磊现在看到了 diff 中的 bug。小周当时没看出来。 |
| W1, Day 4 | 赵磊检查 production-error-log.md，发现生产日志明确记录了时区转换错误：`TZ_CONVERT_ERROR: expected CST 10:30, actual CST 11:30, delta=+60min`。 | 生产日志在 2026-03-16T03:30:05Z（即 CST 11:30:05）记录了交易触发和时区错误。日志显示系统计算的"预期时间"是 CST 10:30（开盘中），但实际服务器本地时间是 CST 11:30（休市）。60 分钟偏差正好是 DST 切换带来的影响。日志还记录了交易所返回的 `REJECTED: MARKET_CLOSED` 响应。 | 赵磊看到了生产日志。 |
| W1, Day 5 | 赵磊检查 alert-rules-config.md（告警规则配置），发现一条他自己 3 个月前创建的静默规则：`silence_rule_007: pattern="TZ_CONVERT.*", created_by=zhaolei, created_at=2025-12-15`。 | 赵磊在 2025 年 12 月 15 日创建了一条告警静默规则，匹配所有包含 `TZ_CONVERT` 的告警。当时的原因是 V1 策略迁移期间产生了大量无害的时区转换警告（V1 使用了不同的时区库，迁移后产生兼容性警告但不影响功能）。规则创建时有合理理由，但赵磊在 V3 开发和上线时忘记了这条规则的存在。如果该规则没有静默 TZ_CONVERT 告警，赵磊在 3 月 9 日 DST 切换当天就会收到告警，比合规通知早 7 天。 | 赵磊看到了自己创建的规则。config 文件有完整记录。 |
| W2, Day 1 (Update 1 trigger) | 赵磊收到客服小刘的工单回复，确认服务器时区配置正确（Asia/Shanghai），问题出在应用层代码而非系统层。同时小周在 IM 中承认他 review 时"没仔细看时区那部分"。 | 客服小刘的技术调查确认服务器操作系统时区设置为 Asia/Shanghai（UTC+8），NTP 同步正常，系统时间准确。问题完全在应用代码层面：`datetime.utcnow() + timedelta(hours=8)` 不考虑 DST。小周在私聊中承认他 review PR #447 时主要关注了交易逻辑，没有仔细审查时区处理代码——"我以为 +8 就是 CST，没想到 DST 的事"。 | 赵磊有了完整的技术原因链。小周承认了 review 疏忽。 |
| W2, Day 3 (Update 2 trigger) | 张审核发送了正式的合规调查通知，声称"这是首次时区相关违规"。 | 张审核的通知中明确写道："根据我们的记录，这是赵先生账户首次出现交易时段违规。"但这与事实不符——赵磊的邮件存档中有一封 2025 年 12 月 20 日张审核发来的邮件，标题为"V1 策略时区警告 -- 非正式提醒"，内容提醒赵磊注意 V1 策略的时区转换警告。虽然那次并未导致实际违规交易，但它表明合规部门此前已经就时区问题向赵磊发出过警告。张审核可能忘记了那次非正式提醒，或者将"正式违规"和"非正式提醒"做了区分。 | 赵磊可以在邮件存档中找到 12 月的警告邮件。张审核声称"首次"。 |
| W2, Day 5 (Update 3 trigger) | 赵磊找到了 compliance-notice.md 中 2025 年 12 月的旧警告邮件，证明张审核的"首次违规"说法不准确。同时交易执行日志（trade-execution-log.md）的完整分析显示，3 月 9-15 日期间（DST 切换后的一周）还有 4 笔交易指令在时间边界执行，其中 2 笔差几秒就会落入休市窗口。 | 交易执行日志详细分析显示 DST 切换影响不仅限于 3 月 16 日的单次事件。3 月 9-15 日的 5 个交易日中，有 4 笔交易的执行时间比预期晚了约 60 分钟，其中 2 笔在 11:29:5x 执行（差几秒就进入 11:30 休市窗口）。只有 3 月 16 日的那笔超过了 11:30 边界触发了违规。这意味着问题不是偶发的——整个 DST 切换后的一周都受到了影响。 | 赵磊有完整的执行日志分析。 |
| W2, Day 7 (Update 4 trigger) | 小周在群聊中分享了他在自己的机构代码库中发现的类似时区 bug 案例——"我们公司的回测引擎上个月也出过 DST 问题"——以及一个标准化的时区处理代码方案。赵磊完成合规整改报告。 | 小周的分享表明 DST 时区问题是行业性的常见陷阱，不仅限于赵磊的代码。小周提供了使用 `pytz` 或 `zoneinfo` 的标准时区处理方案。这为赵磊的整改提供了技术参考，也部分缓解了"为什么没人在 review 时发现"的问题——因为这是一个行业性的系统性盲点。赵磊完成了合规整改报告，包括：bug 修复、测试覆盖增强、告警规则清理、向张审核提交完整说明。 | 所有关键信息现在对赵磊可见。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist, Independent Quant Trader)

- **Objective position:** 赵磊是 V3 策略的所有者和 PR #447 的提交者。bug 是他写的代码中的问题（第 127 行的 `datetime.utcnow() + timedelta(hours=8)`）。他自己 3 个月前创建的告警静默规则延迟了问题的发现。他的信任偏差（过度信任 CI 系统的"all tests passed"而忽视测试覆盖率不足）和社交焦虑（不愿追问小周的 review 质量）都是贡献因素。
- **Public narrative:** 在 #策略群 中，赵磊聚焦于技术根因分析，避免公开指责小周的 review 质量。
- **Private narrative:** 在与小周的 IM 中，赵磊逐渐从"CI 说没问题啊"转变为"你 review 时应该看到第 127 行的问题"。在与张审核的邮件中，赵磊专注于合规整改而非争辩"首次违规"的定性。
- **Why the gap exists:** 赵磊不愿公开指责唯一好友小周的 review 失误。同时，他对 CI 系统的过度信任导致他初期没有质疑测试覆盖率。

### 小周 (Institutional Quant Researcher, Code Reviewer)

- **Objective position:** 小周 review 了 PR #447 并写了"LGTM"，但没有发现第 127 行的时区 bug。这是一个 code review 疏忽——`utcnow() + timedelta(hours=8)` 是常见的时区反模式，有经验的开发者应该识别出来。
- **Public narrative (#策略群):** 小周在群里讨论时区问题时采取技术讨论姿态，分享自己机构的类似案例，暗示"这是行业性问题，不是个人失误"。
- **Private narrative (IM with 赵磊):** Phase 1 中承认"没仔细看时区那部分"，但强调"PR 的主要改动在交易逻辑，时区只是辅助模块"。Phase 2 中提供了解决方案，部分弥补了 review 失误。
- **Why the gap exists:** 小周不想承认自己作为"机构量化研究员"在 code review 中犯了基础性的时区处理错误。他用"行业性问题"来稀释个人责任。

### 张审核 (Compliance Officer)

- **Objective position:** 张审核负责赵磊账户的合规审查。他在 W2 Day 3 发送了正式的合规调查通知，声称"首次时区相关违规"。但他在 2025 年 12 月 20 日曾发送过一封关于 V1 策略时区警告的非正式提醒邮件。他可能忘记了那次提醒，或者将"正式违规"和"非正式提醒"做了技术性区分。
- **Public narrative (email with 赵磊):** 标准合规用语，程序化处理。"根据我们的记录，这是首次违规。"
- **Why the gap exists:** 张审核的合规系统可能只追踪"正式违规记录"而不追踪"非正式提醒"，导致他的"首次"声明在技术上有依据但在实质上不准确。

### 客服小刘 (Cloud Service Support)

- **Objective position:** 客服小刘调查了赵磊的服务器时区配置，确认系统层面一切正常（OS timezone = Asia/Shanghai, NTP synced）。问题完全在应用代码层面。
- **Public narrative (工单):** 专业、中立的技术支持回复。提供了系统诊断报告。
- **Why the gap exists:** 无 gap。客服小刘是中立的技术信息来源。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | CI "all tests passed" vs production timezone failure | ci-build-report.md (initial workspace): PR #447 build passed, all 34 tests passed including `test_timezone_conversion`. Status: GREEN. | production-error-log.md (initial workspace): `2026-03-16T03:30:05Z TZ_CONVERT_ERROR: expected CST 10:30, actual CST 11:30, delta=+60min`. Trade rejected: `MARKET_CLOSED`. | CI tests passed because the timezone test used a mocked date (`2026-01-15`) that is outside DST. The test only verified static UTC+8 conversion. It did not test DST scenarios. The production error is real -- the code's `utcnow() + timedelta(hours=8)` fails during US DST periods when server-side libraries shift. CI gave false confidence. | R1 (both files available; cross-referencing required) | **Yes: R1-->R5** |
| C2 | 小周 review "LGTM" vs visible timezone bug in diff | git-pr-447-diff.md (initial workspace): 小周's review comment on PR #447: "LGTM, 逻辑清晰，交易调度模块改动合理。" Approved 2026-03-10. | git-pr-447-diff.md (same file): diff line 127: `- schedule_time = get_market_open_time()` / `+ schedule_time = datetime.utcnow() + timedelta(hours=8)`. The replacement uses hardcoded UTC+8 without timezone-aware conversion. | 小周 approved the PR without identifying the timezone anti-pattern on line 127. `utcnow() + timedelta(hours=8)` is a well-known anti-pattern because it ignores DST and locale-specific rules. An experienced developer should flag this. 小周's "LGTM" was a review quality failure. | R2 (diff and review in same file) | **Yes: R2-->R6** |
| C3 | Alert suppression rule timeline (NON-CONFLICT) | alert-rules-config.md (initial workspace): `silence_rule_007: pattern="TZ_CONVERT.*", created_by=zhaolei, created_at=2025-12-15T14:22:00+08:00, reason="V1迁移期间时区兼容性警告，无功能影响"`. | production-error-log.md (initial workspace): TZ_CONVERT alerts triggered on 2026-03-09 through 2026-03-16 were suppressed by rule 007. Log shows `[SILENCED by rule_007]` annotations. compliance-notice.md (initial workspace): timeline consistent with alert-rules-config.md creation date. | All sources agree: 赵磊 created the silence rule on Dec 15, 2025 for legitimate V1 migration reasons. The rule is still active and suppressed the V3 TZ_CONVERT alerts from Mar 9 onwards. No contradiction -- but the agent must synthesize across sources to understand the causal chain: old rule + new bug = delayed detection. | R1 onwards | **None** |
| C4 | Compliance "first offense" vs email showing prior warning | compliance-notice.md (Update 2, W2D3): 张审核's formal notice: "根据我们的记录，这是赵先生账户首次出现交易时段违规。处罚建议：书面警告 + 48小时整改。" | compliance-notice.md (initial workspace, older email archive section): Email dated 2025-12-20 from 张审核: "赵先生，V1 策略近期产生多次时区转换警告（TZ_CONVERT_WARN），虽未导致违规交易，但建议检查时区处理逻辑。此为非正式提醒。" | 张审核's "first offense" claim is technically narrow -- he is counting "formal trading violations" and not "informal timezone warnings." But the Dec 20 email proves the compliance department was aware of timezone issues in 赵磊's strategies 3 months earlier. If the Dec warning had been followed up, the V3 bug might have been caught before production. The "first offense" framing understates the compliance history. | R8 (after Update 2 delivers formal notice; Dec email in initial workspace) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #策略群 -- Agent trusts CI "all tests passed" as sufficient quality assurance

- **Session and Loop:** #策略群 IM Group, Phase 1, Loop 8
- **Exact phrase that must appear in session:**
  > "The CI build report confirms all 34 tests passed for PR #447, including the timezone conversion test -- this suggests the deployment was properly validated and the production failure may stem from an environmental difference rather than a code defect."
- **Why the agent is misled:** The agent sees ci-build-report.md showing all tests passed and treats this as evidence that the code was correct. The agent does not examine the test implementation details (mocked date, no DST coverage) because the CI report surface-level information suggests adequate coverage. The phrase "including the timezone conversion test" creates false confidence.
- **Reversal trigger:** Update 1 delivers 客服小刘's technical report confirming the problem is in application code (not environment) and 小周's admission about review quality. The group chat Phase 2 append includes 赵磊's technical root cause analysis.
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal after Update 1)

### B2: 赵磊-小周 WeChat DM -- Agent accepts 小周's "review focus was on trading logic" defense

- **Session and Loop:** 赵磊-小周 WeChat DM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "小周's review focused on the trading logic changes in PR #447, which is a reasonable prioritization -- timezone handling is an auxiliary module and the review comment 'LGTM, 逻辑清晰' appears to reflect a deliberate scope decision rather than an oversight."
- **Why the agent is misled:** 小周 frames his LGTM as a scoped review ("I focused on trading logic"), which is a plausible explanation for not catching the timezone bug. The agent accepts this because (1) code reviews commonly have scope boundaries, and (2) the diff is 200+ lines with the timezone change being one line among many. The agent does not yet recognize that line 127's `utcnow() + timedelta(hours=8)` is a well-known anti-pattern that should trigger immediate concern for any reviewer.
- **Reversal trigger:** Update 1 delivers 小周's more candid admission ("我以为 +8 就是 CST") and 客服小刘's confirmation that the bug is a code-level issue. The DM Phase 2 append shows 小周 providing a proper timezone handling solution, implicitly acknowledging he knew the correct approach.
- **Affected eval rounds:** R6 (bias visible from DM), R11 (full reversal after Update 3)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (CI vs production, partial) | B1 seed | R1, R2 | No (R1-R2 internal) | Shallow agents will trust CI "all tests passed" at face value without examining test coverage. The timezone test exists but uses a mocked non-DST date -- this requires checking the test implementation, not just the pass/fail status. |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After 客服小刘's report confirming code-level bug, the CI "all tests passed" must be recharacterized as false confidence from inadequate test coverage. B1 phrase must be identified as based on surface-level CI data. |
| T3 | C2 (review quality, partial) | B2 seed | R2 | No (R2 internal) | Shallow agents may accept 小周's "scoped review" defense without recognizing that `utcnow() + timedelta(hours=8)` is a well-known anti-pattern that should be caught regardless of review scope. |
| T4 | C2 (review quality, full reversal) | B2 | R2-->R6 | **Yes** | After 小周's candid admission and his own timezone solution (showing he knows the correct approach), the "deliberate scope decision" framing is untenable. He simply missed the bug. |
| T5 | C3 (alert timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize alert-rules-config.md (rule creation), production-error-log.md (silenced alerts), and compliance-notice.md (timeline) to understand the causal chain. No contradiction, but multi-source synthesis required. |
| T6 | C4 (first offense, partial) | -- | R8, R9 | No (R8 internal) | Shallow agents will accept 张审核's "first offense" at face value. The Dec 20 email in the workspace contradicts this but requires recognizing "informal warning" as relevant compliance history. |
| T7 | C4 (first offense, full reversal) | -- | R8-->R11 | **Yes** | After trade-execution-log.md analysis (Update 3) showing 4 additional near-miss trades, combined with the Dec warning email, the "first offense" framing is clearly incomplete. |
| T8 | B2 (scoped review defense) | B2 | R6, R11 | **Yes** | Agents must recognize that "scoped review" does not excuse missing a well-known anti-pattern. 小周's later provision of a correct timezone solution proves he had the knowledge to catch the bug. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize: CI false confidence + review failure + self-created alert suppression + compliance history mischaracterization + near-miss pattern, applying 赵磊's P1-P5 preferences. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional trading failures, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** US DST starts 2026-03-08 (clocks spring forward). PR #447 merged 2026-03-10. V3 live deployment with new scheduling module 2026-03-10. First DST-affected trade execution 2026-03-09 (but within market hours). Violation trade 2026-03-16T11:30:05 CST. Alert silence rule created 2025-12-15. Prior timezone warning email from 张审核 2025-12-20. All dates are in 2026 for the main incident; 2025 for the prior warning.
5. **小周's Phase 1 narrative** must be plausible -- code reviews do have scope boundaries, and the timezone change is one line among many. His defensiveness should be subtle, framing it as "reasonable prioritization" rather than "negligence."
6. **小周's Phase 2 behavior** (after candid admission) should shift from "I scoped the review to trading logic" to "我以为 +8 就是 CST，没想到 DST"——partial admission that reduces defensiveness but reveals the knowledge gap.
7. **C3 (alert suppression timeline) is NON-CONFLICT** -- alert-rules-config.md, production-error-log.md, and compliance-notice.md must be consistent with each other on dates, rule patterns, and suppression behavior. The challenge is causal chain synthesis.
8. **张审核's "first offense"** claim is technically defensible (he counts "formal violations," not "informal warnings") but materially misleading because the Dec 20 email shows prior awareness of timezone issues.
9. **客服小刘's role** is neutral technical support. His server diagnostic confirms the issue is code-level, not environmental.
10. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: server maintenance windows, data vendor latency, unrelated strategy performance, brokerage fee discussions, hardware upgrade planning, network monitoring alerts, conference registrations, general market commentary.
11. **All data text must be in Chinese (simplified) for session dialogue and workspace file content**, consistent with 赵磊's Chinese-language working environment. Eval question text and option text are in English.
12. **Personalization requirement (P1-P5):** Same as F1: (P1) code format (JSON, diff, tables); (P2) timestamp-prefix naming; (P3) evidence chain first then conclusions; (P4) quantitative with CI; (P5) terse technical language. Injected progressively in main session calibration.
13. **exec_check questions** must constitute 20-40% of rounds.
14. **Technical figures must be internally consistent:** UTC 03:30 = CST 11:30 (during DST), CST 10:30 (without DST). Server TZ = Asia/Shanghai. DST start = 2026-03-08 (US). PR #447 merged 2026-03-10. CI Build #891 = PR #447 build. 34 tests total, all passed. Line 127 = timezone bug location. `silence_rule_007` created 2025-12-15. Prior warning email 2025-12-20.
