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
    data, err = _load_json(ws / "work" / "slow_queries_top5.json")
    if err: _finish([err])
    # Structure: must be a list
    if not isinstance(data, list):
        _finish(["slow_queries_top5.json must be a JSON array"])
    if len(data) != 5:
        fails.append("array length == %d (expected exactly 5)" % len(data))
    required_fields = {"queryid", "query_preview", "mean_exec_time_ms", "calls"}
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            fails.append("entry[%d] is not an object" % i); continue
        missing = required_fields - set(entry.keys())
        if missing:
            fails.append("entry[%d] missing fields %s" % (i, sorted(missing))); continue
        # True-value layer: mean_exec_time_ms must be > 500
        try:
            met = float(entry["mean_exec_time_ms"])
        except (TypeError, ValueError):
            fails.append("entry[%d].mean_exec_time_ms not numeric: %r" % (i, entry["mean_exec_time_ms"])); continue
        if met <= 500:
            fails.append("entry[%d].mean_exec_time_ms == %.2f (must be > 500ms)" % (i, met))
        # calls must be a positive integer
        try:
            c = int(entry["calls"])
            if c <= 0:
                fails.append("entry[%d].calls must be positive int, got %d" % (i, c))
        except (TypeError, ValueError):
            fails.append("entry[%d].calls not an int: %r" % (i, entry["calls"]))
        # queryid must be a positive integer
        try:
            qid = int(entry["queryid"])
            if qid <= 0:
                fails.append("entry[%d].queryid must be positive int, got %r" % (i, qid))
        except (TypeError, ValueError):
            fails.append("entry[%d].queryid not an int: %r" % (i, entry["queryid"]))
    # Verify sorted descending by mean_exec_time_ms
    if len(data) == 5:
        times = []
        for e in data:
            try:
                times.append(float(e["mean_exec_time_ms"]))
            except Exception:
                pass
        if times != sorted(times, reverse=True):
            fails.append("array is not sorted descending by mean_exec_time_ms")
    # HARDENED: exact queryid set must be {1003, 1014, 1010, 1013, 1017} (true top-5 from CSV)
    EXACT_QUERYIDS = {1003, 1014, 1010, 1013, 1017}
    if len(data) == 5 and not any("queryid" in (f or "") for f in fails):
        try:
            got_ids = set(int(e["queryid"]) for e in data if isinstance(e, dict))
            if got_ids != EXACT_QUERYIDS:
                fails.append(
                    "queryid set %s != expected %s (read the CSV: top-5 by mean_exec_time are queryids 1003, 1014, 1010, 1013, 1017 — NOT starting at 1001)" % (
                        sorted(got_ids), sorted(EXACT_QUERYIDS)
                    )
                )
        except (TypeError, ValueError, KeyError):
            pass
    # HARDENED: each entry's mean_exec_time_ms must match the CSV value within 1%
    TRUE_TIMES = {1003: 12450.67, 1014: 9870.34, 1010: 8920.45, 1013: 7340.88, 1017: 6120.45}
    for i, entry in enumerate(data):
        if not isinstance(entry, dict): continue
        try:
            qid = int(entry.get("queryid") or 0)
            met = float(entry.get("mean_exec_time_ms") or 0)
            if qid in TRUE_TIMES:
                ref = TRUE_TIMES[qid]
                if not (ref * 0.99 <= met <= ref * 1.01):
                    fails.append(
                        "entry[%d] queryid=%d mean_exec_time_ms=%.2f does not match CSV value %.2f (within 1%%)" % (
                            i, qid, met, ref
                        )
                    )
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
