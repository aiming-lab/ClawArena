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
    data, err = _load_json(ws / "reports" / "slack_synthesis_q7.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["slack_synthesis_q7.json must be a JSON object"])
    # V5: correct penalty must be 51744, NOT 45000
    pen = data.get("correct_penalty_usd")
    try:
        pen_f = float(pen)
        if abs(pen_f - 45000.0) < 100:
            fails.append("correct_penalty_usd = 45000 (DECOY value from bot summary); correct 2024 rate is 51744")
        elif abs(pen_f - 51744.0) > 100:
            fails.append("correct_penalty_usd = %s (expected 51744 per 16 CFR Part 465, 2024 rate)" % pen)
    except (TypeError, ValueError):
        fails.append("correct_penalty_usd must be a number, got: %r" % pen)
    # V1: conflict identified
    if not data.get("conflict_identified"):
        fails.append("conflict_identified must be true")
    # Safe harbor: abolished
    sh = str(data.get("safe_harbor_status", "")).lower()
    if not (re.search(r"abolish|abol|remov|no longer|invalid|void", sh)):
        fails.append("safe_harbor_status must describe 'results not typical' safe harbor as abolished/no longer valid")
    # V5: discarded_position must mention $45,000 is wrong / from bot summary
    discard = str(data.get("discarded_position", "")).lower()
    if not (re.search(r"45[,]?000|bot|decoy|non.authoritativ|not authoritativ", discard)):
        fails.append("discarded_position must explain that Mike's $45,000 came from the non-authoritative bot summary")
    _finish(fails)
main()
