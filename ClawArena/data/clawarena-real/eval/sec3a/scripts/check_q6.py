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
    data, err = _load_json(ws / "output" / "legacy_code_assessment.json")
    if err: _finish([err])
    # 字段层
    for req in ("is_applicable", "reason", "recommendation"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    if data.get("is_applicable") is not False:
        fails.append("is_applicable == %r (expected false)" % data.get("is_applicable"))
    reason = str(data.get("reason", "")).lower()
    if "deprecat" not in reason:
        fails.append("reason must contain 'deprecated' or 'deprecation' explaining why v3.1 is inapplicable")
    rec = str(data.get("recommendation", "")).lower()
    if not re.search(r"v4\.?2|aros.*v4|version 4|current", rec):
        fails.append("recommendation must direct fixes to current v4.2 codebase (not legacy v3.1)")
    _finish(fails)
main()
