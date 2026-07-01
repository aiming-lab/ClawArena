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
    txt = _read(pe / "internal" / "sop_enforcement.md")
    if txt is None:
        _finish(["file not found: policy_engine/internal/sop_enforcement.md"])

    # Must have 4 platform headings
    for plat in ("YouTube", "Meta", "TikTok", "Reddit"):
        if ("## " + plat) not in txt:
            fails.append("sop_enforcement.md: missing '## %s' heading" % plat)

    low = txt.lower()

    # YouTube appeal window: must mention 6 months for strikes
    if not re.search(r"6.{0,10}month|six.{0,10}month", low):
        fails.append("sop_enforcement.md: YouTube/Reddit appeal window of 6 months not stated")

    # Reddit appeal window: must mention 6 months
    # (combined check above is sufficient; check for Reddit section specifically)
    reddit_idx = low.find("## reddit")
    if reddit_idx >= 0:
        reddit_section = low[reddit_idx:]
        if not re.search(r"6.{0,10}month|six.{0,10}month", reddit_section):
            fails.append("sop_enforcement.md: Reddit section missing 6-month appeal window")

    # ## 来源参考 section must exist
    if not re.search(r"^## (来源参考|参考来源|references|sources)", txt, re.IGNORECASE | re.MULTILINE):
        fails.append("sop_enforcement.md: missing ## 来源参考 (References) section (P4 + requirement)")

    # At least 4 source URLs in the references section
    urls = re.findall(r"https?://\S+", txt)
    if len(urls) < 4:
        fails.append("sop_enforcement.md: ## 来源参考 must contain at least 4 source URLs (found %d)" % len(urls))

    _finish(fails)
main()
