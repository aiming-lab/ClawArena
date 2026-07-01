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
    data, err = _load_json(ws / "output" / "violation_ledger_final.json")
    if err: _finish([err])
    for fld in ("violations", "total_count", "superseded_count", "newly_added_count"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层：superseded_count = 4
    sc = data.get("superseded_count")
    try:
        sc_int = int(sc)
        if sc_int != 4:
            fails.append("superseded_count == %d (expected 4 — the 4 Telemetry violations withdrawn by U2)" % sc_int)
    except (TypeError, ValueError):
        fails.append("superseded_count not an int: %r" % sc)
    # newly_added_count = 2
    nac = data.get("newly_added_count")
    try:
        nac_int = int(nac)
        if nac_int != 2:
            fails.append("newly_added_count == %d (expected 2 — the 2 ICU violations added by U2)" % nac_int)
    except (TypeError, ValueError):
        fails.append("newly_added_count not an int: %r" % nac)
    # total_count closure: must not be q9 count + 2 (that would be additive not supersede)
    tc = data.get("total_count")
    violations = data.get("violations", [])
    try:
        tc_int = int(tc)
        # cross-check with violations list length
        if isinstance(violations, list) and len(violations) > 0:
            if tc_int != len(violations):
                fails.append("total_count (%d) != len(violations) (%d)" % (tc_int, len(violations)))
        # 真值层 (A加难)：total_count 必须精确等于 22
        # 计算：Q9 violations = 13 (Oct2024) + 11 (U1 Telemetry Dec28-Jan8)= 24 total
        # U2 supersedes 4 Telemetry (SH-TEL-U1-002..005) → 24-4=20 remaining
        # U2 adds 2 ICU (SH-ICU-LATE-001, -002) → 20+2=22 final violations
        if tc_int != 22:
            fails.append(
                "total_count == %d (expected 22: 13 Oct-2024 + 11 U1-Telemetry - 4 superseded + 2 new ICU = 22); "
                "a common error is grouping Oct violations into 1 aggregate row or miscounting supersede" % tc_int)
    except (TypeError, ValueError):
        fails.append("total_count not an int: %r" % tc)
    # violations array: each entry must have unit, date, shift_id
    if isinstance(violations, list):
        for i, v in enumerate(violations[:3]):
            for fk in ("unit", "date"):
                if fk not in v:
                    fails.append("violations[%d] missing field %r" % (i, fk))
    # 真值层 (C加难)：每个 violation entry 必须是单个独立班次（不得聚合）
    # 检查：unit 字段不能含 "mixed"/"group" 等聚合词；date 字段不能是区间（含 "to"）
    if isinstance(violations, list):
        for i, v in enumerate(violations):
            if not isinstance(v, dict):
                continue
            unit_str = str(v.get("unit", "")).lower()
            date_str = str(v.get("date", "")).lower()
            if "mixed" in unit_str or "group" in unit_str or "various" in unit_str:
                fails.append(
                    "violations[%d] has aggregated unit=%r; each entry must represent a single shift, "
                    "not a group (Oct 2024 has 13 individual shifts)" % (i, v.get("unit")))
                break
            if " to " in date_str or "through" in date_str or "range" in date_str:
                fails.append(
                    "violations[%d] has date range %r; each entry must represent a single shift date" % (i, v.get("date")))
                break
    _finish(fails)
main()
main()
