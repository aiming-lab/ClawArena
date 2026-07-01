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
    txt = _read(ws / "policies" / "review_management_policy_q5.md")
    if txt is None:
        _finish(["file not found: policies/review_management_policy_q5.md"])
    low = txt.lower()
    # V9: §465.2(a) verbatim language
    if "write, create, or sell" not in low and "write, create" not in low:
        fails.append("must include verbatim §465.2(a) language: 'write, create, or sell a consumer review'")
    # V9: §465.7 verbatim language
    if "unfounded or groundless" not in low and "groundless legal threat" not in low:
        fails.append("must include verbatim §465.7 language: 'unfounded or groundless legal threat'")
    # Penalty amount: 51744, NOT 45000
    if "45,000" in txt or "45000" in txt:
        fails.append("penalty amount must be $51,744 (not $45,000 from DECOY summary)")
    if "51,744" not in txt and "51744" not in txt:
        fails.append("must state $51,744 per violation (2024 rate per 16 CFR Part 465)")
    # §465.5 insider reviews
    if "465.5" not in txt and "insider" not in low:
        fails.append("must address §465.5 insider reviews without disclosure")
    _finish(fails)
main()
