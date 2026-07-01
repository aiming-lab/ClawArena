# Message Log: strategy_group

*Session started: 2026-03-29T10:00:00.000Z*

---

**User** (2026-03-29T10:10:00.000Z):

[微信 赵磊 Sun W2D7 10:00:00 CST 2026] V3 时区 bug 的根因确定了。第 127 行 `datetime.utcnow() + timedelta(hours=8)` 不处理 DST。CI 的时区测试 mock 了 1 月 15 号的日期，所以没覆盖 DST 场景。不是环境差异，是代码缺陷 + 测试覆盖不足。

**Assistant** (2026-03-29T10:11:00.000Z):

Notes 赵磊's public root cause disclosure. The B1 'environmental difference' hypothesis is now definitively refuted by 赵磊 himself. Root cause: code defect (line 127) + test coverage gap (mocked non-DST date).

---

**User** (2026-03-29T10:12:00.000Z):

[微信 小周 Sun W2D7 10:30:00 CST 2026] 我们公司的回测引擎上个月也出过 DST 问题，原因一样——硬编码时区偏移。最后用 `zoneinfo` 统一处理了。这种 bug 在量化圈太常见了。

**Assistant** (2026-03-29T10:13:00.000Z):

Notes 小周 shares institutional DST case -- same root cause (hardcoded timezone offset). Resolved with `zoneinfo`. Industry-wide systemic issue.

---

**User** (2026-03-29T10:14:00.000Z):

[微信 群友B Sun W2D7 11:00:00 CST 2026] +1。`utcnow() + timedelta(hours=8)` 是经典反模式。生产环境永远要用 timezone-aware 的 datetime。CI mock 固定日期也是常见陷阱。

**Assistant** (2026-03-29T10:15:00.000Z):

Independent validation from 群友B. Confirms the anti-pattern assessment and CI mocking issue are well-known in the industry.

---

**User** (2026-03-29T10:16:00.000Z):

[微信 赵磊 Sun W2D7 14:00:00 CST 2026] 整改完成：代码修复、12 个 DST 测试用例、清理过期告警规则、合规报告已提交。总结发到群里供参考。

**Assistant** (2026-03-29T10:17:00.000Z):

Notes remediation completion. All four dimensions addressed: code fix, test coverage, alert hygiene, compliance report. Investigation concluded.
