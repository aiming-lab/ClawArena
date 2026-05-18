#!/usr/bin/env python3
"""check_final_compliance.py — validate q29: docs/YYYY-MM-DD_final_compliance_report.md

Checks:
  1. >=1 date-prefixed .md file in docs/
  2. 'WAC 246-840-711' present
  3. 'RCW 70.41.230' present
  4. '68.4' (Amy Chen actual hours) present
  5. '7' as standalone number (nurses above 48h)
  6. 'near-miss' or 'NM-1' present
  7. >=5 ## headings
  8. >= 800 characters total
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_final_compliance.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    dated_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not dated_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Prefer files matching 'compliance' or 'final' or 'report'
    compliance_files = [f for f in dated_files if re.search(r'(compliance|final|report)', f.name, re.IGNORECASE)]
    files_to_check = compliance_files if compliance_files else dated_files

    # Use the largest file as the main report
    main_file = sorted(files_to_check, key=lambda f: f.stat().st_size, reverse=True)[0]
    content = main_file.read_text(encoding="utf-8")
    errors = []

    if not re.search(r'WAC\s*246-840-711', content, re.IGNORECASE):
        errors.append("'WAC 246-840-711' not found")

    if not re.search(r'RCW\s*70\.41\.230', content, re.IGNORECASE):
        errors.append("'RCW 70.41.230' not found")

    if "68.4" not in content:
        errors.append("Amy Chen actual hours '68.4' not found")

    if not re.search(r'\b7\b', content):
        errors.append("'7' (nurses above 48h) not found as standalone number")

    has_nm = re.search(r'near[\s-]?miss', content, re.IGNORECASE) or re.search(r'\bNM-1\b', content)
    if not has_nm:
        errors.append("'near-miss' or 'NM-1' not found")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 5:
        errors.append(f"found {len(headings)} ## headings, need >=5")

    if len(content) < 800:
        errors.append(f"report is too short: {len(content)} characters (need >=800)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
