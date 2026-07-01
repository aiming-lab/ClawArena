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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "oncall_audit.json")
    if err: _finish([err])
    for fld in ("compliant_nurses", "non_compliant_nurses", "gap_count", "recommendation"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 字段层
    cn = data.get("compliant_nurses", [])
    if not isinstance(cn, list) or len(cn) == 0:
        fails.append("compliant_nurses must be a non-empty list")
    # recommendation references SB 596
    rec = str(data.get("recommendation", "")).lower()
    if "sb 596" not in rec and "sb596" not in rec and "sb-596" not in rec:
        fails.append("recommendation must reference SB 596 on-call definition")
    # recommendation length ≤ 150 chars
    if len(str(data.get("recommendation", ""))) > 150:
        fails.append("recommendation exceeds 150 characters (P5 violation)")
    # gap_count must be non-negative int
    gc = data.get("gap_count")
    try:
        if int(gc) < 0:
            fails.append("gap_count must be >= 0")
    except (TypeError, ValueError):
        fails.append("gap_count not an int: %r" % gc)
    # V6 guard: make sure the archived list was NOT used
    # (archived nurses should not appear as compliant)
    archived_ids = {"RN-MS-OLD-01", "RN-ICU-OLD-01", "RN-TEL-OLD-01", "RN-SD-OLD-01"}
    cn_set = set(str(x) for x in cn)
    overlap = archived_ids & cn_set
    if overlap:
        fails.append("compliant_nurses contains archived/obsolete nurse IDs %s (use current list, not v2023-10)" % sorted(overlap))
    _finish(fails)
main()
main()
