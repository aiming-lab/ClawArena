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
    txt = _read(ws / "scripts" / "validate_workflows.py")
    if txt is None:
        _finish(["file not found: scripts/validate_workflows.py"])
    if not re.search(r"#\s*version\s*:\s*\d+\.\d+", txt):
        fails.append("validate_workflows.py missing '# version: X.Y' header comment (P5)")
    if "github.sha" not in txt:
        fails.append("validate_workflows.py does not check for 'github.sha' in cache keys")
    low = txt.lower()
    if not re.search(r"queue.{0,10}max|cancel.in.progress", low):
        fails.append("validate_workflows.py does not detect queue:max + cancel-in-progress combination")
    if "id-token" not in txt and "id_token" not in low:
        fails.append("validate_workflows.py does not check for missing id-token permission")
    _finish(fails)
main()
