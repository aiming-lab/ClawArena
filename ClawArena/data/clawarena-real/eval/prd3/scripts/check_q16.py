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
    data, err = _load_json(ws / "output" / "closure_check.json")
    if err: _finish([err])
    # inventory_days_matches_q6 须为 true
    imq6 = data.get("inventory_days_matches_q6")
    if imq6 is not True:
        fails.append("inventory_days_matches_q6 == %r (expected true; Q6 和 Q11 库存天数须一致)" % imq6)
    # gmv_version_matches_q9 须为 true
    gmq9 = data.get("gmv_version_matches_q9")
    if gmq9 is not True:
        fails.append("gmv_version_matches_q9 == %r (expected true; Q9 和 Q11 GMV 总量须一致)" % gmq9)
    # all_consistent 须为 true（或至少 bool 类型）
    ac = data.get("all_consistent")
    if ac is not True and not (isinstance(ac, list) and len(ac) == 0):
        # 如果是 False 或非空列表，视为存在不一致
        if ac is False:
            fails.append("all_consistent == false (须解决不一致问题)")
    # 验证 Q6 和 Q11 实际闭合
    q6, e6 = _load_json(ws / "output" / "inventory_days_618.json")
    q11, e11 = _load_json(ws / "output" / "kpi_dashboard.json")
    if not e6 and not e11 and q6 and q11:
        try:
            q6_inv = float(q6.get("inventory_days"))
            q11_inv = float(q11.get("inventory_days"))
            if abs(q6_inv - q11_inv) > 0.05:
                fails.append("实际 inventory_days 不一致: Q6=%s != Q11=%s" % (q6_inv, q11_inv))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
