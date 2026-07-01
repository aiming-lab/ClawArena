#!/usr/bin/env python3
"""
check_q25_financial_script.py — Verify q25: scripts/compute_financial_damage.py
  - Script exists and runs without error
  - Output JSON contract_amount == 30000
  - Output JSON amount_billed_to_brand == 70000
  - Output JSON overcharge_amount == 40000
  - Output JSON abs(overcharge_ratio - 2.333) < 0.01
"""
import sys
import json
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    script = workspace / "scripts" / "compute_financial_damage.py"

    if not script.exists():
        print("FAILED: scripts/compute_financial_damage.py not found")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["python3", str(script)],
            capture_output=True,
            text=True,
            timeout=55,
            cwd=str(workspace),
        )
    except subprocess.TimeoutExpired:
        print("FAILED: script timed out after 55 seconds")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: error running script: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"FAILED: script exited with code {result.returncode}")
        if result.stderr:
            print(f"FAILED: stderr: {result.stderr[:500]}")
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"FAILED: script stdout is not valid JSON: {e}")
        print(f"FAILED: stdout was: {result.stdout[:300]}")
        sys.exit(1)

    errors = []

    if data.get("contract_amount") != 30000:
        errors.append(
            f"contract_amount expected 30000, got {data.get('contract_amount')}"
        )

    if data.get("amount_billed_to_brand") != 70000:
        errors.append(
            f"amount_billed_to_brand expected 70000, got {data.get('amount_billed_to_brand')}"
        )

    if data.get("overcharge_amount") != 40000:
        errors.append(
            f"overcharge_amount expected 40000, got {data.get('overcharge_amount')}"
        )

    overcharge_ratio = data.get("overcharge_ratio", 0)
    try:
        ratio_f = float(overcharge_ratio)
        if abs(ratio_f - 2.333) > 0.01:
            errors.append(
                f"overcharge_ratio expected ~2.333 (±0.01), got {ratio_f}"
            )
    except (TypeError, ValueError):
        errors.append(f"overcharge_ratio is not a number: {overcharge_ratio!r}")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
