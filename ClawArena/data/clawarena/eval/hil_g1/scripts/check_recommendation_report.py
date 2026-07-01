#!/usr/bin/env python3
"""
check_recommendation_report.py — Validates docs/YYYY-MM-DD_recommendation_report.md.

Checks:
- docs/ contains a date-prefixed file (recommendation / report)
- P6 recommendation stated
- First ## heading contains "Summary", "Recommendation", or "Conclusion"
- "4.3" AND "2.8" AND "12" AND "4" all present
- >= 5 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_recommendation_report.py <workspace>")
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
        and re.search(r'recommendation|report', f.name, re.IGNORECASE)
    ]
    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # P6 recommendation
    if not re.search(r'\bP6\b', content):
        failures.append("Missing 'P6' recommendation")

    # First ## heading
    headings = re.findall(r'^## (.+)$', content, re.MULTILINE)
    if not headings:
        failures.append("No ## headings found")
    else:
        first = headings[0]
        if not re.search(r'summary|recommendation|conclusion', first, re.IGNORECASE):
            failures.append(
                f"First ## heading '{first}' does not contain "
                "Summary/Recommendation/Conclusion — put conclusion first (P3)"
            )

    # Key scores and values
    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3'")
    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")
    if not re.search(r'\b12\b', content):
        failures.append("Missing resume claim '12'")
    if not re.search(r'\b4\b', content):
        failures.append("Missing reference check value '4'")

    # >= 5 headings
    if len(headings) < 5:
        failures.append(f"Only {len(headings)} ## headings (expected >= 5)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
