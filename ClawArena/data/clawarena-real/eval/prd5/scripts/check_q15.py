#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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
    txt = _read(ws / "output" / "q15_final_report.md")
    if txt is None:
        _finish(["file not found: output/q15_final_report.md"])
    low = txt.lower()
    # Must mention all 12 experiment IDs
    for i in range(1, 13):
        eid = "exp%03d" % i
        if eid not in low:
            fails.append("q15_final_report.md does not mention %s" % eid)
    # exp003 conclusion must be no significant effect (V4 cross-round closure)
    exp003_ctx = ""
    idx = low.find("exp003")
    if idx >= 0:
        exp003_ctx = low[max(0, idx-50):idx+200]
    if not any(kw in exp003_ctx for kw in ("not significant", "no significant", "insignificant",
                                             "no effect", "null result", "p=0.31", "p = 0.31")):
        fails.append("report does not state exp003 as 'no significant effect' (required: V4 cross-round closure)")
    # Must reference Bonferroni (NOT BH as primary method — V10 supersede)
    if "bonferroni" not in low:
        fails.append("report must reference Bonferroni correction (VP BH directive was superseded)")
    # Must cite 57% peeking false positive rate (V4 cross-round with Q6)
    if "57" not in txt:
        fails.append("report must cite 57%% peeking false positive rate (from Q6 analysis)")
    # Must have >= 2 ## section headers
    if len(re.findall(r"^## ", txt, re.MULTILINE)) < 2:
        fails.append("fewer than 2 \'## \' section headers")
    _finish(fails)
main()
