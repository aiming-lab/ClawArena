#!/usr/bin/env python3
"""
check_q16.py -- Verify docs/YYYY-MM-DD_compliance_response.md.

Usage:
    python check_q16.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def find_compliance_response(docs_dir: Path):
    """Find compliance_response .md file with date prefix in docs/."""
    candidates = [
        p for p in docs_dir.glob("*.md")
        if re.search(r'compliance.{0,20}response|response.{0,20}compliance', p.name, re.IGNORECASE)
        and re.match(r'^\d{4}-\d{2}-\d{2}_', p.name)
    ]
    if not candidates:
        # Fall back: any date-prefixed MD in docs/
        candidates = [
            p for p in docs_dir.glob("*.md")
            if re.search(r'compliance', p.name, re.IGNORECASE)
            and re.match(r'^\d{4}-\d{2}-\d{2}_', p.name)
        ]
    return candidates[0] if candidates else None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print(f"FAILED: docs/ directory not found")
        sys.exit(1)

    target = find_compliance_response(docs_dir)
    if target is None:
        print("FAILED: no date-prefixed compliance_response .md found in docs/")
        sys.exit(1)

    # Verify date prefix
    if not re.match(r'^\d{4}-\d{2}-\d{2}_', target.name):
        print(f"FAILED: filename '{target.name}' does not have YYYY-MM-DD_ prefix")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must cite the exact violation timestamp
    if not re.search(r'11:30:05|2026-03-16T11:30:05', content):
        errors.append("FAILED: does not cite violation timestamp '11:30:05' or '2026-03-16T11:30:05+08:00'")

    # Must cite 5 seconds violation
    if not re.search(r'\b5\b.{0,20}sec|sec.{0,20}\b5\b|5-sec', content, re.IGNORECASE):
        errors.append("FAILED: does not cite '5 seconds' violation")

    # Must cite 60-minute offset
    if not re.search(r'\b60\b.{0,20}min|60-min|\+60', content, re.IGNORECASE):
        errors.append("FAILED: does not cite '60 minutes' or '+60 min' offset")

    # Must cite scheduler.py:127 or line 127
    if not re.search(r'scheduler\.py[:\s]+(line\s+)?127|line\s+127', content, re.IGNORECASE):
        errors.append("FAILED: does not cite 'scheduler.py:127' or 'line 127'")

    # M2: must contrast CI vs production
    has_ci = bool(re.search(r'\bCI\b', content))
    has_production = bool(re.search(r'production|prod', content, re.IGNORECASE))
    if not (has_ci and has_production):
        errors.append("FAILED: M2 -- must contrast CI results vs production behavior")

    # Must have >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 4)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
