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
    data, err = _load_json(ws / "output" / "affected_orders_count.json")
    if err: _finish([err])
    # 字段层
    for req in ("total_affected", "time_window_utc_start", "time_window_utc_end"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    start = str(data.get("time_window_utc_start", ""))
    end   = str(data.get("time_window_utc_end", ""))
    if "2024-11-03T14:00:00" not in start:
        fails.append("time_window_utc_start must be 2024-11-03T14:00:00Z (got %r)" % start)
    if "2024-11-03T15:00:00" not in end:
        fails.append("time_window_utc_end must be 2024-11-03T15:00:00Z (got %r)" % end)
    ta = data.get("total_affected")
    try:
        ta = int(ta)
    except (TypeError, ValueError):
        _finish(["total_affected not an int: %r" % ta])
    # 精确值：aros_v4_2_audit_log.jsonl 中 timestamp_utc_reported 在 [14:00,15:00) UTC 的条目恰好 39 条
    # 注意：position_delta_report.csv 有 87 行（全天所有受影响订单），
    # bot_summary 说 63（bot 抽样），但 AROS log window count 是 39
    if ta != 39:
        fails.append(
            "total_affected == %d (expected exactly 39: count entries with "
            "timestamp_utc_reported in [14:00:00, 15:00:00) UTC on 2024-11-03 "
            "from aros_v4_2_audit_log.jsonl; "
            "position_delta_report.csv has 87 rows (all-day total, not window count); "
            "bot_summary says 63 (bot approximation))" % ta
        )
    _finish(fails)
main()
