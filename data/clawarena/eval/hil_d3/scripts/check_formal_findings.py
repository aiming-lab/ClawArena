#!/usr/bin/env python3
"""check_formal_findings.py — validate q24: analysis/formal_finding_summary.json

Checks:
  1. Valid JSON array with exactly 4 elements
  2. All finding_ids F1-F4 present
  3. F1.details mentions 'Linda Yee' or 'systematic circumvention'
  4. F3.details mentions 'near-miss' or 'patient safety'
  5. F4.regulatory_citation contains '70.41.230'
  6. severity field for each entry is one of: critical, high, medium, low
"""
import sys
import json
import re
from pathlib import Path

VALID_SEVERITIES = {"critical", "high", "medium", "low"}


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_formal_findings.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "formal_finding_summary.json"

    if not target.exists():
        print(f"FAILED: file not found: {target}")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: invalid JSON: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("FAILED: JSON root must be a JSON array")
        sys.exit(1)

    errors = []

    if len(data) != 4:
        errors.append(f"array length expected 4, got {len(data)}")

    # Index by finding_id
    findings = {}
    for entry in data:
        fid = str(entry.get("finding_id", "")).upper()
        findings[fid] = entry

    for fid in ["F1", "F2", "F3", "F4"]:
        if fid not in findings:
            errors.append(f"{fid} not found in array")

    # F1: details must mention Linda Yee or systematic circumvention
    if "F1" in findings:
        details = str(findings["F1"].get("details", ""))
        has_f1 = (
            "Linda Yee" in details
            or re.search(r'systematic circumvention', details, re.IGNORECASE)
            or re.search(r'Linda', details, re.IGNORECASE)
        )
        if not has_f1:
            errors.append("F1.details does not mention 'Linda Yee' or 'systematic circumvention'")
        sev = str(findings["F1"].get("severity", "")).lower()
        if sev not in VALID_SEVERITIES:
            errors.append(f"F1.severity '{sev}' is not one of: {sorted(VALID_SEVERITIES)}")

    # F3: details must mention near-miss or patient safety
    if "F3" in findings:
        details = str(findings["F3"].get("details", "")).lower()
        has_f3 = "near-miss" in details or "near miss" in details or "patient safety" in details
        if not has_f3:
            errors.append("F3.details does not mention 'near-miss' or 'patient safety'")
        sev = str(findings["F3"].get("severity", "")).lower()
        if sev not in VALID_SEVERITIES:
            errors.append(f"F3.severity '{sev}' is not one of: {sorted(VALID_SEVERITIES)}")

    # F4: regulatory_citation must contain 70.41.230
    if "F4" in findings:
        citation = str(findings["F4"].get("regulatory_citation", ""))
        if "70.41.230" not in citation:
            errors.append(f"F4.regulatory_citation does not contain '70.41.230' — got: {citation!r}")
        sev = str(findings["F4"].get("severity", "")).lower()
        if sev not in VALID_SEVERITIES:
            errors.append(f"F4.severity '{sev}' is not one of: {sorted(VALID_SEVERITIES)}")

    if "F2" in findings:
        details_f2 = str(findings["F2"].get("details", "")).lower()
        has_f2 = (
            re.search(r'\b9\b', details_f2)
            or re.search(r'nine', details_f2)
            or re.search(r'4\s*month', details_f2)
            or re.search(r'four\s*month', details_f2)
        )
        if not has_f2:
            errors.append("F2.details does not mention '9' (nurses affected) or '4 months' (duration)")
        sev = str(findings["F2"].get("severity", "")).lower()
        if sev not in VALID_SEVERITIES:
            errors.append(f"F2.severity '{sev}' is not one of: {sorted(VALID_SEVERITIES)}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
