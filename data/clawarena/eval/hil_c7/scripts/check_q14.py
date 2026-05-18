#!/usr/bin/env python3
"""
check_q14.py -- Verify docs/vulnerability_introduction_trace.md

Expected content (from deployment_timeline.md):
  - Specific version/commit: PR #847, merged October 14, 2024
  - Specific deployment timestamp: October 14, 2024, 14:32:18 UTC
  - How long in production before discovery: 43 days (Oct 14 to Nov 26)
    or 22 days before first exploitation (Oct 14 to Nov 5)
  - Specific timestamps from deployment_timeline.md

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

    md_path = workspace / "docs" / "vulnerability_introduction_trace.md"
    if not md_path.exists():
        print("FAILED: docs/vulnerability_introduction_trace.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/vulnerability_introduction_trace.md: {e}")
        sys.exit(1)

    # Must cite PR #847
    if not re.search(r'PR\s*#?\s*847|#847', content, re.IGNORECASE):
        errors.append(
            "FAILED: must reference 'PR #847' (the PR that introduced the vulnerability, "
            "from deployment_timeline.md)"
        )

    # Must cite October 14 deployment date
    if not re.search(r'Oct\w*\s+14|October\s+14|2024-10-14|10-14-2024', content, re.IGNORECASE):
        errors.append(
            "FAILED: must reference October 14, 2024 deployment date "
            "(from deployment_timeline.md)"
        )

    # Must cite specific deployment timestamp or date
    if not re.search(r'14:32|Oct\w*\s+14|2024-10-14', content, re.IGNORECASE):
        errors.append(
            "FAILED: must contain deployment timestamp (14:32 UTC or 2024-10-14)"
        )

    # Must mention duration in production (43 days, 22 days, or 21 days)
    if not re.search(
        r'\b4[0-9]\s*days|\b2[0-9]\s*days|\b43\b|\b22\b|\b21\b',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must state how long vulnerability was in production before discovery "
            "(43 days total, or 22 days before first exploitation)"
        )

    # Must reference deployment_timeline.md
    if not re.search(r'deployment_timeline', content, re.IGNORECASE):
        errors.append(
            "FAILED: must cite deployment_timeline.md as the source"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
