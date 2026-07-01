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
    data, err = _load_json(ws / "analysis" / "cve_2023_32681_summary.json")
    if err: _finish([err])
    cve = str(data.get("cve_id") or "")
    if cve != "CVE-2023-32681":
        fails.append("cve_id == %r (expected 'CVE-2023-32681')" % cve)
    fv = str(data.get("fixed_version") or "")
    if fv != "2.31.0":
        fails.append("fixed_version == %r (expected '2.31.0')" % fv)
    rc = str(data.get("root_cause") or "")
    if "Proxy-Authorization" not in rc and "proxy-authorization" not in rc.lower():
        fails.append("root_cause == %r (must describe Proxy-Authorization header forwarding)" % rc[:120])
    # root_cause must also describe that the forwarding happens during redirects
    if "redirect" not in rc.lower():
        fails.append(
            "root_cause == %r: must mention 'redirect' — the vulnerability is that "
            "Proxy-Authorization headers were forwarded to destination servers when following "
            "redirects (read the UPDATE-1 NVD snapshot for the full technical description)" % rc[:120])
    # affected_before field: must identify the affected version threshold
    ab = str(data.get("affected_below") or "")
    if not ab:
        fails.append(
            "missing field 'affected_below': must state the version below which CVE-2023-32681 "
            "is present (read cve_2023_32681_nvd_snapshot.md in analysis/)")
    elif ab != "2.31.0":
        fails.append("affected_below == %r (expected '2.31.0'; the fix was released in 2.31.0)" % ab)
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
