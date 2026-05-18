#!/usr/bin/env python3
"""
check_formal_case.py — Validate docs/YYYY-MM-DD_formal_case_summary.json.

Checks:
  - At least one date-prefixed .json file exists in docs/
  - File is valid JSON
  - Has "evidence_layers" array with >= 4 items
  - Has "contradictions" array with >= 4 items
  - Has "recommended_actions" array with >= 2 items
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_formal_case.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print(f"FAILED: docs/ directory not found: {docs_dir}")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed_jsons = [f for f in docs_dir.glob("*.json") if date_prefix.match(f.name)]

    if not prefixed_jsons:
        print("FAILED: no YYYY-MM-DD_ prefixed .json file found in docs/")
        sys.exit(1)

    # Use the most recently modified date-prefixed JSON file
    case_file = sorted(prefixed_jsons, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    try:
        content = case_file.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAILED: invalid JSON in {case_file.name}: {e}")
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"FAILED: expected a JSON object, got {type(data).__name__} in {case_file.name}")
        sys.exit(1)

    # Check evidence_layers
    evidence_layers = data.get("evidence_layers")
    if evidence_layers is None:
        print(f"FAILED: 'evidence_layers' key not found in {case_file.name}")
        sys.exit(1)
    if not isinstance(evidence_layers, list):
        print(f"FAILED: 'evidence_layers' is not an array in {case_file.name}")
        sys.exit(1)
    if len(evidence_layers) < 4:
        print(f"FAILED: 'evidence_layers' has {len(evidence_layers)} items, expected >= 4")
        sys.exit(1)

    # Check contradictions
    contradictions = data.get("contradictions")
    if contradictions is None:
        print(f"FAILED: 'contradictions' key not found in {case_file.name}")
        sys.exit(1)
    if not isinstance(contradictions, list):
        print(f"FAILED: 'contradictions' is not an array in {case_file.name}")
        sys.exit(1)
    if len(contradictions) < 4:
        print(f"FAILED: 'contradictions' has {len(contradictions)} items, expected >= 4")
        sys.exit(1)

    # Check recommended_actions
    recommended_actions = data.get("recommended_actions")
    if recommended_actions is None:
        print(f"FAILED: 'recommended_actions' key not found in {case_file.name}")
        sys.exit(1)
    if not isinstance(recommended_actions, list):
        print(f"FAILED: 'recommended_actions' is not an array in {case_file.name}")
        sys.exit(1)
    if len(recommended_actions) < 2:
        print(f"FAILED: 'recommended_actions' has {len(recommended_actions)} items, expected >= 2")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
