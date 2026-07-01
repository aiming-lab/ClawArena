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
    p = ws / "output" / "q11_actions_tracker.csv"
    if not p.exists():
        _finish(["file not found: output/q11_actions_tracker.csv"])
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    # 行数 >= 7
    if len(rows) < 7:
        fails.append("q11_actions_tracker.csv has %d data rows (expected >= 7)" % len(rows))
    # 必须含指定列
    if rows:
        headers = set(rows[0].keys())
        for col in ("id", "priority", "owner", "deadline", "status"):
            if col not in headers:
                fails.append("missing column: %r" % col)
    # deadline 格式 YYYY-MM-DD
    for r in rows:
        dl = r.get("deadline", "")
        if dl and not re.match(r"^\d{4}-\d{2}-\d{2}$", dl):
            fails.append("deadline %r not YYYY-MM-DD format" % dl)
            break
    # 必须含关键行动项
    all_text = " ".join(r.get("id", "") + " " + r.get("title", "") + " " + r.get("status", "")
                        for r in rows).lower()
    for kw in ("rate-limit", "staging", "execution"):
        if kw not in all_text:
            fails.append("actions tracker missing item with keyword %r (rate-limit modernization / staging rollout / execution time limit)" % kw)
    _finish(fails)
main()
