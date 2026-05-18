#!/usr/bin/env python3
"""
check_q13_committee_draft.py — Validates docs/YYYY-MM-DD_committee_response_draft.md.

Checks:
  1. A date-prefixed .md file exists in docs/
  2. N=912, N=847, 65 present as word-boundary numbers
  3. Full IRB number BFH-2025-IRB-0342 present
  4. Pipeline V2.0 or 王逸生 present
  5. Negative framing / explicit refutation of selective exclusion complaint (M6)
  6. ≥4 ## headings
  7. [NUMERIC] 912, 847, 65 confirmed via re.search word boundary (not substring)
  8. [NUMERIC] negative assertion about complaint: complaint is NOT supported by evidence
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q13_committee_draft.py <workspace_path>")
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

    # Use the most recently modified date-prefixed file
    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    errors = []

    # --- NUMERIC VALIDATION (word boundary) ---
    if not re.search(r'\b912\b', content):
        errors.append(f"N=912 not found as standalone number in {target.name}")
    if not re.search(r'\b847\b', content):
        errors.append(f"N=847 not found as standalone number in {target.name}")
    if not re.search(r'\b65\b', content):
        errors.append(f"discrepancy count 65 not found as standalone number in {target.name}")

    # Full IRB number
    if "BFH-2025-IRB-0342" not in content:
        errors.append("'BFH-2025-IRB-0342' not found — cite the full IRB approval number")

    # Pipeline V2.0 or 王逸生
    if not re.search(r'V2\.0|王逸生', content):
        errors.append("'V2.0' or '王逸生' not found — cite pipeline version and author")

    # M6: negative assertion — explicit refutation of selective exclusion claim
    refutation_pattern = re.compile(
        r'(complaint.{0,80}(not supported|refuted|contradicted|incorrect|unfounded|disproved)'
        r'|alleges.{0,150}however.{0,150}(pipeline|evidence|log)'
        r'|(pipeline|evidence|log).{0,150}(refutes|contradicts|does not support|shows no)'
        r'|(selective exclusion|selectively excluded).{0,100}(not supported|not evidenced|refuted|contradicted|no evidence)'
        r'|no (evidence|support) (for |of ).{0,50}(selective|exclusion))',
        re.IGNORECASE | re.DOTALL
    )
    if not refutation_pattern.search(content):
        errors.append(
            "M6 check failed: no explicit refutation of complaint's selective exclusion claim found. "
            "The document must contain language such as 'the complaint alleges... however, pipeline "
            "evidence shows...' or 'selective exclusion claim is not supported by pipeline evidence'."
        )

    # Minimum 4 ## headings
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(
            f"only {len(headings)} ## headings found in {target.name} (expected ≥4)"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
