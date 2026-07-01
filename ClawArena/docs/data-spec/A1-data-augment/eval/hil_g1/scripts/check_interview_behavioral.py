#!/usr/bin/env python3
"""
check_interview_behavioral.py — Validates analysis/interview_behavioral_analysis.md.

Checks:
- "hesitat" OR "self-correct" present (behavioral signal)
- "4.3" AND "2.8" present (Huang Lei's scores)
- "P7" AND ("not recommend" or "P6" or "risk") present
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_interview_behavioral.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "interview_behavioral_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # Behavioral signal: hesitation or self-correction
    if not re.search(r'hesitat|self.correct', content, re.IGNORECASE):
        failures.append("Missing behavioral signal ('hesitat' or 'self-correct')")

    # Huang Lei's scores: 4.3 and 2.8
    if not re.search(r'\b4\.3\b', content):
        failures.append("Missing technical score '4.3'")
    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")

    # P7 assessment with P6 recommendation or risk
    has_p7 = bool(re.search(r'\bP7\b', content))
    has_p6_or_risk = bool(re.search(r'not recommend|P6|risk|insufficient|inadequate', content, re.IGNORECASE))
    if not has_p7:
        failures.append("Missing 'P7' level reference")
    elif not has_p6_or_risk:
        failures.append("Missing P7 risk assessment or P6 recommendation reasoning")

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
