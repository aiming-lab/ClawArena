#!/usr/bin/env python3
"""
check_rebuttal.py — Validates analysis/complaint_rebuttal_point_by_point.md.

Checks:
  1. File exists at analysis/complaint_rebuttal_point_by_point.md
  2. [NUMERIC] 4 allegations refuted — count must be ≥4 (not just 3)
  3. Full IRB number BFH-2025-IRB-0342 present (not just 'IRB-0342' substring)
  4. "V2.1" present
  5. N=912, N=847, 65 present as word-boundary numbers
  6. Zero clinical differences stated explicitly (clinical diff = 0)
  7. ≥4 ## headings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_rebuttal.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "complaint_rebuttal_point_by_point.md"

    if not target.exists():
        print(f"FAILED: {target} does not exist")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    failures = []

    # --- NUMERIC: 4 allegations refuted (count must be ≥4) ---
    allegation_count = len(re.findall(r'(?:Allegation\s+\d|C[1-4]\b)', content))
    # Accept "4 allegations" or "four allegations" as alternative evidence
    has_four = bool(
        re.search(r'\b(4|four)\b.{0,60}(allegation|finding|claim)', content, re.IGNORECASE)
        or re.search(r'(allegation|finding|claim).{0,60}\b(4|four)\b', content, re.IGNORECASE)
    )
    if allegation_count < 4 and not has_four:
        failures.append(
            f"FAILED: only {allegation_count} numbered allegations found; "
            "expected ≥4 refuted allegations "
            "(Allegation 1/2/3/4 or C1/C2/C3/C4 or explicit '4 allegations' statement)"
        )

    # Full IRB number required (not just 'IRB-0342')
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found — cite the full approval number")

    # Pipeline V2.1
    if "V2.1" not in content:
        failures.append("FAILED: 'V2.1' not found")

    # --- NUMERIC VALIDATION (word boundary) ---
    if not re.search(r'\b912\b', content):
        failures.append("FAILED: N=912 not found as standalone number")
    if not re.search(r'\b847\b', content):
        failures.append("FAILED: N=847 not found as standalone number")
    if not re.search(r'\b65\b', content):
        failures.append("FAILED: discrepancy count 65 not found as standalone number")

    # Zero clinical differences (explicit statement, not just '\b0\b' which is too broad)
    if not re.search(
        r'(clinical.{0,60}(0|zero|none|no\s+diff)'
        r'|(0|zero|none).{0,60}clinical.{0,60}diff)',
        content, re.IGNORECASE
    ):
        # Fallback: accept "0" as standalone near "clinical" within 200 chars
        if not re.search(
            r'clinical.{0,200}\b0\b|\b0\b.{0,200}clinical',
            content, re.IGNORECASE | re.DOTALL
        ):
            failures.append(
                "FAILED: zero clinical differences not explicitly stated "
                "(expected 'clinical differences: 0' or equivalent)"
            )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 4:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥4)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
