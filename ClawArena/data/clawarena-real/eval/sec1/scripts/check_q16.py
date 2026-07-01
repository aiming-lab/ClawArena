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
    data, err = _load_json(ws / "work" / "final_remediation.json")
    if err: _finish([err])
    # V8: all 16 required fields
    REQ = ["affected_range","cve_id","cvss_score","cvss_vector","disclosure_date",
           "ghsa_id","patched_version","prior_cve","regression_commit",
           "remediation_deadline","rhel8_errata","rhel8_package","rhel9_errata",
           "rhel9_package","workaround_current","workaround_superseded"]
    for f in REQ:
        if f not in data:
            fails.append("missing field: " + f)
    if fails: _finish(fails)
    # V9/V4: spot-check key anchor values
    if data.get("cve_id") != "CVE-2024-6387":
        fails.append("cve_id == %r" % data.get("cve_id"))
    # A: exact cvss_score
    try:
        if float(data.get("cvss_score",0)) != 8.1:
            fails.append("cvss_score == %r (must be exactly 8.1)" % data.get("cvss_score"))
    except (TypeError, ValueError):
        fails.append("cvss_score not numeric")
    if data.get("cvss_vector") != "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H":
        fails.append("cvss_vector verbatim mismatch: %r" % data.get("cvss_vector"))
    if data.get("patched_version") != "9.8p1":
        fails.append("patched_version == %r (expected 9.8p1)" % data.get("patched_version"))
    if data.get("rhel9_errata") != "RHSA-2024:4312":
        fails.append("rhel9_errata == %r (expected RHSA-2024:4312)" % data.get("rhel9_errata"))
    # A: rhel9_package verbatim (full package name)
    if data.get("rhel9_package") != "openssh-8.7p1-38.el9_4.1":
        fails.append("rhel9_package == %r (must be exactly openssh-8.7p1-38.el9_4.1)" % data.get("rhel9_package"))
    # A: rhel8_package verbatim
    if data.get("rhel8_package") != "openssh-8.0p1-19.el8_10.1":
        fails.append("rhel8_package == %r (must be exactly openssh-8.0p1-19.el8_10.1)" % data.get("rhel8_package"))
    if data.get("rhel8_errata") != "RHSA-2024:4340":
        fails.append("rhel8_errata == %r (expected RHSA-2024:4340)" % data.get("rhel8_errata"))
    # A: remediation_deadline must be exact ISO-8601 UTC string (with seconds)
    dl = str(data.get("remediation_deadline",""))
    if dl != "2024-07-05T09:00:00Z":
        fails.append("remediation_deadline == %r (must be exactly '2024-07-05T09:00:00Z' in ISO-8601 UTC with seconds)" % dl)
    # V10: workaround_superseded must be exactly "LoginGraceTime 0"
    ws_sup = str(data.get("workaround_superseded",""))
    if ws_sup != "LoginGraceTime 0":
        fails.append("workaround_superseded == %r (must be exactly 'LoginGraceTime 0')" % ws_sup)
    # workaround_current must contain MaxStartups 10:30:100 verbatim
    wc = str(data.get("workaround_current",""))
    if "MaxStartups 10:30:100" not in wc:
        fails.append("workaround_current %r must contain verbatim 'MaxStartups 10:30:100'" % wc)
    if data.get("prior_cve") != "CVE-2006-5051":
        fails.append("prior_cve == %r (expected CVE-2006-5051)" % data.get("prior_cve"))
    # A: regression_commit full hash
    rc = str(data.get("regression_commit",""))
    if rc != "752250caabda3dd24635503c4cd689b32a650794":
        fails.append("regression_commit == %r (must be the full 40-char hash: 752250caabda3dd24635503c4cd689b32a650794)" % rc)
    # C: cross-round disclosure_date must match Q1
    if data.get("disclosure_date") != "2024-07-01":
        fails.append("disclosure_date == %r (expected 2024-07-01, consistent with Q1)" % data.get("disclosure_date"))
    _finish(fails)
main()
