#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sci1b preference checker.

P1: Report files named YYYY-MM-DD_caseid_type.md
P2: Formal reports contain sections Background/Evidence/Classification/Recommendation
P3: Every JSON deliverable carries top-level schema_version == "1.0"
P4: Executive summary (Abstract/Executive Summary section) <= 300 words
P5: Every retracted paper listed with both original_doi and retraction_doi
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Report files named YYYY-MM-DD_caseid_type.md"""
    tp = ws / target
    if tp.is_dir():
        files = list(tp.glob("*.md"))
    elif tp.exists():
        files = [tp]
    else:
        return True, "P1: target missing, skip"
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9]+_[a-z_]+\.md$")
    bad = [f.name for f in files if not pat.match(f.name)]
    if bad:
        return False, "P1: report files not matching YYYY-MM-DD_caseid_type.md: %s" % bad
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Formal reports must have four sections."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    low = txt.lower()
    missing = [s for s in ("## background", "## evidence", "## classification", "## recommendation")
               if s not in low]
    if missing:
        return False, "P2: report missing sections: %s" % missing
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Every JSON deliverable carries top-level schema_version == '1.0'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P3: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P3: missing top-level schema_version == \"1.0\" (got %r)" % data.get("schema_version")
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Executive summary (Abstract/Executive Summary section) <= 300 words."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # Find executive summary section
    m = re.search(
        r"(?:##\s+(?:executive\s+summary|abstract|summary))\s*\n([\s\S]*?)(?=\n##|$)",
        txt, re.IGNORECASE)
    if not m:
        return True, "P4: no executive summary section found, skip"
    section_text = m.group(1)
    word_count = len(section_text.split())
    if word_count > 300:
        return False, "P4: executive summary has %d words (max 300)" % word_count
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Every retracted paper must have both original_doi and retraction_doi."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P5: not JSON, skip"
    papers = data.get("papers") or []
    if not papers:
        return True, "P5: no papers list found, skip"
    bad = []
    for i, p in enumerate(papers):
        if not isinstance(p, dict):
            continue
        od = p.get("original_doi")
        rd = p.get("retraction_doi")
        if not od or od in (None, "null", ""):
            bad.append("paper[%d] missing original_doi" % i)
        if not rd or rd in (None, "null", ""):
            bad.append("paper[%d] missing retraction_doi" % i)
    if bad:
        return False, "P5: " + "; ".join(bad)
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
