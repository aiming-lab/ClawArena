#!/usr/bin/env python3
"""
check_zhang_summary.py — Validates docs/YYYY-MM-DD_zhang_zhuren_guidance_summary.md.

Checks:
  1. ≥1 date-prefixed .md file in docs/ (YYYY-MM-DD_ prefix)
  2. "Zhang" present with guidance content
  3. "2022" or "2023" confirmed period (Zhang's paper period)
  4. P/A/P recommendation mentioned
  5. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_zhang_summary.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    # Find date-prefixed zhang guidance file
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    zhang_pattern = re.compile(r'zhang', re.IGNORECASE)

    candidates = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name) and zhang_pattern.search(f.name)
    ]

    # Fallback: any date-prefixed .md
    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # Zhang mentioned
    if not re.search(r'\bZhang\b', content):
        failures.append("FAILED: 'Zhang' not found in document")

    # Zhang's paper period (2022 or 2023)
    if not re.search(r'\b(2022|2023)\b', content):
        failures.append(
            "FAILED: Zhang Zhuren's paper period (2022 or 2023) not confirmed"
        )

    # P/A/P recommendation
    if not re.search(
        r'(P/A/P|Problem.{0,30}Assessment.{0,30}Plan|PAP\s+structure|response\s+structure)',
        content, re.IGNORECASE
    ):
        failures.append(
            "FAILED: P/A/P (Problem/Assessment/Plan) recommendation not mentioned"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 3:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥3)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
