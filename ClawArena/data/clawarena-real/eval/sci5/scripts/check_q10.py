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
    txt = _read(ws / "warn_notice_federal_final.md")
    if txt is None:
        _finish(["file not found: warn_notice_federal_final.md"])
    low = txt.lower()
    # 60 天通知期
    if not re.search(r"\b60\b", txt):
        fails.append("notice must contain '60' (days notice period)")
    # 受影响员工数 >= 50
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", txt) if 50 <= int(x) <= 500]
    if not nums:
        fails.append("notice must reference employee count >= 50")
    # plant closing 或 mass layoff
    if not (re.search(r"plant.clos", low) or re.search(r"mass.layoff", low)):
        fails.append("notice must reference 'plant closing' or 'mass layoff'")
    # V9: 29 U.S.C. § 2102
    if not re.search(r"29\s*u\.s\.c\.?\s*[§s]\s*2102", low):
        fails.append("notice must cite 29 U.S.C. § 2102 (verbatim statutory citation required)")
    # P2: document header block
    if not re.search(r"document:.*version:.*date:.*status:", low):
        fails.append("document must carry header: Document: [...] | Version: [...] | Date: [...] | Status: [...]")
    # P3: footer
    if not re.search(r"prepared by.*people operations", low):
        fails.append("document must carry footer: Prepared by: People Operations | Review required before distribution")
    _finish(fails)
main()
