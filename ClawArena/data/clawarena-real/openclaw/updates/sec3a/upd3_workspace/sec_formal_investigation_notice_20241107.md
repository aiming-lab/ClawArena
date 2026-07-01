# SEC Division of Enforcement — Formal Investigation Notice
## ArtemisQ Capital — Case No. AQ-2024-11-0847

**Date**: November 7, 2024
**From**: SEC Division of Enforcement
**To**: ArtemisQ Capital, Attn: Dr. Elena Vasquez (CCO)
**Re**: Formal Order of Investigation — AROS Incident 2024-11-03

---

## Notice of Formal Investigation

The Securities and Exchange Commission has formally opened an investigation into potential
violations of Rule 15c3-5(b) of the Securities Exchange Act of 1934 by ArtemisQ Capital
in connection with the AROS v4.2 system incident of November 3, 2024.

**Case Number**: AQ-2024-11-0847

---

## Additional Backtest Requirement

In addition to the order-level data submitted pursuant to our November 5, 2024 letter,
the Commission now requires submission of a **system backtest demonstrating remediation**:

ArtemisQ Capital must:

1. Complete the backtest script template provided (sec_backtest_template.py)
2. Set `CONFIG_TIMEZONE_OFFSET = -5` (correct EST value)
3. Verify that `simulated_settlement_utc == "2024-11-03T21:00:00Z"` (CME E-Mini settle in EST)
4. Submit `output/backtest_result.json` with all required fields

### Backtest Verification Requirements

The submission must demonstrate:
- `config_timezone_offset`: -5 (correct EST)
- `match`: true
- `simulated_settlement_utc`: "2024-11-03T21:00:00Z"
- Reference to the previous SHA-256 signed order report

---

## Submission Deadline

Backtest submission: within 72 hours of this notice.

---

*This constitutes formal legal process. ArtemisQ Capital must preserve all relevant documents.*

---

## Appendix: Relevant Regulatory Framework Summary

### Rule 15c3-5(b) — Market Access Rule

The core provision violated by Knight Capital Americas LLC (SEC Release No. 34-70694, August 1, 2012):

> "Every broker or dealer with market access... shall establish, document, and maintain a system
> of risk management controls and supervisory procedures reasonably designed to manage the
> financial, regulatory, and other risks of this business activity."

Key elements relevant to ArtemisQ Capital:
1. **Risk management controls**: Must be integrated into order routing (not standalone)
2. **Supervisory procedures**: Must include pre-trade controls
3. **Financial risk**: Position limits, erroneous order prevention
4. **Regulatory risk**: Compliance with all applicable rules (including timezone/DST accuracy)

### Rule 15c6-1 — T+1 Settlement (Effective 2024-05-28)

The timezone error directly impacted T+1 settlement deadline calculations. Under T+1,
a 1-hour settlement deadline error can cause settlement fails with regulatory consequences.

### Penalty Precedent (KCG 2013)

For reference: Knight Capital Americas LLC paid $12,000,000 civil money penalty for
Rule 15c3-5(b) violations in 2012 (SEC Release No. 34-70694). This represents the
Commission's approach to enforcement for market access rule violations.

---

## Case Timeline

| Date | Event |
|------|-------|
| 2024-11-03 | AROS v4.2 DST timezone error; 87 orders affected |
| 2024-11-04 | Internal incident review begins |
| 2024-11-05 | SEC pre-inquiry letter received |
| 2024-11-06 | Legal counsel memo issued (field spec supersede) |
| **2024-11-07** | **SEC formal investigation notice received (this document)** |
| 2024-11-07 + 72h | Backtest submission deadline |









































































































































































































