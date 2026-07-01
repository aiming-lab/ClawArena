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
    p = ws / "work" / "check_rhel_patch.sh"
    if not p.exists():
        _finish(["file not found: work/check_rhel_patch.sh"])
    txt = p.read_text(encoding="utf-8")
    # A: full verbatim package name (with openssh- prefix) must appear somewhere in the file
    # The advisory's fixed_package_version field is "openssh-8.7p1-38.el9_4.1" — use the full name
    if "openssh-8.7p1-38.el9_4.1" not in txt:
        fails.append("check_rhel_patch.sh must reference the full package name openssh-8.7p1-38.el9_4.1 (verbatim from assets/advisories/redhat_RHSA-2024-4312.json fixed_package_version field)")
    # V9: verbatim errata ID
    if "RHSA-2024:4312" not in txt:
        fails.append("check_rhel_patch.sh missing errata ID RHSA-2024:4312")
    # V8: PASS/FAIL output (via echo or printf)
    if "PASS" not in txt or "FAIL" not in txt:
        fails.append("check_rhel_patch.sh must output PASS and FAIL")
    # A: script must use #!/bin/bash or #!/usr/bin/env bash shebang
    if not txt.startswith("#!/"):
        fails.append("check_rhel_patch.sh must start with a bash shebang (#!/bin/bash or #!/usr/bin/env bash)")
    # executable bit
    import stat
    mode = p.stat().st_mode
    if not (mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
        fails.append("check_rhel_patch.sh is not executable (chmod +x required)")
    _finish(fails)
main()
