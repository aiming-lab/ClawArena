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
    data, err = _load_json(ws / "work" / "cve_comparison.json")
    if err: _finish([err])
    # V8: both CVE keys must be present
    if "CVE-2024-6387" not in data:
        fails.append("cve_comparison.json missing CVE-2024-6387 entry")
    if "CVE-2024-6409" not in data:
        fails.append("cve_comparison.json missing CVE-2024-6409 entry")
    if fails: _finish(fails)
    e6387 = data.get("CVE-2024-6387", {})
    e6409 = data.get("CVE-2024-6409", {})
    # D: each entry must have all three required fields: affected_versions, cvss_score, scope
    for cve_key, entry in [("CVE-2024-6387", e6387), ("CVE-2024-6409", e6409)]:
        for field in ("affected_versions", "cvss_score", "scope"):
            if field not in entry:
                fails.append("cve_comparison.json[%r] missing required field %r" % (cve_key, field))
    if fails: _finish(fails)
    # A: CVE-2024-6387 exact cvss_score 8.1
    try:
        s6387 = float(e6387.get("cvss_score", 0))
        if s6387 != 8.1:
            fails.append("CVE-2024-6387 cvss_score == %r (must be exactly 8.1)" % s6387)
    except (TypeError, ValueError):
        fails.append("CVE-2024-6387 cvss_score not numeric: %r" % e6387.get("cvss_score"))
    # A: CVE-2024-6409 exact cvss_score 7.0
    try:
        s6409 = float(e6409.get("cvss_score", 0))
        if s6409 != 7.0:
            fails.append("CVE-2024-6409 cvss_score == %r (must be exactly 7.0 from assets/advisories/CVE-2024-6409_detail.json — not the same as CVE-2024-6387's 8.1)" % s6409)
    except (TypeError, ValueError):
        fails.append("CVE-2024-6409 cvss_score not numeric: %r" % e6409.get("cvss_score"))
    # CVE-2024-6409 must have narrower version range (8.7 or 8.8 RHEL backport)
    av6409 = str(e6409.get("affected_versions",""))
    if not ("8.7" in av6409 or "8.8" in av6409):
        fails.append("CVE-2024-6409 affected_versions must mention 8.7 or 8.8 (RHEL backport versions only); got %r" % av6409)
    # D: scope field for CVE-2024-6409 must reference privilege_separation or child process
    sc6409 = str(e6409.get("scope","")).lower()
    if "privilege" not in sc6409 and "child" not in sc6409 and "privsep" not in sc6409:
        fails.append("CVE-2024-6409 scope %r must reference privilege separation child process (different from CVE-2024-6387's main sshd scope)" % e6409.get("scope"))
    # Must NOT share the same cvss_score as 6387
    try:
        if abs(float(e6387.get("cvss_score",0)) - float(e6409.get("cvss_score",0))) < 0.5:
            fails.append("CVE-2024-6387 and CVE-2024-6409 must have different cvss_score values (6387=8.1, 6409=7.0)")
    except (TypeError, ValueError):
        pass
    _finish(fails)
main()
