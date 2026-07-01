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
    data, err = _load_json(ws / "output" / "q6_why_connect_stats.json")
    if err: _finish([err])
    # V9 verbatim DOI
    doi = str(data.get("paper_doi") or "")
    if doi != "10.1037/pspa0000226":
        fails.append("paper_doi == %r (expected verbatim '10.1037/pspa0000226')" % doi)
    # F-stat closure: 17.69 +/- 0.1
    try:
        f = float(data.get("F_stat"))
        if not (17.59 <= f <= 17.79):
            fails.append("F_stat == %.4f (expected near 17.69, read from part4_why_connect.md)" % f)
    except (TypeError, ValueError):
        fails.append("F_stat not numeric: %r" % data.get("F_stat"))
    try:
        if int(data.get("df1")) != 2:
            fails.append("df1 == %r (expected 2)" % data.get("df1"))
        if int(data.get("df2")) != 596:
            fails.append("df2 == %r (expected 596)" % data.get("df2"))
    except (TypeError, ValueError):
        fails.append("df1 or df2 not int")
    try:
        if float(data.get("p_value")) >= 0.001:
            fails.append("p_value == %r (expected < 0.001)" % data.get("p_value"))
    except (TypeError, ValueError):
        fails.append("p_value not numeric: %r" % data.get("p_value"))
    # F: word_rating_mismatch_count from part4_why_connect.md — 18 impossible pairs
    wm = data.get("word_rating_mismatch_count")
    try:
        if int(wm) != 18:
            fails.append("word_rating_mismatch_count == %r (expected 18, from part4_why_connect.md: 18 Prevention participants with impossible 3.0-rating + positive-word pairs)" % wm)
    except (TypeError, ValueError):
        fails.append("word_rating_mismatch_count missing or not int (expected 18; read part4_why_connect.md)")
    # F: prevention_corr_p from part4_why_connect.md — must be 0.026 (±0.001)
    pcp = data.get("prevention_corr_p")
    try:
        pcpf = float(pcp)
        if not (0.025 <= pcpf <= 0.027):
            fails.append("prevention_corr_p == %r (expected 0.026 ±0.001, from part4_why_connect.md Fisher z test)" % pcp)
    except (TypeError, ValueError):
        fails.append("prevention_corr_p missing or not numeric (expected 0.026; read part4_why_connect.md)")
    _finish(fails)
main()
