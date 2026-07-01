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
    if not (ws / ".github" / "workflows" / "deploy.yml.bak").exists():
        fails.append("backup not found: .github/workflows/deploy.yml.bak")
    txt = _read(ws / ".github" / "workflows" / "deploy.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/deploy.yml"])
    if not re.search(r"id-token\s*:\s*write", txt):
        fails.append("deploy.yml deploy job does not have 'id-token: write' permission")
    if not re.search(r"contents\s*:\s*read", txt):
        fails.append("deploy.yml lost 'contents: read' permission (must be preserved)")
    _finish(fails)
main()
