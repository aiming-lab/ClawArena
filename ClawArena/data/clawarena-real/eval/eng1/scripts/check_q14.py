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
    txt = _read(ws / "docs" / "SECURITY_ADVISORY_CVE-2024-47081.md")
    if txt is None:
        _finish(["file not found: docs/SECURITY_ADVISORY_CVE-2024-47081.md"])
    if "GHSA-9hjg-9r4m-mvj7" not in txt:
        fails.append("missing GHSA ID 'GHSA-9hjg-9r4m-mvj7'")
    if "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N" not in txt:
        fails.append("missing exact CVSS vector 'CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N'")
    if "## Workaround" not in txt:
        fails.append("P4: missing '## Workaround' section")
    if "trust_env=False" not in txt:
        fails.append("missing workaround 'trust_env=False' in advisory")
    # P4: ## Workaround must appear AFTER ## Fix
    fix_pos = txt.find("## Fix")
    wa_pos = txt.find("## Workaround")
    if fix_pos == -1:
        fails.append("missing '## Fix' section")
    elif wa_pos != -1 and wa_pos < fix_pos:
        fails.append("P4: '## Workaround' appears before '## Fix' (must be after)")
    # ## Vulnerability section required (standard advisory structure)
    if "## Vulnerability" not in txt:
        fails.append(
            "missing '## Vulnerability' section: security advisories must include a dedicated "
            "Vulnerability section describing the root cause and affected code path")
    # CWE-522 must appear (from NVD metadata in SECURITY_CONTEXT.md)
    if "CWE-522" not in txt:
        fails.append(
            "missing CWE classification 'CWE-522' (Inadequately Protected Credentials) — "
            "read analysis/cve_metadata.json or SECURITY_CONTEXT.md for the NVD-assigned CWE")
    _finish(fails)
main()
