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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "backtest_result.json")
    if err: _finish([err])
    # 字段层
    for req in ("config_timezone_offset", "simulated_settlement_utc",
                "expected_settlement_utc", "match", "script_version"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    try:
        tz_off = int(data.get("config_timezone_offset"))
    except (TypeError, ValueError):
        _finish(["config_timezone_offset not an int"])
    if tz_off != -5:
        fails.append("config_timezone_offset == %d (expected -5 for correct EST)" % tz_off)
    if data.get("match") is not True:
        fails.append("match == %r (expected true)" % data.get("match"))
    sim = str(data.get("simulated_settlement_utc", ""))
    if "2024-11-03T21:00:00" not in sim:
        fails.append("simulated_settlement_utc must contain '2024-11-03T21:00:00' (CME 15:00 CT = 21:00 UTC in EST, got %r)" % sim)
    exp = str(data.get("expected_settlement_utc", ""))
    if "2024-11-03T21:00:00" not in exp:
        fails.append("expected_settlement_utc must contain '2024-11-03T21:00:00Z' (got %r)" % exp)
    _finish(fails)
main()
