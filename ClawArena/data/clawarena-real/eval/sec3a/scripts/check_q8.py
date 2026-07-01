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
    data, err = _load_json(ws / "output" / "t1_settlement_impact.json")
    if err: _finish([err])
    # 字段层
    for req in ("rule_effective_date", "incorrect_cutoff_utc", "correct_cutoff_utc", "offset_minutes"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    if data.get("rule_effective_date") != "2024-05-28":
        fails.append("rule_effective_date == %r (expected '2024-05-28')" % data.get("rule_effective_date"))
    inc = str(data.get("incorrect_cutoff_utc", ""))
    cor = str(data.get("correct_cutoff_utc", ""))
    if "20:00" not in inc:
        fails.append("incorrect_cutoff_utc must contain '20:00' (UTC-4 error produces 20:00 UTC, got %r)" % inc)
    if "21:00" not in cor:
        fails.append("correct_cutoff_utc must contain '21:00' (correct EST: 21:00 UTC, got %r)" % cor)
    try:
        off = int(data.get("offset_minutes"))
    except (TypeError, ValueError):
        _finish(["offset_minutes not an int"])
    if off != 60:
        fails.append("offset_minutes == %d (expected 60, the 1-hour DST error)" % off)
    _finish(fails)
main()
