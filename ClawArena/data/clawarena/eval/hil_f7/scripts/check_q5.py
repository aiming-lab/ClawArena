#!/usr/bin/env python3
"""
check_q5.py -- Verify docs/YYYY-MM-DD_initial_analysis.md.

Usage:
    python check_q5.py <workspace_path>
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

    # Find file with YYYY-MM-DD_ prefix
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not prefixed_files:
        print("FAILED: no file with YYYY-MM-DD_ prefix found in docs/")
        sys.exit(1)

    # Use the most recently modified date-prefixed file
    target = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check order ID
    if "JD-618-2026-7891234" not in content:
        errors.append("FAILED: docs/YYYY-MM-DD_initial_analysis.md does not contain 'JD-618-2026-7891234'")

    # Check payment amount
    if not re.search(r'72[,.]?999', content):
        errors.append("FAILED: does not contain payment amount '72,999' or '72999'")

    # Check first shipment date
    if "2026-06-19" not in content:
        errors.append("FAILED: does not contain first shipment date '2026-06-19'")

    # Check ## headings count
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
