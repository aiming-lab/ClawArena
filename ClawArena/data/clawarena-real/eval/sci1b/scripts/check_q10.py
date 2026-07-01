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
    data, err = _load_json(ws / "output" / "q10_cope_classification.json")
    if err: _finish([err])
    if data.get("case_id") != "RIO-2023-GINO":
        fails.append("case_id == %r (expected 'RIO-2023-GINO')" % data.get("case_id"))
    cope_type = str(data.get("cope_type") or "").lower()
    if "type 2" not in cope_type and "type 4" not in cope_type:
        fails.append("cope_type == %r (must contain 'Type 2' or 'Type 4')" % data.get("cope_type"))
    papers = data.get("papers") or []
    if len(papers) < 4:
        fails.append("papers array has %d entries (expected >= 4)" % len(papers))
    # V9: PNAS DOI must appear
    all_dois = set()
    for p in papers:
        if isinstance(p, dict):
            all_dois.add(str(p.get("original_doi") or ""))
    if "10.1073/pnas.1209746109" not in all_dois:
        fails.append("PNAS original DOI '10.1073/pnas.1209746109' missing from classification papers")
    # F: cope_section_ref must cite the section from guidelines verbatim
    cref = str(data.get("cope_section_ref") or "").lower()
    if "type 2" not in cref and "type 4" not in cref:
        fails.append("cope_section_ref == %r (must cite the COPE type verbatim e.g. 'Type 2: Research Misconduct'; read protocols/cope_retraction_guidelines.md)" % data.get("cope_section_ref"))
    _finish(fails)
main()
