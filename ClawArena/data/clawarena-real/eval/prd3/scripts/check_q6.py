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
    data, err = _load_json(ws / "output" / "inventory_days_618.json")
    if err: _finish([err])
    # formula_used 须含 360 和 5 quarters
    fu = str(data.get("formula_used") or "").lower()
    if "360" not in fu:
        fails.append("formula_used 未包含 '360': %r" % data.get("formula_used"))
    if "5 quarter" not in fu and "five quarter" not in fu and "5q" not in fu:
        fails.append("formula_used 未包含 '5 quarters': %r" % data.get("formula_used"))
    # inventory_days 须为 LinkMart 618 实算值 32.4（avg_5q/ttm_cogs×360），排除 JD 历史诱饵 31.5
    inv = data.get("inventory_days")
    try:
        inv = float(inv)
    except (TypeError, ValueError):
        _finish(["inventory_days 不是数值: %r" % data.get("inventory_days")])
    if not (32.0 <= inv <= 32.8):
        fails.append("inventory_days == %.1f (expected 32.4 = LinkMart 618 实算值 avg_5q/ttm_cogs×360; 勿用 JD Q4 2024 历史诱饵 31.5)" % inv)
    # multiplier 须为 360
    mult = data.get("multiplier")
    try:
        mult = int(mult)
    except (TypeError, ValueError):
        mult = None
    if mult != 360:
        fails.append("multiplier == %r (expected 360)" % mult)
    _finish(fails)
main()
