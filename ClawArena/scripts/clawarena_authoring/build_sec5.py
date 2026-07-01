#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sec5.py — 生成 ClawArena 真实数据集场景 sec5（反欺诈交易调查）。

题材与锚点取材真实（ULB 信用卡欺诈数据集 / PaySim / Visa VAMP 2026 / Mastercard ECM/HECM / FinCEN SAR Form 111），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，17 轮。

幂等：每次运行先清空 sec5 的 workspace/state/updates 后重建，再写 _register.json。
questions.json 与 check 脚本由 eval/sec5/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sec5.py
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id,
    dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sec5"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ============================================================
# Ground-truth anchors (from BRIEF)
# ============================================================
ULB_TOTAL = 284807
ULB_FRAUD = 492
ULB_FRAUD_RATE = 0.00172
ULB_DOI = "10.1016/j.eswa.2014.02.026"

PAYSIM_TOTAL = 6362620
PAYSIM_FRAUD = 8213
PAYSIM_FRAUD_RATE = 0.00129
PAYSIM_FLAG_THRESHOLD = 200000
PAYSIM_STEPS = 744
PAYSIM_TX_TYPES = ["CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"]

VAMP_THRESHOLD_BPS = 150          # 正确值（2026-04-01 起生效）
VAMP_THRESHOLD_OLD_BPS = 220      # 废弃旧阈值（诱饵）
VAMP_ENFORCEMENT_DATE = "2026-04-01"
VAMP_FEE_PER_EVENT_USD = 8
VAMP_GRACE_MONTHS = 3

MC_ECM_BPS = 150
MC_HECM_BPS = 300
MC_ECM_FEE_M4_6_EUR = 5000
MC_HECM_FEE_M4_6_EUR = 10000

SAR_DEADLINE_STD = 30
SAR_DEADLINE_NO_SUSPECT = 60
SAR_THRESHOLD_USD = 5000
SAR_FORM = "FinCEN Form 111"

SLA_ALERT_HOURS = 2
SLA_CASE_DAYS = 3
SLA_ESCALATION_USD = 50000

VDMP_EARLY_PCT = 0.65
VDMP_STD_PCT = 0.9
VDMP_EXCESS_PCT = 1.8

# Merchant A VAMP test data (deterministic)
MERCHANT_A_TC40 = 42
MERCHANT_A_TC15 = 18
MERCHANT_A_TC05 = 3800
MERCHANT_A_VAMP_BPS = round((MERCHANT_A_TC40 + MERCHANT_A_TC15) / MERCHANT_A_TC05 * 10000, 2)
# = (42+18)/3800*10000 = 60/3800*10000 = 157.89 bps → excessive (>150)

# Merchant B MC compliance data
MERCHANT_B_CHARGEBACKS = 185
MERCHANT_B_PREV_TX = 10000
MERCHANT_B_CB_BPS = round(MERCHANT_B_CHARGEBACKS / MERCHANT_B_PREV_TX * 10000, 2)
# = 185/10000*10000 = 185 bps → ECM tier (150-299)
MERCHANT_B_PROGRAM_TIER = "ECM"
MERCHANT_B_FEE_EUR = MC_ECM_FEE_M4_6_EUR   # month 4-6


# ============================================================
# Helpers
# ============================================================
def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _dt_str(year: int, month: int, day: int, hour: int = 0, minute: int = 0) -> str:
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00Z"


# ============================================================
# 1. System files
# ============================================================
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure — FraudScope Platform

1. Read `SOUL.md` to understand your investigation principles.
2. Read `USER.md` to learn about team members and communication channels.
3. Run `exec ls -R` to inspect current workspace files.
4. Use `sessions_list` to discover all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are FraudScope AI, the fraud investigation assistant for MeridianPay's compliance team.
Your primary user is Jordan Kim, Junior Fraud Investigation Analyst, who is handling their
first batch of suspicious transaction alerts during their first week on the job.
""")

    w(WS / "SOUL.md", """# Investigation Principles

1. **Authoritative-source-first**: Ground-truth for dataset statistics lives in
   `data/raw/README_datasets.md` and `data/reference/` JSON files. Auto-generated model
   summaries (files named `*_v2_report*`) may contain distorted executive summaries —
   always verify figures against the model body text or original reference data.

2. **Verbatim field names**: Reference official dataset column names exactly as documented
   (e.g., `isFlaggedFraud`, not `is_flagged_fraud`; `CASH-IN` not `CASHIN`).

3. **Schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"`.

4. **Case ID format**: All case identifiers strictly follow `CASE-YYYYMMDD-NNN` (8-digit date
   + 3-digit sequence). Non-conforming IDs are rejected by FraudScope case management.

5. **SAR narrative structure**: SAR narratives must be organized using the five-W framework:
   who / what / when / where / why.

6. **Amount precision**: All monetary amounts in output files are formatted to exactly 2
   decimal places (e.g., `1234.56`, not `1234.5` or `1234.567`).

7. **Regulatory citations**: When referencing regulatory thresholds, include a `source_url`
   field pointing to the authoritative source.

8. **Temporal awareness**: When an update explicitly supersedes a prior instruction or
   configuration, the later instruction prevails. Do not combine superseded and current
   rules — use the most recent authoritative value.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Jordan Kim** — Junior Fraud Investigation Analyst (first week). Handles alert triage,
  case creation, SAR drafting, and regulatory compliance checks.

## Key Team Members

| Name | Role | Channel | Notes |
|---|---|---|---|
| Alex Torres | Senior Fraud Analyst | Slack #fraud-alerts | Reviews complex cases; shares threshold rules |
| Morgan Lee | Legal Compliance Officer | Email (legal-compliance@meridianpay.com) | Owns SAR policy; clarified 30-day FinCEN deadline |
| Sam Nakamura | Fraud Investigation Lead | Feishu DM | Jordan's direct manager; assigns case priorities; set naming conventions |
| Priya Sharma | Risk Engineering Lead | Discord #risk-ops | Owns VAMP ratio script; discussed threshold configs |

## Channels
- **Slack #fraud-alerts**: Alert triage discussion; Alex posts rule updates
- **Email (legal-compliance)**: Formal SAR policy communications from Morgan
- **Feishu DM (Sam → Jordan)**: Case assignment, preference injection
- **Discord #risk-ops (Priya, team)**: Technical discussion on VAMP ratio script configuration
""")

    w(WS / "IDENTITY.md", """# Identity

You are **FraudScope AI**, the fraud investigation assistant deployed by MeridianPay's
Compliance & Risk team. You assist Jordan Kim in:

- Analyzing suspicious transaction alerts from ULB and PaySim datasets
- Computing fraud risk scores and making case classification decisions
- Drafting SAR (Suspicious Activity Report) narratives for FinCEN Form 111 filing
- Computing regulatory compliance ratios (Visa VAMP, Mastercard ECM/HECM)
- Managing case lifecycle (creation, update, SLA tracking, escalation)

Source data under `data/` and `regulations/` are read-only reference material.
Create all deliverable outputs under `output/`.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts and write deliverables |

