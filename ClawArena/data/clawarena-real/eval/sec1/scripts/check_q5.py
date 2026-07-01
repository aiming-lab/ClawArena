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
    txt = _read(ws / "work" / "workaround_plan.md")
    if txt is None:
        _finish(["file not found: work/workaround_plan.md"])
    low = txt.lower()
    # LoginGraceTime 0
    if "logingraceTime 0" not in txt and "LoginGraceTime 0" not in txt:
        # case-insensitive check
        if "logingraceTime 0".lower() not in low:
            fails.append("workaround_plan.md missing LoginGraceTime 0 directive")
    # A: DoS risk warning must be explicit — must mention unauthenticated connections not timing out
    if not re.search(r"dos|denial.of.service", low):
        fails.append("workaround_plan.md missing DoS risk warning (must mention denial-of-service risk)")
    if not re.search(r"unauthenticated|未认证|未经认证", low):
        fails.append("workaround_plan.md DoS warning must mention that unauthenticated connections will not time out")
    # systemctl restart sshd (exact command required)
    if "systemctl restart sshd" not in txt:
        fails.append("workaround_plan.md missing 'systemctl restart sshd' command")
    # D: document must have 3-section structure: header, risk/warning section, steps section
    # Check for a header/ticket section (## header or ticket-like metadata)
    has_header = bool(re.search(r"^#+\s+|工单|ticket|incident|header", low, re.MULTILINE))
    if not has_header:
        fails.append("workaround_plan.md must be formatted as an incident response ticket with a header section")
    # Check for steps section (numbered steps or steps header)
    has_steps = bool(re.search(r"step|步骤|实施|implement|procedure|^1\.", low, re.MULTILINE))
    if not has_steps:
        fails.append("workaround_plan.md must include a steps/procedure section with implementation instructions")
    # V6: must NOT actively set LoginGraceTime to 30 (the deprecated value)
    import re as _re
    for line in txt.splitlines():
        ll = line.lower()
        if _re.search(r"logingraceTime\s+30", ll):
            # If this line also mentions deprecated/archive/wrong/draft/old, allow it
            if not _re.search(r"deprecat|archiv|wrong|draft|old|旧|废弃|已废|不可用|错误", ll):
                fails.append("workaround_plan.md has active LoginGraceTime 30 recommendation (correct value is 0, not 30)")
    _finish(fails)
main()
