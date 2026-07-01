#!/usr/bin/env python3
"""
check_q6.py -- Verify analysis/root_cause_analysis.md.

Usage:
    python check_q6.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "root_cause_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must contain scheduler.py:127 or scheduler.py line 127
    if not re.search(r'scheduler\.py[:\s]+(line\s+)?127', content, re.IGNORECASE):
        errors.append("FAILED: does not contain 'scheduler.py:127' or 'scheduler.py line 127'")

    # Must contain +60 or 60 minutes or 60-minute (M1 numeric check)
    if not re.search(r'\+60|60.{0,10}minute|60-minute', content, re.IGNORECASE):
        errors.append("FAILED: does not contain '+60' or '60 minutes' or '60-minute'")

    # Must contain utcnow (the bug pattern)
    if "utcnow" not in content:
        errors.append("FAILED: does not contain 'utcnow' (the bug pattern must be cited)")

    # M2: Must contrast CI vs production (both must be mentioned)
    has_ci = bool(re.search(r'\bCI\b', content))
    has_production = bool(re.search(r'production|prod', content, re.IGNORECASE))
    if not (has_ci and has_production):
        errors.append("FAILED: M2 contradiction missing -- must contrast CI results vs production behavior")

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
