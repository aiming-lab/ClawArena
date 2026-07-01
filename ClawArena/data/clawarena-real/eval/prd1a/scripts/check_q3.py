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
    data, err = _load_json(ws / "reports" / "evidence_assessment_q3.json")
    if err: _finish([err])
    items = data.get("claims") if isinstance(data, dict) else None
    if items is None and isinstance(data, list):
        items = data
    if not isinstance(items, list) or len(items) == 0:
        _finish(["evidence_assessment_q3.json claims array missing or empty"])
    for entry in items:
        if not isinstance(entry, dict): continue
        ev = str(entry.get("evidence_type", "")).lower()
        std = entry.get("meets_ftc_standard")
        # In vitro studies, animal studies, pilot studies must NOT meet standard
        if any(x in ev for x in ("in vitro", "animal", "pilot")):
            if std is True or str(std).lower() == "true":
                fails.append("claim with evidence_type '%s' must have meets_ftc_standard: false per FTC guidance" % ev[:50])
        # RCT claims can meet standard
        if "rct" in ev or "randomized" in ev:
            pass  # acceptable either way for this check
    # At least one entry must be false (in vitro Bi-07 evidence)
    has_false = any(
        e.get("meets_ftc_standard") is False or str(e.get("meets_ftc_standard")).lower() == "false"
        for e in items if isinstance(e, dict)
    )
    if not has_false:
        fails.append("at least one claim must have meets_ftc_standard: false (in vitro/animal/pilot evidence is insufficient per FTC)")
    # At least one entry must be true (LGG has 3 RCTs)
    has_true = any(
        e.get("meets_ftc_standard") is True or str(e.get("meets_ftc_standard")).lower() == "true"
        for e in items if isinstance(e, dict)
    )
    if not has_true:
        fails.append("at least one claim must have meets_ftc_standard: true (LGG has adequate RCT evidence)")
    _finish(fails)
main()
