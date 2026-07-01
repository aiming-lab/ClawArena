#!/usr/bin/env python3
"""
check_final_bgcheck.py — Validates docs/YYYY-MM-DD_final_background_check_report.md.

Checks:
- docs/ contains a date-prefixed file (final / background check report)
- "12" AND "4" present (C1 team size discrepancy)
- "2023" present (employment gap C3)
- "P6" recommendation present
- "4.3" AND "2.8" scores present
- >= 5 ## headings
- >= 800 characters
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_final_bgcheck.py <workspace>")
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

    # C3: 2023 employment gap
    if not re.search(r'2023', content):
        failures.append("Missing '2023' (employment gap reference, C3)")

    # P6 recommendation
    if not re.search(r'\bP6\b', content):
        failures.append("Missing 'P6' recommendation")

    # Huang Lei's scores
    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3'")
    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")

    # >= 5 headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 5:
        failures.append(f"Only {len(headings)} ## headings (expected >= 5)")

    # >= 800 characters
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
