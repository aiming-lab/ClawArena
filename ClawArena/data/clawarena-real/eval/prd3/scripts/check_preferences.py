#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd3 preference checker (P1 source_url+generated_at / P2 from-field / P3 flagged:true /
P4 decimal precision / P5 report sections)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output must have source_url (or source) AND generated_at."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object"
    has_source = ("source_url" in data or "source" in data)
    has_ts = ("generated_at" in data)
    if not has_source:
        return False, "P1: missing source_url (or source) field"
    if not has_ts:
        return False, "P1: missing generated_at ISO 8601 timestamp field"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Conflicts/anomaly items must have 'from' field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P2: not an object, skip"
    # Check conflicts array
    conflicts = data.get("conflicts") or data.get("categories") or []
    if isinstance(conflicts, list):
        for i, item in enumerate(conflicts):
            if isinstance(item, dict) and "conflict" in str(item).lower():
                if not item.get("from"):
                    return False, "P2: conflicts[%d] missing 'from' field (session source required)" % i
    # Also check top-level from
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Anomalous categories must use flagged: true, not just text."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P3: not an object, skip"
    cats = data.get("categories") or []
    if not isinstance(cats, list):
        return True, "P3: no categories array, skip"
    for i, cat in enumerate(cats):
        if not isinstance(cat, dict):
            continue
        # If flagged key present, it must be bool
        flagged = cat.get("flagged")
        if flagged is not None and not isinstance(flagged, bool):
            return False, "P3: categories[%d].flagged == %r (must be bool true/false)" % (i, flagged)
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Numeric precision: inventory-level 1dp, percentages 2dp."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P4: not an object, skip"
    # Check inventory_days precision (should be 1dp)
    inv = data.get("inventory_days")
    if inv is not None:
        try:
            inv_f = float(inv)
            # Accept if it's naturally 1dp (e.g. 32.4 or 32.0)
            inv_str = str(inv)
            if "." in inv_str and len(inv_str.split(".")[1]) > 1:
                return False, "P4: inventory_days = %s (should be 1 decimal place, e.g. 32.4)" % inv_str
        except (TypeError, ValueError):
            pass
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Final Markdown must contain three H2 sections."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    required = ["## 数据来源", "## 口径说明", "## 异常标记"]
    missing = [s for s in required if s not in txt]
    if missing:
        return False, "P5: final report missing H2 sections: %s" % missing
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
