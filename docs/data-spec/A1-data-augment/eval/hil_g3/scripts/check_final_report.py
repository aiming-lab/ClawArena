#!/usr/bin/env python3
"""
check_final_report.py — Validate docs/YYYY-MM-DD_final_investigation_report.md.

Checks:
  - docs/ has at least one date-prefixed .md file
  - That file has >= 5 ## headings
  - Mentions all 4 contradictions (C1, C2, C3, C4)
  - Mentions both critical timestamps (14:22:17 and 15:03:44)
  - Mentions hash "a3f7b2c8e9d1"
  - Has >= 800 characters
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_final_report.py <workspace>")
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

    if len(content) < 800:
        print(f"FAILED: report {report_file.name} has only {len(content)} characters (expected >= 800)")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 5:
        print(f"FAILED: expected >= 5 ## headings, found {len(headings)} in {report_file.name}")
        sys.exit(1)

    for cid in ["C1", "C2", "C3", "C4"]:
        if cid not in content:
            print(f"FAILED: contradiction '{cid}' not mentioned in {report_file.name}")
            sys.exit(1)

    if "14:22:17" not in content:
        print(f"FAILED: download timestamp '14:22:17' not found in {report_file.name}")
        sys.exit(1)

    if "15:03:44" not in content:
        print(f"FAILED: email send timestamp '15:03:44' not found in {report_file.name}")
        sys.exit(1)

    if "a3f7b2c8e9d1" not in content:
        print(f"FAILED: hash value 'a3f7b2c8e9d1' not found in {report_file.name}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
