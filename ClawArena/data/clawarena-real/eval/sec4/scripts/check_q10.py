#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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
    data, err = _load_json(ws / "audit" / "dpo_appointment_check.json")
    if err: _finish([err])
    # mandatory must be "TRUE" string (P4)
    mand = data.get("mandatory")
    if mand != "TRUE":
        fails.append("mandatory == %r (expected string \"TRUE\"; 800k users + systematic monitoring triggers Art.37(1)(b))" % mand)
    # criterion_met must reference "Art. 37(1)(b)" verbatim (P2)
    cm = str(data.get("criterion_met", ""))
    if not re.search(r"Art\.\s*37\(1\)\(b\)", cm):
        fails.append("criterion_met == %r (expected verbatim \"Art. 37(1)(b)\" format; do not use Discord old memo)" % cm)
    # dpo_name must match exactly "Lena Fischer" from company/org_chart.json
    dpo_name = str(data.get("dpo_name", "")).strip()
    if not dpo_name:
        fails.append("dpo_name must be non-empty")
    elif dpo_name.lower() != "lena fischer":
        fails.append(
            "dpo_name == %r (expected verbatim \"Lena Fischer\" from company/org_chart.json; "
            "read the file — do not invent or abbreviate the name)" % dpo_name
        )
    _finish(fails)
main()
