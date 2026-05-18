#!/usr/bin/env python3
"""
check_q29.py -- Verify docs/YYYY-MM-DD_compliance_final_response.md (P1-P5 content check).

Usage:
    python check_q29.py <workspace_path>

Note: This is called alongside check_preferences.py in the eval command:
    python check_q29.py ${workspace} && python check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/
"""
import sys
import re
from pathlib import Path


def find_final_compliance_response(docs_dir: Path):
    """Find date-prefixed final compliance response in docs/."""
    # Try to find compliance_final_response or similar
    candidates = [
        p for p in docs_dir.glob("*.md")
        if re.match(r'^\d{4}-\d{2}-\d{2}_', p.name)
        and re.search(r'compliance|final|response', p.name, re.IGNORECASE)
    ]
    if not candidates:
        # Fall back to newest date-prefixed MD
        candidates = sorted(
            [p for p in docs_dir.glob("*.md") if re.match(r'^\d{4}-\d{2}-\d{2}_', p.name)],
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
    return candidates[0] if candidates else None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    target = find_final_compliance_response(docs_dir)
    if target is None:
        print("FAILED: no date-prefixed compliance response .md found in docs/")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    errors = []

    # Must contain ISO 8601 timestamp (P1 content check)
    if not re.search(r'2026-03-16T11:30:05\+08:00|11:30:05', content):
        errors.append("FAILED: does not cite violation timestamp '2026-03-16T11:30:05+08:00' or '11:30:05'")

    # Must cite scheduler.py:127 (P4 content check)
    if not re.search(r'scheduler\.py[:\s]+(line\s+)?127|line\s+127', content, re.IGNORECASE):
        errors.append("FAILED: does not cite 'scheduler.py:127' or 'line 127' (P4)")

    # Must mention 60-minute offset
    if not re.search(r'\b60\b.{0,20}min|60-min|\+60', content, re.IGNORECASE):
        errors.append("FAILED: does not cite '60 minutes' offset")

    # Must mention 5-second violation
    if not re.search(r'\b5\b.{0,20}sec|5-sec', content, re.IGNORECASE):
        errors.append("FAILED: does not cite '5 seconds' violation")

    # Must mention rule_007 and 7-day silence
    if "rule_007" not in content:
        errors.append("FAILED: does not mention 'rule_007'")
    if not re.search(r'\b7\b.{0,20}day|7-day', content, re.IGNORECASE):
        errors.append("FAILED: does not mention '7 days' or '7-day' silence")

    # Must have TL;DR section
    if not re.search(r'##\s+TL;DR', content, re.IGNORECASE):
        errors.append("FAILED: does not have '## TL;DR' section (P3/P5)")

    # Must have >= 5 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 5)")

    # Must be >= 800 characters
    if len(content) < 800:
        errors.append(f"FAILED: content length {len(content)} < 800 characters")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
