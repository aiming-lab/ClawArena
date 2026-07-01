#!/usr/bin/env python3
"""
check_formal_response.py — Validates docs/YYYY-MM-DD_formal_committee_response.md.

Checks:
  1. ≥1 date-prefixed .md file in docs/
  2. "Problem" AND "Assessment" AND "Plan" headings (P/A/P structure)
  3. All 3 allegations addressed
  4. Full IRB number BFH-2025-IRB-0342 present
  5. N=912, N=847, 65 present as word-boundary numbers
  6. ≥5 ## headings
  7. [NUMERIC] 912, 847, 65 verified via re.search word boundary
  8. [NUMERIC] pipeline versions V2.0 and V2.1 present
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_formal_response.py <workspace_path>")
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

    # P/A/P structure in headings
    heading_lines = re.findall(r'^##\s+.+', content, re.MULTILINE | re.IGNORECASE)
    headings_text = "\n".join(heading_lines).lower()

    if not re.search(r'\b(problem|issue)\b', headings_text):
        failures.append("FAILED: no ## heading containing 'Problem' or 'Issue'")
    if not re.search(r'\b(assessment|analysis)\b', headings_text):
        failures.append("FAILED: no ## heading containing 'Assessment' or 'Analysis'")
    if not re.search(r'\b(plan|recommendation)\b', headings_text):
        failures.append("FAILED: no ## heading containing 'Plan' or 'Recommendation'")

    # 3 allegations addressed
    allegation_count = len(re.findall(r'(?:Allegation\s+\d|C[1-3]\b)', content))
    if allegation_count < 3:
        # Also check for "selective exclusion", "duplicate publication", "data manipulation"
        alt_count = sum(1 for pat in (
            r'selective\s+exclusion', r'duplicate\s+publication', r'data\s+manipulat'
        ) if re.search(pat, content, re.IGNORECASE))
        if alt_count < 3:
            failures.append(
                "FAILED: fewer than 3 allegations addressed "
                "(selective exclusion / duplicate publication / data manipulation)"
            )

    # Full IRB number required
    if 'BFH-2025-IRB-0342' not in content:
        failures.append("FAILED: IRB number #BFH-2025-IRB-0342 not found — cite the full approval number")

    # --- NUMERIC VALIDATION (word boundary) ---
    if not re.search(r'\b912\b', content):
        failures.append(f"FAILED: N=912 not found as standalone number in {target.name}")
    if not re.search(r'\b847\b', content):
        failures.append(f"FAILED: N=847 not found as standalone number in {target.name}")
    if not re.search(r'\b65\b', content):
        failures.append(f"FAILED: discrepancy count 65 not found as standalone number in {target.name}")

    # Pipeline versions
    if "V2.0" not in content:
        failures.append("FAILED: pipeline version 'V2.0' not found")
    if "V2.1" not in content:
        failures.append("FAILED: pipeline version 'V2.1' not found")

    # Minimum heading count
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 5:
        failures.append(
            f"FAILED: only {len(headings)} ## headings found (expected ≥5)"
        )

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
