#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

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
    data, err = _load_json(ws / "output" / "q14_rescored.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("threshold_applied", "alerts", "changed_decisions", "consistency_note",
               "q6_threshold_used"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    t = float(data.get("threshold_applied", 0))
    if abs(t - 0.5) > 0.01:
        fails.append(f"threshold_applied={t} (must be 0.5 — Update-2 confirmed 0.5; do not use 0.3)")

    alerts = data.get("alerts") or []
    if len(alerts) != 3:
        fails.append(f"expected exactly 3 alerts, got {len(alerts)}")

    q14_lookup = {}
    for a in alerts:
        q14_lookup[str(a.get("alert_id", ""))] = str(a.get("decision", "")).upper()

    EXPECTED = {
        "ALRT-20260301-0001": "FRAUD",
        "ALRT-20260301-0005": "LEGITIMATE",
        "ALRT-20260301-0009": "FRAUD",
    }
    for alrt_id, exp_dec in EXPECTED.items():
        dec = q14_lookup.get(alrt_id)
        if dec is None:
            fails.append(f"alert {alrt_id} missing from Q14 alerts list")
        elif dec != exp_dec:
            fails.append(f"{alrt_id}: Q14 decision={dec!r} (expected {exp_dec!r} at threshold=0.5)")

    # C★ cross-round closure: Q14 decisions must match Q6 decisions exactly
    q6_data, q6_err = _load_json(ws / "output" / "q6_risk_scores.json")
    if q6_err:
        fails.append(f"cannot verify cross-round consistency — Q6 output missing: {q6_err}")
    else:
        q6_alerts = q6_data.get("alerts") or q6_data.get("scores") or []
        q6_lookup = {}
        for a in q6_alerts:
            q6_lookup[str(a.get("alert_id", ""))] = str(a.get("decision", "")).upper()
        for alrt_id in EXPECTED:
            q6_dec = q6_lookup.get(alrt_id)
            q14_dec = q14_lookup.get(alrt_id)
            if q6_dec and q14_dec and q6_dec != q14_dec:
                fails.append(
                    f"cross-round inconsistency: {alrt_id} Q6={q6_dec!r} vs Q14={q14_dec!r} — "
                    "both use threshold=0.5 so decisions must be identical"
                )

    # C★ q6_threshold_used must match actual Q6 threshold (cross-round field reference)
    q6_threshold_in_q14 = data.get("q6_threshold_used")
    if q6_threshold_in_q14 is None:
        fails.append("q6_threshold_used is missing — must state the threshold Q6 actually used")
    else:
        try:
            q6t = float(q6_threshold_in_q14)
        except (TypeError, ValueError):
            q6t = -1
        if abs(q6t - 0.5) > 0.01:
            fails.append(f"q6_threshold_used={q6_threshold_in_q14} (Q6 used 0.5; this field must reflect actual Q6 threshold)")
        # Also verify it matches Q6 output
        if not q6_err and q6_data:
            q6_alerts_list = q6_data.get("alerts") or []
            q6_ts = set()
            for a in q6_alerts_list:
                t_val = a.get("threshold_used")
                if t_val is not None:
                    q6_ts.add(float(t_val))
            top_t = q6_data.get("threshold_used")
            if top_t is not None:
                q6_ts.add(float(top_t))
            if q6_ts and abs(q6t - list(q6_ts)[0]) > 0.01:
                fails.append(
                    f"q6_threshold_used={q6t} does not match Q6 output threshold {list(q6_ts)[0]} "
                    f"— must read Q6 output, not assume"
                )

    cd = data.get("changed_decisions")
    if not isinstance(cd, list):
        fails.append(f"changed_decisions must be a list (may be empty), got {type(cd).__name__}")

    cn = str(data.get("consistency_note", "")).strip()
    if not cn:
        fails.append("consistency_note is missing or empty")
    else:
        if "0.5" not in cn:
            fails.append(f"consistency_note must reference threshold '0.5'; got: {cn[:100]!r}")
        if "Q6" not in cn and "q6" not in cn:
            fails.append(f"consistency_note must reference 'Q6' to explain cross-round consistency; got: {cn[:100]!r}")

    _finish(fails)
main()
