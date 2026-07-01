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
    data, err = _load_json(ws / "output" / "q03_trufflehog_scan.json")
    if err: _finish([err])
    # findings 数组存在
    findings = data.get("findings")
    if not isinstance(findings, list) or not findings:
        _finish(["findings must be a non-empty array"])
    # 三种 DetectorName 必须全部出现：TruffleHog 真实输出使用 CamelCase 无连字符
    # 参见 TruffleHog JSON output spec: DetectorName 为 "OpenAI" / "AWS" / "Anthropic"
    # 常见错误：使用 "openai-api-key"/"aws-access-key" 等非官方格式
    REQUIRED_DETECTORS = {"OpenAI", "AWS", "Anthropic"}
    verified_detectors = set()
    for f in findings:
        if not isinstance(f, dict):
            continue
        if f.get("Verified") is True:
            dn = f.get("DetectorName", "")
            verified_detectors.add(dn)
    for det in REQUIRED_DETECTORS:
        if det not in verified_detectors:
            fails.append(
                "findings missing Verified=true entry with DetectorName == %r "
                "(verbatim TruffleHog detector name — use CamelCase, no hyphens; "
                "e.g. \'OpenAI\' not \'openai-api-key\', \'AWS\' not \'aws-access-key\', "
                "\'Anthropic\' not \'anthropic-api-key\')" % det
            )
    # exit_code == 183（--fail 触发时的真实退出码）
    ec = data.get("exit_code")
    try:
        ec = int(ec)
    except (TypeError, ValueError):
        _finish(["exit_code must be an int: %r" % ec])
    if ec != 183:
        fails.append("exit_code == %r (expected 183 — TruffleHog --fail exit code when credentials found)" % ec)
    _finish(fails)
main()
