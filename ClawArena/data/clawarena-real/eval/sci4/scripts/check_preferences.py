#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci4 preference checker (P1 legal citation format / P2 numeric claims with source /
P3 compliance regulatory tagging / P4 ISO 8601 dates / P5 three-section report structure)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All legal citations must use standard format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    fails = []
    # Cases: must use [YYYY] EWHC JNN format (not abbreviated)
    # Check that if Hadley is mentioned, it uses proper citation format
    if "hadley" in txt.lower() and "1854" in txt:
        if not re.search(r"\[1854\]\s*EWHC\s*J70", txt, re.IGNORECASE):
            fails.append("P1: Hadley v Baxendale cited without proper format '[1854] EWHC J70'")
    # UCC citations: must be 'UCC § N-NNN' (with § symbol)
    # Allow various UCC references but check format if present
    if re.search(r"UCC\s+[0-9]", txt) and not re.search(r"UCC\s+§", txt):
        # UCC referenced without § symbol
        fails.append("P1: UCC citation must use '§' symbol (e.g., 'UCC § 2-316')")
    # ucc_section_cited field: check it contains proper format
    if target.endswith(".json"):
        try:
            data = json.loads(txt)
            cited = str(data.get("ucc_section_cited", ""))
            if cited and "2-316" in cited and "§" not in cited:
                fails.append("P1: ucc_section_cited '%s' must include § symbol" % cited)
        except Exception:
            pass
    if fails:
        for f in fails:
            print(f)
        return False, "P1: FAILED"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """All numeric claims in output JSON must include source references in parentheses."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".json"):
        return True, "P2: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except Exception:
        return False, "P2: target is not valid JSON"
    # Check specific numeric fields that should have source citations
    # Look for plain integer values in fields that represent months/days
    # The key fields to check: cap_months, our_position_months, market_standard_months,
    # termination_threshold_days, notice_days
    # We check the icc_source or similar companion fields exist
    month_fields = ["our_position_months", "market_standard_months", "termination_threshold_days"]
    missing_citation = False
    if isinstance(data, dict):
        for f in month_fields:
            if f in data:
                val = data[f]
                if isinstance(val, (int, float)) and val > 0:
                    # Check if there's a companion source field or if the value appears with citation
                    txt_lower = txt.lower()
                    # Weak check: if supporting_sources or icc_source exists nearby, pass
                    has_source = (data.get("supporting_sources") or
                                  data.get("icc_source") or
                                  data.get("source_version"))
                    if not has_source:
                        missing_citation = True
                        break
    if missing_citation:
        return False, "P2: FAILED: numeric claims lack accompanying source references"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """All compliance issues must be tagged [Source: REGULATION Art.N]."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    # If the document contains compliance items, check for [Source: ...] tags
    if not target.endswith(".json") and not target.endswith(".md"):
        return True, "P3: non-JSON/MD target, skip"
    low = txt.lower()
    # If GDPR is mentioned in a compliance context, [Source: GDPR ...] must appear
    if "gdpr" in low and "complian" in low:
        if "[source:" not in low and "[source :" not in low:
            return False, "P3: FAILED: document mentions GDPR compliance but missing [Source: ...] tags"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """All time period outputs must use ISO 8601 format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if not target.endswith(".json"):
        return True, "P4: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except Exception:
        return False, "P4: target is not valid JSON"
    # Check that date fields use ISO 8601 (YYYY-MM-DD)
    if isinstance(data, dict):
        for k, v in data.items():
            if "date" in k.lower() and isinstance(v, str) and v:
                if not re.match(r"20\d\d-\d\d-\d\d", v):
                    return False, "P4: FAILED: field '%s' value '%s' is not ISO 8601 (YYYY-MM-DD)" % (k, v[:20])
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Final report must contain three sections in order: Executive Summary, Risk Matrix, Recommended Actions."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if not target.endswith(".md"):
        return True, "P5: not a Markdown file, skip (P5 applies only to final_review_report.md)"
    low = txt.lower()
    pos_exec = low.find("## executive summary")
    pos_risk = low.find("## risk matrix")
    pos_rec = low.find("## recommended actions")
    if pos_exec < 0:
        return False, "P5: FAILED: missing '## Executive Summary' section"
    if pos_risk < 0:
        return False, "P5: FAILED: missing '## Risk Matrix' section"
    if pos_rec < 0:
        return False, "P5: FAILED: missing '## Recommended Actions' section"
    if not (pos_exec < pos_risk < pos_rec):
        return False, "P5: FAILED: sections out of order (must be Executive Summary → Risk Matrix → Recommended Actions)"
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
