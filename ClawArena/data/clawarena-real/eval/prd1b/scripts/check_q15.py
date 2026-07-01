#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    sign_path = ws / "final" / "signoff_final_20260309.txt"
    if not sign_path.exists():
        # Try any signoff_final*.txt
        candidates = list((ws / "final").glob("signoff_final*.txt")) if (ws / "final").exists() else []
        if candidates:
            sign_path = candidates[0]
        else:
            _finish(["file not found: final/signoff_final_20260309.txt"])
    sign = sign_path.read_text(encoding="utf-8").strip()
    # Pattern: VERIFIED:<64hex>:<filename>
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64}):(.+)", sign)
    if not m:
        _finish(["signoff line must match VERIFIED:<64hex>:<filename> (got %r)" % sign[:80]])
    claimed_hex = m.group(1)
    claimed_fname = m.group(2).strip()
    # Verify the hash
    pr_path = ws / "final" / claimed_fname
    if not pr_path.exists():
        pr_path2 = ws / "final" / "press_release_final_20260309.md"
        if pr_path2.exists():
            pr_path = pr_path2
        else:
            _finish(["cannot verify hash: final/%s not found" % claimed_fname])
    digest = hashlib.sha256(pr_path.read_bytes()).hexdigest()
    if claimed_hex != digest:
        fails.append("SHA-256 mismatch: signoff %s... != recomputed %s..." % (claimed_hex[:12], digest[:12]))
    _finish(fails)
main()
