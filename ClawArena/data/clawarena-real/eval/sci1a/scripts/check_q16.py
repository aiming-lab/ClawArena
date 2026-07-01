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
    data, err = _load_json(ws / "reports" / "final" / "summary.json")
    if err: _finish([err])
    # layer 1: structure
    dfci = data.get("dfci")
    if not isinstance(dfci, dict):
        _finish(["summary.json must have a top-level 'dfci' object"])
    for key in ("retraction_count", "correction_count", "settlement_usd",
                "papers_flagged_final", "whistleblower_usd", "key_dois"):
        if key not in dfci:
            fails.append("dfci missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        rc = int(dfci["retraction_count"])
        cc = int(dfci["correction_count"])
        su = int(dfci["settlement_usd"])
        pff = int(dfci["papers_flagged_final"])
        wu = int(dfci["whistleblower_usd"])
    except (TypeError, ValueError) as e:
        _finish(["dfci numeric field error: " + str(e)])
    # layer 3: truth (A exact values; V4 final numerical closure)
    if rc != 6:
        fails.append("dfci.retraction_count == %d (expected 6)" % rc)
    if cc != 31:
        fails.append("dfci.correction_count == %d (expected 31)" % cc)
    if su != 15000000:
        fails.append("dfci.settlement_usd == %d (expected 15000000)" % su)
    # A: exact value — not a range
    if pff != 95:
        fails.append("dfci.papers_flagged_final == %d (expected exactly 95 per settlement agreement)" % pff)
    # A: exact whistleblower figure
    if wu != 2630000:
        fails.append("dfci.whistleblower_usd == %d (expected exactly 2630000 per settlement_summary.md)" % wu)
    # V9 verbatim DOIs
    key_dois_str = [str(d) for d in (dfci.get("key_dois") or [])]
    for doi in ("10.1126/science.1123480", "10.1038/nm.3867", "10.1182/blood-2008-10-186668"):
        if doi not in key_dois_str:
            fails.append("dfci.key_dois must include '%s'" % doi)
    # V4 cross-round: retraction_count here must equal integrity_matrix.json
    im, em = _load_json(ws / "reports" / "wip" / "integrity_matrix.json")
    if not em and im is not None:
        im_rc = int(im.get("retraction_count", -1))
        if im_rc != rc:
            fails.append("cross-round drift: summary.json dfci.retraction_count %d != integrity_matrix.json %d" % (rc, im_rc))
    _finish(fails)
main()
