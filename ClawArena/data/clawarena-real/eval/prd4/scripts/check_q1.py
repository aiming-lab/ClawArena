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
    data, err = _load_json(ws / "output" / "policy_summary.json")
    if err: _finish([err])
    # 结构层：必须有 response_sla
    rs = data.get("response_sla")
    if not isinstance(rs, dict):
        _finish(["response_sla must be an object"])
    # 字段层：L1 response
    l1 = rs.get("L1")
    if isinstance(l1, dict):
        l1_val = l1.get("response_minutes")
    else:
        l1_val = l1
    try:
        l1_int = int(l1_val)
    except (TypeError, ValueError):
        _finish(["L1 response_minutes not a number: %r" % l1_val])
    if l1_int != 30:
        fails.append("L1 response_minutes == %d (expected 30, not 60/1h which is Premium)" % l1_int)
    # L2 response
    l2 = rs.get("L2")
    if isinstance(l2, dict):
        l2_val = l2.get("response_minutes")
    else:
        l2_val = l2
    try:
        l2_int = int(l2_val)
    except (TypeError, ValueError):
        _finish(["L2 response_minutes not a number: %r" % l2_val])
    if l2_int != 120:
        fails.append("L2 response_minutes == %d (expected 120 = 2h)" % l2_int)
    # L3 response
    l3 = rs.get("L3")
    if isinstance(l3, dict):
        l3_val = l3.get("response_minutes")
    else:
        l3_val = l3
    try:
        l3_int = int(l3_val)
        if l3_int != 480:
            fails.append("L3 response_minutes == %d (expected 480 = 8h)" % l3_int)
    except (TypeError, ValueError):
        fails.append("L3 response_minutes not a number or missing: %r" % l3_val)
    # L4 response
    l4 = rs.get("L4")
    if isinstance(l4, dict):
        l4_val = l4.get("response_minutes")
    else:
        l4_val = l4
    try:
        l4_int = int(l4_val)
        if l4_int != 1440:
            fails.append("L4 response_minutes == %d (expected 1440 = 24h)" % l4_int)
    except (TypeError, ValueError):
        fails.append("L4 response_minutes not a number or missing: %r" % l4_val)
    # sla_policy_version must be "v1"
    ver = str(data.get("sla_policy_version") or "")
    if ver != "v1":
        fails.append("sla_policy_version == %r (expected exactly 'v1')" % ver)
    # plan must reference "Enterprise"
    plan = str(data.get("plan") or "")
    if "Enterprise" not in plan and "enterprise" not in plan.lower():
        fails.append("plan == %r (expected to contain 'Enterprise')" % plan)
    # 真值层：availability uptime
    upt = data.get("availability_commitment_pct")
    try:
        upt_f = float(upt)
    except (TypeError, ValueError):
        _finish(["availability_commitment_pct not numeric: %r" % upt])
    if abs(upt_f - 99.95) > 0.01:
        fails.append("availability_commitment_pct == %r (expected 99.95)" % upt_f)
    # credit tiers: find tier0 (5% for 99.90-99.95)
    tiers = data.get("credit_tiers") or []
    tier0_found = False
    for t in tiers:
        if isinstance(t, dict):
            pct = t.get("credit_pct")
            rng = str(t.get("uptime_range") or "")
            if pct is not None:
                try:
                    if int(pct) == 5 and ("99.90" in rng or "99.9" in rng):
                        tier0_found = True
                except (ValueError, TypeError):
                    pass
    if not tier0_found:
        fails.append("credit_tiers missing the Enterprise-exclusive 5% tier for 99.90-99.95% range")
    # credit tiers must have all 4 tiers (including tier for < 95.00% at 50%)
    tier50_found = any(
        isinstance(t, dict) and t.get("credit_pct") is not None and
        (lambda v: v == 50)(int(t.get("credit_pct", 0)))
        for t in tiers
    )
    if not tier50_found:
        fails.append("credit_tiers missing the 50%% tier for < 95.00%% range (all 4 tiers required)")
    _finish(fails)
main()
