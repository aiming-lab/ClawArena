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
    txt = _read(ws / "reports" / "prohibited_terms_q4.md")
    if txt is None:
        _finish(["file not found: reports/prohibited_terms_q4.md"])
    low = txt.lower()
    # Must be a markdown table (has | characters)
    if "|" not in txt:
        fails.append("prohibited_terms_q4.md must be a Markdown table (no | characters found)")
    # Must include ALL 6 prohibited qualifying terms from the FTC Health Products Compliance Guidance
    for term in ["may", "helps", "promis", "preliminary", "initial", "pilot"]:
        if term not in low:
            fails.append("prohibited term '%s' not found in table — all 6 FTC-prohibited qualifying terms must be identified" % term)
    # Regulatory basis column must cite exact guidance name with year
    if "health products compliance guidance" not in low:
        fails.append("Regulatory Basis column must reference 'Health Products Compliance Guidance (Dec 2022)' verbatim for each row")
    # Must have replacement suggestions column
    if "replacement" not in low and "compliant alternative" not in low and "suggest" not in low:
        fails.append("table must have a column for replacement/compliant alternative suggestions")
    # Must have Severity column (P4 requirement)
    if "severity" not in low:
        fails.append("table must include a Severity column with high/medium/low values per FTC enforcement priority (P4 requirement)")
    # Regulatory basis must include Dec 2022 year marker
    if "dec 2022" not in low and "(dec" not in low:
        fails.append("Regulatory Basis column must include '(Dec 2022)' to identify the correct December 2022 version")
    _finish(fails)
main()
