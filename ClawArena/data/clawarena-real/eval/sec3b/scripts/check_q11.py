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

def main():
    ws = Path(sys.argv[1]); fails = []
    csv_path = ws / "output" / "order_level_diff_report.csv"
    if not csv_path.exists():
        _finish(["file not found: output/order_level_diff_report.csv"])
    try:
        with open(csv_path, encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fieldnames = reader.fieldnames or []
            rows = list(reader)
    except Exception as exc:
        _finish(["cannot read order_level_diff_report.csv: " + str(exc)])
    # Column headers: must have price_diff_vwap_usd (NOT superseded price_diff_usd)
    fn_low = [f.lower() for f in fieldnames]
    if "price_diff_vwap_usd" not in fn_low:
        fails.append("column 'price_diff_vwap_usd' missing (must use revised field name per Update 2 legal memo)")
    if "price_diff_usd" in fn_low and "price_diff_vwap_usd" not in fn_low:
        fails.append("found superseded column 'price_diff_usd' without 'price_diff_vwap_usd' (Update 2 supersedes)")
    # Must have expected_settlement_utc and actual_settlement_utc
    for need in ("expected_settlement_utc", "actual_settlement_utc", "order_id"):
        if need not in fn_low:
            fails.append("column '%s' missing from CSV" % need)
    # ISO 8601 UTC format check for timestamp columns
    ts_col = next((f for f in fieldnames if "expected_settlement" in f.lower()), None)
    if ts_col and rows:
        sample = rows[0].get(ts_col, "")
        if sample and not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", sample):
            fails.append("expected_settlement_utc value %r is not ISO 8601 UTC format" % sample[:40])
    # Row count must match Round 10 affected_order_count_from_detail
    q10, e10 = _load_json(ws / "output" / "sec_response_framework.json")
    if not e10 and q10 is not None:
        oc = q10.get("affected_order_count_from_detail")
        try:
            oc = int(oc)
            if len(rows) != oc:
                fails.append("CSV row count %d != affected_order_count_from_detail %d (V4 closure)" % (len(rows), oc))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
