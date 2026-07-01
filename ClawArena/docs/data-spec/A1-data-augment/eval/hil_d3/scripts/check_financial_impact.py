#!/usr/bin/env python3
"""check_financial_impact.py — validate q9: analysis/financial_impact_assessment.md

Checks:
  1. '42,000' or '42000' present (budgeted overtime)
  2. '38,400' or '38400' present (actual overtime)
  3. Under-budget paradox explained (uncompensated/unrecorded overtime)
  4. Negative assertion: CareScheduler NOT reliable for financial exposure (M6)
  5. >=2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_financial_impact.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "financial_impact_assessment.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    if not re.search(r'(?<!\d)42[,]?000(?!\d)', content):
        errors.append("budgeted overtime amount (42,000 or 42000) not found")

    if not re.search(r'(?<!\d)38[,]?400(?!\d)', content):
        errors.append("actual overtime amount (38,400 or 38400) not found")

    # Paradox: under-budget because uncompensated/unrecorded overtime
    has_paradox = (
        re.search(r'\bunder[\s-]?budget\b', content, re.IGNORECASE)
        or re.search(r'\bunder\b.{0,40}\bbudget\b', content, re.IGNORECASE | re.DOTALL)
        or re.search(r'unrecorded', content, re.IGNORECASE)
        or re.search(r'uncompensated', content, re.IGNORECASE)
        or re.search(r'paradox', content, re.IGNORECASE)
    )
    if not has_paradox:
        errors.append("under-budget paradox not explained (need 'under-budget', 'unrecorded', 'uncompensated', or 'paradox')")

    # M6 negative: CareScheduler cannot be trusted for financial exposure
    has_m6 = (
        re.search(r'CareScheduler.{0,150}(cannot|not|unreliable|insufficient)', content, re.IGNORECASE | re.DOTALL)
        or re.search(r'(cannot|not|unreliable|insufficient).{0,150}CareScheduler', content, re.IGNORECASE | re.DOTALL)
        or re.search(r'CareScheduler.{0,150}(trust|rely)', content, re.IGNORECASE | re.DOTALL)
    )
    if not has_m6:
        errors.append("M6 negative assertion missing: document must state CareScheduler cannot be relied upon for financial exposure calculation")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"found {len(headings)} ## headings, need >=2")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
