#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    data, err = _load_json(ws / "output" / "q12_gh_ss_patch.json")
    if err: _finish([err])
    # state verbatim
    st = data.get("state")
    if st != "resolved":
        fails.append("state == %r (expected verbatim 'resolved' — GitHub SS state enum)" % st)
    # resolution verbatim
    res = data.get("resolution")
    if res != "revoked":
        fails.append("resolution == %r (expected verbatim 'revoked' — GitHub SS resolution enum for revoked key)" % res)
    # alert_number == 1
    an = data.get("alert_number")
    try:
        if int(an) != 1:
            fails.append("alert_number == %r (expected 1 for the triggering OpenAI key alert)" % an)
    except (TypeError, ValueError):
        fails.append("alert_number must be an int: %r" % an)
    _finish(fails)
main()
