#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    txt = _read(ws / "templates" / "disclosure_script_q9.md")
    if txt is None:
        _finish(["file not found: templates/disclosure_script_q9.md"])
    low = txt.lower()
    # Must have #ad or Ad: at beginning of post in written variant
    has_ad_beginning = (
        re.search(r"(#ad|ad:).{0,40}(beginning|start|first|top)", low) or
        re.search(r"(beginning|start|first|top).{0,60}(#ad|ad:)", low)
    )
    if not has_ad_beginning:
        if "#ad" not in low and "ad:" not in low:
            fails.append("written disclosure variant must include '#ad' or 'Ad:' placement at beginning of post")
    # hashtag-only variant must be labeled insufficient
    has_hashtag_insufficient = re.search(
        r"(hashtag.{0,30}insuffic|insuffic.{0,30}hashtag|hashtag.{0,30}inadequat|inadequat.{0,30}hashtag)", low
    )
    if not has_hashtag_insufficient:
        if "insufficient" not in low and "inadequat" not in low:
            fails.append("hashtag-only variant must be explicitly labeled as 'insufficient per FTC guidance'")
    # §255.5 must be cited
    if "255.5" not in txt:
        fails.append("document must cite 16 CFR §255.5")
    # The §255.5 'clear and conspicuous' standard must be quoted verbatim
    # Per regulatory/ftc_endorsement_guides_2023.md: "difficult to miss and be easily understandable by ordinary consumers"
    if "difficult to miss" not in low:
        fails.append(
            "document must quote the §255.5 'clear and conspicuous' standard verbatim: "
            "'difficult to miss and be easily understandable by ordinary consumers' "
            "(from 16 CFR §255.5 Endorsement Guides 2023)"
        )
    # Effective date July 26, 2023
    if "july 26, 2023" not in low and "jul 26, 2023" not in low and "2023-07-26" not in txt and "july 26" not in low:
        fails.append("must cite the 16 CFR Part 255 effective date: July 26, 2023")
    # Must have H1/H2/H3 heading structure per P3 requirement
    h1 = re.findall(r"^# [^#]", txt, re.MULTILINE)
    h2 = re.findall(r"^## [^#]", txt, re.MULTILINE)
    h3 = re.findall(r"^### [^#]", txt, re.MULTILINE)
    if not h1:
        fails.append("document must have an H1 heading (# ...) as document title (P3)")
    if not h2:
        fails.append("document must have H2 headings (## ...) for script categories (P3)")
    if not h3:
        fails.append("document must have H3 headings (### ...) for specific variants (P3)")
    _finish(fails)
main()
