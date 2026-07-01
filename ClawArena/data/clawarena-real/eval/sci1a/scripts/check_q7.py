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

def _read_tsv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading TSV " + p.name + ": " + str(e)

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading CSV " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    # P1 check: file name
    fpath = ws / "reports" / "wip" / "2024-01-02_dfci_preliminary.md"
    txt = _read(fpath)
    if txt is None:
        _finish(["file not found: reports/wip/2024-01-02_dfci_preliminary.md (P1: must use YYYY-MM-DD_caseid_type.md naming)"])
    low = txt.lower()
    # layer 1: existence confirmed
    # layer 2: structure (P2 four sections)
    for section in ("background", "evidence", "classification", "recommendation"):
        if section not in low:
            fails.append("missing mandatory section '%s' (P2 requires Background/Evidence/Classification/Recommendation)" % section)
    # layer 3: truth
    if "15,000,000" not in txt and "15000000" not in txt:
        fails.append("report must contain settlement figure '15,000,000'")
    if "cope" not in low:
        fails.append("report must reference COPE (classification context)")
    # COPE type: accept Type 4 or Type 2
    if "type 4" not in low and "type 2" not in low and "unreliable" not in low and "misconduct" not in low:
        fails.append("Classification section must include COPE Type 4 or Type 2 designation")
    # independent blog count must be cited (47 — from imagetwin_report.json independent analysis)
    if "47" not in txt:
        fails.append(
            "report must cite the independent blog analysis figure '47' image-pair anomalies "
            "(from imagetwin_report.json, the blog's independent tally)"
        )
    _finish(fails)
main()
