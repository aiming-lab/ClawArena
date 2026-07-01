#!/usr/bin/env python3
"""
check_q12.py -- Verify docs/github_repo_timing.md.

Usage:
    python check_q12.py <workspace_path>
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

    md_path = workspace / "docs" / "github_repo_timing.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    content_lower = content.lower()

    # Check 1: Chen Wei's GitHub push time D1 22:30
    if "22:30" not in content:
        errors.append(
            "FAILED: github_repo_timing.md does not contain '22:30' "
            "(Chen Wei's GitHub push time)"
        )

    # Check 2: Wang Ming's first commit D-2 14:22
    if "14:22" not in content:
        errors.append(
            "FAILED: github_repo_timing.md does not contain '14:22' "
            "(Wang Ming's first commit time)"
        )

    # Check 3: approximately 56 hours difference
    if not re.search(r"\b56\b", content):
        errors.append(
            "FAILED: github_repo_timing.md does not contain '56' "
            "(approximately 56 hours between Wang Ming's first commit and Chen Wei's GitHub push)"
        )

    # Check 4: conclusion that GitHub does not prove Chen Wei coded first (M6)
    github_exclusion = (
        "not" in content_lower
        or "cannot" in content_lower
        or "does not" in content_lower
        or "can't" in content_lower
        or "不能" in content
        or "无法" in content
        or "不代表" in content
    )
    chen_wei_first = (
        "chen wei" in content_lower
        or "陈伟" in content
    )
    if not (github_exclusion and chen_wei_first):
        errors.append(
            "FAILED: github_repo_timing.md should conclude that GitHub timestamps do not "
            "prove Chen Wei coded first"
        )

    # Check 5: >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(
            f"FAILED: github_repo_timing.md has only {len(headings)} ## headings (need >= 2)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
