#!/usr/bin/env python3
"""
check_q21_four_contradictions.py — Validates q21 output:
  (a) analysis/four_contradiction_analysis.md
  (b) analysis/contradiction_resolution_v2.json

MD checks:
  - All four contradictions C1-C4 present (as headings or in-text)
  - ≥4 ## headings

JSON checks:
  - Exactly 4 keys: c1, c2, c3, c4
  - Each has: allegation (str), evidence (str), resolution (str), favors_defense (bool: true)
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q21_four_contradictions.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: four_contradiction_analysis.md ---
    md_path = workspace / "analysis" / "four_contradiction_analysis.md"
    if not md_path.exists():
        print("FAILED: analysis/four_contradiction_analysis.md not found")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    # C1-C4 all present
    for label in ("C1", "C2", "C3", "C4"):
        # Accept C1/C2/C3/C4 as labels or spelled out as Contradiction 1/2/3/4
        pattern = rf'{label}|[Cc]ontradiction\s*{label[1]}'
        if not re.search(pattern, md_content):
            errors.append(
                f"four_contradiction_analysis.md: '{label}' not found — "
                f"all four contradictions must be labeled"
            )

    # ≥4 ## headings
    headings = re.findall(r'^##\s+', md_content, re.MULTILINE)
    if len(headings) < 4:
        errors.append(
            f"four_contradiction_analysis.md: only {len(headings)} ## headings (expected ≥4)"
        )

    # --- File 2: contradiction_resolution_v2.json ---
    json_path = workspace / "analysis" / "contradiction_resolution_v2.json"
    if not json_path.exists():
        print("FAILED: analysis/contradiction_resolution_v2.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: contradiction_resolution_v2.json is not valid JSON: {e}")
        sys.exit(1)

    required_keys = ("c1", "c2", "c3", "c4")
    required_subfields = ("allegation", "evidence", "resolution", "favors_defense")

    for key in required_keys:
        if key not in data:
            errors.append(f"contradiction_resolution_v2.json: '{key}' not found")
            continue
        obj = data[key]
        if not isinstance(obj, dict):
            errors.append(f"contradiction_resolution_v2.json: '{key}' is not an object")
            continue
        for sf in required_subfields:
            if sf not in obj:
                errors.append(f"contradiction_resolution_v2.json: '{key}.{sf}' missing")
            elif sf == "favors_defense":
                if obj[sf] is not True:
                    errors.append(
                        f"contradiction_resolution_v2.json: '{key}.favors_defense' "
                        f"expected true, got {obj[sf]!r}"
                    )
            elif not isinstance(obj[sf], str) or not obj[sf].strip():
                errors.append(
                    f"contradiction_resolution_v2.json: '{key}.{sf}' must be non-empty string"
                )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
