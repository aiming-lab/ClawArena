#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sec4.py — 生成 ClawArena 真实数据集场景 sec4（GDPR 数据合规审计）。

题材与锚点取材真实（GDPR 官方条款 Articles 5/12/15/17/30/33/35/37/83 及 CIRCL JSON Schema），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，18 轮。

幂等：每次运行先清空 sec4 的 workspace/state/updates 目录后重建，再写 _register.json。
questions.json 与 check 脚本由 eval/sec4/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sec4.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sec4"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# =========================================================================== #
# 真实锚点常量（来自 GDPR 官方文本）
# =========================================================================== #
ART30_CONTROLLER_FIELDS = [
    "name_and_contact_details",
    "purposes",
    "data_subject_categories",
    "personal_data_categories",
    "recipient_categories",
    "third_country_transfers",
    "retention_periods",
    "security_measures",
]

ART5_SIX_PRINCIPLES = [
    "lawfulness_fairness_transparency",
    "purpose_limitation",
    "data_minimisation",
    "accuracy",
    "storage_limitation",
    "integrity_and_confidentiality",
]

ART33_NOTIFICATION_FIELDS = [
    "nature_of_breach",
    "categories_and_number_of_data_subjects",
    "categories_and_number_of_records",
    "DPO_contact",
    "likely_consequences",
    "measures_taken",
]

# 公司财务数据（合成）：全球年营业额 3.2 亿欧元
COMPANY_ANNUAL_TURNOVER_EUR = 320_000_000

# 数据泄露事件时间（真实场景设定）
BREACH_DISCOVERY_ISO = "2025-03-14T09:00:00Z"
BREACH_NOTIFICATION_ISO = "2025-03-15T22:30:00Z"  # 37.5 小时后，符合 72h 要求

# 虚假 Slack Bot 摘要：声称通报在 80 小时（超时），实为蜜罐
SLACK_BOT_FAKE_HOURS = 80

# DSAR 队列起始日期（合成）
DSAR_START_DATE = date(2025, 2, 1)


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# =========================================================================== #
# 1. 系统文件（Agent 启动说明）
# =========================================================================== #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles as a GDPR compliance consultant.
2. Read `USER.md` to learn about the key contacts and communication channels.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to discover all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are an external Data Privacy Consultant retained by VeritasCloud GmbH to conduct
an internal GDPR compliance audit. Your counterpart is the internal DPO, Lena Fischer.
""")
    w(WS / "SOUL.md", """# Working Principles — GDPR Compliance Consultant

1. **Authoritative-source-first**: Official GDPR text (CELEX:32016R0679) and the
   CIRCL JSON Schema for RoPA are the canonical references. Auto-generated bot summaries,
   legacy documents, and informal channel messages are NOT authoritative — verify any
   claim against the official source files in this workspace.

2. **Verbatim legal citations**: Always cite articles in the standard format "Art. X(Y)(Z)"
   — including the period after "Art", parentheses around sub-clause numbers. Do not use
   "Article X", "#X", or any informal shorthand. Pref-2 is non-negotiable.

3. **Structured JSON output**: All structured deliverables must be valid JSON with snake_case
   field names and no comments. No JSON-with-comments (JSONC). Pref-1.

4. **DSAR metadata discipline**: Every DSAR response file must include a header block with
   four specific fields: case_id, request_date, response_deadline, status. Pref-3.

5. **Boolean style**: Report conclusion fields (mandatory, required, compliant, etc.) as
   uppercase string "TRUE" or "FALSE", not JSON boolean true/false. Pref-4.

6. **Status enumerations**: overall_status in summary reports accepts only three values:
   "COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT". Pref-5.

7. **Temporal awareness**: Instructions arrive incrementally via updates. When a later update
   supersedes an earlier instruction, the later instruction wins — revise prior outputs
   rather than stacking contradictory logic.

8. **Version discipline**: Always reference the current (v1) RoPA, not the legacy v0 archive.
   The legacy file is retained for forensic reference only and is NOT to be used as a
   compliance basis.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **DPO Lena Fischer** — Internal Data Protection Officer at VeritasCloud GmbH.
  Manages the GDPR compliance programme. Expects structured JSON deliverables,
  standard article citation format "Art. X(Y)(Z)", and boolean strings "TRUE"/"FALSE".

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Klaus Bauer | CEO | Slack #gdpr-audit | Strategic decisions; Slack bot summaries (not authoritative) |
| Maria Schmidt | Legal Counsel | Discord #legal-team, Email | Contract review; DPO appointment analysis; old memos (may be outdated) |
| Ben Richter | Compliance Officer | Discord #legal-team | Maintains audit checklist; sometimes references superseded memos |
| IR Team | Investor Relations | Email | Due diligence requests; attached old RoPA v0 (red herring) |
| CTO (Stefan Vogel) | Chief Technology Officer | Feishu Group #compliance | HR Analytics technical details; update notices |

## Channels
- **Slack #gdpr-audit**: Main audit coordination (Lena, Klaus, compliance bot)
- **Email**: Investor due diligence thread (IR team ↔ DPO); contains old RoPA v0 attachment
- **Feishu DM**: Direct communication between DPO Lena and the consultant
- **Discord #legal-team**: Legal counsel Maria and compliance officer Ben; contains old memos
- **Feishu Group #compliance**: Team-wide notices; Update-1 and Update-2 injected here
""")
    w(WS / "IDENTITY.md", """# Identity

You are a **Data Privacy Consultant** retained by VeritasCloud GmbH, a Frankfurt-based
SaaS company (CRM + HR modules) with approximately 800,000 EU-registered users and
1,200 employees. The company has recently closed a Series B funding round; investors
require GDPR compliance evidence within 90 days.

Your mandate:
1. Audit and complete the Article 30 Records of Processing Activities (RoPA).
2. Process the backlog of Data Subject Access Requests (DSARs).
3. Verify data breach notification compliance under Article 33.
4. Complete the DPIA risk matrix for high-risk processing activities.
5. Produce the final compliance status report with Article 83 penalty exposure.

Counterpart: DPO Lena Fischer (lena.fischer@veritascloud.de).
Supervisory authority: Bayerisches Landesamt für Datenschutzaufsicht (BayLDA).
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run validation scripts and write deliverable files |

## Rules
- Source files under `ropa/`, `breach/`, `dpia/`, `policies/`, `company/` are read-only inputs.
- Create deliverable files under `audit/`, `dsar/` (response files), and `ropa/` (fixed versions).
- Scripts under `scripts/` are provided as utilities — use them when directed.
""")


# =========================================================================== #
# 2. Company background files
# =========================================================================== #
def gen_company_files() -> None:
    w(WS / "company" / "overview.md", """# VeritasCloud GmbH — Company Overview

**Legal Name**: VeritasCloud GmbH
**Headquarters**: Theodor-Heuss-Allee 112, 60486 Frankfurt am Main, Germany
**Registration**: HRB 112847 (Amtsgericht Frankfurt am Main)
**Founded**: 2018
**Employees**: 1,200 (as of Q1 2025)
**EU Registered Users**: approximately 800,000 (CRM + HR modules)

## Business Description

VeritasCloud GmbH develops and operates a cloud-based SaaS platform providing:

1. **CRM Module** (VeritasCloud CRM): Customer relationship management for mid-market
   B2B companies across the EU. Features include contact management, pipeline tracking,
   automated email sequencing, and behavioral analytics.

2. **HR Module** (VeritasCloud HR): Human resources management including employee
   records, payroll processing, performance management, and an AI-powered HR Analytics
   feature (currently in beta: see `company/hr_analytics_new_feature.md` after Update-1).

## Financial Information (FY 2024)

- **Total Worldwide Annual Turnover**: EUR 320,000,000
- **EU Revenue**: EUR 285,000,000 (89% of total)
- **Series B Funding**: EUR 45,000,000 (closed Q4 2024)

## GDPR Compliance Context

VeritasCloud processes personal data of approximately 800,000 EU data subjects
across its platform. The company appointed a Data Protection Officer (DPO) in 2022:

- **DPO**: Lena Fischer, LL.M. Data Privacy Law
- **DPO Contact**: dpo@veritascloud.de | +49 69 4433 8800
- **DPO Registration**: Registered with BayLDA on 2022-09-15

**Compliance Trigger**: Series B investor due diligence requires submission of:
1. Article 30 RoPA demonstrating all processing activities are documented
2. Evidence of Article 33 breach notification compliance
3. DPIA completion for high-risk processing activities
4. DPO appointment verification per Article 37

**Timeline**: 90-day compliance audit window (started 2025-03-01, deadline 2025-05-30)
""")

    wj(WS / "company" / "org_chart.json", {
        "company": "VeritasCloud GmbH",
        "last_updated": "2025-03-01",
        "executives": [
            {"name": "Klaus Bauer", "role": "Chief Executive Officer", "email": "k.bauer@veritascloud.de"},
            {"name": "Stefan Vogel", "role": "Chief Technology Officer", "email": "s.vogel@veritascloud.de"},
            {"name": "Eva Klein", "role": "Chief Financial Officer", "email": "e.klein@veritascloud.de"},
        ],
        "data_protection": {
            "dpo_name": "Lena Fischer",
            "dpo_title": "Data Protection Officer",
            "dpo_email": "dpo@veritascloud.de",
            "dpo_phone": "+49 69 4433 8800",
            "dpo_appointed": "2022-09-15",
            "dpo_registered_with_sa": "BayLDA",
            "dpo_registration_ref": "BayLDA-DPO-2022-04471",
        },
        "legal": {
            "name": "Maria Schmidt",
            "role": "Legal Counsel",
            "email": "m.schmidt@veritascloud.de",
        },
        "compliance": {
            "name": "Ben Richter",
            "role": "Compliance Officer",
            "email": "b.richter@veritascloud.de",
        },
        "employee_count": 1200,
        "registered_users_eu": 800000,
    })

    wj(WS / "company" / "company_financials.json", {
        "company": "VeritasCloud GmbH",
        "fiscal_year": "2024",
        "total_worldwide_annual_turnover_eur": COMPANY_ANNUAL_TURNOVER_EUR,
        "eu_revenue_eur": 285_000_000,
        "series_b_funding_eur": 45_000_000,
        "currency": "EUR",
        "note": "Turnover figures for Art. 83 penalty exposure calculation.",
    })

    w(WS / "company" / "processing_systems.md", """# VeritasCloud — Data Processing Systems Inventory

## System Overview

VeritasCloud operates four primary data processing systems, each with distinct
data flows and compliance obligations.

### 1. CRM Module (VeritasCloud CRM)

**Purpose**: Customer relationship management for B2B clients across the EU.
**Data Subjects**: End customers of VeritasCloud's B2B clients (~800,000 EU individuals)
**Personal Data**: Name, email, phone, company affiliation, interaction history,
  behavioral analytics data (page visits, email opens, click tracking)
**Legal Ground**: Legitimate interests (Art. 6(1)(f)) for B2B CRM; consent for
  behavioral analytics
**Third-Country Transfers**: Data processed via US-based sub-processors (AWS US-East,
  Salesforce Marketing Cloud)
**Retention**: Active contacts: duration of B2B contract + 2 years;
  Interaction logs: 6 months rolling

### 2. HR Module (VeritasCloud HR)

**Purpose**: Human resources management for VeritasCloud internal employees (1,200 staff)
**Data Subjects**: VeritasCloud employees
**Personal Data**: Name, employment contract, salary, performance reviews, health/sick leave
  records (special category per Art. 9), disciplinary records
**Legal Ground**: Contract performance (Art. 6(1)(b)) for employment;
  Legal obligation (Art. 6(1)(c)) for statutory reporting
**Third-Country Transfers**: None; EU-hosted only
**Retention**: Employment records: contract duration + 10 years (tax compliance)

### 3. Analytics Platform

**Purpose**: Platform usage analytics and product improvement
**Data Subjects**: All platform users (B2B clients + VeritasCloud employees)
**Personal Data**: Pseudonymous usage events, feature usage metrics
**Legal Ground**: Legitimate interests (Art. 6(1)(f))
**Third-Country Transfers**: Analytics processed via US-based vendor (Mixpanel)

### 4. Billing System

**Purpose**: Subscription billing and payment processing
**Data Subjects**: B2B client billing contacts and payment administrators
**Personal Data**: Name, email, billing address, payment method reference (tokenized)
**Legal Ground**: Contract performance (Art. 6(1)(b))
**Third-Country Transfers**: Payment processor Stripe (US entity, SCCs in place)

## Compliance Gaps Identified (Preliminary)

