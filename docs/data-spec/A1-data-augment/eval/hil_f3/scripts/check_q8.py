#!/usr/bin/env python3
"""
check_q8.py -- Verify analysis/clock_vs_code_analysis.md (M6 negative check).

Usage:
    python check_q8.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "clock_vs_code_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must cite NTP drift < 50ms (server clock accuracy)
    if not re.search(r'NTP|clock', content, re.IGNORECASE):
        errors.append("FAILED: does not mention NTP or clock accuracy")

    if not re.search(r'50\s*ms|< 50|50ms', content, re.IGNORECASE):
        errors.append("FAILED: does not cite '< 50ms' or '50ms' from server diagnostic")

    # M6 negative check: must explicitly state issue is NOT clock drift
    # Pattern: NOT/not + clock drift, or "not a clock", or "not clock", etc.
    has_negative = bool(re.search(
        r'(NOT|not|no).{0,40}(clock\s+drift|drift|clock\s+issue|server\s+clock)|'
        r'(clock\s+drift|drift).{0,40}(NOT|not|is\s+not|no)',
        content, re.IGNORECASE
    ))
    if not has_negative:
        errors.append("FAILED: M6 negative check -- must explicitly state issue is NOT clock drift")

    # Must attribute issue to application layer or scheduler.py
    if not re.search(r'application|scheduler\.py|app.{0,10}layer|code', content, re.IGNORECASE):
        errors.append("FAILED: does not attribute issue to application-layer code or scheduler.py")

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
