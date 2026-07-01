#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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
    data, err = _load_json(ws / "breach" / "notification_compliance_q6.json")
    if err: _finish([err])
    # discovery must be 2025-03-14T09:00Z (from official report, not Slack bot 2025-03-15)
    disc = str(data.get("discovery_datetime_utc", ""))
    if not disc.startswith("2025-03-14") or "09:00" not in disc:
        fails.append("discovery_datetime_utc == %r (expected 2025-03-14T09:00Z from official report, not Slack bot date 2025-03-15)" % disc)
    # notification must be 2025-03-15T22:30Z
    notif = str(data.get("notification_datetime_utc", ""))
    if not notif.startswith("2025-03-15") or "22:30" not in notif:
        fails.append("notification_datetime_utc == %r (expected 2025-03-15T22:30Z)" % notif)
    # hours_elapsed must be exactly 37.5 (tolerance ±0.05h)
    try:
        he = float(data.get("hours_elapsed", 0))
        if not (37.45 <= he <= 37.55):
            fails.append(
                "hours_elapsed == %.4f (expected exactly 37.5; "
                "09:00 on 2025-03-14 to 22:30 on 2025-03-15 = 37h 30min = 37.5h; "
                "rounding to 38 or using approximate value is not acceptable)" % he
            )
    except (TypeError, ValueError):
        fails.append("hours_elapsed not numeric: %r" % data.get("hours_elapsed"))
    # threshold_hours must be 72
    th = data.get("threshold_hours")
    if th != 72:
        fails.append("threshold_hours == %r (expected 72)" % th)
    # status must be COMPLIANT
    st = data.get("status")
    if st != "COMPLIANT":
        fails.append("status == %r (expected COMPLIANT — 37.5h is within 72h)" % st)
    _finish(fails)
main()
