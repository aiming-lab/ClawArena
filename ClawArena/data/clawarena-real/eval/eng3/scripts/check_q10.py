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
    data, err = _load_json(ws / "output" / "q10_causal_chains.json")
    if err: _finish([err])
    for k in ("chain_1", "chain_2"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    c1 = data.get("chain_1") or {}
    c2 = data.get("chain_2") or {}
    # chain_1: trigger含 DDoS/ddos, mechanism含 lua/tail call
    c1_text = " ".join(str(v) for v in c1.values()).lower()
    if not re.search(r"ddos|ddo\s", c1_text):
        fails.append("chain_1 trigger/mechanism must reference 'DDoS' or 'ddos'")
    if not re.search(r"lua|tail.?call", c1_text):
        fails.append("chain_1 mechanism must reference 'Lua' or 'tail call'")
    # chain_2: trigger含 backbone/congestion, 时间窗含 17:33 或 traffic.?manager
    c2_text = " ".join(str(v) for v in c2.values()).lower()
    if not re.search(r"backbone|congestion", c2_text):
        fails.append("chain_2 trigger must reference 'backbone' or 'congestion'")
    if not re.search(r"17:33|17:50|traffic.?manager|trafficmanager", c2_text):
        fails.append("chain_2 must reference 17:33/17:50 time window or Traffic Manager")
    _finish(fails)
main()
