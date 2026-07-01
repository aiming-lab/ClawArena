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
    data, err = _load_json(ws / "output" / "q5_calcchain_findings.json")
    if err: _finish([err])
    # V9: verbatim DOI
    doi = str(data.get("paper_doi") or "")
    if doi != "10.1073/pnas.1209746109":
        fails.append("paper_doi == %r (expected verbatim '10.1073/pnas.1209746109')" % doi)
    sr = data.get("suspicious_rows")
    try:
        if int(sr) != 8:
            fails.append("suspicious_rows == %r (expected 8)" % sr)
    except (TypeError, ValueError):
        fails.append("suspicious_rows not int: %r" % sr)
    method = str(data.get("method") or "")
    if "calcchain_xml" not in method.lower() and "calcchain" not in method.lower():
        fails.append("method == %r (must contain 'calcChain_xml')" % method)
    n = data.get("n_total")
    try:
        if not (95 <= int(n) <= 105):
            fails.append("n_total == %r (expected 101, consistent with q2)" % n)
    except (TypeError, ValueError):
        fails.append("n_total not int: %r" % n)
    # F+C: suspicious_participant_ids must be the exact 8 IDs from calcchain_reference.json
    calcchain_path = ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json"
    ccref, ccerr = _load_json(calcchain_path)
    expected_ids = []
    if not ccerr and ccref:
        expected_ids = [str(x) for x in (ccref.get("suspicious_participant_ids") or [])]
    provided_ids = data.get("suspicious_participant_ids")
    if provided_ids is None:
        fails.append("suspicious_participant_ids field missing (must be the exact participant IDs from calcchain_reference.json: %s)" % expected_ids)
    else:
        prov_set = set(str(x) for x in (provided_ids or []))
        exp_set = set(expected_ids)
        if prov_set != exp_set:
            fails.append("suspicious_participant_ids %s does not match calcchain_reference.json expected %s" % (sorted(prov_set), sorted(exp_set)))
    _finish(fails)
main()
