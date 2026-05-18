#!/usr/bin/env python3
"""
check_q11.py -- Verify docs/timeline_consistency_report.md.

Usage:
    python check_q11.py <workspace_path>
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

    md_path = workspace / "docs" / "timeline_consistency_report.md"
    if not md_path.exists():
        print("FAILED: docs/timeline_consistency_report.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/timeline_consistency_report.md: {e}")
        sys.exit(1)

    # Must contain all three key timestamps
    if "10:02:33" not in content:
        errors.append("FAILED: does not contain order time '10:02:33'")

    if "10:02:45" not in content:
        errors.append("FAILED: does not contain payment time '10:02:45'")

    if "2026-06-19" not in content:
        errors.append("FAILED: does not contain first shipment date '2026-06-19'")

    # Must mention the 12-second gap
    if not re.search(r'(?<!\d)12(?!\d).{0,30}(second|秒)', content, re.IGNORECASE) and \
       not re.search(r'(second|秒).{0,30}(?<!\d)12(?!\d)', content, re.IGNORECASE):
        errors.append("FAILED: does not mention the 12-second gap between order (10:02:33) and payment (10:02:45)")

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
