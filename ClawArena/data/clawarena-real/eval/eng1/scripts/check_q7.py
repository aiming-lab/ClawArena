#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
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
    data, err = _load_json(ws / "analysis" / "cve_metadata.json")
    if err: _finish([err])
    # cvss_score: must be exactly 5.3 (no tolerance); 6.1 (Slack bot) and 7.5 (email) must fail
    cs = data.get("cvss_score")
    try:
        cs = float(cs)
    except (TypeError, ValueError):
        _finish(["cvss_score not numeric: %r" % cs])
    if abs(cs - 5.3) > 0.001:
        fails.append("cvss_score == %.4f (expected exactly 5.3 per NVD; 6.1 is the Slack-bot value, 7.5 is the email value — both wrong)" % cs)
    # cvss_vector must be verbatim full string (not just partial match)
    cv = str(data.get("cvss_vector") or "")
    EXPECTED_VECTOR = "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N"
    if cv != EXPECTED_VECTOR:
        fails.append(
            "cvss_vector == %r (expected verbatim '%s'; read SECURITY_CONTEXT.md for the NVD-authoritative full vector)" % (cv[:120], EXPECTED_VECTOR))
    # cwe_id == CWE-522
    cwe = str(data.get("cwe_id") or "")
    if cwe != "CWE-522":
        fails.append("cwe_id == %r (expected 'CWE-522')" % cwe)
    # epss_score: must be present and equal to "0.1957" (from Miggo research, as stated in the session data)
    epss = str(data.get("epss_score") or "")
    try:
        epss_f = float(epss)
    except (TypeError, ValueError):
        fails.append("epss_score == %r (not numeric; expected '0.1957' from Miggo report)" % epss)
        epss_f = None
    if epss_f is not None and abs(epss_f - 0.1957) > 0.0001:
        fails.append("epss_score == %r (expected '0.1957' from Miggo report in session data)" % epss)
    # snake_case guard
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
