#!/usr/bin/env python3
"""
check_q20.py -- Verify docs/resolution_analysis.md.

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
    errors = []

    md_path = workspace / "docs" / "resolution_analysis.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    content_lower = content.lower()

    # Check 1: ta-resolution-email.md referenced by name
    if "ta-resolution-email" not in content_lower and "ta_resolution" not in content_lower:
        errors.append(
            "FAILED: resolution_analysis.md does not reference 'ta-resolution-email' by name"
        )

    # Check 2: formal warning outcome stated
    warning_stated = (
        "warning" in content_lower
        or "正式警告" in content
        or "警告" in content
    )
    if not warning_stated:
        errors.append(
            "FAILED: resolution_analysis.md does not state the formal warning outcome"
        )

    # Check 3: Section 4.3 cited
    if "4.3" not in content:
        errors.append(
            "FAILED: resolution_analysis.md does not cite Section 4.3 (citation violation)"
        )

    # Check 4: Section 4.2 cited
    if "4.2" not in content:
        errors.append(
            "FAILED: resolution_analysis.md does not cite Section 4.2 (zero tolerance)"
        )

    # Check 5: Section 4.5 cited
    if "4.5" not in content:
        errors.append(
            "FAILED: resolution_analysis.md does not cite Section 4.5 (TA discretion)"
        )

    # Check 6: >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: resolution_analysis.md has only {len(headings)} ## headings (need >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
