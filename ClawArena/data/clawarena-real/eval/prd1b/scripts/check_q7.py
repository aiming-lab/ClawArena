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
    data, err = _load_json(ws / "reports" / "slack_synthesis_q7.json")
    if err: _finish([err])
    # conflict_identified must be True
    if data.get("conflict_identified") is not True:
        fails.append("conflict_identified must be true")
    # decoy_penalty_cited must be 45000
    dpc = data.get("decoy_penalty_cited")
    try:
        dpc = int(float(dpc))
        if dpc != 45000:
            fails.append("decoy_penalty_cited must be 45000 (the DECOY's wrong figure), got %d" % dpc)
    except (TypeError, ValueError):
        fails.append("decoy_penalty_cited not numeric: %r" % dpc)
    # correct_penalty must be 51744
    cp = data.get("correct_penalty")
    try:
        cp = int(float(cp))
        if cp != 51744:
            fails.append("correct_penalty must be 51744 (the real 2024 FTC rate), got %d" % cp)
    except (TypeError, ValueError):
        fails.append("correct_penalty not numeric: %r" % cp)
    # supersede_reference must mention CEO-RETRACT-20260312-01
    sr = str(data.get("supersede_reference","")).upper()
    if "CEO-RETRACT" not in sr and "RETRACT" not in sr:
        fails.append("supersede_reference must reference CEO-RETRACT-20260312-01 (got %r)" % sr[:50])
    # correct_position must mention 51744
    cp_str = str(data.get("correct_position",""))
    if "51,744" not in cp_str and "51744" not in cp_str:
        fails.append("correct_position must cite $51,744 as the accurate penalty figure")
    _finish(fails)
main()
