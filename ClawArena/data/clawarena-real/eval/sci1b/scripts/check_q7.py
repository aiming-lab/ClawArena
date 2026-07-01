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
    data, err = _load_json(ws / "output" / "q7_retraction_registry.json")
    if err: _finish([err])
    # retraction_count
    rc = data.get("retraction_count")
    try:
        if int(rc) != 4:
            fails.append("retraction_count == %r (expected 4)" % rc)
    except (TypeError, ValueError):
        fails.append("retraction_count not int: %r" % rc)
    papers = data.get("papers") or []
    if len(papers) < 4:
        fails.append("papers list has %d entries (expected >= 4)" % len(papers))
    # V9: verbatim PNAS DOI must appear
    all_dois = set()
    for p in papers:
        if isinstance(p, dict):
            all_dois.add(str(p.get("original_doi") or ""))
            all_dois.add(str(p.get("retraction_doi") or ""))
    if "10.1073/pnas.1209746109" not in all_dois:
        fails.append("PNAS original DOI '10.1073/pnas.1209746109' missing from retraction registry")
    # P5: each paper must have both original_doi and retraction_doi (non-null, non-empty)
    for i, p in enumerate(papers):
        if not isinstance(p, dict):
            continue
        od = p.get("original_doi")
        rd = p.get("retraction_doi")
        if not od or od == "null":
            fails.append("paper[%d] missing original_doi" % i)
        if not rd or rd == "null":
            fails.append("paper[%d] missing retraction_doi" % i)
    _finish(fails)
main()
