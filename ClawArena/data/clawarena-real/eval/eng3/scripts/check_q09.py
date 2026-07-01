#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

SLA_FORMULA = "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q09_sla_credit.json")
    if err: _finish([err])
    for k in ("formula", "outage_minutes", "affected_customer_ratio", "scheduled_minutes", "credit_ratio"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # V9: formula 逐字包含
    formula = str(data.get("formula", ""))
    if SLA_FORMULA not in formula:
        fails.append("formula field does not contain verbatim text: %r" % SLA_FORMULA)
    # outage_minutes == 100
    om = data.get("outage_minutes")
    try:
        if not (98 <= int(om) <= 102):
            fails.append("outage_minutes == %r (expected 100)" % om)
    except (TypeError, ValueError):
        fails.append("outage_minutes not int: %r" % om)
    # scheduled_minutes 必须精确为 43200（business_sla.md 明文写明 30-day month = 43200 minutes）
    sm = data.get("scheduled_minutes")
    try:
        sm = int(sm)
        if sm != 43200:
            fails.append("scheduled_minutes == %d (must be exactly 43200 for 30-day billing month as per business_sla.md)" % sm)
    except (TypeError, ValueError):
        fails.append("scheduled_minutes not int: %r" % sm)
    # affected_customer_ratio 必须匹配 sla/affected_customers.csv 的实际计算值（63/3000=0.021）±0.0005
    ar = data.get("affected_customer_ratio")
    try:
        ar_f = float(ar)
        if not (0.0205 <= ar_f <= 0.0215):
            fails.append("affected_customer_ratio == %.6f (must equal 63/3000=0.021000 from sla/affected_customers.csv ±0.0005)" % ar_f)
    except (TypeError, ValueError):
        fails.append("affected_customer_ratio not numeric: %r" % ar)
    # credit_ratio = (outage_minutes * affected_ratio) / scheduled_minutes ±0.0000010
    cr = data.get("credit_ratio")
    try:
        om_f = float(data.get("outage_minutes")); ar_f2 = float(ar); sm_f = float(sm); cr_f = float(cr)
        expected = (om_f * ar_f2) / sm_f
        if abs(cr_f - expected) > 0.000001:
            fails.append("credit_ratio == %.8f does not match (outage*ratio/scheduled) == %.8f (delta > 0.000001)" % (cr_f, expected))
    except (TypeError, ValueError, ZeroDivisionError):
        fails.append("could not compute arithmetic check for credit_ratio")
    _finish(fails)
main()
