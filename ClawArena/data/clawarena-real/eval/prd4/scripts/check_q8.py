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
    data, err = _load_json(ws / "output" / "conflict_resolution.json")
    if err: _finish([err])
    adopted = str(data.get("adopted_value") or "").lower()
    if "90" not in adopted:
        fails.append("adopted_value == %r (expected '90min' or '90' — v2 is current after Update-1)" % data.get("adopted_value"))
    src = str(data.get("source_authority") or "").lower()
    if "v2" not in src and "sla_matrix_v2" not in src:
        fails.append("source_authority == %r (expected reference to sla_matrix_v2)" % data.get("source_authority"))
    # alice_claimed should reference 2h/120min (original)
    alice = str(data.get("alice_claimed") or "").lower()
    if not ("120" in alice or "2h" in alice or "2 h" in alice or "2 hour" in alice):
        fails.append("alice_claimed == %r (expected reference to 2h/120min original value)" % data.get("alice_claimed"))
    _finish(fails)
main()
