#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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

def _field_entry(data, name):
    """从 quality report 取某字段 entry，兼容 fields 为 list 或 dict。"""
    fields = data.get("fields")
    if isinstance(fields, list):
        for e in fields:
            if isinstance(e, dict) and e.get("field_name") == name:
                return e
    elif isinstance(fields, dict):
        e = fields.get(name)
        if isinstance(e, dict):
            return e
        if e is not None:
            return {"field_name": name, "null_count": e}
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q12_vendor_filter_report.json")
    if err: _finish([err])
    try:
        tb = int(data.get("total_before"))
        rr = int(data.get("rows_removed_vendor6"))
        ta = int(data.get("total_after"))
    except (TypeError, ValueError):
        _finish(["total_before / rows_removed_vendor6 / total_after must all be ints"])
    # F: exact values — 3122 (main sample) + 650 (vendor6_sample) = 3772 total
    if tb != 3772:
        fails.append("total_before == %d (expected exactly 3772: 3122 from main sample + 650 from vendor6_sample)" % tb)
    # F: exact vendor6 count = 155 (main sample) + 650 (vendor6_sample) = 805
    if rr != 805:
        fails.append("rows_removed_vendor6 == %d (expected exactly 805: 155 VendorID=6 in main sample + 650 in vendor6_sample)" % rr)
    # arithmetic closure
    if tb - rr != ta:
        fails.append("arithmetic does not close: %d - %d != %d" % (tb, rr, ta))
    if ta != 2967:
        fails.append("total_after == %d (expected exactly 2967)" % ta)
    _finish(fails)
main()
