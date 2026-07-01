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
    data, err = _load_json(ws / "output" / "legacy_code_assessment.json")
    if err: _finish([err])
    # is_applicable must be false (V6: deprecated code must not be used)
    if data.get("is_applicable") is not False:
        fails.append("is_applicable == %r (expected false; the v3.1 code is DEPRECATED)" % data.get("is_applicable"))
    # reason must mention deprecated
    reason = str(data.get("reason") or "").lower()
    if "deprec" not in reason:
        fails.append("reason %r does not mention 'deprecated' (the v3.1 file is deprecated 2023-06-01)" % reason[:80])
    # recommendation must exist and not recommend the deprecated file
    rec = str(data.get("recommendation") or "").lower()
    if not rec:
        fails.append("recommendation field is empty")
    if re.search(r"v3\.1|legacy.*depr", rec):
        fails.append("recommendation should NOT recommend using the deprecated v3.1 code")
    _finish(fails)
main()
