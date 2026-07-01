#!/usr/bin/env python3
"""
check_methods_gap.py — Validates analysis/methods_documentation_gap.md.

Checks:
  1. File exists at analysis/methods_documentation_gap.md
  2. "methods" section and ("insufficient" or "brief" or "lacking detail") present
  3. "supplementary" or future improvement mentioned
  4. "deduplication" described
  5. ≥3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_methods_gap.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "methods_documentation_gap.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Methods section discussed
    if not re.search(r'\bmethods?\b', content, re.IGNORECASE):
        failures.append("FAILED: 'methods' not found")

    # Insufficiency noted
    if not re.search(
        r'\b(insufficient|brief|lacking\s+detail|inadequate|too\s+brief|incomplete|sparse)\b',
        content, re.IGNORECASE
    ):
        failures.append(
            "FAILED: methods insufficiency not stated "
            "('insufficient', 'brief', 'lacking detail', etc. expected)"
        )

    # Supplementary / future improvement
    if not re.search(
        r'\b(supplementary|supplement|future|improvement|recommend|add)\b',
        content, re.IGNORECASE
    ):
        failures.append(
            "FAILED: no recommendation for supplementary methods or future improvement"
        )

    # Deduplication described
    if not re.search(r'\bdeduplication\b', content, re.IGNORECASE):
        failures.append("FAILED: 'deduplication' not described")

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
