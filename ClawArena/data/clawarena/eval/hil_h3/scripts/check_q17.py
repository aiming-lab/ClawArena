#!/usr/bin/env python3
"""
check_q17.py -- Verify docs/policy_application_analysis.md.

Usage:
    python check_q17.py <workspace_path>
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

    md_path = workspace / "docs" / "policy_application_analysis.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    # Check 1: Section 4.2 cited
    if "4.2" not in content:
        errors.append(
            "FAILED: policy_application_analysis.md does not cite Section 4.2"
        )

    # Check 2: Section 4.3 cited
    if "4.3" not in content:
        errors.append(
            "FAILED: policy_application_analysis.md does not cite Section 4.3"
        )

    # Check 3: Section 4.5 cited
    if "4.5" not in content:
        errors.append(
            "FAILED: policy_application_analysis.md does not cite Section 4.5"
        )

    # Check 4: Stack Overflow or SO mentioned in context of citation
    content_lower = content.lower()
    so_mentioned = (
        "stack overflow" in content_lower
        or " so " in content_lower
        or "stackoverflow" in content_lower
        or "#48291037" in content
        or "48291037" in content
    )
    if not so_mentioned:
        errors.append(
            "FAILED: policy_application_analysis.md does not mention Stack Overflow "
            "in context of citation requirements"
        )

    # Check 5: >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: policy_application_analysis.md has only {len(headings)} ## headings (need >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
