#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    data, err = _load_json(ws / "rca_outputs" / "case_C_assessment.json")
    if err: _finish([err])
    # 必须字段
    required = {"status", "reason", "should_include_in_current_rca", "affected_models", "units"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # status 必须表示 archived/legacy
    status = str(data.get("status", "")).upper()
    if not ("ARCHIVE" in status or "LEGACY" in status or "DEPRECATED" in status):
        fails.append("status %r must indicate ARCHIVED_LEGACY (not an active case)" % status)
    # should_include_in_current_rca 必须 false
    incl = data.get("should_include_in_current_rca")
    if incl is not False:
        fails.append("should_include_in_current_rca == %r (must be false — 2019 case is out of scope)" % incl)
    # units 必须为 11299
    try:
        u = int(data.get("units"))
        if u != 11299:
            fails.append(
                "units == %d (must be 11299 — the SynchroMed II recall affected approximately 11,299 units "
                "per the archived recall document; note: 5 is motor stall reports, not units)" % u
            )
    except (TypeError, ValueError):
        fails.append("units not numeric: %r" % data.get("units"))
    # affected_models 必须是含至少两个 Medtronic 型号的列表
    am = data.get("affected_models")
    if not isinstance(am, list) or len(am) < 2:
        fails.append(
            "affected_models must be a list with >= 2 entries (8637-20 and 8637-40 per archived recall document)"
        )
    else:
        am_txt = json.dumps(am, ensure_ascii=False)
        if "8637" not in am_txt:
            fails.append("affected_models must contain the SynchroMed II model numbers (8637-20 and/or 8637-40)")
    _finish(fails)
main()
