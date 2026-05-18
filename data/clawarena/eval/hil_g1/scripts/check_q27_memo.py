#!/usr/bin/env python3
"""
check_q27_memo.py — Validates q27 outputs:
  - docs/YYYY-MM-DD_hiring_recommendation_memo.md
  - analysis/memo_data.json

MD Checks:
  - Date-prefixed file exists in docs/
  - '3x' or '3.0' present (inflation ratio)
  - '7 months' or '7-month' present (gap duration)
  - '4.3' present (technical score)
  - '2.8' present (leadership score)
  - >= 4 ## headings

JSON Checks:
  - team_size_inflation_ratio within ±0.1 of 3.0
  - gap_months == 7
  - technical_score within ±0.1 of 4.3
  - flags_count >= 3
"""
import sys
import re
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_q27_memo.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    failures = []

    # --- Check MD ---
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        failures.append("MD: docs/ directory not found")
    else:
        date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
        candidates = [
            f for f in docs_dir.glob("*.md")
            if date_prefix.match(f.name)
            and re.search(r'memo|recommendation|hiring', f.name, re.IGNORECASE)
        ]
        if not candidates:
            # Fall back to any date-prefixed file
            candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

        if not candidates:
            failures.append("MD: no date-prefixed memo/recommendation .md file found in docs/")
        else:
            target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            content = target.read_text(encoding="utf-8")

            if not re.search(r'3x|3\.0|three times|3-fold', content, re.IGNORECASE):
                failures.append("MD: '3x' or '3.0' (inflation ratio) not found")
            if not re.search(r'7.month|seven.month|7 month', content, re.IGNORECASE):
                failures.append("MD: '7 months' or '7-month' (gap duration) not found")
            if not re.search(r'\b4\.3\b', content):
                failures.append("MD: '4.3' (technical score) not found")
            if not re.search(r'\b2\.8\b', content):
                failures.append("MD: '2.8' (leadership score) not found")

            headings = re.findall(r'^## ', content, re.MULTILINE)
            if len(headings) < 4:
                failures.append(f"MD: only {len(headings)} ## headings (expected >= 4)")

    # --- Check JSON ---
    json_path = workspace / "analysis" / "memo_data.json"
    if not json_path.exists():
        failures.append("JSON: file not found: analysis/memo_data.json")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"JSON: invalid JSON — {exc}")
            data = {}

        if data:
            ratio = data.get("team_size_inflation_ratio")
            if ratio is None or abs(float(ratio) - 3.0) > 0.1:
                failures.append(
                    f"JSON: team_size_inflation_ratio == {ratio} (expected within ±0.1 of 3.0)"
                )
            gap = data.get("gap_months")
            if gap != 7:
                failures.append(f"JSON: gap_months == {gap} (expected 7)")
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
            flags = data.get("flags_count")
            if flags is None or int(flags) < 3:
                failures.append(f"JSON: flags_count == {flags} (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
