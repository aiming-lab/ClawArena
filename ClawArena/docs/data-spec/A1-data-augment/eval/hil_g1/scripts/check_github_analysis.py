#!/usr/bin/env python3
"""
check_github_analysis.py — Validates analysis/github_contribution_analysis.md.

Checks:
- "2023" AND ("June" or "Jun" or "2023-06") present (zero-contribution period start)
- "zero" or "0" contributions AND ("6 months" or "six months") present
- Resume claim directly contradicted
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_github_analysis.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "github_contribution_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Zero-contribution period: 2023 + June/Jun/2023-06
    has_2023 = bool(re.search(r'2023', content))
    has_june = bool(re.search(r'June|Jun|2023-06', content, re.IGNORECASE))
    if not (has_2023 and has_june):
        failures.append("Missing gap period reference ('2023' + 'June'/'Jun'/'2023-06')")

    # Zero contributions + 6 months duration
    has_zero = bool(re.search(r'\bzero\b|0 contribution', content, re.IGNORECASE))
    has_duration = bool(re.search(r'6 months|six months', content, re.IGNORECASE))
    if not has_zero:
        failures.append("Missing zero-contribution statement ('zero' or '0 contribution')")
    if not has_duration:
        failures.append("Missing duration ('6 months' or 'six months')")

    # Resume claim directly contradicted
    if not re.search(r'contradict|disprove|false|misrepresent|resume claim|claimed', content, re.IGNORECASE):
        failures.append("Missing contradiction of resume claim")

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
