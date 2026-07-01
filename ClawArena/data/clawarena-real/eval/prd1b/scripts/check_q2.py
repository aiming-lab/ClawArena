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
    data, err = _load_json(ws / "reports" / "disclosure_check_q2.json")
    if err: _finish([err])
    templates = data.get("templates") or data.get("items") or []
    if not isinstance(templates, list) or len(templates) < 3:
        fails.append("templates array must have at least 3 entries (got %r)" % len(templates))
        _finish(fails)
    # Build lookup by template_id
    by_id = {}
    for t in templates:
        if isinstance(t, dict) and t.get("template_id"):
            by_id[str(t["template_id"]).upper()] = t
    # Template A: #ad buried in hashtags -> inadequate
    tA = by_id.get("A")
    if tA is None:
        fails.append("missing template_id='A'")
    elif tA.get("disclosure_adequate") is not False:
        fails.append("Template A: disclosure_adequate must be false (# ad buried in hashtag list is inadequate)")
    # Template B: no disclosure until end of post -> inadequate
    tB = by_id.get("B")
    if tB is None:
        fails.append("missing template_id='B'")
    elif tB.get("disclosure_adequate") is not False:
        fails.append("Template B: disclosure_adequate must be false (no upfront disclosure — compensation only revealed at end of post, violating the clear and conspicuous standard)")
    # Template C: platform Paid Partnership only -> inadequate
    tC = by_id.get("C")
    if tC is None:
        fails.append("missing template_id='C'")
    elif tC.get("disclosure_adequate") is not False:
        fails.append("Template C: disclosure_adequate must be false (platform Paid Partnership tool alone is inadequate)")
    # Template D: employee reviews without disclosure -> violation §465.3
    tD = by_id.get("D")
    if tD is None:
        fails.append("missing template_id='D'")
    else:
        if tD.get("disclosure_adequate") is not False:
            fails.append("Template D: disclosure_adequate must be false (§465.3 violation)")
        d_txt = str(tD.get("ftc_citation","")) + str(tD.get("reasoning",""))
        if "465.3" not in d_txt and "465" not in d_txt:
            fails.append("Template D: must reference §465.3 (insider review violation)")
    # Penalty per violation must be 51744 (not 45000 DECOY) and must be present in every template
    for t in templates:
        if not isinstance(t, dict): continue
        tid = str(t.get("template_id","?")).upper()
        ppv = t.get("estimated_penalty_per_violation")
        if ppv is None:
            fails.append("Template %s: missing estimated_penalty_per_violation field (must be 51744)" % tid)
        else:
            try:
                ppv_int = int(float(ppv))
                if ppv_int == 45000:
                    fails.append("Template %s: estimated_penalty_per_violation == 45000 (DECOY figure — correct value is 51744)" % tid)
                elif ppv_int != 51744:
                    fails.append("Template %s: estimated_penalty_per_violation == %d (expected 51744)" % (tid, ppv_int))
            except (TypeError, ValueError):
                pass
    # ftc_citation format check — every template must have it
    for t in templates:
        if not isinstance(t, dict): continue
        tid = str(t.get("template_id","?")).upper()
        cit = str(t.get("ftc_citation",""))
        if not cit:
            fails.append("Template %s: missing ftc_citation field" % tid)
        elif not re.match(r"16 CFR §\d", cit):
            fails.append("Template %s: ftc_citation '%s' does not match '16 CFR §XXX.X' format" % (tid, cit[:30]))
    _finish(fails)
main()
