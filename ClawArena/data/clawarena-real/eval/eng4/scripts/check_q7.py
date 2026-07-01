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
    data, err = _load_json(ws / "work" / "optimization_comparison.json")
    if err: _finish([err])
    results = data.get("results") or []
    if not isinstance(results, list):
        _finish(["optimization_comparison.json: results must be a JSON array"])
    if len(results) != 9:
        fails.append("results array length == %d (expected exactly 9)" % len(results))
    required = {"query_id","before_node_type","after_node_type","before_total_cost",
                "after_total_cost","cost_reduction_pct","before_actual_time_ms","after_actual_time_ms"}
    q001_entry = None
    for i, entry in enumerate(results):
        if not isinstance(entry, dict):
            fails.append("results[%d] is not an object" % i); continue
        missing = required - set(entry.keys())
        if missing:
            fails.append("results[%d] missing fields %s" % (i, sorted(missing)))
        qid = str(entry.get("query_id") or "")
        if "001" in qid:
            q001_entry = entry
        # Verify cost_reduction_pct arithmetic
        try:
            bef = float(entry.get("before_total_cost") or 0)
            aft = float(entry.get("after_total_cost") or 0)
            crp = float(entry.get("cost_reduction_pct") or 0)
            if bef > 0:
                expected_pct = round((bef - aft) / bef * 100, 2)
                if abs(crp - expected_pct) > 0.1:
                    fails.append("results[%d].cost_reduction_pct == %.2f but expected %.2f "
                                 "(formula: (before-after)/before*100)" % (i, crp, expected_pct))
        except (TypeError, ValueError):
            fails.append("results[%d] cost fields not numeric" % i)
    # query_001 specific checks
    if q001_entry is not None:
        ant = q001_entry.get("after_node_type")
        if ant != "Index Only Scan":
            fails.append("query_001 after_node_type == %r (expected \"Index Only Scan\")" % ant)
        # Cross-round closure: before_total_cost must match q001_analysis.json
        q2_data, q2_err = _load_json(ws / "work" / "q001_analysis.json")
        if not q2_err and q2_data is not None:
            try:
                q2_cost = float(q2_data.get("total_cost") or 0)
                q7_bef = float(q001_entry.get("before_total_cost") or 0)
                if abs(q7_bef - q2_cost) > q2_cost * 0.01:
                    fails.append("cross-round drift: query_001 before_total_cost %.2f != Q2 total_cost %.2f" % (q7_bef, q2_cost))
            except (TypeError, ValueError):
                pass
    elif len(results) >= 9:
        fails.append("no results entry found for query_001")
    _finish(fails)
main()
