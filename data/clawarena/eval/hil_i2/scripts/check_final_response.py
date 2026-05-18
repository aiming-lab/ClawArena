#!/usr/bin/env python3
"""
check_final_response.py — Validates docs/YYYY-MM-DD_final_response_package.md.

Checks:
  1. ≥1 date-prefixed .md file in docs/
  2. Full IRB number BFH-2025-IRB-0342 present
  3. "V2.0" AND "V2.1" both present
  4. N=912, N=847, 65 present as word-boundary numbers
  5. "corrigendum" or "committee" resolution mentioned
  6. ≥5 ## headings
  7. ≥800 characters total
  8. [NUMERIC] pipeline versions V2.0 / V2.1 verified as exact strings
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_final_response.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # Full IRB number required
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found — cite the full approval number")

    # Pipeline versions as exact strings
    if "V2.0" not in content:
        failures.append("FAILED: 'V2.0' not found")
    if "V2.1" not in content:
        failures.append("FAILED: 'V2.1' not found")

    # --- NUMERIC VALIDATION (word boundary) ---
    if not re.search(r'\b912\b', content):
        failures.append(f"FAILED: N=912 not found as standalone number in {target.name}")
    if not re.search(r'\b847\b', content):
        failures.append(f"FAILED: N=847 not found as standalone number in {target.name}")
    if not re.search(r'\b65\b', content):
        failures.append(f"FAILED: discrepancy count 65 not found as standalone number in {target.name}")

    # Resolution outcome
    if not re.search(r'\b(corrigendum|committee)\b', content, re.IGNORECASE):
        failures.append(
            "FAILED: 'corrigendum' or 'committee' resolution not mentioned"
        )

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 5:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥5)"
        )

    # Minimum length
    if len(content) < 800:
        failures.append(
            f"FAILED: document is only {len(content)} chars (expected ≥800)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
