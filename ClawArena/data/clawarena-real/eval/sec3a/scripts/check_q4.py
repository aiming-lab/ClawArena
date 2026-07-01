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
    data, err = _load_json(ws / "output" / "bot_summary_errors.json")
    if err: _finish([err])
    errors = data.get("errors")
    if not isinstance(errors, list):
        _finish(["'errors' must be a JSON array"])
    if len(errors) < 3:
        fails.append("errors array has %d items (expected >= 3)" % len(errors))
    if fails: _finish(fails)
    # 真值层：至少1项须标记 $440M → $460M 失真
    found_loss = False
    found_offset = False
    found_count = False
    for e in errors:
        if not isinstance(e, dict):
            continue
        claimed = str(e.get("claimed_value", "")).lower()
        correct = str(e.get("correct_value", "")).lower()
        field = str(e.get("field", "")).lower()
        # V5: loss figure distortion ($440M claimed, $460M correct)
        if "440" in claimed and "460" in correct:
            found_loss = True
        # offset error (30 min claimed, 60 min correct)
        if ("30" in claimed and "60" in correct) or ("30" in claimed and "1 hour" in correct):
            found_offset = True
        # order count distortion (63 claimed, 87 correct)
        if "63" in claimed and "87" in correct:
            found_count = True
    if not found_loss:
        fails.append("errors must include an item flagging KCG loss $440M (claimed) vs $460M (correct)")
    if not found_offset:
        fails.append("errors must include an item flagging UTC offset error 30min (claimed) vs 60min/1h (correct)")
    if not found_count:
        fails.append("errors must include an item flagging affected order count 63 (claimed) vs 87 (correct)")
    _finish(fails)
main()
