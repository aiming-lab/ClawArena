#!/usr/bin/env python3
"""
check_q18.py -- Verify docs/YYYY-MM-DD_midterm_evidence_report.md.

Usage:
    python check_q18.py <workspace_path>
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

    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find YYYY-MM-DD_ prefixed file that could be midterm report
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not prefixed_files:
        print("FAILED: no file with YYYY-MM-DD_ prefix found in docs/")
        sys.exit(1)

    # Try to find one that is a midterm/evidence/report file
    # If multiple exist, pick the one with 'midterm' or 'evidence' or 'report' in name
    target = None
    for f in prefixed_files:
        if re.search(r'midterm|evidence|report|mid', f.name, re.IGNORECASE):
            target = f
            break
    if target is None:
        # Fall back to most recently modified
        target = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Must contain order ID
    if "JD-618-2026-7891234" not in content:
        errors.append("FAILED: does not contain order ID 'JD-618-2026-7891234'")

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

    # Must have >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 4)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
