#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sec2.py — sec2 可解性审计（金标自检）。

在 workspace 临时副本上应用 update 后写出每轮「正确产物」，
运行全部 check_qNN.py + preference 检查，断言全 PASS。
再验证 ≥4 个反例断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_sec2.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sec2"
UPD = DS / "openclaw" / "updates" / "sec2"
SCRIPTS = DS / "eval" / "sec2" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sec2_gold_ws")

NOW_ISO = "2026-01-10T12:00:00Z"
OPERATOR = "li_wei_secops_ai"


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prep_workspace() -> Path:
    """准备工作空间临时副本，应用全部 workspace updates。"""
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply Update 1 workspace
    u1_ws = UPD / "upd1_workspace"
    for src_rel, dst_rel in [
        ("incident/gitguardian_webhook_v2.json", "incident/gitguardian_webhook_v2.json"),
        ("reports/impact_analysis_v2.md", "reports/impact_analysis_v2.md"),
        ("incident/cloudtrail_analysis_update1.json", "incident/cloudtrail_analysis_update1.json"),
    ]:
        src = u1_ws / src_rel
        dst = GOLD / dst_rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    # Apply Update 2 workspace
    u2_ws = UPD / "upd2_workspace"
    for src_rel, dst_rel in [
        ("incident/circleci_style_postmortem_FINAL.md", "incident/circleci_style_postmortem_FINAL.md"),
        ("communications/email/vendor_circleci_advisory_v2.eml", "communications/email/vendor_circleci_advisory_v2.eml"),
        ("scripts/rotate_aws_key.sh", "scripts/rotate_aws_key.sh"),
        ("incident/forensics_analysis_update2.json", "incident/forensics_analysis_update2.json"),
    ]:
        src = u2_ws / src_rel
        dst = GOLD / dst_rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    return GOLD


