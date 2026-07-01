#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd1a preference checker (P1-P5).

P1: Every JSON output must carry top-level schema_version == "1.0"
P2: Every compliance issue entry must carry ftc_citation in "16 CFR §XXX.X" format
P3: Markdown reports use H1=document title, H2=claim category, H3=specific provision
P4: Prohibited terms table must include severity column (high/medium/low)
P5: All files under final/ must follow {document_type}_final_YYYYMMDD.{ext} naming
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output file carries a top-level schema_version == '1.0'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \"1.0\" (got %r)" % data.get("schema_version")
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Every compliance issue entry must carry ftc_citation in '16 CFR §XXX.X' format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P2: not JSON, skip"
    # Get items — could be at root list or under 'issues'/'claims'/'entries' key
    items = None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ("issues", "claims", "entries", "items"):
            if isinstance(data.get(k), list):
                items = data[k]; break
    if not items:
        return True, "P2: no items array found, skip"
    for i, entry in enumerate(items):
        if not isinstance(entry, dict): continue
        cit = str(entry.get("ftc_citation", ""))
        if not cit:
            return False, "P2: item[%d] missing ftc_citation field" % i
        if not re.search(r"16 CFR §\d", cit):
            return False, "P2: item[%d] ftc_citation '%s' does not match '16 CFR §XXX.X' format" % (i, cit[:40])
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Markdown reports: H1=document title, H2=claim category, H3=specific provision."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    if not target.endswith(".md"):
        return True, "P3: not a Markdown file, skip"
    # Must have at least one H1 (#) heading
    if not re.search(r"^#\s+\S", txt, re.MULTILINE):
        return False, "P3: Markdown file missing H1 heading (must be '# Document Title')"
    # Must have at least one H2 (##) heading for claim category
    if not re.search(r"^##\s+\S", txt, re.MULTILINE):
        return False, "P3: Markdown file missing H2 section heading (must be '## Claim Category')"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Prohibited terms table must include severity column."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if not target.endswith(".md"):
        return True, "P4: not a Markdown file, skip"
    # Only check if the file has a table
    if "|" not in txt:
        return True, "P4: no Markdown table found, skip"
    if "severity" not in txt.lower():
        return False, "P4: Markdown table missing 'severity' column (must be high/medium/low)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Files under final/ must follow {document_type}_final_YYYYMMDD.{ext} naming."""
    p = Path(target)
    if "final" not in str(p.parent):
        return True, "P5: not under final/, skip"
    name = p.name
    pat = re.compile(r"^[a-z_]+_final_\d{8}\.[a-z]+$")
    if not pat.match(name):
        return False, "P5: file name '%s' does not match {document_type}_final_YYYYMMDD.{ext} pattern" % name
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="reports/")
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
