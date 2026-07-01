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
    txt = _read(ws / "output" / "q12_attribution_log.md")
    if txt is None:
        _finish(["file not found: output/q12_attribution_log.md"])
    low = txt.lower()
    # V10 supersede: must mention superseded
    if "supersed" not in low:
        fails.append("attribution_log.md must use the word 'superseded' (old memo is superseded)")
    # V6 correct attribution: Data Colada or Simonsohn/Nelson/Simmons
    if "data colada" not in low and "simonsohn" not in low:
        fails.append("attribution_log.md must name the Data Colada team (or Simonsohn) as calcChain analysts")
    # V5 bot decoy N=201 must be marked incorrect/rejected
    if "201" not in txt:
        fails.append("attribution_log.md must reference the bot's N=201 claim")
    if "incorrect" not in low and "rejected" not in low and "wrong" not in low and "error" not in low:
        fails.append("attribution_log.md must label the N=201 claim as INCORRECT, rejected, wrong, or error")
    # V4: N=101 affirmed
    if "101" not in txt and "n=101" not in low:
        fails.append("attribution_log.md must affirm N=101")
    # F: must cite the verbatim filename of the superseding legal memo
    if "legal_memo_calcchain_v2" not in txt:
        fails.append("attribution_log.md must cite 'legal_memo_calcchain_v2' (the verbatim filename of the superseding document; read cases/gino/legal_memo_calcchain_v2.md)")
    _finish(fails)
main()
