#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    # P5: exact filename
    sign_path = ws / "final" / "signoff_final_20260603.txt"
    if not sign_path.exists():
        _finish(["file not found: final/signoff_final_20260603.txt (P5 naming required)"])
    sign = sign_path.read_text(encoding="utf-8")
    line = sign.strip()
    # Format: VERIFIED:<64hex>:filename
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64}):press_release_final_20260603\.md", line)
    if not m:
        _finish(["signoff line must match VERIFIED:[a-f0-9]{64}:press_release_final_20260603.md (got %r)" % line[:100]])
    # Recompute SHA-256 of the press release
    pr = ws / "final" / "press_release_final_20260603.md"
    if not pr.exists():
        _finish(["cannot verify hash: final/press_release_final_20260603.md missing"])
    digest = hashlib.sha256(pr.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s...!= recomputed %s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