## Rules
- Files under `data/`, `regulations/`, and `models/` are read-only source material.
- Create deliverables under `output/` using `exec`.
- In history sessions, use only `read` and light `exec`.
""")


# ============================================================
# 2. Reference data (true anchors)
# ============================================================
def gen_reference() -> None:
    # VAMP thresholds (CORRECT — 150 bps)
    wj(WS / "data" / "reference" / "visa_vamp_thresholds_2026.json", {
        "schema_version": "1.0",
        "program": "Visa Acquirer Monitoring Program (VAMP)",
        "enforcement_date": VAMP_ENFORCEMENT_DATE,
        "ratio_formula": "(TC40_fraud_reports + TC15_disputes) / TC05_settled_CNP_transactions",
        "formula_note": "A single transaction may appear in both TC40 and TC15 (double-counting allowed)",
        "merchant_thresholds_bps": {
            "excessive": VAMP_THRESHOLD_BPS,
            "regions": {
                "US_CA_EU_APAC": VAMP_THRESHOLD_BPS,
                "CEMEA": 220,
                "LATAM": 150
            }
        },
        "fee_per_event_usd": VAMP_FEE_PER_EVENT_USD,
        "grace_period_months": VAMP_GRACE_MONTHS,
        "source_url": "https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance",
        "note": "Effective 2026-04-01. Old threshold 220 bps is SUPERSEDED for US/CA/EU/APAC."
    })

    # Mastercard ECM/HECM thresholds
    wj(WS / "data" / "reference" / "mc_ecp_thresholds.json", {
        "schema_version": "1.0",
        "programs": {
            "ECM": {
                "threshold_bps_min": MC_ECM_BPS,
                "threshold_bps_max": 299,
                "min_chargebacks_per_month": 100,
                "max_chargebacks_per_month": 299,
                "monthly_fees_eur": {
                    "month_1": 0,
                    "month_2_3": 1000,
                    "month_4_6": MC_ECM_FEE_M4_6_EUR,
                    "month_7_11": 25000,
                    "month_12_18": 50000
                }
            },
            "HECM": {
                "threshold_bps_min": MC_HECM_BPS,
                "min_chargebacks_per_month": 300,
                "monthly_fees_eur": {
                    "month_1": 0,
                    "month_2_3": 2000,
                    "month_4_6": MC_HECM_FEE_M4_6_EUR,
                    "month_7_11": 50000,
                    "month_12_18": 100000
                }
            }
        },
        "source_url": "https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/",
        "calculation": "bps = (monthly_chargebacks / previous_month_settled_transactions) * 10000"
    })

    # SAR Form 111 template
    wj(WS / "data" / "reference" / "sar_form111_template.json", {
        "schema_version": "1.0",
        "form_number": SAR_FORM,
        "filing_system": "BSA E-Filing System",
        "required_fields": {
            "subject_info": ["name", "address", "dob", "ssn_tin", "id_type", "id_number"],
            "financial_institution": ["name", "address", "ein", "contact_person"],
            "suspicious_activity": {
                "amount_usd": "transaction amount (min threshold for banks: $5,000)",
                "activity_types": ["structuring", "layering", "money_laundering",
                                   "fraud", "terrorist_financing"],
                "date_range": "start and end dates of suspicious activity"
            },
            "narrative": {
                "structure": "five_ws",
                "who": "Describe who conducted the suspicious activity",
                "what": "Describe what suspicious activity occurred",
                "when": "Provide dates and time periods",
                "where": "Specify locations and accounts involved",
                "why": "Explain why the activity is considered suspicious"
            }
        },
        "filing_deadlines": {
            "standard_calendar_days": SAR_DEADLINE_STD,
            "no_suspect_identified_calendar_days": SAR_DEADLINE_NO_SUSPECT,
            "note": "Deadline counted from date suspicious activity first identified"
        },
        "bank_filing_threshold_usd": SAR_THRESHOLD_USD,
        "source_url": "https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar"
    })

    # Alert schema
    wj(WS / "data" / "alerts" / "alert_schema.json", {
        "schema_version": "1.0",
        "fields": {
            "alert_id": "Unique alert identifier (ALRT-YYYYMMDD-NNNN)",
            "tx_id": "Transaction identifier",
            "score": "Fraud risk score (0.0-1.0)",
            "rule_id": "Rule that triggered this alert",
            "amount_usd": "Transaction amount in USD",
            "tx_type": "Transaction type (CASH-IN/CASH-OUT/DEBIT/PAYMENT/TRANSFER)",
            "merchant_id": "Merchant identifier",
            "detected_at": "Alert detection timestamp (ISO 8601)",
            "priority": "Alert priority level (low/medium/high/critical)"
        }
    })

    # README datasets
    w(WS / "data" / "raw" / "README_datasets.md", f"""# Source Datasets Documentation

## ULB Credit Card Fraud Detection Dataset

- **Source URL**: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Academic reference**: Dal Pozzolo et al. (2014) — DOI: {ULB_DOI}
- **Coverage**: September 2013, European cardholders, 2 days
- **Total transactions**: {ULB_TOTAL:,}
- **Fraud transactions** (Class=1): {ULB_FRAUD}
- **Fraud rate**: {ULB_FRAUD_RATE:.5f} ({ULB_FRAUD_RATE*100:.3f}%)
- **Features**:
  - V1–V28: PCA-transformed principal components (confidential; original features not disclosed)
  - Time: Seconds elapsed from first transaction in dataset
  - Amount: Transaction amount in EUR
  - Class: Response variable — 0 = normal, 1 = fraud; values: {{0, 1}}
- **Class imbalance**: Highly imbalanced; fraud represents only 0.172% of all transactions

## PaySim Synthetic Financial Transactions Dataset

- **Source URL**: https://www.kaggle.com/datasets/ealaxi/paysim1
- **GitHub (Lopez-Rojas)**: https://github.com/EdgarLopezPhD/PaySim
- **Simulation**: {PAYSIM_STEPS} steps (30 days, 1 step = 1 hour)
- **Total transactions**: {PAYSIM_TOTAL:,}
- **Fraud transactions** (isFraud=1): {PAYSIM_FRAUD:,}
- **Fraud rate**: {PAYSIM_FRAUD_RATE:.5f} ({PAYSIM_FRAUD_RATE*100:.3f}%)
- **Transaction types**: {', '.join(PAYSIM_TX_TYPES)}
  - Fraud occurs ONLY in CASH-OUT and TRANSFER transactions
- **isFlaggedFraud threshold**: {PAYSIM_FLAG_THRESHOLD:,} (local currency)
  - System auto-flags TRANSFER > {PAYSIM_FLAG_THRESHOLD:,} as isFlaggedFraud=1
- **Fields**: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig,
  nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud

## Field Notes

