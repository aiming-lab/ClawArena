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
    data, err = _load_json(ws / "output" / "penalty_final.json")
    if err: _finish([err])
    for fld in ("pre_2026_total", "post_2026_total", "grand_total"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    try:
        pre = int(data["pre_2026_total"])
        post = int(data["post_2026_total"])
        gt = int(data["grand_total"])
        if pre + post != gt:
            fails.append("arithmetic: pre_2026_total (%d) + post_2026_total (%d) != grand_total (%d)" % (pre, post, gt))
        if pre <= 0:
            fails.append("pre_2026_total must be positive (got %d)" % pre)
        if post <= 0:
            fails.append("post_2026_total must be positive — post-SB596 daily violations remain after supersede")
        if gt <= 0:
            fails.append("grand_total must be positive (got %d)" % gt)
    except (TypeError, ValueError) as exc:
        fails.append("pre/post/grand_total must be integers: %s" % exc)
        _finish(fails)
    # Q12 grand_total must differ from Q9 (U2 supersede changed violation count)
    q9, e9 = _load_json(ws / "output" / "penalty_assessment_v2.json")
    if not e9 and q9 is not None:
        q9_gt = q9.get("grand_total_penalty")
        try:
            if int(data["grand_total"]) == int(q9_gt):
                fails.append("grand_total (%d) equals Q9 total — U2 supersede must change the penalty" % int(data["grand_total"]))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
main()
