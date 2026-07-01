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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "root_cause_analysis.md")
    if txt is None:
        _finish(["file not found: output/root_cause_analysis.md"])
    # 真值层
    if "2024-11-03" not in txt:
        fails.append("RCA must contain incident_date '2024-11-03'")
    if "UTC-4" not in txt and "utc-4" not in txt.lower() and "UTC_OFFSET = -4" not in txt:
        fails.append("RCA must mention UTC-4 (the wrong timezone offset)")
    if "UTC-5" not in txt and "utc-5" not in txt.lower() and "UTC_OFFSET = -5" not in txt:
        fails.append("RCA must mention UTC-5 (the correct EST offset)")
    if "15c3-5(b)" not in txt:
        fails.append("RCA must cite 'Rule 15c3-5(b)' (not just '15c3-5')")
    if "15c6-1" not in txt:
        fails.append("RCA must reference Rule 15c6-1 (T+1 settlement)")
    # V1: must NOT use $440M (the decoy from bot summary / feishu message)
    if "440" in txt:
        low = txt.lower()
        if re.search(r"\$440|440,000,000|440m", low):
            fails.append("RCA must not use $440M (the decoy figure); use $460M+ for KCG reference")
    # V4: financial_impact section must exist
    if not re.search(r"financial.impact|affected.*order|order.*affected", txt.lower()):
        fails.append("RCA must include a financial_impact or affected orders reference")
    _finish(fails)
main()
