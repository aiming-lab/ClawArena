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
    data, err = _load_json(ws / "output" / "risk_matrix.json")
    if err: _finish([err])
    risks = data.get("risks")
    if not isinstance(risks, list):
        _finish(["risks must be a JSON array"])
    if len(risks) < 5:
        fails.append("risks array has %d entries (expected >= 5)" % len(risks))
    # 每个 risk 必须有 risk_id / risk_level / clause_ref / description / recommendation
    for i, r in enumerate(risks):
        if not isinstance(r, dict):
            fails.append("risks[%d] is not an object" % i); continue
        for k in ("risk_id", "risk_level", "clause_ref", "description", "recommendation"):
            if not r.get(k):
                fails.append("risks[%d] missing or empty field '%s'" % (i, k))
        rl = str(r.get("risk_level", "")).strip().upper()
        if rl not in ("HIGH", "MEDIUM", "LOW"):
            fails.append("risks[%d] risk_level == %r (must be exactly HIGH, MEDIUM, or LOW)" % (i, rl))
    # HIGH 级风险必须包含 DPA sub-processor 和 warranty disclaimer
    high_risks = [r for r in risks if isinstance(r, dict) and str(r.get("risk_level","")).upper() == "HIGH"]
    if not high_risks:
        fails.append("no HIGH-level risks found (at least DPA sub-processor and warranty disclaimer must be HIGH)")
    else:
        all_high_text = " ".join(
            json.dumps(r).lower() for r in high_risks
        )
        if "sub-processor" not in all_high_text and "subprocessor" not in all_high_text and "sub processor" not in all_high_text:
            fails.append("HIGH risks must include the DPA sub-processor written authorisation gap")
        if "warranty" not in all_high_text and "disclaimer" not in all_high_text and "as is" not in all_high_text:
            fails.append("HIGH risks must include the AS IS warranty disclaimer compliance concern")
    # 第一个 risk 必须是 HIGH（按 HIGH→LOW 排序）
    if risks and isinstance(risks[0], dict):
        first_rl = str(risks[0].get("risk_level", "")).strip().upper()
        if first_rl != "HIGH":
            fails.append("first risk must be HIGH-level (risks should be sorted HIGH→MEDIUM→LOW)")
    _finish(fails)
main()
