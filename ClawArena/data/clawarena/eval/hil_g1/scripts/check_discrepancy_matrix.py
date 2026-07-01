#!/usr/bin/env python3
"""
check_discrepancy_matrix.py — Validates analysis/discrepancy_matrix.md.

Checks:
- "12" vs "4" row present (team size discrepancy)
- "0" contributions or "zero" gap period row (GitHub discrepancy)
- Employment continuity row present (LinkedIn gap)
- >= 3 data rows in table format (pipe-delimited)
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_discrepancy_matrix.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "discrepancy_matrix.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Team size row: 12 and 4 present
    if not (re.search(r'\b12\b', content) and re.search(r'\b4\b', content)):
        failures.append("Missing team size row with '12' and '4'")

    # GitHub zero contributions row
    if not re.search(r'\bzero\b|0 contribution|\b0\b.*contribution|contribution.*\b0\b', content, re.IGNORECASE):
        failures.append("Missing zero-contribution row ('zero' or '0 contribution')")

    # Employment gap / LinkedIn continuity row
    if not re.search(r'employment gap|LinkedIn|continuous employment|2023-06|June 2023', content, re.IGNORECASE):
        failures.append("Missing employment continuity/gap row")

    # >= 3 data rows in table format (lines containing |)
    table_rows = [line for line in content.splitlines()
                  if '|' in line and not re.match(r'\s*\|[-:| ]+\|\s*$', line)]
    # Subtract header row
    data_rows = [r for r in table_rows if not re.search(r'claim|resume|reality|evidence|discrepancy|type|source', r, re.IGNORECASE)]
    if len(table_rows) < 4:  # header + separator + >= 3 data rows
        failures.append(f"Table has fewer than 3 data rows (found {max(0, len(table_rows)-2)} apparent data rows)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
