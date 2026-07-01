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

REQUIRED_FIELDS = [
    "nature_of_breach",
    "categories_and_number_of_data_subjects",
    "categories_and_number_of_records",
    "DPO_contact",
    "likely_consequences",
    "measures_taken"
]

def _nonempty(v):
    if v is None: return False
    if isinstance(v, (list, dict)): return len(v) > 0
    if isinstance(v, str): return v.strip() != ""
    return True

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "breach" / "breach_notification_final.json")
    if err: _finish([err])
    for f in REQUIRED_FIELDS:
        if not _nonempty(data.get(f)):
            fails.append("breach_notification_final.json missing/empty field: %s" % f)
    # Exact-value anchors from incident_20250314_report.md
    dsub = str(data.get("categories_and_number_of_data_subjects", ""))
    if not re.search(r"15[,.]?000|15000", dsub):
        fails.append(
            "categories_and_number_of_data_subjects %r must include the figure 15,000 "
            "(from incident_20250314_report.md)" % dsub[:100]
        )
    drec = str(data.get("categories_and_number_of_records", ""))
    if not re.search(r"45[,.]?000|45000", drec):
        fails.append(
            "categories_and_number_of_records %r must include the figure 45,000 "
            "(from incident_20250314_report.md)" % drec[:100]
        )
    _finish(fails)
main()
