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
    poc = ws / "scripts" / "reproduce_cve.py"
    if not poc.exists():
        _finish(["file not found: scripts/reproduce_cve.py"])
    txt = poc.read_text(encoding="utf-8")
    if "evil.com" not in txt:
        fails.append("reproduce_cve.py does not contain 'evil.com'")
    # run it
    r = subprocess.run([sys.executable, str(poc)], capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        fails.append("python scripts/reproduce_cve.py exited %d (stdout: %r, stderr: %r)" % (
            r.returncode, r.stdout[:200], r.stderr[:200]))
    _finish(fails)
main()
