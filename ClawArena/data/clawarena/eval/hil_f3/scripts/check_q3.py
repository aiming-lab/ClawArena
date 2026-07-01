#!/usr/bin/env python3
"""
check_q3.py -- Verify docs/ci_test_gap_analysis.md and analysis/ci_coverage_data.json.

Usage:
    python check_q3.py <workspace_path>
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

    # --- File 1: docs/ci_test_gap_analysis.md ---
    md_path = workspace / "docs" / "ci_test_gap_analysis.md"
    if not md_path.exists():
        errors.append(f"FAILED: {md_path} not found")
    else:
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"FAILED: cannot read {md_path}: {e}")
            content = ""

        if content:
            # Must contain mock date 2026-01-15
            if "2026-01-15" not in content:
                errors.append("FAILED: docs/ci_test_gap_analysis.md does not contain '2026-01-15'")

            # Must contain 55 (branch coverage reference)
            if not re.search(r'\b55\b', content):
                errors.append("FAILED: docs/ci_test_gap_analysis.md does not contain '55' (branch coverage)")

            # Must mention DST boundary
            if not re.search(r'DST.{0,20}boundary|boundary.{0,20}DST|DST.{0,20}switch|2026-03-08', content, re.IGNORECASE):
                errors.append("FAILED: docs/ci_test_gap_analysis.md does not mention DST boundary or 2026-03-08")

            # Must mention market close boundary
            if not re.search(r'market.{0,20}close|11:30|midday|休市', content, re.IGNORECASE):
                errors.append("FAILED: docs/ci_test_gap_analysis.md does not mention market close boundary or 11:30")

            # Must have >= 3 ## headings
            headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
            if len(headings) < 3:
                errors.append(f"FAILED: docs/ci_test_gap_analysis.md has only {len(headings)} ## headings (need >= 3)")

    # --- File 2: analysis/ci_coverage_data.json ---
    json_path = workspace / "analysis" / "ci_coverage_data.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if data.get("mock_date") != "2026-01-15":
                errors.append(f"FAILED: ci_coverage_data.json mock_date expected '2026-01-15', got {data.get('mock_date')!r}")

            if data.get("timezone_branch_coverage_pct") != 55:
                errors.append(f"FAILED: ci_coverage_data.json timezone_branch_coverage_pct expected 55, got {data.get('timezone_branch_coverage_pct')!r}")

            gap_categories = data.get("gap_categories", [])
            if not isinstance(gap_categories, list) or len(gap_categories) < 3:
                errors.append(f"FAILED: ci_coverage_data.json gap_categories must be a list with >= 3 items, got {gap_categories!r}")

            if data.get("is_dst_period") is not False:
                errors.append(f"FAILED: ci_coverage_data.json is_dst_period expected false, got {data.get('is_dst_period')!r}")

            if data.get("dst_switch_date") != "2026-03-08":
                errors.append(f"FAILED: ci_coverage_data.json dst_switch_date expected '2026-03-08', got {data.get('dst_switch_date')!r}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
