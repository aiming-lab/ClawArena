#!/usr/bin/env python3
"""
check_q5.py -- Verify docs/YYYY-MM-DD_initial_case_analysis.md.

Usage:
    python check_q5.py <workspace_path>
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

    # Find a YYYY-MM-DD_ prefixed .md file in docs/
    date_prefix = re.compile(r"^\d{4}-\d{2}-\d{2}_")
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]
    if not prefixed_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    # Use the most recently modified one (or any — take the first alphabetically)
    # Use the one most likely to be the initial case analysis
    target = None
    for f in prefixed_files:
        name_lower = f.name.lower()
        if "initial" in name_lower or "case" in name_lower or "analysis" in name_lower:
            target = f
            break
    if target is None:
        # Fall back to any date-prefixed file
        target = sorted(prefixed_files)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Check 1: MOSS similarity 95%
    if not re.search(r"\b95\b", content):
        errors.append(
            "FAILED: initial case analysis does not contain '95' (MOSS similarity percentage)"
        )

    # Check 2: Wang Ming's first commit timestamp D-2 14:22
    if "14:22" not in content:
        errors.append(
            "FAILED: Wang Ming's first commit time '14:22' not found"
        )

    # Check 3: Chen Wei's first GitLab commit D-1 20:00
    if "20:00" not in content:
        errors.append(
            "FAILED: Chen Wei's first GitLab commit time '20:00' not found"
        )

    # Check 4: approximately 30 hours time difference
    if not re.search(r"\b30\b", content):
        errors.append(
            "FAILED: time difference (approximately 30 hours) '30' not found in document"
        )

    # Check 5: Chen Wei's GitHub push D1 22:30
    if "22:30" not in content:
        errors.append(
            "FAILED: Chen Wei's GitHub push time '22:30' not found"
        )

    # Check 6: at least 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: document has only {len(headings)} ## headings (need >= 3)"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
