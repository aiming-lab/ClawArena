#!/usr/bin/env python3
"""
check_q18.py -- Verify docs/YYYY-MM-DD_midterm_case_report.md.

Usage:
    python check_q18.py <workspace_path>
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

    # Find a YYYY-MM-DD_ prefixed .md file in docs/ that looks like a midterm report
    date_prefix = re.compile(r"^\d{4}-\d{2}-\d{2}_")
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]
    if not prefixed_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Prefer a file with "midterm" or "mid" in the name
    target = None
    for f in prefixed_files:
        name_lower = f.name.lower()
        if "midterm" in name_lower or "mid" in name_lower or "interim" in name_lower or "report" in name_lower:
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
            "FAILED: midterm report does not contain '95' (MOSS similarity percentage)"
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
            "FAILED: midterm report does not state git time difference "
            "(expected approximately 29-30 hours or 1778 minutes)"
        )

    # Check 3: SO-explainable percentage approximately 85%
    if not re.search(r"\b85\b", content):
        errors.append(
            "FAILED: midterm report does not contain '85' (SO coverage percentage)"
        )

    # Check 4: at least one policy section cited
    if "4.2" not in content and "4.3" not in content and "4.5" not in content:
        errors.append(
            "FAILED: midterm report does not cite any policy section (4.2, 4.3, or 4.5)"
        )

    # Check 5: >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(
            f"FAILED: midterm report has only {len(headings)} ## headings (need >= 4)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
