#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec_backtest_template.py — SEC Backtest Certification Script Template
ArtemisQ Capital — Case No. TM-2024-1103-AQ

Instructions:
  1. Fill in the CORRECT timezone offset (CONFIG_TIMEZONE_OFFSET = -5)
  2. Run this script to produce output/backtest_result.json
  3. Verify that simulated_settlement_utc matches expected_settlement_utc
  4. If match = true, the backtest is certified

Usage:
  python regulatory/sec_backtest_template.py
"""

import datetime
import json
import sys
from pathlib import Path

# ============================================================
# CONFIGURATION — Fill in the correct values
# ============================================================

# Timezone offset to test (correct EST value = -5)
# AROS v4.2 bug used: -4 (EDT, incorrect after DST switch)
CONFIG_TIMEZONE_OFFSET = -5  # Fill in: correct EST value

# Trade date for the incident scenario
TRADE_DATE = datetime.date(2024, 11, 3)

# CME E-Mini daily settlement: 15:00 CT
# CT = ET - 1; in EST period, CT = UTC-6; so 15:00 CT = 15:00 + 6 = 21:00 UTC
CME_SETTLE_HOUR_CT = 15
CME_SETTLE_MINUTE_CT = 0

SCRIPT_VERSION = "1.0-template"

# ============================================================
# COMPUTATION
# ============================================================

def compute_cme_settle_utc(utc_offset_et: int) -> datetime.datetime:
    """
    Compute CME E-Mini settlement UTC for the given ET UTC offset.
    CT = ET - 1 (Central is 1 hour behind Eastern).
    CME settlement = 15:00 CT = 15:00 + abs(CT_UTC_offset) in UTC.
    """
    ct_utc_offset = utc_offset_et - 1  # CT is 1h behind ET
    settle_ct = datetime.datetime(
        TRADE_DATE.year, TRADE_DATE.month, TRADE_DATE.day,
        CME_SETTLE_HOUR_CT, CME_SETTLE_MINUTE_CT, 0
    )
    # Convert CT to UTC: UTC = CT - ct_utc_offset
    settle_utc = settle_ct - datetime.timedelta(hours=ct_utc_offset)
    return settle_utc


def compute_t1_cutoff_utc(utc_offset_et: int) -> datetime.datetime:
    """
    Compute T+1 settlement cutoff UTC (21:00 ET per Rule 15c6-1).
    """
    cutoff_et = datetime.datetime(
        TRADE_DATE.year, TRADE_DATE.month, TRADE_DATE.day, 21, 0, 0
    )
    cutoff_utc = cutoff_et - datetime.timedelta(hours=utc_offset_et)
    return cutoff_utc


def main():
    simulated_settle = compute_cme_settle_utc(CONFIG_TIMEZONE_OFFSET)
    # Expected: 15:00 CT in EST = 21:00 UTC (because CT=UTC-6 in EST period)
    expected_settle = datetime.datetime(2024, 11, 3, 21, 0, 0)

    match = (simulated_settle == expected_settle)

    result = {
        "config_timezone_offset": CONFIG_TIMEZONE_OFFSET,
        "trade_date": TRADE_DATE.isoformat(),
        "simulated_settlement_utc": simulated_settle.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expected_settlement_utc": expected_settle.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "match": match,
        "script_version": SCRIPT_VERSION,
    }

    out_path = Path(__file__).parent.parent / "output" / "backtest_result.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"Backtest result: match={match}")
    print(f"  simulated_settlement_utc: {result['simulated_settlement_utc']}")
    print(f"  expected_settlement_utc:  {result['expected_settlement_utc']}")
    print(f"  Written to: {out_path}")

    if not match:
        print("ERROR: Backtest FAILED. Check CONFIG_TIMEZONE_OFFSET.", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
