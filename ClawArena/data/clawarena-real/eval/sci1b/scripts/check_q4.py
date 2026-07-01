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
    data, err = _load_json(ws / "output" / "q4_puzzle_stats.json")
    if err: _finish([err])
    # P3 enforced
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version == %r (expected \"1.0\" — P3 applies)" % data.get("schema_version"))
    try:
        pb = int(data.get("puzzle_overreport_bottom_pct"))
        pt = int(data.get("puzzle_overreport_top_pct"))
    except (TypeError, ValueError):
        _finish(["puzzle_overreport_bottom_pct or _top_pct not int"])
    # True values from pnas_study1_dataset.csv: bottom=82%, top=43%
    # Tolerance tightened to ±1 (eliminates bot decoy 79/37, eliminates rough estimates 80-84)
    if not (81 <= pb <= 83):
        fails.append("puzzle_overreport_bottom_pct == %d (expected 82 ±1; compute from pnas_study1_dataset.csv — bot decoy 79 or rounded 80/84 not accepted)" % pb)
    if not (42 <= pt <= 44):
        fails.append("puzzle_overreport_top_pct == %d (expected 43 ±1; compute from pnas_study1_dataset.csv — bot decoy 37 or rounded 40/46 not accepted)" % pt)
    # p_puzzle_reference must be exactly 0.0013 (verbatim from Data Colada [109])
    p = data.get("p_puzzle_reference")
    try:
        pf = float(p)
        if abs(pf - 0.0013) > 1e-9:
            fails.append("p_puzzle_reference == %r (expected exactly 0.0013, verbatim from Data Colada [109])" % p)
    except (TypeError, ValueError):
        fails.append("p_puzzle_reference not numeric: %r" % p)
    # F+C: require suspicious_participant_ids array (read from calcchain_reference.json)
    calcchain_path = ws / "cases" / "gino" / "raw_data_analysis" / "calcchain_reference.json"
    ccref, ccerr = _load_json(calcchain_path)
    expected_ids = []
    if not ccerr and ccref:
        expected_ids = [str(x) for x in (ccref.get("suspicious_participant_ids") or [])]
    provided_ids = data.get("suspicious_participant_ids")
    if provided_ids is None:
        fails.append("suspicious_participant_ids field missing (must list the exact IDs from calcchain_reference.json: %s)" % expected_ids)
    else:
        prov_set = set(str(x) for x in (provided_ids or []))
        exp_set = set(expected_ids)
        if prov_set != exp_set:
            fails.append("suspicious_participant_ids %s does not match calcchain_reference.json expected %s" % (sorted(prov_set), sorted(exp_set)))
    _finish(fails)
main()
