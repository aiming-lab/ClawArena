#!/usr/bin/env python3
"""
check_q27_final_response_pair.py — Validates q27 output:
  (a) docs/YYYY-MM-DD_final_committee_response.md
  (b) analysis/response_evidence_checklist.json

MD checks:
  - Date-prefixed file in docs/ with 'final_committee_response' or similar name
  - '#BFH-2025-IRB-0342' or 'BFH' present
  - ≥5 ## headings

JSON checks:
  - All boolean fields true
  - irb_number contains 'BFH'
"""
import sys
import json
import re
from pathlib import Path


BOOLEAN_FIELDS = (
    "irb_compliance_documented",
    "pipeline_audit_complete",
    "adverse_rate_analysis_complete",
    "coauthor_dispute_addressed",
    "all_allegations_refuted",
)


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q27_final_response_pair.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: docs/YYYY-MM-DD_final_committee_response.md ---
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    # Look for a final_committee_response file or any date-prefixed file in docs/
    candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    # Prefer files with 'final_committee' or 'committee' in name
    preferred = [f for f in candidates if re.search(r'final.{0,20}committee|committee.{0,20}response', f.name, re.IGNORECASE)]
    target = (preferred or candidates)
    target = sorted(target, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")

    # BFH or full IRB number
    if not re.search(r'BFH.{0,30}IRB|IRB.{0,30}BFH|#BFH-2025-IRB-0342', content):
        errors.append(
            f"{target.name}: '#BFH-2025-IRB-0342' or 'BFH' IRB reference not found"
        )

    # ≥5 ## headings
    headings = re.findall(r'^##\s+', content, re.MULTILINE)
    if len(headings) < 5:
        errors.append(
            f"{target.name}: only {len(headings)} ## headings found (expected ≥5)"
        )

    # --- File 2: analysis/response_evidence_checklist.json ---
    json_path = workspace / "analysis" / "response_evidence_checklist.json"
    if not json_path.exists():
        print("FAILED: analysis/response_evidence_checklist.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: response_evidence_checklist.json is not valid JSON: {e}")
        sys.exit(1)

    for field in BOOLEAN_FIELDS:
        if data.get(field) is not True:
            errors.append(
                f"response_evidence_checklist.json: '{field}' expected true, "
                f"got {data.get(field)!r}"
            )

    irb_num = str(data.get("irb_number", ""))
    if "BFH" not in irb_num:
        errors.append(
            f"response_evidence_checklist.json: irb_number does not contain 'BFH' "
            f"(got {irb_num!r})"
        )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
