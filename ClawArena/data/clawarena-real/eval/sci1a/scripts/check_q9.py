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
    data, err = _load_json(ws / "reports" / "wip" / "integrity_matrix.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("case_id", "manipulation_types", "retraction_count",
                "correction_count", "papers_flagged_initial"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["manipulation_types"], list):
        fails.append("manipulation_types must be a list")
    try:
        rc = int(data["retraction_count"])
        cc = int(data["correction_count"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field error: " + str(e)])
    if fails: _finish(fails)
    # layer 3: truth
    if str(data.get("case_id")) != "dfci":
        fails.append("case_id must be 'dfci' (got %r)" % data.get("case_id"))
    mt_str = [str(t).lower() for t in data["manipulation_types"]]
    if not any("image_duplication" in t for t in mt_str):
        fails.append("manipulation_types must contain 'image_duplication'")
    if rc != 6:
        fails.append("retraction_count == %d (expected 6 per DFCI announcement)" % rc)
    if cc != 31:
        fails.append("correction_count == %d (expected 31 per DFCI announcement)" % cc)
    # V4 cross-round: papers_flagged_initial must equal total_papers in papers_meta.json (from Q2)
    try:
        pfi = int(data["papers_flagged_initial"])
    except (TypeError, ValueError):
        fails.append("papers_flagged_initial must be an integer")
        _finish(fails)
    # A: exact value 58 (verbatim row count of papers_flagged.csv)
    if pfi != 58:
        fails.append("papers_flagged_initial == %d (expected exactly 58 — the exact row count of papers_flagged.csv)" % pfi)
    # V4 cross-round closure: must also equal what Q2 recorded in papers_meta.json
    meta, me = _load_json(ws / "reports" / "wip" / "papers_meta.json")
    if not me and meta is not None:
        meta_tp = int(meta.get("total_papers", -1))
        if meta_tp != pfi:
            fails.append("cross-round drift: integrity_matrix papers_flagged_initial %d != papers_meta.json total_papers %d (must be consistent)" % (pfi, meta_tp))
    _finish(fails)
main()
