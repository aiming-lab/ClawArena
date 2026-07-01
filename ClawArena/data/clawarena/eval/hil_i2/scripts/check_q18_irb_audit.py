#!/usr/bin/env python3
"""
check_q18_irb_audit.py — Validates q18 output:
  (a) analysis/irb_compliance_audit.json
  (b) analysis/complaint_rebuttal_matrix.md

JSON checks:
  - irb_number contains 'BFH-2025-IRB-0342'
  - irb_before_extraction == true
  - dedup_step_irb_approved == true

MD checks:
  - Markdown table present with ≥4 data rows
  - 'pipeline' or 'HIS' present in table content
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q18_irb_audit.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: irb_compliance_audit.json ---
    json_path = workspace / "analysis" / "irb_compliance_audit.json"
    if not json_path.exists():
        print("FAILED: analysis/irb_compliance_audit.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: irb_compliance_audit.json is not valid JSON: {e}")
        sys.exit(1)

    irb_num = str(data.get("irb_number", ""))
    if "BFH-2025-IRB-0342" not in irb_num:
        errors.append(
            f"irb_compliance_audit.json: irb_number does not contain 'BFH-2025-IRB-0342' "
            f"(got {irb_num!r})"
        )

    if data.get("irb_before_extraction") is not True:
        errors.append(
            f"irb_compliance_audit.json: irb_before_extraction expected true, "
            f"got {data.get('irb_before_extraction')!r}"
        )

    if data.get("dedup_step_irb_approved") is not True:
        errors.append(
            f"irb_compliance_audit.json: dedup_step_irb_approved expected true, "
            f"got {data.get('dedup_step_irb_approved')!r}"
        )

    # --- File 2: complaint_rebuttal_matrix.md ---
    md_path = workspace / "analysis" / "complaint_rebuttal_matrix.md"
    if not md_path.exists():
        print("FAILED: analysis/complaint_rebuttal_matrix.md not found")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    # Count table data rows (lines starting with | that are not separator lines like |---|)
    table_rows = [
        line for line in md_content.splitlines()
        if line.strip().startswith("|")
        and not re.match(r'^\s*\|[\s\-|]+\|\s*$', line)
        and "|" in line[1:]
    ]
    # Subtract header row if present
    data_rows = [r for r in table_rows if not re.search(r'Allegation|allegation|Evidence|Column', r)]
    if len(data_rows) < 4:
        errors.append(
            f"complaint_rebuttal_matrix.md: only {len(data_rows)} data rows in table (expected ≥4). "
            "Ensure the table has one row per allegation."
        )
    elif len(table_rows) < 4:
        errors.append(
            f"complaint_rebuttal_matrix.md: only {len(table_rows)} table rows total (expected ≥4 data rows)"
        )

    # 'pipeline' or 'HIS' in content
    if not re.search(r'pipeline|HIS', md_content, re.IGNORECASE):
        errors.append(
            "complaint_rebuttal_matrix.md: 'pipeline' or 'HIS' not found as evidence source"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
