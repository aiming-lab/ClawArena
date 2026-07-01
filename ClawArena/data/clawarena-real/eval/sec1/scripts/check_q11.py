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
    txt = _read(ws / "work" / "workaround_plan_v2.md")
    if txt is None:
        _finish(["file not found: work/workaround_plan_v2.md"])
    low = txt.lower()
    # Must contain MaxStartups 10:30:100
    if "MaxStartups 10:30:100" not in txt and "maxstartups 10:30:100" not in low:
        fails.append("workaround_plan_v2.md missing MaxStartups 10:30:100")
    # Must explicitly state LoginGraceTime 0 is superseded
    if not (re.search(r"supersed|revok|replac", low) and re.search(r"logingraceTime\s+0|logingraceTime0", low, re.IGNORECASE)):
        fails.append("workaround_plan_v2.md does not explicitly state LoginGraceTime 0 is superseded/revoked")
    # A: must reference Security Committee Decision ID SC-2024-0708-01 exactly
    if "SC-2024-0708-01" not in txt:
        fails.append("workaround_plan_v2.md missing Security Committee Decision ID SC-2024-0708-01 (from assets/advisories/security_committee_decision.md)")
    # D: must reference the definitive patch target (9.8p1 or RHSA errata) as the final goal
    if "9.8p1" not in txt and "RHSA-2024:4312" not in txt and "RHSA-2024:4340" not in txt:
        fails.append("workaround_plan_v2.md must reference the definitive patch target (OpenSSH 9.8p1 or RHSA-2024:4312 for RHEL 9)")
    # Must NOT actively recommend LoginGraceTime 0 (only mention it as superseded)
    recommend_pattern = r"(?:use|set|apply|configure|add|recommend)[^\n]{0,60}logingraceTime\s+0"
    if re.search(recommend_pattern, low) and not re.search(r"supersed|revok|no\s+longer", low):
        fails.append("workaround_plan_v2.md appears to actively recommend LoginGraceTime 0 (should only mention it as superseded)")
    _finish(fails)
main()
