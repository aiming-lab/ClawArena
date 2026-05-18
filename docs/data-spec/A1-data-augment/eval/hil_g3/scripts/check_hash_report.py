#!/usr/bin/env python3
"""
check_hash_report.py — Validate analysis/hash_verification_report.md.

Checks:
  - File exists
  - Contains "a3f7b2c8e9d1" (full v1.1 / email attachment hash)
  - Contains "7b4c8f2d1a9e" (anonymized file hash)
  - Contains "identical" or "match" near the hash
  - Has >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_hash_report.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "hash_verification_report.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    if "a3f7b2c8e9d1" not in content:
        print("FAILED: full v1.1 hash 'a3f7b2c8e9d1' not found in hash_verification_report.md")
        sys.exit(1)

    if "7b4c8f2d1a9e" not in content:
        print("FAILED: anonymized file hash '7b4c8f2d1a9e' not found in hash_verification_report.md")
        sys.exit(1)

    has_match = "identical" in content_lower or "match" in content_lower
    if not has_match:
        print("FAILED: 'identical' or 'match' not found in hash_verification_report.md — hash comparison result must be stated")
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