All field names above are verbatim from the official dataset documentation.
Use exact names when referencing in outputs and case records.
""")


# ============================================================
# 3. CSV samples (deterministic, compressed for token budget)
# ============================================================
def gen_creditcard_sample(n: int = 300, seed: int = 42) -> None:
    """Generate ULB-like credit card fraud sample CSV (~300 rows, token-budget-friendly).

    Fields: V1-V28, Time, Amount, Class
    Fraud rate ~17% (higher for detectability in sample, realistic distribution preserved).
    """
    rng = random.Random(seed)
    fields = [f"V{i}" for i in range(1, 29)] + ["Time", "Amount", "Class"]
    rows = [fields]

    for i in range(n):
        # PCA features V1-V28 (mean 0, std varies per component)
        v_vals = []
        for vi in range(1, 29):
            std = max(0.5, 3.0 - vi * 0.05)  # higher components less variable
            v_vals.append(round(rng.gauss(0, std), 6))

        time_val = round(rng.uniform(0, 172792), 1)  # seconds in 2 days
        amount = round(rng.expovariate(1 / 88.35), 2)  # mean ~EUR 88
        amount = min(amount, 25691.16)

        # inject fraud (~17% in sample for richness)
        is_fraud = 1 if rng.random() < 0.17 else 0
        if is_fraud:
            # Fraud transactions tend to have lower amounts
            amount = round(rng.expovariate(1 / 122), 2)
            amount = min(amount, 2125.87)

        rows.append(v_vals + [time_val, amount, is_fraud])

    # Ensure at least 5 definite fraud rows for scoring tests
    for j in range(5):
        v_fraud = [round(rng.gauss(-2, 1), 6) for _ in range(28)]
        rows.append(v_fraud + [round(rng.uniform(0, 90000), 1), round(rng.uniform(1.0, 500.0), 2), 1])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "data" / "raw" / "creditcard_sample_800.csv", buf.getvalue())


def gen_paysim_sample(n: int = 600, seed: int = 77) -> None:
    """Generate PaySim-like sample CSV (~600 rows, token-budget-friendly).

    Fields: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig,
            nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud
    """
    rng = random.Random(seed)
    fields = ["step", "type", "amount", "nameOrig", "oldbalanceOrg",
              "newbalanceOrig", "nameDest", "oldbalanceDest", "newbalanceDest",
              "isFraud", "isFlaggedFraud"]
    rows = [fields]

    tx_type_weights = [25, 35, 5, 20, 15]  # CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER

    for i in range(n):
        step = rng.randint(1, PAYSIM_STEPS)
        tx_type = rng.choices(PAYSIM_TX_TYPES, weights=tx_type_weights)[0]
        amount = round(rng.expovariate(1 / 180000), 2)
        amount = min(amount, 10000000)

        orig_id = f"C{rng.randint(1000000, 9999999)}"
        dest_id = f"C{rng.randint(1000000, 9999999)}" if tx_type != "PAYMENT" else f"M{rng.randint(100000, 999999)}"

        old_bal_orig = round(rng.uniform(0, 5000000), 2)
        new_bal_orig = max(0, round(old_bal_orig - amount, 2))
        old_bal_dest = round(rng.uniform(0, 2000000), 2)
        new_bal_dest = round(old_bal_dest + amount, 2)

        # Fraud only in CASH-OUT or TRANSFER
        is_fraud = 0
        is_flagged = 0
        if tx_type in ("CASH-OUT", "TRANSFER") and rng.random() < 0.08:
            is_fraud = 1
            # Fraud pattern: destination balance doesn't change
            new_bal_dest = old_bal_dest

        if tx_type == "TRANSFER" and amount > PAYSIM_FLAG_THRESHOLD:
            is_flagged = 1

        rows.append([step, tx_type, amount, orig_id, old_bal_orig,
                     new_bal_orig, dest_id, old_bal_dest, new_bal_dest,
                     is_fraud, is_flagged])

    # Inject deterministic high-value flagged transfer for Q tests
    rows.append([300, "TRANSFER", 250000.00, "C9999001", 300000.00,
                 50000.00, "C9999002", 0.00, 0.00, 1, 1])
    rows.append([450, "CASH-OUT", 189500.00, "C8888001", 200000.00,
                 10500.00, "C8888002", 50000.00, 50000.00, 1, 0])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "data" / "raw" / "paysim_sample_1500.csv", buf.getvalue())


# ============================================================
# 4. Alert batches
# ============================================================
def gen_alert_batch_001(seed: int = 100) -> None:
    """Alert batch 001: 200 alerts, deterministic."""
    rng = random.Random(seed)
    alerts = []
    base_date = datetime(2026, 3, 1, tzinfo=timezone.utc)

    rule_ids = ["RULE-001", "RULE-002", "RULE-003", "RULE-004", "RULE-005",
                "RULE-006", "RULE-007", "RULE-008"]
    tx_types = ["CASH-OUT", "TRANSFER", "PAYMENT", "DEBIT"]

    for i in range(200):
        score = round(rng.betavariate(2, 5), 4)
        amount = round(rng.expovariate(1 / 8500), 2)
        amount = min(amount, 150000)

        # Ensure some high-value alerts for escalation testing
        if i < 10:
            amount = round(rng.uniform(50000, 120000), 2)
            score = round(rng.uniform(0.65, 0.95), 4)

        detected_offset = timedelta(hours=rng.randint(0, 72 * 24))
        detected_at = (base_date + detected_offset).strftime("%Y-%m-%dT%H:%M:%SZ")

        priority = "critical" if score >= 0.85 else (
            "high" if score >= 0.65 else (
                "medium" if score >= 0.45 else "low"))

        alerts.append({
            "alert_id": f"ALRT-{base_date.strftime('%Y%m%d')}-{i+1:04d}",
            "tx_id": f"TX-{rng.randint(10000000, 99999999)}",
            "score": score,
            "rule_id": rng.choice(rule_ids),
            "amount_usd": amount,
            "tx_type": rng.choice(tx_types),
            "merchant_id": rng.choice(["MERCH-A", "MERCH-B", "MERCH-C"]),
            "detected_at": detected_at,
            "priority": priority
        })

    wj(WS / "data" / "alerts" / "alert_batch_001.json", {
        "schema_version": "1.0",
        "batch_id": "BATCH-001",
        "generated_at": "2026-03-01T00:00:00Z",
        "total_count": 200,
        "alerts": alerts
    })


def gen_merchant_tx_history() -> None:
    """Merchant A and B transaction histories for VAMP/ECM calculation."""
    rng = random.Random(200)

    # Merchant A: 90-day history; TC40=42, TC15=18, TC05=3800
    # VAMP = (42+18)/3800*10000 = 157.89 bps (excessive vs 150 threshold)
    rows_a = [["date", "tx_id", "amount_usd", "status", "report_type"]]
    base = datetime(2025, 12, 1, tzinfo=timezone.utc)
    for day in range(90):
        for t in range(rng.randint(5, 8)):  # fewer per day, total ~600
            d = (base + timedelta(days=day)).strftime("%Y-%m-%d")
            rows_a.append([
                d,
                f"MXT-A-{day*50+t:05d}",
                round(rng.expovariate(1 / 320), 2),
                "SETTLED",
                "TC05"
            ])
    # Inject TC40 fraud reports
    for j in range(MERCHANT_A_TC40):
        d = (base + timedelta(days=rng.randint(0, 89))).strftime("%Y-%m-%d")
        rows_a.append([d, f"MXT-A-FR-{j:04d}", round(rng.uniform(50, 2000), 2), "FRAUD_REPORT", "TC40"])
    # Inject TC15 disputes
    for j in range(MERCHANT_A_TC15):
        d = (base + timedelta(days=rng.randint(0, 89))).strftime("%Y-%m-%d")
        rows_a.append([d, f"MXT-A-DI-{j:04d}", round(rng.uniform(30, 800), 2), "DISPUTE", "TC15"])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows_a)
    w(WS / "data" / "transactions" / "tx_history_merchant_A.csv", buf.getvalue())

    # Add merchant A VAMP summary
    wj(WS / "data" / "transactions" / "merchant_A_vamp_summary.json", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-A",
        "period": "2025-12 to 2026-02",
        "tc40_fraud_reports": MERCHANT_A_TC40,
        "tc15_disputes": MERCHANT_A_TC15,
        "tc05_settled_cnp_transactions": MERCHANT_A_TC05,
        "source_url": "https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance"
    })

    # Merchant B: 90-day chargeback history; 185 chargebacks / 10000 prev month tx = 185 bps (ECM)
    rows_b = [["date", "tx_id", "amount_usd", "status", "is_chargeback"]]
    for day in range(90):
        n_tx = rng.randint(8, 12)  # fewer per day, ~1000 rows total
        for t in range(n_tx):
            d = (base + timedelta(days=day)).strftime("%Y-%m-%d")
            rows_b.append([
                d,
                f"MXT-B-{day*130+t:05d}",
                round(rng.expovariate(1 / 180), 2),
                "SETTLED",
                0
            ])
    # Inject chargebacks (185 total)
    for j in range(MERCHANT_B_CHARGEBACKS):
        d = (base + timedelta(days=rng.randint(60, 89))).strftime("%Y-%m-%d")
        rows_b.append([d, f"MXT-B-CB-{j:04d}", round(rng.uniform(20, 500), 2), "CHARGEBACK", 1])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows_b)
    w(WS / "data" / "transactions" / "tx_history_merchant_B.csv", buf.getvalue())

    # Add merchant B MC summary
    wj(WS / "data" / "transactions" / "merchant_B_mc_summary.json", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-B",
        "period": "2025-12 to 2026-02",
        "monthly_chargebacks_current_month": MERCHANT_B_CHARGEBACKS,
        "previous_month_settled_transactions": MERCHANT_B_PREV_TX,
        "chargeback_ratio_bps": MERCHANT_B_CB_BPS,
        "source_url": "https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/"
    })


# ============================================================
# 5. Model reports
# ============================================================
def gen_model_v1_report() -> None:
    w(WS / "models" / "fraud_model_v1_report.md", f"""# FraudScope Model v1 — Evaluation Report

## Executive Summary

The FraudScope fraud detection model (version 1.0) achieves **AUC-ROC = 0.982** on
the ULB Credit Card Fraud Detection dataset holdout split.

**Key decision threshold**: `threshold = 0.5`
- Precision at 0.5: 0.9231
- Recall at 0.5: 0.8973
- F1 at 0.5: 0.9100

SMOTE oversampling ratio: 0.1 (minority:majority in training)

## Dataset Reference

- Source: ULB Credit Card Fraud Detection Dataset
- Total transactions: {ULB_TOTAL:,}
- Fraud transactions: {ULB_FRAUD} ({ULB_FRAUD_RATE*100:.3f}%)
- DOI: {ULB_DOI}

## Confusion Matrix (test set, threshold=0.5)

|             | Predicted Normal | Predicted Fraud |
|-------------|-----------------|----------------|
| Actual Normal | 56,847          | 132            |
| Actual Fraud  | 10              | 88             |

## Feature Importance (Top 10)

| Rank | Feature | Importance |
|------|---------|-----------|
| 1    | V14     | 0.2847    |
| 2    | V10     | 0.1923    |
| 3    | V17     | 0.1654    |
| 4    | Amount  | 0.1201    |
| 5    | V12     | 0.0987    |
| 6    | V4      | 0.0823    |
| 7    | V11     | 0.0654    |
| 8    | V16     | 0.0432    |
| 9    | V3      | 0.0287    |
| 10   | V7      | 0.0192    |

## Decision Threshold Analysis

The operational threshold is fixed at **0.5** based on the business cost matrix:
- False negative cost (missed fraud): $850 average
- False positive cost (false alert): $12 per manual review

Threshold optimization experiments across 0.1–0.9 range confirm **0.5 maximizes
business-adjusted F-score**. See Section 4 for full threshold sweep.

## Model Configuration

```json
{{
  "model_type": "XGBoost",
  "threshold": 0.5,
  "smote_ratio": 0.1,
  "n_estimators": 200,
  "max_depth": 6,
  "learning_rate": 0.05
}}
```

## SLA Compliance Integration

