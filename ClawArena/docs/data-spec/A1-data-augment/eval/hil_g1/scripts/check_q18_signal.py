#!/usr/bin/env python3
"""
check_q18_signal.py — Validates q18 outputs:
  - analysis/technical_vs_claims_comparison.md
  - analysis/signal_weighting.json

MD Checks:
  - '4.3' and '2.8' present
  - Team size inflation or 3x mentioned
  - >= 3 ## headings

JSON Checks:
  - technical_score within ±0.1 of 4.3
  - leadership_score within ±0.1 of 2.8
  - team_size_inflation_ratio within ±0.1 of 3.0
  - gap_months_hidden == 7
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q18_signal.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    failures = []

    # --- Check MD ---
    md_path = workspace / "analysis" / "technical_vs_claims_comparison.md"
    if not md_path.exists():
        failures.append("MD: file not found: analysis/technical_vs_claims_comparison.md")
    else:
        content = md_path.read_text(encoding="utf-8")

        if not re.search(r'\b4\.3\b', content):
            failures.append("MD: '4.3' (technical score) not found")
        if not re.search(r'\b2\.8\b', content):
            failures.append("MD: '2.8' (leadership score) not found")
        if not re.search(r'3x|3\.0|inflat|three times', content, re.IGNORECASE):
            failures.append(
                "MD: team size inflation ('3x', '3.0', 'inflated') not mentioned"
            )

        headings = re.findall(r'^## ', content, re.MULTILINE)
        if len(headings) < 3:
            failures.append(f"MD: only {len(headings)} ## headings (expected >= 3)")

    # --- Check JSON ---
    json_path = workspace / "analysis" / "signal_weighting.json"
    if not json_path.exists():
        failures.append("JSON: file not found: analysis/signal_weighting.json")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"JSON: invalid JSON — {exc}")
            data = {}

        if data:
            tech = data.get("technical_score")
            if tech is None or abs(float(tech) - 4.3) > 0.1:
                failures.append(
                    f"JSON: technical_score == {tech} (expected within ±0.1 of 4.3)"
                )
            lead = data.get("leadership_score")
            if lead is None or abs(float(lead) - 2.8) > 0.1:
                failures.append(
                    f"JSON: leadership_score == {lead} (expected within ±0.1 of 2.8)"
                )
            ratio = data.get("team_size_inflation_ratio")
            if ratio is None or abs(float(ratio) - 3.0) > 0.1:
                failures.append(
                    f"JSON: team_size_inflation_ratio == {ratio} (expected within ±0.1 of 3.0)"
                )
            gap = data.get("gap_months_hidden")
            if gap != 7:
                failures.append(
                    f"JSON: gap_months_hidden == {gap} (expected 7)"
                )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
