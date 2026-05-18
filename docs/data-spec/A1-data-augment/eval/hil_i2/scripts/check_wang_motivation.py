#!/usr/bin/env python3
"""
check_wang_motivation.py — Validates analysis/wang_yisheng_motivation_analysis.md.

Checks:
  1. File exists at analysis/wang_yisheng_motivation_analysis.md
  2. "Wang" present with evidence of attitude shift timeline
  3. "promotion" or "career" or "self-protect" present (motivation)
  4. Distinguishes self-protection from complicity/guilt
  5. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_wang_motivation.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "wang_yisheng_motivation_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Wang mentioned
    if not re.search(r'\bWang\b', content):
        failures.append("FAILED: 'Wang' not found")

    # Attitude shift / timeline
    if not re.search(r'\b(shift|change|evolv|transition|cooper|collabor)\w*\b',
                     content, re.IGNORECASE):
        failures.append(
            "FAILED: attitude shift not described "
            "(expected words like 'shift', 'change', 'cooperative', etc.)"
        )

    # Career / promotion motivation
    if not re.search(r'\b(promotion|career|self.protect)\b', content, re.IGNORECASE):
        failures.append(
            "FAILED: career motivation not mentioned "
            "('promotion', 'career', or 'self-protect' expected)"
        )

    # Distinguishes self-protection from guilt/complicity
    if not re.search(r'\b(complicity|guilt|misconduct|fraud|manipulat)\b',
                     content, re.IGNORECASE):
        failures.append(
            "FAILED: document does not distinguish self-protective behavior from "
            "complicity or guilt"
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

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
