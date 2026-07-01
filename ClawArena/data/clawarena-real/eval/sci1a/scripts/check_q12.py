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
    data, err = _load_json(ws / "reports" / "wip" / "papers_update_record.json")
    if err: _finish([err])
    # layer 1: structure
    for key in ("papers_v1_count", "papers_v2_count", "count_delta", "anchor_doi_present"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        v1 = int(data["papers_v1_count"])
        v2 = int(data["papers_v2_count"])
        delta = int(data["count_delta"])
    except (TypeError, ValueError) as e:
        _finish(["numeric field error: " + str(e)])
    # layer 3: truth (V2 dynamic update; V4 arithmetic closure; V10 v2 supersedes v1)
    if v2 <= v1:
        fails.append("papers_v2_count (%d) must be > papers_v1_count (%d)" % (v2, v1))
    if delta != v2 - v1:
        fails.append("count_delta == %d but v2-v1 == %d (arithmetic must close)" % (delta, v2 - v1))
    # V4: v2 count should be ~95
    if not (85 <= v2 <= 105):
        fails.append("papers_v2_count == %d (expected ~95 per settlement agreement)" % v2)
    if data.get("anchor_doi_present") is not True:
        fails.append("anchor_doi_present must be true (10.1038/nm.3867 must appear in v2 CSV)")
    _finish(fails)
main()
