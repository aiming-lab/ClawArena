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
    data, err = _load_json(ws / "output" / "q7_quality_report_v2.json")
    if err: _finish([err])
    # passenger_count — exact 1,309,356
    e = _field_entry(data, "passenger_count")
    if e is None:
        fails.append("no passenger_count entry under 'fields'")
        nc7 = None
    else:
        try:
            nc7 = int(e.get("null_count"))
        except (TypeError, ValueError):
            fails.append("passenger_count.null_count not an int: %r" % e.get("null_count"))
            nc7 = None
        if nc7 is not None and nc7 != 1309356:
            fails.append("passenger_count.null_count == %d (must be exactly 1,309,356)" % nc7)
    # RatecodeID — exact 1,309,356
    e2 = _field_entry(data, "RatecodeID")
    if e2 is None:
        fails.append("no RatecodeID entry under 'fields'")
        nc7_rc = None
    else:
        try:
            nc7_rc = int(e2.get("null_count"))
        except (TypeError, ValueError):
            fails.append("RatecodeID.null_count not an int: %r" % e2.get("null_count"))
            nc7_rc = None
        if nc7_rc is not None and nc7_rc != 1309356:
            fails.append("RatecodeID.null_count == %d (must be exactly 1,309,356)" % nc7_rc)
    # timestamp_anomaly_count — positive int
    tac = data.get("timestamp_anomaly_count")
    if not isinstance(tac, int) or tac <= 0:
        fails.append("timestamp_anomaly_count == %r (expected positive int)" % tac)
    # total_zone_count — must be present
    tzc = data.get("total_zone_count")
    if tzc is None:
        fails.append("total_zone_count field missing (must echo q1.total_locations)")
    elif int(tzc) != 265:
        fails.append("total_zone_count == %r (expected 265, matching q1.total_locations)" % tzc)
    # C: cross-round closure with q4 — passenger_count must be byte-for-byte identical
    q4, e4 = _load_json(ws / "output" / "q4_quality_report.json")
    if not e4 and q4 is not None:
        e4f = _field_entry(q4, "passenger_count")
        if e4f is not None and nc7 is not None:
            try:
                nc4 = int(e4f.get("null_count"))
                if nc7 != nc4:
                    fails.append("cross-version drift: q7 passenger_count.null_count %d != q4 value %d (must be identical)" % (nc7, nc4))
            except (TypeError, ValueError):
                pass
        # RatecodeID cross-round
        e4f_rc = _field_entry(q4, "RatecodeID")
        if e4f_rc is not None and nc7_rc is not None:
            try:
                nc4_rc = int(e4f_rc.get("null_count"))
                if nc7_rc != nc4_rc:
                    fails.append("cross-version drift: q7 RatecodeID.null_count %d != q4 value %d" % (nc7_rc, nc4_rc))
            except (TypeError, ValueError):
                pass
    # C: cross-round closure with q6 — timestamp_anomaly_count must exactly match q6.anomaly_count
    q6, e6 = _load_json(ws / "output" / "q6_timestamp_anomalies.json")
    if not e6 and q6 is not None:
        ac6 = q6.get("anomaly_count")
        try:
            if int(ac6) != tac:
                fails.append("cross-version drift: q7 timestamp_anomaly_count %r != q6 anomaly_count %r (must be identical)" % (tac, ac6))
        except (TypeError, ValueError):
            pass
    # C: cross-round closure with q1 — total_zone_count must match q1.total_locations exactly
    q1, e1 = _load_json(ws / "output" / "q1_zone_stats.json")
    if not e1 and q1 is not None and tzc is not None:
        tl1 = q1.get("total_locations")
        try:
            if int(tzc) != int(tl1):
                fails.append("cross-version drift: q7 total_zone_count %r != q1 total_locations %r" % (tzc, tl1))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
