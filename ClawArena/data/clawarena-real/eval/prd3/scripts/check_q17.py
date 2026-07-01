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

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    token_path = ws / "output" / "verification_token.txt"
    if not token_path.exists():
        _finish(["file not found: output/verification_token.txt"])
    line = token_path.read_text(encoding="utf-8").strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["verification_token.txt 须为 VERIFIED:[a-f0-9]{64} 格式（实际: %r）" % line[:80]])
    kpi_path = ws / "output" / "kpi_dashboard.json"
    if not kpi_path.exists():
        _finish(["无法验证哈希：output/kpi_dashboard.json 不存在"])
    digest = hashlib.sha256(kpi_path.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("SHA-256 不匹配: token=%s... != 实算=%s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
