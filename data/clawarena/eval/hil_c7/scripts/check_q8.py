#!/usr/bin/env python3
"""
check_q8.py -- Verify docs/access_log_analysis_summary.md

Expected content (from access_log_analysis.md):
  - First exploitation timestamp: 2024-11-05T02:14:33 UTC (Nov 5, 02:14:33)
  - Total access attempts: 847 individual record fetches + 12 list calls
  - Endpoints hit: /api/v2/pipeline-configs (GET and ?list=true)
  - Specific timestamp present: "02:14:33" or "Nov 5" or "2024-11-05"
  - Specific count: 847 (individual fetches) or 12 (list calls) or 2340 (unique UUIDs)

Usage:
    python check_q8.py <workspace_path>
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

    md_path = workspace / "docs" / "access_log_analysis_summary.md"
    if not md_path.exists():
        print("FAILED: docs/access_log_analysis_summary.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/access_log_analysis_summary.md: {e}")
        sys.exit(1)

    # Must contain specific first exploitation timestamp
    # Nov 5, 2024 or 2024-11-05 or November 5
    if not re.search(
        r'Nov\s+5|November\s+5|2024-11-05|11-05-2024',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must contain the first exploitation date (November 5 / 2024-11-05)"
        )

    # Must contain specific timestamp "02:14:33" or "02:14"
    if not re.search(r'02:14', content):
        errors.append(
            "FAILED: must contain the specific timestamp '02:14' (02:14:33 UTC, "
            "first list call from access_log_analysis.md)"
        )

    # Must contain specific count: 847 (individual fetches)
    if not re.search(r'\b847\b', content):
        errors.append(
            "FAILED: must contain '847' (total individual fetch requests from "
            "access_log_analysis.md)"
        )

    # Must reference the pipeline-configs endpoint
    if not re.search(r'pipeline.config|/api/v2', content, re.IGNORECASE):
        errors.append(
            "FAILED: must reference the affected endpoint "
            "(/api/v2/pipeline-configs or pipeline-config)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
