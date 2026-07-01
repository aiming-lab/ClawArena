#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_penalty_exposure.py — Art. 83 GDPR penalty exposure calculator.

Reads company financial data and computes both Tier 1 and Tier 2 maximum
penalty exposures per Art. 83(4) and Art. 83(5) GDPR.

Art. 83(4) Tier 1: EUR 10,000,000 OR 2% of total worldwide annual turnover
Art. 83(5) Tier 2: EUR 20,000,000 OR 4% of total worldwide annual turnover
(In each tier, the HIGHER amount applies.)

Usage: python scripts/compute_penalty_exposure.py <company_financials_json>
"""
import json
import sys
from pathlib import Path

TIER1_FIXED_EUR = 10_000_000    # Art. 83(4)
TIER1_TURNOVER_PCT = 0.02        # 2%
TIER2_FIXED_EUR = 20_000_000    # Art. 83(5)
TIER2_TURNOVER_PCT = 0.04        # 4%


def compute_exposure(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    turnover = float(data["total_worldwide_annual_turnover_eur"])

    tier1_turnover = turnover * TIER1_TURNOVER_PCT
    tier1_max = max(TIER1_FIXED_EUR, tier1_turnover)

    tier2_turnover = turnover * TIER2_TURNOVER_PCT
    tier2_max = max(TIER2_FIXED_EUR, tier2_turnover)

    return {
        "company": data.get("company"),
        "fiscal_year": data.get("fiscal_year"),
        "total_worldwide_annual_turnover_eur": turnover,
        "tier1_art83_4": {
            "fixed_max_eur": TIER1_FIXED_EUR,
            "turnover_pct": "2%",
            "turnover_based_eur": tier1_turnover,
            "applicable_max_eur": tier1_max,
            "note": "Art. 83(4): applies to Arts. 8, 11, 25-39, 42-43 violations",
        },
        "tier2_art83_5": {
            "fixed_max_eur": TIER2_FIXED_EUR,
            "turnover_pct": "4%",
            "turnover_based_eur": tier2_turnover,
            "applicable_max_eur": tier2_max,
            "note": "Art. 83(5): applies to Arts. 5-7, 9, 12-22, 44-49 violations",
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_penalty_exposure.py <company_financials_json>")
        sys.exit(1)
    r = compute_exposure(sys.argv[1])
    print(json.dumps(r, indent=2))