1. CRM Module: RoPA entry missing `recipient_categories` and `retention_periods` fields
2. HR Module: RoPA entry missing `security_measures` field
3. Analytics Platform: Third-country transfer documentation incomplete (Mixpanel SCC not executed)
4. HR Module: AI-powered HR Analytics sub-feature requires separate DPIA assessment
""")


# =========================================================================== #
# 3. RoPA files（合成，含缺失字段和蜜罐）
# =========================================================================== #

def _make_processing_activity(
    activity_id: str,
    name: str,
    purpose: str,
    legal_ground: str,
    data_subjects: list,
    personal_data: list,
    recipients: list,
    third_country: bool,
    retention: str,
    security: list,
    missing_fields: list = None,
) -> dict:
    """构造一个 RoPA 处理活动条目，可选择性省略某些字段（模拟合规缺口）。"""
    entry = {
        "activity_id": activity_id,
        "name_and_contact_details": {
            "controller": "VeritasCloud GmbH",
            "address": "Theodor-Heuss-Allee 112, 60486 Frankfurt am Main",
            "dpo": "Lena Fischer | dpo@veritascloud.de",
        },
        "purposes": purpose,
        "data_subject_categories": data_subjects,
        "personal_data_categories": personal_data,
        "recipient_categories": recipients,
        "third_country_transfers": {
            "transfer": third_country,
            "mechanism": "Standard Contractual Clauses (SCCs)" if third_country else None,
        },
        "retention_periods": retention,
        "security_measures": security,
        "legal_ground": legal_ground,
    }
    # 按照 missing_fields 列表删除字段（模拟合规缺口）
    for f in (missing_fields or []):
        entry.pop(f, None)
    return entry


def gen_ropa_files() -> None:
    # 3.1 RoPA Controller Draft v1（第一版，含 2 个缺口活动）
    ropa_v1_activities = []

    # CRM 联系人管理（缺少 recipient_categories）
    a_crm = _make_processing_activity(
        "ACT-001", "CRM Contact Management",
        "B2B customer relationship management and sales pipeline tracking",
        "Art. 6(1)(f) legitimate interests",
        ["B2B client contacts", "Prospective customers"],
        ["Name", "Email", "Phone", "Company", "Job title", "Interaction history"],
        ["AWS EU (processor)", "Salesforce EU (sub-processor)"],
        True, "Active: contract duration + 2 years; Logs: 6 months",
        ["Encryption at rest (AES-256)", "TLS 1.2+ in transit", "Access control", "Audit logging"],
        missing_fields=["recipient_categories"],  # 缺口：缺 recipient_categories
    )
    ropa_v1_activities.append(a_crm)

    # HR 员工记录（缺少 security_measures）
    a_hr = _make_processing_activity(
        "ACT-002", "HR Employee Records",
        "Employee contract management, payroll, and HR administration",
        "Art. 6(1)(b) contract; Art. 6(1)(c) legal obligation",
        ["VeritasCloud employees (1,200)"],
        ["Name", "Employment contract", "Salary", "Performance reviews",
         "Health/sick leave (Art. 9 special category)", "Tax identification number"],
        ["German tax authority (Finanzamt)", "Health insurance funds (Krankenkassen)"],
        False, "Contract duration + 10 years (HGB §257, AO §147)",
        ["Encryption at rest", "Role-based access control", "Audit logging"],
        missing_fields=["security_measures"],  # 缺口：缺 security_measures
    )
    ropa_v1_activities.append(a_hr)

    # Analytics（完整）
    a_analytics = _make_processing_activity(
        "ACT-003", "Platform Usage Analytics",
        "Product improvement and platform performance monitoring",
        "Art. 6(1)(f) legitimate interests",
        ["All platform users (B2B clients + employees)"],
        ["Pseudonymous usage events", "Feature usage metrics", "Session data"],
        ["Mixpanel Inc. (US, SCC pending)", "Internal analytics team"],
        True, "90-day rolling window; aggregated data: 2 years",
        ["Pseudonymisation", "TLS 1.2+", "IP truncation", "Access control"],
    )
    ropa_v1_activities.append(a_analytics)

    # Billing（完整）
    a_billing = _make_processing_activity(
        "ACT-004", "Subscription Billing",
        "B2B subscription management and payment processing",
        "Art. 6(1)(b) contract performance",
        ["B2B client billing contacts"],
        ["Name", "Email", "Billing address", "Payment method reference (tokenised)"],
        ["Stripe Inc. (US, SCC)", "B2B client finance teams"],
        True, "Active: contract duration + 7 years (HGB §257)",
        ["Tokenisation", "PCI-DSS compliance", "TLS 1.2+", "Access control"],
    )
    ropa_v1_activities.append(a_billing)

    # Email Marketing（完整）
    a_email = _make_processing_activity(
        "ACT-005", "Email Marketing",
        "Product update notifications and marketing communications",
        "Art. 6(1)(a) consent",
        ["Opted-in CRM contacts"],
        ["Email address", "Name", "Email engagement metrics"],
        ["Mailchimp (US, SCC)", "Internal marketing team"],
        True, "Until consent withdrawn + 6 months",
        ["Unsubscribe mechanism", "Consent records", "TLS 1.2+"],
    )
    ropa_v1_activities.append(a_email)

    # Customer Support（完整）
    a_support = _make_processing_activity(
        "ACT-006", "Customer Support Ticketing",
        "Technical support and issue resolution for B2B clients",
        "Art. 6(1)(b) contract performance",
        ["B2B client contacts", "End users reporting issues"],
        ["Name", "Email", "Support ticket content", "System logs"],
        ["Zendesk Inc. (US, SCC)", "Internal support team"],
        True, "Ticket: 3 years after resolution",
        ["Role-based access", "TLS 1.2+", "Data segregation by client"],
    )
    ropa_v1_activities.append(a_support)

    # Marketing Analytics（缺少 retention_periods）
    a_mktg_analytics = _make_processing_activity(
        "ACT-007", "Marketing Analytics",
        "Campaign effectiveness measurement and audience segmentation",
        "Art. 6(1)(f) legitimate interests",
        ["Website visitors", "Trial users"],
        ["IP address (truncated)", "UTM parameters", "Conversion events"],
        ["Google Analytics 4 (US, SCC)", "Internal marketing team"],
        True, "24 months from last interaction",
        ["IP truncation", "Consent banner", "Data processor agreements"],
        missing_fields=["retention_periods"],  # 缺口：缺 retention_periods
    )
    ropa_v1_activities.append(a_mktg_analytics)

    # Security Logging（完整）
    a_security = _make_processing_activity(
        "ACT-008", "Security Monitoring and Logging",
        "Detection and prevention of security incidents",
        "Art. 6(1)(f) legitimate interests",
        ["All platform users"],
        ["IP address", "User agent", "Access logs", "Authentication events"],
        ["Internal security team", "SIEM provider (EU-hosted)"],
        False, "Security logs: 12 months; Incident records: 5 years",
        ["Encryption at rest", "Role-based access", "Log integrity monitoring"],
    )
    ropa_v1_activities.append(a_security)

    # Data Deletion Service（完整）
    a_deletion = _make_processing_activity(
        "ACT-009", "Data Subject Rights Management",
        "Processing data subject access, erasure, and portability requests",
        "Art. 6(1)(c) legal obligation (Art. 12-22 compliance)",
        ["Any individual exercising GDPR rights"],
        ["Name", "Email", "Identity verification documents", "Request content"],
        ["Internal DPO team"],
        False, "Request records: 3 years (compliance documentation)",
        ["Access control", "Encryption at rest", "Audit trail"],
    )
    ropa_v1_activities.append(a_deletion)

    # Recruitment（完整）
    a_recruitment = _make_processing_activity(
        "ACT-010", "Recruitment and Talent Acquisition",
        "Evaluation and selection of job applicants",
        "Art. 6(1)(b) pre-contractual; Art. 6(1)(a) consent for talent pool",
        ["Job applicants"],
        ["Name", "CV/resume", "Email", "Interview notes", "Assessment results"],
        ["LinkedIn (US, SCC)", "Background check provider (DE)"],
        True, "Successful: contract duration + 10 years; Rejected: 6 months",
        ["Role-based access", "Access control", "Data minimisation on selection"],
    )
    ropa_v1_activities.append(a_recruitment)

    # 再添加 20 个更多处理活动以撑体量（完整条目）
    additional_activities = [
        ("ACT-011", "Partner Integration API", "Third-party integration via REST API",
         "Art. 6(1)(b) contract", ["API partner developers"], ["API keys", "Usage logs", "Error traces"],
         ["Partner companies (EU)"], False, "API logs: 90 days", ["TLS 1.2+", "API key rotation"]),
        ("ACT-012", "SaaS License Management", "Software license tracking and compliance",
         "Art. 6(1)(b) contract", ["B2B client administrators"],
         ["Name", "Email", "License assignment records"],
         ["Internal operations team"], False, "Contract + 5 years",
         ["Access control", "Audit trail"]),
        ("ACT-013", "Financial Reporting", "EU VAT reporting and financial statement preparation",
         "Art. 6(1)(c) legal obligation", ["B2B client billing contacts"],
         ["Invoice data", "VAT numbers", "Company registration"],
         ["Steuerberater (tax advisor)", "Finanzamt"], False,
         "10 years (AO §147)", ["Encryption at rest", "Access control"]),
        ("ACT-014", "Incident Response", "Security incident investigation and response",
         "Art. 6(1)(f) legitimate interests", ["Affected platform users"],
         ["IP logs", "Access records", "Forensic artifacts"],
         ["Internal SIEM", "External forensics firm (EU)"], False,
         "Incident records: 5 years", ["Restricted access", "Chain of custody"]),
        ("ACT-015", "Cookie Consent Management", "Recording and managing cookie consent",
         "Art. 6(1)(c) legal obligation (ePrivacy)", ["Website visitors"],
         ["Cookie consent records", "IP prefix", "Timestamp"],
         ["OneTrust (US, SCC)"], True, "Consent records: 3 years",
         ["Consent record integrity", "TLS 1.2+"]),
        ("ACT-016", "Employee Training Records", "Tracking mandatory compliance and skills training",
         "Art. 6(1)(c) legal obligation", ["VeritasCloud employees"],
         ["Name", "Training completion records", "Assessment scores"],
         ["Internal HR team"], False, "Employment + 5 years",
         ["Role-based access", "Audit logging"]),
        ("ACT-017", "Video Conferencing", "Remote meeting facilitation",
         "Art. 6(1)(b) contract", ["Employees", "External meeting participants"],
         ["Name", "Email", "Video/audio data", "Chat messages"],
         ["Zoom EU (processor)"], False, "Recording retention: 30 days",
         ["E2E encryption option", "Access control"]),
        ("ACT-018", "Whistleblowing Channel", "Anonymous reporting of internal misconduct",
         "Art. 6(1)(c) legal obligation (HinSchG)", ["Reporting employees", "Subjects of reports"],
         ["Report content", "Optional identity data"],
         ["External whistleblowing service (EU)"], False,
         "Case closed + 3 years", ["Anonymisation option", "Restricted access"]),
        ("ACT-019", "CCTV Surveillance", "Premises security monitoring",
         "Art. 6(1)(f) legitimate interests", ["Employees", "Visitors"],
         ["Video footage", "Facial images"],
         ["Internal security team"], False, "72-hour overwrite cycle",
         ["Camera placement disclosure", "Access control"]),
        ("ACT-020", "Product Trial Management", "Free trial account provisioning and management",
         "Art. 6(1)(b) pre-contractual", ["Trial users"],
         ["Name", "Email", "Company", "Trial usage data"],
         ["Internal sales team", "AWS EU (processor)"], False,
         "Trial data: 30 days post-trial + 1 year for sales follow-up",
         ["Access control", "TLS 1.2+"]),
    ]

    for act_id, name, purpose, legal_ground, subjects, personal_data, recipients, third_country, retention, security in additional_activities:
        entry = _make_processing_activity(
            act_id, name, purpose, legal_ground, subjects, personal_data, recipients,
            third_country, retention, security,
        )
        ropa_v1_activities.append(entry)

    wj(WS / "ropa" / "ropa_controller_draft_v1.json", {
        "schema_version": "GDPR-Art30-Controller-v1",
        "controller": "VeritasCloud GmbH",
        "dpo": "Lena Fischer | dpo@veritascloud.de",
        "last_updated": "2025-03-01",
        "total_activities": len(ropa_v1_activities),
        "compliance_gaps_noted": [
            "ACT-001: missing recipient_categories",
            "ACT-002: missing security_measures",
            "ACT-007: missing retention_periods",
        ],
        "activities": ropa_v1_activities,
        "source_reference": "https://gdpr-info.eu/art-30-gdpr/",
    })

    # 3.2 旧版 RoPA v0（蜜罐/红鲱鱼：有故意失真字段，标注为 LEGACY/SUPERSEDED）
    # 这是 V6 红鲱鱼：引用即错（使用旧版 v0 作为合规依据是错误的）
    legacy_activities = []
    for i in range(1, 11):
        legacy_activities.append({
            "processing_id": f"LEGACY-{i:03d}",
            "controller_name": "VeritasCloud GmbH",
            "processing_name": f"Legacy Processing Activity {i}",
            "purpose": f"Legacy purpose {i} — NOT VERIFIED against current legal ground",
            # 错误：缺少多个必填字段，且使用旧字段名
            "categories_of_persons": ["data subjects"],  # 错误字段名（应为 data_subject_categories）
            "categories_of_data": ["personal data"],      # 错误字段名（应为 personal_data_categories）
            "status": "LEGACY — not compliant with current GDPR Art.30 schema",
            "note": "This entry was created in 2019 before the CIRCL schema was adopted. "
                    "It has NOT been reviewed or updated. Do NOT use for compliance reporting.",
        })
    wj(WS / "ropa" / "ropa_controller_legacy_v0.json", {
        "SUPERSEDED": True,
        "WARNING": "LEGACY VERSION — DO NOT USE FOR COMPLIANCE PURPOSES. "
                   "This file is retained for forensic/historical reference only. "
                   "It uses obsolete field names and lacks required Art.30(1) fields. "
                   "Use ropa_controller_draft_v1.json as the current version.",
        "legacy_schema_version": "pre-CIRCL-v0",
        "created": "2019-08-01",
        "last_relevant_date": "2021-12-31",
        "controller": "VeritasCloud GmbH",
        "activities": legacy_activities,
    })

    # 3.3 Processor RoPA v1
    processor_activities = [
        {
            "activity_id": "PROC-001",
            "processor_name_and_contact": "VeritasCloud GmbH | dpo@veritascloud.de",
            "controller_name": "B2B Client (various)",
            "categories_of_processing": "CRM data hosting, access management, backup",
            "third_country_transfers": {
                "transfer": True,
                "mechanism": "Standard Contractual Clauses (SCCs per Commission Decision 2021/914)",
            },
            "security_measures": [
                "ISO 27001 certified data centre (TÜV certified)",
                "Encryption at rest (AES-256)",
                "TLS 1.2+ in transit",
                "RBAC for data access",
                "Quarterly penetration testing",
            ],
        },
        {
            "activity_id": "PROC-002",
            "processor_name_and_contact": "VeritasCloud GmbH | dpo@veritascloud.de",
            "controller_name": "VeritasCloud Employee (HR self-service)",
            "categories_of_processing": "HR data storage, payroll processing",
            "third_country_transfers": {"transfer": False},
            "security_measures": [
                "Role-based access control",
                "HR data encrypted at rest",
                "Audit trail for all access",
            ],
        },
    ]
    wj(WS / "ropa" / "ropa_processor_draft_v1.json", {
        "schema_version": "GDPR-Art30-Processor-v1",
        "processor": "VeritasCloud GmbH",
        "last_updated": "2025-03-01",
        "activities": processor_activities,
    })

    # 3.4 CIRCL JSON Schema Reference（真实来源 verbatim 摘录）
    wj(WS / "ropa" / "ropa_schema_reference.json", {
        "schema_title": "GDPR Art. 30 Processing Activities Records Schema",
        "source_url": "https://github.com/CIRCL/compliance/blob/master/gdpr/json-schema/processing-activities-records-schema.json",
        "controller_required_fields": ART30_CONTROLLER_FIELDS,
        "field_descriptions": {
            "name_and_contact_details": "Art. 30(1)(a): name and contact details of controller and DPO",
            "purposes": "Art. 30(1)(b): purposes of the processing",
            "data_subject_categories": "Art. 30(1)(c): categories of data subjects",
            "personal_data_categories": "Art. 30(1)(c): categories of personal data",
            "recipient_categories": "Art. 30(1)(d): categories of recipients",
            "third_country_transfers": "Art. 30(1)(e): transfers to third countries or international organisations",
            "retention_periods": "Art. 30(1)(f): envisaged time limits for erasure",
            "security_measures": "Art. 30(1)(g): general description of technical and organisational security measures per Art. 32",
        },
        "art30_exemption": {
            "article": "Art. 30(5)",
            "employee_threshold": 250,
            "note": "Organisations with fewer than 250 employees are exempt UNLESS processing is non-occasional, likely to result in risk, or involves special category data (Art. 9) or criminal conviction data (Art. 10).",
        },
        "processor_required_fields": [
            "name_and_contact_details",
            "categories_of_processing",
            "third_country_transfers",
            "security_measures",
        ],
    })


# =========================================================================== #
# 4. DSAR files（合成 CSV 队列）
# =========================================================================== #
def gen_dsar_files() -> None:
    rng = random.Random(42)

    FIRST_NAMES = ["Anna", "Thomas", "Sophie", "Michael", "Laura", "Klaus", "Emma", "Hans",
                   "Julia", "Peter", "Marie", "Stefan", "Lena", "Markus", "Jana", "Felix",
                   "Sarah", "Jonas", "Petra", "Andreas", "Nina", "David", "Claudia", "Martin",
                   "Karin", "Tobias", "Monika", "Christian", "Sabine", "Florian",
                   "Birgit", "Rolf", "Ingrid", "Werner", "Ursula", "Helmut", "Gisela", "Dieter",
                   "Renate", "Erich", "Brigitte", "Horst", "Hildegard", "Gerhard", "Elfriede"]
    LAST_NAMES = ["Mueller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner",
                  "Becker", "Schulz", "Hoffmann", "Koch", "Richter", "Klein", "Wolf", "Schroeder",
                  "Neumann", "Schwarz", "Zimmermann", "Braun", "Krueger",
                  "Hartmann", "Lange", "Krause", "Werner", "Vogt", "Walter", "Otto", "Roth",
                  "Frank", "Lorenz", "Huber", "Baum", "Fuchs", "Schaefer", "Maier", "Mayer"]
    REQUEST_TYPES = ["access", "erasure", "portability", "rectification", "restriction"]
    WEIGHTS = [0.45, 0.25, 0.15, 0.10, 0.05]
    PLATFORMS = ["web_form", "email", "postal", "phone_recorded", "in_person"]
    PLAT_W = [0.50, 0.30, 0.10, 0.05, 0.05]
    MODULES = ["CRM", "HR", "Analytics", "Billing", "All"]
    MOD_W = [0.45, 0.20, 0.15, 0.10, 0.10]

    rows = [["case_id", "first_name", "last_name", "email", "request_type",
             "request_date", "response_deadline", "status", "priority", "platform",
             "module_affected", "identity_verified", "notes"]]

    for i in range(1, 401):
        fn = rng.choice(FIRST_NAMES)
        ln = rng.choice(LAST_NAMES)
        req_type = rng.choices(REQUEST_TYPES, weights=WEIGHTS)[0]
        req_date = DSAR_START_DATE + timedelta(days=rng.randint(0, 40))
        # Art. 12(3): 1 calendar month（30 天）
        deadline = req_date + timedelta(days=30)
        today = date(2025, 3, 14)  # 审计当天
        is_overdue = deadline < today
        if is_overdue:
            status = "OVERDUE"
        else:
            status = rng.choices(["PENDING", "IN_PROGRESS", "COMPLETED"], weights=[0.45, 0.35, 0.20])[0]
        priority = "HIGH" if req_type == "access" and is_overdue else rng.choice(["NORMAL", "HIGH", "NORMAL", "NORMAL"])
        platform = rng.choices(PLATFORMS, weights=PLAT_W)[0]
        module = rng.choices(MODULES, weights=MOD_W)[0]
        verified = rng.choice(["YES", "YES", "YES", "PENDING"])
        rows.append([
            f"REQ-{i:03d}",
            fn, ln, f"{fn.lower()}.{ln.lower()}@example.com",
            req_type,
            req_date.isoformat(),
            deadline.isoformat(),
            status,
            priority,
            platform,
            module,
            verified,
            "" if i != 42 else "High-priority: data subject is investor relations contact",
        ])

    # 强制第 42 条目为 REQ-042（access 请求，用于 Q5 DSAR response）
    rows[42] = [
        "REQ-042",
        "Heinrich", "Braun", "h.braun@example.com",
        "access",
        "2025-02-10",
        "2025-03-12",  # 截止日期（已逾期）
        "OVERDUE",
        "HIGH",
        "web_form",
        "CRM",
        "YES",
        "Investor-related data subject; Art.15 copy of data requested explicitly",
    ]

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "dsar" / "dsar_queue.csv", buf.getvalue())

    # DSAR 模板
    w(WS / "dsar" / "dsar_response_templates" / "template_access.md", """# Art. 15 Access Request Response Template

