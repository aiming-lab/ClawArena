#!/usr/bin/env python3
"""
check_q11.py -- Verify docs/commit_timing_analysis.md.

Usage:
    python check_q11.py <workspace_path>
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

    md_path = workspace / "docs" / "commit_timing_analysis.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    # Check 1: Wang Ming's first commit time 14:22
    if "14:22" not in content:
        errors.append(
            "FAILED: commit_timing_analysis.md does not contain '14:22' "
            "(Wang Ming's first commit time)"
        )

    # Check 2: Chen Wei's first commit time 20:00
    if "20:00" not in content:
        errors.append(
            "FAILED: commit_timing_analysis.md does not contain '20:00' "
            "(Chen Wei's first GitLab commit time)"
        )

    # Check 3: time difference approximately 29-30 hours or 1778 minutes
    has_diff = (
        re.search(r"\b29\b", content)
        or re.search(r"\b30\b", content)
        or re.search(r"\b1778\b", content)
        or re.search(r"\b1779\b", content)
        or re.search(r"\b1780\b", content)
    )
    if not has_diff:
        errors.append(
            "FAILED: commit_timing_analysis.md does not state time difference "
            "(expected approximately 29-30 hours or 1778 minutes)"
        )

    # Check 4: Wang Ming mentioned as earlier committer
    content_lower = content.lower()
    if "wang ming" not in content_lower and "王明" not in content:
        errors.append(
            "FAILED: commit_timing_analysis.md does not mention Wang Ming"
        )

    earlier = (
        "first" in content_lower
        or "earlier" in content_lower
        or "先" in content
        or "早" in content
        or "before" in content_lower
    )
    if not earlier:
        errors.append(
            "FAILED: commit_timing_analysis.md does not conclude who committed first"
        )

    # Check 5: >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(
            f"FAILED: commit_timing_analysis.md has only {len(headings)} ## headings (need >= 2)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
