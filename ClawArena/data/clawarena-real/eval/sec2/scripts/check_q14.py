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
    txt = _read(ws / "output" / "q14_sts_handling.md")
    if txt is None:
        _finish(["file not found: output/q14_sts_handling.md"])
    low = txt.lower()
    # 36 hours 时长（GetSessionToken/GetFederationToken 最大有效期）
    if "36 hour" not in low and "36-hour" not in low and "36小时" not in txt:
        fails.append("q14 must mention '36 hours' (max duration for GetSessionToken/GetFederationToken)")
    # DateLessThan 条件（IAM deny-all 策略关键词）
    if "datelessthan" not in low:
        fails.append("q14 must contain 'DateLessThan' (the IAM deny-all policy condition for STS)")
    # P5: ## Rationale 节（CTO Zhang 要求）
    if "## rationale" not in low:
        fails.append("q14 must have a '## Rationale' section (P5 — required by CTO Zhang in Feishu group)")
    _finish(fails)
main()
