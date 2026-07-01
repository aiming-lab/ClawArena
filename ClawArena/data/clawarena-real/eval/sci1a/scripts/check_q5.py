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
    data, err = _load_json(ws / "reports" / "wip" / "anderson_blot_summary.json")
    if err: _finish([err])
    # layer 1: structure (D: added max_reuse_count field)
    for key in ("researcher_label", "paper_dois", "total_reuse_count", "papers_analysed", "max_reuse_count"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["paper_dois"], list):
        fails.append("paper_dois must be a list")
    try:
        trc = int(data["total_reuse_count"])
        mrc = int(data["max_reuse_count"])
    except (TypeError, ValueError):
        fails.append("total_reuse_count and max_reuse_count must be integers"); _finish(fails)
    if fails: _finish(fails)
    # layer 3: truth (V9 verbatim label from TSV; A exact values; V4 DOI cross-round)
    rl = str(data.get("researcher_label", ""))
    # At Q5 time, the TSV has researcher_label == "Researcher_1" (before Q13 supersede)
    if rl != "Researcher_1":
        fails.append("researcher_label == %r (expected 'Researcher_1' — verbatim from TSV at Q5 time, before Q13 supersede)" % rl)
    dois_str = [str(d) for d in data["paper_dois"]]
    if "10.1016/j.ccr.2007.02.015" not in dois_str:
        fails.append("paper_dois must include '10.1016/j.ccr.2007.02.015' (Cancer Cell 2007 DOI)")
    if trc != 21:
        fails.append("total_reuse_count == %d (expected 21; sum reuse_count column in the TSV)" % trc)
    if mrc != 4:
        fails.append("max_reuse_count == %d (expected 4; max of reuse_count column in the TSV)" % mrc)
    _finish(fails)
main()
