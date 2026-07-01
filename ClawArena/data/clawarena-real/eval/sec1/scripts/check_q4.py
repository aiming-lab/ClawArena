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
    txt = _read(ws / "work" / "regression_analysis.md")
    if txt is None:
        _finish(["file not found: work/regression_analysis.md"])
    # A: full verbatim commit hash (not just abbreviated)
    if "752250caabda3dd24635503c4cd689b32a650794" not in txt and "752250c" not in txt:
        fails.append("regression_analysis.md missing commit hash (need at least abbreviated 752250c)")
    # DO_LOG_SAFE_IN_SIGHAND macro
    if "DO_LOG_SAFE_IN_SIGHAND" not in txt:
        fails.append("regression_analysis.md missing macro DO_LOG_SAFE_IN_SIGHAND")
    # CVE-2006-5051 reference
    if "CVE-2006-5051" not in txt:
        fails.append("regression_analysis.md missing CVE-2006-5051 (prior vulnerability)")
    # A: must cite the exact date "2020-10-16" (not just year 2020)
    if "2020-10-16" not in txt:
        fails.append("regression_analysis.md must contain exact date 2020-10-16 (from oss-security disclosure and GitHub commit metadata — not just the year)")
    # V5: must NOT use bot date 2021-03 without the correct date
    if "2021-03" in txt and "2020-10-16" not in txt:
        fails.append("regression_analysis.md uses bot-error date 2021-03 instead of correct 2020-10-16")
    # A: must explain WHY the regression was introduced (syslog / signal handler)
    low = txt.lower()
    if "syslog" not in low and "signal" not in low:
        fails.append("regression_analysis.md must explain the technical mechanism: syslog() call in signal handler (the reason DO_LOG_SAFE_IN_SIGHAND was needed)")
    # D: must explicitly state the commit AUTHOR (Damien Miller) from the oss-security disclosure/GitHub commit
    if "damien" not in low and "djm" not in low:
        fails.append("regression_analysis.md must identify the commit author Damien Miller (djm@mindrot.org) from the GitHub commit metadata in assets/advisories/openwall_disclosure.txt")
    _finish(fails)
main()
