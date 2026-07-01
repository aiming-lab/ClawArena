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
    if not (ws / ".gitlab-ci.yml.bak").exists():
        fails.append("backup not found: .gitlab-ci.yml.bak")
    txt = _read(ws / ".gitlab-ci.yml")
    if txt is None:
        _finish(["file not found: .gitlab-ci.yml"])
    # Must NOT have invalid '30d' format
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped.startswith("expire_in") and re.search(r"\b30d\b", stripped):
            fails.append(".gitlab-ci.yml still has invalid expire_in: 30d (must be '30 days')")
            break
    # Must have a valid format (check for known valid patterns)
    valid_lines = [l for l in txt.splitlines() if "expire_in" in l]
    valid_found = False
    for vl in valid_lines:
        if re.search(r"30\s+days|never|\d+\s+(seconds?|mins?|hours?|days?|weeks?|months?|mos)|\d+h\d+min", vl, re.IGNORECASE):
            valid_found = True
            break
    if not valid_found:
        fails.append(".gitlab-ci.yml expire_in must be a valid format (e.g., '30 days', 'never')")
    _finish(fails)
main()
