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
    data, err = _load_json(ws / "output" / "metric_glossary.json")
    if err: _finish([err])
    # 顶层须有 source_url（不接受裸 source 字段，须为权威 URL）
    if "source_url" not in data:
        fails.append("metric_glossary.json 缺少 source_url 字段（须为权威来源 URL，如 wallstreetprep.com；裸 source 字段不满足要求）")
    # gmv_formula 须含 transactions、AOV，且须使用 × 乘号（不接受 * 号）
    gmv_raw = str(data.get("gmv_formula") or "")
    gmv = gmv_raw.lower()
    if "transaction" not in gmv or "aov" not in gmv:
        fails.append("gmv_formula == %r (须包含 'transactions' 和 'AOV')" % gmv_raw)
    if "×" not in gmv_raw and "×" not in gmv_raw:
        fails.append("gmv_formula == %r (须使用 × 乘号（Unicode ×），公式须与 metric_definitions.md 中 verbatim 一致；不接受 * 号)" % gmv_raw)
    # inventory_days_multiplier 须为 360
    mult = data.get("inventory_days_multiplier")
    try:
        mult = int(mult)
    except (TypeError, ValueError):
        mult = None
    if mult != 360:
        fails.append("inventory_days_multiplier == %r (expected 360, JD 官方口径, 非 365)" % mult)
    # take_rate_formula 须含 commission 和 GMV（大小写不敏感）
    trf = str(data.get("take_rate_formula") or "").lower()
    if "commission" not in trf or "gmv" not in trf:
        fails.append("take_rate_formula == %r (须包含 'commission' 和 'GMV')" % data.get("take_rate_formula"))
    _finish(fails)
main()
