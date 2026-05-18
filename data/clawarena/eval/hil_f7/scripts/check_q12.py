#!/usr/bin/env python3
"""
check_q12.py -- Verify analysis/evidence_schema.json.

Usage:
    python check_q12.py <workspace_path>
"""
import sys
import json
from pathlib import Path


VALID_FRAUD_TYPES = {"product_substitution", "description_mismatch", "both"}


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "analysis" / "evidence_schema.json"
    if not json_path.exists():
        print("FAILED: analysis/evidence_schema.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse analysis/evidence_schema.json: {e}")
        sys.exit(1)

    # Check all required fields
    required = ["order_id", "product_sku_ordered", "product_sku_received",
                "payment_amount_fen", "rma_id", "fraud_type"]
    missing = [f for f in required if f not in data]
    if missing:
        errors.append(f"FAILED: missing required fields: {missing}")

    if "order_id" in data and data["order_id"] != "JD-618-2026-7891234":
        errors.append(f"FAILED: order_id expected 'JD-618-2026-7891234', got {data['order_id']!r}")

    if "product_sku_ordered" in data and data["product_sku_ordered"] != "GPU-A100-80G":
        errors.append(f"FAILED: product_sku_ordered expected 'GPU-A100-80G', got {data['product_sku_ordered']!r}")

    if "product_sku_received" in data and data["product_sku_received"] != "GPU-A40-48G":
        errors.append(f"FAILED: product_sku_received expected 'GPU-A40-48G', got {data['product_sku_received']!r}")

    if "payment_amount_fen" in data:
        val = data["payment_amount_fen"]
        if not isinstance(val, int):
            errors.append(f"FAILED: payment_amount_fen must be an integer, got {type(val).__name__}")
        elif val != 7299900:
            errors.append(f"FAILED: payment_amount_fen expected 7299900 (=¥72,999.00 × 100), got {val}")

    if "rma_id" in data and data["rma_id"] != "RMA-2026-0620-001":
        errors.append(f"FAILED: rma_id expected 'RMA-2026-0620-001', got {data['rma_id']!r}")

    if "fraud_type" in data and data["fraud_type"] not in VALID_FRAUD_TYPES:
        errors.append(
            f"FAILED: fraud_type must be one of {VALID_FRAUD_TYPES}, got {data['fraud_type']!r}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
