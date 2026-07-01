#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
from pathlib import Path
from datetime import date, timedelta

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
    txt = _read(ws / "warn_notice_cal_final.md")
    if txt is None:
        _finish(["file not found: warn_notice_cal_final.md"])
    low = txt.lower()
    # V9: verbatim full name — "california employment development department"
    if "california employment development department" not in low:
        fails.append("document must contain 'California Employment Development Department' (exact full name — not just 'EDD')")
    # 60 days
    if not re.search(r"\b60\b", txt):
        fails.append("notice must contain '60' (days notice period)")
    # trigger: 50
    if not re.search(r"\b50\b", txt):
        fails.append("notice must reference '50' (Cal-WARN trigger threshold)")
    # P2: document header
    if not re.search(r"document:.*version:.*date:.*status:", low):
        fails.append("document must carry header: Document: [...] | Version: [...] | Date: [...] | Status: [...]")
    # P3: footer
    if not re.search(r"prepared by.*people operations", low):
        fails.append("document must carry footer: Prepared by: People Operations | Review required before distribution")
    _finish(fails)
main()
