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
    data, err = _load_json(ws / "output" / "medsurg_night_analysis.json")
    if err: _finish([err])
    # 结构层
    for fld in ("violation_shifts", "total_violation_count", "root_cause", "corrective_measures"):
        if fld not in data:
            # try plural/singular variants
            alt = fld.rstrip("s") if fld.endswith("s") else fld + "s"
            if alt not in data:
                fails.append("missing field %r (or %r)" % (fld, alt))
    if fails: _finish(fails)
    # 字段层
    vc_key = "total_violation_count" if "total_violation_count" in data else "violation_count"
    vs_key = "violation_shifts" if "violation_shifts" in data else "violations"
    cm_key = "corrective_measures" if "corrective_measures" in data else "corrective_actions"
    try:
        vc = int(data.get(vc_key, 0))
        if vc < 5:
            fails.append("total_violation_count == %d (expected >= 5)" % vc)
    except (TypeError, ValueError):
        fails.append("total_violation_count not an int: %r" % data.get(vc_key))
    # 真值层：root_cause mentions FMLA or CFRA
    rc = str(data.get("root_cause", "")).lower()
    if "fmla" not in rc and "cfra" not in rc and "family.medical" not in rc:
        fails.append("root_cause does not mention FMLA or CFRA")
    # corrective_measures contains float pool and on-call list
    cm = data.get(cm_key, [])
    cm_text = " ".join(str(c) for c in cm).lower() if isinstance(cm, list) else str(cm).lower()
    if "float" not in cm_text and "pool" not in cm_text:
        fails.append("corrective_measures does not mention float pool expansion")
    if ("on-call" not in cm_text and "on.call" not in cm_text and
            "on_call" not in cm_text and "oncall" not in cm_text):
        fails.append("corrective_measures does not mention on-call list update")
    _finish(fails)
main()
main()
