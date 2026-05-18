#!/usr/bin/env python3
"""
check_confrontation_framework.py — Validates analysis/confrontation_session_framework.md.

Checks:
- Confrontation questions or criteria listed
- "P6" vs rejection criteria stated
- "honest explanation" condition present
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_confrontation_framework.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "confrontation_session_framework.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Confrontation questions or criteria
    if not re.search(r'question|criteria|ask|prompt|assess|evasion|evasive', content, re.IGNORECASE):
        failures.append("Missing confrontation questions or assessment criteria")

    # P6 vs rejection decision criteria
    if not re.search(r'\bP6\b', content):
        failures.append("Missing 'P6' offer outcome")
    if not re.search(r'reject|decline|withdraw|not proceed', content, re.IGNORECASE):
        failures.append("Missing rejection outcome criteria")

    # Honest explanation condition
    if not re.search(r'honest|candid|transparent|acknowledge|admission', content, re.IGNORECASE):
        failures.append("Missing honest explanation condition")

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
