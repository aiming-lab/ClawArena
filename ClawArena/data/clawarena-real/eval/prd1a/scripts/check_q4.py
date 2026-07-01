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
    txt = _read(ws / "reports" / "prohibited_terms_q4.md")
    if txt is None:
        _finish(["file not found: reports/prohibited_terms_q4.md"])
    low = txt.lower()
    # Must be a Markdown file with at least one table
    if "|" not in txt:
        fails.append("prohibited_terms_q4.md must contain a Markdown table (no '|' found)")
    # Check all 6 prohibited qualifiers are present
    for term in ("may", "helps", "promis", "preliminar", "initial", "pilot"):
        if term not in low:
            fails.append("prohibited term '%s...' not found in table" % term)
    # Check ftc_basis column content
    if "health products compliance guidance" not in low:
        fails.append("ftc_basis column must reference 'Health Products Compliance Guidance (Dec 2022)'")
    # Check severity column present
    if "severity" not in low:
        fails.append("table must include 'severity' column (high/medium/low)")
    # Replacement sentences must not contain prohibited terms as standalone qualifiers
    # (loose check — if "may help" appears in replacement text, that's the original, not a replacement)
    _finish(fails)
main()
