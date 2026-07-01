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
    txt = _read(ws / "training" / "ad_compliance_card_q13.md")
    if txt is None:
        _finish(["file not found: training/ad_compliance_card_q13.md"])
    low = txt.lower()
    # All 6 prohibited qualifiers must be listed
    for term in ("may", "helps", "promis", "preliminar", "initial", "pilot"):
        if term not in low:
            fails.append("prohibited qualifier '%s...' not found in training card" % term)
    # #ad disclosure example
    if "#ad" not in txt and "ad:" not in low:
        fails.append("must include '#ad' or 'Ad:' disclosure example")
    # July 26, 2023 effective date
    if "july 26, 2023" not in low and "july 26 2023" not in low and "2023-07-26" not in txt:
        fails.append("must reference July 26, 2023 (effective date of 16 CFR Part 255)")
    # severity column
    if "severity" not in low:
        fails.append("any prohibited terms table must include 'severity' column (P4)")
    # H1 heading present (P3)
    if not re.search(r"^#\s+", txt, re.MULTILINE):
        fails.append("must have H1 heading (P3 heading structure)")
    _finish(fails)
main()
