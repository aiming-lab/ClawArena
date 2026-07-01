#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_vamp_ratio.py — Compute VAMP ratio for a given merchant.

VAMP Ratio = (TC40_fraud_reports + TC15_disputes) / TC05_settled_CNP_transactions

Source: https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance
        https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026

Usage:
    python scripts/compute_vamp_ratio.py --tc40 <int> --tc15 <int> --tc05 <int>
    python scripts/compute_vamp_ratio.py --merchant-id MERCH-A
"""
import argparse
import json
import sys
from pathlib import Path

VAMP_THRESHOLD_BPS = 150   # 2026-04-01 threshold for US/CA/EU/APAC
FEE_PER_EVENT_USD = 8
SOURCE_URL = "https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance"


def compute_vamp(tc40: int, tc15: int, tc05: int) -> dict:
    """Compute VAMP ratio and compliance status."""
    if tc05 <= 0:
        raise ValueError("TC05 (settled CNP transactions) must be > 0")
    ratio_decimal = (tc40 + tc15) / tc05
    ratio_bps = ratio_decimal * 10000
    is_excessive = ratio_bps > VAMP_THRESHOLD_BPS
    return {
        "tc40_fraud_reports": tc40,
        "tc15_disputes": tc15,
        "tc05_settled_cnp": tc05,
        "vamp_ratio_bps": round(ratio_bps, 4),
        "threshold_bps": VAMP_THRESHOLD_BPS,
        "is_excessive": is_excessive,
        "source_url": SOURCE_URL,
    }


def main():
    parser = argparse.ArgumentParser(description="Compute VAMP ratio")
    parser.add_argument("--tc40", type=int, default=42)
    parser.add_argument("--tc15", type=int, default=18)
    parser.add_argument("--tc05", type=int, default=3800)
    parser.add_argument("--merchant-id", default="MERCH-A")
    args = parser.parse_args()

    result = compute_vamp(args.tc40, args.tc15, args.tc05)
    result["merchant_id"] = args.merchant_id
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