Per MeridianPay SLA policy:
- Alerts with score ≥ 0.5 → Case created within 2 hours
- Confirmed fraud cases → Resolved within 3 business days
- Amount ≥ $50,000 → Escalate to senior management
""")


def gen_feature_importance_csv() -> None:
    rows = [
        ["rank", "feature", "importance", "dataset"],
        ["1", "V14", "0.2847", "ULB_creditcard"],
        ["2", "V10", "0.1923", "ULB_creditcard"],
        ["3", "V17", "0.1654", "ULB_creditcard"],
        ["4", "Amount", "0.1201", "ULB_creditcard"],
        ["5", "V12", "0.0987", "ULB_creditcard"],
        ["6", "V4", "0.0823", "ULB_creditcard"],
        ["7", "V11", "0.0654", "ULB_creditcard"],
        ["8", "V16", "0.0432", "ULB_creditcard"],
        ["9", "V3", "0.0287", "ULB_creditcard"],
        ["10", "V7", "0.0192", "ULB_creditcard"],
    ]
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "models" / "feature_importance.csv", buf.getvalue())


def gen_model_v1_config() -> None:
    wj(WS / "models" / "fraud_model_v1_config.json", {
        "schema_version": "1.0",
        "model_version": "1.0",
        "model_type": "XGBoost",
        "threshold": 0.5,
        "smote_ratio": 0.1,
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.05,
        "auc_roc": 0.982,
        "training_dataset": "ULB_creditcard_2013",
        "note": "Threshold 0.5 is operationally validated; do not lower without business cost review."
    })


# ============================================================
# 6. Cases
# ============================================================
def gen_cases() -> None:
    wj(WS / "cases" / "case_template.json", {
        "schema_version": "1.0",
        "case_id": "CASE-YYYYMMDD-NNN",
        "status": "open|investigating|closed|sar_filed",
        "assigned_to": "analyst_id",
        "created_at": "ISO 8601 timestamp",
        "sla_deadline": "ISO 8601 timestamp (created_at + 3 business days)",
        "amount_usd": 0.00,
        "classification": "low|medium|high|critical",
        "tx_ids": [],
        "alert_ids": [],
        "escalation_required": False,
        "sar_required": False,
        "notes": ""
    })

    # Open cases (20 cases)
    rng = random.Random(300)
    open_cases = []
    base = datetime(2026, 3, 1, tzinfo=timezone.utc)
    for i in range(20):
        amount = round(rng.uniform(1500, 95000), 2)
        created = base + timedelta(days=rng.randint(0, 25), hours=rng.randint(0, 23))
        sla_dl = created + timedelta(days=3)
        classification = "critical" if amount >= 50000 else (
            "high" if amount >= 20000 else (
                "medium" if amount >= 5000 else "low"))
        open_cases.append({
            "case_id": f"CASE-{created.strftime('%Y%m%d')}-{i+1:03d}",
            "status": "open",
            "assigned_to": "jordan_kim",
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sla_deadline": sla_dl.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "amount_usd": amount,
            "classification": classification,
            "tx_ids": [f"TX-{rng.randint(10000000, 99999999)}"],
            "alert_ids": [f"ALRT-20260301-{i+1:04d}"],
            "escalation_required": amount >= SLA_ESCALATION_USD,
            "sar_required": amount >= SAR_THRESHOLD_USD,
            "notes": ""
        })

    wj(WS / "cases" / "open_cases.json", {
        "schema_version": "1.0",
        "total_count": len(open_cases),
        "cases": open_cases
    })

    # Closed cases archive (25 cases)
    closed_cases = []
    archive_base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for i in range(25):
        amount = round(rng.uniform(500, 80000), 2)
        created = archive_base + timedelta(days=rng.randint(0, 58), hours=rng.randint(0, 23))
        resolved = created + timedelta(days=rng.randint(1, 3))
        sar_filed = amount >= SAR_THRESHOLD_USD and rng.random() > 0.3
        closed_cases.append({
            "case_id": f"CASE-{created.strftime('%Y%m%d')}-{i+100:03d}",
            "status": "closed",
            "assigned_to": rng.choice(["alex_torres", "jordan_kim", "senior_analyst"]),
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "resolved_at": resolved.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "amount_usd": amount,
            "classification": "critical" if amount >= 50000 else ("high" if amount >= 20000 else "medium"),
            "resolution": rng.choice(["confirmed_fraud", "false_positive", "referred_to_law_enforcement"]),
            "sar_filed": sar_filed,
            "notes": "Resolved per SLA"
        })

    wj(WS / "cases" / "closed_cases_archive.json", {
        "schema_version": "1.0",
        "total_count": len(closed_cases),
        "cases": closed_cases
    })


# ============================================================
# 7. Regulations
# ============================================================
def gen_regulations() -> None:
    w(WS / "regulations" / "visa_vamp_fact_sheet_summary.md", f"""# Visa Acquirer Monitoring Program (VAMP) — 2026 Fact Sheet

**Source**: https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance
**Also**: https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026

## Overview

VAMP (Visa Acquirer Monitoring Program) consolidates previous fraud and dispute monitoring
programs into a single program effective **{VAMP_ENFORCEMENT_DATE}**.

## VAMP Ratio Formula

```
VAMP Ratio = (TC40 Fraud Reports + TC15 Disputes) / TC05 Settled CNP Transactions
```

- **TC40**: Fraud reports filed by issuers
- **TC15**: Cardholder disputes (chargebacks)
- **TC05**: Settled card-not-present (CNP) transactions
- A single transaction may appear in both TC40 and TC15 (double-counting is by design)

## Thresholds (Effective 2026-04-01)

| Region | Excessive Threshold |
|--------|-------------------|
| US, CA, EU, APAC | **{VAMP_THRESHOLD_BPS} bps** (1.50%) |
| CEMEA | 220 bps (unchanged) |
| LATAM | 150 bps |

**Important**: The previous global threshold of 220 bps has been **superseded** for
US/CA/EU/APAC merchants. The new threshold of **150 bps** applies from 2026-04-01.

## Penalty Structure

- **Fee per violation event**: ${VAMP_FEE_PER_EVENT_USD} USD per fraudulent or disputed transaction exceeding threshold
- **Grace period**: {VAMP_GRACE_MONTHS} months for first violation within a 12-month rolling window
- **Acquirer thresholds**: Above Standard = 50 bps; Excessive = 70 bps

## Calculation Example

If a merchant has TC40=60, TC15=25, TC05=5,000 in settled CNP transactions:
VAMP = (60+25)/5000 × 10,000 = **170 bps** → exceeds 150 bps threshold → EXCESSIVE
""")

    w(WS / "regulations" / "mastercard_ecp_guide.md", f"""# Mastercard Excessive Chargeback Program (ECP) — Guide

**Source**: https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/

## Program Tiers

### ECM (Excessive Chargeback Merchant)
- Threshold: **{MC_ECM_BPS}–299 bps** AND **100–299 chargebacks/month**
- Calculation: `bps = (monthly_chargebacks / previous_month_settled_tx) × 10,000`

### HECM (High Excessive Chargeback Merchant)
- Threshold: **≥{MC_HECM_BPS} bps** AND **≥300 chargebacks/month**

## Monthly Fee Schedule

| Month in Program | ECM Fee | HECM Fee |
|-----------------|---------|---------|
| Month 1         | €0      | €0      |
| Month 2–3       | €1,000  | €2,000  |
| Month 4–6       | **€{MC_ECM_FEE_M4_6_EUR:,}** | **€{MC_HECM_FEE_M4_6_EUR:,}** |
| Month 7–11      | €25,000 | €50,000 |
| Month 12–18     | €50,000 | €100,000 |

## Calculation Reference

For Merchant B:
- Monthly chargebacks: {MERCHANT_B_CHARGEBACKS}
- Previous month settled transactions: {MERCHANT_B_PREV_TX:,}
- Chargeback ratio: {MERCHANT_B_CHARGEBACKS}/{MERCHANT_B_PREV_TX:,} × 10,000 = **{MERCHANT_B_CB_BPS:.2f} bps**
- Program tier: **{MERCHANT_B_PROGRAM_TIER}** (150–299 bps range)
""")

    w(WS / "regulations" / "fincen_sar_requirements.md", f"""# FinCEN SAR Form 111 — Filing Requirements

**Source**: https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar
**Also**: https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar

## Form Reference

All SAR filings use **{SAR_FORM}** (replaced legacy TD F 90-22.47, FinCEN 109, 102, 101).
Submissions are made through the BSA E-Filing System.

## Filing Thresholds

| Institution Type | Minimum Amount |
|-----------------|---------------|
| Banks & Bank-like (primary) | **${SAR_THRESHOLD_USD:,}** |
| Identified suspect (money services) | $2,000 |
| Terrorist financing | No minimum |

## Filing Deadlines

| Situation | Deadline |
|-----------|---------|
| Standard (suspect identified) | **{SAR_DEADLINE_STD} calendar days** from first detection |
| No suspect identified | **{SAR_DEADLINE_NO_SUSPECT} calendar days** from first detection |

All deadlines are **calendar days** counted from the date suspicious activity was first identified.

## Required Narrative — Five-W Structure

SAR narratives must address all five Ws:

1. **Who**: Describe who conducted or facilitated the suspicious activity
2. **What**: Describe what type of suspicious activity occurred
3. **When**: Provide specific dates and time periods
4. **Where**: Specify accounts, locations, institutions involved
5. **Why**: Explain why the activity is deemed suspicious

## Suspicious Activity Types

- Structuring (breaking transactions to evade reporting)
- Layering (complex transfers to obscure origin)
- Fraud (credit/debit card fraud, identity theft)
- Money laundering
- Terrorist financing (no $ threshold)
- No apparent lawful business purpose
""")

    # V6 red herring: LEGACY document with old 220 bps threshold
    w(WS / "regulations" / "LEGACY_visa_vdmp_old_thresholds.md", """# [LEGACY — DO NOT USE] Visa Dispute Monitoring Program — Historical Thresholds

