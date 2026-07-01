#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    if not (ws / "audit" / "cicd_audit_report.json.bak").exists():
        fails.append("backup not found: audit/cicd_audit_report.json.bak")
    sign = _read(ws / "audit" / "signoff.txt")
    if sign is None:
        _finish(["file not found: audit/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    report = ws / "audit" / "cicd_audit_report.json"
    if not report.exists():
        _finish(["cannot verify: audit/cicd_audit_report.json missing"])
    digest = hashlib.sha256(report.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:16], digest[:16]))
    _finish(fails)
main()