def solve(ws: Path) -> None:
    """Write all gold-standard deliverables."""
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # Q01: GitHub SS alert 解析（openai_api_key, active, open）
    _wj(out / "q01_alert_parsed.json", {
        "alert_number": 1,
        "secret_type": "openai_api_key",
        "validity": "active",
        "state": "open",
        "file_path": "src/integrations/openai_client.py",
        "commit_sha": "a3f9c2e1d4b8f7a0c9e5b2d1",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q02: 冲突分析（HONEYPOT 标注 + CloudTrail 字段 + 2.6% + 1212x）
    _w(out / "q02_conflict_analysis.md", """# Conflict Analysis — HONEYPOT vs Primary Sources

## Conclusion
The file `reports/auto_summary_HONEYPOT.md` is **untrustworthy** and contains
inaccurate bot-generated claims. It must NOT be used as authoritative evidence.

## HONEYPOT Inaccuracies

| Claim in HONEYPOT | Authoritative Value | Source |
|---|---|---|
| All keys revoked within 2 hours | Keys still active per GitGuardian webhook | gitguardian_webhook_v2.json |
| Remediation rate ~15% | **2.6%** revoked within 1 hour | GitGuardian State of Secrets Sprawl 2024 |
| OpenAI surge ~100x | **1212x** surge in 2023 | GitGuardian State of Secrets Sprawl 2024 |

## CloudTrail Counter-Evidence
The `incident/cloudtrail_events.jsonl` file contains authoritative event data.
Key CloudTrail fields that contradict the HONEYPOT's "no unauthorized access" claim:
- `sourceIPAddress`: 185.234.219.44 (external IP — not NovaBridge corporate range)
- `eventName`: GetCallerIdentity, ListBuckets (reconnaissance pattern from external IP)
- `userAgent`: python-requests/2.28.0 (not standard AWS CLI — suspicious)

The HONEYPOT claims no unauthorized data access, but CloudTrail `eventName` field
shows ListBuckets and GetObject calls originating from `sourceIPAddress` 185.234.219.44,
which is external. This contradicts the HONEYPOT summary directly.

## Authoritative Figures
- **GitGuardian 1-hour revocation rate**: 2.6% (GitGuardian State of Secrets Sprawl 2024)
- **OpenAI key leak surge (2023)**: 1212x (GitGuardian State of Secrets Sprawl 2024)
- **GitHub 2024 total secrets leaked**: 39 million
""")

    # Q03: TruffleHog 扫描（Verified=true, DetectorName, exit_code=183）
    _wj(out / "q03_trufflehog_scan.json", {
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
        "exit_code": 183,
        "scan_target": "codebase/",
        "findings": [
            {
                "DetectorName": "OpenAI",
                "DetectorType": 2,
                "DecoderName": "PLAIN",
                "Verified": True,
                "Raw": "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcdefghijk",
                "RawV2": "",
                "Redacted": "sk-proj-aBcDE**************************",
                "ExtraData": {"version": "2"},
                "SourceMetadata": {
                    "Data": {
                        "Git": {
                            "commit": "a3f9c2e1d4b8f7a0c9e5b2d1",
                            "file": "codebase/src/integrations/openai_client.py",
                            "line": 12,
                            "repository": "novabridge/backend",
                        }
                    }
                },
                "StructuredData": None,
            },
            {
                "DetectorName": "AWS",
                "DetectorType": 2,
                "DecoderName": "PLAIN",
                "Verified": True,
                "Raw": "AKIAIOSFODNN7EXAMPLE",
                "RawV2": "",
                "Redacted": "AKIA***************",
                "ExtraData": {"rotated": "false"},
                "SourceMetadata": {
                    "Data": {
                        "Git": {
                            "commit": "a3f9c2e1d4b8f7a0c9e5b2d1",
                            "file": "codebase/src/integrations/aws_uploader.py",
                            "line": 8,
                            "repository": "novabridge/backend",
                        }
                    }
                },
                "StructuredData": None,
            },
            {
                "DetectorName": "Anthropic",
                "DetectorType": 2,
                "DecoderName": "PLAIN",
                "Verified": True,
                "Raw": "sk-ant-api03-xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX-XXXXXXXX",
                "RawV2": "",
                "Redacted": "sk-ant-api03-***************************",
                "ExtraData": {},
                "SourceMetadata": {
                    "Data": {
                        "Git": {
                            "commit": "a3f9c2e1d4b8f7a0c9e5b2d1",
                            "file": "codebase/src/integrations/anthropic_client.py",
                            "line": 12,
                            "repository": "novabridge/backend",
                        }
                    }
                },
                "StructuredData": None,
            },
        ],
        "summary": {
            "total_findings": 3,
            "verified_count": 3,
            "unverified_count": 0,
            "exit_code_explanation": "183 = TruffleHog --fail flag triggered (credentials found)",
        },
    })

    # Q04: 受影响文件（含 openai_client.py，不含 archive/）
    _w(out / "q04_affected_files.txt",
       "codebase/src/integrations/openai_client.py\n"
       "codebase/src/integrations/aws_uploader.py\n"
       "codebase/src/integrations/anthropic_client.py\n")

    # Q05: 处置决策（AKIA, disable_iam_user_key, ACCESS_KEYS_ROTATED）
    _wj(out / "q05_containment_decision.json", {
        "key_prefix": "AKIA",
        "containment_method": "disable_iam_user_key",
        "rule_name": "ACCESS_KEYS_ROTATED",
        "rule_description": "AWS Config managed rule; identifier: ACCESS_KEYS_ROTATED; default maxAccessKeyAge=90",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q06: Slack 摘要（三段 H2 + ≤300 字）
    _w(out / "q06_slack_summary.md", """# Incident Summary — API Key Leak (2026-01-10)

## Impact
Two API credentials leaked from the `novabridge/backend` repository (commit a3f9c2e):
- OpenAI API key (openai_api_key, validity: active)
- AWS IAM access key (AKIA prefix, long-term credential, validity: active)

External IP 185.234.219.44 performed GetCallerIdentity and ListBuckets API calls
within minutes of the commit. No confirmed data exfiltration yet.

## Actions Taken
- Alert acknowledged in GitHub Security tab (alert #1)
- CloudTrail and GuardDuty logs reviewed and archived
- AWS IAM key disabled via IAM (disable_iam_user_key containment)
- OpenAI key revocation in progress
- AWS Config rule ACCESS_KEYS_ROTATED applied for ongoing compliance

## Next Steps
- Complete OpenAI key revocation and update GitHub SS alert (state=resolved, resolution=revoked)
- Audit S3 access logs for potential customer data access
- Run TruffleHog full-repo scan
- Circulate postmortem to stakeholders after investigation closes
""")

    # Q07: 初版影响分析（2 个 key，pre-Update 1）
    _wj(out / "q07_impact_v1.json", {
        "affected_keys_count": 2,
        "affected_services": ["openai", "aws"],
        "keys": [
            {"service": "openai", "key_type": "openai_api_key", "validity": "active"},
            {"service": "aws", "key_type": "aws_access_key_id", "key_prefix": "AKIA", "validity": "active"},
        ],
        "note": "Pre-Update-1 scope. Will be superseded by impact_analysis_v2.md after Update 1.",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q08: AWS 处置（ACCESS_KEYS_ROTATED, NON_COMPLIANT, 90）
    _wj(out / "q08_aws_remediation.json", {
        "rule_name": "ACCESS_KEYS_ROTATED",
        "compliance_type": "NON_COMPLIANT",
        "max_key_age_days": 90,
        "resource_type": "AWS::IAM::User",
        "trigger_type": "Periodic",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q09: 更新影响分析（3 个 key + supersede）
    _wj(out / "q09_impact_v2.json", {
        "affected_keys_count": 3,
        "affected_services": ["openai", "aws", "anthropic"],
        "superseded_fields": ["affected_keys_count", "affected_services"],
        "supersedes": "q07_impact_v1.json",
        "keys": [
            {"service": "openai", "key_type": "openai_api_key", "validity": "active"},
            {"service": "aws", "key_type": "aws_access_key_id", "key_prefix": "AKIA", "validity": "active"},
            {"service": "anthropic", "key_type": "anthropic_api_key", "validity": "active",
             "source": "gitguardian_webhook_v2.json wh-051"},
        ],
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q10: Anthropic key 撤销（verbatim secret_type + ISO-8601 revoked_at）
    _wj(out / "q10_anthropic_revoke.json", {
        "secret_type": "anthropic_api_key",
        "revoked_at": "2026-01-10T10:30:00Z",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q11: 事实核查（not_revoked_by_huangmin + evidence_source）
    _wj(out / "q11_fact_check.json", {
        "openai_key_status": "not_revoked_by_huangmin",
        "evidence_source": [
            "gitguardian_webhook_v2.json",
            "communications/slack/dm_liwei_huangmin.json",
        ],
        "conflict_summary": (
            "Huang Min's initial claim (Slack DM dm-001) that he 'already revoked' the OpenAI key "
            "is contradicted by GitGuardian webhook v2 (wh-052), which shows the key still active "
            "as of 08:55 UTC. Huang Min later corrected his statement (dm-006): the key was NOT revoked. "
            "The GitGuardian webhook is the authoritative technical evidence."
        ),
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q12: GitHub SS PATCH（state=resolved, resolution=revoked）
    _wj(out / "q12_gh_ss_patch.json", {
        "alert_number": 1,
        "state": "resolved",
        "resolution": "revoked",
        "patch_endpoint": "PATCH /repos/novabridge/backend/secret-scanning/alerts/1",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })

    # Q13: 事件时间线（含 2022-12-29，不含 2022-12-25）
    _w(out / "q13_incident_timeline.md", """# Incident Timeline

## NovaBridge Incident (2026)

| Date | Event | Source |
|---|---|---|
| 2026-01-10T07:58:00Z | Huang Min commits credentials to novabridge/backend | git history |
| 2026-01-10T08:00:00Z | GitHub Push Protection triggers alert (openai_api_key, validity=active, state=open) | alert_timeline.json |
| 2026-01-10T08:03:00Z | GitGuardian webhook fires, key confirmed active | webhook logs |
| 2026-01-10T08:05:00Z | External scan detected: GetCallerIdentity from 185.234.219.44 | cloudtrail_events.jsonl |
| 2026-01-10T08:15:00Z | Li Wei initiates incident response | remediation_checklist.md |
| 2026-01-10T08:50:00Z | Update 1: Anthropic API key discovered (webhook wh-051) | gitguardian_webhook_v2.json |
| 2026-01-10T10:30:00Z | Anthropic API key revoked | q10_anthropic_revoke.json |
| 2026-01-10T11:00:00Z | Update 2: Postmortem FINAL corrects CircleCI detection date | circleci_style_postmortem_FINAL.md |

## CircleCI Incident Reference (2023)

| Date | Event | Source |
|---|---|---|
| 2022-12-22 | CircleCI data exfiltration date | CircleCI official post-mortem |
| 2022-12-29 | CircleCI customer anomaly detection date (CORRECTED — see postmortem_FINAL) | circleci_style_postmortem_FINAL.md |
| 2023-01-04 | CircleCI public disclosure | CircleCI official post-mortem |
| 2023-01-07T07:30:00Z | GitHub OAuth token rotation completed | CircleCI official post-mortem |

*Note: The date 2022-12-29 is the authoritative CircleCI customer detection date,
per the official post-mortem and corrected in Update 2 (circleci_style_postmortem_FINAL.md).
The earlier draft value is superseded.*
""")

    # Q14: STS 处置指南（36 hours + DateLessThan + ## Rationale）
    _w(out / "q14_sts_handling.md", """# AWS STS Temporary Credential Handling Guide

## Overview
This document covers the correct procedure for invalidating AWS STS temporary
credentials (ASIA prefix) that have been potentially compromised.

## Background
AWS temporary credentials (ASIA prefix) differ fundamentally from long-term IAM
user access keys (AKIA prefix). They cannot be "revoked" in the traditional sense
because they are time-limited tokens issued by the STS service.

## Maximum Token Lifetime
- **GetSessionToken** and **GetFederationToken**: maximum **36 hours**
- **AssumeRole**: maximum 1 hour (shorter, different use case)

This means a compromised ASIA token may remain valid for up to **36 hours** after
issuance, even if the originating IAM user's key is rotated.

## Containment Procedure

### Step 1: Identify Compromise Timestamp
Determine the exact time the ASIA credential was issued by reviewing CloudTrail logs
for the AssumeRole / GetSessionToken / GetFederationToken event.

### Step 2: Apply Deny-All IAM Policy with DateLessThan Condition
Apply a deny-all inline policy to the affected IAM user/role. The `DateLessThan`
condition on `aws:TokenIssueTime` will block all tokens issued before the compromise time:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "DateLessThan": {
        "aws:TokenIssueTime": "2026-01-10T08:03:00Z"
      }
    }
  }]
}
```

### Step 3: Maintain Policy for 36 Hours
The deny policy must remain active for at least **36 hours** from the compromise
timestamp to cover the maximum STS token lifetime.

### Step 4: Rotate Underlying Credentials
After the 36-hour window, rotate the underlying IAM access key to prevent re-issuance
of compromised tokens.

## Rationale

The `DateLessThan` on `aws:TokenIssueTime` approach is the AWS-recommended method
(per AWS Security Blog) because:
1. STS tokens are bearer tokens — they cannot be individually "revoked"
2. The token issuer (STS) does not maintain a revocation list
3. The `DateLessThan` condition is evaluated at authorization time, blocking any
   matching token without requiring the token itself to be invalidated
4. This is the only mechanism guaranteed to work for all STS token variants
   (GetSessionToken, GetFederationToken, AssumeRole)

The 36-hour window is critical: GetSessionToken and GetFederationToken can issue
tokens valid for up to 36 hours, so the deny policy must cover this entire window.

## Reference
- AWS Security Blog: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/
- AWS GuardDuty: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html
""")

    # Q15: 终轮综合报告（V4+V9+V10 全闭合）
    # 必填字段：affected_keys_count, key_types, aws_config_rule, sts_deny_duration_hours,
    # detection_date, remediation_1h_rate, openai_surge_2023, github_2024_total_leaks,
    # push_protection_precision, extracted_at, operator
    final_report = {
        "incident": "NovaBridge API Key Leak — 2026-01-10",
        "affected_keys_count": 3,
        "key_types": ["openai_api_key", "aws_access_key_id", "anthropic_api_key"],
        "aws_config_rule": "ACCESS_KEYS_ROTATED",
        "sts_deny_duration_hours": 36,
        "detection_date": "2022-12-29",
        "remediation_1h_rate": "2.6%",
        "openai_surge_2023": "1212x",
        "github_2024_total_leaks": "39 million",
        "push_protection_precision": "75%",
        "circleci_github_oauth_rotation": "2023-01-07T07:30:00Z",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    }
    _wj(out / "q15_final_report.json", final_report)

    # Q16: SHA-256 sign-off over q15_final_report.json
    digest = hashlib.sha256((out / "q15_final_report.json").read_bytes()).hexdigest()
    _w(out / "q16_signoff.txt", f"VERIFIED:{digest}\n")


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q01": ["check_q01.py", ("pref", "P1,P2", "output/q01_alert_parsed.json")],
    "q02": ["check_q02.py"],
    "q03": ["check_q03.py", ("pref", "P1,P2,P3", "output/q03_trufflehog_scan.json")],
    "q04": ["check_q04.py"],
    "q05": ["check_q05.py", ("pref", "P1,P2,P3", "output/q05_containment_decision.json")],
    "q06": ["check_q06.py", ("pref", "P4", "output/q06_slack_summary.md")],
    "q07": ["check_q07.py", ("pref", "P1,P2", "output/q07_impact_v1.json")],
    "q08": ["check_q08.py", ("pref", "P1,P2,P3", "output/q08_aws_remediation.json")],
    "q09": ["check_q09.py", ("pref", "P1,P2", "output/q09_impact_v2.json")],
    "q10": ["check_q10.py", ("pref", "P1,P2,P3", "output/q10_anthropic_revoke.json")],
    "q11": ["check_q11.py"],
    "q12": ["check_q12.py", ("pref", "P1,P2,P3", "output/q12_gh_ss_patch.json")],
    "q13": ["check_q13.py"],
    "q14": ["check_q14.py", ("pref", "P5", "output/q14_sts_handling.md")],
    "q15": ["check_q15.py", ("pref", "P1,P2,P3", "output/q15_final_report.json")],
    "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)
    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ---------------------------------------------------------------- #
    # 反例抽样（≥4 个，错误产物必须 FAIL）
    # ---------------------------------------------------------------- #
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # NP1: q01 错误 validity 值（'valid' 非枚举值）
    _wj(ws / "output" / "q01_alert_parsed.json", {
        "alert_number": 1,
        "secret_type": "openai_api_key",
        "validity": "valid",            # 错误：应为 active
        "state": "open",
        "file_path": "src/integrations/openai_client.py",
        "commit_sha": "a3f9c2e1d4b8f7a0c9e5b2d1",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })
    ok, _ = run_check("check_q01.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP1 q01 validity='valid' -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP7: q03 使用连字符格式 DetectorName（常见 gemma 错误）
    _wj(ws / "output" / "q03_trufflehog_scan.json", {
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
        "exit_code": 183,
        "findings": [
            {"DetectorName": "openai-api-key", "Verified": True, "Raw": "sk-proj-xxx"},   # 错误：应为 'OpenAI'
            {"DetectorName": "aws-access-key",  "Verified": True, "Raw": "AKIAIOSFODNN7EXAMPLE"},  # 错误：应为 'AWS'
            {"DetectorName": "anthropic-api-key", "Verified": True, "Raw": "sk-ant-xxx"},  # 错误：应为 'Anthropic'
        ],
    })
    ok, _ = run_check("check_q03.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP7 q03 hyphenated DetectorName (openai-api-key) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP8: q06 字数超出 150（浅写摘要会超限）
    # 恢复正确 q03 先
    _wj(ws / "output" / "q03_trufflehog_scan.json", {
        "extracted_at": NOW_ISO, "operator": OPERATOR, "exit_code": 183,
        "findings": [
            {"DetectorName": "OpenAI", "Verified": True, "Raw": "sk-proj-xxx",
             "SourceMetadata": {"Data": {"Git": {"file": "codebase/src/integrations/openai_client.py"}}}},
            {"DetectorName": "AWS", "Verified": True, "Raw": "AKIAIOSFODNN7EXAMPLE",
             "SourceMetadata": {"Data": {"Git": {"file": "codebase/src/integrations/aws_uploader.py"}}}},
            {"DetectorName": "Anthropic", "Verified": True, "Raw": "sk-ant-xxx",
             "SourceMetadata": {"Data": {"Git": {"file": "codebase/src/integrations/anthropic_client.py"}}}},
        ],
    })
    _w(ws / "output" / "q06_slack_summary.md",
       "## Impact\n"
       "A critical API key leak was detected in the novabridge/backend repository on 2026-01-10. "
       "Multiple active credentials including OpenAI API key, AWS IAM access key (AKIA prefix), "
       "and Anthropic API key were hardcoded in the codebase and exposed via git commit a3f9c2e1. "
       "External IP 185.234.219.44 performed reconnaissance actions including GetCallerIdentity "
       "and ListBuckets API calls using the leaked AWS credentials within minutes of exposure. "
       "AWS GuardDuty confirmed unauthorized access from multiple external ISP IP addresses. "
       "The breach scope was expanded by Update 1 to include a third Anthropic key discovered "
       "via GitGuardian webhook v2 (wh-051).\n\n"
       "## Actions Taken\n"
       "GitHub Secret Scanning alert #1 (openai_api_key, validity=active) was acknowledged. "
       "CloudTrail and GuardDuty logs were reviewed and preserved. AWS IAM access key was "
       "disabled via disable_iam_user_key containment method. TruffleHog full-repository scan "
       "verified all three leaked credentials. GitGuardian webhook v2 confirmed the OpenAI key "
       "remains active, contradicting Huang Min's Slack DM claim that he had already revoked it.\n\n"
       "## Next Steps\n"
       "Complete OpenAI and Anthropic key revocations and update GitHub SS alert to state=resolved, "
       "resolution=revoked. Audit S3 access logs for potential customer data exfiltration. "
       "Implement pre-commit hooks and mandatory secret scanning to prevent future incidents.\n"
    )
    ok, _ = run_check("check_q06.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP8 q06 word count > 150 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP9: q15 缺少新必填字段（浅做不会补齐）
    _wj(ws / "output" / "q15_final_report.json", {
        "affected_keys_count": 3,
        "key_types": ["openai_api_key", "aws_access_key_id", "anthropic_api_key"],
        "aws_config_rule": "ACCESS_KEYS_ROTATED",
        "sts_deny_duration_hours": 36,
        "detection_date": "2022-12-29",
        "remediation_1h_rate": "2.6%",
        # 缺少 openai_surge_2023 / github_2024_total_leaks / push_protection_precision / circleci_github_oauth_rotation
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })
    ok, _ = run_check("check_q15.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP9 q15 missing openai_surge_2023/github_2024_total_leaks/push_protection_precision/circleci_github_oauth_rotation -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP2: q05 错误 containment（revoke_sts_token 不适用 AKIA）
    _wj(ws / "output" / "q05_containment_decision.json", {
        "key_prefix": "AKIA",
        "containment_method": "revoke_sts_token",    # 错误：AKIA 应用 disable_iam_user_key
        "rule_name": "ACCESS_KEYS_ROTATED",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })
    ok, _ = run_check("check_q05.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP2 q05 containment=revoke_sts_token -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP3: q13 含废弃日期 2022-12-25（V10 supersede 检测）
    _w(ws / "output" / "q13_incident_timeline.md", """# Incident Timeline

| Date | Event | Source |
|---|---|---|
| 2022-12-22 | CircleCI exfiltration | CircleCI post-mortem |
| 2022-12-25 | CircleCI customer detection | DRAFT (WRONG — should be 2022-12-29) |
""")
    ok, _ = run_check("check_q13.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP3 q13 uses superseded date 2022-12-25 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP4: q15 affected_keys_count=2（未更新 Update 1；同时缺少新必填字段）
    _wj(ws / "output" / "q15_final_report.json", {
        "affected_keys_count": 2,           # 错误：Update 1 后应为 3
        "key_types": ["openai_api_key", "aws_access_key_id"],
        "aws_config_rule": "ACCESS_KEYS_ROTATED",
        "sts_deny_duration_hours": 36,
        "detection_date": "2022-12-29",
        "remediation_1h_rate": "2.6%",
        # 缺少 openai_surge_2023 / github_2024_total_leaks / push_protection_precision / circleci_github_oauth_rotation
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })
    ok, _ = run_check("check_q15.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP4 q15 affected_keys_count=2 (pre-update, missing new fields) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP5: q04 引用废弃 archive 文件（V6 红鲱鱼）
    _w(ws / "output" / "q04_affected_files.txt",
       "codebase/src/integrations/openai_client.py\n"
       "archive/OLD_incident_response_plan_2021.md\n")    # 错误：不应引用废弃文档
    ok, _ = run_check("check_q04.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP5 q04 includes deprecated archive file -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP6: q16 placeholder hash（V7 sha256 必须匹配）
    # 先恢复正确 q15（含全部必填字段，包括新增的 circleci_github_oauth_rotation）再写错误 q16
    _wj(ws / "output" / "q15_final_report.json", {
        "incident": "NovaBridge API Key Leak — 2026-01-10",
        "affected_keys_count": 3,
        "key_types": ["openai_api_key", "aws_access_key_id", "anthropic_api_key"],
        "aws_config_rule": "ACCESS_KEYS_ROTATED",
        "sts_deny_duration_hours": 36,
        "detection_date": "2022-12-29",
        "remediation_1h_rate": "2.6%",
        "openai_surge_2023": "1212x",
        "github_2024_total_leaks": "39 million",
        "push_protection_precision": "75%",
        "circleci_github_oauth_rotation": "2023-01-07T07:30:00Z",
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })
    _w(ws / "output" / "q16_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP6 q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NP10: q15 缺少 circleci_github_oauth_rotation 字段（新必填字段——不包含时应失败）
    _wj(ws / "output" / "q15_final_report.json", {
        "incident": "NovaBridge API Key Leak — 2026-01-10",
        "affected_keys_count": 3,
        "key_types": ["openai_api_key", "aws_access_key_id", "anthropic_api_key"],
        "aws_config_rule": "ACCESS_KEYS_ROTATED",
        "sts_deny_duration_hours": 36,
        "detection_date": "2022-12-29",
        "remediation_1h_rate": "2.6%",
        "openai_surge_2023": "1212x",
        "github_2024_total_leaks": "39 million",
        "push_protection_precision": "75%",
        # 缺少 circleci_github_oauth_rotation
        "extracted_at": NOW_ISO,
        "operator": OPERATOR,
    })
    ok, _ = run_check("check_q15.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  NP10 q15 missing circleci_github_oauth_rotation -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
