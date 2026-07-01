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
    txt = _read(ws / "output" / "verification_report.txt")
    if txt is None:
        _finish(["file not found: output/verification_report.txt"])
    first_line = txt.strip().splitlines()[0] if txt.strip() else ""
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", first_line)
    if not m:
        _finish(["first line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % first_line[:80]])
    # recompute hash of submission_manifest.json
    manifest_path = ws / "output" / "submission_manifest.json"
    if not manifest_path.exists():
        _finish(["cannot verify: output/submission_manifest.json missing"])
    actual = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if m.group(1) != actual:
        fails.append("sha256 mismatch: report=%s recomputed=%s" % (m.group(1)[:12], actual[:12]))
    _finish(fails)
main()
main()
