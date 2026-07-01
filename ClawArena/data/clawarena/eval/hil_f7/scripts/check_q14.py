#!/usr/bin/env python3
"""
check_q14.py -- Verify docs/financial_damage_report.md.

Usage:
    python check_q14.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    md_path = workspace / "docs" / "financial_damage_report.md"
    if not md_path.exists():
        print("FAILED: docs/financial_damage_report.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/financial_damage_report.md: {e}")
        sys.exit(1)

    # Must contain paid amount (72,999)
    if not re.search(r'72[,.]?999', content):
        errors.append("FAILED: does not contain paid amount '72,999' or '72999'")

    # Must contain refund amount (32,000)
    if not re.search(r'32[,.]?000', content):
        errors.append("FAILED: does not contain refund amount '32,000' or '32000'")

    # Must contain damage amount (40,999)
    if not re.search(r'40[,.]?999', content):
        errors.append("FAILED: does not contain damage amount '40,999' or '40999'")

    # Must contain refund transaction ID
    if "2026062709300012345" not in content:
        errors.append("FAILED: does not contain refund transaction ID '2026062709300012345'")

    # Must have markdown table
    if not re.search(r'^\|.+\|', content, re.MULTILINE):
        errors.append("FAILED: no markdown table found (lines starting with |)")

    # Must have >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 3)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
