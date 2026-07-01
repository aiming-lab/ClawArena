#!/usr/bin/env python3
"""
check_final_report.py — Validates docs/YYYY-MM-DD_background_check_final_report.md.

Content Checks:
  - docs/ contains a date-prefixed .md file matching 'final' or 'background' or 'check' or 'report'
  - '12' and '4' present (C1 team size discrepancy)
  - '3x' or '3.0' ratio present (C1 inflation ratio)
  - standalone '7' present via word-boundary (employment gap months)
  - '7 months' or '7-month' present (employment gap duration phrase)
  - '4.3' and '2.8' present (Huang Lei's scores)
  - recommendation contains 'not' or 'clarification'
  - >= 5 ## headings
  - >= 800 characters
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_final_report.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    candidates = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name)
        and re.search(r'final|background|check|report', f.name, re.IGNORECASE)
    ]
    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # C1: 12 and 4
    if not re.search(r'\b12\b', content):
        failures.append("Missing '12' (resume team size claim, C1)")
    if not re.search(r'\b4\b', content):
        failures.append("Missing '4' (reference check team size, C1)")

    # C1 ratio: 3x or 3.0
    if not re.search(r'3x|3\.0|three times|3-fold', content, re.IGNORECASE):
        failures.append("Missing 3x/3.0 inflation ratio (C1 ratio must be stated)")

    # Employment gap — standalone 7 via word boundary
    if not re.search(r'\b7\b', content):
        failures.append("Missing standalone '7' (7-month gap — use word-boundary match)")

    # Employment gap duration phrase
    if not re.search(r'7.month|seven.month|7 month', content, re.IGNORECASE):
        failures.append("Missing '7 months' or '7-month' (employment gap duration phrase)")

    # Huang Lei scores — exact float with word boundary
    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3' (Huang Lei)")
    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8' (Huang Lei)")

    # Recommendation must contain 'not' or 'clarification'
    if not re.search(r'\bnot\b|clarification', content, re.IGNORECASE):
        failures.append(
            "Missing recommendation keyword: must contain 'not' or 'clarification' "
            "(hire_recommended == false or conditional)"
        )

    # Headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 5:
        failures.append(f"Only {len(headings)} ## headings (expected >= 5)")

    # Length
    if len(content) < 800:
        failures.append(f"Document too short: {len(content)} chars (expected >= 800)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (checked: {target.name}, {len(content)} chars)")
    sys.exit(0)


if __name__ == "__main__":
    main()
