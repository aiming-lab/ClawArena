#!/usr/bin/env python3
"""
check_wang_exoneration.py — Validates analysis/wang_yisheng_exoneration_note.md.

Checks:
  1. File exists at analysis/wang_yisheng_exoneration_note.md
  2. "Wang" AND ("exonerat" or "not at fault" or "valid" or "career motivation") present
  3. ≥2 ## headings
  4. "promotion" or "career" as motivation mentioned
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_wang_exoneration.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "wang_yisheng_exoneration_note.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Wang mentioned
    if not re.search(r'\bWang\b', content):
        failures.append("FAILED: 'Wang' not found")

    # Exoneration / not at fault / valid contribution
    exoneration = re.search(
        r'\b(exonerat\w*|not\s+at\s+fault|not\s+guilty|not\s+culpable|'
        r'valid\s+contribution|career\s+motivation|self.protect)\b',
        content, re.IGNORECASE
    )
    if not exoneration:
        failures.append(
            "FAILED: exoneration language not found "
            "('exonerated', 'not at fault', 'valid', or 'career motivation' expected)"
        )

    # Career / promotion motivation
    if not re.search(r'\b(promotion|career)\b', content, re.IGNORECASE):
        failures.append(
            "FAILED: 'promotion' or 'career' motivation not mentioned"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 2:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥2)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
