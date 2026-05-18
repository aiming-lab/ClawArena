#!/usr/bin/env python3
"""check_cross_validation.py — validate q11 and q22 outputs.

Mode 1 (default, q11): checks both
  analysis/cross_source_validation.md and analysis/charge_nurse_asymmetry.json

Mode 2 (--mode preliminary_critique, q22): checks
  analysis/preliminary_audit_critique.md

Usage:
  python check_cross_validation.py <workspace>
  python check_cross_validation.py <workspace> --mode preliminary_critique
"""
import sys
import json
import re
import argparse
from pathlib import Path


def check_q11(workspace, errors):
    # --- File 1: analysis/cross_source_validation.md ---
    md_path = workspace / "analysis" / "cross_source_validation.md"
    if not md_path.exists():
        errors.append(f"{md_path} not found")
        return

    content = md_path.read_text(encoding="utf-8")

    if not re.search(r'\bindependent\b', content, re.IGNORECASE):
        errors.append("cross_source_validation.md: 'independent' not found")

    has_concordant = (
        re.search(r'\bconcordant\b', content, re.IGNORECASE)
        or re.search(r'cross[\s-]?verif', content, re.IGNORECASE)
        or re.search(r'\bcorroborat', content, re.IGNORECASE)
    )
    if not has_concordant:
        errors.append("cross_source_validation.md: 'concordant', 'cross-verified', or 'corroborated' not found")

    if not re.search(r'\b7\b', content):
        errors.append("cross_source_validation.md: '7' (nurses above 48h) not found as standalone number")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"cross_source_validation.md: found {len(headings)} ## headings, need >=3")

    # --- File 2: analysis/charge_nurse_asymmetry.json ---
    json_path = workspace / "analysis" / "charge_nurse_asymmetry.json"
    if not json_path.exists():
        errors.append(f"{json_path} not found")
        return

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"charge_nurse_asymmetry.json is not valid JSON: {e}")
        return

    count = data.get("staff_nurses_understated_count")
    if count != 9:
        errors.append(f"charge_nurse_asymmetry.json: staff_nurses_understated_count expected 9, got {count!r}")

    if "charge_nurses_accurate" not in data:
        errors.append("charge_nurse_asymmetry.json: missing field 'charge_nurses_accurate'")

    if "probability_by_chance_pct" not in data:
        errors.append("charge_nurse_asymmetry.json: missing field 'probability_by_chance_pct'")

    if data.get("mechanism") != "systematic":
        errors.append(f"charge_nurse_asymmetry.json: mechanism expected 'systematic', got {data.get('mechanism')!r}")


def check_preliminary_critique(workspace, errors):
    target = workspace / "analysis" / "preliminary_audit_critique.md"
    if not target.exists():
        errors.append(f"{target} not found")
        return

    content = target.read_text(encoding="utf-8")

    if not re.search(r'\bCareScheduler\b', content, re.IGNORECASE):
        errors.append("preliminary_audit_critique.md: 'CareScheduler' not found as the unreliable source")

    has_preliminary = re.search(r'\bpreliminary\b', content, re.IGNORECASE)
    if not has_preliminary:
        errors.append("preliminary_audit_critique.md: 'preliminary' (review) not mentioned")

    if not re.search(r'charge nurse', content, re.IGNORECASE):
        errors.append("preliminary_audit_critique.md: 'charge nurse' not identified as data entry source")

    headings = re.findall(r'^##\s+.+', content, re.MULTILINE)
    if len(headings) < 2:
        errors.append(f"preliminary_audit_critique.md: found {len(headings)} ## headings, need >=2")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--mode", default="cross_validation")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    errors = []

    if args.mode == "preliminary_critique":
        check_preliminary_critique(workspace, errors)
    else:
        check_q11(workspace, errors)

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
