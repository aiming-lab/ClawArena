#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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
    data, err = _load_json(ws / "audit" / "final_report_signoff.json")
    if err: _finish([err])
    signoff = str(data.get("signoff", ""))
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", signoff)
    if not m:
        _finish(["signoff field must match VERIFIED:[a-f0-9]{64} (got %r)" % signoff[:80]])
    # Recompute SHA-256 of compliance_summary.json
    target = ws / "audit" / "compliance_summary.json"
    if not target.exists():
        _finish(["cannot verify: audit/compliance_summary.json not found"])
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if m.group(1) != actual:
        fails.append("sha256 mismatch: signoff has %s... but recomputed is %s..." % (
            m.group(1)[:12], actual[:12]))
    # target_file field
    tf = data.get("target_file", "")
    if "compliance_summary" not in str(tf):
        fails.append("target_file %r should reference compliance_summary.json" % tf)
    _finish(fails)
main()
