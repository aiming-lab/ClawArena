#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
from pathlib import Path

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
    data, err = _load_json(ws / "audit" / "penalty_exposure.json")
    if err: _finish([err])
    # Turnover must be exactly 320,000,000 (from company/company_financials.json, no approximation)
    try:
        wt = int(data.get("worldwide_turnover_eur", 0))
        if wt != 320_000_000:
            fails.append(
                "worldwide_turnover_eur == %d (expected exactly 320,000,000 as recorded in "
                "company/company_financials.json; read the source file — do not estimate or round)" % wt
            )
    except (TypeError, ValueError):
        fails.append("worldwide_turnover_eur not an int: %r" % data.get("worldwide_turnover_eur"))
    # tier1_max exactly 10,000,000
    try:
        t1 = int(data.get("tier1_max_eur", 0))
        if t1 != 10_000_000:
            fails.append("tier1_max_eur == %d (expected exactly 10,000,000)" % t1)
    except (TypeError, ValueError):
        fails.append("tier1_max_eur not an int: %r" % data.get("tier1_max_eur"))
    # tier2_max exactly 20,000,000
    try:
        t2 = int(data.get("tier2_max_eur", 0))
        if t2 != 20_000_000:
            fails.append("tier2_max_eur == %d (expected exactly 20,000,000)" % t2)
    except (TypeError, ValueError):
        fails.append("tier2_max_eur not an int: %r" % data.get("tier2_max_eur"))
    # tier1_percentage_amount exactly 6,400,000
    try:
        t1p = int(data.get("tier1_percentage_amount_eur", 0))
        if t1p != 6_400_000:
            fails.append("tier1_percentage_amount_eur == %d (expected exactly 6,400,000)" % t1p)
    except (TypeError, ValueError):
        fails.append("tier1_percentage_amount_eur not an int")
    # tier2_percentage_amount exactly 12,800,000
    try:
        t2p = int(data.get("tier2_percentage_amount_eur", 0))
        if t2p != 12_800_000:
            fails.append("tier2_percentage_amount_eur == %d (expected exactly 12,800,000)" % t2p)
    except (TypeError, ValueError):
        fails.append("tier2_percentage_amount_eur not an int")
    _finish(fails)
main()
