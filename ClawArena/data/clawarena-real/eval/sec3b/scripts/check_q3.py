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

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "affected_orders_count.json")
    if err: _finish([err])
    # time window must be exactly 14:00-15:00 UTC on 2024-11-03
    start = str(data.get("time_window_utc_start") or "")
    end = str(data.get("time_window_utc_end") or "")
    if "2024-11-03T14:00:00" not in start:
        fails.append("time_window_utc_start == %r (expected '2024-11-03T14:00:00Z')" % start)
    if "2024-11-03T15:00:00" not in end:
        fails.append("time_window_utc_end == %r (expected '2024-11-03T15:00:00Z')" % end)
    # total_affected must be the exact count of ANOMALY_DST_MISMATCH entries in the audit log
    ta = data.get("total_affected")
    try:
        ta = int(ta)
    except (TypeError, ValueError):
        _finish(["total_affected not an int: %r" % ta])
    if ta <= 0:
        fails.append("total_affected == %d (expected positive int matching audit log count)" % ta)
    # audit_log_total_scanned: required field — must be the TOTAL line count scanned
    # (not just the anomalies — the entire audit log file). Used in downstream cross-round closures.
    tsc = data.get("audit_log_total_scanned")
    if tsc is None:
        fails.append(
            "audit_log_total_scanned field missing — must be the total number of non-empty "
            "lines scanned in incident/aros_v4_2_audit_log.jsonl (required for downstream audit trail)"
        )
    else:
        try:
            tsc = int(tsc)
        except (TypeError, ValueError):
            _finish(["audit_log_total_scanned not an int: %r" % tsc])
        # Recount from audit log to verify both total and anomaly counts
        audit_log = ws / "incident" / "aros_v4_2_audit_log.jsonl"
        if audit_log.exists():
            import json as _json
            real_count = 0
            real_total = 0
            with open(audit_log, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    real_total += 1
                    try:
                        entry = _json.loads(line)
                        if entry.get("status") == "ANOMALY_DST_MISMATCH":
                            real_count += 1
                    except _json.JSONDecodeError:
                        pass
            if ta != real_count:
                fails.append(
                    "total_affected == %d but audit log has exactly %d ANOMALY_DST_MISMATCH entries "
                    "(must read and count the log accurately)" % (ta, real_count)
                )
            if tsc != real_total:
                fails.append(
                    "audit_log_total_scanned == %d but audit log has exactly %d non-empty lines "
                    "(must count all scanned lines, not just anomalies)" % (tsc, real_total)
                )
        else:
            if ta != real_count if False else False:
                pass  # skip if no audit log
    _finish(fails)
main()
