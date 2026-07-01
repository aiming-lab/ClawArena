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

    # Find the violation stats file — must follow P5 naming convention
    reports_dir = pe / "reports"
    # Accept: violation_stats_latest.json or violation_stats_YYYY-MM.json
    import re as _re
    candidates = list(reports_dir.glob("violation_stats*.json"))
    if not candidates:
        _finish(["reports/ dir missing violation_stats*.json file (must follow P5 naming: violation_stats_latest.json or violation_stats_YYYY-MM.json)"])

    # Also reject bare 'violation_stats.json' (P5 violation)
    bare = reports_dir / "violation_stats.json"
    if bare.exists() and not (reports_dir / "violation_stats_latest.json").exists():
        # Bare name without date/latest suffix
        has_good = any(f.name != "violation_stats.json" for f in candidates)
        if not has_good:
            fails.append("violation_stats.json: P5 violation — must use violation_stats_latest.json or violation_stats_YYYY-MM.json naming")

    # Use the best-named candidate
    good = [f for f in candidates if f.name != "violation_stats.json"]
    target = good[0] if good else candidates[0]

    data, err = _load_json(target)
    if err: _finish([err])

    # Must have platform data for all 4 platforms
    platforms = data.get("platforms") or data.get("by_platform") or {}
    if not isinstance(platforms, dict):
        # Try looking for platform keys at top level
        plat_keys = {"youtube", "meta", "tiktok", "reddit"}
        platforms = {k: v for k, v in data.items() if k in plat_keys}

    for plat in ("youtube", "meta", "tiktok", "reddit"):
        if plat not in platforms:
            fails.append("violation stats: missing '%s' platform data" % plat)

    # Each platform must have a total_count
    for plat, plat_data in platforms.items():
        if plat not in ("youtube", "meta", "tiktok", "reddit"):
            continue
        if isinstance(plat_data, dict):
            tc = plat_data.get("total_count") or plat_data.get("total") or plat_data.get("count")
            if tc is None:
                fails.append("violation stats: platform '%s' missing total_count field" % plat)

    _finish(fails)
main()
