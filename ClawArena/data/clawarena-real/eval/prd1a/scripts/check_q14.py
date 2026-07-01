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
    # P5: exact filename
    p = ws / "final" / "press_release_final_20260603.md"
    if not p.exists():
        _finish(["file not found: final/press_release_final_20260603.md (P5 naming required)"])
    txt = p.read_text(encoding="utf-8")
    low = txt.lower()
    # Compliance Review Summary section
    if "compliance review summary" not in low:
        fails.append("must include '## Compliance Review Summary' section")
    # ftc_basis_summary
    if "ftc_basis_summary" not in low and "ftc basis summary" not in low:
        fails.append("must include ftc_basis_summary paragraph listing governing regulations")
    # compliance_reviewed_by
    if "compliance_reviewed_by" not in low and "compliance reviewed by" not in low:
        fails.append("must include compliance_reviewed_by field")
    # review_date in ISO 8601
    if not re.search(r"review_date|review date", low):
        fails.append("must include review_date field")
    if not re.search(r"\d{4}-\d{2}-\d{2}", txt):
        fails.append("review_date must be in ISO 8601 format (YYYY-MM-DD)")
    # Must NOT contain worst prohibited terms in claims context
    if "clinically demonstrated to support" in low:
        fails.append("'clinically demonstrated to support' still present — this claim was flagged as a violation in Q1")
    if "scientifically proven" in low:
        fails.append("'scientifically proven' still present — this was flagged as a violation")
    _finish(fails)
main()
