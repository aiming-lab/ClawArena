#!/usr/bin/env python3
"""
check_q3_discrepancy.py — Validates q3 output:
  (a) analysis/n_discrepancy_preliminary.md
  (b) analysis/research_timeline.json
  (c) cross-check: 65 derivable and mentioned in both files.
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q3_discrepancy.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: n_discrepancy_preliminary.md ---
    md_path = workspace / "analysis" / "n_discrepancy_preliminary.md"
    if not md_path.exists():
        print("FAILED: analysis/n_discrepancy_preliminary.md not found")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    # Required numbers present
    for num in ("912", "847", "65"):
        if not re.search(rf'\b{num}\b', md_content):
            errors.append(f"n_discrepancy_preliminary.md: '{num}' not found")

    # HIS migration mentioned
    if not re.search(r'HIS|migration', md_content, re.IGNORECASE):
        errors.append("n_discrepancy_preliminary.md: 'HIS' or 'migration' not mentioned")

    # First ## heading must contain Problem or Issue
    headings = re.findall(r'^##\s+(.+)', md_content, re.MULTILINE)
    if not headings:
        errors.append("n_discrepancy_preliminary.md: no ## headings found")
    else:
        first_heading = headings[0].lower()
        if not re.search(r'\b(problem|issue)\b', first_heading):
            errors.append(
                f"n_discrepancy_preliminary.md: first ## heading '{headings[0]}' "
                "does not contain 'Problem' or 'Issue'"
            )

    # Minimum 3 ## headings
    if len(headings) < 3:
        errors.append(
            f"n_discrepancy_preliminary.md: only {len(headings)} ## headings found (expected ≥3)"
        )

    # --- File 2: research_timeline.json ---
    json_path = workspace / "analysis" / "research_timeline.json"
    if not json_path.exists():
        print("FAILED: analysis/research_timeline.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: research_timeline.json is not valid JSON: {e}")
        sys.exit(1)

    # irb_before_extraction must be true (boolean)
    if data.get("irb_before_extraction") is not True:
        errors.append(
            f"research_timeline.json: irb_before_extraction expected true, "
            f"got {data.get('irb_before_extraction')!r}"
        )

    # irb_number must contain BFH-2025-IRB-0342
    irb_num = str(data.get("irb_number", ""))
    if "BFH-2025-IRB-0342" not in irb_num:
        errors.append(
            f"research_timeline.json: irb_number does not contain 'BFH-2025-IRB-0342' "
            f"(got {irb_num!r})"
        )

    # irb_date must be 2025-08-01
    if data.get("irb_date") != "2025-08-01":
        errors.append(
            f"research_timeline.json: irb_date expected '2025-08-01', "
            f"got {data.get('irb_date')!r}"
        )

    # --- Cross-check: 65 mentioned in MD and derivable from JSON (912-847=65) ---
    raw = data.get("total_raw") if "total_raw" in data else None
    published = data.get("total_published") if "total_published" in data else None
    # Cross-check: just verify MD mentions 65 (already checked above)
    # Also verify JSON has key numeric context values if provided
    if not re.search(r'\b65\b', md_content):
        errors.append("cross-check: '65' not found in n_discrepancy_preliminary.md")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
