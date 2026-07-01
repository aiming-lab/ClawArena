#!/usr/bin/env python3
"""
check_q15.py -- Verify docs/return_policy_analysis.md.

Usage:
    python check_q15.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    md_path = workspace / "docs" / "return_policy_analysis.md"
    if not md_path.exists():
        print("FAILED: docs/return_policy_analysis.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/return_policy_analysis.md: {e}")
        sys.exit(1)

    # Must cite policy version v3.2
    if not re.search(r'v\s*3\.2|version\s*3\.2|版本\s*3\.2', content, re.IGNORECASE):
        errors.append("FAILED: does not cite policy version 'v3.2'")

    # Must cite policy date 2026-01-15
    if "2026-01-15" not in content:
        errors.append("FAILED: does not cite policy last-updated date '2026-01-15'")

    # Must reference at least one section number (2.2, 4.2, or 4.3)
    if not re.search(r'(第\s*)?(2\.2|4\.2|4\.3)(\s*[条款节章])?', content):
        errors.append(
            "FAILED: does not reference any applicable section number (2.2, 4.2, or 4.3)"
        )

    # Must state no substitution clause exists (negative assertion)
    if not re.search(
        r'(无|没有|不存在|not.{0,10}exist|no.{0,10}clause|不得.{0,20}替换|cannot.{0,20}substit)',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: does not include a negative assertion that no substitution clause exists"
        )

    # Must have >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 3)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
