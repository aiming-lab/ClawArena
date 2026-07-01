#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q11_mc_compliance.json")
    if err: _finish([err])

    for k in ("monthly_chargebacks", "previous_month_transactions", "chargeback_ratio_bps",
               "program_tier", "monthly_fee_eur", "source_url", "merchant_id"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    mid = str(data.get("merchant_id", ""))
    if not any(kw in mid.upper() for kw in ("MERCH-B", "MERCHANT-B", "MERCHANT_B", "B")):
        fails.append(f"merchant_id={mid!r} does not identify Merchant B")

    if int(data.get("monthly_chargebacks", -1)) != 185:
        fails.append(f"monthly_chargebacks={data.get('monthly_chargebacks')} (expected 185)")
    if int(data.get("previous_month_transactions", -1)) != 10000:
        fails.append(f"previous_month_transactions={data.get('previous_month_transactions')} (expected 10000)")

    ratio = float(data.get("chargeback_ratio_bps", 0))
    expected = 185.0
    if abs(ratio - expected) > 0.01:
        fails.append(f"chargeback_ratio_bps={ratio:.4f} (expected exactly {expected:.2f}, tolerance ±0.01)")

    ratio_str = str(data.get("chargeback_ratio_bps", ""))
    if "." in ratio_str:
        dp = len(ratio_str.split(".")[1])
        if dp > 2:
            fails.append(f"chargeback_ratio_bps={ratio_str} has >2 decimal places (P4)")

    tier = str(data.get("program_tier", "")).strip()
    if tier not in ("ECM", "HECM", "none"):
        fails.append(f"program_tier={tier!r} must be 'ECM', 'HECM', or 'none'")
    if tier != "ECM":
        fails.append(f"program_tier={tier!r} — 185 bps (150-299 range) with 185 chargebacks (100-299) = ECM")

    fee = data.get("monthly_fee_eur")
    try:
        fee_int = int(fee)
    except (TypeError, ValueError):
        fee_int = -1
    if fee_int != 5000:
        fails.append(f"monthly_fee_eur={fee} (expected 5000 for ECM month 4-6)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    _finish(fails)
main()
