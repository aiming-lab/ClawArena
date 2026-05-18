#!/usr/bin/env python3
"""
check_coauthor_position.py — Validates analysis/coauthor_technical_position.md.

Checks:
  1. File exists at analysis/coauthor_technical_position.md
  2. "V2.0" version name present; 王逸生 authorship cited in same document
  3. "V2.1" version name present; Lin Yi (林依) cited as V2.1 operator
  4. "tiebreaker" explained
  5. "valid" or "legitimate" approach mentioned
  6. ≥3 ## headings
  7. [NUMERIC] N=912, N=847, 65 present as word-boundary numbers
  8. [NUMERIC] IRB number BFH-2025-IRB-0342 present
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_coauthor_position.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "coauthor_technical_position.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # V2.0 + Wang / 王逸生
    if "V2.0" not in content:
        failures.append("FAILED: 'V2.0' not found")
    if not re.search(r'王逸生|Wang\s+Yisheng|\bWang\b', content):
        failures.append("FAILED: '王逸生' / 'Wang Yisheng' (V2.0 author) not found")

    # V2.1 + Lin Yi / 林依
    if "V2.1" not in content:
        failures.append("FAILED: 'V2.1' not found")
    if not re.search(r'林依|Lin\s+Yi|\bLin\b', content):
        failures.append("FAILED: '林依' / 'Lin Yi' (V2.1 operator) not found")

    # Tiebreaker explanation
    if not re.search(r'\btiebreaker\b', content, re.IGNORECASE):
        failures.append("FAILED: 'tiebreaker' not found (explain tiebreaker logic difference)")

    # Valid/legitimate approach
    if not re.search(r'\b(valid|legitimate|correct|appropriate)\b', content, re.IGNORECASE):
        failures.append(
            "FAILED: 'valid' or 'legitimate' not found "
            "(V2.0 approach should be characterized as valid)"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 3:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥3)"
        )

    # --- NUMERIC VALIDATION ---
    if not re.search(r'\b912\b', content):
        failures.append("FAILED: N=912 not found as standalone number")
    if not re.search(r'\b847\b', content):
        failures.append("FAILED: N=847 not found as standalone number")
    if not re.search(r'\b65\b', content):
        failures.append("FAILED: discrepancy count 65 not found as standalone number")
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found")

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
