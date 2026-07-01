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
    txt = _read(ws / "output" / "timezone_bug_report.md")
    if txt is None:
        _finish(["file not found: output/timezone_bug_report.md"])
    low = txt.lower()
    # Must mention error value UTC-4 and correct value UTC-5
    if "utc-4" not in txt and "utc -4" not in txt and "-4" not in txt:
        fails.append("report does not mention UTC-4 (the error value)")
    if "utc-5" not in txt and "utc -5" not in txt and "-5" not in txt:
        fails.append("report does not mention UTC-5 (the correct EST value)")
    # Must reference a line number (digit follows 'line')
    if not re.search(r"line\s+\d+", low):
        fails.append("report does not reference a specific line number (e.g. 'line 42')")
    # Must not RECOMMEND the deprecated v3 file (mentioning it as deprecated/not-to-use is fine)
    # Fail if the report suggests using the v3 file without a negation in context
    if re.search(r"(use|apply|reference|copy|recommend)[^\n]{0,60}(aros_v3|v3\.1|legacy.*router)", low):
        fails.append("report appears to recommend using the deprecated v3 file (V6 red herring)")
    _finish(fails)
main()
