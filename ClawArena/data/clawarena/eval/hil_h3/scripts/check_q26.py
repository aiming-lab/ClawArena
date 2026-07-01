#!/usr/bin/env python3
"""
check_q26.py -- Verify docs/YYYY-MM-DD_final_case_assessment.md.

Usage:
    python check_q26.py <workspace_path>
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

    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find a YYYY-MM-DD_ prefixed .md file in docs/ that looks like a final assessment
    date_prefix = re.compile(r"^\d{4}-\d{2}-\d{2}_")
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]
    if not prefixed_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Prefer a file with "final" or "assessment" in the name
    target = None
    for f in prefixed_files:
        name_lower = f.name.lower()
        if "final" in name_lower or "assessment" in name_lower or "conclusion" in name_lower:
            target = f
            break
    if target is None:
        # Fall back to most recently modified
        target = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check 1: MOSS similarity 95%
    if not re.search(r"\b95\b", content):
        errors.append(
            "FAILED: final case assessment does not contain '95' (MOSS similarity percentage)"
        )

    # Check 2: git time difference approximately 29-30 hours or 1778 minutes
    has_diff = (
        re.search(r"\b29\b", content)
        or re.search(r"\b30\b", content)
        or re.search(r"\b1778\b", content)
        or re.search(r"\b1779\b", content)
        or re.search(r"\b1780\b", content)
    )
    if not has_diff:
        errors.append(
            "FAILED: final case assessment does not state the git time difference "
            "(expected approximately 29-30 hours or 1778 minutes)"
        )

    # Check 3: SO coverage approximately 85%
    if not re.search(r"\b85\b", content):
        errors.append(
            "FAILED: final case assessment does not contain '85' (SO coverage percentage)"
        )

    # Check 4: M6 GitHub exclusion — 56 hours stated
    if not re.search(r"\b56\b", content):
        errors.append(
            "FAILED: final case assessment does not contain '56' "
            "(M6: GitHub push is 56 hours after Wang Ming's first commit)"
        )

    # Check 5: at least two policy sections cited
    sections_cited = sum(
        1 for sec in ["4.2", "4.3", "4.5"] if sec in content
    )
    if sections_cited < 2:
        errors.append(
            f"FAILED: final case assessment cites only {sections_cited} policy section(s) "
            "(need at least 2 of: 4.2, 4.3, 4.5)"
        )

    # Check 6: TA resolution (warning) mentioned
    content_lower = content.lower()
    warning_mentioned = (
        "warning" in content_lower
        or "警告" in content
    )
    if not warning_mentioned:
        errors.append(
            "FAILED: final case assessment does not mention the TA's formal warning resolution"
        )

    # Check 7: >= 5 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        errors.append(
            f"FAILED: final case assessment has only {len(headings)} ## headings (need >= 5)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
