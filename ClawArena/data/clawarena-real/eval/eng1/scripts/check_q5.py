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
    txt = _read(ws / "src" / "requests" / "utils.py")
    if txt is None:
        _finish(["file not found: src/requests/utils.py"])
    # Check for the actual vulnerable assignment (not mentions in docstrings/comments)
    # The vulnerable pattern is an assignment: host = ri.netloc.split(...)
    if re.search(r"^\s*host\s*=\s*ri\.netloc\.split", txt, re.MULTILINE):
        fails.append("src/requests/utils.py still has 'host = ri.netloc.split(...)' assignment (vulnerability not removed)")
    if "ri.hostname" not in txt:
        fails.append("src/requests/utils.py does not contain 'ri.hostname' (fix not applied)")
    if "if host is None:" not in txt:
        fails.append("src/requests/utils.py missing 'if host is None:' None check")
    if "get_netrc_auth" not in txt:
        fails.append("get_netrc_auth function no longer present in utils.py")
    _finish(fails)
main()
