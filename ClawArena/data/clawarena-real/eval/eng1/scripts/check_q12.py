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
    data, err = _load_json(ws / "analysis" / "impact_assessment.json")
    if err: _finish([err])
    svcs = data.get("affected_services")
    if not isinstance(svcs, list):
        _finish(["affected_services must be a JSON array (list)"])
    if len(svcs) != 3:
        fails.append(
            "affected_services has %d elements (expected exactly 3: "
            "services with uses_netrc=true AND requests < 2.32.4)" % len(svcs))
    for i, svc in enumerate(svcs):
        if not isinstance(svc, dict):
            fails.append("affected_services[%d] is not a JSON object" % i)
            continue
        for field in ("service_name", "requests_version", "uses_netrc"):
            if field not in svc:
                fails.append("affected_services[%d] missing field %r" % (i, field))
    # snake_case guard
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
