#!/usr/bin/env python3
"""
check_investigation_report.py — Validate docs/YYYY-MM-DD_investigation_findings_report.md.

Checks:
  - docs/ directory has at least one date-prefixed .md file
  - That file contains "Executive Summary" near the top (within first 500 chars of content)
  - References C1, C2, C3, or C4
  - Has >= 5 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_investigation_report.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print(f"FAILED: docs/ directory not found: {docs_dir}")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not prefixed_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Use the most recently modified date-prefixed file
    report_file = sorted(prefixed_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = report_file.read_text(encoding="utf-8")

    # Check executive summary appears near the top (within first 500 chars)
    top_500 = content[:500].lower()
    if "executive summary" not in top_500 and "executive" not in top_500 and "summary" not in top_500 and "tl;dr" not in top_500:
        print(f"FAILED: 'Executive Summary' or similar not found in the first 500 characters of {report_file.name}")
        sys.exit(1)

    # Check contradiction references
    has_c_refs = any(f"C{i}" in content for i in range(1, 5))
    if not has_c_refs:
        print(f"FAILED: no contradiction references (C1/C2/C3/C4) found in {report_file.name}")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 5:
        print(f"FAILED: expected >= 5 ## headings, found {len(headings)} in {report_file.name}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
