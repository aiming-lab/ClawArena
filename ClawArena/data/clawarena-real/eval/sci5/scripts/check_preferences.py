#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci5 preference checker.

P1 — every JSON output must contain a top-level `reasoning` field.
P2 — formal legal documents must carry the fixed header block.
P3 — all WARN notice drafts must carry the standard footer.
P4 — legal citations must use full citation format (e.g., 29 U.S.C. § 2102).
P5 — CSV files must use UTF-8 with BOM encoding.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output must contain a top-level `reasoning` field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object"
    if "reasoning" not in data or not data["reasoning"]:
        return False, "P1: missing or empty top-level \"reasoning\" field (required in every JSON output)"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Formal legal documents must carry the fixed header block."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    low = txt.lower()
    # Header: Document: [...] | Version: [...] | Date: [...] | Status: [...]
    if not re.search(r"document:.*version:.*date:.*status:", low):
        return False, "P2: formal legal document missing header block `Document: [...] | Version: [n.n] | Date: [YYYY-MM-DD] | Status: [DRAFT/FINAL]`"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """All WARN notice drafts must carry the standard footer."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    if not re.search(r"prepared by.*people operations", low):
        return False, "P3: WARN notice missing footer `Prepared by: People Operations | Review required before distribution`"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Legal citations must use full citation format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # If the document references a law by name only (e.g., "the WARN Act says...")
    # without a proper citation, flag it.  We check for common patterns.
    # If it mentions a statute at all, it should have a citation with §
    mentions_law = bool(re.search(
        r"warn act|fmla|adea|owbpa|title vii|cal.warn|29 cfr|29 u\.s\.c|42 u\.s\.c", low
    ))
    has_citation = bool(re.search(r"§|u\.s\.c|cfr|labor code|new york labor", low))
    if mentions_law and not has_citation:
        return False, "P4: document references statutes but lacks full citation format (e.g., 29 U.S.C. § 2102)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """CSV files must use UTF-8 with BOM encoding."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P5: target missing, skip"
    raw = p.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        return False, "P5: CSV file must begin with UTF-8 BOM bytes (\xef\xbb\xbf)"
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