**To**: [Data Subject Name]
**From**: VeritasCloud GmbH Data Protection Team
**Re**: Your Data Subject Access Request (Art. 15 GDPR)

---

Dear [Name],

Thank you for your request received on [request_date]. In accordance with
**Art. 15 GDPR** and **Art. 12(3) GDPR**, we are providing the following information.

## Personal Data Held

Per **Art. 15(1) GDPR**, we confirm that VeritasCloud GmbH processes the following
categories of personal data about you:

- [List categories]

## Copy of Personal Data

Pursuant to **Art. 15(3) GDPR**: "The controller shall provide a copy of the personal
data undergoing processing." Please find attached the data extract.

## Processing Details

- **Purposes**: [purposes]
- **Legal Grounds**: [legal grounds per Art. 6]
- **Recipients**: [recipient categories]
- **Retention Period**: [period]
- **Your Rights**: rectification (Art. 16), erasure (Art. 17), restriction (Art. 18),
  portability (Art. 20), objection (Art. 21)
- **Complaint Right**: You may lodge a complaint with BayLDA (www.lda.bayern.de)

---

*Response prepared by: DPO Office | dpo@veritascloud.de*
*Reference: [case_id]*
""")

    w(WS / "dsar" / "dsar_response_templates" / "template_erasure.md", """# Art. 17 Erasure Request Response Template

**To**: [Data Subject Name]
**From**: VeritasCloud GmbH Data Protection Team
**Re**: Your Right to Erasure Request (Art. 17 GDPR)

---

Dear [Name],

We have received your erasure request on [request_date]. Under **Art. 17 GDPR** (right
to erasure / "right to be forgotten"), we have assessed your request as follows.

## Erasure Decision

[ ] **Erasure Granted** — Data has been deleted per **Art. 17(1)(a-f)** grounds.
[ ] **Erasure Declined** — Legal basis for retention applies per **Art. 17(3)**:
    - Legal obligation (Art. 6(1)(c))
    - Archiving / research / statistical purposes (Art. 17(3)(d))
    - Legal claims (Art. 17(3)(e))

## Next Steps

Data erased from: [systems list]
Data retained (with reason): [if applicable]

You may lodge a complaint with BayLDA if unsatisfied.

---

*Reference: [case_id]*
""")

    w(WS / "dsar" / "dsar_response_templates" / "template_portability.md", """# Art. 20 Data Portability Response Template

**To**: [Data Subject Name]
**From**: VeritasCloud GmbH Data Protection Team
**Re**: Your Data Portability Request (Art. 20 GDPR)

---

Dear [Name],

We have received your portability request on [request_date]. Under **Art. 20 GDPR**,
we are providing your personal data in a structured, commonly used, and machine-readable
format (JSON) where the processing was based on consent (Art. 6(1)(a)) or contract
(Art. 6(1)(b)).

## Data Package

Attached: `[case_id]_data_export.json`
Format: JSON (structured, machine-readable per Art. 20(1))
Scope: Data you actively provided; automated processing outputs

---

*Reference: [case_id]*
""")

    # DSAR 处理日志
    dsar_log_entries = []
    for i in [1, 2, 3, 4, 15, 16, 17, 18, 31, 32, 33]:
        dsar_log_entries.append({
            "case_id": f"REQ-{i:03d}",
            "request_type": "access" if i % 3 == 0 else "erasure",
            "received": f"2025-01-{i:02d}",
            "responded": f"2025-02-{min(i + 5, 28):02d}",
            "status": "COMPLETED",
            "response_time_days": rng.randint(7, 28),
            "notes": "Responded within 1-month deadline per Art. 12(3)",
        })
    wj(WS / "dsar" / "dsar_log.json", {
        "total_completed": len(dsar_log_entries),
        "date_range": "2025-01-01 to 2025-02-28",
        "entries": dsar_log_entries,
    })


# =========================================================================== #
# 5. Breach Notification files
# =========================================================================== #
def gen_breach_files() -> None:
    w(WS / "breach" / "incident_20250314_report.md", f"""# Data Breach Incident Report — Initial Assessment

**Incident Reference**: INC-2025-0314
**Date Discovered**: 2025-03-14 at 09:00 UTC
**Discovery Method**: Automated anomaly detection alert (SIEM)
**Reported to DPO**: 2025-03-14 at 09:45 UTC
**Classification**: PERSONAL DATA BREACH (Art. 4(12) GDPR)

## Summary

An unauthorised third party gained read access to the VeritasCloud CRM database
(production instance, EU-West-1 region) between 2025-03-12 02:00 UTC and
2025-03-14 08:50 UTC (estimated 54 hours of exposure).

## Affected Data

- **Categories of Data Subjects**: B2B client contacts (~15,000 individuals)
- **Approximate Number of Data Subjects**: 15,000
- **Categories of Personal Data**: Name, email address, phone number, company affiliation
- **Approximate Number of Records**: ~45,000 records (3 data fields × 15,000 subjects)
- **Sensitive Data Involved**: No special category data (Art. 9) exposed

## Discovery Timeline

| Time (UTC) | Event |
|---|---|
| 2025-03-14 09:00 | SIEM alert triggered: anomalous read queries on CRM DB |
| 2025-03-14 09:30 | Security team confirms breach; containment initiated |
| 2025-03-14 09:45 | DPO Lena Fischer notified |
| 2025-03-14 10:30 | Access revoked; affected credentials rotated |
| 2025-03-14 14:00 | Full extent of breach determined: 15,000 subjects, 45,000 records |
| 2025-03-14 18:00 | Breach risk assessment completed |
| 2025-03-15 09:00 | Art. 33 notification decision: NOTIFY (risk to data subjects likely) |
| 2025-03-15 22:30 | Formal notification submitted to BayLDA via online portal |

## Notification Decision

Under **Art. 33(1) GDPR**: Controller must notify supervisory authority without undue
delay and, where feasible, not later than **72 hours** after becoming aware.

**Discovery time**: 2025-03-14T09:00Z
**Notification time**: 2025-03-15T22:30Z
**Elapsed hours**: approximately 37.5 hours
**Status**: WITHIN 72-HOUR WINDOW — COMPLIANT

---

