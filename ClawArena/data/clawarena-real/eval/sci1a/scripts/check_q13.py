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
    # Check 1: anderson_blot_analysis.tsv researcher_label (V6 supersede; V2 update)
    rows, err = _read_tsv(ws / "cases" / "dfci" / "image_analysis" / "anderson_blot_analysis.tsv")
    if err: _finish([err])
    if len(rows) == 0:
        _finish(["anderson_blot_analysis.tsv is empty"])
    # All rows must have researcher_label == "Kenneth_C._Anderson"
    for i, row in enumerate(rows):
        rl = str(row.get("researcher_label", "")).strip()
        if rl != "Kenneth_C._Anderson":
            fails.append(
                "anderson_blot_analysis.tsv row %d: researcher_label == %r "
                "(expected 'Kenneth_C._Anderson' after supersede; not 'Researcher_1' or 'William_Hahn')" % (i + 1, rl)
            )
    # Check 2: researcher_id_log.md (V10 supersede record)
    txt = _read(ws / "reports" / "wip" / "researcher_id_log.md")
    if txt is None:
        fails.append("file not found: reports/wip/researcher_id_log.md")
    else:
        low = txt.lower()
        if "supersede" not in low and "superseded" not in low:
            fails.append("researcher_id_log.md must contain 'superseded' (recording the supersede event)")
        if "2025-12" not in txt:
            fails.append("researcher_id_log.md must reference date '2025-12' (date of legal supersede confirmation)")
    _finish(fails)
main()
