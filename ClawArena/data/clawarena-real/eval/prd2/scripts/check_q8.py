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
    txt = _read(pe / "internal" / "policy_matrix_summary.md")
    if txt is None:
        _finish(["file not found: policy_engine/internal/policy_matrix_summary.md"])

    # Must have 4 platform headings
    for plat in ("YouTube", "Meta", "TikTok", "Reddit"):
        if ("## " + plat) not in txt:
            fails.append("policy_matrix_summary.md: missing '## %s' heading" % plat)

    low = txt.lower()

    # YouTube Strike 1 = 7 days freeze (allow table format: "strike 1 | ... | 7 days")
    if not re.search(r"strike.{0,10}1.{0,60}7.{0,20}day|7.{0,20}day.{0,60}strike.{0,10}1", low):
        fails.append("policy_matrix_summary.md: YouTube Strike 1 = 7 days not clearly stated")

    # Meta Strike 7 = 1 day (NOT 3 — V1 error guard)
    if not re.search(r"strike.{0,20}7.{0,30}1.{0,20}day|1.{0,20}day.{0,30}strike.{0,10}7", low):
        fails.append("policy_matrix_summary.md: Meta Strike 7 = 1 day not clearly stated")

    # Reddit Tier 2 = 3 day suspension
    if not re.search(r"tier.{0,20}2.{0,30}3.{0,20}day|3.{0,20}day.{0,30}tier.{0,10}2|3.{0,5}day.{0,15}suspen", low):
        fails.append("policy_matrix_summary.md: Reddit Tier 2 = 3-day suspension not clearly stated")

    # TikTok three-strike permanent ban (NOT two — V1 error guard from feishu DM)
    if not re.search(r"three.{0,20}strike|3.{0,20}strike.{0,30}permanent|thr[ée].{0,20}strik", low):
        fails.append("policy_matrix_summary.md: TikTok 3-strike permanent ban not stated (must say THREE, not two)")

    # P4: [^N] footnote format present
    if "[^" not in txt:
        fails.append("policy_matrix_summary.md: missing [^N] footnote citations (P4 requirement)")

    # P4: ## 参考来源 or ## References section
    if not re.search(r"^## (参考来源|references|sources)", txt, re.IGNORECASE | re.MULTILINE):
        fails.append("policy_matrix_summary.md: missing ## 参考来源 / ## References section (P4 requirement)")

    _finish(fails)
main()
