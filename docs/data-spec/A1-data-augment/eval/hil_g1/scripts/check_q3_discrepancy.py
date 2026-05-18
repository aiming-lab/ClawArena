#!/usr/bin/env python3
"""
check_q3_discrepancy.py — Validates q3 outputs:
  - analysis/initial_discrepancy_summary.md
  - analysis/discrepancy_data.json

Checks:
  MD:
    - First ## heading contains Executive/Summary/Findings/Key Findings
    - '12' and '4' present
    - '3x' or '3.0' or 'ratio' present
    - Single-source caveat mentioned
    - >= 3 ## headings
  JSON:
    - resume_team_size == 12
    - reference_team_size == 4
    - discrepancy_ratio == 3.0 (within 0.01)
    - corroboration_needed == true
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q3_discrepancy.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    failures = []

    # --- Check MD ---
    md_path = workspace / "analysis" / "initial_discrepancy_summary.md"
    if not md_path.exists():
        failures.append("MD: file not found: analysis/initial_discrepancy_summary.md")
    else:
        content = md_path.read_text(encoding="utf-8")

        headings = re.findall(r'^## (.+)$', content, re.MULTILINE)
        if not headings:
            failures.append("MD: no ## headings found")
        else:
            first = headings[0]
            if not re.search(r'executive|summary|finding|conclusion', first, re.IGNORECASE):
                failures.append(
                    f"MD: first ## heading '{first}' does not contain "
                    "Executive/Summary/Finding/Conclusion — lead with the answer"
                )

        if not re.search(r'\b12\b', content):
            failures.append("MD: '12' (resume team size) not found")
        if not re.search(r'\b4\b', content):
            failures.append("MD: '4' (reference team size) not found")
        if not re.search(r'3x|3\.0|three times|ratio', content, re.IGNORECASE):
            failures.append("MD: discrepancy ratio ('3x', '3.0', or 'ratio') not found")
        if not re.search(
            r'single.source|one source|only source|corrobor|additional|further',
            content, re.IGNORECASE
        ):
            failures.append(
                "MD: single-source caveat not found "
                "(must note that Liu Wei is the only reference obtained)"
            )
        if len(headings) < 3:
            failures.append(f"MD: only {len(headings)} ## headings (expected >= 3)")

    # --- Check JSON ---
    json_path = workspace / "analysis" / "discrepancy_data.json"
    if not json_path.exists():
        failures.append("JSON: file not found: analysis/discrepancy_data.json")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"JSON: invalid JSON — {exc}")
            data = {}

        if data:
            if data.get("resume_team_size") != 12:
                failures.append(
                    f"JSON: resume_team_size == {data.get('resume_team_size')} (expected 12)"
                )
            if data.get("reference_team_size") != 4:
                failures.append(
                    f"JSON: reference_team_size == {data.get('reference_team_size')} (expected 4)"
                )
            ratio = data.get("discrepancy_ratio")
            if ratio is None or abs(float(ratio) - 3.0) > 0.01:
                failures.append(
                    f"JSON: discrepancy_ratio == {ratio} (expected 3.0)"
                )
            if data.get("corroboration_needed") is not True:
                failures.append(
                    f"JSON: corroboration_needed == {data.get('corroboration_needed')} (expected true)"
                )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
