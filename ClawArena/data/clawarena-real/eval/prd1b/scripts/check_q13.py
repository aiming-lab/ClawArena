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
    txt = _read(ws / "training" / "ad_compliance_card_q13.md")
    if txt is None:
        _finish(["file not found: training/ad_compliance_card_q13.md"])
    low = txt.lower()
    # All 6 prohibited terms must appear as table rows in the prohibited-term table
    for term, pattern in [
        ("may", r"\|\s*may\s*\|"),
        ("helps", r"\|\s*helps\s*\|"),
        ("promising", r"\|\s*promis"),
        ("preliminary", r"\|\s*preliminary\s*\|"),
        ("initial", r"\|\s*initial\s*\|"),
        ("pilot", r"\|\s*pilot\s*\|"),
    ]:
        if not re.search(pattern, low):
            fails.append("prohibited-term table must include a row for '%s' (all 6 FTC-prohibited qualifying terms must appear as individual table rows)" % term)
    # Disclosure rules: #ad or Ad: at beginning
    if "#ad" not in low and "ad:" not in low:
        fails.append("training card must mention '#ad' or 'Ad:' disclosure format")
    # Civil penalty $51,744 — exact figure required (not $45,000 DECOY)
    if "51,744" not in txt and "51744" not in txt:
        fails.append("training card must state $51,744 per-violation civil penalty (2024 rate per 16 CFR Part 465)")
    # Must be Markdown with H1/H2/H3 hierarchy
    h1 = re.findall(r"^# [^#]", txt, re.MULTILINE)
    h2 = re.findall(r"^## [^#]", txt, re.MULTILINE)
    h3 = re.findall(r"^### [^#]", txt, re.MULTILINE)
    if not h1:
        fails.append("training card must have an H1 heading (# ...) as document title (P3)")
    if not h2:
        fails.append("training card must have H2 headings (## ...) for major sections (P3)")
    if not h3:
        fails.append("training card must have H3 headings (### ...) for specific rules/subsections (P3)")
    # Must have some table (|)
    if "|" not in txt:
        fails.append("training card must include a Markdown table (prohibited terms replacement table)")
    # severity column with valid values
    if "severity" not in low:
        fails.append("prohibited-term table must include a 'Severity' column (high/medium/low per P4)")
    elif not any(v in low for v in ("high", "medium", "low")):
        fails.append("Severity column must contain values: high, medium, or low")
    _finish(fails)
main()
