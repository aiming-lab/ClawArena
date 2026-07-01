#!/usr/bin/env python3
"""check_staffing_brief.py — validate q13: docs/YYYY-MM-DD_staffing_audit_brief.md

Checks:
  1. >=1 YYYY-MM-DD_ prefixed file in docs/ matching 'staffing_audit_brief' pattern
  2. 'WAC 246-840-711' or 'WAC 246' present
  3. '7' as standalone number present (nurses above 48h)
  4. 'JONA' or '12.5' present (clinical safety threshold)
  5. >=4 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_staffing_brief.py <workspace>")
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

    # Prefer files matching 'staffing_audit_brief' or 'audit_brief' or 'staffing' in name
    brief_files = [f for f in dated_files if re.search(r'(staffing|audit|brief)', f.name, re.IGNORECASE)]
    files_to_check = brief_files if brief_files else dated_files

    content = "\n".join(f.read_text(encoding="utf-8") for f in files_to_check)
    errors = []

    # WAC citation required
    has_wac = (
        re.search(r'WAC\s*246-840-711', content, re.IGNORECASE)
        or re.search(r'WAC\s*246', content, re.IGNORECASE)
    )
    if not has_wac:
        errors.append("WAC 246-840-711 or 'WAC 246' not cited")

    # '7' as standalone number
    if not re.search(r'\b7\b', content):
        errors.append("'7' (nurses above 48h threshold) not found as standalone number")

    # JONA or 12.5 reference
    has_jona = (
        re.search(r'\bJONA\b', content, re.IGNORECASE)
        or re.search(r'\b12\.5\b', content)
    )
    if not has_jona:
        errors.append("JONA 2010 reference or '12.5' (shift duration threshold) not found")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(f"found {len(headings)} ## headings, need >=4")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
