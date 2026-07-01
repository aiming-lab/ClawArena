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
    data, err = _load_json(ws / "output" / "q1_zone_stats.json")
    if err: _finish([err])
    # total_locations exact 265
    if data.get("total_locations") != 265:
        fails.append("total_locations == %r (expected 265)" % data.get("total_locations"))
    # boroughs list must include all 7 borough strings
    bs = set(str(b) for b in (data.get("boroughs") or []))
    need = {"EWR", "Queens", "Bronx", "Manhattan", "Staten Island", "Brooklyn", "Unknown"}
    miss = need - bs
    if miss:
        fails.append("boroughs missing %s" % sorted(miss))
    # F: borough_counts must be present and exactly correct
    bc = data.get("borough_counts")
    if not isinstance(bc, dict):
        fails.append("borough_counts must be a JSON object (mapping Borough -> int count)")
    else:
        EXACT_BC = {
            "EWR": 1, "Staten Island": 49, "Brooklyn": 54, "Queens": 56,
            "Manhattan": 52, "Bronx": 52, "Unknown": 1
        }
        for boro, expected in EXACT_BC.items():
            got = bc.get(boro)
            try:
                got_int = int(got)
            except (TypeError, ValueError):
                fails.append("borough_counts[%r] == %r (not an int; expected %d)" % (boro, got, expected))
                continue
            if got_int != expected:
                fails.append("borough_counts[%r] == %d (expected %d)" % (boro, got_int, expected))
    # F: service_zone_counts must be present and exactly correct
    szc = data.get("service_zone_counts")
    if not isinstance(szc, dict):
        fails.append("service_zone_counts must be a JSON object (mapping service_zone -> int count)")
    else:
        EXACT_SZ = {"EWR": 1, "Boro Zone": 209, "Yellow Zone": 52, "Airports": 2, "N/A": 1}
        for sz, expected in EXACT_SZ.items():
            got = szc.get(sz)
            try:
                got_int = int(got)
            except (TypeError, ValueError):
                fails.append("service_zone_counts[%r] == %r (not an int; expected %d)" % (sz, got, expected))
                continue
            if got_int != expected:
                fails.append("service_zone_counts[%r] == %d (expected %d)" % (sz, got_int, expected))
    _finish(fails)
main()
