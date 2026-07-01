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
    data, err = _load_json(ws / "output" / "npg12_gap_analysis.json")
    if err: _finish([err])
    # elements array
    eps = data.get("elements_of_performance") or data.get("elements") or data.get("eps") or []
    if not isinstance(eps, list):
        _finish(["elements_of_performance must be an array"])
    # 真值层 (D加难)：至少 8 个 EP 条目（NPG 12 共有多个 EP，全面分析需要覆盖 8+ 个）
    if len(eps) < 8:
        fails.append(
            "elements_of_performance has %d entries (expected >= 8; "
            "JC NPG 12 requires analysis of at least 8 Elements of Performance across "
            "NPG.12.01, NPG.12.02, and NPG.12.06 standards)" % len(eps))
    # must have EP NPG.12.02.01 EP4
    found_1202_ep4 = any(
        "12.02.01" in str(e.get("ep_id", "")) and "ep4" in str(e.get("ep_id", "")).lower()
        for e in eps if isinstance(e, dict)
    )
    if not found_1202_ep4:
        # also accept it embedded in requirement text
        found_1202_ep4 = any(
            "12.02.01" in str(e.get("ep_id", "")) and (
                "24" in str(e.get("requirement", "")) or "rn oversight" in str(e.get("requirement", "")).lower()
            )
            for e in eps if isinstance(e, dict)
        )
    if not found_1202_ep4:
        fails.append("no EP entry with ep_id containing 'NPG.12.02.01' and EP4 (24/7 RN oversight)")
    # must have EP NPG.12.06.01 EP1
    found_1206_ep1 = any(
        "12.06.01" in str(e.get("ep_id", ""))
        for e in eps if isinstance(e, dict)
    )
    if not found_1206_ep1:
        fails.append("no EP entry with ep_id containing 'NPG.12.06.01' (QAPI integration)")
    # effective_date 2026-01-01 somewhere in the data
    data_str = json.dumps(data)
    if "2026-01-01" not in data_str and "2026" not in data_str:
        fails.append("effective_date '2026-01-01' not found anywhere in npg12_gap_analysis.json")
    # 真值层 (D加难)：每个 EP 条目必须包含 action_required 字段
    eps_missing_action = [
        str(e.get("ep_id", "ep[%d]" % i))
        for i, e in enumerate(eps)
        if isinstance(e, dict) and not e.get("action_required")
    ]
    if eps_missing_action:
        fails.append(
            "EP entries missing action_required field: %s (all EP entries must include a concrete action)" % eps_missing_action[:3])
    _finish(fails)
main()
main()
