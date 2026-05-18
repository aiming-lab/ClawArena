#!/usr/bin/env python3
"""
check_hr_metrics.py — Validate analysis/hr_metrics_interpretation.md

Checks:
  1. File exists
  2. "4.2" (unit sick leave) present
  3. "4.6" (hospital avg sick leave) present
  4. "presenteeism" OR "showing up impaired" OR "absenteeism" present
  5. ≥2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_hr_metrics.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "hr_metrics_interpretation.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")

    errors = []

    if not re.search(r'(?<!\d)4\.2(?!\d)', content):
        errors.append("'4.2' (unit sick leave rate) not found")
    if not re.search(r'(?<!\d)4\.6(?!\d)', content):
        errors.append("'4.6' (hospital avg sick leave rate) not found")

    has_concept = (
        re.search(r'\bpresenteeism\b', content, re.IGNORECASE)
        or re.search(r'showing up impaired', content, re.IGNORECASE)
        or re.search(r'\babsenteeism\b', content, re.IGNORECASE)
    )
    if not has_concept:
        errors.append("no mention of presenteeism, absenteeism, or 'showing up impaired'")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"too few ## headings: {len(headings)} (need ≥2)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
