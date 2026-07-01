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
    data, err = _load_json(ws / "output" / "conversion_funnel_v2.json")
    if err: _finish([err])
    def _pct(key, lo, hi, dp=2):
        v = data.get(key)
        try:
            v = float(v)
        except (TypeError, ValueError):
            fails.append("%s 不是数值: %r" % (key, v)); return None
        if not (lo <= v <= hi):
            fails.append("%s == %.{0}f (expected %.1f-%.1f)".format(dp) % (key, v, lo, hi))
        return v
    _pct("overall_conversion_rate", 1.5, 5.0)
    _pct("add_to_cart_rate", 5.0, 10.0)
    _pct("cart_to_checkout_rate", 55.0, 75.0)
    # 每个字段须有 calculation 字段
    for key in ("overall_conversion_rate", "add_to_cart_rate", "cart_to_checkout_rate"):
        calc_key = key + "_calculation" if key + "_calculation" in data else None
        # 也接受嵌套对象形式
        v = data.get(key)
        if isinstance(v, dict) and not v.get("calculation"):
            fails.append("嵌套对象 %s 须含 calculation 字段" % key)
    _finish(fails)
main()
