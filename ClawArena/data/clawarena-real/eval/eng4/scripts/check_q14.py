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
    report_path = ws / "work" / "final_optimization_report.json"
    sign_path = ws / "work" / "signoff.txt"
    data, err = _load_json(report_path)
    if err: _finish([err])
    # total_queries_optimized must be 12 (consistent with Q12)
    tqo = data.get("total_queries_optimized")
    try:
        tqo = int(tqo)
        if tqo != 12:
            fails.append("total_queries_optimized == %d (expected 12, must match Q12 total_queries)" % tqo)
    except (TypeError, ValueError):
        fails.append("total_queries_optimized not an int: %r" % data.get("total_queries_optimized"))
    # work_mem_modified must be False (architect superseded the work_mem change)
    wmm = data.get("work_mem_modified")
    if wmm is not False:
        fails.append("work_mem_modified == %r (must be false — architect superseded the work_mem=256MB directive)" % wmm)
    # indexes_created must be present and non-empty
    ic = data.get("indexes_created") or []
    if not isinstance(ic, list) or len(ic) == 0:
        fails.append("indexes_created must be a non-empty array")
    # statistics_created must reference CREATE STATISTICS
    sc = data.get("statistics_created") or []
    if not isinstance(sc, list) or len(sc) == 0:
        fails.append("statistics_created must be a non-empty array")
    else:
        found_deps = any("statistic" in str(s).lower() for s in sc)
        if not found_deps:
            fails.append("statistics_created must include the CREATE STATISTICS DDL")
    # Cross-round closure with optimization_log.jsonl: indexes_created length must match log entries
    log_txt = _read(ws / "work" / "optimization_log.jsonl")
    if log_txt:
        log_count = sum(1 for l in log_txt.splitlines() if l.strip())
        if log_count > 0 and len(ic) != log_count:
            fails.append("indexes_created length %d != optimization_log.jsonl entries %d (cross-round closure)" % (len(ic), log_count))
    # Check signoff.txt
    sign = _read(sign_path)
    if sign is None:
        _finish(["file not found: work/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        fails.append("signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80])
    elif report_path.exists():
        digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
        if m.group(1) != digest:
            fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
