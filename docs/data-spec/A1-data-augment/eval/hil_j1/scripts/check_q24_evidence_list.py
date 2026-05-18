#!/usr/bin/env python3
"""
check_q24_evidence_list.py — Verify q24: analysis/欺诈证据清单.json (M4 strict schema)
  - File exists and is valid JSON
  - financial_damage.contract_amount == 30000
  - financial_damage.actual_billed == 70000
  - abs(financial_damage.overcharge_ratio - 2.33) < 0.05
  - legal_threshold_met == true
  - evidence_items is a list with >= 3 elements
  - Each evidence_item has id, type, description, verified fields
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target = workspace / "analysis" / "欺诈证据清单.json"

    if not target.exists():
        print("FAILED: analysis/欺诈证据清单.json not found")
        sys.exit(1)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)

    errors = []

    # Check financial_damage
    financial = data.get("financial_damage")
    if not isinstance(financial, dict):
        errors.append("JSON: 'financial_damage' field is missing or not an object")
    else:
        if financial.get("contract_amount") != 30000:
            errors.append(
                f"JSON: financial_damage.contract_amount expected 30000, got {financial.get('contract_amount')}"
            )
        if financial.get("actual_billed") != 70000:
            errors.append(
                f"JSON: financial_damage.actual_billed expected 70000, got {financial.get('actual_billed')}"
            )
        overcharge = financial.get("overcharge_ratio", 0)
        try:
            overcharge_f = float(overcharge)
            if abs(overcharge_f - 2.33) > 0.05:
                errors.append(
                    f"JSON: financial_damage.overcharge_ratio expected ~2.33 (±0.05), got {overcharge_f}"
                )
        except (TypeError, ValueError):
            errors.append(f"JSON: financial_damage.overcharge_ratio is not a number: {overcharge!r}")

    # Check legal_threshold_met
    if data.get("legal_threshold_met") is not True:
        errors.append(
            f"JSON: legal_threshold_met expected true, got {data.get('legal_threshold_met')!r}"
        )

    # Check evidence_items
    items = data.get("evidence_items")
    if not isinstance(items, list):
        errors.append("JSON: 'evidence_items' field is missing or not an array")
    else:
        if len(items) < 3:
            errors.append(f"JSON: evidence_items length expected >= 3, got {len(items)}")
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"JSON: evidence_items[{i}] is not an object")
                continue
            for field in ["id", "type", "description", "verified"]:
                if field not in item:
                    errors.append(f"JSON: evidence_items[{i}] missing field '{field}'")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
