#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    # Check file exists (may use the date-named convention)
    pr_path = ws / "final" / "press_release_final_20260309.md"
    if not pr_path.exists():
        # Try to find any press_release_final_*.md in final/
        candidates = list((ws / "final").glob("press_release_final_*.md")) if (ws / "final").exists() else []
        if candidates:
            pr_path = candidates[0]
        else:
            _finish(["file not found: final/press_release_final_20260309.md (or any press_release_final_*.md)"])
    txt = pr_path.read_text(encoding="utf-8")
    low = txt.lower()
    # No prohibited qualifiers
    # Check no prohibited qualifiers used as health claim hedges (not as educational listing)
    for term in ["may help", "helps support", "promising results", "preliminary research",
                 "initial research", "pilot studies", "pilot research"]:
        if term in low:
            fails.append("final press release still contains prohibited qualifier: '%s'" % term)
    # Also check standalone 'preliminary' not in a health claim context
    if re.search(r"preliminary.{0,20}(research|data|evidence|study|trial)", low):
        fails.append("final press release contains 'preliminary' in a health claim context")
    # compliance_reviewed_by section
    if "compliance_reviewed_by" not in low and "compliance reviewed by" not in low:
        fails.append("press release must include 'compliance_reviewed_by' section")
    # review_date in ISO 8601 format
    if "2026-03-09" not in txt and "2026-03-09" not in txt:
        if not re.search(r"2026-0[1-9]-\d{2}", txt):
            fails.append("press release must include review_date in ISO 8601 format (2026-03-09)")
    # ftc_basis_summary
    if "ftc_basis_summary" not in low and "ftc basis" not in low and "governing regulation" not in low:
        fails.append("press release must include an 'ftc_basis_summary' paragraph or section")
    # Must have heading structure
    if len(re.findall(r"^#{1,3} ", txt, re.MULTILINE)) < 2:
        fails.append("press release must have at least 2 Markdown headings")
    _finish(fails)
main()
