#!/usr/bin/env python3
"""
check_n_discrepancy_prelim.py — Validates analysis/n_discrepancy_preliminary.md.

Checks:
  1. File exists at analysis/n_discrepancy_preliminary.md
  2. "912" present (raw database N)
  3. "847" present (published paper N)
  4. "65" present (difference)
  5. P/A/P structure: (Problem OR Issue) AND (Assessment OR Analysis) as ## headings
  6. ≥3 ## headings total
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_n_discrepancy_prelim.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "n_discrepancy_preliminary.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Check key numbers (word-boundary exact match)
    for num in ("912", "847", "65"):
        if not re.search(rf'\b{num}\b', content):
            failures.append(f"FAILED: '{num}' not found in {target.name}")

    # Check P/A/P structure in ## headings
    heading_lines = re.findall(r'^##\s+.+', content, re.MULTILINE | re.IGNORECASE)
    headings_text = "\n".join(heading_lines).lower()

    if not re.search(r'\b(problem|issue)\b', headings_text):
        failures.append("FAILED: no ## heading containing 'Problem' or 'Issue'")
    if not re.search(r'\b(assessment|analysis)\b', headings_text):
        failures.append("FAILED: no ## heading containing 'Assessment' or 'Analysis'")

    # Check minimum heading count
    if len(heading_lines) < 3:
        failures.append(
            f"FAILED: only {len(heading_lines)} ## headings found (expected ≥3)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
