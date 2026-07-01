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
    data, err = _load_json(ws / "output" / "force_majeure_review.json")
    if err: _finish([err])
    # termination_threshold_days 必须是 120（ICC 2020 标准，非 90）
    thr = data.get("termination_threshold_days")
    try:
        thr = int(thr)
    except (TypeError, ValueError):
        _finish(["termination_threshold_days not an int: %r" % thr])
    if thr != 120:
        fails.append("termination_threshold_days == %d (expected 120 per ICC 2020 standard, NOT 90)" % thr)
    # notice_days 必须是正整数（从 MSA v2.3 §11.2 提取）
    nd = data.get("notice_days")
    try:
        nd = int(nd)
        if nd <= 0:
            fails.append("notice_days must be a positive int")
    except (TypeError, ValueError):
        fails.append("notice_days not an int: %r" % nd)
    # compliant_with_icc_2020 必须是 bool
    if not isinstance(data.get("compliant_with_icc_2020"), bool):
        fails.append("compliant_with_icc_2020 must be a boolean")
    # icc_source 必须非空
    if not data.get("icc_source"):
        fails.append("icc_source must be present and non-empty")
    _finish(fails)
main()
