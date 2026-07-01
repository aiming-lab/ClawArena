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
    data, err = _load_json(ws / "output" / "sec_response_framework.json")
    if err: _finish([err])
    # 字段层
    for req in ("deadline_utc", "required_fields", "affected_order_count_from_detail"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    deadline = str(data.get("deadline_utc", ""))
    if "2024-11-07T09:00:00" not in deadline:
        fails.append("deadline_utc must be 2024-11-07T09:00:00Z (from SEC letter, got %r)" % deadline)
    req_fields = [str(f) for f in (data.get("required_fields") or [])]
    req_set = set(req_fields)
    # Update1 specifies these 4 fields (note: Update2 supersedes price_diff_usd → price_diff_vwap_usd,
    # but q10 is BEFORE update2, so the original field name from the SEC letter must appear here)
    for need in ("order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"):
        if need not in req_set:
            fails.append("required_fields missing %r (the field as specified in the SEC letter)" % need)
    try:
        cnt = int(data.get("affected_order_count_from_detail"))
    except (TypeError, ValueError):
        _finish(["affected_order_count_from_detail not an int"])
    if cnt != 87:
        fails.append("affected_order_count_from_detail == %d (expected 87, from affected_orders_detail.csv)" % cnt)
    _finish(fails)
main()
