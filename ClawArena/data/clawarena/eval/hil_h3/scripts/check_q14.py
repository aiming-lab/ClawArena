#!/usr/bin/env python3
"""
check_q14.py -- Verify docs/so_coverage_analysis.md.

Usage:
    python check_q14.py <workspace_path>
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

    md_path = workspace / "docs" / "so_coverage_analysis.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    # Check 1: SO question number 48291037
    if "48291037" not in content:
        errors.append(
            "FAILED: so_coverage_analysis.md does not contain '48291037' "
            "(Stack Overflow question number)"
        )

    # Check 2: 847 upvotes
    if not re.search(r"\b847\b", content):
        errors.append(
            "FAILED: so_coverage_analysis.md does not contain '847' (upvote count)"
        )

    # Check 3: approximately 85% SO-explainable coverage
    if not re.search(r"\b85\b", content):
        errors.append(
            "FAILED: so_coverage_analysis.md does not contain '85' "
            "(approximately 85% SO-explainable coverage)"
        )

    # Check 4: naming pattern (prev_node, curr_node, or next_temp)
    naming_found = (
        "prev_node" in content
        or "curr_node" in content
        or "next_temp" in content
    )
    if not naming_found:
        errors.append(
            "FAILED: so_coverage_analysis.md does not mention the variable naming pattern "
            "(prev_node, curr_node, or next_temp)"
        )

    # Check 5: reverse_linked_list mentioned
    if "reverse_linked_list" not in content and "reverse" not in content.lower():
        errors.append(
            "FAILED: so_coverage_analysis.md does not mention 'reverse_linked_list' or reversal function"
        )

    # Check 6: >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: so_coverage_analysis.md has only {len(headings)} ## headings (need >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
