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
    txt = _read(ws / ".github" / "workflows" / "nightly.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/nightly.yml"])
    has_queue_max = bool(re.search(r"queue\s*:\s*max", txt))
    has_cancel = bool(re.search(r"cancel-in-progress\s*:\s*true", txt))
    if has_queue_max and has_cancel:
        fails.append("nightly.yml still has forbidden combination: queue:max + cancel-in-progress:true")
    md = _read(ws / "audit" / "concurrency_fix.md")
    if md is None:
        fails.append("file not found: audit/concurrency_fix.md")
    else:
        low = md.lower()
        if not re.search(r"queue.{0,10}max|cancel.in.progress", low):
            fails.append("concurrency_fix.md does not explain the forbidden combination")
    _finish(fails)
main()
