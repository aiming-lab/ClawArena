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

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "corrective_action_plan.md")
    if txt is None:
        _finish(["file not found: output/corrective_action_plan.md"])
    low = txt.lower()
    # 结构层: 含 incident_ref
    if "2024-11-03" not in txt:
        fails.append("CAP must reference incident_ref (2024-11-03)")
    # 真值层: Rule citations
    if "15c3-5(b)" not in txt:
        fails.append("CAP must cite 'Rule 15c3-5(b)' (not just 'Rule 15c3-5')")
    if "15c6-1" not in txt:
        fails.append("CAP must cite 'Rule 15c6-1' (T+1 settlement)")
    # V9: timezone automation fix must be present
    if not re.search(r"timezone|dst|utc.?offset|daylight", low):
        fails.append("CAP must include a timezone/DST automation remediation item")
    # P4 隐式: owner field in each item — check at least 4 owner mentions
    owner_count = len(re.findall(r"\bowner\b", low))
    if owner_count < 4:
        fails.append("CAP must have >= 4 remediation items each with an 'owner' field (found %d 'owner' mentions)" % owner_count)
    # deadline_days: positive integer must appear
    deadlines = re.findall(r"deadline.?days[^\d]*(\d+)", low)
    if not deadlines:
        fails.append("CAP must include deadline_days fields with positive int values")
    else:
        for d in deadlines:
            if int(d) <= 0:
                fails.append("deadline_days value %r must be a positive integer" % d)
    _finish(fails)
main()
