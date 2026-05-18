#!/usr/bin/env python3
"""
check_q14_registry.py — Validates q14 outputs:
  - analysis/discrepancy_registry.json
  - analysis/discrepancy_registry_summary.md

JSON Checks:
  - 'discrepancies' array with exactly 4 objects
  - D1 ratio == 3.0 (within 0.01)
  - D2 type == 'employment_gap_omission'
  - D4 present with self-correction evidence

MD Checks:
  - References D1, D2, D3, D4 (or all four contradictions)
  - '3.0' or '3x' ratio for C1/D1
  - >= 3 ## headings
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q14_registry.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    failures = []

    # --- Check JSON ---
    json_path = workspace / "analysis" / "discrepancy_registry.json"
    if not json_path.exists():
        failures.append("JSON: file not found: analysis/discrepancy_registry.json")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"JSON: invalid JSON — {exc}")
            data = {}

        if data:
            discrepancies = data.get("discrepancies", [])
            if len(discrepancies) < 4:
                failures.append(
                    f"JSON: 'discrepancies' array has {len(discrepancies)} items (expected >= 4)"
                )
            else:
                # Find D1
                d1 = next((d for d in discrepancies if d.get("id") == "D1"), None)
                if d1 is None:
                    failures.append("JSON: D1 object not found in discrepancies array")
                else:
                    ratio = d1.get("ratio")
                    if ratio is None or abs(float(ratio) - 3.0) > 0.01:
                        failures.append(
                            f"JSON: D1.ratio == {ratio} (expected 3.0)"
                        )

                # Find D2
                d2 = next((d for d in discrepancies if d.get("id") == "D2"), None)
                if d2 is None:
                    failures.append("JSON: D2 object not found in discrepancies array")
                else:
                    d2_type = d2.get("type", "")
                    if d2_type != "employment_gap_omission":
                        failures.append(
                            f"JSON: D2.type == '{d2_type}' (expected 'employment_gap_omission')"
                        )

                # Find D4
                d4 = next((d for d in discrepancies if d.get("id") == "D4"), None)
                if d4 is None:
                    failures.append("JSON: D4 object not found in discrepancies array")
                else:
                    evidence = d4.get("evidence", "")
                    if not re.search(r'self.correct|4.5|direct report', evidence, re.IGNORECASE):
                        failures.append(
                            f"JSON: D4.evidence '{evidence}' does not reference "
                            "self-correction or 4-5 direct reports"
                        )

    # --- Check MD ---
    md_path = workspace / "analysis" / "discrepancy_registry_summary.md"
    if not md_path.exists():
        failures.append("MD: file not found: analysis/discrepancy_registry_summary.md")
    else:
        content = md_path.read_text(encoding="utf-8")

        # All four discrepancies referenced
        for label in ["D1", "D2", "D3", "D4"]:
            if not re.search(label, content):
                failures.append(f"MD: '{label}' not referenced in summary")

        # 3x or 3.0 ratio for D1
        if not re.search(r'3x|3\.0|three times|3-fold', content, re.IGNORECASE):
            failures.append("MD: D1 ratio ('3x', '3.0', 'three times') not found")

        headings = re.findall(r'^## ', content, re.MULTILINE)
        if len(headings) < 3:
            failures.append(f"MD: only {len(headings)} ## headings (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
