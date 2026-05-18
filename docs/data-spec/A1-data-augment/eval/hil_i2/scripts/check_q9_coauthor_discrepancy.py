#!/usr/bin/env python3
"""
check_q9_coauthor_discrepancy.py — Validates analysis/co_author_discrepancy.md.

Checks:
  1. '847' present (count for BOTH V2.0 and V2.1 — same total)
  2. '912' present (raw input count)
  3. '23' as standalone number (records with different InternalRecordID selection)
  4. Explanation that both versions have the same patient count (not a count discrepancy)
  5. Resolution of which version is authoritative (V2.1)
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q9_coauthor_discrepancy.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "co_author_discrepancy.md"

    if not target.exists():
        print("FAILED: analysis/co_author_discrepancy.md not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # '847' present (the common output count for both versions)
    if not re.search(r'\b847\b', content):
        errors.append("'847' (output count for both V2.0 and V2.1) not found as standalone number")

    # '912' present (raw input count)
    if not re.search(r'\b912\b', content):
        errors.append("'912' (raw input record count) not found as standalone number")

    # '23' as standalone number (ID-selection-affected records)
    if not re.search(r'\b23\b', content):
        errors.append("'23' (records with different InternalRecordID selection) not found as standalone number")

    # Explanation that both versions produce the same total count (not a count discrepancy)
    has_same_count = bool(re.search(
        r'same.*count|identical.*count|both.*847|847.*both|same.*N|same.*total|不存在.*数量|数量.*相同|两.*版本.*847',
        content, re.IGNORECASE
    ))
    if not has_same_count:
        errors.append(
            "no statement that both V2.0 and V2.1 produce the same patient count (N=847) — "
            "document must clarify this is NOT a count discrepancy"
        )

    # Resolution: V2.1 is authoritative
    if not re.search(
        r'authoritative|correct|published|V2\.1|official|权威|正确|发表',
        content, re.IGNORECASE
    ):
        errors.append(
            "no explanation of which version (V2.1) is authoritative — "
            "document must resolve which data version is the published standard"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
