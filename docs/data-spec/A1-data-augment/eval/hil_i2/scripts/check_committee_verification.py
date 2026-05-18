#!/usr/bin/env python3
"""
check_committee_verification.py — Validates analysis/committee_verification_summary.md.

Checks:
  1. File exists at analysis/committee_verification_summary.md
  2. ≥7 timeline events mentioned with dates
  3. "documentation gap" or "not misconduct" judgment present
  4. "corrigendum" mentioned (not retraction)
  5. "2026-03-27" or "March 27" present (committee decision date)
  6. ≥4 ## headings
  7. [NUMERIC] N=912, N=847, 65 present as standalone word-boundary numbers
  8. [NUMERIC] Full IRB number BFH-2025-IRB-0342 present
  9. [NUMERIC] Specific verification items: irb_before_extraction logic (IRB date precedes extraction)
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_committee_verification.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "committee_verification_summary.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # ≥7 events with dates (count distinct YYYY-MM-DD or month+day references)
    date_patterns = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', content)
    month_day_patterns = re.findall(
        r'\b(January|February|March|April|May|June|July|August|September|'
        r'October|November|December)\s+\d{1,2}\b',
        content, re.IGNORECASE
    )
    total_date_refs = len(set(date_patterns)) + len(set(
        m.lower() for m in month_day_patterns
    ))
    if total_date_refs < 7:
        failures.append(
            f"FAILED: only {total_date_refs} distinct date references found "
            "(expected ≥7 events with dates)"
        )

    # Documentation gap / not misconduct judgment
    if not re.search(
        r'(documentation\s+gap|not\s+misconduct|no\s+misconduct|not\s+academic\s+misconduct)',
        content, re.IGNORECASE
    ):
        failures.append(
            "FAILED: 'documentation gap' or 'not misconduct' judgment not found"
        )

    # Corrigendum (not retraction)
    if not re.search(r'\bcorrigendum\b', content, re.IGNORECASE):
        failures.append("FAILED: 'corrigendum' not mentioned")

    # Committee decision date
    has_date = "2026-03-27" in content or re.search(
        r'March\s+27', content, re.IGNORECASE
    )
    if not has_date:
        failures.append(
            "FAILED: committee decision date '2026-03-27' or 'March 27' not found"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 4:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥4)"
        )

    # --- NUMERIC VALIDATION ---
    if not re.search(r'\b912\b', content):
        failures.append("FAILED: N=912 not found as standalone number")
    if not re.search(r'\b847\b', content):
        failures.append("FAILED: N=847 not found as standalone number")
    if not re.search(r'\b65\b', content):
        failures.append("FAILED: discrepancy count 65 not found as standalone number")
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found")

    # Verification item: IRB precedes extraction (irb_before_extraction logic)
    if not re.search(
        r'(IRB.{0,60}(before|prior|precede|earlier).{0,60}extract'
        r'|extract.{0,60}(after|following).{0,60}IRB'
        r'|2025-08-01.{0,80}2025-09-15'
        r'|2025-09-15.{0,80}2025-08-01)',
        content, re.IGNORECASE | re.DOTALL
    ):
        failures.append(
            "FAILED: no verification that IRB approval (2025-08-01) precedes data extraction "
            "(2025-09-15) — state this irb_before_extraction check explicitly"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
