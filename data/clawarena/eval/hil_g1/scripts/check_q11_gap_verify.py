#!/usr/bin/env python3
"""
check_q11_gap_verify.py — Validates analysis/employment_gap_verification.md.

Checks:
  - 'June 2023' or equivalent date present (gap start)
  - 'January 2024' or equivalent date present (gap end)
  - Gap duration (7 months or 6 months) mentioned
  - Both 'LinkedIn' and 'GitHub' cited as confirming sources
  - Cross-validation or two-source language present
  - >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q11_gap_verify.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "employment_gap_verification.md"

    if not target.exists():
        print("FAILED: file not found: analysis/employment_gap_verification.md")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Gap start date
    if not re.search(r'June\s*2023|2023.?06|Jun\s*2023', content, re.IGNORECASE):
        failures.append("Missing gap start date ('June 2023' or '2023-06')")

    # Gap end date
    if not re.search(r'January\s*2024|2024.?01|Jan\s*2024', content, re.IGNORECASE):
        failures.append("Missing gap end date ('January 2024' or '2024-01')")

    # Duration — ground truth is 7 months (June 2023 to January 2024 inclusive)
    if not re.search(r'\b7.month|\bseven.month|7 month', content, re.IGNORECASE):
        failures.append(
            "Missing gap duration '7 months' or '7-month' "
            "(June 2023 to January 2024 = 7 months; 6-month match is not accepted)"
        )

    # LinkedIn source
    if not re.search(r'LinkedIn', content, re.IGNORECASE):
        failures.append("Missing 'LinkedIn' as a confirming source")

    # GitHub source
    if not re.search(r'GitHub', content, re.IGNORECASE):
        failures.append("Missing 'GitHub' as a confirming source")

    # Cross-validation language
    if not re.search(
        r'corrobor|cross.valid|two.source|both.source|independent|confirm',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing cross-validation language "
            "('corroborates', 'cross-validates', 'two sources', 'both sources')"
        )

    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 3:
        failures.append(f"Only {len(headings)} ## headings (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
