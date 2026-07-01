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
    data, err = _load_json(ws / "output" / "sb596_penalty_projection.json")
    if err: _finish([err])
    # 结构层
    for fld in ("effective_date", "pre_sb596_total", "post_sb596_total", "diff"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层
    ed = str(data.get("effective_date", ""))
    if ed != "2026-01-01":
        fails.append("effective_date == %r (expected '2026-01-01')" % ed)
    try:
        pre = int(data["pre_sb596_total"])
        post = int(data["post_sb596_total"])
        diff = int(data["diff"])
        if post <= pre:
            fails.append("post_sb596_total (%d) must be > pre_sb596_total (%d)" % (post, pre))
        if diff != post - pre:
            fails.append("diff (%d) != post_sb596_total - pre_sb596_total (%d)" % (diff, post - pre))
    except (TypeError, ValueError) as exc:
        fails.append("pre/post/diff must be integers: %s" % exc)
    # cross-round closure: pre_sb596_total must match Q3 total (if Q3 exists)
    q3, e3 = _load_json(ws / "output" / "penalty_assessment.json")
    if not e3 and q3 is not None:
        q3_total = q3.get("total_penalty_usd")
        try:
            if int(data["pre_sb596_total"]) != int(q3_total):
                fails.append("pre_sb596_total (%d) != Q3 total_penalty_usd (%d) (cross-round closure)" % (
                    int(data["pre_sb596_total"]), int(q3_total)))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
main()
