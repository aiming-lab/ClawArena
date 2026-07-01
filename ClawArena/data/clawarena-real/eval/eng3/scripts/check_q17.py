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

SLA_FORMULA = "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "postmortem" / "FINAL.md")
    if txt is None:
        _finish(["file not found: postmortem/FINAL.md"])
    lines = txt.splitlines()
    # file >= 80 lines
    if len(lines) < 80:
        fails.append("FINAL.md has %d lines (expected >= 80)" % len(lines))
    # V9 verbatim anchors
    for anchor in ("get_cookie_key", "parent_key_generator",
                   "2024-06-20T17:47", "2024-06-20T19:27"):
        if anchor not in txt:
            fails.append("FINAL.md missing verbatim anchor: %r" % anchor)
    # V9 SLA formula
    if SLA_FORMULA not in txt:
        fails.append("FINAL.md missing verbatim SLA formula: %r" % SLA_FORMULA)
    # V10 supersede: CA-003 with strikethrough ~~
    if "~~" not in txt:
        fails.append("FINAL.md must use ~~ strikethrough to mark the superseded action item (CA-003)")
    # CA-003-revised (automated watchdog) must appear without strikethrough
    if "automated-restart-watchdog" not in txt and "automated restart watchdog" not in txt.lower():
        fails.append("FINAL.md must include CA-003-revised (automated-restart-watchdog) as active item")
    _finish(fails)
main()
