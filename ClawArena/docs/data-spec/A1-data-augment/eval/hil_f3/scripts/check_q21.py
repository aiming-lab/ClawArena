#!/usr/bin/env python3
"""
check_q21.py -- Verify analysis/ci_remediation_spec.json and analysis/remediation_timeline.md (M3 + M4).

Usage:
    python check_q21.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/ci_remediation_spec.json ---
    json_path = workspace / "analysis" / "ci_remediation_spec.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if data.get("rule_to_delete") != "rule_007":
                errors.append(f"FAILED: ci_remediation_spec.json rule_to_delete expected 'rule_007', got {data.get('rule_to_delete')!r}")

            test_to_add = data.get("test_to_add", [])
            if not isinstance(test_to_add, list) or len(test_to_add) < 2:
                errors.append(f"FAILED: ci_remediation_spec.json test_to_add must have >= 2 items, got {test_to_add!r}")

            min_cov = data.get("min_coverage_target_pct")
            if not isinstance(min_cov, (int, float)) or min_cov < 80:
                errors.append(f"FAILED: ci_remediation_spec.json min_coverage_target_pct must be >= 80, got {min_cov!r}")

    # --- File 2: analysis/remediation_timeline.md ---
    md_path = workspace / "analysis" / "remediation_timeline.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            if "rule_007" not in content:
                errors.append("FAILED: remediation_timeline.md does not mention 'rule_007'")

            if not re.search(r'85%|85\s*percent|coverage.{0,20}target|target.{0,20}coverage', content, re.IGNORECASE):
                errors.append("FAILED: remediation_timeline.md does not mention '85%' or coverage target")

            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(f"FAILED: remediation_timeline.md has only {len(headings)} ## headings (need >= 3)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
