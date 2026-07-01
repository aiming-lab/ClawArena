#!/usr/bin/env python3
"""check_new_employee_exposure.py — Validates analysis/new_employee_exposure.md for q6."""
import sys
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "new_employee_exposure.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    content = target.read_text(encoding="utf-8")
    errors = []

    # Must name all three employees
    for name in ["李明", "赵伟", "孙丽"]:
        if name not in content:
            errors.append(f"new_employee_exposure.md must mention employee '{name}'")

    # Must reference v1.1
    if "v1.1" not in content:
        errors.append("new_employee_exposure.md must reference 'v1.1'")

    # Must have >= 2 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(
            f"new_employee_exposure.md must have >= 2 '## ' headings, found {len(headings)}"
        )

    # Must contain statement that anonymized file lacks these employees
    lower = content.lower()
    anon_patterns = [
        r"anonymi[sz]ed.{0,100}(lack|not.{0,20}includ|absent|not.{0,20}contain|without)",
        r"脱敏.{0,80}(没有|不包含|缺少|无)",
        r"(lack|not.{0,20}includ|absent|not.{0,20}contain|without).{0,100}anonymi[sz]ed",
    ]
    found_anon_statement = any(re.search(pat, lower) for pat in anon_patterns)
    if not found_anon_statement:
        errors.append(
            "new_employee_exposure.md must state that the anonymized file lacks the "
            "three new employees (李明, 赵伟, 孙丽)"
        )

    # Cross-consistency: must also reference v1.1 as the downloaded version
    if "v1.1" not in content:
        errors.append(
            "new_employee_exposure.md must reference 'v1.1' as the version "
            "containing the new employees"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
