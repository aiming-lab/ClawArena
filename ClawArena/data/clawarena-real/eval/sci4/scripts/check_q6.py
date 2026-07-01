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
    data, err = _load_json(ws / "output" / "dpa_compliance.json")
    if err: _finish([err])
    # missing_items 必须含子处理器授权机制
    missing = [str(x).lower() for x in (data.get("missing_items") or [])]
    missing_str = " ".join(missing)
    if "sub-processor" not in missing_str and "subprocessor" not in missing_str and "sub processor" not in missing_str:
        fails.append("missing_items must include the sub-processor written authorisation mechanism (GDPR Art.28(3)(d))")
    # penalty_risk 必须引用 €10,000,000 或 10000000 或 2%
    pr = str(data.get("penalty_risk", "")).lower()
    has_penalty = ("10,000,000" in pr or "10000000" in pr or "€10" in pr or
                   "eur 10" in pr or "10 million" in pr or "10m" in pr)
    has_pct = ("2%" in pr or "2 percent" in pr or "two percent" in pr)
    if not (has_penalty or has_pct):
        fails.append("penalty_risk must reference '€10,000,000' or '2%%' from GDPR Art.83(4)")
    # overall_compliant 必须是 false（有缺失项）
    if data.get("overall_compliant") is not False:
        fails.append("overall_compliant must be false (DPA has identified gaps)")
    # compliant_items 必须非空
    ci = data.get("compliant_items")
    if not isinstance(ci, list) or len(ci) == 0:
        fails.append("compliant_items must be a non-empty list")
    _finish(fails)
main()
