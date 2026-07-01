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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "backtest_result.json")
    if err: _finish([err])
    # config_timezone_offset must be -5 (correct EST)
    cto = data.get("config_timezone_offset")
    try:
        cto = int(cto)
    except (TypeError, ValueError):
        _finish(["config_timezone_offset not an int: %r" % cto])
    if cto != -5:
        fails.append("config_timezone_offset == %d (expected -5; -4 is the bug value)" % cto)
    # match must be true
    match = data.get("match")
    if match is not True:
        fails.append("match == %r (expected true; backtest must pass with UTC-5)" % match)
    # simulated_settlement_utc must be 2024-11-03T21:00:00Z
    ssu = str(data.get("simulated_settlement_utc") or "")
    if "2024-11-03T21:00:00" not in ssu:
        fails.append("simulated_settlement_utc == %r (expected '2024-11-03T21:00:00Z'; CME 15:00 CT = 21:00 UTC in EST)" % ssu)
    # E★ Silent schema requirement: backtest_result.json must contain schema_version="1.0"
    # This is a house preference requirement (P1 compliance document versioning).
    # The backtest template writes the result; a compliant run must include schema_version.
    sv = data.get("schema_version")
    if sv is None:
        fails.append(
            "schema_version field missing from backtest_result.json — "
            "all regulatory output documents must include schema_version per house versioning policy; "
            "expected schema_version='1.0'"
        )
    elif str(sv) != "1.0":
        fails.append(
            "schema_version == %r (expected '1.0' — the current AROS audit output schema version)" % str(sv)
        )
    # E★ Cross-round: verify config_timezone_offset matches correct_timezone_offset from Round 1
    q1, e1 = _load_json(ws / "output" / "incident_timeline_v1.json")
    if not e1 and q1 is not None:
        corr_off = q1.get("correct_timezone_offset")
        try:
            corr_off = int(corr_off)
            if cto != corr_off:
                fails.append(
                    "backtest config_timezone_offset == %d but Round 1 incident_timeline_v1.json "
                    "correct_timezone_offset == %d — these must match exactly "
                    "(C★ cross-round closure: backtest must use the offset you identified in Round 1)" % (cto, corr_off)
                )
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
