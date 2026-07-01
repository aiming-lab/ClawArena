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
    data, err = _load_json(ws / "work" / "exposure_report.json")
    if err: _finish([err])
    # V8: required fields
    for f in ("total_scanned","vulnerable_count","version_distribution","top_5_exposed_orgs"):
        if f not in data:
            fails.append("missing field: " + f)
    if fails: _finish(fails)
    # A: total_scanned must be exactly 220 (entries in shodan_export_2024-07-02.json)
    ts = data.get("total_scanned")
    if not isinstance(ts, int) or ts != 220:
        fails.append("total_scanned == %r (must be exactly 220 — the count of entries in shodan_export_2024-07-02.json)" % ts)
    # A: vulnerable_count must be exactly 151
    vc = data.get("vulnerable_count")
    if not isinstance(vc, int) or vc != 151:
        fails.append("vulnerable_count == %r (must be exactly 151 — entries where CVE-2024-6387 is in the vulns list)" % vc)
    # A: version_distribution must only contain VULNERABLE versions (8.5p1–9.7p1 range)
    # Do NOT include non-vulnerable versions like 7.x, 8.0-8.4, 9.8p1 (patched)
    VULN_VERS = {
        "OpenSSH_8.5p1","OpenSSH_8.6p1","OpenSSH_8.7p1","OpenSSH_8.8p1",
        "OpenSSH_8.9p1","OpenSSH_9.0p1","OpenSSH_9.1p1","OpenSSH_9.2p1",
        "OpenSSH_9.3p2","OpenSSH_9.4p1","OpenSSH_9.5p1","OpenSSH_9.6p1",
        "OpenSSH_9.7p1"
    }
    vd = data.get("version_distribution")
    if not isinstance(vd, dict) or not vd:
        fails.append("version_distribution must be a non-empty object")
    else:
        non_vuln_keys = [k for k in vd.keys() if k not in VULN_VERS]
        if non_vuln_keys:
            fails.append("version_distribution contains non-vulnerable versions %r — only include versions where CVE-2024-6387 is in the vulns list" % non_vuln_keys[:3])
    # top_5_exposed_orgs: list of 5 strings
    t5 = data.get("top_5_exposed_orgs")
    if not isinstance(t5, list) or len(t5) != 5:
        fails.append("top_5_exposed_orgs must be a list of exactly 5 elements; got %r" % t5)
    _finish(fails)
main()
