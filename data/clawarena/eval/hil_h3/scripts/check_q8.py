#!/usr/bin/env python3
"""
check_q8.py -- Verify docs/ta_notes_analysis.md.

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
    errors = []

    md_path = workspace / "docs" / "ta_notes_analysis.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    # Check 1: 30 hours time difference
    if not re.search(r"\b30\b", content):
        errors.append(
            "FAILED: ta_notes_analysis.md does not contain '30' (30-hour time difference)"
        )

    # Check 2: naming pattern observation (prev_node, curr_node, or next_temp)
    naming_found = (
        "prev_node" in content
        or "curr_node" in content
        or "next_temp" in content
    )
    if not naming_found:
        errors.append(
            "FAILED: ta_notes_analysis.md does not mention the variable naming pattern "
            "(prev_node, curr_node, or next_temp)"
        )

    # Check 3: TA supports Wang Ming's timeline
    content_lower = content.lower()
    wang_supported = (
        "wang ming" in content_lower
        or "王明" in content
    )
    timeline_mentioned = (
        "timeline" in content_lower
        or "时间" in content
        or "earlier" in content_lower
        or "先" in content
        or "before" in content_lower
    )
    if not (wang_supported and timeline_mentioned):
        errors.append(
            "FAILED: ta_notes_analysis.md should mention TA's support for Wang Ming's timeline"
        )

    # Check 4: common source hypothesis mentioned
    common_source = (
        "common source" in content_lower
        or "common reference" in content_lower
        or "same source" in content_lower
        or "公共" in content
        or "共同" in content
        or "来源" in content
        or "stack overflow" in content_lower
        or "SO" in content
    )
    if not common_source:
        errors.append(
            "FAILED: ta_notes_analysis.md should mention the common-source hypothesis"
        )

    # Check 5: >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: ta_notes_analysis.md has only {len(headings)} ## headings (need >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
