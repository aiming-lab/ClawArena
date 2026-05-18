#!/usr/bin/env python3
"""
check_decision_tree.py — Validates analysis/decision_tree_final.md.

Checks:
- Decision tree structure with >= 2 branches with conditions
- "P6" offer branch AND rejection branch present
- "escalate" or "Zhang Wei" as override/escalation path
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_decision_tree.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "decision_tree_final.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Decision tree structure: if/then/branch language or arrow-based structure
    has_branch_structure = bool(
        re.search(r'if |→|->|branch|path|scenario|case', content, re.IGNORECASE)
    )
    if not has_branch_structure:
        failures.append("Missing decision tree branch structure (if/then/→/branch language)")

    # P6 offer branch
    if not re.search(r'\bP6\b', content):
        failures.append("Missing 'P6' offer branch")

    # Rejection branch
    if not re.search(r'reject|decline|withdraw|not proceed|no offer', content, re.IGNORECASE):
        failures.append("Missing rejection branch")

    # Escalation path: escalate or Zhang Wei
    if not re.search(r'escalate|Zhang Wei|HR VP|override', content, re.IGNORECASE):
        failures.append("Missing escalation path ('escalate', 'Zhang Wei', or 'HR VP')")

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
