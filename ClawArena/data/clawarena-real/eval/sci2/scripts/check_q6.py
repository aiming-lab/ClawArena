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
    csv_path = ws / "rca_outputs" / "failure_mode_stats.csv"
    if not csv_path.exists():
        _finish(["file not found: rca_outputs/failure_mode_stats.csv"])
    import csv as csvmod
    rows = []
    with csv_path.open(encoding="utf-8") as fh:
        reader = csvmod.DictReader(fh)
        for r in reader:
            rows.append(r)
    if not rows:
        _finish(["failure_mode_stats.csv is empty"])
    # 检查必要列
    cols = set(rows[0].keys())
    for need in ("failure_mode", "count", "pct_of_total"):
        if need not in cols:
            fails.append("missing column: %s" % need)
    if fails:
        _finish(fails)
    # 总数精确 = 3698（零容差）
    total = 0
    for r in rows:
        try:
            total += int(r["count"])
        except (ValueError, TypeError):
            fails.append("count not numeric in row: %r" % r)
    if not fails and total != 3698:
        fails.append(
            "sum of count == %d (must equal exactly 3698; this is the authoritative complaint "
            "count from the FDA recall notice — the CSV must be derived from the actual data, "
            "not an approximate figure)" % total
        )
    # pct_of_total 须为 2 位小数格式字符串（如 "27.72"，不接受整数或 1 位小数）
    import re as _re
    for r in rows:
        pct_str = str(r.get("pct_of_total", ""))
        try:
            float(pct_str)
        except (ValueError, TypeError):
            fails.append("pct_of_total not numeric in row: %r" % r)
            break
        if not _re.fullmatch(r"-?\d+\.\d{2}", pct_str.strip()):
            fails.append(
                "pct_of_total %r in row '%s' must be formatted as a 2-decimal-place number "
                "(e.g. '27.72', not '27.7' or 27) — required precision for regulatory reporting" % (
                    pct_str, r.get("failure_mode", "?"))
            )
            break
    # C★ 跨轮闭合：与 Q1 nimbus_recall_metadata.json 中的 complaints 字段交叉核验
    meta_path = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            q1_complaints = int(meta.get("complaints", -1))
            if q1_complaints != total:
                fails.append(
                    "cross-round consistency failure: failure_mode_stats.csv total count (%d) "
                    "does not match nimbus_recall_metadata.json complaints field (%d) — "
                    "Q1 and Q6 outputs must be internally consistent" % (total, q1_complaints)
                )
        except Exception as e:
            fails.append("could not cross-check with nimbus_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "nimbus_recall_metadata.json not found — Q6 requires Q1 output for cross-round "
            "consistency verification of the 3,698 complaint total"
        )
    _finish(fails)
main()
