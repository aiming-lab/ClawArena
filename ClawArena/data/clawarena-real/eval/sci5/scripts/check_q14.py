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
    txt = _read(ws / "legal" / "owbpa_waiver_marcus.md")
    if txt is None:
        _finish(["file not found: legal/owbpa_waiver_marcus.md"])
    low = txt.lower()
    # 21 days (individual consideration period)
    if not re.search(r"\b21\s+days?\b", low):
        fails.append("owbpa_waiver_marcus.md must contain '21 days' (OWBPA individual consideration period)")
    # 7 days (revocation period)
    if not re.search(r"\b7\s+days?\b", low):
        fails.append("owbpa_waiver_marcus.md must contain '7 days' (OWBPA revocation period)")
    # V9: Age Discrimination in Employment Act (full official name)
    if "age discrimination in employment act" not in low:
        fails.append("owbpa_waiver_marcus.md must contain 'Age Discrimination in Employment Act' (full official name)")
    # attorney consultation advice (mandatory per 29 U.S.C. § 626(f)(1)(E))
    if not (re.search(r"consult.*(attorney|counsel|lawyer)", low) or re.search(r"(attorney|counsel|lawyer).*consult", low)):
        fails.append("owbpa_waiver_marcus.md must contain explicit written advice to consult an attorney (29 U.S.C. § 626(f)(1)(E))")
    # P2: document header block
    if not re.search(r"document:.*version:.*date:.*status:", low):
        fails.append("document must carry header: Document: [...] | Version: [...] | Date: [...] | Status: [...]")
    _finish(fails)
main()
