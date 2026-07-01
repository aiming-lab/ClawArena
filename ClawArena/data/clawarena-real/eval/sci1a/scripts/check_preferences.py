#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci1a preference checker:
P1: report files named YYYY-MM-DD_caseid_type.md
P2: formal reports contain Background/Evidence/Classification/Recommendation
P3: every JSON deliverable carries top-level schema_version == "1.0"
P4: Abstract/Executive Summary <= 300 words
P5: each retracted paper lists both original_doi and retraction_doi separately
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Report file name must match YYYY-MM-DD_caseid_type.md."""
    tp = ws / target
    fname = tp.name
    # Pattern: YYYY-MM-DD_<rest>.md where rest is alphanumeric/underscore
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9_]+\.md$")
    if not pat.match(fname):
        return False, "P1: filename '%s' does not match YYYY-MM-DD_caseid_type.md" % fname
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Formal report must contain all four sections."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    low = txt.lower()
    missing = [s for s in ("background", "evidence", "classification", "recommendation")
               if s not in low]
    if missing:
        return False, "P2: missing sections %s (all four required)" % missing
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
    """Abstract / Executive Summary section must not exceed 300 words."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # Find abstract/executive summary section
    patterns = [
        r"(?:^##?\s+(?:abstract|executive summary).*?$)(.*?)(?=^##?\s|\Z)",
    ]
    found = False
    for pat in patterns:
        m = re.search(pat, low, re.MULTILINE | re.DOTALL)
        if m:
            found = True
            abstract_text = m.group(1).strip()
            words = len(abstract_text.split())
            if words > 300:
                return False, "P4: Abstract/Executive Summary has %d words (must be <= 300)" % words
    if not found:
        # If no abstract section, check if report begins with one
        lines = txt.splitlines()
        # Check first 20 lines for abstract-like heading
        for i, line in enumerate(lines[:20]):
            if re.match(r"^##?\s+(abstract|executive\s+summary)", line.lower()):
                found = True
                break
    # Skip if no abstract section found (no penalty for missing one at this check level)
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Each retracted paper must list both original_doi and retraction_doi separately."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    low = txt.lower()
    # Check: if "retraction" appears in the file, both original_doi and retraction_doi fields/labels should appear
    if "retraction" in low:
        has_original = "original_doi" in low or "original doi" in low
        has_retraction_doi = "retraction_doi" in low or "retraction doi" in low
        if not (has_original and has_retraction_doi):
            return False, "P5: file mentions retraction but does not list both 'original_doi' and 'retraction_doi' separately"
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
