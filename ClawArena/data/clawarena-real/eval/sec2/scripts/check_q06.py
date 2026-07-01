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
    txt = _read(ws / "output" / "q06_slack_summary.md")
    if txt is None:
        _finish(["file not found: output/q06_slack_summary.md"])
    # P4: 三段 H2 结构（区分大小写——Manager Chen 的格式要求精确标题）
    if "## Impact" not in txt:
        fails.append("q06 must have H2 heading '## Impact' (exact case — per Manager Chen's format requirement)")
    if "## Actions Taken" not in txt:
        fails.append("q06 must have H2 heading '## Actions Taken' (exact case — per Manager Chen's format requirement)")
    if "## Next Steps" not in txt:
        fails.append("q06 must have H2 heading '## Next Steps' (exact case — per Manager Chen's format requirement)")
    # 字数 <= 150（Slack 频道摘要必须高度精炼，非技术受众阅读体验优先）
    word_count = len(txt.split())
    if word_count > 150:
        fails.append("q06 word count %d exceeds 150 (Slack channel summary must be concise — target non-technical audience)" % word_count)
    _finish(fails)
main()
