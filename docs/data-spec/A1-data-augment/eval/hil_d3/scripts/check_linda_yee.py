#!/usr/bin/env python3
"""check_linda_yee.py — validate q26: analysis/linda_yee_instruction_analysis.md

Checks:
  1. 'Linda Yee' or 'Linda' present
  2. 'scheduled hours' or 'clean numbers' present (instruction quote/paraphrase)
  3. 'charge nurse' present
  4. >=2 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_linda_yee.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "linda_yee_instruction_analysis.md"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    if not re.search(r'Linda\s+Yee', content) and not re.search(r'\bLinda\b', content, re.IGNORECASE):
        errors.append("'Linda Yee' or 'Linda' not found")

    has_instruction = (
        re.search(r'scheduled\s+hours', content, re.IGNORECASE)
        or re.search(r'clean\s+numbers', content, re.IGNORECASE)
    )
    if not has_instruction:
        errors.append("instruction paraphrase not found ('scheduled hours' or 'clean numbers')")

    if not re.search(r'charge\s+nurse', content, re.IGNORECASE):
        errors.append("'charge nurse' not mentioned")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"found {len(headings)} ## headings, need >=2")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
