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
    txt = _read(ws / "templates" / "disclosure_script_q9.md")
    if txt is None:
        _finish(["file not found: templates/disclosure_script_q9.md"])
    low = txt.lower()
    # Must have #ad or Ad: at beginning of post example
    if not re.search(r"(#ad|ad:).*beginning|beginning.*(#ad|ad:)|start.*#ad|#ad.*start", low):
        # More lenient: just check #ad or Ad: appears AND beginning somewhere
        if not re.search(r"#ad|ad:", low):
            fails.append("social media version must include '#ad' or 'Ad:' disclosure example")
        elif "beginning" not in low and "start" not in low:
            fails.append("must specify that '#ad' or 'Ad:' goes at the BEGINNING of the post")
    # Hashtag-only version must be labeled insufficient
    if not re.search(r"hashtag.{0,60}(insuffici|inadequat|not.?enough|not.?compliant)", low) and        not re.search(r"(insuffici|inadequat|not.?enough).{0,60}hashtag", low):
        fails.append("hashtag-only version must be explicitly labeled as insufficient per FTC guidance")
    # July 26 2023 effective date
    if "july 26, 2023" not in low and "july 26 2023" not in low and "2023-07-26" not in txt:
        fails.append("must reference July 26, 2023 (effective date of 16 CFR Part 255)")
    # V9: §255.5 material connection definition
    if "materially affect" not in low and "material connection" not in low:
        fails.append("must quote or reference §255.5 material connection language")
    _finish(fails)
main()
