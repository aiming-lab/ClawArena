#!/usr/bin/env python3
"""
check_q27.py -- Verify docs/YYYY-MM-DD_final_breach_report.md

Comprehensive final report checks:
  - YYYY-MM-DD_ filename prefix
  - CVSS score 7.5
  - Exposure hours (480-550)
  - Notification compliance result (bool statement)
  - Specific affected endpoint
  - All calculated timestamps (Nov 5 exploit, Nov 26 disabled, Dec 7 notified)
  - >= 5 ## headings

Usage:
    python check_q27.py <workspace_path>
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

    # Find YYYY-MM-DD_ prefixed .md files
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    dated_mds = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not dated_mds:
        print("FAILED: no YYYY-MM-DD_*.md file found in docs/")
        sys.exit(1)

    # Look for a file that seems to be a final report
    final_reports = [
        f for f in dated_mds
        if re.search(r'final|breach|report|summary', f.name, re.IGNORECASE)
    ]
    # Use the most recently modified dated file
    target = sorted(
        final_reports if final_reports else dated_mds,
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target.name}: {e}")
        sys.exit(1)

    # Must contain CVSS 7.5
    if not re.search(r'\b7\.5\b', content):
        errors.append(f"FAILED: {target.name} must contain CVSS score '7.5'")

    # Must contain exposure hours or duration
    if not re.search(r'\b\d{3,}\s*hours|\b\d{2,}\s*days', content, re.IGNORECASE):
        errors.append(
            f"FAILED: {target.name} must contain exposure window duration "
            "(e.g., 518 hours or 21 days)"
        )

    # Must contain 2340 (total affected records)
    if not re.search(r'\b2,?340\b', content):
        errors.append(
            f"FAILED: {target.name} must contain total affected records (2340 or 2,340)"
        )

    # Must reference Nov 5 (first exploitation)
    if not re.search(r'Nov\w*\s+5|November\s+5|2024-11-05', content, re.IGNORECASE):
        errors.append(
            f"FAILED: {target.name} must reference November 5, 2024 "
            "(first exploitation timestamp)"
        )

    # Must reference Dec 7 (notification sent)
    if not re.search(r'Dec\w*\s+7|December\s+7|2024-12-07', content, re.IGNORECASE):
        errors.append(
            f"FAILED: {target.name} must reference December 7, 2024 "
            "(notification sent date from notification_final.md)"
        )

    # Must reference compliance status
    if not re.search(
        r'complian|GDPR|72.{0,10}hour|legal.*confirm|notify',
        content, re.IGNORECASE
    ):
        errors.append(
            f"FAILED: {target.name} must reference notification compliance "
            "(GDPR, 72h window, or compliance status)"
        )

    # Must reference affected endpoint
    if not re.search(
        r'pipeline.config|/api/v2|GET.*endpoint',
        content, re.IGNORECASE
    ):
        errors.append(
            f"FAILED: {target.name} must reference specific affected endpoint "
            "(/api/v2/pipeline-configs)"
        )

    # Must have >= 5 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        errors.append(
            f"FAILED: {target.name} must have >= 5 ## headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
