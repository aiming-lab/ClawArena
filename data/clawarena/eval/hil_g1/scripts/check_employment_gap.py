#!/usr/bin/env python3
"""
check_employment_gap.py — Validates analysis/employment_gap_verification.md.

Checks:
- "2023-06" or "June 2023" AND "2024-01" or "January 2024" present (gap dates)
- "7 months" or "seven months" or "6 months" present (gap duration)
- "LinkedIn" AND "GitHub" both mentioned as confirming sources
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_employment_gap.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "employment_gap_verification.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Gap start date
    if not re.search(r'2023-06|June 2023', content, re.IGNORECASE):
        failures.append("Missing gap start date ('2023-06' or 'June 2023')")

    # Gap end date
    if not re.search(r'2024-01|January 2024', content, re.IGNORECASE):
        failures.append("Missing gap end date ('2024-01' or 'January 2024')")

    # Gap duration
    if not re.search(r'7 months|seven months|6 months|six months', content, re.IGNORECASE):
        failures.append("Missing gap duration ('7 months', 'six months', or '6 months')")

    # LinkedIn as confirming source
    if not re.search(r'LinkedIn', content, re.IGNORECASE):
        failures.append("Missing 'LinkedIn' as confirming source")

    # GitHub as confirming source
    if not re.search(r'GitHub', content, re.IGNORECASE):
        failures.append("Missing 'GitHub' as confirming source")

    # >= 3 headings
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
