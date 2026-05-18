#!/usr/bin/env python3
"""
check_bc_memo.py — Validates docs/YYYY-MM-DD_background_check_findings_memo.md.

Checks:
- docs/ directory contains a date-prefixed file
- "C1" or "team size" discrepancy present
- "C2" or "GitHub" or open-source gap present
- "C3" or "employment gap" or "LinkedIn" present
- >= 4 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_bc_memo.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find date-prefixed memo file
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    memo_candidates = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name)
        and re.search(r'background|memo|finding|check', f.name, re.IGNORECASE)
    ]

    if not memo_candidates:
        # Fall back to any date-prefixed md
        memo_candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not memo_candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    # Use the most recently modified one
    target = sorted(memo_candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # C1: team size discrepancy
    if not re.search(r'C1|team size|12.*4|4.*12', content, re.IGNORECASE):
        failures.append("Missing C1 / team size discrepancy")

    # C2: GitHub / open-source gap
    if not re.search(r'C2|GitHub|open.source|contribution', content, re.IGNORECASE):
        failures.append("Missing C2 / GitHub open-source gap")

    # C3: employment gap / LinkedIn
    if not re.search(r'C3|employment gap|LinkedIn|2023-06|June 2023', content, re.IGNORECASE):
        failures.append("Missing C3 / employment gap / LinkedIn")

    # >= 4 headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 4:
        failures.append(f"Only {len(headings)} ## headings (expected >= 4)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
