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
    p = ws / "output" / "order_level_diff_report.csv"
    if not p.exists():
        _finish(["file not found: output/order_level_diff_report.csv"])
    # 读取 CSV（跳过注释行）
    fieldnames, rows = _csv_rows(p)
    if fieldnames is None:
        _finish(["order_level_diff_report.csv has no header row"])
    # V10 supersede check: must use price_diff_vwap_usd, NOT price_diff_usd
    if "price_diff_vwap_usd" not in fieldnames:
        fails.append("CSV must have column 'price_diff_vwap_usd' (supersedes 'price_diff_usd' per legal memo)")
    if "price_diff_usd" in fieldnames and "price_diff_vwap_usd" not in fieldnames:
        fails.append("CSV uses old field 'price_diff_usd' which was superseded — must use 'price_diff_vwap_usd'")
    # V4 cross-round closure: must have exactly 87 data rows
    if len(rows) != 87:
        fails.append("CSV must have exactly 87 data rows (got %d); consistent with affected_orders_detail.csv" % len(rows))
    # V8 schema: required columns present
    for col in ("order_id", "expected_settlement_utc", "actual_settlement_utc"):
        if col not in (fieldnames or []):
            fails.append("CSV missing required column '%s'" % col)
    if fails: _finish(fails)
    # 真值层: timestamp format check (ISO 8601 UTC)
    sample = rows[:5] if rows else []
    for r in sample:
        for col in ("expected_settlement_utc", "actual_settlement_utc"):
            v = r.get(col, "")
            if v and not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|\+00:00)", v):
                fails.append("column %s value %r is not ISO 8601 UTC format" % (col, v))
    _finish(fails)
main()
