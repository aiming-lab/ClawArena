#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
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
    txt = _read(ws / "CHANGELOG_ENTRY.md")
    if txt is None:
        _finish(["file not found: CHANGELOG_ENTRY.md"])
    if "CVE-2024-47081" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing 'CVE-2024-47081'")
    if "2.32.4" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing fixed version '2.32.4'")
    if "get_netrc_auth" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing root cause function 'get_netrc_auth'")
    if "trust_env=False" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing workaround 'trust_env=False'")
    # P2: **Security** or **Bugfixes** header in RST style
    if "**Security**" not in txt and "**Bugfixes**" not in txt:
        fails.append("P2: CHANGELOG_ENTRY.md missing RST-style header '**Security**' or '**Bugfixes**'")
    # GHSA ID must appear (from the SECURITY_CONTEXT.md / NVD sources)
    if "GHSA-9hjg-9r4m-mvj7" not in txt:
        fails.append(
            "CHANGELOG_ENTRY.md missing GHSA ID 'GHSA-9hjg-9r4m-mvj7' "
            "(look up HISTORY.md style: real changelogs reference the GHSA alongside the CVE)")
    # PR reference in RST citation style must appear (HISTORY.md style uses :pr:`N`)
    if ":pr:`6965`" not in txt:
        fails.append(
            "CHANGELOG_ENTRY.md missing RST PR citation ':pr:`6965`' "
            "(HISTORY.md style cites the authoritative PR number; PR#6965 is the fix, not PR#6963)")
    _finish(fails)
main()
