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
    data, err = _load_json(ws / "output" / "submission_manifest.json")
    if err: _finish([err])
    # total_files >= 12
    tf = data.get("total_files")
    try:
        tf = int(tf)
        if tf < 12:
            fails.append("total_files == %d (expected >= 12)" % tf)
    except (TypeError, ValueError):
        fails.append("total_files 须为整数")
    # files 数组每条须含 path/schema_valid/data_version
    files = data.get("files") or []
    if not isinstance(files, list) or len(files) < 12:
        fails.append("files 数组须含至少 12 条（实际: %d）" % len(files))
    for i, f in enumerate(files[:5]):  # 检查前 5 条
        if not isinstance(f, dict):
            continue
        for key in ("path", "schema_valid", "data_version"):
            if key not in f:
                fails.append("files[%d] 缺少字段 '%s'" % (i, key))
        if f.get("schema_valid") is not True:
            fails.append("files[%d].schema_valid == %r (expected true)" % (i, f.get("schema_valid")))
    # verification_token 须与 output/verification_token.txt 一致
    vt_file = ws / "output" / "verification_token.txt"
    if vt_file.exists():
        expected_vt = vt_file.read_text(encoding="utf-8").strip()
        manifest_vt = str(data.get("verification_token") or "").strip()
        if manifest_vt != expected_vt:
            fails.append("verification_token 与 output/verification_token.txt 不一致")
    # generated_at 须存在（ISO 8601）
    ga = data.get("generated_at")
    if not ga:
        fails.append("generated_at 字段缺失（P1 要求 ISO 8601 时间戳）")
    _finish(fails)
main()
