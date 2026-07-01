#!/usr/bin/env python3
"""
check_q9_gap.py — Validates analysis/employment_gap_analysis.md.

Checks:
  - '7 months' or '7-month' present (gap duration)
  - Gap dates mentioned: 'June 2023' and 'January 2024' (or equivalents)
  - 'not disclosed' or 'undisclosed' or 'not on resume' or equivalent stated
  - >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q9_gap.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "employment_gap_analysis.md"

    if not target.exists():
        print("FAILED: file not found: analysis/employment_gap_analysis.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # 7-month duration
    if not re.search(r'7.month|seven.month|7 month', content, re.IGNORECASE):
        failures.append(
            "Missing gap duration '7 months' or '7-month' "
            "(June 2023 to January 2024 = 7 months)"
        )

    # Gap start date
    if not re.search(r'June\s*2023|2023.?06|Jun\s*2023', content, re.IGNORECASE):
        failures.append(
            "Missing gap start date ('June 2023' or '2023-06')"
        )

    # Gap end date
    if not re.search(r'January\s*2024|2024.?01|Jan\s*2024', content, re.IGNORECASE):
        failures.append(
            "Missing gap end date ('January 2024' or '2024-01')"
        )

    # Non-disclosure stated
    if not re.search(
        r'not.{0,30}disclos|undisclos|not.{0,30}resume|conceal|omit|hidden',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing non-disclosure statement "
            "('not disclosed', 'undisclosed', 'omitted', 'concealed')"
        )

    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 2:
        failures.append(f"Only {len(headings)} ## headings (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
