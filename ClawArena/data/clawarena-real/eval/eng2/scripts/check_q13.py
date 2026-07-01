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
    data, err = _load_json(ws / "output" / "q13_archive_compat.json")
    if err: _finish([err])
    if data.get("compatible") is not False:
        fails.append("compatible == %r (expected false)" % data.get("compatible"))
    dep = data.get("deprecated_fields")
    if not isinstance(dep, list):
        fails.append("deprecated_fields must be a list")
        _finish(fails)
    dep_set = set(str(x) for x in dep)
    # all six verbatim deprecated fields must be present
    REQUIRED = {"pickup_datetime", "dropoff_datetime",
                "pickup_longitude", "pickup_latitude",
                "dropoff_longitude", "dropoff_latitude"}
    for need in sorted(REQUIRED):
        if need not in dep_set:
            fails.append("deprecated_fields missing %r (present in archive but absent from schema_v2)" % need)
    # F: order must match archive header order exactly
    # Archive header: VendorID, pickup_datetime, dropoff_datetime, passenger_count, trip_distance,
    #                 pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, fare_amount
    # Deprecated in header order: pickup_datetime, dropoff_datetime, pickup_longitude, pickup_latitude,
    #                              dropoff_longitude, dropoff_latitude
    EXPECTED_ORDER = [
        "pickup_datetime", "dropoff_datetime",
        "pickup_longitude", "pickup_latitude",
        "dropoff_longitude", "dropoff_latitude",
    ]
    # Only check order if all 6 are present
    if dep_set >= REQUIRED:
        filtered = [x for x in dep if x in REQUIRED]
        if filtered != EXPECTED_ORDER:
            fails.append(
                "deprecated_fields order must match archive header order: %s (got: %s)" % (
                    EXPECTED_ORDER, filtered))
    _finish(fails)
main()
