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
    data, err = _load_json(ws / "analysis" / "fix_commit.json")
    if err: _finish([err])
    sha = str(data.get("commit_sha") or "")
    if sha != "57acb7c26d809cf864ec439b8bcd6364702022d5":
        fails.append(
            "commit_sha == %r (expected '57acb7c26d809cf864ec439b8bcd6364702022d5' "
            "per UPDATE-2 supersede)" % sha)
    sp = str(data.get("supersedes_pr") or "")
    if sp != "6963":
        fails.append("supersedes_pr == %r (expected '6963')" % sp)
    ap = str(data.get("authoritative_pr") or "")
    if ap != "6965":
        fails.append("authoritative_pr == %r (expected '6965')" % ap)
    _finish(fails)
main()
