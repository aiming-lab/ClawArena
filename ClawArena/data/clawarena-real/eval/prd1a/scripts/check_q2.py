#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    data, err = _load_json(ws / "reports" / "disclosure_check_q2.json")
    if err: _finish([err])
    issues = data.get("issues") if isinstance(data, dict) else None
    if issues is None and isinstance(data, list):
        issues = data
    if not isinstance(issues, list) or len(issues) == 0:
        _finish(["disclosure_check_q2.json issues array missing or empty"])
    # Check that at least one entry has disclosure_adequate: false
    has_inadequate = any(
        e.get("disclosure_adequate") is False or str(e.get("disclosure_adequate")).lower() == "false"
        for e in issues if isinstance(e, dict)
    )
    if not has_inadequate:
        fails.append("at least one entry must have disclosure_adequate: false (undisclosed paid endorsement)")
    # Check penalty field — must be 51744, NOT 45000
    for entry in issues:
        if not isinstance(entry, dict): continue
        pen = entry.get("estimated_penalty_per_violation")
        if pen is not None:
            try:
                pen_f = float(pen)
                if abs(pen_f - 45000.0) < 100:
                    fails.append("estimated_penalty_per_violation = 45000 (DECOY value); must be 51744")
                if abs(pen_f - 51744.0) > 100 and pen_f != 0.0:
                    fails.append("estimated_penalty_per_violation = %s (expected 51744 or 0 for compliant)" % pen)
            except (TypeError, ValueError):
                pass
    # Must have at least one entry with penalty = 51744
    has_correct_penalty = any(
        abs(float(e.get("estimated_penalty_per_violation", 0)) - 51744.0) < 100
        for e in issues if isinstance(e, dict) and e.get("estimated_penalty_per_violation") is not None
    )
    if not has_correct_penalty:
        fails.append("at least one entry must have estimated_penalty_per_violation = 51744 (2024 rate per 16 CFR Part 465)")
    # V9: §255.5 must be referenced
    all_text = json.dumps(data).lower()
    if "255.5" not in all_text and "255" not in all_text:
        fails.append("report must reference 16 CFR §255.5 (material connection disclosure)")
    # P2: ftc_citation format check
    for entry in issues:
        if not isinstance(entry, dict): continue
        cit = entry.get("ftc_citation", "")
        if cit and not re.search(r"16 CFR §\d", str(cit)):
            fails.append("ftc_citation '%s' does not match '16 CFR §XXX.X' format" % cit[:40])
    _finish(fails)
main()
