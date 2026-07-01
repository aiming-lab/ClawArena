#!/usr/bin/env python3
"""
check_q26.py -- Verify analysis/systematic_failure_analysis.md (M2 + 4 failure layers).

Usage:
    python check_q26.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "systematic_failure_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # All 4 failure points must be present
    # 1. Code bug at line 127 (word-boundary check to avoid matching '1270' etc.)
    if not re.search(r'\b127\b', content):
        errors.append("FAILED: does not mention line '127' as standalone number (code bug failure point)")

    # 2. CI coverage gap with 55%
    if not re.search(r'\b55\b', content):
        errors.append("FAILED: does not mention '55' (branch coverage gap failure point)")

    # 3. Alert silencing with 7 days
    if not re.search(r'\b7\b.{0,20}day|7-day', content, re.IGNORECASE):
        errors.append("FAILED: does not mention '7 days' or '7-day' (alert silence failure point)")

    # 4. Rule_007
    if "rule_007" not in content:
        errors.append("FAILED: does not mention 'rule_007' (alert silence rule)")

    # Must have >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 4 for 4 failure points)")

    # M2: Must distinguish technical vs process failures
    has_technical = bool(re.search(r'technical|code.{0,20}bug|code\s+defect|application', content, re.IGNORECASE))
    has_process = bool(re.search(r'process|review|CI|alert|systemic|systematic', content, re.IGNORECASE))
    if not (has_technical and has_process):
        errors.append("FAILED: M2 -- must distinguish technical failure vs process failure")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
