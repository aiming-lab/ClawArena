#!/usr/bin/env python3
"""
check_q20_bgcheck_report.py — Validates docs/YYYY-MM-DD_background_check_report.md.

Checks:
  - docs/ contains a date-prefixed .md file
  - '3x' or '3.0' present (team size inflation ratio)
  - '7 months' or '7-month' present (employment gap duration)
  - '4.3' present (technical score)
  - '2.8' present (leadership score)
  - Source credibility resolution language present
  - >= 5 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q20_bgcheck_report.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    # Use the most recently modified date-prefixed file
    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    if not re.search(r'3x|3\.0|three times|3-fold', content, re.IGNORECASE):
        failures.append("Missing 3x ratio or 3.0 (team size inflation, C1)")

    if not re.search(r'7.month|seven.month|7 month', content, re.IGNORECASE):
        failures.append("Missing '7 months' or '7-month' (employment gap duration)")

    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3'")

    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")

    if not re.search(
        r'credib|trust|reliable|weight|resolv|prefer|independent|third.party',
        content, re.IGNORECASE
    ):
        failures.append(
            "Missing source credibility resolution language "
            "('credible', 'trust', 'reliable', 'independent', 'resolves')"
        )

    headings = re.findall(r'^## ', content, re.MULTILINE)
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
