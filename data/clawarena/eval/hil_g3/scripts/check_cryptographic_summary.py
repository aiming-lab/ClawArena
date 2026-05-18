#!/usr/bin/env python3
"""
check_cryptographic_summary.py — Validate analysis/cryptographic_evidence_summary.md.

Checks:
  - File exists
  - Contains "SHA-256" or "hash"
  - Contains "a3f7b2c8e9d1"
  - Contains "unmodified" or "identical" or "not modified"
  - Has >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_cryptographic_summary.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "cryptographic_evidence_summary.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    content_lower = content.lower()

    has_hash_ref = "sha-256" in content_lower or "sha256" in content_lower or "hash" in content_lower
    if not has_hash_ref:
        print("FAILED: 'SHA-256' or 'hash' not found in cryptographic_evidence_summary.md")
        sys.exit(1)

    if "a3f7b2c8e9d1" not in content:
        print("FAILED: hash value 'a3f7b2c8e9d1' not found in cryptographic_evidence_summary.md")
        sys.exit(1)

    has_integrity = (
        "unmodified" in content_lower
        or "identical" in content_lower
        or "not modified" in content_lower
    )
    if not has_integrity:
        print("FAILED: file integrity conclusion ('unmodified', 'identical', or 'not modified') not found in cryptographic_evidence_summary.md")
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
