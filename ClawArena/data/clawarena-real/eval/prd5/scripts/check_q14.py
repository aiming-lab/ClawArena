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
    data, err = _load_json(ws / "output" / "q14_twyman_check.json")
    if err: _finish([err])
    for key in ("confidence_level", "diagnostic_steps", "flagged_metric",
                "reported_lift", "suspicion_reason"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    fm = str(data.get("flagged_metric", "")).lower()
    if "checkout_conversion" not in fm and "checkout" not in fm:
        fails.append("flagged_metric %r should be checkout_conversion_rate" % data.get("flagged_metric"))
    sr = str(data.get("suspicion_reason", "")).lower()
    # Hardened: must explicitly name "Twyman" (not just "suspicious" or "unusual")
    if "twyman" not in sr:
        fails.append("suspicion_reason must explicitly reference \'Twyman\'s Law\' by name (got: %r)" % data.get("suspicion_reason", "")[:80])
    steps = data.get("diagnostic_steps")
    # Hardened: raised from >=3 to >=5 diagnostic steps
    if not isinstance(steps, list) or len(steps) < 5:
        fails.append("diagnostic_steps must be a list with >= 5 items (got %d); each step should cover a distinct diagnostic angle" % (len(steps) if isinstance(steps, list) else 0))
    else:
        # Each step must be a non-empty string of at least 10 characters
        for i, step in enumerate(steps):
            if not isinstance(step, str) or len(step.strip()) < 10:
                fails.append("diagnostic_steps[%d] is too short or not a string (each step must be a substantive description)" % i)
    cl = str(data.get("confidence_level", "")).lower()
    if cl not in ("high", "medium", "low"):
        fails.append("confidence_level == %r (must be high/medium/low)" % data.get("confidence_level"))
    # reported_lift must contain a two-digit number 40-49 AND "%" symbol
    rl = str(data.get("reported_lift", ""))
    if not re.search(r"4[0-9]", rl):
        fails.append("reported_lift %r does not reflect the +45%% anomalous lift" % rl[:30])
    if "%" not in rl:
        fails.append("reported_lift %r must include the %% symbol (e.g. '+45%%' or '45%%')" % rl[:30])
    _finish(fails)
main()
