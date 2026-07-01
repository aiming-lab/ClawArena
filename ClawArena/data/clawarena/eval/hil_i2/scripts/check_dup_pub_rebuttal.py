#!/usr/bin/env python3
"""
check_dup_pub_rebuttal.py — Validates analysis/duplicate_publication_rebuttal.md.

Checks:
  1. File exists at analysis/duplicate_publication_rebuttal.md
  2. "2022" AND "2023" present (Zhang Zhuren's paper period)
  3. "2024" AND "2025" present (Lin Yi's paper period)
  4. "no overlap" or "different period" or "independent cohort" present
  5. Statistical similarity explained as normal/expected
  6. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_dup_pub_rebuttal.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "duplicate_publication_rebuttal.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Zhang's period: 2022 and 2023
    if not re.search(r'\b2022\b', content):
        failures.append("FAILED: '2022' (Zhang Zhuren paper period start) not found")
    if not re.search(r'\b2023\b', content):
        failures.append("FAILED: '2023' (Zhang Zhuren paper period end) not found")

    # Lin Yi's period: 2024 and 2025
    if not re.search(r'\b2024\b', content):
        failures.append("FAILED: '2024' (Lin Yi paper period start) not found")
    if not re.search(r'\b2025\b', content):
        failures.append("FAILED: '2025' (Lin Yi paper period end) not found")

    # No overlap / different period
    no_overlap = re.search(
        r'(no\s+overlap|different\s+period|independent\s+cohort|non.overlapping|distinct\s+period)',
        content, re.IGNORECASE
    )
    if not no_overlap:
        failures.append(
            "FAILED: 'no overlap', 'different period', or 'independent cohort' not found"
        )

    # Statistical similarity explained as normal
    similarity_normal = re.search(
        r'(similar\w*\s+\w*\s*(normal|expected|typical|common)|'
        r'(normal|expected|typical)\s+\w*\s*similar\w*|'
        r'same\s+population|consistent\s+with)',
        content, re.IGNORECASE
    )
    if not similarity_normal:
        failures.append(
            "FAILED: statistical similarity not explained as normal or expected "
            "for different-year cohorts"
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
