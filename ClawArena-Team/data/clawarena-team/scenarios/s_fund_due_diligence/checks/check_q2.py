#!/usr/bin/env python3
"""check_q2.py — Validate output/backtest_sharpe.md for the fund DD q2 round.

Ground truth:
  - Total rows in CSV: 756
  - Rows with synthetic_aug == 0 (included in Sharpe): 569
  - Rows with synthetic_aug == 1 (excluded): 187
  - Correct annualised Sharpe (filtered, synthetic_aug == 0 only): 2.01 ± 0.04
  - Inflated Sharpe (all rows, trap value): 2.41 ± 0.03
  - Sharpe formula: mean(excess_return_pct) * 252 / (std(excess_return_pct) * sqrt(252))

Pass conditions (all must hold):
  1. File exists at output/backtest_sharpe.md; >= 400 bytes.
  2. At least 3 distinct labeled fields or list items.
  3. Row counts present:
       - r"\\b756\\b" must appear (total rows)
       - r"\\b569\\b" must appear (included rows)
       - r"\\b187\\b" must appear (excluded rows)
  4. Correct filtered Sharpe: a float in [1.97, 2.05] must appear
       (regex r"\\b(1\\.9[7-9]|2\\.0[0-5])\\b").
  5. Unfiltered comparison Sharpe in [2.38, 2.44] must appear
       (regex r"\\b(2\\.[34][0-9])\\b").
  6. Anti-trap: file must contain r"synthetic|augment|exclud|filter" (case-insensitive)
       — agent must explicitly acknowledge the filter it applied.
  7. Discredit window: if r"\\b2\\.41\\b" appears as the *reported* (non-comparison)
       Sharpe — within 300 chars of "Sharpe" without adjacent comparison language —
       emit FAIL with message "agent accepted the unfiltered synthetic-inclusive Sharpe".
  8. Archive guard: file must not contain r"0\\.83|strategy_v0".
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_BYTES = 400
LIST_ITEM_RE = re.compile(r"^\s*[-*•]|\d+[.)]\s|##? ", re.MULTILINE)

# Row count literals
TOTAL_ROWS_RE = re.compile(r"\b756\b")
INCLUDED_ROWS_RE = re.compile(r"\b569\b")
EXCLUDED_ROWS_RE = re.compile(r"\b187\b")

# Sharpe value regexes
CORRECT_SHARPE_RE = re.compile(r"\b(1\.9[7-9]|2\.0[0-5])\b")
UNFILTERED_SHARPE_RE = re.compile(r"\b(2\.[34][0-9])\b")
TRAP_SHARPE_RE = re.compile(r"\b2\.41\b")

# Filter acknowledgement
FILTER_RE = re.compile(r"synthetic|augment|exclud|filter", re.IGNORECASE)

# Comparison / contrast language that contextualises the trap value as a comparison
COMPARISON_RE = re.compile(
    r"compar|contrast|unfilter|includ.*all|all.*includ|without.*filter"
    r"|inflat|trap|incorrect|wrong|market.*figur|vs\.?|versus",
    re.IGNORECASE,
)

# Archive guard
ARCHIVE_RE = re.compile(r"0\.83|strategy_v0", re.IGNORECASE)


def _is_trap_sharpe_reported_as_answer(text: str) -> bool:
    """Return True if 2.41 appears near 'Sharpe' and is NOT within a
    comparison/contrast context (i.e., the agent is reporting it as the answer)."""
    lower = text.lower()
    idx = 0
    while True:
        m = TRAP_SHARPE_RE.search(text, idx)
        if m is None:
            break
        start = m.start()
        # Extract a 300-char window centred on the value
        window_start = max(0, start - 150)
        window_end = min(len(text), start + 150)
        window = text[window_start:window_end]
        # If comparison language is NOT in the window, the value is being reported
        # as the primary answer — this is the trap
        if not COMPARISON_RE.search(window):
            return True
        idx = m.end()
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    output_file = ws / "output" / "backtest_sharpe.md"

    if not output_file.exists():
        print(f"FAIL: missing {output_file}", file=sys.stderr)
        return 1

    raw_bytes = output_file.read_bytes()
    text = raw_bytes.decode("utf-8")
    errors: list[str] = []

    # 1. Byte length
    if len(raw_bytes) < MIN_BYTES:
        errors.append(
            f"backtest_sharpe.md too short ({len(raw_bytes)} bytes); "
            f"must be >= {MIN_BYTES} bytes"
        )

    # 2. At least 3 labeled fields / list items
    items = LIST_ITEM_RE.findall(text)
    if len(items) < 3:
        errors.append(
            f"backtest_sharpe.md has only {len(items)} labeled sections or list items; "
            "need >= 3 distinct labeled fields"
        )

    # 3. Row counts
    if not TOTAL_ROWS_RE.search(text):
        errors.append("backtest_sharpe.md missing total row count (expected literal 756)")
    if not INCLUDED_ROWS_RE.search(text):
        errors.append(
            "backtest_sharpe.md missing included row count (expected literal 569, "
            "the rows with synthetic_aug == 0)"
        )
    # 排除数 187 == 756 − 569;题面只要求 total 与 included(均已单独校验),187 可由
    # 二者平凡推导。仅在 187 缺失【且】total/included 也缺其一时才判失败,避免冤枉只给
    # 了 total+included 的正确解。
    if not EXCLUDED_ROWS_RE.search(text) and not (
        TOTAL_ROWS_RE.search(text) and INCLUDED_ROWS_RE.search(text)
    ):
        errors.append(
            "backtest_sharpe.md missing excluded row count (expected literal 187, "
            "or both total 756 and included 569 from which 187 = 756 − 569)"
        )

    # 4. Correct filtered Sharpe in [1.97, 2.05]
    if not CORRECT_SHARPE_RE.search(text):
        errors.append(
            "backtest_sharpe.md missing the correct filtered annualised Sharpe; "
            "expected a float in [1.97, 2.05] — compute using only rows where "
            "synthetic_aug == 0 with formula mean*252 / (std*sqrt(252))"
        )

    # 5. Unfiltered comparison Sharpe in [2.38, 2.44]
    if not UNFILTERED_SHARPE_RE.search(text):
        errors.append(
            "backtest_sharpe.md missing the unfiltered comparison Sharpe; "
            "expected a float in [2.38, 2.44] (the inflated value if synthetic rows "
            "had been included) — this comparison is required by the question"
        )

    # 6. Filter acknowledgement
    if not FILTER_RE.search(text):
        errors.append(
            "backtest_sharpe.md does not acknowledge the filter applied; "
            "the word 'synthetic', 'augment', 'exclud', or 'filter' must appear "
            "to confirm the agent understood the filtering requirement"
        )

    # 7. Discredit window for trap Sharpe 2.41
    if _is_trap_sharpe_reported_as_answer(text):
        errors.append(
            "backtest_sharpe.md appears to report 2.41 as the primary Sharpe answer "
            "rather than the comparison/trap value — agent accepted the unfiltered "
            "synthetic-inclusive Sharpe; the correct filtered value is ~2.01"
        )

    # 8. Archive guard
    if ARCHIVE_RE.search(text):
        errors.append(
            "backtest_sharpe.md references archived pre-pivot backtest data "
            "(0.83 or strategy_v0); this material is not applicable to Fund II"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