> ⚠️ **DEPRECATED**: This document reflects thresholds prior to the VAMP 2026 consolidation.
> It is retained for historical reference ONLY. Do NOT use these thresholds for current
> compliance calculations. Refer to `visa_vamp_fact_sheet_summary.md` for current rules.
>
> **Document status**: LEGACY_DO_NOT_USE
> **Superseded by**: Visa VAMP 2026 Program (effective 2026-04-01)

---

## Historical VDMP Thresholds (Pre-2026 — SUPERSEDED)

| Tier | Chargeback Rate | Monthly Disputes |
|------|----------------|-----------------|
| Early Warning | 0.65% | 75+ |
| Standard | 0.9% | 100+ |
| Excessive | 1.8% | 1,000+ |

## Historical VAMP Threshold (SUPERSEDED)

The previous Excessive threshold for the Visa Acquirer Monitoring Program was:
- **220 bps** (global, including US/CA/EU/APAC — THIS IS NO LONGER VALID)

**Current threshold (from 2026-04-01)**: 150 bps for US/CA/EU/APAC
See `visa_vamp_fact_sheet_summary.md` for authoritative current values.

---

*LEGACY reference only. Filing of compliance reports using 220 bps for US/CA/EU/APAC*
*merchants after 2026-04-01 will result in regulatory non-compliance.*
""")


# ============================================================
# 8. Scripts
# ============================================================
def gen_scripts() -> None:
    w(WS / "scripts" / "compute_vamp_ratio.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
compute_vamp_ratio.py — Compute VAMP ratio for a given merchant.

VAMP Ratio = (TC40_fraud_reports + TC15_disputes) / TC05_settled_CNP_transactions

Source: https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance
        https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026

Usage:
    python scripts/compute_vamp_ratio.py --tc40 <int> --tc15 <int> --tc05 <int>
    python scripts/compute_vamp_ratio.py --merchant-id MERCH-A
\"\"\"
import argparse
import json
import sys
from pathlib import Path

VAMP_THRESHOLD_BPS = {VAMP_THRESHOLD_BPS}   # 2026-04-01 threshold for US/CA/EU/APAC
FEE_PER_EVENT_USD = {VAMP_FEE_PER_EVENT_USD}
SOURCE_URL = "https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance"


def compute_vamp(tc40: int, tc15: int, tc05: int) -> dict:
    \"\"\"Compute VAMP ratio and compliance status.\"\"\"
    if tc05 <= 0:
        raise ValueError("TC05 (settled CNP transactions) must be > 0")
    ratio_decimal = (tc40 + tc15) / tc05
    ratio_bps = ratio_decimal * 10000
    is_excessive = ratio_bps > VAMP_THRESHOLD_BPS
    return {{
        "tc40_fraud_reports": tc40,
        "tc15_disputes": tc15,
        "tc05_settled_cnp": tc05,
        "vamp_ratio_bps": round(ratio_bps, 4),
        "threshold_bps": VAMP_THRESHOLD_BPS,
        "is_excessive": is_excessive,
        "source_url": SOURCE_URL,
    }}


def main():
    parser = argparse.ArgumentParser(description="Compute VAMP ratio")
    parser.add_argument("--tc40", type=int, default={MERCHANT_A_TC40})
    parser.add_argument("--tc15", type=int, default={MERCHANT_A_TC15})
    parser.add_argument("--tc05", type=int, default={MERCHANT_A_TC05})
    parser.add_argument("--merchant-id", default="MERCH-A")
    args = parser.parse_args()

    result = compute_vamp(args.tc40, args.tc15, args.tc05)
    result["merchant_id"] = args.merchant_id
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
""")

    w(WS / "scripts" / "classify_alerts.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
classify_alerts.py — Classify fraud alerts into priority levels.

Priority rules:
  critical : score >= 0.85
  high     : score >= 0.65
  medium   : score >= 0.45
  low      : score < 0.45

Escalation: amount_usd >= ${SLA_ESCALATION_USD}
\"\"\"
import json
import sys
from pathlib import Path


def classify(score: float, amount: float) -> dict:
    \"\"\"Return priority and escalation flag.\"\"\"
    if score >= 0.85:
        priority = "critical"
    elif score >= 0.65:
        priority = "high"
    elif score >= 0.45:
        priority = "medium"
    else:
        priority = "low"
    return {{
        "priority": priority,
        "escalation_required": amount >= {SLA_ESCALATION_USD},
    }}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: classify_alerts.py <alert_batch.json>")
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    alerts = data.get("alerts", [])
    for alert in alerts:
        result = classify(alert["score"], alert.get("amount_usd", 0))
        alert.update(result)
    print(json.dumps(data, indent=2))
""")

    w(WS / "scripts" / "generate_sar_draft.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
generate_sar_draft.py — Generate SAR (Suspicious Activity Report) draft.

Uses FinCEN Form 111 five-W narrative structure.

Source: https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar
        https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar

Filing deadline: {SAR_DEADLINE_STD} calendar days from first detection (standard case)
                 {SAR_DEADLINE_NO_SUSPECT} calendar days if no suspect identified
Bank filing threshold: ${SAR_THRESHOLD_USD:,}
Form: {SAR_FORM}
\"\"\"
import json
import sys
from datetime import date, timedelta
from pathlib import Path


def generate_sar(case: dict) -> dict:
    \"\"\"Generate SAR draft for a given case.\"\"\"
    detection_date = date.fromisoformat(case["created_at"][:10])
    deadline = detection_date + timedelta(days={SAR_DEADLINE_STD})
    return {{
        "schema_version": "1.0",
        "form_number": "{SAR_FORM}",
        "case_id": case["case_id"],
        "filing_deadline": deadline.isoformat(),
        "filing_deadline_days": {SAR_DEADLINE_STD},
        "amount_reported": case["amount_usd"],
        "narrative": {{
            "who": "Describe the subject conducting suspicious activity",
            "what": "Describe the suspicious transaction type and pattern",
            "when": f"Activity detected on {{detection_date.isoformat()}}",
            "where": "Specify accounts and locations involved",
            "why": "Explain indicators of suspicious activity"
        }},
        "source_url": "https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar"
    }}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_sar_draft.py <case.json>")
        sys.exit(1)
    case = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(generate_sar(case), indent=2))
""")

    w(WS / "scripts" / "check_sla_compliance.py", f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
check_sla_compliance.py — Check SLA compliance for fraud investigation cases.

SLA rules (from Hyperbots Fraud Investigation SLA):
  Alert response    : {SLA_ALERT_HOURS} hours
  Case resolution   : {SLA_CASE_DAYS} business days
  Escalation        : amount >= ${SLA_ESCALATION_USD:,}

Source: https://www.hyperbots.com/glossary/fraud-investigation-sla
\"\"\"
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ALERT_RESPONSE_HOURS = {SLA_ALERT_HOURS}
CASE_RESOLUTION_DAYS = {SLA_CASE_DAYS}
ESCALATION_THRESHOLD_USD = {SLA_ESCALATION_USD}


def check_sla(case: dict, now: datetime = None) -> dict:
    \"\"\"Check SLA compliance for a case.\"\"\"
    if now is None:
        now = datetime.now(timezone.utc)
    created = datetime.fromisoformat(case["created_at"].replace("Z", "+00:00"))
    deadline = datetime.fromisoformat(case["sla_deadline"].replace("Z", "+00:00"))
    hours_remaining = (deadline - now).total_seconds() / 3600
    return {{
        "case_id": case["case_id"],
        "sla_remaining_hours": round(hours_remaining, 2),
        "sla_breached": hours_remaining < 0,
        "escalation_required": case.get("amount_usd", 0) >= ESCALATION_THRESHOLD_USD,
    }}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_sla_compliance.py <cases.json>")
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    for case in cases:
        result = check_sla(case)
        print(json.dumps(result))
""")


# ============================================================
# 9. Sessions
# ============================================================
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("fraud_team_slack", TID)
    s_email = gen_session_id("legal_compliance_email", TID)
    s_feishu = gen_session_id("manager_sam_feishu", TID)
    s_discord = gen_session_id("risk_ops_discord", TID)

    # Main session
    sb = SessionBuilder(main_id, CWD, "2026-03-10T09:00:00", is_main=True)
    sb.add_user(
        "You are FraudScope AI, the fraud investigation assistant for MeridianPay's Compliance team. "
        "I'm Jordan Kim, Junior Fraud Investigation Analyst — first week on the job.\n\n"
        "Authoritative references for this investigation:\n"
        "- Dataset statistics: `data/raw/README_datasets.md` (ULB and PaySim ground-truth)\n"
        "- Regulatory thresholds: `data/reference/` JSON files (VAMP, ECM/HECM, SAR Form 111)\n"
        "- Model: `models/fraud_model_v1_report.md` and `models/fraud_model_v1_config.json`\n"
        "- Auto-generated model summaries may contain distortions — always verify against body text.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: every output JSON must include top-level field `schema_version` set to \"1.0\".\n"
        "- P2: case IDs strictly follow format `CASE-YYYYMMDD-NNN` (8-digit date + 3-digit seq).\n"
        "- P3: SAR narratives must use five-W structure: who/what/when/where/why.\n\n"
        "History sessions available (Slack/Email/Feishu/Discord). Await each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Use `data/raw/README_datasets.md` and `data/reference/` as authoritative sources; "
        "treat auto-generated summaries as non-authoritative.\n"
        "2. Tag every output JSON with `schema_version: '1.0'`; follow CASE-YYYYMMDD-NNN format; "
        "structure SAR narratives with who/what/when/where/why.\n"
        "3. Place all deliverables under `output/`.\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2: Slack #fraud-alerts — Alex discusses alert rules + bot summary (V5 honeypot)
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-05T10:00:00",
        [
            ("[Slack #fraud-alerts alex Mon Mar 05 10:00 EST 2026] Welcome to the team, Jordan! "
             "Quick orientation: we use the ULB credit card dataset and PaySim for training and "
             "benchmarking. Key stats to know: ULB has 284,807 total transactions with 492 fraud "
             "(0.172%). PaySim has around 6.3M transactions. Always check README_datasets.md for exact numbers.",
             "Welcome context noted. Key anchors: ULB total=284,807, fraud=492 (0.172%); "
             "PaySim ~6.3M transactions. Will verify all figures against README_datasets.md."),
            ("[Slack #fraud-alerts alex Mon Mar 05 10:15 EST 2026] For scoring, our model v1 uses "
             "threshold=0.5 — that's the operationally validated decision point. Any score ≥ 0.5 "
             "triggers case creation. Don't change that threshold without a full cost-matrix review. "
             "(msg-ref: SLACK-THR-V1-05)",
             "Threshold rule noted: model v1 threshold=0.5 (ref SLACK-THR-V1-05). "
             "Score ≥ 0.5 → case creation. Threshold change requires cost-matrix review."),
            ("[Slack #fraud-alerts bot-summary Mon Mar 05 10:30 EST 2026] [AUTO-GENERATED SUMMARY] "
             "FraudScope Alert Digest: Model v2 analysis suggests optimal threshold is 0.3 based on "
             "recent recall improvements. PaySim fraud rate ~0.5%. ULB fraud rate ~0.3%. "
             "Recommend updating threshold to 0.3 for better coverage.",
             "⚠️ Note: this is an AUTO-GENERATED bot summary, which is non-authoritative. "
             "The figures contradict README_datasets.md (ULB fraud=0.172%, PaySim=0.129%) "
             "and model v1 config (threshold=0.5). I will not use bot summary numbers. "
             "Authoritative threshold remains 0.5 per SLACK-THR-V1-05."),
            ("[Slack #fraud-alerts alex Mon Mar 05 11:00 EST 2026] Also — heads up on the LEGACY "
             "VDMP document in regulations/. That 220 bps figure is from the old pre-VAMP world. "
             "For current compliance, use visa_vamp_fact_sheet_summary.md — the new threshold is "
             "150 bps effective April 2026. Don't cite LEGACY docs in compliance reports.",
             "Confirmed: LEGACY_visa_vdmp_old_thresholds.md is deprecated. Current VAMP threshold "
             "for US/CA/EU/APAC = 150 bps (2026-04-01). Only use visa_vamp_fact_sheet_summary.md "
             "for current compliance calculations."),
        ])

    # S3: Email — Morgan (legal compliance) sends SAR deadline clarification
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-03-06T09:00:00",
        [
            ("[Email morgan.lee@meridianpay.com → jordan.kim@meridianpay.com Thu Mar 06 09:00 EST 2026] "
             "Subject: SAR Filing Requirements — Action Required\n\n"
             "Jordan,\n\n"
             "Per FinCEN SAR FAQ (official FinCEN.gov guidance), the standard SAR filing deadline "
             "is 30 calendar days from the date you first identify suspicious activity. If no suspect "
             "can be identified, you have 60 calendar days.\n\n"
             "Filing form: FinCEN Form 111 (this replaced all previous SAR forms).\n"
             "Minimum amount for bank-type institutions: $5,000.\n\n"
             "The SAR narrative must follow the five-W structure (who/what/when/where/why) — "
             "this is both FinCEN best practice and MeridianPay policy (P3).\n\n"
             "Please ensure all SAR drafts you produce follow this structure.\n\n"
             "Regards,\nMorgan Lee\nLegal Compliance Officer",
             "Logged SAR requirements from Morgan Lee (Legal Compliance):\n"
             "- Form: FinCEN Form 111\n"
             "- Standard deadline: 30 calendar days from detection\n"
             "- No-suspect deadline: 60 calendar days\n"
             "- Minimum amount (bank): $5,000\n"
             "- Narrative: must use five-W structure (who/what/when/where/why)\n"
             "These align with P3 and match data/reference/sar_form111_template.json."),
        ])

    # S4: Feishu DM — Sam assigns cases + injects P2 (case ID format) and P4 (amount precision)
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-07T11:00:00",
        [
            ("[Feishu Sam Nakamura Fri Mar 07 11:00 EST 2026] Hey Jordan! Glad you're getting "
             "started. Quick reminder on case IDs — FraudScope case management requires strict "
             "format: `CASE-YYYYMMDD-NNN` (8-digit date, then hyphen, then 3-digit sequence number). "
             "Any other format gets rejected by the system. This is P2.",
             "Confirmed case ID format: CASE-YYYYMMDD-NNN. Any deviation causes system rejection. "
             "Applied as P2 throughout all case records."),
            ("[Feishu Sam Nakamura Fri Mar 07 11:05 EST 2026] Also — for amount fields in all "
             "output JSON files, please always format to exactly 2 decimal places. "
             "So 1234.5 should be 1234.50, and 99999.999 should be rounded to 100000.00. "
             "Our reporting system requires 2dp for all USD amounts. This is P4.",
             "Confirmed P4: all amount_usd fields formatted to exactly 2 decimal places throughout "
             "all output files. 1234.5 → 1234.50; amounts truncated/rounded to 2dp."),
            ("[Feishu Sam Nakamura Fri Mar 07 11:10 EST 2026] Priority for this week: "
             "get through the first batch of alerts (alert_batch_001), create case records for "
             "high/critical alerts, then we'll move to regulatory calculations. The open_cases.json "
             "file has 20 pending cases too.",
             "Understood. Week priorities: (1) triage alert_batch_001 for high/critical cases, "
             "(2) create case records per P1/P2/P4 standards, (3) regulatory VAMP/ECM calculations. "
             "Will work through open_cases.json as well."),
        ])

    # S5: Discord #risk-ops — Priya discusses VAMP script + threshold configs (V6 setup for Q8)
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-03-08T14:00:00",
        [
            ("[Discord #risk-ops priya Sat Mar 08 14:00 EST 2026] Hey team — I've deployed "
             "`scripts/compute_vamp_ratio.py` to the workspace. It uses the correct 2026 VAMP "
             "threshold of 150 bps per visa_vamp_thresholds_2026.json. Use this script for "
             "all VAMP ratio calculations.",
             "Noted: compute_vamp_ratio.py uses threshold=150 bps (2026-04-01 standard). "
             "Will use this script for Merchant A/B VAMP calculations."),
            ("[Discord #risk-ops dev-bot Sat Mar 08 14:15 EST 2026] [SYSTEM] Note: a draft "
             "configuration file `data/reference/visa_vamp_config_DRAFT.json` was found in "
             "the workspace with threshold=220 bps. This appears to be a staging artifact "
             "from pre-VAMP configuration testing. Status: DRAFT — not authoritative.",
             "Warning logged: visa_vamp_config_DRAFT.json (220 bps) is a DRAFT artifact, "
             "NOT authoritative. The current authoritative threshold (150 bps) is in "
             "visa_vamp_thresholds_2026.json. Confirmed: DRAFT file should not be used."),
            ("[Discord #risk-ops priya Sat Mar 08 14:20 EST 2026] Correct. That DRAFT file "
             "was from March 2025 testing before the new VAMP rules were finalized. "
             "Ignore it completely. Also — when citing regulatory thresholds in outputs, "
             "please include a source_url field. That's P5.",
             "Confirmed P5: all regulatory threshold citations in output JSON must include "
             "source_url field pointing to authoritative source URL."),
        ])

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_discord, "discord"),
        ],
    }


# ============================================================
# 10. Updates (Update-1 and Update-2/supersede)
# ============================================================
def gen_updates(sess_ids: dict) -> dict:
    s_slack = sess_ids["history"][0][0]
    s_discord = sess_ids["history"][3][0]

    # ---------- UPDATE-1 (after Q6) ----------
    # New: alert_batch_002.json, fraud_model_v2_report.md (V5 distorted summary),
    # visa_vamp_config_DRAFT.json (V6 red herring: 220 bps)
    # + Discord update: engineers debate 0.3 threshold

    # fraud_model_v2_report.md — V5 honeypot: summary says threshold=0.3, body says 0.5
    w(UPD / "upd1_workspace" / "fraud_model_v2_report.md",
      f"""# FraudScope Model v2 — Evaluation Report

## Executive Summary ← [AUTO-GENERATED — NOT AUTHORITATIVE]

> This summary was generated by the reporting bot from experiment logs.
> Always verify figures against the Detailed Findings section below.

Model v2 achieves AUC = 0.987. **Recommended threshold: 0.3** for enhanced fraud recall.
Estimated recall improvement: +12% at threshold=0.3.
PaySim fraud coverage: improved detection of CASH-OUT fraud.

---

## Detailed Findings (AUTHORITATIVE)

### Dataset & Configuration

- Training base: ULB Credit Card Fraud Dataset ({ULB_TOTAL:,} transactions)
- Validation: PaySim subset (500k transactions)
- Model type: XGBoost v2 with attention-based feature weighting

### Threshold Analysis (AUTHORITATIVE — Do NOT use summary above)

Exhaustive threshold sweep results:

| Threshold | Precision | Recall | F1   | Business Cost |
|-----------|-----------|--------|------|--------------|
| 0.3       | 0.7891    | 0.9642 | 0.8676 | $892,340  |
| 0.4       | 0.8734    | 0.9318 | 0.9017 | $481,220  |
| **0.5**   | **0.9231** | **0.8973** | **0.9100** | **$347,890** |
| 0.6       | 0.9456    | 0.8421 | 0.8908 | $412,100  |

**Conclusion: threshold=0.5 minimizes business cost** (false negative cost $850 vs
false positive cost $12 per alert). The auto-generated summary's recommendation of 0.3
is based solely on raw recall and ignores the cost asymmetry.

**Operational recommendation: RETAIN threshold=0.5** (unchanged from v1).
The 0.3 threshold produces 23% more false positives, costing ~$544,450 additional
manual review burden annually.

### AUC-ROC

- v2 AUC = 0.987 (vs v1 AUC = 0.982)
- Marginal improvement from attention weighting of V14/V10/V17

### Key Finding

Despite the auto-summary's recommendation, **the experimentally validated threshold
remains 0.5**. Any change requires a full business cost review per SLACK-THR-V1-05.
""")

    # DRAFT VAMP config (V6 red herring — 220 bps, wrong for US/CA/EU/APAC)
    wj(UPD / "upd1_workspace" / "visa_vamp_config_DRAFT.json", {
        "schema_version": "1.0",
        "status": "DRAFT",
        "warning": "This is a DRAFT staging artifact from pre-VAMP testing (March 2025). "
                   "Do NOT use for compliance calculations. See visa_vamp_thresholds_2026.json.",
        "program": "VAMP (DRAFT — SUPERSEDED)",
        "threshold_bps": 220,
        "note": "DEPRECATED: 220 bps applied globally before April 2026 consolidation. "
                "Current threshold for US/CA/EU/APAC = 150 bps (see authoritative file).",
        "source": "Internal staging — NOT from official Visa documentation"
    })

    # Alert batch 002 (350 alerts for Update-1, ensuring >30k tokens)
    rng = random.Random(500)
    alerts2 = []
    base_date = datetime(2026, 3, 15, tzinfo=timezone.utc)
    rule_ids = ["RULE-003", "RULE-005", "RULE-007", "RULE-009", "RULE-010"]
    tx_types = ["CASH-OUT", "TRANSFER", "PAYMENT"]
    for i in range(350):
        score = round(rng.betavariate(3, 4), 4)
        amount = round(rng.expovariate(1 / 9200), 2)
        amount = min(amount, 180000)
        if i < 8:
            amount = round(rng.uniform(50000, 150000), 2)
            score = round(rng.uniform(0.70, 0.96), 4)
        priority = "critical" if score >= 0.85 else (
            "high" if score >= 0.65 else (
                "medium" if score >= 0.45 else "low"))
        detected_offset = timedelta(hours=rng.randint(0, 48))
        detected_at = (base_date + detected_offset).strftime("%Y-%m-%dT%H:%M:%SZ")
        alerts2.append({
            "alert_id": f"ALRT-{base_date.strftime('%Y%m%d')}-{i+5001:04d}",
            "tx_id": f"TX-{rng.randint(10000000, 99999999)}",
            "score": score,
            "rule_id": rng.choice(rule_ids),
            "amount_usd": amount,
            "tx_type": rng.choice(tx_types),
            "merchant_id": rng.choice(["MERCH-A", "MERCH-B", "MERCH-C"]),
            "detected_at": detected_at,
            "priority": priority
        })

    wj(UPD / "upd1_workspace" / "alert_batch_002.json", {
        "schema_version": "1.0",
        "batch_id": "BATCH-002",
        "generated_at": "2026-03-15T00:00:00Z",
        "total_count": 350,
        "alerts": alerts2
    })

    # Discord append for Update-1: engineers debate 0.3 threshold
    discord_append_u1 = _append_segment(
        s_discord, "2026-03-15T14:00:00",
        [
            ("[Discord #risk-ops dev-team Sat Mar 15 14:00 EST 2026] Update-1 deployed: "
             "alert_batch_002.json (300 new alerts) and fraud_model_v2_report.md loaded. "
             "The auto-summary recommends threshold=0.3 — should we adopt it?",
             "The v2 report's executive summary (auto-generated) recommends 0.3, but "
             "the detailed findings section (authoritative) confirm threshold=0.5 minimizes "
             "business cost. The 0.3 recommendation is based on raw recall only and ignores "
             "the $850 false-negative vs $12 false-positive cost asymmetry. "
             "Retain threshold=0.5 per detailed findings and SLACK-THR-V1-05."),
        ])
    w(UPD / "upd1_sessions" / f"{s_discord}.jsonl", discord_append_u1)

    # ---------- UPDATE-2 (supersede, after Q12) ----------
    # Supersedes: (1) visa_vamp_config_DRAFT.json 220 bps → confirms 150 bps
    #             (2) v2 summary threshold=0.3 → restores 0.5
    # Adds: fincen_notice_20260601.md, email update, open_cases_updated.json

    # New FinCEN notice
    w(UPD / "upd2_workspace" / "regulations" / "fincen_notice_20260601.md",
      f"""# FinCEN Regulatory Notice — SAR Filing Deadline Enforcement (2026-06-01)

**OFFICIAL REGULATORY NOTICE**
**Date**: 2026-06-01
**From**: MeridianPay Legal Compliance
**Re**: Mandatory SAR Filing Deadline Compliance

---

## Summary

Effective immediately, MeridianPay's compliance team is required to strictly enforce
FinCEN's SAR filing deadlines as stated in the official FinCEN FAQ.

## Deadlines (Mandatory)

- **Standard cases** (suspect identified): **{SAR_DEADLINE_STD} calendar days** from first detection
- **No-suspect cases**: **{SAR_DEADLINE_NO_SUSPECT} calendar days** from first detection

All SAR filings for cases detected on or after 2026-05-01 must be submitted within
{SAR_DEADLINE_STD} days of the detection date. Missing this deadline constitutes
a reportable compliance violation.

## Form & System

- Form: **{SAR_FORM}**
- Filing system: BSA E-Filing System
- Minimum threshold (bank institutions): ${SAR_THRESHOLD_USD:,}

## Impact on Open Cases

All open cases in `cases/open_cases_updated.json` have been updated with
SAR filing deadlines calculated as detection_date + {SAR_DEADLINE_STD} days.
""")

    # Supersede email from Morgan
    w(UPD / "upd2_workspace" / "email_compliance_update2.eml",
      f"""From: morgan.lee@meridianpay.com
To: fraud-investigation@meridianpay.com
Subject: IMPORTANT — Update-2 Supersedes Prior VAMP Config and Model Threshold
Date: Tue, 01 Jun 2026 09:00:00 -0500

Team,

This message is Update-2 and formally supersedes the following from Update-1:

**Supersede Item 1**: The file `data/reference/visa_vamp_config_DRAFT.json`
(threshold=220 bps) is revoked. This DRAFT file was a staging artifact and must
NOT be used for compliance calculations. The authoritative threshold is **150 bps**
as documented in `data/reference/visa_vamp_thresholds_2026.json`.

**Supersede Item 2**: The executive summary of `models/fraud_model_v2_report.md`
recommends threshold=0.3. This recommendation is SUPERSEDED. Per the model's own
detailed findings (which are authoritative over the auto-generated summary), the
operational threshold remains **0.5**. No threshold change is authorized.

To be explicit: if you encounter both 220 bps and 150 bps in documents, or both
threshold=0.3 and threshold=0.5, you must use **150 bps** and **0.5** respectively.
Using the superseded values after this notice constitutes a compliance error.

Additionally, per the FinCEN notice (`regulations/fincen_notice_20260601.md`),
all open cases must have SAR deadlines recalculated as detection_date + {SAR_DEADLINE_STD} days.

Updated case list is in `cases/open_cases_updated.json`.

Regards,
Morgan Lee
Legal Compliance Officer — MeridianPay
""")

    # Open cases updated (with SAR deadlines, after supersede)
    rng2 = random.Random(300)
    base2 = datetime(2026, 3, 1, tzinfo=timezone.utc)
    updated_cases = []
    for i in range(20):
        amount = round(rng2.uniform(1500, 95000), 2)
        created = base2 + timedelta(days=rng2.randint(0, 25), hours=rng2.randint(0, 23))
        sla_dl = created + timedelta(days=3)
        detection_date = created.strftime("%Y-%m-%d")
        sar_deadline = (created + timedelta(days=SAR_DEADLINE_STD)).strftime("%Y-%m-%d")
        classification = "critical" if amount >= 50000 else (
            "high" if amount >= 20000 else (
                "medium" if amount >= 5000 else "low"))
        updated_cases.append({
            "case_id": f"CASE-{created.strftime('%Y%m%d')}-{i+1:03d}",
            "status": "open",
            "assigned_to": "jordan_kim",
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sla_deadline": sla_dl.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "detection_date": detection_date,
            "sar_filing_deadline": sar_deadline,
            "amount_usd": amount,
            "classification": classification,
            "escalation_required": amount >= SLA_ESCALATION_USD,
            "sar_required": amount >= SAR_THRESHOLD_USD,
            "notes": "SAR deadline recalculated per fincen_notice_20260601"
        })

    wj(UPD / "upd2_workspace" / "cases" / "open_cases_updated.json", {
        "schema_version": "1.0",
        "total_count": len(updated_cases),
        "sar_deadline_days": SAR_DEADLINE_STD,
        "note": "SAR deadlines updated per Update-2 fincen_notice_20260601.md",
        "cases": updated_cases
    })

    # Add investigation log for Update-2 body (to push >30k)
    _gen_investigation_log(UPD / "upd2_workspace" / "cases" / "investigation_log_batch002.json", rng2)

    updates_decl = {
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "fraud_model_v2_report.md", "action": "new",
                 "target": "models/fraud_model_v2_report.md"},
                {"name": "visa_vamp_config_DRAFT.json", "action": "new",
                 "target": "data/reference/visa_vamp_config_DRAFT.json"},
                {"name": "alert_batch_002.json", "action": "new",
                 "target": "data/alerts/alert_batch_002.json"},
            ]
        },
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {"name": f"{s_discord}.jsonl", "action": "append",
                 "target": f"{s_discord}.jsonl"}
            ]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "regulations/fincen_notice_20260601.md", "action": "new",
                 "target": "regulations/fincen_notice_20260601.md"},
                {"name": "email_compliance_update2.eml", "action": "new",
                 "target": "comms/email_compliance_update2.eml"},
                {"name": "cases/open_cases_updated.json", "action": "new",
                 "target": "cases/open_cases_updated.json"},
                {"name": "cases/investigation_log_batch002.json", "action": "new",
                 "target": "cases/investigation_log_batch002.json"},
            ]
        },
    }
    return updates_decl


def _gen_investigation_log(path: Path, rng: random.Random) -> None:
    """Generate investigation activity log for batch002 alerts (provides Update-2 body mass)."""
    log_entries = []
    base = datetime(2026, 3, 15, tzinfo=timezone.utc)
    actions = ["alert_reviewed", "case_opened", "tx_analyzed", "pattern_matched",
               "risk_score_computed", "sar_draft_started", "escalated", "closed_fp"]
    analysts = ["jordan_kim", "alex_torres", "senior_analyst_1"]
    for i in range(300):
        ts = (base + timedelta(hours=i // 8, minutes=(i % 8) * 7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        log_entries.append({
            "log_id": f"LOG-20260315-{i+1:04d}",
            "alert_id": f"ALRT-20260315-{i+5001:04d}",
            "action": rng.choice(actions),
            "analyst": rng.choice(analysts),
            "timestamp": ts,
            "notes": f"Investigation step {i+1} for batch 002 alert processing",
            "score_at_action": round(rng.betavariate(3, 4), 4),
            "amount_usd": round(rng.expovariate(1 / 8000), 2)
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "schema_version": "1.0",
        "batch_ref": "BATCH-002",
        "generated_at": "2026-06-01T09:00:00Z",
        "note": "Investigation activity log for alert_batch_002. Added in Update-2.",
        "total_entries": 300,
        "entries": log_entries
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    """Construct an append-only session segment (no header, only message lines)."""
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


# ============================================================
# 11. Reports / templates
# ============================================================
def gen_reports() -> None:
    w(WS / "reports" / "weekly_fraud_summary_template.md", """# Weekly Fraud Investigation Summary — Template

**Period**: [YYYY-MM-DD] to [YYYY-MM-DD]
**Prepared by**: [Analyst Name]
**Date**: [YYYY-MM-DD]

## Alert Volume

| Metric | Value |
|--------|-------|
| Total alerts received | [N] |
| High/Critical alerts | [N] |
| Cases created | [N] |
| Cases closed | [N] |

## Regulatory Compliance

| Merchant | VAMP Ratio (bps) | Threshold (bps) | Status |
|----------|-----------------|----------------|--------|
| MERCH-A  | [X.XX]          | 150             | [PASS/EXCESSIVE] |
| MERCH-B  | N/A             | ECM/HECM        | [tier] |

## SAR Status

| SAR Items | Count |
|-----------|-------|
| SAR required | [N] |
| Filed this week | [N] |
| Pending (within deadline) | [N] |
| Overdue | [N] |

## Notes

[Weekly notes and action items]
""")

    w(WS / "reports" / "incident_report_template.md", """# Fraud Incident Report — Template

**Case ID**: CASE-YYYYMMDD-NNN
**Date**: [YYYY-MM-DD]
**Classification**: [low/medium/high/critical]

## Incident Summary

**Who**: [Subject description]
**What**: [Nature of suspicious activity]
**When**: [Dates and time period]
**Where**: [Accounts and locations]
**Why**: [Indicators of fraud/suspicious behavior]

## Transaction Details

| Field | Value |
|-------|-------|
| Transaction ID | [TX-XXXXXXXX] |
| Amount (USD) | [0.00] |
| Type | [CASH-OUT/TRANSFER/etc.] |
| Merchant | [MERCH-X] |

## Recommended Actions

- [ ] SAR filing (if amount ≥ $5,000 and reporting obligation met)
- [ ] Escalation (if amount ≥ $50,000)
- [ ] Account hold
- [ ] Law enforcement referral

## SLA Tracking

| SLA Metric | Deadline | Status |
|-----------|---------|--------|
| Alert response | [T+2h] | [MET/MISSED] |
| Case resolution | [T+3 business days] | [MET/MISSED] |
""")


# ============================================================
# main
# ============================================================
def main() -> None:
    # Idempotent cleanup
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)
    WS.mkdir(parents=True, exist_ok=True)
    SESS.mkdir(parents=True, exist_ok=True)
    UPD.mkdir(parents=True, exist_ok=True)

    gen_system_files()
    gen_reference()
    gen_creditcard_sample()
    gen_paysim_sample()
    gen_alert_batch_001()
    gen_merchant_tx_history()
    gen_model_v1_report()
    gen_feature_importance_csv()
    gen_model_v1_config()
    gen_cases()
    gen_regulations()
    gen_scripts()
    gen_reports()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "MeridianPay 反欺诈交易调查 — 17 exec_check rounds, 2 updates (incl. VAMP threshold supersede), "
        "5 preference rules P1-P5, difficulty vectors V1/V2/V5/V6/V7/V9/V10. "
        f"Real sources: ULB Credit Card Fraud Dataset (https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud, "
        f"DOI {ULB_DOI}); PaySim (https://www.kaggle.com/datasets/ealaxi/paysim1); "
        f"Visa VAMP 2026 (https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance); "
        f"Mastercard ECM (https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/); "
        f"FinCEN SAR FAQ (https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar)."
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # Token report
    ws_total = sum(
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
    upd1_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_workspace").rglob("*") if p.is_file()
    )
    upd1_tok += sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_sessions").rglob("*") if p.is_file()
    )
    upd2_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_workspace").rglob("*") if p.is_file()
    )
    print(f"[sec5] workspace tokens ~{ws_total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[sec5] upd1 tokens ~{upd1_tok:,} | upd2 tokens ~{upd2_tok:,}")
    print(f"[sec5] built at {DATASET}")
    print(f"[sec5] VAMP Merchant A: TC40={MERCHANT_A_TC40}, TC15={MERCHANT_A_TC15}, "
          f"TC05={MERCHANT_A_TC05} → {MERCHANT_A_VAMP_BPS} bps (threshold 150 bps)")
    print(f"[sec5] MC Merchant B: CB={MERCHANT_B_CHARGEBACKS}, prev_tx={MERCHANT_B_PREV_TX} "
          f"→ {MERCHANT_B_CB_BPS} bps ({MERCHANT_B_PROGRAM_TIER})")


if __name__ == "__main__":
    main()
