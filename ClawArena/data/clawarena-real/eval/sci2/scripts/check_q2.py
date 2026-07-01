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
    data, err = _load_json(ws / "rca_outputs" / "honeypot_flags.json")
    if err: _finish([err])
    fe = data.get("flagged_errors")
    if not isinstance(fe, list) or len(fe) == 0:
        _finish(["flagged_errors must be a non-empty list"])
    # 必须标记两个已知错误
    all_txt = json.dumps(fe, ensure_ascii=False).lower()
    # Error 1: ivenix_injuries bot=5, real=2
    if not (("injur" in all_txt or "ivenix" in all_txt) and
            ("5" in all_txt or "five" in all_txt) and
            ("2" in all_txt or "two" in all_txt)):
        fails.append("flagged_errors must include ivenix injuries error (bot:5 vs real:2)")
    # Error 2: nimbus support cutoff bot=2024-08-31, real=2024-06-20
    if not (("cutoff" in all_txt or "support" in all_txt or "2024-08-31" in all_txt) and
            ("2024-06-20" in all_txt or "june" in all_txt or "06-20" in all_txt)):
        fails.append("flagged_errors must include nimbus support_cutoff error (bot:2024-08-31 vs real:2024-06-20)")
    _finish(fails)
main()
