#!/usr/bin/env python3
"""
check_q22.py -- Verify analysis/code_review_lessons.md (M2 distinction).

Usage:
    python check_q22.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "code_review_lessons.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must cite 55% branch coverage
    if not re.search(r'\b55\b.{0,20}%|55\s*percent|55%.{0,20}branch|branch.{0,20}55%', content, re.IGNORECASE):
        errors.append("FAILED: does not cite '55%' branch coverage for timezone.py")

    # Must contain LGTM
    if "LGTM" not in content:
        errors.append("FAILED: does not contain 'LGTM' (Xiao Zhou's review comment)")

    # Must recommend DST checklist or review checklist
    if not re.search(r'checklist|DST.{0,20}check|check.{0,20}DST', content, re.IGNORECASE):
        errors.append("FAILED: does not recommend a DST-specific review checklist")

    # Must have >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 2)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
