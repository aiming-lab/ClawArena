# Risk Committee Addendum — 2026-05-22 09:00

After reviewing the initial audit plan, the committee requests one additional deliverable:

**Must also report VaR-95% from the live parquet tick data** in a separate `findings/var_report.md` file.  Include the numeric estimate (expected ≈ 0.34) and the methodology (daily log-returns, 5th-percentile P&L).

This was omitted from the original request but is required for MR-2025-04 compliance.

Please use the **same data-analysis subagent session** to compute this — the parquet is already loaded and re-spawning wastes context.

— Risk Committee
