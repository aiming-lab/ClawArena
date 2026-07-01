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
    data, err = _load_json(ws / "analysis" / "vuln_location.json")
    if err: _finish([err])
    # 1. cve_id verbatim
    cve = str(data.get("cve_id") or "")
    if cve != "CVE-2024-47081":
        fails.append("cve_id == %r (expected 'CVE-2024-47081')" % cve)
    # 2. root_cause_function == get_netrc_auth (not the bot decoy build_response)
    rcf = str(data.get("root_cause_function") or "")
    if rcf != "get_netrc_auth":
        fails.append("root_cause_function == %r (expected 'get_netrc_auth', not bot decoy 'build_response')" % rcf)
    # 3. vulnerable_file contains utils.py
    vf = str(data.get("vulnerable_file") or "")
    if "utils.py" not in vf:
        fails.append("vulnerable_file == %r (expected path containing 'utils.py')" % vf)
    # 4. vulnerable_line_range: must be present and start with the actual function start line 112
    #    The real get_netrc_auth function is at line 112 in src/requests/utils.py.
    #    Accepted format examples: "112-169", "112-168", "112-170" — must begin with "112".
    vlr = str(data.get("vulnerable_line_range") or "")
    if not vlr:
        fails.append("vulnerable_line_range field is missing or empty (read src/requests/utils.py to find the actual line)")
    else:
        m = re.match(r"^(\d+)", vlr)
        if not m or int(m.group(1)) != 112:
            fails.append(
                "vulnerable_line_range == %r: start line must be 112 "
                "(the actual start of get_netrc_auth in src/requests/utils.py; "
                "do NOT rely on the example in the question prompt)" % vlr)
    # 5. snake_case guard: no camelCase keys
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1 snake_case requirement" % k)
    _finish(fails)
main()
