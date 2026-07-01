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
    out_dir = ws / "rca_outputs"
    # 文件名匹配 final_rca_report_YYYYMMDD.md
    pattern = re.compile(r"final_rca_report_\d{8}\.md$")
    matching = [f for f in out_dir.iterdir() if f.is_file() and pattern.match(f.name)]
    if not matching:
        fails.append("no file matching final_rca_report_YYYYMMDD.md in rca_outputs/ (P5 naming convention from Feishu session)")
        _finish(fails)
    # 检查内容：Class I 出现次数 >= 2
    txt = matching[0].read_text(encoding="utf-8")
    class1_count = len(re.findall(r"Class\s+I(?!\s*I)", txt))
    if class1_count < 2:
        fails.append("final report mentions 'Class I' only %d time(s) (expected >= 2)" % class1_count)
    _finish(fails)
main()
