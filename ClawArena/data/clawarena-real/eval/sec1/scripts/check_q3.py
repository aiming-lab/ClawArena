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
    txt = _read(ws / "work" / "cvss_breakdown.md")
    if txt is None:
        _finish(["file not found: work/cvss_breakdown.md"])
    # V9: verbatim vector
    if "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H" not in txt:
        fails.append("cvss_breakdown.md missing verbatim CVSS vector string")
    # V8: each metric code present
    for code in ("AV:N","AC:H","PR:N","UI:N","S:U","C:H","I:H","A:H"):
        if code not in txt:
            fails.append("cvss_breakdown.md missing metric code %r" % code)
    # score 8.1 mentioned (exact value from NVD)
    if "8.1" not in txt:
        fails.append("cvss_breakdown.md does not mention score 8.1")
    low = txt.lower()
    # D: AV:N must explain Network attack vector
    if "network" not in low:
        fails.append("cvss_breakdown.md missing AV:N meaning (Attack Vector: Network)")
    # D: AC:H must explain High complexity (race condition or signal)
    if "high" not in low:
        fails.append("cvss_breakdown.md missing AC:H meaning (Attack Complexity: High)")
    # D: PR:N must explain None privileges
    if "none" not in low and "no priv" not in low and "no auth" not in low and "unauthenticated" not in low:
        fails.append("cvss_breakdown.md missing PR:N meaning (Privileges Required: None / unauthenticated)")
    # D: S:U must explain Unchanged scope
    if "unchanged" not in low and "scope" not in low:
        fails.append("cvss_breakdown.md missing S:U meaning (Scope: Unchanged)")
    # D: must reference the cvss worksheet or explain why AC:H results in score 8.1 (not 9.8)
    # We require the document to explain that AC:H (not AC:L) reduces the score
    if "ac:h" not in low and "attack complexity" not in low:
        fails.append("cvss_breakdown.md must explain AC:H (Attack Complexity: High) as read from the CVSS worksheet")
    # D: each impact dimension (C:H, I:H, A:H) must be explained
    for metric, keyword in [("C:H", ["confidentiality", "机密"]),
                             ("I:H", ["integrity", "完整"]),
                             ("A:H", ["availability", "可用"])]:
        found = any(kw in low for kw in keyword)
        if not found:
            fails.append("cvss_breakdown.md missing %s meaning (must explain impact on %s)" % (metric, keyword[0]))
    # D: must cite the exact Exploitability sub-score numeric value (2.22 or 2.220) from the CVSS worksheet
    # The briefing slide used 1.82 — that is incorrect. Authoritative: assets/compliance/cvss_calculation_worksheet.md
    has_exploit_val = ("2.22" in txt or "2.220" in txt)
    if not has_exploit_val:
        fails.append("cvss_breakdown.md must state the exact Exploitability sub-score 2.22 (or 2.220) from assets/compliance/cvss_calculation_worksheet.md — do not use the briefing slide value of 1.82")
    # D: must also cite ISS=0.915 (from the worksheet)
    has_iss_val = ("0.915" in txt)
    if not has_iss_val:
        fails.append("cvss_breakdown.md must state the ISS sub-score 0.915 from assets/compliance/cvss_calculation_worksheet.md")
    _finish(fails)
main()