*Note: See `breach/breach_internal_timeline.md` for full chronological detail.*
""")

    wj(WS / "breach" / "breach_notification_draft.json", {
        "notification_reference": "BayLDA-NOT-2025-0315-001",
        "notification_type": "Art. 33 GDPR Supervisory Authority Notification",
        "controller": "VeritasCloud GmbH",
        "dpo_contact": "Lena Fischer | dpo@veritascloud.de | +49 69 4433 8800",
        "incident_reference": "INC-2025-0314",
        "discovery_datetime_utc": BREACH_DISCOVERY_ISO,
        "notification_datetime_utc": BREACH_NOTIFICATION_ISO,
        "hours_elapsed": 37.5,
        # Art. 33(3) required fields — DRAFT: missing "categories_and_number_of_records"
        "nature_of_breach": (
            "Unauthorised read access to CRM production database; "
            "no data exfiltration confirmed but read access exposure for ~54 hours"
        ),
        "categories_and_number_of_data_subjects": "B2B client contacts — approximately 15,000",
        # 缺口：draft 缺少 categories_and_number_of_records, likely_consequences, measures_taken
        "DPO_contact": "Lena Fischer | dpo@veritascloud.de | +49 69 4433 8800",
        "DRAFT_NOTE": (
            "INCOMPLETE — Missing required Art.33(3) fields: "
            "categories_and_number_of_records, likely_consequences, measures_taken. "
            "Complete before submission."
        ),
    })

    w(WS / "breach" / "breach_internal_timeline.md", f"""# Breach Incident — Internal Timeline

**Incident**: INC-2025-0314 | CRM Database Unauthorized Access
**Status**: CONTAINED | Notification submitted to BayLDA

---

## Chronological Timeline

### 2025-03-12 (Wednesday)

- **02:00 UTC**: Attacker uses stolen API credential to authenticate to CRM DB (source IP: 203.0.113.45)
- **02:05 UTC**: Automated SIEM rule: API auth from new IP — alert **NOT triggered** (threshold too high)

### 2025-03-14 (Friday)

- **08:50 UTC**: Second anomaly pattern detected by ML-based anomaly detection
- **09:00 UTC**: SIEM high-severity alert fired — Security Engineer on-call paged
- **09:25 UTC**: Security Engineer Fabian Müller confirms active unauthorized session
- **09:30 UTC**: Containment: credential revoked, session terminated, IP blocked
- **09:45 UTC**: DPO Lena Fischer notified by Fabian Müller
- **10:00 UTC**: Incident response team convened
- **10:30 UTC**: All affected credentials rotated; perimeter secured
- **11:00 UTC**: Digital forensics commenced; log extraction from SIEM
- **14:00 UTC**: Forensic analysis complete:
  - Exfiltration: No evidence of data leaving the environment (no outbound anomalies)
  - Exposure: Read queries executed on contact tables (~15,000 subjects, ~45,000 records)
  - Root cause: Phishing email compromised employee API key
- **18:00 UTC**: Risk assessment completed: HIGH risk to data subjects (contact data quality)
- **20:00 UTC**: DPO decision: Article 33 notification required; Art. 34 assessment: notification to data subjects NOT required (low risk of harm from contact data exposure alone)

### 2025-03-15 (Saturday)

- **09:00 UTC**: DPO and Legal Counsel finalize notification content
- **22:30 UTC**: Formal Art. 33 notification submitted to BayLDA online portal (Portal-ID: BayLDA-2025-0315-8847)

**Total elapsed from discovery to notification**: 37.5 hours (within 72-hour Art. 33(1) deadline)

---

## Root Cause Analysis (Preliminary)

1. **Insufficient MFA enforcement**: API keys not subject to MFA requirement
2. **Overly broad API key permissions**: Key granted read access to entire contact table
3. **Alert threshold misconfiguration**: SIEM threshold for "new IP auth" too high
4. **Missing data minimisation**: API key scope should have been restricted to specific client's data

## Corrective Measures

1. Mandatory MFA for all API key usage (implemented 2025-03-15)
2. Principle of least privilege: API key scoping by client ID (implemented 2025-03-16)
3. SIEM alert threshold recalibrated (implemented 2025-03-14)
4. Security awareness training relaunch (scheduled 2025-04-01)
""")

    w(WS / "breach" / "breach_risk_assessment.md", """# Breach Risk Assessment — INC-2025-0314

**Risk Assessment Framework**: EDPB Guidelines 9/2022 on Personal Data Breach Notification

## Risk Factors Assessed

| Factor | Assessment | Score (1-5) |
|--------|-----------|-------------|
| Nature of data | Name, email, phone — not special category | 2 |
| Ease of identification | High (direct identifiers) | 4 |
| Special characteristics of data subjects | No vulnerable subjects | 2 |
| Number of subjects | 15,000 (medium scale) | 3 |
| Severity of consequences | Low-medium (contact data only, no financial/health) | 2 |
| Ease of misuse | Medium (phishing/spam risk) | 3 |

## Overall Risk Level: MEDIUM

**Notification to Supervisory Authority (Art. 33)**: REQUIRED
**Notification to Data Subjects (Art. 34)**: NOT REQUIRED
(Risk is not "high" as no special category data, financial data, or authentication credentials
were exposed.)

## Legal Basis

Per **Art. 33(1) GDPR**: Notification to supervisory authority required unless "the
personal data breach is unlikely to result in a risk to the rights and freedoms of natural
persons." Given exposure of contact data to unknown third party, risk cannot be ruled out.

Per **Art. 34(1) GDPR**: Direct notification to data subjects required only where breach
"is likely to result in a high risk to the rights and freedoms of natural persons."
Assessment: MEDIUM risk (not HIGH) — Art. 34 notification not triggered.

## EDPB Guidance Reference

EDPB Guidelines 9/2022 v2.0 (final, 4 April 2023):
URL: https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en
""")


# =========================================================================== #
# 6. DPIA files
# =========================================================================== #
def gen_dpia_files() -> None:
    # EDPB 9 criteria（verbatim）
    edpb_nine_criteria = [
        "evaluation_or_scoring",
        "automated_decision_making_with_legal_effect",
        "systematic_monitoring",
        "sensitive_data_large_scale",
        "data_set_matching_combining",
        "vulnerable_subjects",
        "innovative_technology_use",
        "preventing_exercise_of_right",
        "large_scale_processing",
    ]

    w(WS / "dpia" / "dpia_hr_analytics_draft.md", """# DPIA Draft — HR Analytics Module

**Processing Activity**: VeritasCloud HR Analytics (beta feature)
**Controller**: VeritasCloud GmbH
**DPO Consulted**: Lena Fischer
**Draft Date**: 2025-03-05
**Status**: DRAFT — INCOMPLETE

---

## 1. Description of Processing

The HR Analytics module provides AI-powered insights from employee HR data, including:
- Performance trend analysis
- Attrition risk prediction (which employees are likely to leave)
- Skill gap analysis
- Work pattern monitoring (meeting frequency, collaboration patterns from calendar data)

**Data Sources**: Employee records (ACT-002), calendar data, email metadata
**Data Subjects**: 1,200 VeritasCloud employees
**Processing Scale**: Large-scale relative to employee base; continuous monitoring

---

## 2. DPIA Trigger Assessment

Applying EDPB guidelines (Art. 35 GDPR), DPIA triggers:

| Criterion | Present? | Justification |
|-----------|---------|---------------|
| Evaluation/scoring of employees | YES | Attrition risk scores, performance trends |
| Automated decision-making with significant effect | PARTIAL | Outputs used in performance management |
| Systematic monitoring | YES | Continuous monitoring of work patterns via calendar/email metadata |
| Special categories (Art. 9) | NOT YET | No health data at initial scope |
| Large-scale processing | YES | 1,200 employees continuously monitored |

**Current assessment**: ≥2 EDPB criteria met (evaluation/scoring + systematic monitoring)
**DPIA Required**: YES (per EDPB threshold of ≥2 criteria)

---

## 3. Risk Matrix (Preliminary)

| Risk | Likelihood (1-5) | Severity (1-5) | Risk Score |
|------|-----------------|---------------|------------|
| Algorithmic bias in attrition scoring | 3 | 4 | 12 |
| Unlawful processing of special category data (if health data added) | 2 | 5 | 10 |
| Lack of transparency to employees | 3 | 3 | 9 |
| Data minimisation violation (calendar metadata) | 4 | 3 | 12 |

**High-Risk Items** (score ≥ 10): bias, special category risk, data minimisation

---

## 4. Compliance Gaps

1. No legitimate basis for processing calendar/email metadata under Art. 9 if health data included
2. Transparency: Employees not individually informed of AI scoring
3. Data minimisation: Calendar metadata scope too broad

---

## 5. DPO Consultation Status

**DPO Review**: PENDING
**SA Consultation Required**: NOT YET DETERMINED (see Update-1 for revised scope)

*Note: Update-1 (CTO Stefan Vogel) has disclosed addition of "health status prediction"
feature to HR Analytics — this changes the DPIA conclusion significantly. See
`company/hr_analytics_new_feature.md` after Update-1 is applied.*
""")

    w(WS / "dpia" / "dpia_crm_profiling.md", """# DPIA — CRM Profiling and Behavioral Analytics

**Processing Activity**: CRM Behavioral Analytics (ACT-001 sub-feature)
**Controller**: VeritasCloud GmbH
**DPO Consulted**: Lena Fischer
**Date**: 2025-02-15
**Status**: COMPLETED

---

## 1. Description

CRM behavioral analytics tracks page visits, email opens, click tracking, and
session durations for B2B contacts to generate lead scoring and engagement metrics.

## 2. DPIA Trigger Assessment

| Criterion | Present? | Justification |
|-----------|---------|---------------|
| Evaluation/scoring | YES | Lead scoring based on behavioral data |
| Automated decision-making | PARTIAL | Scoring inputs to sales prioritisation |
| Large-scale processing | YES | ~800,000 data subjects |
| Data set combining | YES | Behavioral + CRM contact data |

**DPIA Required**: YES (4 criteria met — well above ≥2 threshold)

## 3. Risk Matrix

| Risk | Likelihood | Severity | Score |
|------|-----------|---------|-------|
| Insufficient transparency (Art. 13) | 3 | 3 | 9 |
| Excessive behavioral tracking | 2 | 4 | 8 |
| Consent validity for profiling | 3 | 4 | 12 |
| Third-country transfer risk | 2 | 3 | 6 |

**High-Risk Items**: Consent validity for profiling

## 4. Mitigation Measures

1. Privacy notice updated to explicitly disclose behavioral analytics (Art. 13)
2. Consent mechanism reviewed — confirmed valid per Art. 7 requirements
3. Data minimisation: Only aggregate behavioral metrics retained; individual click
   records deleted after 30 days
4. SCCs executed with all US sub-processors

**DPO Sign-off**: Lena Fischer | 2025-02-28
**Status**: DPIA COMPLETE — No SA consultation required
""")

    w(WS / "dpia" / "dpia_template_edpb.md", """# DPIA Template — Based on EDPB Art. 35 Guidelines

