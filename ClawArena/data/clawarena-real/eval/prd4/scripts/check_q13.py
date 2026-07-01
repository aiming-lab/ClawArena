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
    data, err = _load_json(ws / "output" / "incident_timeline.json")
    if err: _finish([err])
    # incident_id must be exactly "INC-2026-04-001"
    inc_id = str(data.get("incident_id") or "")
    if inc_id != "INC-2026-04-001":
        fails.append("incident_id == %r (expected exactly 'INC-2026-04-001')" % inc_id)
    # mttd_min must be exactly 27 (no rounding tolerance)
    mttd = data.get("mttd_min")
    try:
        mttd_i = int(mttd)
        if mttd_i != 27:
            fails.append("mttd_min == %d (expected exactly 27 — (08:12 - 07:45) = 27 min, no tolerance)" % mttd_i)
    except (TypeError, ValueError):
        fails.append("mttd_min not numeric: %r" % mttd)
    # mttr_min must be exactly 153 (no tolerance)
    mttr = data.get("mttr_min")
    try:
        mttr_i = int(mttr)
        if mttr_i != 153:
            fails.append("mttr_min == %d (expected exactly 153 — (10:45 - 08:12) = 153 min, no tolerance)" % mttr_i)
    except (TypeError, ValueError):
        fails.append("mttr_min not numeric: %r" % mttr)
    # sla_breach must be false (27 < 30)
    breach = data.get("sla_breach")
    if breach is not False:
        fails.append("sla_breach == %r (expected false — mttd=27 < L1 threshold=30)" % breach)
    # severity must be L1
    sev = data.get("severity")
    if str(sev) != "L1":
        fails.append("severity == %r (expected 'L1')" % sev)
    # sla_threshold_min must be present and equal 30
    threshold = data.get("sla_threshold_min")
    if threshold is None:
        fails.append("sla_threshold_min field missing (must be 30, the L1 SLA response threshold)")
    else:
        try:
            thr_i = int(threshold)
            if thr_i != 30:
                fails.append("sla_threshold_min == %d (expected 30 for L1 Enterprise SLA)" % thr_i)
        except (TypeError, ValueError):
            fails.append("sla_threshold_min not numeric: %r" % threshold)
    # issue_detected_at must be exactly "2026-04-04T07:45:00Z"
    detected = str(data.get("issue_detected_at") or "")
    if detected != "2026-04-04T07:45:00Z":
        fails.append("issue_detected_at == %r (expected exactly '2026-04-04T07:45:00Z')" % detected)
    # first_response_at must be exactly "2026-04-04T08:12:00Z"
    response = str(data.get("first_response_at") or "")
    if response != "2026-04-04T08:12:00Z":
        fails.append("first_response_at == %r (expected exactly '2026-04-04T08:12:00Z')" % response)
    _finish(fails)
main()
