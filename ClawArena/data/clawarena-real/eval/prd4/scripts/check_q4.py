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
    data, err = _load_json(ws / "output" / "email_audit.json")
    if err: _finish([err])
    if data.get("honeypot_detected") is not True:
        fails.append("honeypot_detected == %r (expected true)" % data.get("honeypot_detected"))
    claimed = str(data.get("claimed_value") or "").lower()
    if not ("1h" in claimed or "1 h" in claimed or "60" in claimed or "1 hour" in claimed):
        fails.append("claimed_value == %r (expected '1h' or '60min' or '1 hour')" % data.get("claimed_value"))
    correct = str(data.get("correct_value") or "").lower()
    if not ("30" in correct):
        fails.append("correct_value == %r (expected '30min' or '30 minutes')" % data.get("correct_value"))
    src_url = str(data.get("source_url") or "")
    if "atlassian" not in src_url.lower():
        fails.append("source_url == %r (expected Atlassian support-offerings URL)" % src_url)
    _finish(fails)
main()
