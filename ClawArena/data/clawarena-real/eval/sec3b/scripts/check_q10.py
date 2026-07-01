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
    data, err = _load_json(ws / "output" / "sec_response_framework.json")
    if err: _finish([err])
    # deadline_utc: exactly 2024-11-07T15:00:00Z (48h after 2024-11-05T15:00Z)
    dl = str(data.get("deadline_utc") or "")
    if "2024-11-07T15:00:00" not in dl:
        fails.append("deadline_utc == %r (expected '2024-11-07T15:00:00Z'; "
                     "48 hours after 2024-11-05T15:00:00Z — must be exactly that datetime)" % dl)
    # required_fields: must include exactly the 4 SEC-specified fields from the inquiry letter
    # At Round 10, Update 2 (legal counsel memo) has NOT yet arrived — do NOT use price_diff_vwap_usd
    rq = data.get("required_fields")
    if not isinstance(rq, list):
        _finish(["required_fields must be a list"])
    rq_str = [str(x).strip().lower() for x in rq]
    rq_set = set(rq_str)
    required_exact = {"order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"}
    for need in required_exact:
        if need not in rq_set:
            fails.append("required_fields missing '%s' (verbatim from SEC inquiry letter, Update 1)" % need)
    # price_diff_vwap_usd must NOT appear — that is the Update 2 superseded name, not yet issued at Round 10
    if "price_diff_vwap_usd" in rq_set:
        fails.append("required_fields contains 'price_diff_vwap_usd' which is the Update 2 "
                     "revised field name — Update 2 has NOT yet arrived at Round 10; "
                     "use 'price_diff_usd' from the SEC inquiry letter")
    # affected_order_count_from_detail: must be a positive int matching the CSV row count
    oc = data.get("affected_order_count_from_detail")
    try:
        oc = int(oc)
    except (TypeError, ValueError):
        _finish(["affected_order_count_from_detail not an int: %r" % oc])
    if oc <= 0:
        fails.append("affected_order_count_from_detail == %d (expected positive int)" % oc)
    # Cross-verify: recount from the actual CSV to ensure the agent read it accurately
    detail_csv = ws / "incident" / "affected_orders_detail.csv"
    if detail_csv.exists():
        import csv as _csv
        with open(detail_csv, encoding="utf-8") as fh:
            real_count = sum(1 for _ in _csv.DictReader(fh))
        if oc != real_count:
            fails.append(
                "affected_order_count_from_detail == %d but incident/affected_orders_detail.csv "
                "has exactly %d data rows (count the file accurately)" % (oc, real_count)
            )
    _finish(fails)
main()
