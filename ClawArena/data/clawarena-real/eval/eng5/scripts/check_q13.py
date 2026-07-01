#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_q13.py — audit report: >= 8 fixes, severity enum, official docs URLs, deadline field
import sys, json, re
from pathlib import Path

VALID_SEVERITY = {"critical", "high", "medium", "low"}

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def _find_val(obj, needle):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and needle in v: return True
            if _find_val(v, needle): return True
    elif isinstance(obj, list):
        for item in obj:
            if _find_val(item, needle): return True
    return False

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "cicd_audit_report.json")
    if err: _finish([err])
    fixes = data.get("fixes")
    if not isinstance(fixes, list):
        _finish(["'fixes' must be a list"])
    if len(fixes) < 8:
        fails.append("fixes array has %d entries (expected >= 8)" % len(fixes))
    required_fields = ["file", "issue_type", "severity", "old_value", "new_value", "reference_url"]
    has_deadline_2025_04_01 = False
    for i, fix in enumerate(fixes):
        if not isinstance(fix, dict): continue
        for field in required_fields:
            if field not in fix or not fix[field]:
                fails.append("fix[%d] missing or empty field '%s'" % (i, field))
        # A: severity must be exactly one of the allowed enum values
        sev = str(fix.get("severity", ""))
        if sev and sev not in VALID_SEVERITY:
            fails.append(
                "fix[%d] severity %r is not a valid enum value; must be one of %s"
                % (i, sev, sorted(VALID_SEVERITY))
            )
        # A: reference_url must point to docs.github.com or docs.gitlab.com only
        url = str(fix.get("reference_url", ""))
        if url:
            if not re.search(r"https?://docs\.(github|gitlab)\.com", url):
                fails.append(
                    "fix[%d] reference_url must be from docs.github.com or docs.gitlab.com "
                    "(blog posts and discussion threads are not accepted — got %r)" % (i, url[:80])
                )
        # C: check for deadline field referencing 2025-04-01 (deployments permission change)
        if _find_val(fix, "2025-04-01"):
            has_deadline_2025_04_01 = True
    if not has_deadline_2025_04_01:
        fails.append(
            "fixes must include at least one entry with deadline '2025-04-01' "
            "(for the deployments permission change effective April 1, 2025)"
        )
    all_urls = [str(f.get("reference_url", "")) for f in fixes if isinstance(f, dict)]
    has_real = any("docs.github.com" in u or "docs.gitlab.com" in u for u in all_urls)
    if not has_real:
        fails.append("fixes must include at least one docs.github.com or docs.gitlab.com URL")
    _finish(fails)
main()
