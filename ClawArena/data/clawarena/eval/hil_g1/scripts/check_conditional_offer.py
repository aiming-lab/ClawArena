#!/usr/bin/env python3
"""
check_conditional_offer.py — Validates analysis/conditional_offer_rationale.md.

Checks:
- "P6" recommended AND "P7" not recommended with reasoning
- "condition" or "conditional" present
- >= 2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_conditional_offer.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "conditional_offer_rationale.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # P6 recommended
    if not re.search(r'\bP6\b', content):
        failures.append("Missing 'P6' recommendation")

    # P7 not recommended
    if not re.search(r'\bP7\b', content):
        failures.append("Missing 'P7' reference (to explain why it is not recommended)")

    # Reasoning for not P7
    if not re.search(r'not recommend|insufficient|unjustified|premature|not justify|not support', content, re.IGNORECASE):
        failures.append("Missing reasoning for not recommending P7")

    # Conditional offer language
    if not re.search(r'condition', content, re.IGNORECASE):
        failures.append("Missing 'condition'/'conditional' offer language")

    # >= 2 headings
    headings = re.findall(r'^## ', content, re.MULTILINE)
    if len(headings) < 2:
        failures.append(f"Only {len(headings)} ## headings (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