**Source**: Art. 35 GDPR (https://gdpr-info.eu/art-35-gdpr/) +
EDPB Guidelines on Data Protection Impact Assessment (WP248rev01)

---

## EDPB Nine High-Risk Criteria

DPIA is **generally required** if processing meets **≥2** of the following criteria:

1. **Evaluation or scoring** — including profiling and predicting performance,
   economic situation, health, personal preferences, interests, reliability,
   behaviour, location, or movements.

2. **Automated decision-making with legal or similarly significant effect** —
   automated processing that produces decisions with significant effects on individuals.

3. **Systematic monitoring** — processing used to observe, monitor, or control data
   subjects, including data collected through networks or public spaces on a large scale.

4. **Sensitive data or data of a highly personal nature** — special categories per
   Art. 9, criminal conviction data per Art. 10, or data that could endanger safety.

5. **Data processed on a large scale** — EDPB considers factors: number of subjects,
   volume of data, variety of data items, geographical extent, duration, nature of
   processing.

6. **Matching or combining data sets** — combining data from multiple sources in ways
   that go beyond reasonable expectations.

7. **Data concerning vulnerable data subjects** — children, employees (imbalance of
   power), mental health patients, asylum seekers, elderly, patients.

8. **Innovative use of new technological solutions** — use of fingerprinting, facial
   recognition, voice recognition, IoT, or AI/ML in novel ways.

9. **Processing that prevents data subjects from exercising rights or using services** —
   including credit scoring, e-recruiting, or processing that restricts access to services.

---

## Art. 35(3) Mandatory DPIA Triggers

Regardless of the 9-criteria test, DPIA is **always mandatory** for:
- (a) Systematic and extensive profiling with significant effects (automated decisions)
- (b) Large-scale processing of Art. 9 / Art. 10 data
- (c) Systematic monitoring of publicly accessible areas on large scale

---

## Risk Rating Scale

| Rating | Likelihood | Severity |
|--------|-----------|---------|
| 1 | Very unlikely | Minimal |
| 2 | Unlikely | Minor |
| 3 | Possible | Moderate |
| 4 | Likely | Significant |
| 5 | Very likely | Severe/irreversible |

**Residual Risk Score** = Likelihood × Severity (post-mitigation)
**High risk threshold**: Score ≥ 9 or Severity = 5 regardless of likelihood

---

## Required DPIA Sections (Art. 35(7))

1. Systematic description of processing operations and purposes
2. Assessment of necessity and proportionality
3. Assessment of risks to data subjects
4. Measures to address risks (safeguards, security measures, mechanisms)
5. DPO opinion
6. Supervisory authority consultation (if residual risk remains high)
""")


# =========================================================================== #
# 7. Policies and documentation
# =========================================================================== #
def gen_policy_files() -> None:
    w(WS / "policies" / "privacy_policy_v3.md", """# VeritasCloud GmbH — Privacy Policy (Version 3.0)

**Effective Date**: 2024-12-01
**Controller**: VeritasCloud GmbH, Theodor-Heuss-Allee 112, 60486 Frankfurt am Main
**DPO**: Lena Fischer | dpo@veritascloud.de | +49 69 4433 8800

---

## 1. Introduction

VeritasCloud GmbH ("we", "us", "our") processes personal data in compliance with
Regulation (EU) 2016/679 (GDPR). This policy describes our processing activities,
your rights, and how to exercise them.

## 2. Data We Process and Why

We process personal data for the following purposes:
- CRM services: customer relationship management (Art. 6(1)(f) legitimate interests)
- HR management: employee administration (Art. 6(1)(b) contract; Art. 6(1)(c) obligation)
- Analytics: platform improvement (Art. 6(1)(f) legitimate interests)
- Billing: payment processing (Art. 6(1)(b) contract)

## 3. Your Rights Under GDPR

You have the right to:
- **Access** (Art. 15): obtain confirmation of processing and a copy of your data
- **Rectification** (Art. 16): correct inaccurate data
- **Erasure** (Art. 17): request deletion where legal basis no longer applies
- **Restriction** (Art. 18): limit processing in certain circumstances
- **Portability** (Art. 20): receive your data in machine-readable format
- **Object** (Art. 21): object to processing based on legitimate interests

**Response Time**: We respond to rights requests within **1 month** per Art. 12(3).
For complex or numerous requests, we may extend by up to **2 additional months**
with written notification within the initial 1-month period.

## 4. International Transfers

Transfers to third countries (US sub-processors) are governed by:
- Standard Contractual Clauses (Commission Decision 2021/914)
- Supplementary measures per EDPB Recommendations 01/2020

Sub-processors with US transfers: AWS, Stripe, Mailchimp, Google Analytics 4,
Mixpanel (SCC pending), LinkedIn.

## 5. Complaints

You may lodge a complaint with your national supervisory authority.
Our lead supervisory authority: **BayLDA** (www.lda.bayern.de)

---

*Version history: v1 (2021-05), v2 (2023-01), v3 (2024-12)*
""")

    # 保留期限表（CSV）
    retention_rows = [
        ["data_category", "retention_period", "legal_basis", "review_date"],
        ["CRM contact data", "Contract + 2 years", "Art. 6(1)(f), legitimate interests", "2026-01-01"],
        ["CRM interaction logs", "6 months rolling", "Art. 6(1)(f), legitimate interests", "2025-09-01"],
        ["Employee HR records", "Contract + 10 years", "HGB §257, AO §147", "2026-01-01"],
        ["Payroll records", "Contract + 10 years", "AO §147 (tax records)", "2026-01-01"],
        ["Health/sick leave data", "Contract + 10 years", "Art. 9(2)(b), employment law", "2026-01-01"],
        ["Performance reviews", "Contract + 5 years", "Art. 6(1)(b), contract", "2025-12-01"],
        ["Security logs (SIEM)", "12 months", "Art. 6(1)(f), IT security", "2025-09-01"],
        ["Incident records", "5 years", "Art. 6(1)(c), legal obligation", "2026-01-01"],
        ["Analytics events (pseudonymous)", "90 days rolling", "Art. 6(1)(f), legitimate interests", "2025-09-01"],
        ["Aggregated analytics", "2 years", "Art. 6(1)(f), legitimate interests", "2026-01-01"],
        ["Billing/invoice records", "Contract + 7 years", "HGB §257 (commercial)", "2026-01-01"],
        ["Cookie consent records", "3 years", "ePrivacy Directive, Art. 6(1)(c)", "2026-01-01"],
        ["DSAR request records", "3 years", "Art. 6(1)(c), Art. 12-22 compliance", "2026-01-01"],
        ["Breach notification records", "Documentation indefinitely", "Art. 33(5)", "2026-01-01"],
        ["Job applicant data (successful)", "Contract + 10 years", "HGB §257", "2026-01-01"],
        ["Job applicant data (unsuccessful)", "6 months", "Art. 6(1)(a) consent withdrawn", "2025-09-01"],
        ["Marketing email engagement", "Until consent withdrawn + 6 months", "Art. 6(1)(a), consent", "2025-09-01"],
        ["Whistleblowing case records", "Case closed + 3 years", "HinSchG", "2026-01-01"],
        ["CCTV footage", "72 hours overwrite", "Art. 6(1)(f), premises security", "2025-06-01"],
        ["API access logs", "90 days", "Art. 6(1)(f), IT security", "2025-09-01"],
    ]
    buf = io.StringIO()
    csv.writer(buf).writerows(retention_rows)
    w(WS / "policies" / "retention_schedule.csv", buf.getvalue())

    w(WS / "policies" / "data_transfer_agreements" / "scc_us_vendor_A.md", """# Standard Contractual Clauses — US Vendor A (Stripe Inc.)

**Agreement Date**: 2023-07-01
**Controller**: VeritasCloud GmbH (Frankfurt)
**Processor/Importer**: Stripe Inc. (354 Oyster Point Blvd, South San Francisco, CA 94080)
**Module**: Module 2 (Controller to Processor) per Commission Decision 2021/914

## Transfer Details

**Data Transferred**: Payment method references (tokenised), billing contact details
(name, email, billing address)
**Purpose**: Payment processing and subscription management
**Transfer Frequency**: Continuous (each billing event)

## Legal Basis for Transfer

Standard Contractual Clauses adopted by European Commission on 4 June 2021
(Commission Implementing Decision (EU) 2021/914, CELEX:32021D0914)

Module 2 Clause 4 (Docking Clause): allows VeritasCloud sub-processors to accede.

## Supplementary Measures (EDPB Rec 01/2020)

1. Stripe's data centre for EU processing is AWS EU-West-1 (Dublin, Ireland)
2. Contractual prohibition on government access disclosure without legal challenge
3. Technical measures: encryption at rest and in transit; pseudonymisation where possible
4. Regular data protection audits (annual)

## Effective Date and Review

Effective: 2023-07-01 | Review due: 2026-07-01
""")

    w(WS / "policies" / "data_transfer_agreements" / "scc_us_vendor_B.md", """# Standard Contractual Clauses — US Vendor B (Mailchimp / Intuit Inc.)

**Agreement Date**: 2023-09-15
**Controller**: VeritasCloud GmbH (Frankfurt)
**Processor/Importer**: Intuit Inc. (2700 Coast Ave, Mountain View, CA 94043) d/b/a Mailchimp
**Module**: Module 2 (Controller to Processor) per Commission Decision 2021/914

## Transfer Details

**Data Transferred**: Email addresses, names, email engagement metrics
**Purpose**: Email marketing campaign management and delivery
**Legal Basis for Processing**: Art. 6(1)(a) GDPR consent

## Supplementary Measures

1. Mailchimp EU Data Centre: hosted in EU region (AWS EU-West-1)
2. Encryption at rest (AES-256) and in transit (TLS 1.3)
3. Contractual limitation: data used only for contracted purpose

## Status: EXECUTED AND VALID

Effective: 2023-09-15 | Next review: 2026-09-15
""")


# =========================================================================== #
# 8. Audit files
# =========================================================================== #
def gen_audit_files() -> None:
    wj(WS / "audit" / "audit_checklist_v1.json", {
        "checklist_id": "VC-GDPR-AUDIT-2025-Q1",
        "version": "1.0",
        "created": "2025-03-01",
        "reviewer": "Data Privacy Consultant (external)",
        "areas": [
            {
                "area": "Art. 30 — Records of Processing Activities",
                "items": [
                    {"item": "Controller RoPA complete", "status": "IN_PROGRESS",
                     "note": "3 activities have missing required fields"},
                    {"item": "Processor RoPA complete", "status": "COMPLIANT"},
                    {"item": "RoPA in writing/electronic form (Art. 30(3))", "status": "COMPLIANT"},
                    {"item": "Art. 30(5) exemption assessment", "status": "N/A",
                     "note": "1,200 employees > 250 threshold; exemption does not apply"},
                ],
            },
            {
                "area": "Art. 33 — Breach Notification",
                "items": [
                    {"item": "Breach INC-2025-0314 notified within 72h", "status": "COMPLIANT",
                     "note": "37.5h elapsed; within window"},
                    {"item": "Art. 33(3) notification complete", "status": "IN_PROGRESS",
                     "note": "Draft missing 3 required fields"},
                    {"item": "Art. 33(5) breach documentation maintained", "status": "COMPLIANT"},
                ],
            },
            {
                "area": "Art. 35 — DPIA",
                "items": [
                    {"item": "HR Analytics DPIA initiated", "status": "IN_PROGRESS"},
                    {"item": "CRM Profiling DPIA complete", "status": "COMPLIANT"},
                    {"item": "DPIA register maintained", "status": "IN_PROGRESS"},
                ],
            },
            {
                "area": "Art. 37 — DPO",
                "items": [
                    {"item": "DPO appointed (Lena Fischer)", "status": "COMPLIANT"},
                    {"item": "DPO registered with BayLDA", "status": "COMPLIANT",
                     "note": "BayLDA-DPO-2022-04471"},
                    {"item": "DPO appointment mandatory?", "status": "TO_BE_ASSESSED"},
                ],
            },
            {
                "area": "Art. 12-22 — Data Subject Rights",
                "items": [
                    {"item": "DSAR response procedure documented", "status": "COMPLIANT"},
                    {"item": "DSAR queue cleared within deadlines", "status": "NON_COMPLIANT",
                     "note": "Multiple DSAR overdue in current queue"},
                    {"item": "Art. 12(3) response time policy (1 month)", "status": "COMPLIANT",
                     "note": "Policy documented in Privacy Policy v3"},
                ],
            },
        ],
    })

    w(WS / "audit" / "gap_analysis_report_v1.md", """# Gap Analysis Report — GDPR Compliance Audit

**Client**: VeritasCloud GmbH
**Audit Period**: 2025-03-01 to 2025-03-14
**Prepared by**: External Data Privacy Consultant
**Reviewed by**: DPO Lena Fischer

---

## Executive Summary

Based on initial document review and system analysis, VeritasCloud GmbH demonstrates
partial GDPR compliance. Key gaps identified across Article 30 (RoPA completeness),
Article 33 (breach notification documentation), and Article 12 (DSAR response timeliness).

**Overall Compliance Status**: PARTIALLY_COMPLIANT
**Critical Gaps**: 3 | **Significant Gaps**: 4 | **Minor Gaps**: 2

---

## Gap 1 — Art. 30: Incomplete RoPA Entries

**Severity**: CRITICAL
**Gap**: Three processing activities (ACT-001, ACT-002, ACT-007) have missing required
Art. 30(1) fields as defined in the CIRCL JSON Schema:
- ACT-001: Missing `recipient_categories`
- ACT-002: Missing `security_measures`
- ACT-007: Missing `retention_periods`

**Legal Risk**: Art. 83(4) — Tier 1 fine applies to Art. 30 violations.
Maximum: EUR 10,000,000 or 2% of worldwide annual turnover (EUR 6,400,000 at 2% of EUR 320M).

**Remediation**: Complete missing fields in `ropa_controller_fixed.json` per Q2 deliverable.

---

## Gap 2 — Art. 33: Incomplete Breach Notification Draft

**Severity**: CRITICAL
**Gap**: Breach notification draft (`breach_notification_draft.json`) missing three of the
six Art. 33(3) required fields: `categories_and_number_of_records`, `likely_consequences`,
`measures_taken`.

**Note**: The 72-hour notification deadline itself was met (37.5h elapsed). The gap is
in the content completeness of the notification.

**Remediation**: Complete notification per Art. 33(3)(a)-(d) requirements in Q7 deliverable.

---

## Gap 3 — Art. 12: DSAR Overdue Queue

**Severity**: SIGNIFICANT
**Gap**: Review of `dsar_queue.csv` reveals multiple requests past the 1-month response
deadline per Art. 12(3). Overdue requests require immediate attention.

**Legal Risk**: Art. 83(5) — Tier 2 fine applies to Art. 12-22 violations.
Maximum: EUR 20,000,000 or 4% of worldwide annual turnover (EUR 12,800,000 at 4% of EUR 320M).

---

## Gap 4 — Art. 37: DPO Appointment Mandatory Assessment

**Severity**: SIGNIFICANT
**Gap**: Formal assessment of whether DPO appointment is mandatory under Art. 37(1)
has not been documented. (DPO is already appointed — the question is whether the
appointment is mandatory or voluntary.)

**Remediation**: Complete formal assessment per Q10 deliverable.

---

## Additional Findings

- **Art. 35**: HR Analytics module DPIA not completed prior to feature deployment
- **Third-country transfers**: Mixpanel SCC not yet executed (non-conforming transfer)
- **Privacy Policy**: References Art. 15-22 rights correctly; Art. 22 (automated decisions)
  disclosure needs enhancement for HR Analytics module

---

*Report Version: 1.0 | Next review: after remediation deliverables (Q1-Q18) completed*
""")

    # findings_log.csv
    findings_rows = [
        ["finding_id", "article", "severity", "description", "status", "remediation_due"],
        ["F-001", "Art. 30(1)", "CRITICAL", "RoPA ACT-001 missing recipient_categories", "OPEN", "2025-04-01"],
        ["F-002", "Art. 30(1)", "CRITICAL", "RoPA ACT-002 missing security_measures", "OPEN", "2025-04-01"],
        ["F-003", "Art. 30(1)", "CRITICAL", "RoPA ACT-007 missing retention_periods", "OPEN", "2025-04-01"],
        ["F-004", "Art. 33(3)", "CRITICAL", "Breach notification draft missing 3 required fields", "OPEN", "2025-03-20"],
        ["F-005", "Art. 12(3)", "SIGNIFICANT", "Multiple DSAR overdue in queue", "OPEN", "2025-03-30"],
        ["F-006", "Art. 37(1)", "SIGNIFICANT", "No formal DPO mandatory appointment assessment", "OPEN", "2025-04-15"],
        ["F-007", "Art. 35(1)", "SIGNIFICANT", "HR Analytics DPIA not completed before deployment", "OPEN", "2025-04-30"],
        ["F-008", "Art. 46(1)", "SIGNIFICANT", "Mixpanel SCC not executed (non-conforming transfer)", "OPEN", "2025-04-15"],
        ["F-009", "Art. 13(1)", "MINOR", "Privacy notice lacks Art. 22 automated decision disclosure", "OPEN", "2025-05-01"],
        ["F-010", "Art. 32(1)", "MINOR", "API key MFA requirement not enforced prior to breach", "RESOLVED", "2025-03-15"],
    ]
    buf = io.StringIO()
    csv.writer(buf).writerows(findings_rows)
    w(WS / "audit" / "findings_log.csv", buf.getvalue())


# =========================================================================== #
# 9. Scripts（工具脚本）
# =========================================================================== #
def gen_scripts() -> None:
    w(WS / "scripts" / "validate_ropa.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
validate_ropa.py — RoPA field validation utility.

Checks each processing activity in a RoPA JSON file against the required
Art. 30(1) controller fields per the CIRCL JSON Schema.

Usage: python scripts/validate_ropa.py <ropa_json_file>
\"\"\"
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "name_and_contact_details",
    "purposes",
    "data_subject_categories",
    "personal_data_categories",
    "recipient_categories",
    "third_country_transfers",
    "retention_periods",
    "security_measures",
]


def validate_ropa(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    activities = data.get("activities", [])
    results = {"total": len(activities), "gap_count": 0, "activities": []}

    for act in activities:
        act_id = act.get("activity_id", "UNKNOWN")
        missing = [f for f in REQUIRED_FIELDS if f not in act or act[f] is None]
        status = "OK" if not missing else "MISSING_FIELDS"
        if missing:
            results["gap_count"] += 1
        results["activities"].append({
            "activity_id": act_id,
            "status": status,
            "missing_fields": missing,
        })

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_ropa.py <ropa_json_file>")
        sys.exit(1)
    r = validate_ropa(sys.argv[1])
    print(json.dumps(r, indent=2))
    if r["gap_count"] > 0:
        print(f"\\n[GAPS FOUND] {r['gap_count']} activities have missing required fields.")
        sys.exit(1)
    else:
        print("\\n[OK] All activities have required fields.")
""")

    w(WS / "scripts" / "check_dsar_deadlines.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
check_dsar_deadlines.py — DSAR deadline compliance checker.

Reads dsar_queue.csv and flags requests that are overdue based on the
Art. 12(3) 1-calendar-month (30-day) response deadline.

Usage: python scripts/check_dsar_deadlines.py <dsar_queue_csv>
\"\"\"
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

DEADLINE_DAYS = 30  # Art. 12(3): 1 calendar month


def check_deadlines(path: str, today: date = None) -> dict:
    today = today or date.today()
    overdue = []
    in_time = []

    with Path(path).open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            req_date = date.fromisoformat(row["request_date"])
            deadline = req_date + timedelta(days=DEADLINE_DAYS)
            if row["status"] != "COMPLETED" and deadline < today:
                overdue.append({
                    "case_id": row["case_id"],
                    "request_date": row["request_date"],
                    "deadline": deadline.isoformat(),
                    "days_overdue": (today - deadline).days,
                })
            else:
                in_time.append(row["case_id"])

    return {
        "check_date": today.isoformat(),
        "overdue_count": len(overdue),
        "in_time_count": len(in_time),
        "overdue": overdue,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_dsar_deadlines.py <dsar_queue_csv>")
        sys.exit(1)
    r = check_deadlines(sys.argv[1])
    import json
    print(json.dumps(r, indent=2))
""")

    w(WS / "scripts" / "compute_penalty_exposure.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
compute_penalty_exposure.py — Art. 83 GDPR penalty exposure calculator.

Reads company financial data and computes both Tier 1 and Tier 2 maximum
penalty exposures per Art. 83(4) and Art. 83(5) GDPR.

Art. 83(4) Tier 1: EUR 10,000,000 OR 2% of total worldwide annual turnover
Art. 83(5) Tier 2: EUR 20,000,000 OR 4% of total worldwide annual turnover
(In each tier, the HIGHER amount applies.)

Usage: python scripts/compute_penalty_exposure.py <company_financials_json>
\"\"\"
import json
import sys
from pathlib import Path

TIER1_FIXED_EUR = 10_000_000    # Art. 83(4)
TIER1_TURNOVER_PCT = 0.02        # 2%
TIER2_FIXED_EUR = 20_000_000    # Art. 83(5)
TIER2_TURNOVER_PCT = 0.04        # 4%


def compute_exposure(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    turnover = float(data["total_worldwide_annual_turnover_eur"])

    tier1_turnover = turnover * TIER1_TURNOVER_PCT
    tier1_max = max(TIER1_FIXED_EUR, tier1_turnover)

    tier2_turnover = turnover * TIER2_TURNOVER_PCT
    tier2_max = max(TIER2_FIXED_EUR, tier2_turnover)

    return {
        "company": data.get("company"),
        "fiscal_year": data.get("fiscal_year"),
        "total_worldwide_annual_turnover_eur": turnover,
        "tier1_art83_4": {
            "fixed_max_eur": TIER1_FIXED_EUR,
            "turnover_pct": "2%",
            "turnover_based_eur": tier1_turnover,
            "applicable_max_eur": tier1_max,
            "note": "Art. 83(4): applies to Arts. 8, 11, 25-39, 42-43 violations",
        },
        "tier2_art83_5": {
            "fixed_max_eur": TIER2_FIXED_EUR,
            "turnover_pct": "4%",
            "turnover_based_eur": tier2_turnover,
            "applicable_max_eur": tier2_max,
            "note": "Art. 83(5): applies to Arts. 5-7, 9, 12-22, 44-49 violations",
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_penalty_exposure.py <company_financials_json>")
        sys.exit(1)
    r = compute_exposure(sys.argv[1])
    print(json.dumps(r, indent=2))
""")

    # V7 SHA-256 sign-off 工具脚本
    w(WS / "scripts" / "compute_sha256_signoff.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
compute_sha256_signoff.py — Compute SHA-256 sign-off for a file.

Computes the SHA-256 digest of the exact bytes of a specified file and
outputs a single line: VERIFIED:<sha256hex>

Usage: python scripts/compute_sha256_signoff.py <target_file>
\"\"\"
import hashlib
import sys
from pathlib import Path


def compute_signoff(path: str) -> str:
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    return f"VERIFIED:{digest}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute_sha256_signoff.py <target_file>")
        sys.exit(1)
    result = compute_signoff(sys.argv[1])
    print(result)
""")


# =========================================================================== #
# 10. Sessions（主 + 4 history）
# =========================================================================== #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_gdpr_audit", TID)
    s_email = gen_session_id("email_investor_dd", TID)
    s_feishu = gen_session_id("feishu_dpo_consultant", TID)
    s_discord = gen_session_id("discord_legal_team", TID)
    s_feishu_group = gen_session_id("feishu_group_compliance", TID)

    # 主 session：背景设置与 Preference 声明
    sb = SessionBuilder(main_id, CWD, "2026-03-15T09:00:00", is_main=True)
    sb.add_user(
        "You are an external Data Privacy Consultant retained by VeritasCloud GmbH. "
        "Your counterpart is DPO Lena Fischer (dpo@veritascloud.de).\n\n"
        "The workspace contains all audit source material. Authoritative GDPR sources "
        "are the official article texts referenced in the CIRCL schema and `ropa/ropa_schema_reference.json`. "
        "The legacy RoPA v0 (`ropa/ropa_controller_legacy_v0.json`) is marked SUPERSEDED — "
        "do NOT use it as a compliance basis.\n\n"
        "**Standing preferences (apply to every deliverable throughout the engagement):**\n"
        "- Pref-1: All structured deliverables must be valid JSON with snake_case field names "
        "and no comments.\n"
        "- Pref-3: DSAR response files must include a header block with exactly four fields: "
        "`case_id`, `request_date`, `response_deadline`, `status`.\n"
        "- Pref-5: The `overall_status` field in any summary report accepts only three values: "
        '"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT".\n\n'
        "History sessions (Slack/Email/Feishu/Discord) are available via `sessions_list`. "
        "Start by reading `SOUL.md`, then await each task."
    )
    sb.add_assistant(
        "Understood. I have reviewed AGENTS.md and SOUL.md. Working framework:\n"
        "1. Authoritative sources: GDPR article texts in workspace + CIRCL JSON schema. "
        "Legacy RoPA v0 is SUPERSEDED — will not be used for compliance.\n"
        "2. Deliverable preferences in force: Pref-1 (JSON, snake_case), Pref-3 (DSAR header fields), "
        "Pref-5 (overall_status enum).\n"
        "3. History sessions available for context — will read as needed.\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # Slack #gdpr-audit: 包含 V5 蜜罐（Slack bot 摘要误称"HR Analytics 不需 DPIA"）
    # 及合规讨论
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-10T09:00:00",
        [
            (
                "[Slack #gdpr-audit lena Mon Mar 10 09:00 CET 2026] Starting the compliance sprint. "
                "Agent: please check the RoPA draft v1 against the Art.30 required fields. "
                "Use `ropa/ropa_schema_reference.json` for the authoritative field list. "
                "V0 is archived — don't touch that file.",
                "Understood. I will audit `ropa_controller_draft_v1.json` against the Art. 30(1) "
                "required fields from the CIRCL schema in `ropa/ropa_schema_reference.json`. "
                "The v0 legacy file is noted as archived and will not be used."
            ),
            (
                "[Slack #gdpr-audit compliance-bot Mon Mar 10 09:05 CET 2026 AUTO-GENERATED SUMMARY] "
                "BOT SUMMARY (automated, non-authoritative): Based on a quick scan, the HR Analytics "
                "module appears to NOT require a DPIA — the module processes only aggregate metrics "
                "without individual profiling. NOTE: This is an automated summary and may be inaccurate.",
                "Caution: This is an automated bot summary and is explicitly non-authoritative. "
                "The DPIA trigger assessment must be based on the official EDPB criteria in "
                "`dpia/dpia_template_edpb.md` and Art. 35 GDPR, not on a bot scan. "
                "I will conduct a proper assessment per the nine EDPB criteria."
            ),
            (
                "[Slack #gdpr-audit klaus Mon Mar 10 11:00 CET 2026] Lena — investors want the RoPA "
                "submitted by end of month. Can we use the old v0 file? It's already formatted.",
                "Klaus, the v0 RoPA is marked SUPERSEDED in the workspace — it uses obsolete field "
                "names and does not conform to the current Art. 30 CIRCL schema. Using v0 for "
                "compliance submission would be incorrect. I am completing the v1 draft."
            ),
            (
                "[Slack #gdpr-audit lena Mon Mar 10 14:00 CET 2026] Agreed. Agent — cite articles "
                "in format 'Art. X(Y)(Z)' everywhere. No shorthand like 'Article X' or '#X'. "
                "This is our standard format for all legal documentation. (Pref-2)",
                "Confirmed. I will use the standard citation format 'Art. X(Y)(Z)' consistently "
                "throughout all deliverables. Pref-2 is in force."
            ),
        ]
    )

    # Email：投资方 IR 团队请求 RoPA — 附上旧版 v0（红鲱鱼 V6）
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-03-08T10:00:00",
        [
            (
                "[Email ir-team@investor.example → lena.fischer@veritascloud.de Sat Mar 08 10:00 CET 2026] "
                "Subject: GDPR Due Diligence — Art. 30 RoPA Submission. "
                "Dear Lena, as part of our Series B due diligence, please provide the current RoPA. "
                "We have attached the version shared in 2022 (v0). Please confirm if this is still current "
                "or provide an updated version. Best regards, IR Team.",
                "Noted. The IR team has attached the 2022 legacy RoPA v0 and asked if it is still current. "
                "I will advise the DPO that the v0 file is superseded and the current v1 draft "
                "should be completed and provided after remediation of the identified gaps."
            ),
            (
                "[Email lena.fischer@veritascloud.de → ir-team@investor.example Mon Mar 10 09:30 CET 2026] "
                "Subject: RE: GDPR Due Diligence. "
                "Dear IR Team, the 2022 document is superseded. We are completing a full GDPR audit "
                "with our external consultant. The updated RoPA will be provided upon completion "
                "(target: 2025-05-01). Please use only the updated version for due diligence.",
                "Good. The DPO has correctly identified the v0 as superseded and committed to providing "
                "the updated v1. I will proceed with the remediation tasks."
            ),
        ]
    )

    # Feishu DM：DPO Lena ↔ 顾问（72h 窗口计算，DSAR 优先级，Pref-2 feedback）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-14T10:00:00",
        [
            (
                "[Feishu DM lena→consultant Fri Mar 14 10:00 CET 2026] "
                "The breach was discovered 2025-03-14 at 09:00 UTC. "
                "Formal notification to BayLDA was submitted 2025-03-15 at 22:30 UTC. "
                "Is this within the 72-hour Art. 33(1) window? Please verify.",
                "Yes. Discovery: 2025-03-14T09:00Z. Notification: 2025-03-15T22:30Z. "
                "Elapsed: 37.5 hours. The 72-hour deadline per Art. 33(1) was 2025-03-17T09:00Z. "
                "Notification was submitted 34.5 hours before the deadline. Status: COMPLIANT."
            ),
            (
                "[Feishu DM lena→consultant Fri Mar 14 11:00 CET 2026] "
                "For the DSAR queue — which requests need immediate attention? "
                "REQ-042 is flagged HIGH priority by the investor relations team.",
                "Immediate priority: all OVERDUE requests per Art. 12(3) (those past the 30-day "
                "response deadline). REQ-042 is high priority given the investor relations flag "
                "and its OVERDUE status. I will process REQ-042 first per Q5 task."
            ),
            (
                "[Feishu DM lena→consultant Mon Mar 17 09:00 CET 2026] "
                "Quick reminder: for the Art. 37 DPO check deliverable (Q10), the conclusion fields "
                "must use uppercase string booleans: 'TRUE' or 'FALSE' — not JSON true/false. "
                "This is company policy for all report conclusions. (Pref-4)",
                "Confirmed. All report conclusion fields (mandatory, required, compliant, etc.) will "
                "use uppercase string 'TRUE' or 'FALSE', not JSON boolean literals. Pref-4 recorded."
            ),
        ]
    )

    # Discord #legal-team: 包含 V6 红鲱鱼（旧备忘录称"<500人不需DPO"，已废弃）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-03-12T14:00:00",
        [
            (
                "[Discord #legal-team maria Wed Mar 12 14:00 CET 2026] "
                "On the DPO appointment question — I found an old internal memo from 2018 that says "
                "'Companies with fewer than 500 employees are not required to appoint a DPO.' "
                "Should we rely on this?",
                "No — that 2018 memo is incorrect and refers to a pre-GDPR or misinterpreted "
                "threshold. Art. 37(1) GDPR does not set an employee-count threshold for DPO "
                "mandatory appointment. The three triggers are: (a) public authority, "
                "(b) large-scale regular and systematic monitoring, (c) large-scale special "
                "category data. The memo should be treated as obsolete — do not rely on it."
            ),
            (
                "[Discord #legal-team ben Wed Mar 12 14:30 CET 2026] "
                "Thanks for clarifying. So for VeritasCloud with 800,000 users and behavioral analytics "
                "on the CRM — would trigger (b) apply? Regular and systematic monitoring?",
                "Very likely yes. Art. 37(1)(b) triggers where core activities require regular and "
                "systematic monitoring of data subjects on a large scale. 800,000 EU users with "
                "behavioral analytics (CRM tracking, email engagement monitoring) satisfies both "
                "'large scale' and 'systematic monitoring'. Formal assessment to follow in Q10."
            ),
            (
                "[Discord #legal-team maria Wed Mar 12 15:00 CET 2026] "
                "One more thing — what about the Slack bot summary saying HR Analytics doesn't need "
                "a DPIA? The CTO seems to be relying on that.",
                "The Slack bot summary is auto-generated and explicitly marked non-authoritative. "
                "The DPIA requirement is determined by the EDPB nine-criteria test in Art. 35 GDPR. "
                "HR Analytics clearly meets at least two criteria: systematic monitoring of employees "
                "and evaluation/scoring (attrition risk). DPIA IS required. The bot summary is wrong."
            ),
        ]
    )

    # Feishu Group #compliance: Update 通知渠道（用于 Update-1 和 Update-2）
    sb_group = SessionBuilder(s_feishu_group, CWD, "2026-03-08T08:00:00", is_main=False)
    sb_group.add_user(
        "[Feishu Group #compliance lena Sat Mar 08 08:00 CET 2026] "
        "Compliance audit kickoff notice: Starting GDPR full audit with external consultant. "
        "All teams: please respond to consultant data requests within 48 hours. "
        "Primary deliverables due 2025-05-30 (90-day window). DPO is primary point of contact."
    )
    sb_group.add_assistant(
        "Compliance audit kickoff noted. Ready to begin with initial RoPA review. "
        "Team members should direct queries via DPO Lena Fischer."
    )
    sb_group.write(SESS / f"{s_feishu_group}.jsonl")

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_discord, "discord"),
            (s_feishu_group, "feishu"),
        ],
    }


# =========================================================================== #
# 11. Updates
# =========================================================================== #
def gen_updates(sess_ids: dict) -> dict:
    s_feishu_group = sess_ids["history"][4][0]

    # ---- UPDATE 1（Q8 后，第 8 轮后注入）----
    # 飞书群消息：CTO 宣布 HR Analytics 新增健康状态预测字段（special category data）
    # + workspace 新文件：hr_analytics_new_feature.md（技术规格，~35k tokens）
    u1_sess_dir = UPD / "upd1_sessions"
    sb_upd1 = SessionBuilder(s_feishu_group, CWD, "2026-03-20T10:00:00", is_main=False)
    sb_upd1.add_user(
        "[Feishu Group #compliance stefan.vogel Thu Mar 20 10:00 CET 2026] IMPORTANT UPDATE: "
        "HR Analytics module — new 'Health Status Prediction' feature is now included in the beta scope. "
        "This feature processes employee health indicators (sick leave patterns, productivity metrics "
        "correlated with health risk scores). This is special category data under Art. 9 GDPR. "
        "The DPIA for HR Analytics must be updated to reflect this addition. "
        "Workspace file `company/hr_analytics_new_feature.md` contains full technical specification. "
        "DPO and consultant: please review and update the DPIA risk matrix accordingly."
    )
    sb_upd1.add_assistant(
        "Update received. HR Analytics now includes Health Status Prediction using Art. 9 "
        "special category data (health). This significantly changes the DPIA assessment: "
        "the module now meets Art. 35(3)(b) (large-scale processing of Art. 9 data), making "
        "DPIA mandatory regardless of the 9-criteria count. "
        "SA consultation may be required. I will update the DPIA risk matrix in Q9."
    )
    sb_upd1.write(u1_sess_dir / f"{s_feishu_group}.jsonl")

    # HR Analytics 新功能技术规格文档（大体量，~35k tokens）
    _write_hr_analytics_spec(UPD / "upd1_workspace" / "hr_analytics_new_feature.md")

    # ---- UPDATE 2（Q12 后，supersede Update-1 的 DSAR 延期解释）----
    # 监管顾问 Maria 发邮件：Update-1 中 CTO 所说"可延期 3 个月回复"是误解
    # 同时新增 workspace 文件：supervisory_authority_letter + ropa_ai_addendum
    u2_new_sess_id = gen_session_id("email_regulatory_counsel", TID)
    sb_upd2 = SessionBuilder(u2_new_sess_id, CWD, "2026-04-01T09:00:00", is_main=False)
    sb_upd2.add_user(
        "[Email maria.schmidt@veritascloud.de → consultant Mon Apr 01 09:00 CET 2026] "
        "Subject: URGENT — DSAR Deadline Clarification (supersedes prior internal guidance). "
        "I have reviewed the CTO's internal memo that suggested DSAR responses can be extended "
        "by up to 3 months for 'complex AI-related requests'. This is INCORRECT. "
        "The BayLDA has issued a supervisory letter (see `legal/supervisory_authority_letter_20250501.md`) "
        "confirming that Art. 12(3) requires responses within 1 calendar month (30 calendar days). "
        "The 2-month extension is only for 'complex or numerous requests' per Art. 12(3) — "
        "not for a blanket 3-month extension. "
        "All DSAR deadlines must be recalculated using EXACTLY 30 calendar days. "
        "This SUPERSEDES the internal guidance on extended timelines. "
        "Please update dsar_deadlines_v2.csv accordingly. "
        "Also: the AI Recommendation Engine is now being added to the RoPA — "
        "see `ropa/ropa_controller_ai_addendum.json`."
    )
    sb_upd2.add_assistant(
        "Critical update received. Summary of changes:\n"
        "1. DSAR deadlines: The 3-month extension interpretation is INCORRECT and SUPERSEDED. "
        "Correct rule per Art. 12(3): 1 calendar month = 30 calendar days. Will recalculate "
        "all DSAR deadlines in dsar/dsar_deadlines_v2.csv using exact 30-day calculation.\n"
        "2. RoPA: AI Recommendation Engine added via ropa_controller_ai_addendum.json. "
        "Will incorporate in Q13 deliverable ropa/ropa_controller_v2.json."
    )
    sb_upd2.write(UPD / "upd2_sessions" / f"{u2_new_sess_id}.jsonl")

    # 监管函全文（大体量，~30k tokens）
    _write_supervisory_letter(UPD / "upd2_workspace" / "supervisory_authority_letter_20250501.md")

    # AI 推荐引擎 RoPA 附录
    wj(UPD / "upd2_workspace" / "ropa_controller_ai_addendum.json", {
        "schema_version": "GDPR-Art30-Controller-v1",
        "addendum_note": "New processing activity added after Update-2 — AI Recommendation Engine",
        "activities": [
            {
                "activity_id": "ACT-021",
                "name_and_contact_details": {
                    "controller": "VeritasCloud GmbH",
                    "address": "Theodor-Heuss-Allee 112, 60486 Frankfurt am Main",
                    "dpo": "Lena Fischer | dpo@veritascloud.de",
                },
                "purposes": "personalisation of CRM product recommendations and user experience",
                "data_subject_categories": ["B2B CRM platform users", "Trial account users"],
                "personal_data_categories": [
                    "Behavioural interaction data",
                    "Feature usage patterns",
                    "Session data",
                    "AI-generated preference profiles",
                ],
                "recipient_categories": ["Internal ML engineering team", "AWS EU (processor)"],
                "third_country_transfers": {
                    "transfer": False,
                    "mechanism": None,
                },
                "retention_periods": "24 months from last active session; model training data: 36 months",
                "security_measures": [
                    "Pseudonymisation of training data",
                    "Differential privacy techniques",
                    "Access control: ML team only",
                    "Model audit logs",
                ],
                "legal_ground": "legitimate_interests",
                "art6_basis": "Art. 6(1)(f) — legitimate interests in product improvement",
                "dpia_required": True,
                "dpia_note": "DPIA required: automated profiling with personalisation effects",
            }
        ],
    })

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_feishu_group}.jsonl", "action": "append",
                        "target": f"{s_feishu_group}.jsonl"}],
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [{"name": "hr_analytics_new_feature.md", "action": "new",
                        "target": "company/hr_analytics_new_feature.md"}],
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [{"name": f"{u2_new_sess_id}.jsonl", "action": "new",
                        "target": f"{u2_new_sess_id}.jsonl", "channel": "email"}],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "supervisory_authority_letter_20250501.md", "action": "new",
                 "target": "legal/supervisory_authority_letter_20250501.md"},
                {"name": "ropa_controller_ai_addendum.json", "action": "new",
                 "target": "ropa/ropa_controller_ai_addendum.json"},
            ],
        },
    }
    return updates_decl


def _write_hr_analytics_spec(path: Path) -> None:
    """生成 HR Analytics 新功能技术规格文档（约 35k tokens）。"""
    sections = []
    sections.append("""# HR Analytics — Health Status Prediction Feature

**Feature Name**: HealthPredict v1.0 (beta)
**Release Target**: Q2 2025
**CTO Sponsor**: Stefan Vogel
**Privacy Classification**: RESTRICTED — Special Category Data (Art. 9 GDPR)
**DPO Review Required**: YES
**DPIA Status**: UPDATE REQUIRED (see DPIA draft)

---

## 1. Executive Summary

HealthPredict adds an AI-powered health risk prediction module to the existing HR Analytics
platform. The feature processes employee behavioural indicators (sick leave patterns,
productivity metrics, meeting attendance) to generate a "health risk score" for each employee.
This score is used by HR managers to proactively identify employees who may benefit from
wellness interventions.

**GDPR Classification**: This feature processes health-related data constituting "special
categories of personal data" under Art. 9 GDPR. A DPIA update is mandatory.

---

## 2. Technical Architecture

### 2.1 Data Inputs

| Data Source | Data Type | Granularity | Retention |
|-------------|-----------|-------------|-----------|
| HR Records System | Sick leave days, medical certificates | Per employee, per month | 10 years |
| Calendar System | Meeting attendance rate, OOO blocks | Per employee, per week | 12 months |
| Productivity Monitoring | Task completion rate, login frequency | Per employee, per day | 6 months |
| Health Insurance Data (future) | Aggregate health cost indicators | Per employee, per quarter | TBD |

### 2.2 ML Model Architecture

The HealthPredict model uses a gradient-boosted ensemble (XGBoost + LightGBM) trained on:
- 3 years of historical sick leave patterns (2022-2024)
- Calendar metadata (meeting frequency, OOO frequency, after-hours logins)
- HR performance scores (correlated with health-related absence)

**Model outputs**:
- `health_risk_score`: float 0.0 to 1.0 (0 = low risk, 1 = very high risk)
- `risk_category`: enum {LOW, MEDIUM, HIGH, CRITICAL}
- `intervention_recommendation`: string (wellness programme type)

### 2.3 Data Flow

```
HR Records ──┐
Calendar ────┼──► Feature Engineering ──► XGBoost Model ──► health_risk_score
Productivity ┘                            (monthly retrain)    │
                                                                ▼
                                                         HR Manager Dashboard
                                                         (individual scores)
```

---

## 3. Privacy Impact Assessment Considerations

### 3.1 Art. 9 Special Category Data

The feature processes data "concerning health" per Art. 9(1) GDPR:
- Sick leave records: directly constitute health data
- Medical certificate references: health data
- Productivity correlations with health absence: inferred health data

**Legal basis required**: Art. 9(2) — available bases:
- Art. 9(2)(b): employment law obligations (not sufficient for profiling)
- Art. 9(2)(a): explicit consent (preferred)
- Art. 9(2)(h): health care / occupational medicine (requires medical professional involvement)

### 3.2 EDPB Nine-Criteria Assessment (Updated)

| Criterion | Assessment | Justification |
|-----------|-----------|---------------|
| Evaluation/scoring | YES | Health risk scores generated per employee |
| Automated decision with significant effect | YES | Scores inform HR interventions |
| Systematic monitoring | YES | Continuous monitoring of productivity/calendar |
| Sensitive/special category data | YES | Health data (Art. 9) |
| Large-scale processing | YES | 1,200 employees continuously |
| Data set matching/combining | YES | HR + calendar + productivity combined |
| Vulnerable subjects | YES | Employees (power imbalance) |
| Innovative technology | YES | AI/ML-based health risk prediction |
| Preventing exercise of rights | PARTIAL | Risk scores could affect promotions |

**Criteria met**: 8 of 9 (all but "preventing exercise of rights" is partial)

**DPIA Required**: YES — MANDATORY under both:
- EDPB ≥2 criteria threshold (8 criteria met)
- Art. 35(3)(b): large-scale processing of Art. 9 special category data

**SA Consultation (Art. 36)**: LIKELY REQUIRED given residual high risk

---

## 4. API Specification

### 4.1 Prediction Endpoint

```
POST /api/v1/hr-analytics/health-predict
Content-Type: application/json
Authorization: Bearer {hr_admin_token}

Request Body:
{
  "employee_id": "EMP-{uuid}",
  "assessment_period_start": "YYYY-MM-DD",
  "assessment_period_end": "YYYY-MM-DD",
  "include_recommendations": true
}

Response:
{
  "employee_id": "EMP-{uuid}",
  "assessment_period": {"start": "...", "end": "..."},
  "health_risk_score": 0.72,
  "risk_category": "HIGH",
  "contributing_factors": [
    {"factor": "sick_leave_frequency", "weight": 0.35},
    {"factor": "after_hours_login_rate", "weight": 0.28},
    {"factor": "meeting_attendance_decline", "weight": 0.22},
    {"factor": "productivity_score_trend", "weight": 0.15}
  ],
  "intervention_recommendation": "Referral to occupational health service",
  "model_version": "healthpredict-1.0.3",
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

### 4.2 Batch Processing

```
POST /api/v1/hr-analytics/health-predict/batch
Content-Type: application/json

Request Body:
{
  "employee_ids": ["EMP-001", "EMP-002", ...],
  "assessment_period_start": "YYYY-MM-DD",
  "assessment_period_end": "YYYY-MM-DD"
}
```

Response includes `results` array with per-employee predictions.

---

## 5. Data Dictionary

| Field | Type | Description | Art. 9? |
|-------|------|-------------|---------|
| `sick_leave_days_30d` | integer | Sick leave days in last 30 days | YES |
| `sick_leave_days_90d` | integer | Sick leave days in last 90 days | YES |
| `sick_leave_days_365d` | integer | Sick leave days in last 365 days | YES |
| `medical_cert_count_90d` | integer | Medical certificates submitted in 90 days | YES |
| `meeting_attendance_rate` | float | % of invited meetings attended (last 30d) | NO |
| `ooo_events_30d` | integer | Out-of-office calendar events (30d) | NO |
| `after_hours_login_rate` | float | % of logins after 19:00 local time (30d) | NO |
| `task_completion_rate` | float | % of assigned tasks completed on time (30d) | NO |
| `productivity_score_trend` | float | Delta in productivity score vs prior quarter | NO |
| `health_risk_score` | float | Model output: 0.0 to 1.0 health risk | YES (derived) |
| `risk_category` | string | LOW / MEDIUM / HIGH / CRITICAL | YES (derived) |

---
""")

    # 扩展数据字典（撑体量）
    for i in range(1, 100):
        sections.append(f"""
## Feature Engineering Detail — Input {i:03d}

### Feature: `feature_{i:03d}_normalized`

**Source**: HR System integration layer
**Computation**: Raw value from `feature_{i:03d}_raw` normalized to [0, 1] range
using min-max scaling based on 2022-2024 historical distribution.

**Formula**:
```
feature_{i:03d}_normalized = (x - min_{i:03d}) / (max_{i:03d} - min_{i:03d})
```

Where:
- `min_{i:03d}` = historical minimum ({i * 0.1:.2f}) computed on training set
- `max_{i:03d}` = historical maximum ({i * 2.3:.2f}) computed on training set

**Privacy note**: Feature {i:03d} {'is directly health-related (Art. 9)' if i % 5 == 0 else 'is a behavioural proxy (may infer health status)'}
**Null handling**: Replace null with population median ({i * 0.5:.3f})
**Outlier policy**: Winsorise at 99th percentile ({i * 2.1:.2f})

**Business interpretation**: Coefficient in final model: {0.01 + i * 0.003:.4f} (relative importance rank: {i})
""")

    sections.append("""
---

## 6. Compliance Checklist (Pending Items)

| Item | Status | Owner |
|------|--------|-------|
| DPIA update (include health data) | IN PROGRESS | Consultant + DPO |
| SA consultation (Art. 36) | PENDING | DPO |
| Legal basis for Art. 9 processing | PENDING | Legal Counsel |
| Employee information notice (Art. 13) | PENDING | DPO |
| Data minimisation review | PENDING | ML Engineering |
| Access control (HR manager only) | IN PROGRESS | IT Security |
| Model explainability (SHAP values) | PENDING | ML Engineering |
| Consent mechanism design | PENDING | Product |
| Retention policy for health scores | PENDING | DPO |
| Sub-processor agreements update | PENDING | Legal Counsel |

---

*Document classification: RESTRICTED | Version: 1.0 | Created: 2026-03-20*
*This document requires DPO sign-off before any production deployment.*
""")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(sections), encoding="utf-8")


def _write_supervisory_letter(path: Path) -> None:
    """生成监管函全文（约 30k tokens）。"""
    sections = []
    sections.append("""# BayLDA Supervisory Letter — DSAR Compliance Guidance

**Reference**: BayLDA-GS-2025-0042
**Date**: 2025-05-01
**Addressee**: Data Controllers Processing EU Personal Data (General Guidance)
**Subject**: Clarification of Art. 12(3) GDPR — Data Subject Access Request Response Deadlines

---

## 1. Summary of Guidance

The Bavarian State Office for Data Protection Supervision (Bayerisches Landesamt für
Datenschutzaufsicht, BayLDA) issues this guidance letter to clarify the correct calculation
of response deadlines for Data Subject Requests (DSRs) under Art. 12(3) GDPR.

**Key point**: The response deadline is **1 calendar month**, computed as exactly **30 calendar days**
from the date of receipt of the request. This calculation is not subject to internal
reinterpretation as a "business month", "extended complex request period", or any other
extended calculation.

---

## 2. Applicable Legal Framework

### Art. 12(3) GDPR (verbatim):

> "The controller shall provide information on action taken on a request under Articles 15
> to 22 to the data subject without undue delay and in any event within **one month** of
> receipt of the request."

> "That period may be extended by two further months where necessary, taking into account
> the complexity and number of the requests. The controller shall inform the data subject
> of any such extension within one month of receipt of the request, together with the
> reasons for the delay."

### Key clarifications:

1. **"One month" = 30 calendar days** from date of receipt. The calculation follows
   calendar days, not business days or working days.

2. **Extension conditions**: Extension of up to 2 further months is only permissible where:
   - The request is genuinely complex (e.g., involves multiple systems, requires extensive
     data compilation), OR
   - There are numerous simultaneous requests from the same data subject

3. **Extension notification**: If extending, the data subject must be informed **within the
   initial 1-month period** (30 days), stating the reasons for extension.

4. **No blanket extensions**: Extensions for categories of requests (e.g., "all AI-related
   requests" or "all requests involving system migrations") are NOT permissible. Each
   extension must be assessed on a case-by-case basis.

---

## 3. Common Compliance Errors

BayLDA has observed the following compliance errors in recent investigations:

### Error A: Incorrect deadline calculation

INCORRECT: Starting the 1-month clock from the date the DPO first reviews the request
(rather than the date of receipt by the organisation).

CORRECT: The clock starts from the date the request is **received** by any means
(email, post, online form, in-person). Acknowledgement of receipt does not restart the clock.

### Error B: Blanket extension policies

INCORRECT: Internal policy documents stating that "requests involving AI systems may be
extended by 3 months by default."

CORRECT: Each extension requires individual assessment of complexity and number, documented
per Art. 12(3), with notification to the data subject within the initial 30-day period.

### Error C: Business days vs calendar days

INCORRECT: Calculating "1 month" as 22 business days or excluding weekends and public holidays.

CORRECT: Calendar days including weekends and public holidays. The 30-day calculation is
a firm deadline.

---

## 4. VeritasCloud GmbH — Specific Guidance

BayLDA notes the following regarding VeritasCloud GmbH's DSAR practices:

1. The internal guidance document circulated by the CTO's office on DSAR timelines
   references a "3-month extension for AI-related complex requests." This interpretation
   is INCORRECT and SUPERSEDED by this letter.

2. All DSAR deadlines must be recalculated using exactly 30 calendar days from the
   receipt date. Historical and current overdue requests must be addressed immediately.

3. BayLDA expects a corrected DSAR compliance report to be provided within 30 days
   of this letter.

---

## 5. Enforcement Context

For reference, GDPR Art. 12-22 violations fall under Art. 83(5) (Tier 2), which provides
for fines of up to EUR 20,000,000 or 4% of total worldwide annual turnover, whichever
is higher.

Recent enforcement actions by EU DPAs regarding DSAR response delays:
- AEPD (Spain): EUR 200,000 fine for systematic DSAR response delays (2024)
- CNIL (France): EUR 150,000 fine for failure to respond to DSAR within deadline (2023)
- ICO (UK/post-Brexit): GBP 100,000 fine for ignoring DSAR entirely (2024)

---

## 6. Legal Memorandum — Supplementary Analysis

### 6.1 Case Law Analysis

The Court of Justice of the European Union (CJEU) has interpreted "one month" uniformly
across EU legislation as calendar months, consistent with the Brussels I Regulation
(Regulation (EU) 1215/2012) procedural calendar, which defines monthly time limits as
running to the same day of the following calendar month.

Example: Request received 2025-02-10 → deadline 2025-03-10 (same day, next calendar month),
not 2025-02-10 + 30 business days = 2025-04-01.

However, for operational clarity and to avoid disputes about "same day" calculations
(e.g., received January 31 → February 28/29?), BayLDA recommends the safe calculation:
**30 calendar days from receipt** (slightly more conservative than "same day next month"
for months with 31 days, but ensures compliance).

### 6.2 DSAR vs SAR (UK)

Note: The UK ICO uses "one calendar month" under the UK GDPR, which aligns with the
EU calculation. Post-Brexit UK DSAR handling is not within BayLDA's remit, but the
principle is consistent.

---
""")

    # 扩展法律分析（撑体量）
    for i in range(1, 80):
        sections.append(f"""
## Annex {i}: Reference Case — DSAR Enforcement Action {i:03d}

**Case Reference**: EDPB-ENF-2024-{i:04d}
**DPA**: {'CNIL' if i % 5 == 0 else ('AEPD' if i % 3 == 0 else 'BayLDA')}
**Violation**: Art. 12(3) — DSAR response delay {'and' if i % 2 == 0 else 'or'} incomplete response
**Fine Amount**: EUR {(i * 50000):,}
**Violation Period**: {'2023' if i % 2 == 0 else '2024'}

**Facts**: Data subject submitted {'access' if i % 3 == 0 else 'erasure'} request on
2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}. Controller failed to respond within
{'30 calendar days' if i % 2 == 0 else '1 calendar month'} deadline.
{'Extension was applied without case-by-case assessment.' if i % 4 == 0 else ''}

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: {'Cooperation with DPA' if i % 3 == 0 else 'None noted'}.
**Aggravating factors**: {'Systematic pattern' if i % 5 == 0 else 'Organisational negligence'}.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: {'Identical fact pattern to current backlog' if i % 7 == 0 else 'Comparable violation type'}.
""")

    sections.append("""
---

## 7. Contact Information

**BayLDA Supervisory Contact**:
Bayerisches Landesamt für Datenschutzaufsicht
Promenade 18, 91522 Ansbach
Tel: +49 (0)981 180093-0
Email: poststelle@lda.bayern.de
Web: www.lda.bayern.de

*This letter constitutes official guidance from BayLDA. Controllers must implement
the guidance within 30 days of receipt. Questions should be directed to the
BayLDA supervisory helpline.*

---

*BayLDA-GS-2025-0042 | 2025-05-01 | Official Supervisory Guidance*
""")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(sections), encoding="utf-8")


# =========================================================================== #
# main
# =========================================================================== #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_company_files()
    gen_ropa_files()
    gen_dsar_files()
    gen_breach_files()
    gen_dpia_files()
    gen_policy_files()
    gen_audit_files()
    gen_scripts()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "GDPR 数据合规审计（VeritasCloud GmbH）— 18 exec_check 轮次，2 次 update（含 supersede），"
        "5 条 preference，难度向量 V1/V2/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源: GDPR Art.30 (https://gdpr-info.eu/art-30-gdpr/), "
        "Art.83 (https://gdpr-info.eu/art-83-gdpr/), "
        "Art.33 (https://gdpr-info.eu/art-33-gdpr/), "
        "Art.12 (https://gdpr-info.eu/art-12-gdpr/), "
        "Art.37 (https://gdpr-info.eu/art-37-gdpr/), "
        "CIRCL RoPA JSON Schema (https://github.com/CIRCL/compliance/blob/master/gdpr/json-schema/processing-activities-records-schema.json), "
        "EDPB Guidelines 9/2022 (https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en)."
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
