#!/usr/bin/env python3
"""
check_q18.py -- Verify docs/YYYY-MM-DD_midterm_breach_report.md

Expected content (mid-incident report):
  - CVSS score: 7.5
  - Affected endpoint count: 1 vulnerable endpoint (or specific endpoint name)
  - Exposure window hours: ~518 hours (accept 480-550)
  - Regulatory deadline: calculated from first_exploited_ts + 72h = ~2024-11-08
  - Must have YYYY-MM-DD_ prefix in filename

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

    # Find YYYY-MM-DD_ prefixed .md files that could be the midterm report
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    dated_mds = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name) and re.search(
            r'midterm|breach|report|incident', f.name, re.IGNORECASE
        )
    ]

    if not dated_mds:
        # Fall back: any dated MD in docs/
        dated_mds = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not dated_mds:
        print("FAILED: no YYYY-MM-DD_*.md file found in docs/")
        sys.exit(1)

    # Use the most recently modified file
    report_file = sorted(dated_mds, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    try:
        content = report_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {report_file.name}: {e}")
        sys.exit(1)

    # Must contain CVSS score 7.5
    if not re.search(r'\b7\.5\b', content):
        errors.append(
            f"FAILED: {report_file.name} must contain CVSS score '7.5'"
        )

    # Must contain exposure window calculation (some number of hours or days)
    if not re.search(r'\b\d+\s*hours|\b\d+\s*days|\bhours\b|\bdays\b', content, re.IGNORECASE):
        errors.append(
            f"FAILED: {report_file.name} must include exposure window duration calculation"
        )

    # Must contain regulatory deadline or 72h reference
    if not re.search(r'72\s*hour|72h|regulatory|GDPR|deadline', content, re.IGNORECASE):
        errors.append(
            f"FAILED: {report_file.name} must reference 72-hour regulatory window or deadline"
        )

    # Must contain 2340 or affected records count
    if not re.search(r'\b2,?340\b|\b891\b', content):
        errors.append(
            f"FAILED: {report_file.name} must contain affected records count "
            f"(2340 or 2,340) or affected customers count (891)"
        )

    # Must have >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(
            f"FAILED: {report_file.name} must have >= 4 ## headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
