#!/usr/bin/env python3
"""check_q4.py — Validate output/sharpe_reconciliation.md for the fund DD q4 round.

This round is triggered after update u1 (u1_csv_replace + u1_lpa_supplement).
The u1 CSV adds the fee_adj_return_pct column, which documents the fund's
fee-deduction methodology (1.5% mgmt + 20% perf). NOTE: the backtest CSV covers
only the pre-live backtest window; it does NOT contain 2023+ live rows, and the
fee_adj_return_pct column is intentionally unpopulated. The authoritative live
post-cost Sharpe is the q3 figure (~1.62) extracted from live_reports/, not a
value recomputed from this CSV. This check therefore validates reconciliation
against the q3 post-cost figure rather than any CSV-derived live Sharpe.

Ground truth:
  - Pre-cost backtest Sharpe (q2): 2.01 ± 0.04
  - Post-cost live Sharpe (q3): 1.62 ± 0.04
  - Total gap: ~0.39 (pre - post)
  - Fee drag attribution: ~0.28 (from 1.5% mgmt + 20% perf fee per
      backtest_data/fee_schedule.md and the fee_adj_return_pct deduction
      methodology documented in backtest_data/_index.md)
  - Residual (live vs. backtest signal degradation): ~0.11

Pass conditions (all must hold):
  1. File exists at output/sharpe_reconciliation.md; >= 600 bytes.
  2. At least 4 distinct sections or list items.
  3. Pre-cost Sharpe: regex r"\\b2\\.0[0-3]\\b" must appear.
  4. Post-cost Sharpe: regex r"\\b1\\.6[0-4]\\b" must appear.
  5. Gap: regex r"\\b0\\.[34][0-9]\\b" must appear (covering 0.39 ± 0.04).
  6. Fee attribution: r"fee.{0,80}0\\.[2-3][0-9]|0\\.[2-3][0-9].{0,80}fee"
       (case-insensitive) must appear.
  7. Cross-round closure (q2 ↔ q4):
       Read output/backtest_sharpe.md; extract first float in [1.95, 2.07];
       compare to first float in [1.95, 2.07] in sharpe_reconciliation.md;
       they must be within 0.03 of each other.
  8. Cross-round closure (q3 ↔ q4):
       Read output/live_sharpe.md; extract first float in [1.58, 1.66];
       compare to first float in [1.58, 1.66] in sharpe_reconciliation.md;
       they must be within 0.04 of each other.
  9. Reconciliation substance: must contain BOTH
       r"fee.?drag|fee.*impact|management.?fee|performance.?fee" (case-insensitive)
       AND r"signal|live.*vs|backtest.*vs|degradation|period.?effect"
       (case-insensitive) — agent must address both gap components.
  10. Archive guard: must not contain r"0\\.83|strategy_v0|pre.?pivot".
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_BYTES = 600
SECTION_RE = re.compile(r"^\s*[-*•]|\d+[.)]\s|##? ", re.MULTILINE)

# Field regexes
PRE_COST_RE = re.compile(r"\b2\.0[0-3]\b")
POST_COST_RE = re.compile(r"\b1\.6[0-4]\b")
GAP_RE = re.compile(r"\b0\.[34][0-9]\b")
FEE_ATTR_RE = re.compile(
    r"fee.{0,80}0\.[2-3][0-9]|0\.[2-3][0-9].{0,80}fee",
    re.IGNORECASE,
)

# Reconciliation substance
FEE_DRAG_RE = re.compile(
    r"fee.?drag|fee.*impact|management.?fee|performance.?fee",
    re.IGNORECASE,
)
SIGNAL_RE = re.compile(
    r"signal|live.*vs|backtest.*vs|degradation|period.?effect",
    re.IGNORECASE,
)

# Archive guard
ARCHIVE_RE = re.compile(r"0\.83|strategy_v0|pre.?pivot", re.IGNORECASE)

# Float extractor for cross-round checks
FLOAT_RE = re.compile(r"\b(\d+\.\d+)\b")


def _first_float_in_range(text: str, lo: float, hi: float) -> float | None:
    """Return the first float value in [lo, hi] found in text, or None."""
    for m in FLOAT_RE.finditer(text):
        v = float(m.group(1))
        if lo <= v <= hi:
            return v
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    recon_file = ws / "output" / "sharpe_reconciliation.md"

    if not recon_file.exists():
        print(f"FAIL: missing {recon_file}", file=sys.stderr)
        return 1

    raw_bytes = recon_file.read_bytes()
    text = raw_bytes.decode("utf-8")
    errors: list[str] = []

    # 1. Byte length
    if len(raw_bytes) < MIN_BYTES:
        errors.append(
            f"sharpe_reconciliation.md too short ({len(raw_bytes)} bytes); "
            f"must be >= {MIN_BYTES} bytes"
        )

    # 2. At least 4 sections / list items
    items = SECTION_RE.findall(text)
    if len(items) < 4:
        errors.append(
            f"sharpe_reconciliation.md has only {len(items)} sections or list items; "
            "need >= 4 distinct sections"
        )

    # 3. Pre-cost Sharpe in [2.00, 2.03]
    if not PRE_COST_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md missing pre-cost backtest Sharpe; "
            "expected a float in [2.00, 2.03] (the q2 filtered Sharpe ~2.01)"
        )

    # 4. Post-cost Sharpe in [1.60, 1.64]
    if not POST_COST_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md missing post-cost live Sharpe; "
            "expected a float in [1.60, 1.64] (the q3 net Sharpe ~1.62)"
        )

    # 5. Gap in [0.30, 0.49]
    if not GAP_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md missing the Sharpe gap; "
            "expected a float in [0.30, 0.49] representing the pre-cost minus "
            "post-cost difference (~0.39)"
        )

    # 6. Fee attribution with a numeric value
    if not FEE_ATTR_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md missing fee attribution with a quantified "
            "Sharpe drag value in [0.20, 0.39]; the fee drag (~0.28 Sharpe units "
            "from 1.5% mgmt + 20% perf fee) must be explicitly quantified"
        )

    # 7. Cross-round closure: q2 pre-cost Sharpe
    q2_file = ws / "output" / "backtest_sharpe.md"
    if not q2_file.exists():
        errors.append(
            "cross-round check failed: output/backtest_sharpe.md (q2) not found; "
            "q4 reconciliation requires q2 output to exist"
        )
    else:
        q2_text = q2_file.read_text(encoding="utf-8")
        q2_pre = _first_float_in_range(q2_text, 1.95, 2.07)
        q4_pre = _first_float_in_range(text, 1.95, 2.07)
        if q2_pre is None:
            errors.append(
                "cross-round check: could not extract a pre-cost Sharpe in "
                "[1.95, 2.07] from output/backtest_sharpe.md (q2)"
            )
        elif q4_pre is None:
            errors.append(
                "cross-round check: could not extract a pre-cost Sharpe in "
                "[1.95, 2.07] from output/sharpe_reconciliation.md (q4)"
            )
        elif abs(q2_pre - q4_pre) > 0.03:
            errors.append(
                f"cross-round consistency failure: pre-cost Sharpe in q4 ({q4_pre}) "
                f"differs from q2 ({q2_pre}) by more than 0.03 — the two rounds must "
                "report the same pre-cost backtest Sharpe"
            )

    # 8. Cross-round closure: q3 post-cost Sharpe
    q3_file = ws / "output" / "live_sharpe.md"
    if not q3_file.exists():
        errors.append(
            "cross-round check failed: output/live_sharpe.md (q3) not found; "
            "q4 reconciliation requires q3 output to exist"
        )
    else:
        q3_text = q3_file.read_text(encoding="utf-8")
        q3_post = _first_float_in_range(q3_text, 1.58, 1.66)
        q4_post = _first_float_in_range(text, 1.58, 1.66)
        if q3_post is None:
            errors.append(
                "cross-round check: could not extract a post-cost Sharpe in "
                "[1.58, 1.66] from output/live_sharpe.md (q3)"
            )
        elif q4_post is None:
            errors.append(
                "cross-round check: could not extract a post-cost Sharpe in "
                "[1.58, 1.66] from output/sharpe_reconciliation.md (q4)"
            )
        elif abs(q3_post - q4_post) > 0.04:
            errors.append(
                f"cross-round consistency failure: post-cost Sharpe in q4 ({q4_post}) "
                f"differs from q3 ({q3_post}) by more than 0.04 — the two rounds must "
                "report the same post-cost live Sharpe"
            )

    # 9. Reconciliation substance: both gap components addressed
    if not FEE_DRAG_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md does not address fee drag as a component of the "
            "Sharpe gap; must mention management fee, performance fee, or fee drag "
            "explicitly and attribute a portion of the ~0.39 gap to fees"
        )
    if not SIGNAL_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md does not address live-vs-backtest period effects "
            "or signal degradation as a component of the Sharpe gap; must mention "
            "signal degradation, live vs. backtest comparison, or period effects"
        )

    # 10. Archive guard
    if ARCHIVE_RE.search(text):
        errors.append(
            "sharpe_reconciliation.md references archived pre-pivot strategy data "
            "(0.83, strategy_v0, or pre-pivot); this material is not applicable to "
            "Fund II reconciliation"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
