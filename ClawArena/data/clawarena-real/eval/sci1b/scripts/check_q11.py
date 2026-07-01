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
    data, err = _load_json(ws / "output" / "q11_falsification_matrix.json")
    if err: _finish([err])
    mt = data.get("manipulation_types") or []
    mt_str = " ".join(str(x).lower() for x in mt)
    if "row_relocation" not in mt_str and "data_row" not in mt_str:
        fails.append("manipulation_types must contain 'row_relocation' or 'data_row_relocation' (got %s)" % mt)
    rc = data.get("retraction_count")
    try:
        if int(rc) != 4:
            fails.append("retraction_count == %r (expected 4)" % rc)
    except (TypeError, ValueError):
        fails.append("retraction_count not int: %r" % rc)
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected '1.0')" % data.get("schema_version"))
    # F: primary_forensic_method must be exactly "calcChain_xml" — verbatim from calcchain_reference.json method field
    pfm = str(data.get("primary_forensic_method") or "")
    if pfm != "calcChain_xml":
        fails.append("primary_forensic_method == %r (expected exactly 'calcChain_xml' — verbatim from cases/gino/raw_data_analysis/calcchain_reference.json 'method' field; not 'calcChain_xml_analysis' or other variant)" % pfm)
    _finish(fails)
main()
