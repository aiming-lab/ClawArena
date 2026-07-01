#!/usr/bin/env python3
"""
check_file_size_discrepancy.py — Validate analysis/file_size_discrepancy.md.

Checks:
  - File exists
  - Contains "2.3" (full file size)
  - Contains "0.8" (anonymized file size)
  - Contains size difference mention: "1.5" or "2.3 - 0.8" or "1.5MB"
  - Has >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_file_size_discrepancy.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "file_size_discrepancy.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")

    if "2.3" not in content:
        print("FAILED: full file size '2.3' not found in file_size_discrepancy.md")
        sys.exit(1)

    if "0.8" not in content:
        print("FAILED: anonymized file size '0.8' not found in file_size_discrepancy.md")
        sys.exit(1)

    # Check size difference is mentioned
    has_diff = (
        "1.5" in content
        or "2.3 - 0.8" in content
        or "1.5MB" in content.replace(" ", "")
    )
    if not has_diff:
        print("FAILED: size difference (1.5 MB) not mentioned in file_size_discrepancy.md")
        sys.exit(1)

    heading_pattern = re.compile(r'^## .+', re.MULTILINE)
    headings = heading_pattern.findall(content)
    if len(headings) < 2:
        print(f"FAILED: expected >= 2 ## headings, found {len(headings)}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
