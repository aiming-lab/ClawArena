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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "kpi_dashboard.json")
    if err: _finish([err])
    # data_version 须为 v2
    dv = str(data.get("data_version") or "")
    if dv != "v2":
        fails.append("data_version == %r (expected 'v2')" % dv)
    # inventory_days 须与 Q6 完全一致（cross-round drift = fail）
    q6, e6 = _load_json(ws / "output" / "inventory_days_618.json")
    if not e6 and q6 is not None:
        q6_inv = q6.get("inventory_days")
        q11_inv = data.get("inventory_days")
        try:
            q6_inv = float(q6_inv); q11_inv = float(q11_inv)
            if abs(q6_inv - q11_inv) > 0.05:
                fails.append("inventory_days drift: Q11=%s != Q6=%s (须完全一致)" % (q11_inv, q6_inv))
        except (TypeError, ValueError):
            fails.append("inventory_days 须为数值")
    # gmv_total 须与 Q9 v2_total_gmv 一致（±1% 容差）
    q9, e9 = _load_json(ws / "output" / "gmv_revision_v2.json")
    if not e9 and q9 is not None:
        q9_gmv = q9.get("v2_total_gmv")
        q11_gmv = data.get("gmv_total")
        try:
            q9_gmv = float(q9_gmv); q11_gmv = float(q11_gmv)
            if abs(q9_gmv - q11_gmv) / max(q9_gmv, 1) > 0.01:
                fails.append("gmv_total drift: Q11=%s != Q9 v2=%s (须一致，容差 1%%)" % (q11_gmv, q9_gmv))
        except (TypeError, ValueError):
            fails.append("gmv_total 须为数值")
    # return_rate_overall 须在合理区间
    rr = data.get("return_rate_overall")
    try:
        rr = float(rr)
        if not (5.0 <= rr <= 30.0):
            fails.append("return_rate_overall == %.2f (expected 5-30%%)" % rr)
    except (TypeError, ValueError):
        fails.append("return_rate_overall 须为数值")
    _finish(fails)
main()
