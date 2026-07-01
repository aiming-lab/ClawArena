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
    txt = _read(ws / "output" / "mifir_field28_correction.md")
    if txt is None:
        _finish(["file not found: output/mifir_field28_correction.md"])
    low = txt.lower()
    # Must contain 'Field 28' (verbatim field reference)
    if "field 28" not in low and "field28" not in low:
        fails.append("report does not contain 'Field 28' reference")
    # Must mention UTC explicitly
    if "utc" not in low:
        fails.append("report does not mention UTC")
    # Must cite Market Watch 59 (FCA Market Watch 59)
    if "market watch 59" not in low and "market watch59" not in low:
        fails.append("report does not cite 'Market Watch 59' (FCA guidance on Field 28)")
    # Must mention DST, BST, or summer/standard time
    if not re.search(r"dst|daylight|summer time|standard time|bst|clocks", low):
        fails.append("report does not mention DST/BST/summer-time/standard-time transition")
    # Must cite Article 26 of MiFIR (the specific regulatory article governing Field 28)
    if "article 26" not in low:
        fails.append("report does not cite 'Article 26' of MiFIR (the transaction reporting obligation "
                     "that mandates Field 28 UTC format — verbatim citation required)")
    # Must cite RTS 22 (the technical standard specifying Field 28 format)
    if "rts 22" not in low and "rts22" not in low:
        fails.append("report does not cite 'RTS 22' (the technical standard defining the "
                     "ISO 8601 UTC format requirement for Field 28)")
    # Must include a concrete remediation action (not just description of the error)
    if not re.search(r"remediat|action|fix|correct|replac|implement", low):
        fails.append("report does not include a concrete remediation action")
    _finish(fails)
main()
