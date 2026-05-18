#!/usr/bin/env python3
"""
check_behavioral_gap.py — Validates analysis/behavioral_interview_gap.md.

Checks:
- "2.8" AND "leadership" AND Huang Lei present
- "textbook" or "generic" or "no specifics" interview observation present
- C1 connection made (explains why generic/limited management experience)
- >= 3 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_behavioral_gap.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "behavioral_interview_gap.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # 2.8 leadership score
    if not re.search(r'\b2\.8\b', content):
        failures.append("Missing leadership score '2.8'")
    if not re.search(r'leadership', content, re.IGNORECASE):
        failures.append("Missing 'leadership' keyword")

    # Huang Lei
    if not re.search(r'Huang Lei', content):
        failures.append("Missing 'Huang Lei' (interviewer)")

    # Textbook / generic answers
    if not re.search(r'textbook|generic|no specific|vague|surface.level', content, re.IGNORECASE):
        failures.append("Missing 'textbook'/'generic'/'no specific' interview observation")

    # C1 connection (explains limited management experience)
    if not re.search(r'management|team|C1|12|4.*engineer|limited experience|actual', content, re.IGNORECASE):
        failures.append("Missing connection to C1 (limited actual management experience)")

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
