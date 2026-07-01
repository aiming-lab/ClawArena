#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []

    # YouTube index.json
    data, err = _load_json(pe / "platforms" / "youtube" / "index.json")
    if err: _finish([err])
    cats = data.get("policy_categories") or []
    if len(cats) < 5:
        fails.append("youtube index: policy_categories must have >=5 entries (got %d)" % len(cats))
    if data.get("strike_window_days") != 90:
        fails.append("youtube index: strike_window_days must be 90 (got %r)" % data.get("strike_window_days"))

    # Meta index.json
    data2, err2 = _load_json(pe / "platforms" / "meta" / "index.json")
    if err2: _finish([err2])
    pcc = data2.get("policy_category_count")
    if pcc != 27:
        fails.append("meta index: policy_category_count must be 27 (got %r)" % pcc)

    # TikTok index.json
    data3, err3 = _load_json(pe / "platforms" / "tiktok" / "index.json")
    if err3: _finish([err3])
    if "safety_civility" not in data3:
        fails.append("tiktok index: missing safety_civility field (verbatim category key required)")
    else:
        sc = data3["safety_civility"]
        if not isinstance(sc, dict):
            fails.append("tiktok index: safety_civility must be an object with q1_2025_removal_pct field")
        else:
            rpct = sc.get("q1_2025_removal_pct")
            try:
                rpct = float(rpct)
                if not (0.1127 <= rpct <= 0.1173):
                    fails.append(
                        "tiktok index: safety_civility.q1_2025_removal_pct must be ~0.115 (±2%%) "
                        "from Q1 2025 transparency report (got %.4f)" % rpct
                    )
            except (TypeError, ValueError):
                fails.append(
                    "tiktok index: safety_civility.q1_2025_removal_pct must be numeric ~0.115 "
                    "(got %r)" % rpct
                )

    # Reddit index.json
    data4, err4 = _load_json(pe / "platforms" / "reddit" / "index.json")
    if err4: _finish([err4])
    for fld in ("rule1", "rule2", "rule5"):
        if fld not in data4:
            fails.append("reddit index: missing '%s' field" % fld)
    # rule1 must contain verbatim key phrase from official NY report
    r1_text = str(data4.get("rule1") or "").lower()
    if "promote hate based on identity" not in r1_text and "incite violence" not in r1_text:
        fails.append(
            "reddit index: rule1 must contain verbatim text from official NY S895B/A6789B report "
            "('incite violence' or 'promote hate based on identity')"
        )

    _finish(fails)
main()
