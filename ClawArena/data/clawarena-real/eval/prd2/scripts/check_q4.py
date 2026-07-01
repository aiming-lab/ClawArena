#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "platforms" / "reddit" / "enforcement_tiers.json")
    if err: _finish([err])

    tiers = data.get("tiers") or []
    if len(tiers) < 3:
        _finish(["enforcement_tiers.json: expected at least 3 tiers, got %d" % len(tiers)])

    # tiers[0].action = 'warning'
    t0_action = str(tiers[0].get("action") or "")
    if "warning" not in t0_action:
        fails.append("tiers[0].action must contain 'warning' (got %r)" % t0_action)

    # tiers[1].suspend_days = 3
    t1_days = tiers[1].get("suspend_days")
    try:
        if int(t1_days) != 3:
            fails.append("tiers[1].suspend_days must be 3 (got %r)" % t1_days)
    except (TypeError, ValueError):
        fails.append("tiers[1].suspend_days must be int 3 (got %r)" % t1_days)

    # tiers[2].suspend_days = 7
    t2_days = tiers[2].get("suspend_days")
    try:
        if int(t2_days) != 7:
            fails.append("tiers[2].suspend_days must be 7 (got %r)" % t2_days)
    except (TypeError, ValueError):
        fails.append("tiers[2].suspend_days must be int 7 (got %r)" % t2_days)

    # h1_2025.harassment.removed = 68550 (±2%) — exact figure from NY S895B/A6789B report
    h1 = data.get("h1_2025") or {}
    har = h1.get("harassment") or {}
    removed = har.get("removed")
    try:
        removed = int(removed)
        if not (67179 <= removed <= 69921):
            fails.append(
                "h1_2025.harassment.removed must be ~68550 (±2%%) from NY S895B/A6789B report "
                "(got %d — note: ±10%% tolerance no longer applies, use the exact source value)" % removed
            )
    except (TypeError, ValueError):
        fails.append("h1_2025.harassment.removed must be numeric (got %r)" % removed)

    # h1_2025.hateful.appeal_reversal_rate = 0.300 (±2%) — exact figure from NY report
    hat = h1.get("hateful") or {}
    rev_rate = hat.get("appeal_reversal_rate")
    try:
        rev_rate = float(rev_rate)
        if not (0.294 <= rev_rate <= 0.306):
            fails.append(
                "h1_2025.hateful.appeal_reversal_rate must be ~0.300 (±2%%) from NY S895B/A6789B report "
                "(got %.4f — read the actual report value)" % rev_rate
            )
    except (TypeError, ValueError):
        fails.append("h1_2025.hateful.appeal_reversal_rate must be numeric (got %r)" % rev_rate)

    # rule1_verbatim: must contain full verbatim key phrase from NY report (V9 — verbatim match)
    r1 = str(data.get("rule1_verbatim") or "").lower()
    if "promote hate based on identity" not in r1 and "incite violence" not in r1:
        fails.append(
            "rule1_verbatim must contain verbatim Reddit Rule 1 text from the NY S895B/A6789B report "
            "('incite violence' or 'promote hate based on identity or vulnerability')"
        )

    _finish(fails)
main()
