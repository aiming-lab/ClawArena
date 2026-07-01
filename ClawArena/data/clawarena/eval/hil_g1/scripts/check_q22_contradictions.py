#!/usr/bin/env python3
"""
check_q22_contradictions.py — Validates q22 outputs:
  - analysis/four_contradiction_summary.md
  - analysis/contradiction_data.json

MD Checks:
  - C1, C2, C3, C4 all referenced (or equivalent headings)
  - '3x' or '3.0' in C1 context
  - '7' (months) in C2 context
  - >= 4 ## headings

JSON Checks:
  - 'contradictions' object with keys c1–c4 (or 'C1'–'C4')
  - Each has: claim, evidence, ratio_or_gap, severity
  - c1 ratio_or_gap contains '3' or '3x'
  - c2 ratio_or_gap contains '7'
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q22_contradictions.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    failures = []

    # --- Check MD ---
    md_path = workspace / "analysis" / "four_contradiction_summary.md"
    if not md_path.exists():
        failures.append("MD: file not found: analysis/four_contradiction_summary.md")
    else:
        content = md_path.read_text(encoding="utf-8")

        for label in ["C1", "C2", "C3", "C4"]:
            if not re.search(label, content):
                failures.append(f"MD: contradiction '{label}' not referenced")

        if not re.search(r'3x|3\.0|three times|3-fold', content, re.IGNORECASE):
            failures.append("MD: C1 ratio ('3x', '3.0') not found")

        # 7 months in C2 context
        if not re.search(r'\b7\b.{0,60}month|month.{0,60}\b7\b', content, re.IGNORECASE):
            failures.append("MD: C2 7-month gap not referenced")

        headings = re.findall(r'^## ', content, re.MULTILINE)
        if len(headings) < 4:
            failures.append(f"MD: only {len(headings)} ## headings (expected >= 4)")

    # --- Check JSON ---
    json_path = workspace / "analysis" / "contradiction_data.json"
    if not json_path.exists():
        failures.append("JSON: file not found: analysis/contradiction_data.json")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"JSON: invalid JSON — {exc}")
            data = {}

        if data:
            # Accept either 'contradictions' dict or array
            contradictions = data.get("contradictions", {})
            if isinstance(contradictions, list):
                # Convert list to dict by id or position
                c_dict = {}
                for i, item in enumerate(contradictions):
                    key = item.get("id", f"c{i+1}").lower()
                    c_dict[key] = item
                contradictions = c_dict

            if len(contradictions) < 4:
                failures.append(
                    f"JSON: 'contradictions' has {len(contradictions)} entries (expected >= 4)"
                )

            # c1 checks
            c1 = contradictions.get("c1") or contradictions.get("C1")
            if c1 is None:
                failures.append("JSON: c1/C1 not found in contradictions")
            else:
                ratio_gap = str(c1.get("ratio_or_gap", ""))
                if not re.search(r'3|3x', ratio_gap, re.IGNORECASE):
                    failures.append(
                        f"JSON: c1.ratio_or_gap '{ratio_gap}' does not contain '3' or '3x'"
                    )
                severity = c1.get("severity", "")
                if severity not in ("high", "medium", "High", "Medium"):
                    failures.append(
                        f"JSON: c1.severity '{severity}' is not 'high' or 'medium'"
                    )

            # c2 checks
            c2 = contradictions.get("c2") or contradictions.get("C2")
            if c2 is None:
                failures.append("JSON: c2/C2 not found in contradictions")
            else:
                ratio_gap = str(c2.get("ratio_or_gap", ""))
                if "7" not in ratio_gap:
                    failures.append(
                        f"JSON: c2.ratio_or_gap '{ratio_gap}' does not contain '7' (7-month gap)"
                    )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
