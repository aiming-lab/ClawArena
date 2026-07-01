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
    txt = _read(ws / "output" / "q13_n_verification.md")
    if txt is None:
        _finish(["file not found: output/q13_n_verification.md"])
    low = txt.lower()
    # V4: N=101 affirmed
    if "n=101" not in low and "n_total: 101" not in low and "n_total=101" not in low and "101" not in txt:
        fails.append("n_verification.md must state N=101")
    # V5: N=201 explicitly rejected
    if "201" not in txt:
        fails.append("n_verification.md must reference the bot's N=201 claim to reject it")
    if "incorrect" not in low and "rejected" not in low and "wrong" not in low and "error" not in low:
        fails.append("n_verification.md must label N=201 as INCORRECT, rejected, wrong, or error")
    # V1: bot/automated summary cited as source of error
    if "bot" not in low and "automated" not in low and "auto" not in low:
        fails.append("n_verification.md must reference the bot or automated summary as source of N=201 error")
    # V9: PNAS DOI referenced
    if "10.1073/pnas.1209746109" not in txt:
        fails.append("n_verification.md must reference PNAS DOI '10.1073/pnas.1209746109'")
    # F: must include the exact URL https://datacolada.org/109
    if "https://datacolada.org/109" not in txt:
        fails.append("n_verification.md must include the exact URL https://datacolada.org/109 (the primary source; read cases/gino/datacolada_reports/part1_pnas_analysis.md)")
    _finish(fails)
main()
