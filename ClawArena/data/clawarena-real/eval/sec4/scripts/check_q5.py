#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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
    txt = _read(ws / "dsar" / "response_req_042.md")
    if txt is None:
        _finish(["file not found: dsar/response_req_042.md"])
    low = txt.lower()
    # V9: verbatim Art.15(3) statutory text
    if "copy of the personal data undergoing processing" not in low:
        fails.append("response_req_042.md does not contain verbatim statutory text: 'copy of the personal data undergoing processing'")
    # V9: correct article reference format "Art. 15(3)"
    if not re.search(r"Art\.\s*15\(3\)", txt):
        fails.append("response_req_042.md does not reference Art. 15(3) in the required format 'Art. 15(3)'")
    # P3: four metadata fields in document
    for field in ("case_id", "request_date", "response_deadline", "status"):
        if field not in low:
            fails.append("response_req_042.md missing metadata field: %s" % field)
    # Must reference REQ-042
    if "req-042" not in low and "req_042" not in low:
        fails.append("response_req_042.md does not reference case REQ-042")
    _finish(fails)
main()
