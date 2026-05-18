#!/usr/bin/env python3
"""check_mandatory_reporting.py — validate q27 outputs:
  docs/YYYY-MM-DD_mandatory_reporting_memo.md and analysis/regulatory_citation_index.json

Memo checks:
  - 'RCW 70.41.230' or '70.41.230' present
  - '72' present (deadline)
  - >=3 ## headings

JSON checks:
  - deadline_hours == 72
  - threshold_hours == 48
  - violated_by_count == 7
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_mandatory_reporting.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: docs/YYYY-MM-DD_mandatory_reporting_memo.md ---
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        print("FAILED: docs/ directory does not exist")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    dated_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not dated_files:
        print("FAILED: no YYYY-MM-DD_ prefixed .md file found in docs/")
        sys.exit(1)

    memo_files = [f for f in dated_files if re.search(r'(mandatory|reporting|memo)', f.name, re.IGNORECASE)]
    files_to_check = memo_files if memo_files else dated_files
    memo_content = "\n".join(f.read_text(encoding="utf-8") for f in files_to_check)

    if not re.search(r'70\.41\.230', memo_content):
        errors.append("mandatory_reporting_memo: 'RCW 70.41.230' or '70.41.230' not found")

    if not re.search(r'\b72\b', memo_content):
        errors.append("mandatory_reporting_memo: '72' (hour deadline) not found")

    headings = re.findall(r'^##\s+.+', memo_content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"mandatory_reporting_memo: found {len(headings)} ## headings, need >=3")

    # --- File 2: analysis/regulatory_citation_index.json ---
    json_path = workspace / "analysis" / "regulatory_citation_index.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: regulatory_citation_index.json is not valid JSON: {e}")
        sys.exit(1)

    rcw = data.get("rcw_70_41_230", {})
    deadline = rcw.get("deadline_hours")
    if deadline != 72:
        errors.append(f"rcw_70_41_230.deadline_hours expected 72, got {deadline!r}")

    wac = data.get("wac_246_840_711", {})
    threshold = wac.get("threshold_hours")
    if threshold != 48:
        errors.append(f"wac_246_840_711.threshold_hours expected 48, got {threshold!r}")

    violated_count = wac.get("violated_by_count")
    if violated_count != 7:
        errors.append(f"wac_246_840_711.violated_by_count expected 7, got {violated_count!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
