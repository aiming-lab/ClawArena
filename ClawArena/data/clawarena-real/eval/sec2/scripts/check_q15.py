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
    data, err = _load_json(ws / "output" / "q15_final_report.json")
    if err: _finish([err])
    # affected_keys_count == 3（Update 1 修正后）
    akc = data.get("affected_keys_count")
    try:
        akc = int(akc)
    except (TypeError, ValueError):
        _finish(["affected_keys_count not an int: %r" % akc])
    if akc != 3:
        fails.append("affected_keys_count == %d (expected 3 after Update 1)" % akc)
    # key_types 含三个 verbatim secret_type 值
    kt = [str(k) for k in (data.get("key_types") or [])]
    for need in ("openai_api_key", "aws_access_key_id", "anthropic_api_key"):
        if not any(need in k for k in kt):
            fails.append("key_types missing verbatim GitHub SS type: %r" % need)
    # aws_config_rule verbatim
    acr = data.get("aws_config_rule")
    if acr != "ACCESS_KEYS_ROTATED":
        fails.append("aws_config_rule == %r (expected verbatim 'ACCESS_KEYS_ROTATED')" % acr)
    # sts_deny_duration_hours == 36
    sdd = data.get("sts_deny_duration_hours")
    try:
        sdd = int(sdd)
    except (TypeError, ValueError):
        _finish(["sts_deny_duration_hours not an int: %r" % sdd])
    if sdd != 36:
        fails.append("sts_deny_duration_hours == %d (expected 36)" % sdd)
    # detection_date == 2022-12-29（Update 2 修正日期）
    dd = data.get("detection_date")
    if dd != "2022-12-29":
        fails.append("detection_date == %r (expected '2022-12-29' — CircleCI corrected date; NOT '2022-12-25')" % dd)
    # remediation_1h_rate == 2.6%
    r1h = str(data.get("remediation_1h_rate", ""))
    if "2.6" not in r1h:
        fails.append("remediation_1h_rate == %r (expected '2.6%%' — GitGuardian 2024 authoritative figure)" % r1h)
    # openai_surge_2023 == 1212x（GitGuardian 真实数据）
    surge = str(data.get("openai_surge_2023", ""))
    if "1212" not in surge:
        fails.append("openai_surge_2023 == %r (expected '1212x' — GitGuardian State of Secrets Sprawl 2024)" % surge)
    # github_2024_total_leaks 含 '39'（39 million secrets leaked in 2024）
    total_leaks = str(data.get("github_2024_total_leaks", ""))
    if "39" not in total_leaks:
        fails.append("github_2024_total_leaks == %r (expected to contain '39' for '39 million')" % total_leaks)
    # push_protection_precision == 75%（GitHub Push Protection precision rate）
    pp = str(data.get("push_protection_precision", ""))
    if "75" not in pp:
        fails.append("push_protection_precision == %r (expected '75%%' — GitHub Push Protection precision rate)" % pp)
    # circleci_github_oauth_rotation == 2023-01-07T07:30:00Z（CircleCI OAuth token rotation datetime — verbatim from postmortem_FINAL）
    cgr = str(data.get("circleci_github_oauth_rotation", ""))
    if "2023-01-07T07:30:00Z" not in cgr:
        fails.append("circleci_github_oauth_rotation == %r (expected verbatim '2023-01-07T07:30:00Z' — per incident/circleci_style_postmortem_FINAL.md)" % cgr)
    # P1/P2: extracted_at 和 operator 字段
    if not data.get("extracted_at"):
        fails.append("missing extracted_at field (P1)")
    if not data.get("operator"):
        fails.append("missing operator field (P2)")
    _finish(fails)
main()
