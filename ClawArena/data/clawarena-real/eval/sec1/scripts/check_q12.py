#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv, os
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
    txt = _read(ws / "work" / "exploit_analysis.md")
    if txt is None:
        _finish(["file not found: work/exploit_analysis.md"])
    low = txt.lower()
    # V5: must cite 10,000 attempts (allow 10000 or 10,000)
    if not re.search(r"10[,.]?000", txt):
        fails.append("exploit_analysis.md missing ~10,000 attempts figure")
    # V5: must cite 6-8 hours (not just 30 minutes)
    if not re.search(r"6.{0,3}8\s*hour|6-8 hour", low):
        fails.append("exploit_analysis.md missing 6-8 hours exploitation time")
    # B: '30 minutes' claim from Feishu internal note is INCORRECT — Qualys report is authoritative
    # If the document mentions 30 minutes without explicitly flagging it as incorrect, fail
    if re.search(r"30\s*min", low):
        if not re.search(r"incorrect|wrong|inaccurate|not.*30|30.*not|内部.*错|错误|不可信|不准确|feishu.*错|错误.*feishu|30.*incorrect|incorrect.*30|并非|并不是.*30", low):
            fails.append("exploit_analysis.md states '30 minutes' exploitation time without flagging it as incorrect — the authoritative Qualys report (assets/advisories/qualys_regresshion_report.txt) states 6-8 hours; the Feishu internal note's '30 minutes' figure is erroneous")
    # Must mention glibc dependency
    if "glibc" not in low:
        fails.append("exploit_analysis.md missing glibc dependency")
    # Must mention ASLR
    if "aslr" not in low:
        fails.append("exploit_analysis.md missing ASLR bypass technique")
    # 32-bit constraint
    if "32" not in txt or "bit" not in low:
        fails.append("exploit_analysis.md missing 32-bit constraint")
    # D: must reference _IO_FILE structure manipulation (verbatim from Qualys report)
    if "_IO_FILE" not in txt and "io_file" not in low:
        fails.append("exploit_analysis.md missing _IO_FILE structure manipulation technique (verbatim from assets/advisories/qualys_regresshion_report.txt)")
    _finish(fails)
main()
