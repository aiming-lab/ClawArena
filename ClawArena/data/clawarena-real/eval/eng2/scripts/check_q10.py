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
    data, err = _load_json(ws / "output" / "q10_daily_summary.json")
    if err: _finish([err])
    # F: exact trip_count per month (computed from real data: year=2023, fare>=0)
    EXACT_TRIPS = {
        "2023-01": 256, "2023-02": 252, "2023-03": 256, "2023-04": 256,
        "2023-05": 252, "2023-06": 257, "2023-07": 255, "2023-08": 253,
        "2023-09": 256, "2023-10": 256, "2023-11": 260, "2023-12": 253,
    }
    # F: avg_fare bounds ±1.0 of true values (not just a loose [10,25] range)
    AVG_FARE_BOUNDS = {
        "2023-01": (16.85, 18.85), "2023-02": (16.43, 18.43),
        "2023-03": (17.34, 19.34), "2023-04": (16.53, 18.53),
        "2023-05": (16.54, 18.54), "2023-06": (16.62, 18.62),
        "2023-07": (17.29, 19.29), "2023-08": (17.93, 19.93),
        "2023-09": (16.60, 18.60), "2023-10": (17.55, 19.55),
        "2023-11": (16.63, 18.63), "2023-12": (17.53, 19.53),
    }
    sum_trip = 0
    for m in range(1, 13):
        key = "2023-%02d" % m
        if key not in data:
            fails.append("missing month key %s" % key)
            continue
        entry = data[key]
        if not isinstance(entry, dict):
            fails.append("%s value is not an object" % key); continue
        # trip_count exact
        tc = entry.get("trip_count")
        try:
            tc = int(tc)
        except (TypeError, ValueError):
            fails.append("%s trip_count not an int: %r" % (key, tc)); continue
        if tc != EXACT_TRIPS[key]:
            fails.append("%s trip_count == %d (expected exactly %d; only count year=2023 rows with fare>=0)" % (key, tc, EXACT_TRIPS[key]))
        sum_trip += tc
        # avg_fare bounds
        af = entry.get("avg_fare")
        try:
            af = float(af)
        except (TypeError, ValueError):
            fails.append("%s avg_fare not numeric: %r" % (key, af)); continue
        lo, hi = AVG_FARE_BOUNDS[key]
        if not (lo <= af <= hi):
            fails.append("%s avg_fare == %.4f (expected within [%.2f, %.2f] — +-1.0 of true value)" % (key, af, lo, hi))
    # C: total_trip_count cross-check
    ttc = data.get("total_trip_count")
    if ttc is None:
        fails.append("total_trip_count field missing (must equal sum of monthly trip_counts = 3062)")
    else:
        try:
            ttc_int = int(ttc)
        except (TypeError, ValueError):
            fails.append("total_trip_count not an int: %r" % ttc)
            ttc_int = None
        if ttc_int is not None:
            if ttc_int != sum_trip:
                fails.append("total_trip_count == %d != sum of monthly trip_counts %d" % (ttc_int, sum_trip))
            elif ttc_int != 3062:
                fails.append("total_trip_count == %d (expected 3062 from the real sample)" % ttc_int)
    _finish(fails)
main()
