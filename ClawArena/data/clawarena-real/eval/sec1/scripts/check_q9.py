#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv, os
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
    data, err = _load_json(ws / "work" / "risk_matrix.json")
    if err: _finish([err])
    # V8: required fields
    REQ = ["cve_id","cvss_score","estimated_exposure_hours","internet_exposed_count",
           "prod_host_count","remediation_priority","risk_level"]
    for f in REQ:
        if f not in data:
            fails.append("missing field: " + f)
    if fails: _finish(fails)
    if data.get("cve_id") != "CVE-2024-6387":
        fails.append("cve_id == %r (expected CVE-2024-6387)" % data.get("cve_id"))
    # A: exact score (no ±tolerance)
    try:
        score = float(data.get("cvss_score"))
        if score != 8.1:
            fails.append("cvss_score == %r (must be exactly 8.1)" % score)
    except (TypeError, ValueError):
        fails.append("cvss_score not numeric: %r" % data.get("cvss_score"))
    if str(data.get("risk_level","")).upper() != "HIGH":
        fails.append("risk_level == %r (expected HIGH)" % data.get("risk_level"))
    if str(data.get("remediation_priority","")) != "P1":
        fails.append("remediation_priority == %r (expected P1)" % data.get("remediation_priority"))
    # A: estimated_exposure_hours must be exactly 33
    # (disclosure 2024-07-01 00:00 UTC, report as-of 2024-07-02 09:00 UTC = 33 hours)
    eeh = data.get("estimated_exposure_hours")
    try:
        eeh = int(eeh)
        if eeh != 33:
            fails.append("estimated_exposure_hours == %d (must be exactly 33: from 2024-07-01T00:00Z to 2024-07-02T09:00Z)" % eeh)
    except (TypeError, ValueError):
        fails.append("estimated_exposure_hours not numeric: %r" % data.get("estimated_exposure_hours"))
    # C: prod_host_count must exactly match Q2's affected_assets.csv prod count
    phc = data.get("prod_host_count")
    try:
        phc = int(phc)
        # Cross-round closure: check against Q2 file if it exists
        q2_path = ws / "work" / "affected_assets.csv"
        if q2_path.exists():
            with q2_path.open(encoding="utf-8") as fh:
                q2_rows = list(csv.DictReader(fh))
            prod_count_q2 = sum(1 for r in q2_rows if r.get("env","").strip().lower() == "prod")
            if prod_count_q2 > 0 and phc != prod_count_q2:
                fails.append("prod_host_count drift: risk_matrix=%d, Q2 affected_assets prod=%d (must be identical)" % (phc, prod_count_q2))
        else:
            # No Q2 file: check against known value
            if phc != 154:
                fails.append("prod_host_count == %d (expected 154 from Q2 internal_inventory.csv)" % phc)
    except (TypeError, ValueError):
        fails.append("prod_host_count not int: %r" % data.get("prod_host_count"))
    # C: internet_exposed_count must match Q7 vulnerable_count (151)
    iec = data.get("internet_exposed_count")
    try:
        iec_val = int(iec)
        if iec_val <= 0:
            fails.append("internet_exposed_count must be positive")
        # Cross-round: if Q7 exposure_report.json exists, must match exactly
        q7_path = ws / "work" / "exposure_report.json"
        if q7_path.exists():
            q7_data = json.loads(q7_path.read_text(encoding="utf-8"))
            vc_q7 = q7_data.get("vulnerable_count")
            if vc_q7 is not None and iec_val != int(vc_q7):
                fails.append("internet_exposed_count drift: risk_matrix=%d, Q7 vulnerable_count=%d (must match exactly)" % (iec_val, int(vc_q7)))
    except (TypeError, ValueError):
        fails.append("internet_exposed_count not numeric: %r" % iec)
    _finish(fails)
main()
