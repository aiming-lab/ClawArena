#!/usr/bin/env python3
"""
check_q11_contradiction_registry.py — Validates q11 output:
  (a) analysis/coauthor_behavior_analysis.md
  (b) analysis/contradiction_registry.json

MD checks:
  - '王逸生' present
  - co-signed / co-author language present
  - distanced / distancing language present
  - contemporaneous or pre-complaint contrast
  - ≥3 ## headings

JSON checks:
  - c1, c2, c3 all present
  - each has 'claim', 'evidence', 'resolved_by' sub-fields
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q11_contradiction_registry.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: coauthor_behavior_analysis.md ---
    md_path = workspace / "analysis" / "coauthor_behavior_analysis.md"
    if not md_path.exists():
        print("FAILED: analysis/coauthor_behavior_analysis.md not found")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    if "王逸生" not in md_content:
        errors.append("coauthor_behavior_analysis.md: '王逸生' not found")

    if not re.search(r'co-sign|co-author|cosign|coauthor|co sign', md_content, re.IGNORECASE):
        errors.append(
            "coauthor_behavior_analysis.md: co-signature language not found "
            "(expected 'co-signed', 'co-author', etc.)"
        )

    if not re.search(r'distanc|withdrew|disengag|avoided|step back', md_content, re.IGNORECASE):
        errors.append(
            "coauthor_behavior_analysis.md: distancing language not found "
            "(expected 'distanced', 'withdrew', 'disengaged', etc.)"
        )

    if not re.search(
        r'contemporaneous|pre-complaint|before.{0,30}complaint|original.{0,30}sign',
        md_content,
        re.IGNORECASE
    ):
        errors.append(
            "coauthor_behavior_analysis.md: no contemporaneous/pre-complaint contrast found — "
            "document must contrast the original co-signature with the later distancing"
        )

    headings = re.findall(r'^##\s+', md_content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(
            f"coauthor_behavior_analysis.md: only {len(headings)} ## headings (expected ≥3)"
        )

    # --- File 2: contradiction_registry.json ---
    json_path = workspace / "analysis" / "contradiction_registry.json"
    if not json_path.exists():
        print("FAILED: analysis/contradiction_registry.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: contradiction_registry.json is not valid JSON: {e}")
        sys.exit(1)

    required_keys = ("c1", "c2", "c3")
    required_subfields = ("claim", "evidence", "resolved_by")

    for key in required_keys:
        if key not in data:
            errors.append(f"contradiction_registry.json: '{key}' object not found")
            continue
        obj = data[key]
        if not isinstance(obj, dict):
            errors.append(f"contradiction_registry.json: '{key}' is not an object")
            continue
        for subfield in required_subfields:
            if subfield not in obj:
                errors.append(
                    f"contradiction_registry.json: '{key}' missing sub-field '{subfield}'"
                )
            elif not isinstance(obj[subfield], str) or not obj[subfield].strip():
                errors.append(
                    f"contradiction_registry.json: '{key}.{subfield}' must be a non-empty string"
                )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
