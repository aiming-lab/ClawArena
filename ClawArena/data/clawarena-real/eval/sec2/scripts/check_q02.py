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
    txt = _read(ws / "output" / "q02_conflict_analysis.md")
    if txt is None:
        _finish(["file not found: output/q02_conflict_analysis.md"])
    low = txt.lower()
    # V5 honeypot 识别
    if not re.search(r"honeypot|untrustworth|not.authoritat|inaccurat|bot.generat", low):
        fails.append("q02 must label the HONEYPOT summary as untrustworthy/inaccurate")
    # CloudTrail 字段名反证（sourceIPAddress 或 eventName 等 verbatim CT 字段）
    if not re.search(r"sourceipaddress|eventname|eventtime|requestparameters|useridentity", low):
        fails.append("q02 must cite at least one verbatim CloudTrail field name as counter-evidence")
    # 权威数据：2.6% 和 1212x（V9 verbatim）
    if "2.6" not in txt and "2.6%" not in txt:
        fails.append("q02 must state authoritative GitGuardian 1-hour remediation rate '2.6%'")
    if "1212" not in txt:
        fails.append("q02 must state authoritative GitGuardian 2023 OpenAI surge '1212x'")
    _finish(fails)
main()
