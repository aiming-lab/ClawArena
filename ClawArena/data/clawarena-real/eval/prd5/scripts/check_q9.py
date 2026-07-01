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
    data, err = _load_json(ws / "output" / "q9_experiment_summary.json")
    if err: _finish([err])
    # Must be a list of experiment entries
    if isinstance(data, list):
        entries = {str(e.get("exp_id", "")): e for e in data if isinstance(e, dict)}
    elif isinstance(data, dict):
        entries = {}
        for k, v in data.items():
            if isinstance(v, dict):
                entries[str(k)] = v
            elif k not in ("schema_version",):
                entries[str(k)] = {"exp_id": k, "conclusion": str(v)}
    else:
        _finish(["q9 output must be list or object"])
    # All 3 ended experiments must be present
    for eid in ("exp001", "exp002", "exp003"):
        if eid not in entries:
            fails.append("missing entry for %s" % eid)
    if fails: _finish(fails)
    # exp002 must be invalid_srm
    e002 = entries.get("exp002") or {}
    conc002 = str(e002.get("conclusion", "")).lower()
    if "srm" not in conc002 and "invalid" not in conc002 and "mismatch" not in conc002:
        fails.append("exp002 conclusion %r does not reflect SRM invalidation (must be \'invalid_srm\')" % conc002[:60])
    # exp003 must be not_significant (V4 cross-round: must reflect Q8 cleaned analysis)
    e003 = entries.get("exp003") or {}
    conc003 = str(e003.get("conclusion", "")).lower()
    if not any(kw in conc003 for kw in ("not_significant", "not significant", "insignificant", "no significant")):
        pv003 = e003.get("primary_p_value")
        try:
            pv003 = float(pv003)
            if pv003 <= 0.05:
                fails.append("exp003 conclusion or p_value must reflect not_significant (cleaned data p=0.31, not original 0.023)")
        except (TypeError, ValueError):
            fails.append("exp003 conclusion %r must reflect not_significant result (consistent with Q8 cleanup)" % conc003[:60])
    # exp003 primary_p_value must be numeric and in cleaned-data range [0.15, 0.55]
    pv003_raw = e003.get("primary_p_value")
    if pv003_raw is not None:
        try:
            pv003 = float(pv003_raw)
            if not (0.15 <= pv003 <= 0.55):
                fails.append("exp003 primary_p_value == %.4f — must be in [0.15, 0.55] reflecting cleaned data p=0.31" % pv003)
        except (TypeError, ValueError):
            fails.append("exp003 primary_p_value %r is not numeric" % pv003_raw)
    # exp001: conclusion must signal that result requires investigation (Twyman flag)
    # It must NOT conclude significant or not_significant definitively — it is flagged/unresolved
    e001 = entries.get("exp001") or {}
    conc001 = str(e001.get("conclusion", "")).lower()
    notes001 = str(e001.get("notes", "")).lower()
    combined001 = conc001 + " " + notes001
    if not any(kw in combined001 for kw in ("investigat", "twyman", "flagged", "suspicious", "unresolved", "requires")):
        fails.append(
            "exp001 conclusion/notes %r must indicate the result requires investigation "
            "(Twyman\'s Law: +45%% lift is suspicious, cannot conclude significant/not_significant yet)" % conc001[:60]
        )
    _finish(fails)
main()
