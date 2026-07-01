#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

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

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "file_inventory.json")
    if err: _finish([err])
    files = data.get("files")
    if not isinstance(files, list):
        _finish(["'files' must be a list"])
    paths = [str(f.get("path", "")) for f in files if isinstance(f, dict)]
    gh_expected = [
        ".github/workflows/ci.yml",
        ".github/workflows/deploy.yml",
        ".github/workflows/release.yml",
        ".github/workflows/nightly.yml",
    ]
    for exp in gh_expected:
        if not any(exp in p for p in paths):
            fails.append("files missing GitHub workflow: %r" % exp)
    gl_expected = [
        ".gitlab/ci/build.yml",
        ".gitlab/ci/test.yml",
        ".gitlab/ci/deploy.yml",
    ]
    for exp in gl_expected:
        if not any(exp in p for p in paths):
            fails.append("files missing GitLab CI stage file: %r" % exp)
    if len(files) != 7:
        fails.append("files list has %d entries (expected 7: 4 github + 3 gitlab)" % len(files))
    for f in files:
        if not isinstance(f, dict): continue
        s = f.get("system", "")
        if s not in ("github_actions", "gitlab_ci"):
            fails.append("file %r has invalid system %r" % (f.get("path"), s))
    _finish(fails)
main()
