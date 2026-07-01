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
    data, err = _load_json(ws / "output" / "warranty_review.json")
    if err: _finish([err])
    # ucc_section_cited 必须引用 2-316
    cited = str(data.get("ucc_section_cited", "")).strip()
    if "2-316" not in cited:
        fails.append("ucc_section_cited == %r (must contain '2-316' — UCC § 2-316)" % cited)
    # issues 必须非空且至少一项涉及 merchantability
    issues = data.get("issues")
    if not isinstance(issues, list) or len(issues) == 0:
        fails.append("issues must be a non-empty list of compliance gaps")
    else:
        issues_text = " ".join(str(x).lower() for x in issues)
        if "merchant" not in issues_text:
            fails.append("issues must address the 'merchantability' explicit mention requirement from UCC § 2-316(2)")
    # compliant 必须是 bool
    if not isinstance(data.get("compliant"), bool):
        fails.append("compliant must be a boolean value")
    # conspicuous 必须是 bool
    if not isinstance(data.get("conspicuous"), bool):
        fails.append("conspicuous must be a boolean value")
    _finish(fails)
main()
