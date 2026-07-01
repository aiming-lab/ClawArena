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
    data, err = _load_json(ws / "output" / "sla_compliance_Q4.json")
    if err: _finish([err])
    total = data.get("total_count")
    breach = data.get("breach_count")
    try:
        total_i = int(total); breach_i = int(breach)
    except (TypeError, ValueError):
        _finish(["total_count or breach_count not numeric: %r %r" % (total, breach)])
    if total_i != 200:
        fails.append("total_count == %d (expected 200)" % total_i)
    # cross-round closure with Q3 breach file
    q3, e3 = _load_json(ws / "output" / "breach_tickets_Q4.json")
    if not e3 and q3 is not None:
        q3_tix = q3 if isinstance(q3, list) else q3.get("tickets", [])
        if breach_i != len(q3_tix):
            fails.append("breach_count %d != Q3 breach file count %d (cross-round closure fail)" % (breach_i, len(q3_tix)))
    # by_severity arithmetic
    by_sev = data.get("by_severity") or {}
    for sev, entry in by_sev.items():
        if not isinstance(entry, dict):
            continue
        sc = entry.get("total_count"); bc = entry.get("breach_count"); cr = entry.get("compliance_rate")
        try:
            sc_i = int(sc); bc_i = int(bc); cr_f = float(cr)
        except (TypeError, ValueError):
            continue
        expected_cr = round((sc_i - bc_i) / sc_i * 100, 2) if sc_i > 0 else 0
        if abs(cr_f - expected_cr) > 0.1:
            fails.append("by_severity[%s] compliance_rate=%.2f != expected %.2f" % (sev, cr_f, expected_cr))
    _finish(fails)
main()
