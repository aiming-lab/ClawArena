#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
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
    sign = _read(ws / "signoff" / "final_signoff.txt")
    if sign is None:
        _finish(["file not found: signoff/final_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # Recompute: SHA256 of the four files concatenated in this exact order:
    #   1. src/requests/utils.py
    #   2. analysis/fix_commit.json
    #   3. analysis/cve_metadata.json
    #   4. analysis/impact_assessment.json
    files = [
        ws / "src" / "requests" / "utils.py",
        ws / "analysis" / "fix_commit.json",
        ws / "analysis" / "cve_metadata.json",
        ws / "analysis" / "impact_assessment.json",
    ]
    for f in files:
        if not Path(f).exists():
            _finish(["cannot verify hash: %s missing" % f])
    combined = b""
    for f in files:
        combined += Path(f).read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s "
                     "(hash must cover utils.py + fix_commit.json + cve_metadata.json + impact_assessment.json "
                     "in that order)" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
