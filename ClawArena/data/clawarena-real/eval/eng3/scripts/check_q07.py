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

def _get_val(obj, key):
    v = obj.get(key)
    if isinstance(v, dict):
        return v.get("value")
    return v

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q07_region_impact.json")
    if err: _finish([err])
    for k in ("western_europe_loss_pct", "eastern_europe_loss_pct"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # western_europe_loss_pct == 10.0 精确（±0.01，读自 region_capacity.csv）
    wv = _get_val(data, "western_europe_loss_pct")
    try:
        if not (9.99 <= float(wv) <= 10.01):
            fails.append("western_europe_loss_pct.value == %r (expected exactly 10.0 from region_capacity.csv; no rounding allowed)" % wv)
    except (TypeError, ValueError):
        fails.append("western_europe_loss_pct not numeric: %r" % wv)
    # eastern_europe_loss_pct == 4.0 精确（±0.01，读自 region_capacity.csv）
    ev = _get_val(data, "eastern_europe_loss_pct")
    try:
        if not (3.99 <= float(ev) <= 4.01):
            fails.append("eastern_europe_loss_pct.value == %r (expected exactly 4.0 from region_capacity.csv; no rounding allowed)" % ev)
    except (TypeError, ValueError):
        fails.append("eastern_europe_loss_pct not numeric: %r" % ev)
    # P2: 值必须是 value/unit 对象结构，unit 必须为 "percent"
    for k in ("western_europe_loss_pct", "eastern_europe_loss_pct"):
        v = data.get(k)
        if not isinstance(v, dict):
            fails.append("%s must be an object {value, unit} (P2 requirement); got %r" % (k, v))
        elif v.get("unit") != "percent":
            fails.append("%s.unit must be \'percent\' (P2 requirement); got %r" % (k, v.get("unit")))
    _finish(fails)
main()
