#!/usr/bin/env python3
"""
check_q14.py -- Verify analysis/pr_review_analysis.md (M6 negative check).

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
    target = workspace / "analysis" / "pr_review_analysis.md"

    if not target.exists():
        print(f"FAILED: {target} not found")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must contain 187 and 92 (PR stats)
    if "187" not in content:
        errors.append("FAILED: does not contain '187' (lines added in PR #447)")
    if "92" not in content:
        errors.append("FAILED: does not contain '92' (lines deleted in PR #447)")

    # Must contain LGTM (review comment)
    if "LGTM" not in content:
        errors.append("FAILED: does not contain 'LGTM' (Xiao Zhou's review comment)")

    # Must reference line 127 (the missed point) — word-boundary check to avoid matching '1270'
    if not re.search(r'\b127\b', content):
        errors.append("FAILED: does not contain standalone '127' (the missed line number)")

    # M6 negative: must explicitly state DST was NOT identified or NOT flagged
    has_negative = bool(re.search(
        r'(NOT|not|no|never|did\s+not|didn.t).{0,50}(DST|flag|identif|catch|notice)|'
        r'(DST).{0,50}(NOT|not|never|missed|overlooked|ignored)',
        content, re.IGNORECASE
    ))
    if not has_negative:
        errors.append("FAILED: M6 negative -- must explicitly state DST risk was NOT identified/flagged by the review")

    # Must have >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 2)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
