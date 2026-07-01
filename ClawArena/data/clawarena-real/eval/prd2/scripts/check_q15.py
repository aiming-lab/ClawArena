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
    data, err = _load_json(pe / "internal" / "regulatory_addendum.json")
    if err: _finish([err])

    # regulation = 'EU_DSA'
    reg = str(data.get("regulation") or "")
    if "EU_DSA" not in reg and "EU DSA" not in reg and "DSA" not in reg:
        fails.append("regulatory_addendum: regulation field must contain 'EU_DSA' (got %r)" % reg)

    # affected_platforms: must contain youtube, meta, tiktok
    affected = [str(p).lower() for p in (data.get("affected_platforms") or [])]
    for plat in ("youtube", "meta", "tiktok"):
        if plat not in affected:
            fails.append("regulatory_addendum: affected_platforms must include '%s'" % plat)

    # reddit must NOT be in affected_platforms (supersede: Reddit is not VLOP)
    if "reddit" in affected:
        fails.append("regulatory_addendum: reddit must NOT be in affected_platforms (final email confirms Reddit is not a VLOP; supersedes early draft)")

    # article_reference: must include 'Art. 34' and 'Art. 35' (V9 verbatim)
    articles = [str(a) for a in (data.get("article_reference") or [])]
    for art in ("Art. 34", "Art. 35"):
        if art not in articles:
            fails.append("regulatory_addendum: article_reference must contain verbatim '%s' (got %s)" % (art, articles))

    # non_affected_platforms: must contain reddit
    non_affected = [str(p).lower() for p in (data.get("non_affected_platforms") or [])]
    if "reddit" not in non_affected:
        fails.append("regulatory_addendum: non_affected_platforms must include 'reddit'")

    # vlop_threshold_eu_users must be exactly 45000000 (the DSA threshold)
    threshold = data.get("vlop_threshold_eu_users")
    try:
        if int(threshold) != 45000000:
            fails.append(
                "regulatory_addendum: vlop_threshold_eu_users must be exactly 45000000 "
                "(the DSA VLOP designation threshold; got %r)" % threshold
            )
    except (TypeError, ValueError):
        fails.append(
            "regulatory_addendum: vlop_threshold_eu_users must be integer 45000000 "
            "(from DSA Article definition; got %r)" % threshold
        )

    _finish(fails)
main()
