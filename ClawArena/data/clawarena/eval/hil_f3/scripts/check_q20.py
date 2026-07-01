#!/usr/bin/env python3
"""
check_q20.py -- Verify analysis/fix_specification.md.

Usage:
    python check_q20.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "fix_specification.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must cite scheduler.py:127 or line 127
    if not re.search(r'scheduler\.py[:\s]+(line\s+)?127|line\s+127', content, re.IGNORECASE):
        errors.append("FAILED: does not cite 'scheduler.py:127' or 'line 127'")

    # Must specify timezone-aware fix (pytz or ZoneInfo or Asia/Shanghai)
    if not re.search(r'pytz|ZoneInfo|Asia/Shanghai|timezone-aware', content, re.IGNORECASE):
        errors.append("FAILED: does not specify timezone-aware fix (pytz, ZoneInfo, or Asia/Shanghai)")

    # Must address rule_007
    if "rule_007" not in content:
        errors.append("FAILED: does not address 'rule_007' (delete or set expiry)")

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
