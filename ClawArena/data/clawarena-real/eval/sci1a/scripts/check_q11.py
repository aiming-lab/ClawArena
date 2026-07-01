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

def _read_tsv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading TSV " + p.name + ": " + str(e)

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        rows = []
        with p.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return None, "error reading CSV " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "cases" / "dfci" / "case_summary.md")
    if txt is None:
        _finish(["file not found: cases/dfci/case_summary.md"])
    # layer 3: truth (V2 update reversal: 58 -> 95)
    if "95" not in txt:
        fails.append("case_summary.md must contain '95' (the updated paper count after Update 1)")
    # Settlement figures (V4 numerical closure)
    if "15,000,000" not in txt and "15000000" not in txt:
        fails.append("case_summary.md must contain settlement amount '15,000,000'")
    if "2,630,000" not in txt and "2630000" not in txt:
        fails.append("case_summary.md must contain whistleblower amount '2,630,000'")
    # V10 supersede: 58 may appear only as historical reference, not current total
    # Simpler check: "total.*58" or "count.*58" as current claim
    import re
    current_58 = re.search(r"(total|flagged|current)\s+\S{0,15}\s*:?\s*\*?\*?58\b", txt, re.IGNORECASE)
    if current_58:
        fails.append("case_summary.md still uses 58 as the current paper count (must be 95 after Update 1)")
    _finish(fails)
main()
