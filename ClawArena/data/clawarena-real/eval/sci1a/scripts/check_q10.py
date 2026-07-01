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
    # layer 1: hahn_nature_paper sub-object must exist
    hnp = data.get("hahn_nature_paper")
    if hnp is None:
        _finish(["integrity_matrix.json missing 'hahn_nature_paper' sub-object"])
    if not isinstance(hnp, dict):
        _finish(["hahn_nature_paper must be a JSON object"])
    for key in ("doi", "year", "citation_count_threshold"):
        if key not in hnp:
            fails.append("hahn_nature_paper missing key: " + key)
    if fails: _finish(fails)
    # layer 2: types
    try:
        year = int(hnp["year"])
        threshold = int(hnp["citation_count_threshold"])
    except (TypeError, ValueError) as e:
        _finish(["hahn_nature_paper numeric field error: " + str(e)])
    # layer 3: truth (V4 cross-round DOI, V9 verbatim)
    if str(hnp.get("doi")) != "10.1038/22780":
        fails.append("hahn_nature_paper.doi == %r (expected '10.1038/22780')" % hnp.get("doi"))
    if year != 1999:
        fails.append("hahn_nature_paper.year == %d (expected 1999)" % year)
    if threshold != 3000:
        fails.append("hahn_nature_paper.citation_count_threshold == %d (expected 3000, from '>3000' in document)" % threshold)
    # V4: retraction_count and correction_count must still be preserved from Q9
    if int(data.get("retraction_count", 0)) != 6:
        fails.append("retraction_count must still be 6 after Q10 update (V4 cross-round closure)")
    if int(data.get("correction_count", 0)) != 31:
        fails.append("correction_count must still be 31 after Q10 update (V4 cross-round closure)")
    _finish(fails)
main()
