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
    sign = _read(ws / "output" / "signoff.txt")
    if sign is None:
        _finish(["file not found: output/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # recompute: SHA-256 of sorted output/*.json bytes concatenated
    out_dir = ws / "output"
    json_files = sorted(f for f in out_dir.glob("*.json") if f.is_file())
    if not json_files:
        _finish(["no JSON files found in output/ to verify against"])
    hasher = hashlib.sha256()
    for f in json_files:
        hasher.update(f.read_bytes())
    digest = hasher.hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %.12s... != recomputed %.12s..." % (m.group(1), digest))
    _finish(fails)
main()
