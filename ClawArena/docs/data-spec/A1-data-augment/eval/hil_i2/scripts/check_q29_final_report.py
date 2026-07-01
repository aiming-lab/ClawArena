#!/usr/bin/env python3
"""
check_q29_final_report.py — Validates docs/YYYY-MM-DD_final_research_integrity_report.md.

Content checks (ALL required):
  1. N=912 present as word-boundary number  re.search(r'\b912\b', content)
  2. N=847 present as word-boundary number  re.search(r'\b847\b', content)
  3. 65 present as word-boundary number     re.search(r'\b65\b', content)
  4. '#BFH-2025-IRB-0342' present (exact string)
  5. 'V2.0' present (exact string)
  6. 'V2.1' present (exact string)
  7. Adverse rate consistency stated (rates not significantly different)
  8. All 4 allegations refuted
  9. >= 5 ## headings  len(re.findall(r'^## ', content)) >= 5
  10. ≥800 characters total  len(content) >= 800
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q29_final_report.py <workspace_path>")
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

    # Prefer files with 'final_research_integrity_report' or 'integrity_report' in name
    preferred = [
        f for f in candidates
        if re.search(r'integrity.{0,20}report|research.{0,20}report', f.name, re.IGNORECASE)
    ]
    target_list = preferred or candidates
    target = sorted(target_list, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    errors = []

    # --- NUMERIC VALIDATION (word boundary — all three required) ---
    if not re.search(r'\b912\b', content):
        errors.append(f"N=912 not found as standalone number in {target.name}")
    if not re.search(r'\b847\b', content):
        errors.append(f"N=847 not found as standalone number in {target.name}")
    if not re.search(r'\b65\b', content):
        errors.append(f"discrepancy count 65 not found as standalone number in {target.name}")

    # Full IRB number (exact string, with or without leading #)
    if 'BFH-2025-IRB-0342' not in content:
        errors.append("'BFH-2025-IRB-0342' (IRB number) not found — cite #BFH-2025-IRB-0342 explicitly")

    # Pipeline versions (exact strings)
    if "V2.0" not in content:
        errors.append("'V2.0' not found")
    if "V2.1" not in content:
        errors.append("'V2.1' not found")

    # V2.0 authorship: 王逸生 or Wang
    if not re.search(r'王逸生|Wang\s+Yisheng|Wang', content):
        errors.append("'王逸生' or 'Wang Yisheng' not found — cite V2.0 pipeline author")

    # V2.1 authorship: 林依 or Lin Yi
    if not re.search(r'林依|Lin\s+Yi', content):
        errors.append("'林依' or 'Lin Yi' not found — cite V2.1 pipeline author")

    # Adverse rate consistency
    if not re.search(
        r'adverse.{0,80}(consistent|similar|not significant|no significant|comparable)',
        content,
        re.IGNORECASE
    ):
        errors.append(
            "adverse outcome rate consistency not stated — "
            "document must confirm excluded and published rates are not significantly different"
        )

    # All 4 allegations refuted
    if not re.search(
        r'(4|four).{0,50}(allegation|finding|claim).{0,50}(refut|address|answer)'
        r'|(allegation|claim|finding).{0,50}(refut|address).{0,50}(4|four|all)',
        content,
        re.IGNORECASE
    ):
        # Fallback: explicit refutation language + the digit 4
        if not (
            re.search(r'\b4\b', content) and
            re.search(r'refut|disprove|not supported|unfounded|address', content, re.IGNORECASE)
        ):
            errors.append(
                "not clear that all 4 allegations are refuted — "
                "document must state all four allegations are addressed/refuted"
            )

    # ≥5 ## headings
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 5:
        errors.append(f"only {len(headings)} ## headings found (expected ≥5)")

    # ≥800 characters
    if len(content) < 800:
        errors.append(f"document is only {len(content)} chars (expected ≥800)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print(f"PASSED (checked {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
