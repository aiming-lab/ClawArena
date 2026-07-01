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
    if not (ws / ".github" / "workflows" / "ci.yml.bak").exists():
        fails.append("backup not found: .github/workflows/ci.yml.bak")
    txt = _read(ws / ".github" / "workflows" / "ci.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/ci.yml"])
    # Check for github.sha in a key: context
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped.startswith("key:") and "github.sha" in stripped:
            fails.append("cache key still uses github.sha (should use hashFiles)")
            break
    if "hashFiles" not in txt:
        fails.append("ci.yml does not use hashFiles() in cache key")
    if "package-lock.json" not in txt:
        fails.append("cache key must reference package-lock.json via hashFiles")
    if "actions/cache@v2" in txt:
        fails.append("ci.yml still uses deprecated actions/cache@v2 (must upgrade to v4)")
    if "actions/cache@v4" not in txt and "actions/cache@v3" not in txt:
        fails.append("ci.yml does not use actions/cache@v4 (or v3)")
    _finish(fails)
main()
