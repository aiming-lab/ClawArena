#!/usr/bin/env python3
"""
check_q22.py -- Verify docs/github_exclusion_argument.md (M6 negative assertion).

Usage:
    python check_q22.py <workspace_path>
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

    md_path = workspace / "docs" / "github_exclusion_argument.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    content_lower = content.lower()

    # Check 1: "GitHub" present
    if "github" not in content_lower:
        errors.append(
            "FAILED: github_exclusion_argument.md does not mention 'GitHub'"
        )

    # Check 2: 56 hours difference
    if not re.search(r"\b56\b", content):
        errors.append(
            "FAILED: github_exclusion_argument.md does not contain '56' "
            "(approximately 56 hours between Wang Ming's first commit and Chen Wei's GitHub push)"
        )

    # Check 3: M6 explicit exclusion — GitHub timestamps do not prove Chen Wei coded first
    exclusion_phrases = [
        "not" in content_lower,
        "cannot" in content_lower,
        "does not" in content_lower,
        "can't" in content_lower,
        "不能" in content,
        "无法" in content,
        "cannot prove" in content_lower,
        "does not prove" in content_lower,
        "not evidence" in content_lower,
    ]
    if not any(exclusion_phrases):
        errors.append(
            "FAILED: github_exclusion_argument.md lacks explicit exclusion statement "
            "(e.g., 'cannot prove', 'does not prove', 'not evidence') — M6 requirement"
        )

    # Check 4: Wang Ming's earlier timestamp referenced
    wang_ming_ts = "14:22" in content or "D-2" in content
    if not wang_ming_ts:
        errors.append(
            "FAILED: github_exclusion_argument.md does not reference Wang Ming's "
            "first commit timestamp (D-2 14:22)"
        )

    # Check 5: >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(
            f"FAILED: github_exclusion_argument.md has only {len(headings)} ## headings (need >= 2)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
