#!/usr/bin/env python3
"""
check_q6_interview.py — Validates q6 outputs:
  - analysis/interview_behavioral_analysis.md
  - analysis/interview_scores.json

Checks:
  MD:
    - 'hesitat' or 'self-correct' present
    - '4.3' present (technical score)
    - '2.8' present (leadership score)
    - P6 recommendation or P7 not-recommended reasoning present
    - >= 3 ## headings
  JSON:
    - huang_lei_technical within ±0.1 of 4.3
    - huang_lei_leadership within ±0.1 of 2.8
    - self_correction_observed == true
    - p7_recommended == false
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q6_interview.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    failures = []

    # --- Check MD ---
    md_path = workspace / "analysis" / "interview_behavioral_analysis.md"
    if not md_path.exists():
        failures.append("MD: file not found: analysis/interview_behavioral_analysis.md")
    else:
        content = md_path.read_text(encoding="utf-8")

        if not re.search(r'hesitat|self.correct|self.correc', content, re.IGNORECASE):
            failures.append("MD: missing hesitation/self-correction observation")
        if not re.search(r'\b4\.3\b', content):
            failures.append("MD: '4.3' (technical score) not found")
        if not re.search(r'\b2\.8\b', content):
            failures.append("MD: '2.8' (leadership score) not found")
        if not re.search(r'\bP6\b|\bP7\b.{0,60}not|not.{0,60}\bP7\b', content, re.IGNORECASE):
            failures.append(
                "MD: P6 recommendation or P7 not-recommended reasoning not found"
            )
        headings = re.findall(r'^## ', content, re.MULTILINE)
        if len(headings) < 3:
            failures.append(f"MD: only {len(headings)} ## headings (expected >= 3)")

    # --- Check JSON ---
    json_path = workspace / "analysis" / "interview_scores.json"
    if not json_path.exists():
        failures.append("JSON: file not found: analysis/interview_scores.json")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"JSON: invalid JSON — {exc}")
            data = {}

        if data:
            tech = data.get("huang_lei_technical")
            if tech is None or abs(float(tech) - 4.3) > 0.1:
                failures.append(
                    f"JSON: huang_lei_technical == {tech} (expected within ±0.1 of 4.3)"
                )
            lead = data.get("huang_lei_leadership")
            if lead is None or abs(float(lead) - 2.8) > 0.1:
                failures.append(
                    f"JSON: huang_lei_leadership == {lead} (expected within ±0.1 of 2.8)"
                )
            if data.get("self_correction_observed") is not True:
                failures.append(
                    f"JSON: self_correction_observed == {data.get('self_correction_observed')} (expected true)"
                )
            if data.get("p7_recommended") is not False:
                failures.append(
                    f"JSON: p7_recommended == {data.get('p7_recommended')} (expected false)"
                )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
