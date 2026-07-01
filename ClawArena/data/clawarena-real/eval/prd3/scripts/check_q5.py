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
    data, err = _load_json(ws / "output" / "return_rate_analysis.json")
    if err: _finish([err])
    cats = data.get("categories") or []
    if not isinstance(cats, list) or len(cats) < 2:
        fails.append("categories 须为含至少 2 个品类的列表")
    found_apparel = found_electronics = False
    for cat in cats:
        if not isinstance(cat, dict):
            continue
        name = str(cat.get("category") or "").lower()
        rr = cat.get("return_rate_pct")
        try:
            rr = float(rr)
        except (TypeError, ValueError):
            fails.append("品类 %r return_rate_pct 不是数值" % name)
            continue
        if "apparel" in name or "服装" in name:
            found_apparel = True
            if not (20.0 <= rr <= 40.0):
                fails.append("apparel return_rate_pct == %.2f (expected 20-40%%)" % rr)
        if "electron" in name or "电子" in name:
            found_electronics = True
            if not (8.0 <= rr <= 15.0):
                fails.append("electronics return_rate_pct == %.2f (expected 8-15%%, 修订前基准)" % rr)
        # flagged 字段须为 bool
        flagged = cat.get("flagged")
        if flagged is not None and not isinstance(flagged, bool):
            fails.append("品类 %r flagged 须为 bool 类型（不得仅用文字说明）" % name)
    if not found_apparel:
        fails.append("categories 中未找到 apparel 品类")
    if not found_electronics:
        fails.append("categories 中未找到 electronics 品类")
    _finish(fails)
main()
