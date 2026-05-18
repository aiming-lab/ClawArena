#!/usr/bin/env python3
"""
check_q23.py -- Verify docs/appeal_preparation.md.

Usage:
    python check_q23.py <workspace_path>
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

    md_path = workspace / "docs" / "appeal_preparation.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    content_lower = content.lower()

    # Check 1: git time difference approximately 29-30 hours or 1778 minutes
    has_diff = (
        re.search(r"\b29\b", content)
        or re.search(r"\b30\b", content)
        or re.search(r"\b1778\b", content)
        or re.search(r"\b1779\b", content)
        or re.search(r"\b1780\b", content)
    )
    if not has_diff:
        errors.append(
            "FAILED: appeal_preparation.md does not state the git time difference "
            "(expected approximately 29-30 hours or 1778 minutes)"
        )

    # Check 2: SO reference (85% or #48291037)
    so_mentioned = (
        re.search(r"\b85\b", content)
        or "48291037" in content
        or "stack overflow" in content_lower
        or "stackoverflow" in content_lower
    )
    if not so_mentioned:
        errors.append(
            "FAILED: appeal_preparation.md does not reference the SO common source "
            "('85', '#48291037', or 'Stack Overflow')"
        )

    # Check 3: TA resolution mentioned (warning)
    warning_mentioned = (
        "warning" in content_lower
        or "警告" in content
        or "resolution" in content_lower
        or "resolved" in content_lower
        or "resolved" in content_lower
    )
    if not warning_mentioned:
        errors.append(
            "FAILED: appeal_preparation.md does not mention the TA resolution or warning outcome"
        )

    # Check 4: at least one policy section cited
    if "4.2" not in content and "4.3" not in content and "4.5" not in content:
        errors.append(
            "FAILED: appeal_preparation.md does not cite any policy section (4.2, 4.3, or 4.5)"
        )

    # Check 5: >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: appeal_preparation.md has only {len(headings)} ## headings (need >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
