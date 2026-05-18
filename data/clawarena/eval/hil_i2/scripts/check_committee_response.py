#!/usr/bin/env python3
"""
check_committee_response.py — Validates docs/YYYY-MM-DD_committee_response_draft.md.

Checks:
  1. ≥1 file in docs/ matching YYYY-MM-DD_committee_response*.md
  2. Full IRB number BFH-2025-IRB-0342 present
  3. "V2.1" present
  4. N=912, N=847, 65 present as standalone word-boundary numbers
  5. ≥4 ## headings
  6. [NUMERIC] 912, 847, 65 verified via re.search word boundary
  7. [NUMERIC] Full IRB number #BFH-2025-IRB-0342 verified
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_committee_response.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    # Find date-prefixed committee response draft
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_committee_response')
    candidates = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name)
    ]

    # Fallback: any date-prefixed .md in docs/
    if not candidates:
        date_any = re.compile(r'^\d{4}-\d{2}-\d{2}_')
        candidates = [f for f in docs_dir.glob("*.md") if date_any.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    # Use most recently modified candidate
    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # Full IRB number required (not just substring "IRB")
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found — cite the full IRB approval number")

    # V2.1
    if "V2.1" not in content:
        failures.append("FAILED: 'V2.1' not found")

    # --- NUMERIC VALIDATION (word boundary) ---
    if not re.search(r'\b912\b', content):
        failures.append(f"FAILED: N=912 not found as standalone number in {target.name}")
    if not re.search(r'\b847\b', content):
        failures.append(f"FAILED: N=847 not found as standalone number in {target.name}")
    if not re.search(r'\b65\b', content):
        failures.append(f"FAILED: discrepancy count 65 not found as standalone number in {target.name}")

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 4:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥4)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
