#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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
    tok = _read(ws / "rca_outputs" / "verification_token.txt")
    if tok is None:
        _finish(["file not found: rca_outputs/verification_token.txt"])
    line = tok.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["verification_token.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    meta = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if not meta.exists():
        _finish(["cannot verify hash: rca_outputs/nimbus_recall_metadata.json missing"])
    digest = hashlib.sha256(meta.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: token %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    # C★ 跨轮闭合：验证 nimbus_recall_metadata.json 内容符合权威值
    try:
        meta_data = json.loads(meta.read_text(encoding="utf-8"))
        ur = int(meta_data.get("units_recalled", -1))
        if ur != 52328:
            fails.append(
                "nimbus_recall_metadata.json units_recalled == %d (must be exactly 52328); "
                "the verification token was computed from this file — data integrity check failed" % ur
            )
        cmp = int(meta_data.get("complaints", -1))
        if cmp != 3698:
            fails.append(
                "nimbus_recall_metadata.json complaints == %d (must be exactly 3698); "
                "data integrity check failed" % cmp
            )
        si = int(meta_data.get("serious_injuries", -1))
        if si != 6:
            fails.append(
                "nimbus_recall_metadata.json serious_injuries == %d (must be exactly 6); "
                "data integrity check failed" % si
            )
    except Exception as e:
        fails.append("could not validate nimbus_recall_metadata.json content: %s" % e)
    _finish(fails)
main()
