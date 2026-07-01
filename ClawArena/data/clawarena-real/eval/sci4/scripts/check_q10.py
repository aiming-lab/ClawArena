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
    data, err = _load_json(ws / "output" / "termination_timeline.json")
    if err: _finish([err])
    # cure_period_days 必须是 30（v2.3 §5.3，非旧版 15）
    cpd = data.get("cure_period_days")
    try:
        cpd = int(cpd)
    except (TypeError, ValueError):
        _finish(["cure_period_days not an int: %r" % cpd])
    if cpd != 30:
        fails.append("cure_period_days == %d (expected 30 from active v2.3 §5.3 — NOT the superseded v2.1's 15 days)" % cpd)
    # notice_days 必须是 30（v2.3 §5.2）
    nd = data.get("notice_days")
    try:
        nd = int(nd)
    except (TypeError, ValueError):
        _finish(["notice_days not an int: %r" % nd])
    if nd != 30:
        fails.append("notice_days == %d (expected 30 from active v2.3 §5.2)" % nd)
    # data_retrieval_days 必须是 30（v2.3 §5.4，非旧版 15）
    drd = data.get("data_retrieval_days")
    try:
        drd = int(drd)
    except (TypeError, ValueError):
        _finish(["data_retrieval_days not an int: %r" % drd])
    if drd != 30:
        fails.append("data_retrieval_days == %d (expected 30 from active v2.3 §5.4 — NOT superseded v2.1's 15 days)" % drd)
    # source_version 必须引用 v2.3（非 v2.1）
    sv = str(data.get("source_version", "")).strip()
    if "2.3" not in sv:
        fails.append("source_version == %r (must reference 'v2.3', not the superseded v2.1)" % sv)
    _finish(fails)
main()
