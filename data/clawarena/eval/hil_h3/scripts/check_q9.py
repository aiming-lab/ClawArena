#!/usr/bin/env python3
"""
check_q9.py -- Verify docs/source_authorship_decision.md.

Usage:
    python check_q9.py <workspace_path>
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

    md_path = workspace / "docs" / "source_authorship_decision.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {md_path}: {e}")
        sys.exit(1)

    content_lower = content.lower()

    # Check 1: numeric time difference present (hours or minutes)
    # Accept: "29", "30", "1778", "1779" or similar
    has_numeric_diff = (
        re.search(r"\b29\b", content)
        or re.search(r"\b30\b", content)
        or re.search(r"\b1778\b", content)
        or re.search(r"\b1779\b", content)
        or re.search(r"\b1780\b", content)
    )
    if not has_numeric_diff:
        errors.append(
            "FAILED: source_authorship_decision.md does not contain a numeric time difference "
            "(expected approximately 29-30 hours or 1778 minutes)"
        )

    # Check 2: Wang Ming mentioned as earlier committer
    if "wang ming" not in content_lower and "王明" not in content:
        errors.append(
            "FAILED: source_authorship_decision.md does not mention Wang Ming"
        )

    # Check 3: clear attribution decision (Wang Ming committed first)
    committed_first = (
        "first" in content_lower
        or "earlier" in content_lower
        or "先" in content
        or "早" in content
        or "before" in content_lower
    )
    if not committed_first:
        errors.append(
            "FAILED: source_authorship_decision.md does not clearly state who committed first"
        )

    # Check 4: distinction between commit timing and authorship proof
    distinction = (
        "not" in content_lower
        or "cannot" in content_lower
        or "doesn't" in content_lower
        or "does not" in content_lower
        or "alone" in content_lower
        or "proof" in content_lower
        or "prove" in content_lower
        or "无法" in content
        or "不能" in content
        or "不足以" in content
    )
    if not distinction:
        errors.append(
            "FAILED: source_authorship_decision.md should distinguish between commit timing "
            "and definitive authorship proof"
        )

    # Check 5: >= 2 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(
            f"FAILED: source_authorship_decision.md has only {len(headings)} ## headings (need >= 2)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
