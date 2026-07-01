#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "penalty_assessment_v2.json")
    if err: _finish([err])
    for fld in ("post_sb596_count", "grand_total_penalty", "pre_sb596_count"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层：post_sb596_count = 7 (the 7 daily violations Jan 2-8)
    psc = data.get("post_sb596_count")
    try:
        psc_int = int(psc)
        if psc_int != 7:
            fails.append("post_sb596_count == %d (expected 7 — the 7 daily violations Jan 2-8 2026)" % psc_int)
    except (TypeError, ValueError):
        fails.append("post_sb596_count not an int: %r" % psc)
    # 真值层 (A加难)：pre_sb596_count 必须精确等于 17
    # 说明：Oct 2024 有 13 个违规班次 (SH-1008 to SH-1488)；pre-SB596 Telemetry 有 4 个 (Dec 28-31)
    # 总共 17 个 pre-SB596 违规计数。注意 SB 596 生效日期为 2026-01-01，
    # 因此 Dec 2025 的 Telemetry 违规（4 次）均属于 pre-SB596 范畴。
    # 浅做的模型可能只统计 Oct 2024 违规 (13)，或者误将 Dec Telemetry 作为 post 计算。
    pre_count = data.get("pre_sb596_count")
    try:
        pre_int = int(pre_count)
        if pre_int != 17:
            fails.append(
                "pre_sb596_count == %d (expected 17: 13 Oct-2024 violation shifts + 4 pre-SB596 "
                "Telemetry Dec 28-31 2025; SB 596 effective 2026-01-01)" % pre_int)
    except (TypeError, ValueError):
        fails.append("pre_sb596_count not an int: %r" % pre_count)
    # grand_total > Q3 total
    q3, e3 = _load_json(ws / "output" / "penalty_assessment.json")
    gtp = data.get("grand_total_penalty")
    try:
        gtp_int = int(gtp)
        if not e3 and q3 is not None:
            q3t = int(q3.get("total_penalty_usd", 0))
            if gtp_int <= q3t:
                fails.append("grand_total_penalty (%d) must be > Q3 total (%d) — new violations added" % (gtp_int, q3t))
        # 真值层 (C加难)：grand_total 精确验证
        # 计算: pre-SB596 penalty = $15k (Oct first) + $30k (Dec Tel group) = $45k
        # post-SB596 penalty = 7 × $30k = $210k; grand_total = $45k + $210k = $255k
        if gtp_int != 255000:
            fails.append(
                "grand_total_penalty == %d (expected 255000: "
                "pre=$45k [Oct first@$15k + Dec-Tel@$30k] + post=$210k [7 daily@$30k])" % gtp_int)
    except (TypeError, ValueError):
        fails.append("grand_total_penalty not an int: %r" % gtp)
    _finish(fails)
main()
main()
