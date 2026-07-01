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
    data, err = _load_json(pe / "internal" / "conflict_report.json")
    if err: _finish([err])

    conflicts = data.get("conflicts") or []
    if len(conflicts) < 3:
        fails.append("conflict_report: must have at least 3 conflict records (got %d)" % len(conflicts))

    # Each record must have required fields
    required_fields = ("source_channel", "claimed_value", "official_value", "official_url")
    for i, c in enumerate(conflicts[:5]):
        for fld in required_fields:
            if not c.get(fld):
                fails.append("conflict_report entry[%d]: missing or empty field '%s'" % (i, fld))
                break

    # Meta Strike 7 conflict must be identified
    meta_s7_found = False
    for c in conflicts:
        topic = str(c.get("topic") or c.get("field") or c.get("id") or "").lower()
        claimed = str(c.get("claimed_value") or "").lower()
        official = str(c.get("official_value") or "").lower()
        if "meta" in topic and "strike" in topic and "7" in topic:
            meta_s7_found = True
            break
        if "meta" in str(c).lower() and "strike" in str(c).lower() and (
            "3" in claimed and "1" in official or "strike_7" in str(c).lower()
        ):
            meta_s7_found = True
            break
    if not meta_s7_found:
        fails.append("conflict_report: Meta Strike 7 conflict (3 days vs 1 day) not identified")

    # YouTube appeal window conflict must be identified
    yt_appeal_found = False
    for c in conflicts:
        blob = str(c).lower()
        if "youtube" in blob and "appeal" in blob and ("3" in blob or "6" in blob):
            yt_appeal_found = True
            break
    if not yt_appeal_found:
        fails.append("conflict_report: YouTube appeal window conflict (3 months bot vs 6 months official) not identified")

    # TikTok permanent ban conflict must be identified
    tt_ban_found = False
    for c in conflicts:
        blob = str(c).lower()
        if "tiktok" in blob and ("permanent" in blob or "ban" in blob) and (
            "two" in blob or "2" in blob or "three" in blob or "3" in blob
        ):
            tt_ban_found = True
            break
    if not tt_ban_found:
        fails.append("conflict_report: TikTok permanent ban threshold conflict (2 vs 3 strikes) not identified")

    _finish(fails)
main()
