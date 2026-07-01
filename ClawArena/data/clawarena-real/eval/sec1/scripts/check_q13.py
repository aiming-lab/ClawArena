#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv, os
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
    txt = _read(ws / "work" / "executive_report.md")
    if txt is None:
        _finish(["file not found: work/executive_report.md"])
    low = txt.lower()
    # V9: verbatim CVE ID
    if "CVE-2024-6387" not in txt:
        fails.append("executive_report.md missing CVE-2024-6387")
    # A: exact CVSS score 8.1
    if "8.1" not in txt:
        fails.append("executive_report.md missing CVSS score 8.1")
    # RHSA-2024:4312
    if "RHSA-2024:4312" not in txt:
        fails.append("executive_report.md missing RHSA-2024:4312")
    # errata date 2024-07-03
    if "2024-07-03" not in txt:
        fails.append("executive_report.md missing errata release date 2024-07-03 (RHSA-2024:4312 was published on this date)")
    # patched version 9.8p1
    if "9.8p1" not in txt:
        fails.append("executive_report.md missing patched version 9.8p1")
    # B: current workaround must be MaxStartups (per Update 2 — LoginGraceTime 0 was superseded)
    if "MaxStartups" not in txt and "maxstartups" not in low:
        fails.append("executive_report.md missing current workaround MaxStartups (per Update 2 — LoginGraceTime 0 was revoked by SC-2024-0708-01)")
    # A: TL;DR section present — Alice Wang's internal style guide caps board-facing TL;DRs at 60 words
    # (The CTO Carol's email references '≤200 words' for the full report; but the TL;DR paragraph itself
    # must be ≤60 words per the internal security team style guide — a separate constraint not surfaced in the
    # session email thread. Read assets/templates/ or SOUL.md for Alice's standing guidance.)
    tldr_match = re.search(r"##?\s*TL;?DR(.+?)(?=^##|\Z)", txt, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not tldr_match:
        fails.append("executive_report.md missing standalone TL;DR section (CTO requirement)")
    else:
        tldr_text = tldr_match.group(1).strip()
        word_count = len(tldr_text.split())
        if word_count > 60:
            fails.append("TL;DR section has %d words (must be ≤60 words per Alice Wang's style guide for board-facing TL;DR paragraphs — the CTO's '200 words' refers to the full executive summary, not just the TL;DR)" % word_count)
    _finish(fails)
main()
