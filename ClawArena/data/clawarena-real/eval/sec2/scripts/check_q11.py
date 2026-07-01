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
    data, err = _load_json(ws / "output" / "q11_fact_check.json")
    if err: _finish([err])
    # openai_key_status 必须是 not_revoked_by_huangmin
    oks = data.get("openai_key_status")
    if oks != "not_revoked_by_huangmin":
        fails.append("openai_key_status == %r (expected 'not_revoked_by_huangmin' — "
                     "Huang Min's claim was disproved by GitGuardian webhook v2)" % oks)
    # evidence_source 含 gitguardian_webhook_v2.json
    ev = [str(s).lower() for s in (data.get("evidence_source") or [])]
    if not any("gitguardian_webhook_v2" in e for e in ev):
        fails.append("evidence_source must include 'gitguardian_webhook_v2.json' as counter-evidence")
    _finish(fails)
main()
