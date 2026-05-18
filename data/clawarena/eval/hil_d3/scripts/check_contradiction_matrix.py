#!/usr/bin/env python3
"""check_contradiction_matrix.py — validate q21 outputs:
  analysis/four_contradiction_matrix.md and analysis/contradiction_resolution.json

MD checks:
  - C1 through C4 all labeled
  - '42.3' and '58.4' both present
  - '67%' or 9/3 decline referenced
  - Angela preliminary vs full audit contrast
  - >=4 ## headings OR >=4 table rows

JSON checks:
  - All 9 required fields present
  - c1_official contains '42.3'
  - c1_actual contains '58.4'
  - reliable_source present
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_contradiction_matrix.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/four_contradiction_matrix.md ---
    md_path = workspace / "analysis" / "four_contradiction_matrix.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    content = md_path.read_text(encoding="utf-8")

    # C1: CareScheduler vs badge/Walsh hours
    c1 = re.search(r'\bC1\b', content) or (
        "42.3" in content and "58.4" in content
    )
    if not c1:
        errors.append("four_contradiction_matrix.md: C1 (42.3 vs 58.4 h/week discrepancy) not found")

    # C2: sick leave vs burnout/presenteeism
    c2 = re.search(r'\bC2\b', content) or (
        re.search(r'sick\s+leave', content, re.IGNORECASE)
        and re.search(r'burnout|presenteeism', content, re.IGNORECASE)
    )
    if not c2:
        errors.append("four_contradiction_matrix.md: C2 (sick leave vs burnout) not found")

    # C3: ClinAlert decline vs near-misses
    c3 = re.search(r'\bC3\b', content) or (
        re.search(r'\bClinAlert\b', content, re.IGNORECASE)
        and re.search(r'near[\s-]?miss', content, re.IGNORECASE)
    )
    if not c3:
        errors.append("four_contradiction_matrix.md: C3 (ClinAlert decline vs near-misses) not found")

    # C4: Angela preliminary vs full audit
    c4 = re.search(r'\bC4\b', content) or (
        re.search(r'preliminary', content, re.IGNORECASE)
        and re.search(r'full|formal', content, re.IGNORECASE)
    )
    if not c4:
        errors.append("four_contradiction_matrix.md: C4 (preliminary vs full audit) not found")

    # 42.3 and 58.4 must both be present (word-boundary safe for floats)
    if not re.search(r'(?<!\d)42\.3(?!\d)', content):
        errors.append("four_contradiction_matrix.md: '42.3' not found")
    if not re.search(r'(?<!\d)58\.4(?!\d)', content):
        errors.append("four_contradiction_matrix.md: '58.4' not found")

    # 67% decline or 9/3 pattern
    has_decline = re.search(r'(?<!\d)67\s*%', content) or (re.search(r'\b9\b', content) and re.search(r'\b3\b', content))
    if not has_decline:
        errors.append("four_contradiction_matrix.md: '67%' or 9-to-3 ClinAlert decline not referenced")

    # Structural requirement: >=4 headings or >=4 table rows
    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    table_rows = [
        ln for ln in content.splitlines()
        if "|" in ln
        and not re.match(r'^\s*\|[-:| ]+\|\s*$', ln)
    ]
    if len(headings) < 4 and len(table_rows) < 4:
        errors.append(f"four_contradiction_matrix.md: {len(headings)} ## headings and {len(table_rows)} table rows — need >=4 of either")

    # --- File 2: analysis/contradiction_resolution.json ---
    json_path = workspace / "analysis" / "contradiction_resolution.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: contradiction_resolution.json is not valid JSON: {e}")
        sys.exit(1)

    required_fields = ["c1_official", "c1_actual", "c1_resolved_by",
                       "c2_official", "c2_actual", "c3_official", "c3_actual",
                       "c4_official", "c4_actual"]
    for field in required_fields:
        if field not in data:
            errors.append(f"contradiction_resolution.json: missing field '{field}'")

    c1_off = str(data.get("c1_official", ""))
    if not re.search(r'(?<!\d)42\.3(?!\d)', c1_off):
        errors.append(f"contradiction_resolution.json: c1_official does not contain '42.3' — got: {c1_off!r}")

    c1_act = str(data.get("c1_actual", ""))
    if not re.search(r'(?<!\d)58\.4(?!\d)', c1_act):
        errors.append(f"contradiction_resolution.json: c1_actual does not contain '58.4' — got: {c1_act!r}")

    if "reliable_source" not in data:
        errors.append("contradiction_resolution.json: missing field 'reliable_source'")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
