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
    data, err = _load_json(ws / "reports" / "wip" / "papers_meta.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("total_papers", "issue_types", "anchor_dois"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    if not isinstance(data["total_papers"], int):
        fails.append("total_papers must be an int")
    if not isinstance(data["issue_types"], list):
        fails.append("issue_types must be a list")
    if not isinstance(data["anchor_dois"], list):
        fails.append("anchor_dois must be a list")
    if fails: _finish(fails)
    # layer 3: truth (A: exact count; issue_types completeness)
    anchor_dois_str = [str(d) for d in data["anchor_dois"]]
    if "10.1038/nm.3867" not in anchor_dois_str:
        fails.append("anchor_dois must contain '10.1038/nm.3867' (verbatim DOI from CSV; got %s)" % anchor_dois_str[:3])
    issue_types_str = sorted([str(t).lower().strip() for t in data["issue_types"]])
    # All three issue types present in the CSV must be enumerated
    for required in ("image_duplication", "mouse_figure_fabrication", "western_blot_manipulation"):
        if not any(required in t for t in issue_types_str):
            fails.append("issue_types missing '%s' (all three issue types from the CSV must be listed)" % required)
    # Exact count: papers_flagged.csv has exactly 58 rows
    if data["total_papers"] != 58:
        fails.append("total_papers == %d (expected exactly 58; count actual rows in papers_flagged.csv, not a guess)" % data["total_papers"])
    _finish(fails)
main()
