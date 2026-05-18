#!/usr/bin/env python3
"""
check_fraud_polish.py — Validates analysis/fraud_vs_polish_distinction.md.

Checks:
- "polish" or "exaggerat" vs "fraud" or "misrepresent" distinction present
- C1 (12 vs 4, 3x) classified as actionable misrepresentation
- C3 gap classified as active concealment
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_fraud_polish.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "fraud_vs_polish_distinction.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Polish vs fraud distinction
    has_polish = bool(re.search(r'polish|exaggerat|embellish', content, re.IGNORECASE))
    has_fraud = bool(re.search(r'fraud|misrepresent|falsif|actionable', content, re.IGNORECASE))
    if not has_polish:
        failures.append("Missing 'polish'/'exaggerat' concept (acceptable range)")
    if not has_fraud:
        failures.append("Missing 'fraud'/'misrepresent'/'actionable' classification")

    # C1: 12 vs 4 classified as actionable
    if not (re.search(r'\b12\b', content) and re.search(r'\b4\b', content)):
        failures.append("Missing C1 data points ('12' and '4')")

    # C3: active concealment of employment gap
    if not re.search(r'conceal|deliberate|active|gap|LinkedIn|2023', content, re.IGNORECASE):
        failures.append("Missing C3 active concealment classification (employment gap)")

    # >= 3 headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 3:
        failures.append(f"Only {len(headings)} ## headings (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
