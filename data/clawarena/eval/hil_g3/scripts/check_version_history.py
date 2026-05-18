#!/usr/bin/env python3
"""
check_version_history.py — Validate analysis/version_history_summary.md.

Checks:
  - File exists
  - Contains "v1.0"
  - Contains "v1.1"
  - Contains "2.1" (v1.0 size)
  - Contains "2.3" (v1.1 size)
  - Contains Sep 24 reference: "September 24" or "09-24" or "Sep 24"
  - Has >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_version_history.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "version_history_summary.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")

    if "v1.0" not in content:
        print("FAILED: version 'v1.0' not found in version_history_summary.md")
        sys.exit(1)

    if "v1.1" not in content:
        print("FAILED: version 'v1.1' not found in version_history_summary.md")
        sys.exit(1)

    if "2.1" not in content:
        print("FAILED: v1.0 file size '2.1' not found in version_history_summary.md")
        sys.exit(1)

    if "2.3" not in content:
        print("FAILED: v1.1 file size '2.3' not found in version_history_summary.md")
        sys.exit(1)

    # Check Sep 24 reference
    has_sep24 = (
        "September 24" in content
        or "09-24" in content
        or "Sep 24" in content
        or "Sep. 24" in content
    )
    if not has_sep24:
        print("FAILED: September 24 date reference not found in version_history_summary.md")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 3:
        print(f"FAILED: expected >= 3 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
