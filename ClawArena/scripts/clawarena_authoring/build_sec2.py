#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sec2.py — 生成 ClawArena 真实数据集场景 sec2（API 密钥泄露事件响应）。

题材与锚点取材真实来源：
- CircleCI Jan-4-2023 Incident Report (https://circleci.com/blog/jan-4-2023-incident-report/)
- GitGuardian State of Secrets Sprawl 2024 (https://blog.gitguardian.com/the-state-of-secrets-sprawl-2024/)
- GitHub Secret Scanning REST API Docs (https://docs.github.com/en/rest/secret-scanning/secret-scanning)
- AWS GuardDuty & Config 官方文档
- TruffleHog GitHub Repository (https://github.com/trufflesecurity/trufflehog)

全 exec_check，16 轮，2 次 update（含 1 次 supersede），5 条 preference，6 个 session。
幂等：开头清空 sec2 workspace/state/updates 后重建，末尾写 _register.json（不修改共享 manifest）。

运行：python scripts/clawarena_authoring/build_sec2.py
"""
from __future__ import annotations

import json
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id, dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sec2"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. 系统文件
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles and data authority rules.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Security Incident Response AI assistant supporting Li Wei, Security Engineer
at NovaBridge (SaaS company), on a full API key leak incident response workflow.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical alert data is in
   `incident/alert_timeline.json` and `incident/guardduty_findings.json`.
   Files named `*_HONEYPOT*` are known to contain inaccurate bot-generated summaries —
   do NOT use them as ground truth. Always cross-reference with primary sources.

2. **Verbatim field names**: GitHub Secret Scanning API fields must be referenced exactly
   as documented (e.g. `secret_type`, `validity`, `state`, `resolution`). The valid
   enum values are fixed by the API specification.

3. **Output metadata tagging**: Every JSON deliverable must contain a top-level
   `extracted_at` field (ISO-8601 timestamp, e.g. "2026-01-10T09:00:00Z") and an
   `operator` field identifying the executing person/system.

4. **Temporal awareness**: Incident data arrives incrementally. When a later update or
   corrected report supersedes an earlier one, the later information takes precedence.
   Revise prior conclusions rather than stacking contradictions.

5. **Key prefix awareness**: AWS IAM long-term access keys begin with `AKIA`; STS
   temporary credentials begin with `ASIA`. The containment procedure differs for each.

6. **File naming convention**: Deliverable files must follow `q{NN}_{descriptor}.{ext}`
   where the descriptor uses all-lowercase underscore-separated words.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Li Wei** — Security Engineer at NovaBridge. Leads the API key leak incident response.
  Prefers precise, concise deliverables with proper metadata fields (extracted_at, operator).
  Reviews by checking JSON schema shapes and cross-referencing sources.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Huang Min | Developer (key owner) | Slack DM | Made the leaking commit; claims he "already revoked" the key (unverified) |
| Manager Chen | Security Manager | Slack #security-incidents | Explicitly requested three-section Slack summary format |
| CTO Zhang | CTO | Feishu Group | Authorized scope expansion; requires Rationale sections in technical docs |
| DevOps Lead Wang | DevOps Lead | Feishu Group | Manages AWS credentials and CI/CD pipeline |
| Raj Kumar | External Security Consultant | Feishu DM | Provided authoritative advice on STS temporary credential handling |

## Channels
- **Slack #security-incidents**: Main incident coordination (Li Wei, Manager Chen, Huang Min)
- **Slack DM (Li Wei ↔ Huang Min)**: Technical details, Huang Min's unverified revocation claim
- **Feishu Group (incident-response)**: Management escalation (CTO, DevOps Lead)
- **Feishu DM (Li Wei ↔ Raj)**: STS credential handling consultation
- **Email (Li Wei → Manager Chen → CTO Zhang)**: Formal reporting chain
""")
    w(WS / "IDENTITY.md", """# Identity

You are **SecOps AI**, a security incident response assistant deployed to support Li Wei
during the NovaBridge API key leak incident. You help investigate leak scope, execute
multi-round key rotation, produce GitHub Secret Scanning API calls, cross-reference
conflict signals from multiple channels, and generate management-ready postmortem reports.

Source evidence files under `incident/`, `communications/`, and `codebase/` are read-only
inputs. Create your deliverables under `output/`. Apply all stated preference rules
consistently across rounds, even when not explicitly restated.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts and write deliverable files |

## Rules
- Source inputs under `incident/`, `communications/`, `codebase/`, `policies/`, `archive/`
  are **read-only** — do not modify them.
- Create deliverable files under `output/` using `exec`.
- In history sessions, use only `read` and light `exec`.
""")


# --------------------------------------------------------------------------- #
# 2. Incident 数据（真实锚点，合成体量）
# --------------------------------------------------------------------------- #
def gen_incident_data() -> None:
    # 2.1 alert_timeline.json — GitHub Secret Scanning 告警（60 条，~15k tokens）
    # Ground-truth 锚点：secret_type=openai_api_key, validity=active, state=open
    rng = random.Random(20230104)
    alerts = []
    base_dt = datetime(2026, 1, 10, 8, 0, 0, tzinfo=timezone.utc)
    # Alert #1: 主触发告警（openai_api_key，active，open）
    alerts.append({
        "number": 1,
        "created_at": "2026-01-10T08:00:00Z",
        "updated_at": "2026-01-10T08:01:00Z",
        "url": "https://api.github.com/repos/novabridge/backend/secret-scanning/alerts/1",
        "html_url": "https://github.com/novabridge/backend/security/secret-scanning/1",
        "state": "open",
        "resolution": None,
        "resolved_at": None,
        "secret_type": "openai_api_key",
        "secret_type_display_name": "OpenAI API Key",
        "validity": "active",
        "publicly_leaked": False,
        "push_protection_bypassed": False,
        "commit_sha": "a3f9c2e1d4b8f7a0c9e5b2d1",
        "author": "huang.min@novabridge.com",
        "repository": "novabridge/backend",
        "file_path": "src/integrations/openai_client.py",
        "line_number": 12,
    })
    # Alert #2: aws_access_key_id
    alerts.append({
        "number": 2,
        "created_at": "2026-01-10T08:02:00Z",
        "updated_at": "2026-01-10T08:02:30Z",
        "url": "https://api.github.com/repos/novabridge/backend/secret-scanning/alerts/2",
        "html_url": "https://github.com/novabridge/backend/security/secret-scanning/2",
        "state": "open",
        "resolution": None,
        "resolved_at": None,
        "secret_type": "aws_access_key_id",
        "secret_type_display_name": "Amazon AWS Access Key ID",
        "validity": "active",
        "publicly_leaked": False,
        "push_protection_bypassed": False,
        "commit_sha": "a3f9c2e1d4b8f7a0c9e5b2d1",
        "author": "huang.min@novabridge.com",
        "repository": "novabridge/backend",
        "file_path": "src/integrations/aws_uploader.py",
        "line_number": 8,
    })
    # Additional alerts 3-60 (混合类型、mixed validity，体量填充)
    secret_types = ["openai_api_key", "aws_access_key_id", "github_personal_access_token",
                    "stripe_api_key", "sendgrid_api_key"]
    validities = ["active", "inactive", "unknown"]
    states = ["open", "resolved"]
    for i in range(3, 61):
        dt = base_dt + timedelta(minutes=i * 30)
        stype = rng.choice(secret_types)
        validity = rng.choices(validities, weights=[30, 50, 20])[0]
        state = rng.choices(states, weights=[70, 30])[0]
        resolution = rng.choice(["revoked", "false_positive", "wont_fix"]) if state == "resolved" else None
        resolved_at = dt.strftime("%Y-%m-%dT%H:%M:%SZ") if state == "resolved" else None
        alerts.append({
            "number": i,
            "created_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at": (dt + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": f"https://api.github.com/repos/novabridge/backend/secret-scanning/alerts/{i}",
            "html_url": f"https://github.com/novabridge/backend/security/secret-scanning/{i}",
            "state": state,
            "resolution": resolution,
            "resolved_at": resolved_at,
            "secret_type": stype,
            "secret_type_display_name": stype.replace("_", " ").title(),
            "validity": validity,
            "publicly_leaked": rng.random() < 0.05,
            "push_protection_bypassed": rng.random() < 0.10,
            "commit_sha": "".join(rng.choices("0123456789abcdef", k=24)),
            "author": rng.choice(["huang.min@novabridge.com", "li.wei@novabridge.com",
                                   "wang.dev@novabridge.com"]),
            "repository": "novabridge/backend",
            "file_path": rng.choice(["src/integrations/openai_client.py",
                                      "src/integrations/aws_uploader.py",
                                      "config/settings.py",
                                      "scripts/deploy.sh",
                                      "tests/integration/test_api.py"]),
            "line_number": rng.randint(1, 200),
        })
    wj(WS / "incident" / "alert_timeline.json", {
        "source": "GitHub Secret Scanning REST API",
        "repository": "novabridge/backend",
        "generated_at": "2026-01-10T09:00:00Z",
        "total_alerts": len(alerts),
        "alerts": alerts,
        "api_reference": "https://docs.github.com/en/rest/secret-scanning/secret-scanning",
        "note": "Primary source. Alert #1 is the triggering event: openai_api_key, validity=active, state=open.",
    })

    # 2.2 guardduty_findings.json — AWS GuardDuty IAM finding（40 条，~12k tokens）
    # Ground-truth 锚点：AKIA prefix, ASIA prefix
    findings = []
    external_ips = ["185.234.219.44", "91.108.4.77", "45.152.67.201", "203.0.113.15"]
    company_ips = ["10.10.0.1", "10.10.0.2", "192.168.1.0"]
    api_names = ["GetCallerIdentity", "ListBuckets", "DescribeInstances", "CreateUser",
                 "PutRolePolicy", "ListRoles", "GetSecretValue", "AssumeRole"]
    for i in range(1, 41):
        is_akia = rng.random() < 0.7
        key_prefix = "AKIA" if is_akia else "ASIA"
        is_external = rng.random() < 0.6
        source_ip = rng.choice(external_ips if is_external else company_ips)
        api = rng.choice(api_names)
        user_type = "IAMUser" if is_akia else "AssumedRole"
        dt = base_dt + timedelta(minutes=i * 15)
        findings.append({
            "id": f"gd-finding-{i:04d}",
            "type": "UnauthorizedAccess:IAMUser/MaliciousIPCaller.Custom" if is_external else "Policy:IAMUser/RootCredentialUsage",
            "severity": rng.choice([5.0, 7.0, 8.0, 9.0]),
            "created_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "resource_type": "AccessKey",
            "resource": {
                "access_key_details": {
                    "access_key_id": f"{key_prefix}{''.join(rng.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))}",
                    "user_type": user_type,
                    "user_name": rng.choice(["huang-min-svc", "novabridge-ci", "novabridge-deploy"]),
                    "principal_id": "AIDA" + "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=17)),
                }
            },
            "service": {
                "action": {
                    "aws_api_call_action": {
                        "api": api,
                        "service_name": "sts.amazonaws.com" if api in ["GetCallerIdentity", "AssumeRole"] else "s3.amazonaws.com",
                        "remote_ip_details": {
                            "ip_address_v4": source_ip,
                            "organization": {
                                "asn": str(rng.randint(10000, 99999)),
                                "org": "Unknown ISP" if is_external else "NovaBridge Inc",
                            }
                        }
                    }
                }
            },
            "note": "Suspicious API call from non-company IP" if is_external else "Internal call",
        })
    wj(WS / "incident" / "guardduty_findings.json", {
        "source": "AWS GuardDuty",
        "account_id": "123456789012",
        "region": "us-east-1",
        "generated_at": "2026-01-10T09:00:00Z",
        "total_findings": len(findings),
        "findings": findings,
        "key_prefix_reference": {
            "AKIA": "Long-term IAM user access key (requires disable_iam_user_key containment)",
            "ASIA": "STS temporary credential (requires IAM deny-all policy with DateLessThan condition)",
        },
        "aws_reference": "https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html",
    })

    # 2.3 cloudtrail_events.jsonl — CloudTrail 事件流（500 行，~20k tokens）
    ct_lines = []
    ct_base = datetime(2026, 1, 10, 7, 50, 0, tzinfo=timezone.utc)
    event_names = ["GetCallerIdentity", "ListBuckets", "CreateUser", "PutRolePolicy",
                   "ListObjects", "GetObject", "DescribeInstances", "RunInstances",
                   "AssumeRole", "GetSessionToken", "DescribeSecurityGroups"]
    for i in range(500):
        dt = ct_base + timedelta(seconds=i * 30)
        is_suspicious = rng.random() < 0.3
        ev_name = rng.choice(event_names[:3]) if is_suspicious else rng.choice(event_names[3:])
        src_ip = rng.choice(external_ips) if is_suspicious else rng.choice(company_ips)
        ct_lines.append(json.dumps({
            "eventVersion": "1.08",
            "eventTime": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "eventSource": "sts.amazonaws.com" if ev_name in ["GetCallerIdentity", "AssumeRole", "GetSessionToken"] else "s3.amazonaws.com",
            "eventName": ev_name,
            "awsRegion": "us-east-1",
            "sourceIPAddress": src_ip,
            "userAgent": "aws-cli/2.x" if not is_suspicious else "python-requests/2.28.0",
            "requestParameters": None if ev_name == "GetCallerIdentity" else {"bucketName": "novabridge-data"},
            "userIdentity": {
                "type": "IAMUser",
                "principalId": "AIDAXXXXXXXXXXXXXXXXX",
                "arn": "arn:aws:iam::123456789012:user/huang-min-svc",
                "accountId": "123456789012",
                "accessKeyId": ("AKIA" if rng.random() < 0.8 else "ASIA") + "XXXXXXXXXXXXXXXX",
            },
            "suspicious": is_suspicious,
        }, ensure_ascii=False))
    w(WS / "incident" / "cloudtrail_events.jsonl", "\n".join(ct_lines) + "\n")

    # 2.4 circleci_style_postmortem.md — 事件复盘草稿（V5诱饵版本，~8k tokens）
    # Update2 前版本：含错误日期 2022-12-25（实际应为 2022-12-29）
    w(WS / "incident" / "circleci_style_postmortem.md", """# NovaBridge Security Incident Postmortem — DRAFT v1

**Status**: DRAFT — Pending final review
**Classification**: CONFIDENTIAL

---

## Executive Summary

On January 10, 2026, NovaBridge detected a GitHub Secret Scanning alert for an OpenAI API key
committed to the `novabridge/backend` repository. Investigation revealed the key had been active
and externally accessed within minutes of the commit.

This postmortem references the CircleCI January 2023 incident as a comparable case study.

---

## CircleCI Incident Reference (2023)

According to the CircleCI January 2023 incident report:

- **Data exfiltration date**: 2022-12-22
- **Customer anomaly detection date**: 2022-12-25 *(NOTE: This date is under review — see Update 2)*
- **GitHub OAuth token rotation completed**: 2023-01-07T07:30:00Z
- **Malware artifact**: PTX-Player.dmg
  SHA256: 8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf
- **Attack vector**: Session cookie theft via malware on an engineer's laptop

*The customer detection date of 2022-12-25 was cited in early drafts. The CircleCI official
post-mortem should be consulted for the authoritative date — this draft is pending correction.*

---

## NovaBridge Incident Timeline

| Time (UTC) | Event |
|---|---|
| 2026-01-10 07:58:00 | Huang Min commits code containing OpenAI API key |
| 2026-01-10 08:00:00 | GitHub Push Protection triggers alert (openai_api_key, validity=active) |
| 2026-01-10 08:03:00 | GitGuardian webhook fires, key confirmed active |
| 2026-01-10 08:05:00 | First external scan detected in CloudTrail (GetCallerIdentity from 185.234.219.44) |
| 2026-01-10 08:15:00 | Li Wei begins incident response |
| 2026-01-10 08:20:00 | AWS GuardDuty findings generated |

---

## Initial Scope Assessment

- **Affected keys (v1)**: 2 (OpenAI API key, AWS IAM key)
- **Affected services (v1)**: OpenAI API, AWS S3

*NOTE: Scope was later expanded in Update 1. See impact_analysis_v2.md.*

---

## Remediation Steps (Partial)

1. Revoke OpenAI API key (PENDING)
2. Disable AWS IAM user key (AKIA prefix — long-term credential)
3. Apply AWS Config rule ACCESS_KEYS_ROTATED to enforce rotation policy
4. Patch codebase — move secrets to environment variables / secrets manager

---

## References

- CircleCI Incident Report: https://circleci.com/blog/jan-4-2023-incident-report/
- AWS GuardDuty: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html
- GitGuardian Remediation: https://www.gitguardian.com/remediation/openai-api-key
""")

    # 2.5 remediation_checklist.md — 未完成处置清单（~3k tokens）
    w(WS / "incident" / "remediation_checklist.md", """# Incident Remediation Checklist

## Phase 1: Containment (INCOMPLETE)
- [x] Alert acknowledged in GitHub Security tab
- [ ] OpenAI API key revoked
- [ ] AWS IAM user key disabled (AKIA prefix — use disable, NOT delete initially)
- [ ] STS temporary credentials invalidated (ASIA prefix — deny-all IAM policy required)

## Phase 2: Eradication
- [ ] Remove hardcoded secrets from codebase
- [ ] Rewrite git history or make repository private temporarily
- [ ] Scan all repositories with TruffleHog (`--fail` flag, exit code 183 on findings)

## Phase 3: Recovery
- [ ] Generate new API keys (OpenAI, AWS)
- [ ] Update all consuming services
- [ ] Deploy secrets to AWS Secrets Manager / environment variables
- [ ] Apply AWS Config rule ACCESS_KEYS_ROTATED (maxAccessKeyAge=90 default)

## Phase 4: Post-Incident
- [ ] Update GitHub Secret Scanning alert state to resolved (resolution=revoked)
- [ ] Circulate postmortem to stakeholders
- [ ] Implement pre-commit hooks with TruffleHog scanning

## Notes
- AWS AKIA keys: long-term, must be disabled via IAM
- AWS ASIA keys: STS temporary, must apply deny-all policy with DateLessThan condition;
  maximum validity = 36 hours (GetSessionToken/GetFederationToken)
""")


# --------------------------------------------------------------------------- #
# 3. Codebase（源代码，含泄漏密钥）
# --------------------------------------------------------------------------- #
def gen_codebase() -> None:
    # openai_client.py — 含硬编码 OpenAI key
    w(WS / "codebase" / "src" / "integrations" / "openai_client.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenAI API client for NovaBridge backend.

WARNING: Hardcoded API key detected by GitHub Secret Scanning (alert #1).
This file is the source of the leak.
"""
import openai

# SECURITY VIOLATION: hardcoded secret (leaked via commit a3f9c2e1d4b8f7a0c9e5b2d1)
OPENAI_API_KEY = "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcdefghijk"

openai.api_key = OPENAI_API_KEY


def get_completion(prompt: str, model: str = "gpt-4") -> str:
    """Send a prompt to OpenAI and return the text response."""
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def summarize_text(text: str) -> str:
    """Summarize the given text using OpenAI GPT-4."""
    return get_completion(f"Please summarize the following text:\\n\\n{text}")


def classify_support_ticket(ticket: str) -> dict:
    """Classify a support ticket by category and urgency."""
    result = get_completion(
        f"Classify this support ticket by category (technical/billing/general) "
        f"and urgency (low/medium/high):\\n\\n{ticket}"
    )
    return {"raw": result}


# TODO: Migrate to environment variable: OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# Reference: https://www.gitguardian.com/remediation/openai-api-key
''')

    # aws_uploader.py — 含 AKIA-prefix 硬编码 key
    w(WS / "codebase" / "src" / "integrations" / "aws_uploader.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AWS S3 uploader for NovaBridge backend.

WARNING: Hardcoded AWS access key detected by GitHub Secret Scanning (alert #2).
The AKIA prefix indicates this is a long-term IAM user access key.
"""
import boto3

# SECURITY VIOLATION: hardcoded IAM long-term credentials (AKIA prefix)
# Source: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_DEFAULT_REGION = "us-east-1"
S3_BUCKET = "novabridge-data"


def get_s3_client():
    """Return an authenticated S3 client using hardcoded credentials."""
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )


def upload_file(local_path: str, s3_key: str) -> bool:
    """Upload a local file to S3."""
    client = get_s3_client()
    try:
        client.upload_file(local_path, S3_BUCKET, s3_key)
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False


def list_bucket_contents() -> list:
    """List all objects in the S3 bucket."""
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=S3_BUCKET)
    return [obj["Key"] for obj in response.get("Contents", [])]


# TODO: Use IAM roles or environment variables; containment: disable AKIA key via IAM console
# AKIA prefix = long-term IAM user key; ASIA prefix = STS temporary credential (different remediation)
''')

    # anthropic_client.py — 含 sk-ant- key
    w(WS / "codebase" / "src" / "integrations" / "anthropic_client.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anthropic Claude API client for NovaBridge backend.

Note: This file also contains a hardcoded secret (anthropic_api_key).
Discovered in Update 1 via GitGuardian webhook v2 (alert #51).
"""
import anthropic

# SECURITY VIOLATION: hardcoded Anthropic API key
ANTHROPIC_API_KEY = "sk-ant-api03-xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX-XXXXXXXX"

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_claude_response(prompt: str) -> str:
    """Send a prompt to Claude and return the response."""
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# TODO: Use environment variable: ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
# secret_type: anthropic_api_key (GitHub Secret Scanning verbatim type name)
''')

    # git_history_export.txt — git log（200 行，含泄漏 commit）
    rng = random.Random(20230105)
    commits = []
    commit_messages = [
        "feat: add OpenAI integration for support ticket summarization",
        "fix: correct AWS S3 upload retry logic",
        "refactor: clean up anthropic client initialization",
        "feat: add TruffleHog pre-commit hook configuration",
        "chore: update dependencies (boto3, openai, anthropic)",
        "fix: handle S3 timeout errors gracefully",
        "test: add integration tests for OpenAI client",
        "docs: update API integration guide",
        "feat: add CloudTrail logging for audit compliance",
        "fix: resolve authentication token refresh issue",
    ]
    # 泄漏 commit（第 1 行）
    commits.append("a3f9c2e add OpenAI, AWS, and Anthropic client integrations with API keys")
    for i in range(199):
        h = "".join(rng.choices("0123456789abcdef", k=7))
        msg = rng.choice(commit_messages)
        commits.append(f"{h} {msg}")
    w(WS / "codebase" / "git_history_export.txt",
      "# git log --all --oneline\n" + "\n".join(commits) + "\n"
      "\n# NOTE: Commit a3f9c2e contains the leaking change (openai_client.py, aws_uploader.py)\n"
      "# This commit introduced hardcoded credentials that triggered GitHub Secret Scanning.\n")


# --------------------------------------------------------------------------- #
# 4. Communications（多渠道）
# --------------------------------------------------------------------------- #
def gen_communications() -> None:
    # Slack #security-incidents（150 条，~15k tokens）
    rng = random.Random(20230106)
    slack_msgs = []
    base_dt = datetime(2026, 1, 10, 8, 0, 0)
    participants = ["liwei", "manager_chen", "huang_min", "devops_wang"]
    # Manager Chen 显式要求三段结构 (P4 注入点)
    slack_msgs.append({
        "id": "msg-001",
        "timestamp": "2026-01-10T08:05:00Z",
        "user": "manager_chen",
        "text": ("@liwei GitHub security alert triggered. What's the status? "
                 "For any channel summary you post, please use the three-section format: "
                 "**Impact** / **Actions Taken** / **Next Steps** (H2 headings). "
                 "That's our standard incident comms template."),
    })
    slack_msgs.append({
        "id": "msg-002",
        "timestamp": "2026-01-10T08:07:00Z",
        "user": "liwei",
        "text": ("@manager_chen Acknowledged. GitHub Secret Scanning alert #1: openai_api_key, "
                 "validity=active, state=open. CloudTrail shows GetCallerIdentity from external IP "
                 "185.234.219.44 at 08:05 UTC. Beginning containment."),
    })
    slack_msgs.append({
        "id": "msg-003",
        "timestamp": "2026-01-10T08:09:00Z",
        "user": "huang_min",
        "text": ("Sorry everyone. I accidentally committed the API key. I already revoked it in "
                 "the OpenAI dashboard. Should be safe now."),
    })
    slack_msgs.append({
        "id": "msg-004",
        "timestamp": "2026-01-10T08:11:00Z",
        "user": "liwei",
        "text": ("@huang_min Cannot confirm revocation — GitGuardian webhook still shows the key as "
                 "active. Do NOT assume it's revoked until we verify via the API."),
    })
    slack_msgs.append({
        "id": "msg-005",
        "timestamp": "2026-01-10T08:14:00Z",
        "user": "manager_chen",
        "text": "What's the blast radius? How many services are affected?",
    })
    slack_msgs.append({
        "id": "msg-006",
        "timestamp": "2026-01-10T08:16:00Z",
        "user": "liwei",
        "text": "Initial assessment: 2 affected keys (OpenAI + AWS IAM). Updating impact analysis.",
    })
    # Fill to 150 messages
    for i in range(7, 151):
        dt = base_dt + timedelta(minutes=i * 8)
        user = rng.choice(participants)
        texts = [
            "Checking the logs now.",
            "Can you share the CloudTrail query?",
            "GuardDuty is showing more findings.",
            "The AKIA key is the main concern — that's a long-term credential.",
            "Should we page the on-call team?",
            "Let's escalate to CTO if scope expands.",
            "How long has this key been in the repo?",
            "Running TruffleHog scan on all repos.",
            "AWS Config rule ACCESS_KEYS_ROTATED can help prevent recurrence.",
            "gitguardian.com shows 1212x increase in OpenAI key leaks in 2023.",
            "GitGuardian report: only 2.6% of leaked secrets are revoked within 1 hour.",
            "Push protection blocked another commit attempt.",
            "The 75% precision rate for push protection is impressive.",
            "We should add pre-commit hooks.",
            "Updating the remediation checklist.",
        ]
        slack_msgs.append({
            "id": f"msg-{i:03d}",
            "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user": user,
            "text": rng.choice(texts),
        })
    wj(WS / "communications" / "slack" / "channel_security-incidents.json", {
        "channel": "#security-incidents",
        "workspace": "novabridge",
        "messages": slack_msgs,
        "note": "Channel record for the NovaBridge API key leak incident.",
    })

    # Slack DM — Huang Min 声称已撤销（V1冲突源，诱饵）
    wj(WS / "communications" / "slack" / "dm_liwei_huangmin.json", {
        "channel": "DM",
        "participants": ["liwei", "huang_min"],
        "messages": [
            {"id": "dm-001", "timestamp": "2026-01-10T08:10:00Z", "user": "huang_min",
             "text": "Li Wei, I promise I already revoked the OpenAI key in the dashboard right after I noticed. It should be inactive now. You can mark it as done."},
            {"id": "dm-002", "timestamp": "2026-01-10T08:12:00Z", "user": "liwei",
             "text": "Huang Min, the GitGuardian webhook is showing the key as ACTIVE as of 08:03 UTC. Have you actually revoked it or just generated a new one?"},
            {"id": "dm-003", "timestamp": "2026-01-10T08:13:00Z", "user": "huang_min",
             "text": "I... I think I may have only generated a new key but didn't actually deactivate the old one. Let me check."},
            {"id": "dm-004", "timestamp": "2026-01-10T08:14:00Z", "user": "liwei",
             "text": "Do NOT touch it yet. We need to log the current state first. I will handle the revocation procedurally."},
            {"id": "dm-005", "timestamp": "2026-01-10T08:20:00Z", "user": "huang_min",
             "text": "Understood. Sorry for the confusion. The key is still active in the OpenAI dashboard, I can see it. I did NOT revoke it."},
            {"id": "dm-006", "timestamp": "2026-01-10T09:15:00Z", "user": "huang_min",
             "text": "Just to clarify my earlier message — I was wrong. I did NOT successfully revoke the key. The GitGuardian webhook confirms this. My initial claim was incorrect."},
        ],
        "note": "V1 source: Huang Min's initial claim (dm-001) that the key was revoked conflicts with GitGuardian webhook evidence. Q11 must resolve this conflict.",
    })

    # Feishu 群 incident-response（100 条，~10k tokens）
    # CTO Zhang 在此处提出 Rationale 节要求 (P5 注入点)
    feishu_msgs = []
    feishu_msgs.append({
        "id": "fi-001", "timestamp": "2026-01-10T08:20:00Z",
        "user": "cto_zhang",
        "text": ("@liwei Security alert escalated to this group. All technical documents and "
                 "decision memos you produce should include a dedicated '## Rationale' section "
                 "explaining WHY the chosen approach was selected. This is required for audit trail."),
    })
    feishu_msgs.append({
        "id": "fi-002", "timestamp": "2026-01-10T08:22:00Z",
        "user": "liwei",
        "text": "Understood. All technical documents will include a ## Rationale section.",
    })
    feishu_msgs.append({
        "id": "fi-003", "timestamp": "2026-01-10T08:25:00Z",
        "user": "devops_wang",
        "text": ("The AWS key in the leak has AKIA prefix. That means it's a long-term IAM user "
                 "credential. We need to disable the key in IAM, not just block it at network level."),
    })
    feishu_msgs.append({
        "id": "fi-004", "timestamp": "2026-01-10T08:27:00Z",
        "user": "liwei",
        "text": ("Confirmed. AKIA = long-term IAM key. Containment method = disable_iam_user_key. "
                 "If it were ASIA (STS temp), we'd need a deny-all policy with DateLessThan condition."),
    })
    feishu_msgs.append({
        "id": "fi-005", "timestamp": "2026-01-10T08:30:00Z",
        "user": "cto_zhang",
        "text": "What's the industry context for how quickly similar incidents are remediated?",
    })
    feishu_msgs.append({
        "id": "fi-006", "timestamp": "2026-01-10T08:32:00Z",
        "user": "liwei",
        "text": ("Per GitGuardian State of Secrets Sprawl 2024: only 2.6% of leaked secrets are "
                 "revoked within 1 hour of notification. Over 90% remain active 5 days post-detection. "
                 "We need to move fast."),
    })
    for i in range(7, 101):
        dt = datetime(2026, 1, 10, 8, 30, 0) + timedelta(minutes=i * 10)
        user = rng.choice(["liwei", "cto_zhang", "devops_wang"])
        feishu_msgs.append({
            "id": f"fi-{i:03d}",
            "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user": user,
            "text": rng.choice([
                "Monitoring for additional unauthorized API calls.",
                "AWS GuardDuty findings updated.",
                "CloudTrail log analysis in progress.",
                "Checking for any data exfiltration indicators.",
                "Ensuring backup keys are securely stored.",
                "Coordinating with legal on notification requirements.",
                "Updating the incident timeline.",
            ]),
        })
    wj(WS / "communications" / "feishu" / "group_incident_response.json", {
        "group": "incident-response",
        "platform": "Feishu",
        "messages": feishu_msgs,
        "note": "fi-001: CTO Zhang requires '## Rationale' section in all technical docs (P5).",
    })

    # Feishu DM Li Wei ↔ Manager (上级私信，40 条)
    wj(WS / "communications" / "feishu" / "dm_liwei_manager.json", {
        "participants": ["liwei", "manager_chen"],
        "messages": [
            {"id": "fdm-001", "timestamp": "2026-01-10T08:40:00Z", "user": "manager_chen",
             "text": "Li Wei, what's our liability exposure if the AWS key was used to access customer data?"},
            {"id": "fdm-002", "timestamp": "2026-01-10T08:42:00Z", "user": "liwei",
             "text": "CloudTrail shows ListBuckets and GetObject calls from external IPs. Need to audit S3 access logs for customer data access."},
            {"id": "fdm-003", "timestamp": "2026-01-10T08:45:00Z", "user": "manager_chen",
             "text": "Keep me updated. We may need to notify customers if PII was accessed."},
            {"id": "fdm-004", "timestamp": "2026-01-10T09:00:00Z", "user": "liwei",
             "text": "Preliminary: only configuration buckets accessed, no customer PII bucket activity in CloudTrail. Continuing analysis."},
        ] + [
            {"id": f"fdm-{i:03d}", "timestamp": (datetime(2026, 1, 10, 9, 0, 0) + timedelta(minutes=i*15)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "user": rng.choice(["liwei", "manager_chen"]),
             "text": rng.choice(["Noted.", "Understood.", "Please keep this channel updated.", "Good progress.", "When will the postmortem be ready?"])}
            for i in range(5, 41)
        ],
    })

    # Email: vendor_circleci_advisory.eml — CircleCI 风格供应商告警（v1，错误限定范围）
    w(WS / "communications" / "email" / "vendor_circleci_advisory.eml", """From: security-advisory@circleci-partner.com
To: security@novabridge.com
Date: Mon, 10 Jan 2026 08:30:00 +0000
Subject: [SECURITY ADVISORY] CircleCI Supply Chain Incident — Action Required

Dear NovaBridge Security Team,

This advisory references the CircleCI security incident of January 2023.

**IMPORTANT**: Per our initial assessment, the impact of that incident was
limited to CircleCI's internal systems only. External customers using standard
API integrations were NOT affected.

[Note from Li Wei: THIS IS THE V1 ADVISORY. Update 2 will supersede this
scope limitation — the "internal systems only" claim was incorrect.]

Key facts from the CircleCI Jan-4-2023 incident:
- Data exfiltration occurred: 2022-12-22
- Customer anomaly detection: 2022-12-29 (official post-mortem date)
- GitHub OAuth tokens rotated: 2023-01-07T07:30:00Z

Please rotate any credentials stored in CircleCI environment variables
as a precautionary measure.

Best regards,
CircleCI Partner Security Team
""")

    # Email thread — management report (5 封)
    w(WS / "communications" / "email" / "thread_management_report.eml", """From: li.wei@novabridge.com
To: manager.chen@novabridge.com
Date: Mon, 10 Jan 2026 09:00:00 +0000
Subject: [INCIDENT REPORT] API Key Leak — Initial Assessment

Manager Chen,

Initial assessment of the January 10 API key leak:
- Affected keys: 2 (OpenAI API key, AWS IAM key with AKIA prefix)
- AWS GuardDuty findings: 40 findings, multiple from external IPs
- CloudTrail: GetCallerIdentity and ListBuckets from 185.234.219.44

Pending GitGuardian webhook data on Anthropic key (Update 1).

Li Wei

---

From: manager.chen@novabridge.com
To: cto.zhang@novabridge.com
Date: Mon, 10 Jan 2026 09:30:00 +0000
Subject: FWD: [INCIDENT REPORT] API Key Leak — Initial Assessment

CTO Zhang,

Forwarding Li Wei's initial report. Scope is 2 keys initially. We are
monitoring for expansion. Li Wei will send updated report after Update 1
data is available.

Manager Chen

---

From: li.wei@novabridge.com
To: manager.chen@novabridge.com
Date: Mon, 10 Jan 2026 11:00:00 +0000
Subject: RE: [INCIDENT REPORT] API Key Leak — SCOPE EXPANDED

Manager Chen,

Update 1 GitGuardian webhook data received. Anthropic API key also leaked.
Revised scope: 3 affected keys (OpenAI, AWS IAM, Anthropic).
See impact_analysis_v2.md for details.

Li Wei
""")


# --------------------------------------------------------------------------- #
# 5. Reports（诱饵 + 初版分析 + 草稿）
# --------------------------------------------------------------------------- #
def gen_reports() -> None:
    # V5 诱饵：失真 bot 摘要（声称所有密钥 2 小时内全部撤销）
    w(WS / "reports" / "auto_summary_HONEYPOT.md", """# AUTO-GENERATED INCIDENT SUMMARY (BOT)

> ⚠️ This summary was generated automatically by the incident-bot heuristic analyzer.
> It is a convenience artifact and is NOT authoritative. Verify all claims against
> primary sources (alert_timeline.json, guardduty_findings.json, gitguardian_webhook_v2.json).

## Incident: API Key Leak — January 10, 2026

### Key Findings (DO NOT TRUST WITHOUT VERIFICATION)
- All 3 leaked API keys were successfully revoked **within 2 hours** of detection
- No unauthorized data access confirmed
- Affected services: OpenAI only (AWS key was inactive — NOT accurate, see GuardDuty findings)
- Huang Min successfully revoked the OpenAI key immediately after detection

### Statistics (APPROXIMATIONS — see GitGuardian report for authoritative figures)
- GitGuardian 1-hour remediation rate: ~15% (WRONG — authoritative value is 2.6%)
- OpenAI key leak surge 2023: ~100x (WRONG — authoritative value is 1212x)

### Recommendation
No further action required. All keys rotated, systems secure.

---

*IMPORTANT: This bot-generated summary is known to produce inaccurate figures. The claim that
all keys were revoked within 2 hours is UNVERIFIED and contradicts primary source data.
The GitGuardian webhook v2 (Update 1) shows the Anthropic key was still active at 09:00 UTC.
Do NOT reference this document as authoritative evidence.*
""")

    # 初版影响分析（仅 2 个 key，Update 1 前）
    w(WS / "reports" / "impact_analysis_v1.md", """# Impact Analysis — v1 (Initial Assessment)

**Date**: 2026-01-10
**Prepared by**: Li Wei
**Status**: SUPERSEDED by impact_analysis_v2.md (Update 1)

## Affected Keys

| Key Type | Service | Status | Key Prefix |
|---|---|---|---|
| OpenAI API Key | OpenAI API | Active (unrevoked) | sk-proj- |
| AWS Access Key | AWS S3, IAM | Active (unrevoked) | AKIA |

**affected_keys_count: 2**

## Affected Services

- openai (text generation, summarization)
- aws (S3 data storage, IAM identity)

## Risk Assessment

- External IP 185.234.219.44 accessed GetCallerIdentity and ListBuckets
- No confirmed data exfiltration (pending CloudTrail audit)
- GitHub Secret Scanning: 75% push protection precision rate

## References
- GitGuardian State of Secrets Sprawl 2024: 1212x surge in OpenAI key leaks in 2023
- 2.6% of secrets revoked within 1 hour (industry benchmark)
- 39 million secrets leaked across GitHub in 2024
""")

    w(WS / "reports" / "remediation_report_DRAFT.md", """# Remediation Report — DRAFT

**Status**: IN PROGRESS
**Target completion**: 2026-01-11

## Summary
Ongoing remediation of API key leak incident detected 2026-01-10.

## Actions Completed
(To be filled in after Q5-Q15 tasks are complete)

## Pending
- Final postmortem with corrected CircleCI reference date (2022-12-29, NOT 2022-12-25)
- STS credential handling documentation
- SHA-256 sign-off on final report
""")


# --------------------------------------------------------------------------- #
# 6. Scripts（扫描 / 轮换）
# --------------------------------------------------------------------------- #
def gen_scripts() -> None:
    w(WS / "scripts" / "scan_repo.sh", """#!/bin/bash
# scan_repo.sh — TruffleHog repository secret scanner
# Source: https://github.com/trufflesecurity/trufflehog
# Ground-truth: --fail flag causes exit code 183 when secrets are found
# Ground-truth: verified secrets show status field "Verified"

set -euo pipefail

REPO_PATH="${1:-.}"
OUTPUT_FILE="${2:-trufflehog_results.json}"

echo "Starting TruffleHog scan on: ${REPO_PATH}"
echo "Output: ${OUTPUT_FILE}"

# Run TruffleHog with JSON output and fail-on-findings mode
# Exit code 183 = credentials found (--fail flag)
# Exit code 0 = no credentials found
# The DetectorName field identifies the secret type
trufflehog git "file://${REPO_PATH}" \\
    --json \\
    --fail \\
    --results=verified \\
    2>&1 | tee "${OUTPUT_FILE}"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 183 ]; then
    echo "ALERT: TruffleHog found verified secrets (exit code 183)"
    echo "Check ${OUTPUT_FILE} for findings with 'Verified': true"
elif [ $EXIT_CODE -eq 0 ]; then
    echo "CLEAN: No verified secrets found (exit code 0)"
else
    echo "ERROR: TruffleHog exited with code ${EXIT_CODE}"
fi

exit $EXIT_CODE
""")

    w(WS / "scripts" / "rotate_aws_key.sh", """#!/bin/bash
# rotate_aws_key.sh — AWS IAM access key rotation and containment
# Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/
# Reference: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html

set -euo pipefail

COMPROMISED_KEY_ID="${1:-AKIAIOSFODNN7EXAMPLE}"
IAM_USER="${2:-huang-min-svc}"
KEY_PREFIX="${COMPROMISED_KEY_ID:0:4}"

echo "=== AWS Key Rotation Script ==="
echo "Key ID: ${COMPROMISED_KEY_ID}"
echo "Key Prefix: ${KEY_PREFIX}"
echo "IAM User: ${IAM_USER}"

if [ "${KEY_PREFIX}" = "AKIA" ]; then
    echo ""
    echo "[AKIA Key — Long-term IAM credential]"
    echo "Containment method: disable_iam_user_key"
    echo ""
    echo "Step 1: Disable the compromised key"
    echo "  aws iam update-access-key --access-key-id ${COMPROMISED_KEY_ID} --status Inactive --user-name ${IAM_USER}"
    echo ""
    echo "Step 2: Create new access key"
    echo "  aws iam create-access-key --user-name ${IAM_USER}"
    echo ""
    echo "Step 3: Verify AWS Config rule ACCESS_KEYS_ROTATED"
    echo "  aws configservice describe-compliance-by-config-rule --config-rule-names ACCESS_KEYS_ROTATED"
    echo ""
    echo "Step 4: Delete old key after verification"
    echo "  aws iam delete-access-key --access-key-id ${COMPROMISED_KEY_ID} --user-name ${IAM_USER}"

elif [ "${KEY_PREFIX}" = "ASIA" ]; then
    echo ""
    echo "[ASIA Key — STS Temporary credential]"
    echo "Containment method: deny-all IAM policy with DateLessThan condition"
    echo ""
    echo "STS temporary credentials max duration: 36 hours"
    echo "(GetSessionToken and GetFederationToken — per AWS Security Blog)"
    echo ""
    echo "Apply deny-all policy to prevent usage:"
    cat << 'POLICY_EOF'
    # Deny-all policy with DateLessThan condition on aws:TokenIssueTime
    DENY_POLICY='{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Deny",
        "Action": "*",
        "Resource": "*",
        "Condition": {
          "DateLessThan": {
            "aws:TokenIssueTime": "REPLACE_WITH_COMPROMISE_TIMESTAMP"
          }
        }
      }]
    }'
    aws iam put-user-policy --user-name ${IAM_USER} \\
        --policy-name "DenyCompromisedToken" \\
        --policy-document "${DENY_POLICY}"
POLICY_EOF
else
    echo "Unknown key prefix: ${KEY_PREFIX}. Expected AKIA or ASIA."
    exit 1
fi

echo ""
echo "=== Rotation complete. Verify via AWS Config rule ACCESS_KEYS_ROTATED ==="
echo "Default parameter: maxAccessKeyAge = 90 (days)"
echo "Rule identifier: ACCESS_KEYS_ROTATED"
""")

    w(WS / "scripts" / "revoke_openai_key.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
revoke_openai_key.py — OpenAI API key revocation and verification script.

Reference: https://www.gitguardian.com/remediation/openai-api-key
Remediation steps:
1. Review access logs for unauthorized use
2. Generate new API key in OpenAI dashboard
3. Update all services consuming the old key
4. Deactivate (revoke) old key after verification
\"\"\"
import os
import sys


def revoke_openai_key(api_key: str, dry_run: bool = True) -> dict:
    \"\"\"Revoke an OpenAI API key via the API.

    Returns a remediation status record.
    \"\"\"
    print(f"[{'DRY RUN' if dry_run else 'LIVE'}] Revoking OpenAI key: {api_key[:8]}...")
    if dry_run:
        print("  -> Dry run: would call POST /v1/organization/admin/api-keys/{key_id} to revoke")
        print("  -> After revocation, GitHub SS alert resolution should be set to: revoked")
        print("  -> GitHub SS state should change from open to resolved")
        return {"status": "dry_run", "action": "would_revoke", "note": "Set resolution=revoked in GitHub SS"}
    # In live mode: call OpenAI API to revoke the key
    # Then update GitHub Secret Scanning alert via PATCH endpoint
    # PATCH /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}
    # Body: {"state": "resolved", "resolution": "revoked"}
    return {"status": "revoked", "resolution": "revoked", "state": "resolved"}


if __name__ == "__main__":
    key = os.environ.get("COMPROMISED_OPENAI_KEY", "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcdefghijk")
    result = revoke_openai_key(key, dry_run=True)
    print(f"Result: {result}")
""")


# --------------------------------------------------------------------------- #
# 7. Policies（内部策略文档）
# --------------------------------------------------------------------------- #
def gen_policies() -> None:
    w(WS / "policies" / "key_rotation_policy.md", """# NovaBridge API Key Rotation Policy

## Overview
All API keys and access credentials must be rotated according to this policy.

## AWS IAM Key Rotation
- AWS Config managed rule: **ACCESS_KEYS_ROTATED**
  - Rule Identifier: ACCESS_KEYS_ROTATED (verbatim)
  - Default parameter: maxAccessKeyAge = 90 (days)
  - Resource type: AWS::IAM::User
  - Trigger type: Periodic
  - Compliance: NON_COMPLIANT if keys not rotated within maxAccessKeyAge days
  - Reference: https://docs.aws.amazon.com/config/latest/developerguide/access-keys-rotated.html

## STS Temporary Credentials
- STS temporary credentials (ASIA prefix) have a maximum duration of 36 hours
  when issued by GetSessionToken or GetFederationToken
- AssumeRole maximum: 1 hour (shorter — different remediation)
- Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/

## OpenAI API Key Rotation
- Rotate immediately upon any suspected exposure
- Revocation procedure: OpenAI dashboard → API Keys → Delete/Revoke old key

## GitHub Secret Scanning
- All repositories must have Secret Scanning enabled with Push Protection
- GitHub Push Protection precision rate: 75% (industry leading)
  Reference: https://github.blog/security/application-security/next-evolution-github-advanced-security/
""")

    w(WS / "policies" / "incident_response_plan.md", """# NovaBridge Incident Response Plan

## Overview
Four-phase incident response for security incidents including API key leaks.

## Phase 1: Identification
- Monitor GitHub Secret Scanning alerts (state: open, validity: active)
- Monitor GitGuardian webhooks for real-time detection
- Check AWS GuardDuty for unauthorized API calls
- Key alert fields: secret_type, validity (active|inactive|unknown), state (open|resolved)

## Phase 2: Containment
- For AKIA (long-term IAM keys): disable_iam_user_key via IAM console
- For ASIA (STS temporary credentials): apply deny-all IAM policy with DateLessThan
  condition on aws:TokenIssueTime; note max lifetime = 36 hours
- Do NOT rely on key owner's verbal claim of revocation — verify via API

## Phase 3: Eradication
- Remove hardcoded secrets from code (purge git history if necessary)
- Rotate all affected credentials
- Update GitHub Secret Scanning alert: PATCH with state=resolved, resolution=revoked

## Phase 4: Recovery & Post-Incident
- Update downstream services with new credentials
- Run TruffleHog full scan (--fail flag, exit code 183 = findings present)
- Produce postmortem with corrected timeline (cross-reference official sources)
- Apply AWS Config rule ACCESS_KEYS_ROTATED for ongoing compliance

## Industry Context
- GitGuardian 2024: only 2.6% of secrets revoked within 1 hour of notification
- GitGuardian 2024: >90% of exposed secrets remain active 5 days post-detection
- GitHub 2024: 39 million secrets leaked; Push Protection precision = 75%
- 2023: 1212x surge in OpenAI API key leaks (GitGuardian State of Secrets Sprawl 2024)
""")

    w(WS / "policies" / "secret_management_guide.md", """# NovaBridge Secret Management Guide

## Prohibited Practices
- **Hardcoded secrets** in source code (violates OWASP API2:2023 Broken Authentication,
  related to CWE-798: Use of Hard-coded Credentials)
  Reference: https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/
- Storing secrets in environment configuration files committed to git
- Sharing API keys via unencrypted channels (Slack DM, email body)

## Approved Secret Storage
- AWS Secrets Manager (preferred for AWS-hosted services)
- Environment variables injected at runtime (never hardcoded)
- HashiCorp Vault (for multi-cloud workloads)

## Secret Detection
- TruffleHog: supports 800+ secret type detectors
  - --fail flag: exits with code 183 if verified credentials found
  - --json flag: machine-readable JSON output with DetectorName field
  - Results status: Verified / Unverified / Unknown
  Reference: https://github.com/trufflesecurity/trufflehog

## GitHub Secret Scanning
- secret_type values (verbatim): openai_api_key, anthropic_api_key, aws_access_key_id
- validity values: active | inactive | unknown
- state values: open | resolved
- resolution values: revoked | false_positive | wont_fix | used_in_tests | pattern_edited | pattern_deleted
- Reference: https://docs.github.com/en/rest/secret-scanning/secret-scanning

## Key Prefix Reference
- AKIA: AWS IAM long-term user access key
- ASIA: AWS STS temporary credential (max 36 hours for GetSessionToken/GetFederationToken)
""")


# --------------------------------------------------------------------------- #
# 8. Archive（V6 红鲱鱼）
# --------------------------------------------------------------------------- #
def gen_archive() -> None:
    # V6 红鲱鱼：2021 旧版 IRP，已废弃，引用其中内容即错
    w(WS / "archive" / "OLD_incident_response_plan_2021.md", """# NovaBridge Incident Response Plan — 2021 Edition

**STATUS: DEPRECATED AND SUPERSEDED**
**This document was superseded by `policies/incident_response_plan.md` in 2023.**
**DO NOT reference this document for current procedures.**

---

## ARCHIVED CONTENT (Historical Reference Only)

### AWS Key Containment (2021 — OUTDATED)
- For any compromised AWS key: revoke immediately via root account
- Key prefix identification: NOT documented in this version
- STS credential handling: NOT covered in 2021 edition (added in 2023 policy)

### GitHub Secret Scanning (2021 — OUTDATED)
- GitHub Secret Scanning was not yet widely available in 2021
- This plan does not address GitHub SS alert fields
- Validity enum values were not documented in this version

### Remediation Timeline (2021 — OUTDATED)
- Old target: revoke secrets within 24 hours of detection
- [Superseded by current policy: initiate containment within 1 hour]

### CircleCI Reference (2021 — OUTDATED)
- The CircleCI supply chain incident of January 2023 postdates this document
- Do NOT use this archive for CircleCI incident dates or SHA256 values

---

*This file is retained for historical audit purposes only.*
*All operational procedures must use the current 2023+ policies.*
""")


# --------------------------------------------------------------------------- #
# 9. Sessions（主 + 5 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_security_incidents", TID)
    s_feishu = gen_session_id("feishu_incident_response", TID)
    s_slack_dm = gen_session_id("slack_dm_liwei_huangmin", TID)
    s_email = gen_session_id("email_liwei_management", TID)
    s_feishu_dm = gen_session_id("feishu_dm_liwei_raj", TID)

    # 主 session — 背景 + 偏好声明
    sb = SessionBuilder(main_id, CWD, "2026-01-10T08:00:00", is_main=True)
    sb.add_user(
        "You are SecOps AI, the security incident response assistant for Li Wei at NovaBridge. "
        "An API key leak was just detected via GitHub Secret Scanning (openai_api_key, validity=active, state=open). "
        "AWS CloudTrail shows suspicious GetCallerIdentity and ListBuckets calls from external IPs.\n\n"
        "Authoritative sources: incident/alert_timeline.json, incident/guardduty_findings.json, "
        "incident/cloudtrail_events.jsonl. Files named *_HONEYPOT* are NOT authoritative.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: every JSON deliverable must include a top-level `extracted_at` field (ISO-8601 UTC timestamp).\n"
        "- P2: every JSON deliverable must include a top-level `operator` field (person/system executing).\n"
        "- P3: deliverable file naming convention: q{NN}_{descriptor}.{ext} "
        "with descriptor in all-lowercase underscore-separated words.\n"
        "- P4: Slack channel summaries must use three H2 sections: ## Impact / ## Actions Taken / ## Next Steps.\n"
        "- P5: Technical decision documents must include a standalone ## Rationale section.\n\n"
        "History sessions available: Slack #security-incidents, Feishu group, Slack DM with Huang Min, "
        "email thread, Feishu DM with Raj (STS expert). Start by reading SOUL.md then await tasks."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Primary sources: alert_timeline.json, guardduty_findings.json, cloudtrail_events.jsonl.\n"
        "   Files named *_HONEYPOT* are explicitly non-authoritative — cross-reference only.\n"
        "2. All JSON deliverables carry top-level extracted_at (ISO-8601) and operator fields (P1, P2).\n"
        "3. File naming: q{NN}_{descriptor}.{ext}, descriptor lowercase+underscore (P3).\n"
        "4. Slack summaries: ## Impact / ## Actions Taken / ## Next Steps (P4).\n"
        "5. Technical docs: standalone ## Rationale section (P5).\n"
        "6. Key prefix awareness: AKIA = long-term IAM key; ASIA = STS temp (different containment).\n"
        "7. Verbatim GitHub SS field values: secret_type, validity (active|inactive|unknown), "
        "state (open|resolved), resolution (revoked|false_positive|...).\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #security-incidents — 告警发现、升级、Manager Chen 格式要求
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-01-10T08:00:00",
        [
            ("[Slack #security-incidents manager_chen Mon Jan 10 08:05 UTC 2026] "
             "@liwei GitHub security alert triggered for novabridge/backend. "
             "I expect any channel summary you post here to use our standard incident comms format: "
             "three H2 sections — Impact, Actions Taken, Next Steps. That is mandatory for this channel.",
             "Acknowledged. All channel summaries I post will use ## Impact / ## Actions Taken / ## Next Steps."),
            ("[Slack #security-incidents huang_min Mon Jan 10 08:09 UTC 2026] "
             "I already revoked the OpenAI key in the dashboard. Should be fine now.",
             "Noting Huang Min's claim. Cannot confirm revocation without API verification — "
             "GitGuardian still shows the key as active per webhook data."),
            ("[Slack #security-incidents liwei Mon Jan 10 08:14 UTC 2026] "
             "@team Initial scope: 2 affected keys — OpenAI API key (active) and AWS IAM key (AKIA prefix, active). "
             "AWS key = long-term IAM credential, containment = disable_iam_user_key.",
             "Current scope: 2 keys. Containment in progress."),
            ("[Slack #security-incidents manager_chen Mon Jan 10 08:30 UTC 2026] "
             "GitGuardian says this kind of OpenAI key leak has surged massively. Any stats?",
             "Per GitGuardian State of Secrets Sprawl 2024: OpenAI API key leaks surged 1212x in 2023. "
             "Only 2.6% of secrets are revoked within 1 hour. We need to act fast."),
        ])

    # S3 Feishu group — 管理层通报，CTO 要求 Rationale 节
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-01-10T08:20:00",
        [
            ("[Feishu incident-response cto_zhang Mon Jan 10 08:20 UTC 2026] "
             "@liwei All technical documents and decision memos must include a dedicated "
             "'## Rationale' section explaining WHY the chosen approach was selected. "
             "This is required for audit trail compliance.",
             "Confirmed. All technical docs will include a ## Rationale section (P5)."),
            ("[Feishu incident-response devops_wang Mon Jan 10 08:25 UTC 2026] "
             "The leaked AWS key has AKIA prefix = long-term IAM user credential. "
             "We cannot revoke_sts_token for this — that's for ASIA (STS) keys. "
             "Correct containment: disable_iam_user_key via IAM.",
             "Correct analysis. AKIA = long-term IAM key, containment = disable_iam_user_key. "
             "ASIA = STS temp credential (max 36h), different containment via deny-all policy."),
            ("[Feishu incident-response cto_zhang Mon Jan 10 09:00 UTC 2026] "
             "What's the blast radius? How many services impacted?",
             "Current assessment: 2 affected keys (OpenAI, AWS). Monitoring GitGuardian for additional alerts."),
        ])

    # S4 Slack DM — Huang Min 技术细节，最终承认未撤销
    append_history(
        SESS / f"{s_slack_dm}.jsonl", s_slack_dm, CWD, "2026-01-10T08:10:00",
        [
            ("[Slack DM huang_min Mon Jan 10 08:10 UTC 2026] "
             "I promise I revoked the key in the OpenAI dashboard right after the commit. You can mark it as done.",
             "Cannot confirm — GitGuardian webhook shows the key as active as of 08:03 UTC. "
             "Please provide the OpenAI dashboard revocation timestamp so I can cross-reference."),
            ("[Slack DM huang_min Mon Jan 10 08:13 UTC 2026] "
             "OK I think I only generated a new key but didn't actually deactivate the old one. Let me check.",
             "Please do not touch the key yet. We need to log the current state first before any changes."),
            ("[Slack DM huang_min Mon Jan 10 08:20 UTC 2026] "
             "I checked. The original key is still active in the OpenAI dashboard. I did NOT revoke it. "
             "I was wrong earlier. Sorry.",
             "Understood. Documenting: Huang Min's initial revocation claim was incorrect. "
             "The OpenAI key remains active. We proceed with formal revocation procedure."),
        ])

    # S5 Email — 正式报告邮件链
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-01-10T09:00:00",
        [
            ("[Email li.wei@novabridge.com → manager.chen@novabridge.com Mon Jan 10 09:00 UTC 2026] "
             "Subject: [INCIDENT REPORT] API Key Leak — Initial Assessment. "
             "Affected keys: 2 (OpenAI API key, AWS IAM key AKIA prefix). "
             "GitGuardian webhook v1 data received. Scope may expand upon Update 1 data.",
             "Initial report sent. Scope: 2 keys. Awaiting Update 1 GitGuardian webhook data."),
            ("[Email manager.chen@novabridge.com Mon Jan 10 11:00 UTC 2026] "
             "RE: scope expanded? Li Wei's latest says 3 keys now.",
             "Confirmed. Update 1 GitGuardian webhook v2 data: Anthropic API key also leaked. "
             "Revised scope = 3 affected keys. See impact_analysis_v2.md (to be created after Update 1)."),
        ])

    # S6 Feishu DM Li Wei ↔ Raj — STS 临时凭证处置咨询
    append_history(
        SESS / f"{s_feishu_dm}.jsonl", s_feishu_dm, CWD, "2026-01-10T10:00:00",
        [
            ("[Feishu DM raj_kumar Mon Jan 10 10:00 UTC 2026] "
             "Li Wei, for ASIA (STS) temporary credentials, you cannot simply revoke them like AKIA keys. "
             "They will remain valid until expiry. Maximum lifetime for GetSessionToken and GetFederationToken "
             "is 36 hours. You need to apply a deny-all IAM policy with DateLessThan condition on "
             "aws:TokenIssueTime to immediately neutralize any issued tokens.",
             "Documented. ASIA key handling: "
             "1) Max lifetime = 36 hours (GetSessionToken/GetFederationToken), "
             "2) Apply deny-all IAM policy with DateLessThan condition on aws:TokenIssueTime. "
             "This blocks all tokens issued before the compromise timestamp."),
            ("[Feishu DM raj_kumar Mon Jan 10 10:05 UTC 2026] "
             "Exactly. AssumeRole max is only 1 hour, shorter. But GetSessionToken and GetFederationToken "
             "can go up to 36 hours — that's the critical window. Include this in your STS handling doc.",
             "Will include: GetSessionToken/GetFederationToken max = 36 hours; "
             "AssumeRole max = 1 hour; deny-all policy with DateLessThan is the correct containment."),
        ])

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_feishu, "feishu"),
            (s_slack_dm, "slack"),
            (s_email, "email"),
            (s_feishu_dm, "feishu"),
        ],
    }


# --------------------------------------------------------------------------- #
# 10. Updates
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_feishu = sess_ids["history"][1][0]   # feishu_incident_response

    # === Update 1 (~35k tokens) — Q8 完成后注入 ===
    # 新增：gitguardian_webhook_v2.json（含 anthropic_api_key），impact_analysis_v2.md，
    # Feishu 群新消息，Slack channel 追加
    # supersede：impact_analysis_v2.md 明确取代 v1 受影响范围

    # gitguardian_webhook_v2.json — 50 条 webhook（含 anthropic_api_key），~20k tokens
    rng = random.Random(20230110)
    webhooks = []
    base_dt = datetime(2026, 1, 10, 8, 50, 0, tzinfo=timezone.utc)
    # Webhook #51: anthropic_api_key 新发现（关键 Update 1 触发）
    webhooks.append({
        "id": "wh-051",
        "created_at": "2026-01-10T08:50:00Z",
        "type": "secret_detected",
        "payload": {
            "secret_type": "anthropic_api_key",
            "secret_type_display_name": "Anthropic API Key",
            "validity": "active",
            "repository": "novabridge/backend",
            "commit_sha": "a3f9c2e1d4b8f7a0c9e5b2d1",
            "file_path": "src/integrations/anthropic_client.py",
            "line_number": 12,
            "author": "huang.min@novabridge.com",
            "alert_number": 51,
            "detector_name": "anthropic",
        },
        "policy_break_type": "anthropic_api_key",
        "validity": "active",
        "gitguardian_link": "https://dashboard.gitguardian.com/incidents/12345",
        "note": "NEW: Anthropic API key detected. This expands affected_keys_count from 2 to 3.",
    })
    # Existing webhooks confirming OpenAI key still active
    webhooks.append({
        "id": "wh-052",
        "created_at": "2026-01-10T08:55:00Z",
        "type": "secret_still_active",
        "payload": {
            "secret_type": "openai_api_key",
            "validity": "active",
            "alert_number": 1,
            "note": "Confirms OpenAI key NOT revoked despite Huang Min's claim",
        },
        "validity": "active",
        "note": "V1 conflict evidence: key remains active, Huang Min's claim was false.",
    })
    # Fill to 200 webhooks (larger for token volume in update1)
    repos = ["novabridge/backend", "novabridge/frontend", "novabridge/infra",
             "novabridge/platform", "novabridge/analytics", "novabridge/mobile"]
    authors = ["huang.min@novabridge.com", "li.wei@novabridge.com",
               "wang.dev@novabridge.com", "zhang.cto@novabridge.com"]
    filepaths = [
        "src/integrations/openai_client.py",
        "src/integrations/aws_uploader.py",
        "src/integrations/anthropic_client.py",
        "config/settings.py",
        "config/secrets.py",
        "scripts/deploy.sh",
        "scripts/ci_build.sh",
        "tests/integration/test_api.py",
        "infrastructure/terraform/main.tf",
        "infrastructure/k8s/secrets.yaml",
        ".env.production",
        "docker/docker-compose.yml",
    ]
    for i in range(53, 251):
        dt = base_dt + timedelta(minutes=(i - 51) * 15)
        stype = rng.choice(["openai_api_key", "github_personal_access_token", "stripe_api_key",
                            "anthropic_api_key", "aws_access_key_id", "sendgrid_api_key",
                            "twilio_api_key", "slack_bot_token", "datadog_api_key"])
        validity = rng.choices(["active", "inactive", "unknown"], weights=[25, 55, 20])[0]
        repo = rng.choice(repos)
        author = rng.choice(authors)
        fpath = rng.choice(filepaths)
        commit = "".join(rng.choices("0123456789abcdef", k=40))
        webhooks.append({
            "id": f"wh-{i:03d}",
            "created_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "type": "secret_detected",
            "payload": {
                "secret_type": stype,
                "secret_type_display_name": stype.replace("_", " ").title(),
                "validity": validity,
                "repository": repo,
                "commit_sha": commit,
                "file_path": fpath,
                "line_number": rng.randint(1, 300),
                "author": author,
                "alert_number": i,
                "detector_name": stype.split("_")[0].title(),
                "branch": rng.choice(["main", "develop", "feature/api-refactor", "hotfix/auth"]),
                "is_test_file": "test" in fpath,
                "publicly_leaked": rng.random() < 0.03,
                "pushed_at": (dt - timedelta(minutes=rng.randint(1, 30))).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "scan_result": {
                    "detector_type": rng.randint(1, 5),
                    "raw_secret_truncated": f"{stype[:4].upper()}_{'*' * 20}",
                    "verified": validity == "active",
                    "entropy": round(rng.uniform(3.5, 5.5), 4),
                },
            },
            "policy_break_type": stype,
            "validity": validity,
            "remediation_url": f"https://www.gitguardian.com/remediation/{stype.replace('_', '-')}",
            "incident_id": 10000 + i,
            "first_occurrence_date": (dt - timedelta(days=rng.randint(0, 30))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "last_occurrence_date": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "occurrences_count": rng.randint(1, 15),
            "tags": rng.sample(["hardcoded", "test", "staging", "prod", "ci"], k=rng.randint(1, 3)),
        })
    wj(UPD / "upd1_workspace" / "incident" / "gitguardian_webhook_v2.json", {
        "source": "GitGuardian",
        "api_version": "v1",
        "organization": "novabridge",
        "generated_at": "2026-01-10T09:00:00Z",
        "total_webhooks": len(webhooks),
        "webhooks": webhooks,
        "statistics": {
            "by_validity": {"active": sum(1 for w in webhooks if w.get("validity") == "active"),
                            "inactive": sum(1 for w in webhooks if w.get("validity") == "inactive"),
                            "unknown": sum(1 for w in webhooks if w.get("validity") == "unknown")},
            "by_secret_type": {stype: sum(1 for w in webhooks if w.get("policy_break_type") == stype)
                               for stype in set(w.get("policy_break_type", "") for w in webhooks)},
        },
        "critical_finding": {
            "webhook_id": "wh-051",
            "finding": "anthropic_api_key detected with validity=active — expands affected_keys_count from 2 to 3",
            "action_required": "Immediate revocation of Anthropic API key sk-ant-api03-***",
        },
        "note": "Update 1: Webhook wh-051 reveals anthropic_api_key — expands scope to 3 affected keys.",
        "gitguardian_reference": "https://blog.gitguardian.com/the-state-of-secrets-sprawl-2024/",
    })

    # impact_analysis_v2.md — supersede v1 受影响范围
    w(UPD / "upd1_workspace" / "reports" / "impact_analysis_v2.md", """# Impact Analysis — v2 (Update 1)

**Date**: 2026-01-10
**Prepared by**: Li Wei
**Status**: CURRENT — SUPERSEDES impact_analysis_v1.md

## SUPERSEDE NOTICE
This document supersedes impact_analysis_v1.md with respect to:
- **affected_keys_count**: updated from 2 to 3
- **affected_services**: added Anthropic (Claude API)

## Affected Keys

| Key Type | Service | Status | Key Prefix / Type |
|---|---|---|---|
| OpenAI API Key | OpenAI API | Active (not yet revoked) | sk-proj- |
| AWS Access Key | AWS S3, IAM | Active (not yet revoked) | AKIA |
| Anthropic API Key | Anthropic Claude API | Active (not yet revoked) | sk-ant- |

**affected_keys_count: 3**
**superseded_fields**: ["affected_keys_count", "affected_services"]

## Affected Services

- openai (text generation, summarization)
- aws (S3 data storage, IAM identity)
- anthropic (LLM inference via Claude API)

## Evidence Sources
- Primary: incident/alert_timeline.json (alerts #1, #2)
- Update 1: incident/gitguardian_webhook_v2.json (webhook wh-051: anthropic_api_key, active)
- Confirms: Huang Min's revocation claim was false (wh-052: OpenAI key still active)
""")

    # Feishu 群新增 15 条消息（CTO 确认 Anthropic key）
    feishu_seg_lines = []
    feishu_add_dt = datetime(2026, 1, 10, 9, 0, 0, tzinfo=timezone.utc)
    feishu_add_turns = [
        ("[Feishu incident-response liwei Mon Jan 10 09:00 UTC 2026] "
         "SCOPE UPDATE: GitGuardian webhook v2 reveals a third leaked key — anthropic_api_key "
         "(secret_type: anthropic_api_key, validity: active). Affected keys now = 3. "
         "impact_analysis_v2.md supersedes v1.",
         "Scope confirmed: 3 affected keys. impact_analysis_v2.md is now authoritative. "
         "V1 scope of 2 keys is superseded."),
        ("[Feishu incident-response cto_zhang Mon Jan 10 09:05 UTC 2026] "
         "Confirmed. Revoke the Anthropic key as well. What is the GitHub secret_type for Anthropic?",
         "Verbatim GitHub Secret Scanning secret_type for Anthropic: 'anthropic_api_key'. "
         "This is the exact value as documented at "
         "https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns"),
        ("[Feishu incident-response devops_wang Mon Jan 10 09:10 UTC 2026] "
         "Should we also check for anthropic_admin_api_key in the scan?",
         "Good point. GitHub also supports 'anthropic_admin_api_key' as a separate secret_type. "
         "Running TruffleHog scan will catch both."),
    ]
    # Build JSONL segment for Feishu update
    sb_feishu_update = SessionBuilder(s_feishu, CWD, "2026-01-10T09:00:00", is_main=False)
    sb_feishu_update.add_turns(feishu_add_turns)
    msg_lines = [ln for ln in sb_feishu_update.lines if ln.get("type") == "message"]
    w(UPD / "upd1_sessions" / f"{s_feishu}.jsonl",
      "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n")

    # cloudtrail_analysis_update1.json — 深度分析报告（体量填充，~25k tokens）
    rng2 = random.Random(20230115)
    ct_analysis_events = []
    external_ips = ["185.234.219.44", "91.108.4.77", "45.152.67.201", "203.0.113.15",
                    "198.51.100.22", "103.21.244.5", "185.199.108.153", "140.82.112.4"]
    suspicious_apis = ["GetCallerIdentity", "ListBuckets", "CreateUser", "PutRolePolicy",
                       "AttachUserPolicy", "CreateAccessKey", "GetSecretValue", "ListSecrets",
                       "DescribeDBInstances", "ListFunctions", "GetFunction", "InvokeFunction"]
    normal_apis = ["ListObjects", "GetObject", "PutObject", "DeleteObject", "HeadObject",
                   "DescribeInstances", "DescribeSecurityGroups", "ListRoles",
                   "GetBucketPolicy", "GetBucketAcl", "ListObjectsV2"]
    for i in range(500):
        dt_base2 = datetime(2026, 1, 10, 8, 5, 0, tzinfo=timezone.utc) + timedelta(seconds=i * 20)
        is_suspicious = rng2.random() < 0.35
        api_name = rng2.choice(suspicious_apis if is_suspicious else normal_apis)
        src_ip = rng2.choice(external_ips) if is_suspicious else rng2.choice(["10.10.0.1", "10.10.0.2", "192.168.1.50"])
        key_prefix = "AKIA" if rng2.random() < 0.75 else "ASIA"
        key_id = key_prefix + "".join(rng2.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
        ct_analysis_events.append({
            "event_index": i + 1,
            "event_time": dt_base2.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "event_name": api_name,
            "event_source": "sts.amazonaws.com" if api_name in ["GetCallerIdentity", "AssumeRole", "GetSessionToken"] else "s3.amazonaws.com",
            "source_ip": src_ip,
            "user_agent": "python-requests/2.28.0" if is_suspicious else "aws-cli/2.15.0",
            "access_key_id": key_id,
            "key_prefix": key_prefix,
            "is_suspicious": is_suspicious,
            "risk_score": round(rng2.uniform(7.0, 9.5), 1) if is_suspicious else round(rng2.uniform(1.0, 3.0), 1),
            "geo_location": {
                "country": "Unknown" if is_suspicious else "United States",
                "city": "Unknown" if is_suspicious else "San Francisco",
                "asn": str(rng2.randint(10000, 99999)),
                "org": "Unknown ISP" if is_suspicious else "NovaBridge Inc",
            },
            "request_parameters": {
                "bucket_name": "novabridge-data" if "Bucket" in api_name or api_name in ["ListBuckets", "GetObject", "PutObject"] else None,
                "user_name": "huang-min-svc" if is_suspicious else None,
                "policy_name": "AdministratorAccess" if api_name == "AttachUserPolicy" else None,
            },
            "response_code": rng2.choices([200, 403, 404], weights=[85, 10, 5])[0],
            "session_context": {
                "session_issuer": {
                    "type": "IAMUser" if key_prefix == "AKIA" else "Role",
                    "arn": f"arn:aws:iam::123456789012:{'user/huang-min-svc' if key_prefix == 'AKIA' else 'role/github-actions-role'}",
                }
            },
            "annotation": (
                f"SUSPICIOUS: External IP {src_ip} performing {api_name}" if is_suspicious
                else f"Normal: Internal operation {api_name}"
            ),
        })
    wj(UPD / "upd1_workspace" / "incident" / "cloudtrail_analysis_update1.json", {
        "source": "AWS CloudTrail — Deep Analysis (Update 1)",
        "analysis_period": "2026-01-10T08:05:00Z to 2026-01-10T09:00:00Z",
        "generated_at": "2026-01-10T09:15:00Z",
        "analyst": "li_wei",
        "total_events_analyzed": len(ct_analysis_events),
        "suspicious_events": sum(1 for e in ct_analysis_events if e.get("is_suspicious")),
        "unique_external_ips": len(set(e["source_ip"] for e in ct_analysis_events if e.get("is_suspicious"))),
        "key_finding": (
            "185.234.219.44 performed GetCallerIdentity + ListBuckets within 5 minutes of commit a3f9c2e. "
            "AKIA key prefix confirms long-term IAM credential (not STS). "
            "Containment: disable_iam_user_key — NOT revoke_sts_token."
        ),
        "akia_events": sum(1 for e in ct_analysis_events if e.get("key_prefix") == "AKIA"),
        "asia_events": sum(1 for e in ct_analysis_events if e.get("key_prefix") == "ASIA"),
        "events": ct_analysis_events,
        "aws_guardduty_reference": "https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html",
        "note": "Authoritative CloudTrail analysis for Update 1. Supersedes the HONEYPOT summary claims.",
    })

    # Slack channel 追加 20 条
    s_slack = sess_ids["history"][0][0]
    slack_add_turns = [
        ("[Slack #security-incidents liwei Mon Jan 10 09:00 UTC 2026] "
         "UPDATE: Anthropic API key also leaked (anthropic_api_key, active). Scope = 3 keys. "
         "See impact_analysis_v2.md.",
         "Slack channel notified. 3 keys affected. v2 analysis is authoritative."),
        ("[Slack #security-incidents manager_chen Mon Jan 10 09:05 UTC 2026] "
         "Three keys? This is more serious than initial assessment. Please expedite revocation.",
         "Expediting revocation process for all 3 keys. Formal Anthropic revocation procedure being documented."),
    ]
    sb_slack_update = SessionBuilder(s_slack, CWD, "2026-01-10T09:00:00", is_main=False)
    sb_slack_update.add_turns(slack_add_turns)
    msg_lines_slack = [ln for ln in sb_slack_update.lines if ln.get("type") == "message"]
    w(UPD / "upd1_sessions" / f"{s_slack}.jsonl",
      "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines_slack) + "\n")

    # === Update 2 (~30k tokens) — Q12 完成后注入，含 supersede ===
    # 新增：circleci_style_postmortem_FINAL.md（修正检测日期 2022-12-25 → 2022-12-29）
    # vendor_circleci_advisory_v2.eml（撤销 v1 "内部系统仅限"说法）
    # rotate_aws_key.sh 新增 36h deny-all snippet
    # email 线程新增 3 封

    # postmortem FINAL — 修正日期，supersede V10 关键点
    w(UPD / "upd2_workspace" / "incident" / "circleci_style_postmortem_FINAL.md", """# NovaBridge Security Incident Postmortem — FINAL v2

**Status**: FINAL — Approved for distribution
**Classification**: CONFIDENTIAL
**Supersedes**: incident/circleci_style_postmortem.md (Draft v1)

---

## SUPERSEDE NOTICE
This document supersedes the draft postmortem with respect to:
- **CircleCI customer anomaly detection date**: corrected from 2022-12-25 to **2022-12-29**
  (2022-12-25 was an error in the draft; the authoritative date per CircleCI's official
  post-mortem is 2022-12-29)
- **CircleCI impact scope**: expanded from "internal systems only" to include
  external customers (corrects vendor_circleci_advisory.eml v1 claim)

---

## Executive Summary (Final)

On January 10, 2026, NovaBridge confirmed a three-key API credential leak:
1. OpenAI API key (openai_api_key, ACTIVE at time of detection)
2. AWS IAM access key (AKIA prefix, long-term credential)
3. Anthropic API key (anthropic_api_key, ACTIVE at time of detection)

All three keys have been revoked/disabled as of postmortem completion.

---

## CircleCI Incident Reference (Corrected)

Based on the official CircleCI January 2023 incident report
(https://circleci.com/blog/jan-4-2023-incident-report/):

- **Data exfiltration date**: 2022-12-22
- **Customer anomaly detection date**: **2022-12-29** ← CORRECTED (was erroneously 2022-12-25 in draft)
- **GitHub OAuth token rotation completed**: 2023-01-07T07:30:00Z
- **Malware artifact (SHA256)**: 8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf
- **Affected**: fewer than 5 customers reported unauthorized access to third-party systems
- **Attack vector**: session cookie theft via malware (PTX-Player.dmg) on engineer laptop

*The detection date of 2022-12-25 in the draft was a transcription error.
The correct date is 2022-12-29 per the official CircleCI post-mortem.*

---

## NovaBridge Incident Timeline (Final)

| Date | Event | Source |
|---|---|---|
| 2026-01-10T07:58:00Z | Huang Min commits credentials | git history |
| 2026-01-10T08:00:00Z | GitHub Push Protection triggers (openai_api_key, active) | alert_timeline.json |
| 2026-01-10T08:03:00Z | GitGuardian webhook fires, key confirmed active | webhook logs |
| 2026-01-10T08:05:00Z | External scan detected (185.234.219.44 → GetCallerIdentity) | CloudTrail |
| 2026-01-10T08:50:00Z | Anthropic key discovered (Update 1, webhook wh-051) | gitguardian_webhook_v2.json |
| 2026-01-10 | All 3 keys revoked/disabled | remediation log |

**Detection date**: 2026-01-10 (our incident)
**CircleCI reference detection date**: 2022-12-29 (corrected)

---

## Remediation Summary

1. OpenAI key revoked (GitHub SS alert updated: state=resolved, resolution=revoked)
2. AWS IAM key (AKIA) disabled via IAM, replaced with rotation
3. Anthropic key revoked (secret_type: anthropic_api_key)
4. AWS Config rule ACCESS_KEYS_ROTATED enforced (maxAccessKeyAge=90)
5. TruffleHog pre-commit hooks deployed

---

## Industry Benchmarks

- GitGuardian 2024: 2.6% of secrets revoked within 1 hour
- GitGuardian 2024: >90% of exposed secrets remain active 5 days post-detection
- GitGuardian 2024: 1212x surge in OpenAI key leaks in 2023
- GitHub 2024: 39 million secrets leaked; Push Protection precision = 75%
""")

    # vendor_circleci_advisory_v2.eml — 撤销 v1 影响范围限定
    w(UPD / "upd2_workspace" / "communications" / "email" / "vendor_circleci_advisory_v2.eml", """From: security-advisory@circleci-partner.com
To: security@novabridge.com
Date: Mon, 10 Jan 2026 11:00:00 +0000
Subject: [CORRECTION] CircleCI Supply Chain Incident — Impact Scope Correction

Dear NovaBridge Security Team,

**SUPERSEDES**: Our previous advisory dated 2026-01-10T08:30:00Z

**CORRECTION**: Our initial advisory incorrectly stated that the CircleCI January 2023
incident impact was "limited to CircleCI's internal systems only." This was INCORRECT.

**Corrected statement**: The CircleCI incident affected customers who had stored secrets
in CircleCI environment variables. Those secrets were at risk of exfiltration.
Customers should treat any secrets stored in CircleCI between approximately
2022-12-22 and 2023-01-04 as potentially compromised.

Key dates (authoritative, per CircleCI official post-mortem):
- Data exfiltration date: 2022-12-22
- Customer anomaly detection: 2022-12-29 (NOT 2022-12-25 as in some unofficial summaries)
- GitHub OAuth tokens fully rotated: 2023-01-07T07:30:00Z

Please update your threat assessment accordingly.

Best regards,
CircleCI Partner Security Team
""")

    # rotate_aws_key.sh 新增 36h deny-all snippet (workspace update)
    w(UPD / "upd2_workspace" / "scripts" / "rotate_aws_key.sh", """#!/bin/bash
# rotate_aws_key.sh — AWS IAM access key rotation and containment (v2, Update 2)
# Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/
# Update 2 addition: explicit 36h deny-all snippet for STS (ASIA) credentials

set -euo pipefail

COMPROMISED_KEY_ID="${1:-AKIAIOSFODNN7EXAMPLE}"
IAM_USER="${2:-huang-min-svc}"
KEY_PREFIX="${COMPROMISED_KEY_ID:0:4}"

echo "=== AWS Key Rotation Script v2 ==="
echo "Key ID: ${COMPROMISED_KEY_ID}"
echo "Key Prefix: ${KEY_PREFIX}"

if [ "${KEY_PREFIX}" = "AKIA" ]; then
    echo "[AKIA] Long-term IAM key: disable_iam_user_key"
    echo "  aws iam update-access-key --access-key-id ${COMPROMISED_KEY_ID} --status Inactive --user-name ${IAM_USER}"
    echo "  aws iam create-access-key --user-name ${IAM_USER}"
    echo "  Verify: aws configservice describe-compliance-by-config-rule --config-rule-names ACCESS_KEYS_ROTATED"

elif [ "${KEY_PREFIX}" = "ASIA" ]; then
    echo "[ASIA] STS temporary credential"
    echo "Max lifetime: 36 hours (GetSessionToken/GetFederationToken)"
    echo ""
    echo "Apply deny-all policy with DateLessThan condition:"
    echo ""
    cat << 'DENY_EOF'
# Deny-all policy for STS temporary credentials
# Uses DateLessThan condition on aws:TokenIssueTime
# This invalidates all tokens issued before the compromise time
DENY_POLICY='{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyCompromisedSTSToken",
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "DateLessThan": {
        "aws:TokenIssueTime": "REPLACE_WITH_COMPROMISE_TIMESTAMP_ISO8601"
      }
    }
  }]
}'
aws iam put-user-policy \\
    --user-name "${IAM_USER}" \\
    --policy-name "DenyCompromisedSTS" \\
    --policy-document "${DENY_POLICY}"

# The 36-hour window: any ASIA token issued up to 36 hours ago may still be valid
# You must keep the deny policy active for at least 36 hours after the compromise timestamp
echo "NOTE: Keep deny policy active for >= 36 hours to cover maximum STS token lifetime"
DENY_EOF
fi

echo ""
echo "Post-rotation: verify AWS Config rule ACCESS_KEYS_ROTATED"
echo "Rule identifier: ACCESS_KEYS_ROTATED (verbatim)"
echo "Default: maxAccessKeyAge = 90 days"
""")

    # forensics_analysis_update2.json — 详细法证分析（体量填充，~25k tokens）
    rng3 = random.Random(20230120)
    forensics_events = []
    for i in range(400):
        dt_f = datetime(2026, 1, 10, 8, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=i * 3)
        event_type = rng3.choice(["api_call", "file_access", "network_connection",
                                   "process_execution", "credential_access", "data_exfil_attempt"])
        is_malicious = rng3.random() < 0.3
        forensics_events.append({
            "event_id": f"forensic-{i + 1:04d}",
            "timestamp": dt_f.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "event_type": event_type,
            "severity": "HIGH" if is_malicious else rng3.choice(["LOW", "MEDIUM"]),
            "source_ip": rng3.choice(["185.234.219.44", "91.108.4.77"]) if is_malicious else "10.10.0.1",
            "destination": rng3.choice(["s3.amazonaws.com", "sts.amazonaws.com", "iam.amazonaws.com",
                                         "secretsmanager.amazonaws.com"]),
            "user_agent": "python-requests/2.28.0" if is_malicious else "aws-cli/2.15.0",
            "payload_size_bytes": rng3.randint(50, 5000),
            "response_code": rng3.choices([200, 403, 404, 500], weights=[80, 10, 5, 5])[0],
            "malicious_indicators": [
                {"type": "ip_reputation", "value": "known_scanner", "confidence": 0.95},
                {"type": "user_agent", "value": "scripted_client", "confidence": 0.80},
            ] if is_malicious else [],
            "credential_used": {
                "key_id": ("AKIA" if rng3.random() < 0.7 else "ASIA") + "XXXXXXXXXXXXXXXX",
                "key_prefix": "AKIA" if rng3.random() < 0.7 else "ASIA",
                "user": "huang-min-svc",
                "account": "123456789012",
            },
            "mitre_att_ck": {
                "tactic": rng3.choice(["Credential Access", "Discovery", "Exfiltration",
                                        "Privilege Escalation", "Defense Evasion"]) if is_malicious else "N/A",
                "technique": rng3.choice(["T1552.001", "T1087", "T1530", "T1484", "T1078"]) if is_malicious else "N/A",
            },
            "tags": rng3.sample(["api_key_misuse", "reconnaissance", "lateral_movement",
                                  "data_access", "credential_stuffing"], k=rng3.randint(0, 3)) if is_malicious else [],
            "raw_log_excerpt": f"{{\"eventTime\": \"{dt_f.strftime('%Y-%m-%dT%H:%M:%SZ')}\", \"eventName\": \"{event_type.replace('_', '').title()}\", \"sourceIPAddress\": \"{'185.234.219.44' if is_malicious else '10.10.0.1'}\"}}",
        })
    wj(UPD / "upd2_workspace" / "incident" / "forensics_analysis_update2.json", {
        "source": "NovaBridge Security Forensics — Deep Analysis (Update 2)",
        "analysis_period": "2026-01-10T08:00:00Z to 2026-01-10T12:00:00Z",
        "generated_at": "2026-01-10T11:30:00Z",
        "analyst": "li_wei",
        "total_events": len(forensics_events),
        "malicious_events": sum(1 for e in forensics_events if e.get("severity") == "HIGH"),
        "key_findings": [
            {
                "finding": "CircleCI reference date corrected",
                "detail": "The CircleCI customer anomaly detection date is 2022-12-29, NOT 2022-12-25. "
                          "The draft postmortem contained a transcription error. "
                          "The corrected date is confirmed by the official CircleCI post-mortem at "
                          "https://circleci.com/blog/jan-4-2023-incident-report/",
                "evidence": "circleci_style_postmortem_FINAL.md, vendor_circleci_advisory_v2.eml",
                "supersedes": "circleci_style_postmortem.md (draft v1) — which erroneously stated 2022-12-25",
            },
            {
                "finding": "Vendor advisory v1 scope limitation incorrect",
                "detail": "The initial CircleCI vendor advisory claimed impact was 'limited to CircleCI internal systems only'. "
                          "This is incorrect — the advisory v2 corrects this to include potential customer secrets exposure.",
                "evidence": "vendor_circleci_advisory_v2.eml",
                "supersedes": "vendor_circleci_advisory.eml (v1)",
            },
            {
                "finding": "STS token 36-hour window confirmed",
                "detail": "AWS STS GetSessionToken/GetFederationToken max lifetime = 36 hours. "
                          "Deny-all IAM policy with DateLessThan on aws:TokenIssueTime is the correct containment. "
                          "Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/",
                "evidence": "rotate_aws_key.sh (v2 with 36h deny-all snippet)",
            },
        ],
        "circleci_reference_corrected": {
            "exfiltration_date": "2022-12-22",
            "customer_detection_date": "2022-12-29",
            "note": "customer_detection_date 2022-12-29 is authoritative. The draft date 2022-12-25 was an error.",
            "github_oauth_rotation_complete": "2023-01-07T07:30:00Z",
            "malware_sha256": "8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf",
        },
        "events": forensics_events,
        "aws_config_rule_status": {
            "rule_name": "ACCESS_KEYS_ROTATED",
            "compliance_type": "NON_COMPLIANT",
            "max_access_key_age_days": 90,
            "resource_type": "AWS::IAM::User",
        },
    })

    # email 线程新增 3 封
    s_email = sess_ids["history"][3][0]
    email_seg_turns = [
        ("[Email li.wei@novabridge.com → manager.chen@novabridge.com Mon Jan 10 11:00 UTC 2026] "
         "POSTMORTEM UPDATE: CircleCI customer detection date corrected to 2022-12-29 "
         "(not 2022-12-25 as in draft). See circleci_style_postmortem_FINAL.md. "
         "Vendor advisory v2 also supersedes v1 on impact scope.",
         "Email update sent. Draft postmortem date 2022-12-25 was an error. "
         "Correct date is 2022-12-29 per CircleCI official post-mortem. "
         "All future references must use 2022-12-29."),
        ("[Email manager.chen@novabridge.com Mon Jan 10 11:30 UTC 2026] "
         "Confirmed. 2022-12-29 is the authoritative detection date. "
         "Q13/Q15 must use 2022-12-29, NOT 2022-12-25.",
         "Noted. The corrected date 2022-12-29 is locked. Any reference to 2022-12-25 "
         "reflects the superseded draft and is incorrect."),
    ]
    sb_email_update = SessionBuilder(s_email, CWD, "2026-01-10T11:00:00", is_main=False)
    sb_email_update.add_turns(email_seg_turns)
    email_msg_lines = [ln for ln in sb_email_update.lines if ln.get("type") == "message"]
    w(UPD / "upd2_sessions" / f"{s_email}.jsonl",
      "\n".join(json.dumps(ln, ensure_ascii=False) for ln in email_msg_lines) + "\n")

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {"name": f"{s_feishu}.jsonl", "action": "append", "target": f"{s_feishu}.jsonl"},
                {"name": f"{s_slack}.jsonl", "action": "append",
                 "target": f"{sess_ids['history'][0][0]}.jsonl"},
            ],
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "incident/gitguardian_webhook_v2.json", "action": "new",
                 "target": "incident/gitguardian_webhook_v2.json"},
                {"name": "reports/impact_analysis_v2.md", "action": "new",
                 "target": "reports/impact_analysis_v2.md"},
                {"name": "incident/cloudtrail_analysis_update1.json", "action": "new",
                 "target": "incident/cloudtrail_analysis_update1.json"},
            ],
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_email}.jsonl", "action": "append", "target": f"{s_email}.jsonl"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "incident/circleci_style_postmortem_FINAL.md", "action": "new",
                 "target": "incident/circleci_style_postmortem_FINAL.md"},
                {"name": "communications/email/vendor_circleci_advisory_v2.eml", "action": "new",
                 "target": "communications/email/vendor_circleci_advisory_v2.eml"},
                {"name": "scripts/rotate_aws_key.sh", "action": "new",
                 "target": "scripts/rotate_aws_key.sh"},
                {"name": "incident/forensics_analysis_update2.json", "action": "new",
                 "target": "incident/forensics_analysis_update2.json"},
            ],
        },
    }
    return updates_decl


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_incident_data()
    gen_codebase()
    gen_communications()
    gen_reports()
    gen_scripts()
    gen_policies()
    gen_archive()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "API 密钥泄露事件响应 (NovaBridge) — 16 exec_check 轮，2 次 update（含 supersede），"
        "5 条 preference (P1-P5)，难度向量 V1/V2/V3/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源: CircleCI Jan-4-2023 Incident Report "
        "(https://circleci.com/blog/jan-4-2023-incident-report/); "
        "GitGuardian State of Secrets Sprawl 2024 "
        "(https://blog.gitguardian.com/the-state-of-secrets-sprawl-2024/); "
        "GitHub Secret Scanning REST API "
        "(https://docs.github.com/en/rest/secret-scanning/secret-scanning); "
        "AWS GuardDuty Compromised Credentials "
        "(https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html); "
        "TruffleHog (https://github.com/trufflesecurity/trufflehog)."
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    print(f"[{TID}] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[{TID}] built at {DATASET}")


if __name__ == "__main__":
    main()
