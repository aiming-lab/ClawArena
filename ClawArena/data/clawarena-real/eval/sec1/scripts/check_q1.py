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
    data, err = _load_json(ws / "work" / "vuln_summary.json")
    if err: _finish([err])
    # V8: schema-by-shape — required fields
    REQ = ["affected_range", "cve_id", "cwe_ids", "cvss_score", "cvss_vector",
           "disclosure_date", "ghsa_id", "severity"]
    for f in REQ:
        if f not in data:
            fails.append("missing required field: " + f)
    if fails: _finish(fails)
    # V9: verbatim field values
    if data.get("cve_id") != "CVE-2024-6387":
        fails.append("cve_id == %r (expected CVE-2024-6387)" % data.get("cve_id"))
    # A: exact score match (not ±0.2 — NVD verbatim is 8.1)
    try:
        score = float(data.get("cvss_score"))
        if score != 8.1:
            fails.append("cvss_score == %r (must be exactly 8.1 from NVD — do not round)" % score)
    except (TypeError, ValueError):
        fails.append("cvss_score not numeric: %r" % data.get("cvss_score"))
    if data.get("cvss_vector") != "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H":
        fails.append("cvss_vector == %r (expected verbatim NVD vector)" % data.get("cvss_vector"))
    cwe_ids = data.get("cwe_ids") or []
    if not isinstance(cwe_ids, list) or "CWE-362" not in cwe_ids:
        fails.append("cwe_ids must be a list containing CWE-362; got %r" % cwe_ids)
    if data.get("disclosure_date") != "2024-07-01":
        fails.append("disclosure_date == %r (expected 2024-07-01)" % data.get("disclosure_date"))
    if data.get("ghsa_id") != "GHSA-2x8c-95vh-gfv4":
        fails.append("ghsa_id == %r (expected GHSA-2x8c-95vh-gfv4)" % data.get("ghsa_id"))
    # A: severity must be verbatim "High" (title case) as in GHSA advisory — not "HIGH" or "high"
    sev = str(data.get("severity", ""))
    if sev != "High":
        fails.append("severity == %r (must be verbatim 'High' from the GHSA advisory — not 'HIGH' or 'high')" % sev)
    # A: affected_range must use the NVD/GHSA canonical format with <= and <
    ar = str(data.get("affected_range", ""))
    if not ("8.5p1" in ar and "9.8p1" in ar):
        fails.append("affected_range %r must reference both 8.5p1 and 9.8p1 (the actual advisory bounds)" % ar)
    _finish(fails)
main()
