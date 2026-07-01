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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "submission_manifest.json")
    if err: _finish([err])
    files = data.get("files", [])
    if not isinstance(files, list) or len(files) == 0:
        _finish(["files array is empty"])
    # required files
    required = {
        "cdph_staffing_log_week1.csv",
        "cdph_staffing_log_week2.csv",
        "violation_ledger_final.json",
        "penalty_final.json",
    }
    found_paths = set()
    for entry in files:
        if isinstance(entry, dict):
            p = str(entry.get("path", ""))
            found_paths.add(Path(p).name)
    missing_req = required - found_paths
    if missing_req:
        fails.append("missing required files in manifest: %s" % sorted(missing_req))
    # sha256 hashes must match actual file content
    for entry in files:
        if not isinstance(entry, dict):
            continue
        p_str = str(entry.get("path", ""))
        sha_manifest = str(entry.get("sha256", "")).lower().strip()
        if not sha_manifest:
            fails.append("entry %r has no sha256" % p_str)
            continue
        # resolve path
        target = ws / "output" / Path(p_str).name
        if not target.exists():
            # try as relative path from workspace
            target2 = ws / p_str
            if target2.exists():
                target = target2
            else:
                fails.append("manifest file %r not found at %s or %s" % (p_str, target, target2))
                continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if sha_manifest != actual:
            fails.append("sha256 mismatch for %s: manifest=%s actual=%s" % (
                Path(p_str).name, sha_manifest[:12], actual[:12]))
    _finish(fails)
main()
main()
