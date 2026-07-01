#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".gitlab" / "ci" / "test.yml.bak").exists():
        fails.append("backup not found: .gitlab/ci/test.yml.bak")
    txt = _read(ws / ".gitlab" / "ci" / "test.yml")
    if txt is None:
        _finish(["file not found: .gitlab/ci/test.yml"])
    # All policy lines in test.yml must be 'pull', not 'pull-push'
    policy_lines = re.findall(r"policy\s*:\s*(\S+)", txt)
    for pol in policy_lines:
        if pol.strip().rstrip('"').rstrip("'") == "pull-push":
            fails.append("test.yml still has 'policy: pull-push' — parallel test jobs must use 'policy: pull'")
            break
    if not any(p.strip().rstrip('"').rstrip("'") == "pull" for p in policy_lines):
        fails.append("test.yml has no 'policy: pull' entries — parallel test jobs must use pull")
    btxt = _read(ws / ".gitlab" / "ci" / "build.yml")
    if btxt is None:
        fails.append("file not found: .gitlab/ci/build.yml")
    elif "pull-push" not in btxt:
        fails.append("build.yml lost 'policy: pull-push' for compile job — it must keep pull-push")
    _finish(fails)
main()
