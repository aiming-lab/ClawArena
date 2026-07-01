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
    data, err = _load_json(ws / "output" / "q05_containment_decision.json")
    if err: _finish([err])
    # key_prefix 必须是 AKIA（GuardDuty findings 中的主要 prefix）
    kp = data.get("key_prefix")
    if str(kp).upper() != "AKIA":
        fails.append("key_prefix == %r (expected 'AKIA' — long-term IAM key identified from GuardDuty findings)" % kp)
    # containment_method 必须是 disable_iam_user_key（非 revoke_sts_token）
    cm = str(data.get("containment_method", "")).lower()
    if "disable_iam" not in cm and "disable" not in cm:
        fails.append("containment_method == %r (expected 'disable_iam_user_key' — not 'revoke_sts_token' which is for ASIA keys)" % data.get("containment_method"))
    if "sts" in cm or "revoke_sts" in cm:
        fails.append("containment_method must NOT be revoke_sts_token — that is for STS/ASIA keys, not AKIA")
    # rule_name verbatim（大写完整标识符）
    rn = str(data.get("rule_name", ""))
    if rn != "ACCESS_KEYS_ROTATED":
        fails.append("rule_name == %r (expected verbatim 'ACCESS_KEYS_ROTATED' — exact AWS Config rule identifier)" % rn)
    _finish(fails)
main()
