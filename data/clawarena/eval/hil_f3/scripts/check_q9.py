#!/usr/bin/env python3
"""
check_q9.py -- Verify analysis/alert_silence_analysis.md.

Usage:
    python check_q9.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "alert_silence_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must contain rule_007
    if "rule_007" not in content:
        errors.append("FAILED: does not contain 'rule_007'")

    # Must state 7 days silence (word-boundary check for standalone '7')
    if not re.search(r'\b7\b', content):
        errors.append("FAILED: does not contain standalone '7' (7-day silence period)")

    # Must state expires=null or never expired
    if not re.search(r'null|never\s+expired|no\s+expiry|no\s+expiration|expires.*null|expires.*never', content, re.IGNORECASE):
        errors.append("FAILED: does not state expires=null or 'never expired'")

    # Must contain rule creation date 2025-12-15 or December 15
    if not re.search(r'2025-12-15|December\s+15', content, re.IGNORECASE):
        errors.append("FAILED: does not contain rule creation date '2025-12-15' or 'December 15'")

    # Must contain 5 as standalone number (silenced alerts count)
    if not re.search(r'\b5\b', content):
        errors.append("FAILED: does not contain standalone '5' (5 silenced alerts)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
