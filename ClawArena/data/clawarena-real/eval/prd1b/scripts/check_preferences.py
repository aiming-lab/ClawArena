#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd1b preference checker (P1 schema_version / P2 ftc_citation format /
P3 Markdown heading hierarchy / P4 severity column / P5 final/ naming convention)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output file carries a top-level schema_version == "1.0"."""
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
        return False, "P2: target is not valid JSON"
    # Find all objects in the structure that look like issue/template entries
    entries = []
    def _collect(obj):
        if isinstance(obj, dict):
            entries.append(obj)
            for v in obj.values():
                _collect(v)
        elif isinstance(obj, list):
            for item in obj:
                _collect(item)
    _collect(data)
    issue_like = [e for e in entries if any(k in e for k in
        ("issue_id", "template_id", "claim_text", "ingredient", "recommendation"))]
    if not issue_like:
        return True, "P2: no compliance issue entries found, skip"
    missing_citation = []
    for e in issue_like:
        cit = e.get("ftc_citation","")
        if cit and not re.match(r"16 CFR §\d", str(cit)):
            missing_citation.append(str(cit)[:20])
        elif not cit:
            missing_citation.append("<empty>")
    if missing_citation:
        return False, "P2: ftc_citation missing or not in '16 CFR §XXX.X' format: %s" % missing_citation[:3]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Markdown heading hierarchy: H1=document title, H2=category, H3=provision."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    h1 = re.findall(r"^# [^#]", txt, re.MULTILINE)
    h2 = re.findall(r"^## [^#]", txt, re.MULTILINE)
    h3 = re.findall(r"^### [^#]", txt, re.MULTILINE)
    if not h1:
        return False, "P3: no H1 heading (# ...) found in Markdown document"
    if not h2:
        return False, "P3: no H2 headings (## ...) found — document must use H2 for categories"
    if not h3:
        return False, "P3: no H3 headings (### ...) found — document must use H3 for specific provisions"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Prohibited-term replacement tables must include a severity column."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    if "severity" not in low:
        return False, "P4: prohibited-term table/section must include a 'Severity' column (high/medium/low)"
    # Must have at least one valid severity value
    if not re.search(r"\b(high|medium|low)\b", low):
        return False, "P4: severity values must be high/medium/low"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Files in final/ must follow {document_type}_final_YYYYMMDD.{ext} naming."""
    tp = ws / target
    if not tp.exists():
        return True, "P5: target missing, skip"
    fname = tp.name
    pat = re.compile(r"^[a-z_]+_final_\d{8}\.[a-z]+$")
    if not pat.match(fname):
        return False, "P5: filename '%s' must match {type}_final_YYYYMMDD.{ext} convention" % fname
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
