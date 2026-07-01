#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_q4.py — restore-keys: exactly 2 entries (build- then bare); no stale -node- restore-keys
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
    txt = _read(ws / ".github" / "workflows" / "ci.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/ci.yml"])
    if "restore-keys" not in txt:
        fails.append("ci.yml has no restore-keys configuration")
        _finish(fails)
    # Must have runner.os }}-build- as first restore key (matching key prefix from Q3)
    if "runner.os }}-build-" not in txt:
        fails.append("restore-keys must include '${{ runner.os }}-build-' (matching the hashFiles key prefix)")
    # Count lines containing runner.os in a restore-keys context
    rk_lines = [
        l.strip() for l in txt.splitlines()
        if "runner.os" in l and l.strip().startswith("${{")
        and ("build-" in l or l.strip().rstrip("\n").strip().endswith("-"))
    ]
    if len(rk_lines) < 2:
        fails.append("restore-keys must have at least 2 entries: runner.os-build- then runner.os-")
    # A: stale -node- or -pip- style restore-keys from original file must NOT remain
    # Parse restore-keys blocks and detect old prefix patterns
    in_rk = False
    for line in txt.splitlines():
        stripped = line.strip()
        if re.match(r"restore-keys\s*:", stripped):
            in_rk = True
            continue
        if in_rk:
            if stripped.startswith("${{") or stripped.startswith("-"):
                # Detect old -node- prefix: e.g. "${{ runner.os }}-node-"
                if re.search(r"runner\.os\s*\}\}-node-", stripped):
                    fails.append(
                        "ci.yml still has a stale '-node-' restore-key prefix in restore-keys block: %r — "
                        "it must be replaced with '-build-' to match the Q3 key" % stripped
                    )
            elif stripped and not stripped.startswith("#"):
                in_rk = False
    _finish(fails)
main()
