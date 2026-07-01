#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    data, err = _load_json(ws / "output" / "q5_bot_errors.json")
    if err: _finish([err])
    if not isinstance(data, list):
        _finish(["q5 output must be a JSON array of error objects"])
    if len(data) < 4:
        fails.append("only %d errors identified (need >= 4: peeking FPR, CUPED window, SRM freq, exp003 conclusion)" % len(data))
    # Check for key errors using text search across all field values
    all_text = json.dumps(data).lower()
    # Error 1: peeking FPR — correct_value must mention 57%
    if "57" not in all_text:
        fails.append("missing peeking FPR error (BOT said 5%, correct_value must cite 57%)")
    # Error 2: CUPED window — must distinguish 14 days (BOT) vs 7 days (correct)
    if not (("14" in all_text or "fourteen" in all_text) and ("7" in all_text or "seven" in all_text)):
        fails.append("missing CUPED window error (BOT said 14 days, correct is 7 days)")
    # Error 3: SRM frequency — must mention both 3% (BOT) and 6% (correct)
    if "6" not in all_text or "3" not in all_text:
        fails.append("missing SRM frequency error (BOT said 3%, correct is ~6%)")
    # Error 4: exp003 conclusion status — must mention the invalidation of the BOT conclusion
    if "exp003" not in all_text and "invalidat" not in all_text:
        fails.append("missing exp003 conclusion error (BOT claimed VALID/significant; correct: invalidated by bot traffic)")
    # Each element must have all three required fields: field, bot_value, correct_value
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            fails.append("error item %d is not an object" % i)
            continue
        missing_keys = [k for k in ("field", "bot_value", "correct_value") if k not in item]
        if missing_keys:
            fails.append("error item %d missing required keys: %s (must have field, bot_value, correct_value)" % (i, missing_keys))
    _finish(fails)
main()
