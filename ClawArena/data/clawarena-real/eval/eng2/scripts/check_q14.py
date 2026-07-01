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
    data, err = _load_json(ws / "output" / "q14_payment_zone_pivot.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["pivot must be a JSON object keyed by payment_type code"])
    # top-level payment_type codes must include at least 1,2,3
    keys = set(str(k) for k in data.keys() if k not in ("schema_version", "grand_total"))
    need = {"1", "2", "3"}
    miss = need - keys
    if miss:
        fails.append("top-level payment_type code keys missing %s (use official codes, not labels)" % sorted(miss))
    # F: exact per-borough counts for each payment_type code
    EXACT_PIVOT = {
        "1": {"Bronx": 453, "Queens": 468, "Brooklyn": 498, "EWR": 13,
              "Staten Island": 442, "Manhattan": 407, "Unknown": 10},
        "2": {"Manhattan": 86, "Brooklyn": 103, "Bronx": 101, "Queens": 112,
              "Staten Island": 80, "EWR": 1, "Unknown": 1},
        "3": {"Brooklyn": 7, "Queens": 14, "Staten Island": 15, "Bronx": 7,
              "Manhattan": 22, "Unknown": 2},
        "4": {"Manhattan": 10, "Queens": 24, "Brooklyn": 22, "Bronx": 18,
              "Staten Island": 18},
    }
    computed_grand = 0
    for code, expected_boros in EXACT_PIVOT.items():
        if code not in data:
            fails.append("payment_type %r missing from pivot" % code)
            continue
        v = data[code]
        if not isinstance(v, dict) or not v:
            fails.append("payment_type %r value is not a non-empty borough mapping" % code)
            continue
        for boro, expected_count in expected_boros.items():
            got = v.get(boro)
            try:
                got_int = int(got)
            except (TypeError, ValueError):
                fails.append("pivot[%r][%r] == %r (not an int; expected %d)" % (code, boro, got, expected_count))
                continue
            if got_int != expected_count:
                fails.append("pivot[%r][%r] == %d (expected exactly %d)" % (code, boro, got_int, expected_count))
            computed_grand += got_int
    # F: grand_total must be present and equal 2934
    gt = data.get("grand_total")
    if gt is None:
        fails.append("grand_total field missing (must equal 2934)")
    else:
        try:
            gt_int = int(gt)
        except (TypeError, ValueError):
            fails.append("grand_total not an int: %r" % gt)
            gt_int = None
        if gt_int is not None and gt_int != 2934:
            fails.append("grand_total == %d (expected exactly 2934)" % gt_int)
    # C: cross-round closure with q10 — q10.total_trip_count (3062) - vendor6_in_sample (154+negyear) != q14 grand
    # The check is simply: verify grand_total reported == computed from the pivot cells
    if gt is not None:
        try:
            if int(gt) != computed_grand and computed_grand > 0:
                fails.append("grand_total %d != sum of pivot cell counts %d" % (int(gt), computed_grand))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
