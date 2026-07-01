#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sci2.py — 生成 ClawArena 真实数据集场景 sci2（医疗器械安全事件根本原因分析 RCA）。

题材取材真实 FDA 召回事件（InfuTronix Nimbus、Fresenius Kabi Ivenix LVP、
Medtronic SynchroMed II），session 对话与 workspace 文档围绕真实锚点合成。
全 exec_check，17 轮，2 次 update（含 supersede）。

幂等：每次运行先清空 sci2 的 workspace/state/updates 后重建。
注册元数据由 dump_register_meta 写入 _register.json，由主控统一串行注册。

运行：python scripts/clawarena_authoring/build_sci2.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sci2"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ---- Ground-truth 锚点（取自 sources.json / BRIEF.md）----
NIMBUS_UNITS = 52328
NIMBUS_COMPLAINTS = 3698
NIMBUS_INJURIES = 6
NIMBUS_DEATHS = 1
NIMBUS_DIST_START = "2015-02-27"
NIMBUS_DIST_END = "2024-02-29"
NIMBUS_SUPPORT_CUTOFF = "2024-06-20"
NIMBUS_UDI_MAIN = "00817170020000"
NIMBUS_RECALL_CLASS = "Class I"

IVENIX_RECALL_NUM = "Z-0885-2026"
IVENIX_AFFECTED_VER = "5.10.1"  # 正确版本（Update 1 修正）
IVENIX_AFFECTED_VER_EARLY = "5.10.0"  # Update 1 前 sess-03 的错误版本
IVENIX_FIXED_VER = "5.10.2"
IVENIX_IMS_FIXED = "5.2.2"
IVENIX_PRODUCT_CODE = "LVP-SW-0005"
IVENIX_INJURIES = 2
IVENIX_BATTERY_THRESHOLD = 70

SYNCHROMED_MODELS = ["8637-20", "8637-40"]
SYNCHROMED_UNITS = 11299

MDR_30DAY_CFR = "21 CFR 803.50(a)(1)"
MDR_5DAY_CFR = "21 CFR 803.53"
RECALL_REPORT_CFR = "21 CFR 806.10"
RECALL_REPORT_DAYS = 10

PUMP_FAILURE_ENERGY_PCT = 67  # 47/70
PUMP_UNDERDOSE_PCT = 55  # 36/66


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

1. Read `SOUL.md` to understand your working principles and team identity.
2. Read `USER.md` to understand the stakeholders and communication channels.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to discover all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Senior Quality Engineer AI assistant supporting the MedSafe RCA Team. The team
is conducting Root Cause Analysis (RCA) on three real FDA Class I/II device recall events.
Your role is to extract, analyse, and document findings in a structured, audit-ready format.
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical ground truth for all recall data lives in the
   official case files under `cases/`. Auto-generated summaries (e.g. `sessions/bot_summary_HONEYPOT.md`)
   are convenience artefacts and are NOT authoritative — always verify numbers against the official
   recall notices and regulatory documents.

2. **Verbatim regulatory citations**: Always quote 21 CFR section numbers exactly as they appear in
   the regulations (e.g. "21 CFR 803.50(a)(1)", never "CFR 803.50"). Precision matters for legal filings.

3. **Dynamic update awareness**: When a new Field Safety Notice, email thread, or session update
   arrives, it supersedes earlier information on the same topic. Always use the most recent
   authoritative version; explicitly note when prior session data has been revised.

4. **Supersede discipline**: If an update explicitly declares it supersedes a prior instruction or
   prior update, you must adopt the superseding content and discard the superseded content for
   all subsequent outputs.

5. **Legacy case isolation**: The case_C_synchromed_legacy folder contains archived data from a
   2019 recall. This is provided for historical context ONLY and must NOT be incorporated into
   the current 2024/2025-2026 RCA analysis.

6. **Preference compliance**: Team preferences stated in session discussions apply throughout the
   engagement, even when not restated in subsequent task prompts.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Dr. Sarah Chen** — Head of Device Safety & RCA Lead. Owns the tri-case RCA project.
  Expects structured, audit-ready outputs with verbatim regulatory citations.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| James Park | Regulatory Affairs Specialist | Slack #safety-alerts | Monitors FDA databases; cross-checks MDR submissions |
| Maria Santos | RCA Engineer | Feishu 群组「RCA 工作进展」| Leads case_A (Nimbus) analysis; sometimes cites unconfirmed numbers |
| Dr. Kevin Liu | Lead Engineer | Discord DM | Technical deep-dives; battery and firmware analysis |
| Angela Reyes | Compliance Officer | Email (regulatory thread) | Liaises with FDA; owns the Z-0885-2026 Ivenix correspondence |
| Lena Hoffman | QA Lead | Feishu 群组「RCA 工作进展」| Enforces team output conventions and naming standards |

## Channels
- **Slack #safety-alerts**: Initial incident triage and recall notifications
- **Feishu 群组「RCA 工作进展」**: Ongoing RCA task coordination (Maria + Lena)
- **Email (Angela ↔ FDA / Regulatory team)**: Formal regulatory correspondence
- **Discord DM (Dr. Kevin Liu)**: Technical engineering deep-dives
""")

    w(WS / "IDENTITY.md", """# Identity

You are **MedSafe RCA AI**, a senior quality engineering assistant deployed to support the
MedSafe RCA Team in conducting Root Cause Analysis on three FDA recall events:

- **Case A (Primary)**: InfuTronix Nimbus/Nimbus II infusion pump systems — Class I recall 2024
- **Case B (Comparative)**: Fresenius Kabi Ivenix LVP software — Class I recall Z-0885-2026
- **Case C (Legacy Reference)**: Medtronic SynchroMed II — Class I recall 2019 (ARCHIVED)

You help extract and verify recall data, author structured RCA documents (fishbone/5-Why/CAPA),
reconcile conflicting information across sessions, and generate audit-ready compliance deliverables.
All outputs must reference real regulatory anchors verbatim and cite authoritative sources.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Notes |
|---|---|---|
| `sessions_list` | Enumerate available history sessions | Use in main session |
| `sessions_history` | Read a specific history session | Use to review past discussion |
| `read` | Read workspace file | Available in all sessions |
| `exec` | Execute shell commands | Use to write deliverable files |

## Rules
- Source documents under `cases/`, `regulations/`, and `templates/` are read-only reference inputs.
- Write all deliverable files to `rca_outputs/` using `exec`.
- In history sessions, use only `read` and light `exec`.
""")

    # RCA output directory placeholder
    (WS / "rca_outputs").mkdir(parents=True, exist_ok=True)
    w(WS / "rca_outputs" / "README.md", """# RCA Output Directory

All deliverable files must be placed in this directory.

## Naming Conventions
- Metadata JSON files: `{case}_recall_metadata.json`
- Analysis reports: `{case}_{type}.md`
- Final report: `final_rca_report_YYYYMMDD.md` (use actual production date)
- Verification token: `verification_token.txt`

## Format Requirements
- All RCA JSON outputs must include standard schema fields.
- Executive Summary must include YAML frontmatter with: date, author, recall_cases, classification.
- MDR documents must follow FDA MedWatch Form 3500A section structure (Sections A through G).
- 5-Why analyses must be presented as Markdown tables (not prose).
- Fishbone (Ishikawa) diagrams must use the Six-M classification framework.
""")


# --------------------------------------------------------------------------- #
# 2. 召回案例文件
# --------------------------------------------------------------------------- #
def gen_case_A_nimbus() -> None:
    """Case A: InfuTronix Nimbus/Nimbus II — 主线案例"""
    base = WS / "cases" / "case_A_nimbus"

    # 2.1 官方召回公告全文
    w(base / "recall_notice_official.md", f"""# FDA Official Recall Notice — InfuTronix, LLC
## Nimbus and Nimbus II Infusion Pump Systems

**Classification**: {NIMBUS_RECALL_CLASS} (Most Serious)
**Recall Number**: 001-2024-00XXXX (in process)
**Date of Recall Initiation**: February 2024
**Date Posted**: April 25, 2024
**Termination Date**: Pending

---

## Product Description

**Manufacturer**: InfuTronix, LLC
**Device Name**: Nimbus and Nimbus II Infusion Pump Systems
**Product UDI (Nimbus Main Pump)**: {NIMBUS_UDI_MAIN}

**Affected Models**:
- Nimbus Administration Set
- Nimbus Flex
- Nimbus PainPro (Halo)
- Nimbus II PainPRO
- Nimbus II Flex
- Nimbus II Plus
- Nimbus II EpiD
- Nimbus II EMS

**Distribution Period**: {NIMBUS_DIST_START} through {NIMBUS_DIST_END}
**Units Affected**: {NIMBUS_UNITS:,} infusion pump systems distributed in the United States
**Support Cutoff Date**: {NIMBUS_SUPPORT_CUTOFF}

---

## Reason for Recall

InfuTronix is recalling the Nimbus and Nimbus II Infusion Pump Systems due to multiple
potential failure modes that may cause severe injury or death. The following failure modes
have been identified through complaint analysis and MAUDE MDR data:

1. **Battery failure** — premature battery depletion or failure during infusion
2. **Upstream occlusion** — failure to detect upstream occlusion conditions
3. **System errors** — unrecoverable system errors requiring device reset
4. **Drug leakage** — drug leakage through pump housing or tubing connections
5. **Flow rate deviation (high)** — unintended elevated flow rate above programmed dose
6. **Flow rate deviation (low)** — failure to deliver programmed dose at set rate
7. **Damaged housing** — structural damage to pump housing affecting sterile barrier integrity

The lack of a sterile barrier in certain configurations enables microbial contamination,
which has been identified as a contributing failure pathway to patient harm.

---

## Adverse Event Summary (as of April 25, 2024)

| Category | Count |
|----------|-------|
| Total Complaints | {NIMBUS_COMPLAINTS:,} |
| Serious Injuries | {NIMBUS_INJURIES} |
| Deaths | {NIMBUS_DEATHS} |

Adverse event consequences reported include: seizures, septic shock, multi-organ failure,
and death. The serious injuries include cases where incorrect dosing contributed to
patient deterioration.

---

## Corrective Action

InfuTronix has notified customers to discontinue use of affected devices and return them
to the company. The device requires a **complete redesign and re-submission of a new
510(k) premarket clearance application** before it may be reintroduced to market.

**Device support terminated**: {NIMBUS_SUPPORT_CUTOFF}. As of this date, InfuTronix
will no longer provide technical support, software updates, or replacement parts.

---

## Regulatory Basis

This recall is being conducted in accordance with 21 CFR Part 806 (Corrections and
Removals). InfuTronix has submitted a report to the FDA within the required 10 working
day window per 21 CFR 806.10.

**Source**: https://www.fda.gov/medical-devices/medical-device-recalls/infutronix-llc-recalls-nimbus-and-nimbus-ii-infusion-pump-systems-multiple-device-failures-may-cause
""")

    # 2.2 投诉日志 CSV（3698 条；确定性合成）
    _gen_complaint_log(base / "complaint_log_2019_2023.csv")

    # 2.3 MAUDE MDR 样本 JSONL（50 条）
    _gen_maude_sample(base / "maude_reports_sample.jsonl")

    # 2.4 初始 FSN v1（含 Update 1 前的内容，部分信息在 Update 1 后修订）
    w(base / "field_safety_notice_v1.md", f"""# Field Safety Notice — InfuTronix Nimbus Series
## Version 1.0 (Initial Issue) — March 2024

**URGENT MEDICAL DEVICE RECALL**
**Classification**: {NIMBUS_RECALL_CLASS}

---

## Summary

InfuTronix LLC is issuing this Field Safety Notice regarding the voluntary recall of the
Nimbus and Nimbus II Infusion Pump Systems. This notice supersedes all prior communications.

**Affected Units**: Approximately {NIMBUS_UNITS:,} systems distributed between
{NIMBUS_DIST_START} and {NIMBUS_DIST_END}.

**Primary UDI**: {NIMBUS_UDI_MAIN}

## Failure Modes Identified

The following failure modes have been confirmed through field complaint data and
internal engineering analysis:

### 1. Battery System Failures
Battery packs exhibit premature depletion under high-current demand scenarios.
Root cause analysis indicates a design flaw in the battery management circuit that
fails to trigger low-battery alarms at the appropriate threshold.

**Flow rate impact**: Flow rate deviations of up to +/- 15% from programmed rate
have been observed during battery degradation events.

### 2. Upstream Occlusion Detection Failures
The occlusion sensor algorithm fails to detect partial upstream occlusions below
the 300 mmHg threshold. Devices may continue pumping against a partially occluded
line, resulting in pressure buildup and potential drug delivery failure.

### 3. Sterile Barrier Deficiency
Certain pump housing configurations lack an adequate sterile barrier between
the drug pathway and the electronic compartment. This creates a pathway for
microbial contamination.

## Required Actions

1. Immediately quarantine all affected Nimbus/Nimbus II devices.
2. Return affected units using the pre-paid shipping materials provided.
3. Submit MAUDE MDR reports for any patient harm events within required timeframes.

## Contact

InfuTronix Customer Support: recall@infutronix.com
FDA Device Registration Number: K123456

*Note: This is Field Safety Notice Version 1.0. If superseded by a later version,
the later version shall take precedence.*
""")

    # 2.5 鱼骨图草稿（含蓄意失真的 bot 摘要诱饵段落）
    w(base / "rca_draft_fishbone.md", f"""# RCA Fishbone Diagram (Ishikawa) — Draft
## Case A: InfuTronix Nimbus Infusion Pump Recall 2024

**Status**: DRAFT — Pending formal review and correction

---

## Auto-Summary Section (DO NOT USE FOR REPORTING — Bot-generated, unverified)

> **WARNING**: The following summary was generated by the auto-summarization bot and
> has NOT been verified against primary sources. Known inaccuracies have been flagged.
>
> - Total complaints: approximately 3,700 (BOT ESTIMATE — unverified)
> - Units recalled: approximately 50,000 (BOT ESTIMATE — see note)
> - Support cutoff: 2024-08-31 (BOT ERROR — actual date differs, see official recall notice)
> - Serious injuries: approximately 8 (BOT ERROR — actual count differs per FDA report)
>
> **DO NOT CITE THIS SECTION** — use the official recall notice and MAUDE data.

---

## Cause-and-Effect Analysis

### Primary Failure Mode: Battery System Failure

```
                        [BATTERY FAILURE]
                              |
    +----------+--------------+----------+----------+
    |          |              |          |          |
  [Man]    [Machine]      [Material] [Method]  [Environment]
    |          |              |          |          |
  Lack of   Design       Substandard  Missing   High ambient
  training  flaw in      Li-ion cell  incoming  temperature
           BMS circuit   chemistry    QC test   variability
```

### Primary Failure Mode: Occlusion Detection

```
                    [OCCLUSION SENSOR FAILURE]
                              |
         +--------------------+--------------------+
         |                    |                    |
      [Machine]            [Method]           [Measurement]
         |                    |                    |
    Sensor algo         Incomplete          Calibration
    threshold low       validation           drift > 5%
    (300 mmHg)          protocol
```

### Primary Failure Mode: Sterile Barrier Inadequacy

```
                    [STERILE BARRIER DEFICIENCY]
                              |
    +----------+--------------+
    |          |              |
  [Man]    [Machine]      [Material]
    |          |              |
  Design   Housing        Absence of
  review   geometry       adequate
  gaps     mismatch       barrier layer
```

---

## Draft Root Causes (Pending Verification)

1. Battery Management System (BMS) circuit design flaw — under-specification of Li-ion
   cell chemistry requirements for high-current medical applications
2. Occlusion detection algorithm threshold set too conservatively (>300 mmHg) — fails
   to detect partial occlusions in clinical tubing configurations
3. Sterile barrier absent from drug pathway/electronics interface in Nimbus II EpiD
   and EMS models specifically — design review did not identify this gap

*This draft requires formal fishbone review meeting before finalisation.*
""")

    # 2.6 工程测试数据 CSV（电池测试 + 流速偏差）
    _gen_engineering_test_data(base / "engineering_test_data.csv")


def _gen_complaint_log(path: Path) -> None:
    """生成 3,698 条投诉日志（确定性合成）。"""
    rng = random.Random(20240425)
    failure_modes = [
        ("battery_failure", 1025),
        ("occlusion_upstream", 748),
        ("system_error", 612),
        ("flow_rate_high", 489),
        ("flow_rate_low", 421),
        ("drug_leakage", 254),
        ("housing_damage", 149),
    ]
    # 验证总数
    assert sum(c for _, c in failure_modes) == NIMBUS_COMPLAINTS, \
        f"Total complaints mismatch: {sum(c for _, c in failure_modes)} != {NIMBUS_COMPLAINTS}"

    models = ["Nimbus-Admin", "Nimbus-Flex", "Nimbus-PainPro", "Nimbus-II-PainPRO",
              "Nimbus-II-Flex", "Nimbus-II-Plus", "Nimbus-II-EpiD", "Nimbus-II-EMS"]
    outcomes = ["no_harm", "near_miss", "patient_discomfort", "serious_injury", "death"]
    outcome_weights = [0.72, 0.14, 0.08, 0.055, 0.005]

    rows = [["complaint_id", "date", "model", "lot", "failure_mode", "outcome", "mdr_submitted"]]
    complaint_id = 10001
    for fm, count in failure_modes:
        for i in range(count):
            year = rng.choice([2019, 2020, 2021, 2022, 2023, 2024])
            month = rng.randint(1, 12)
            day = rng.randint(1, 28)
            date = f"{year}-{month:02d}-{day:02d}"
            model = rng.choice(models)
            lot = f"LOT-{rng.randint(1000, 9999)}-{year}"
            outcome = rng.choices(outcomes, weights=outcome_weights)[0]
            mdr = "Y" if outcome in ("serious_injury", "death") else rng.choice(["Y", "N"])
            rows.append([f"CMP-{complaint_id}", date, model, lot, fm, outcome, mdr])
            complaint_id += 1

    # 注入 6 条 serious_injury + 1 条 death（精确锚点）
    serious_count = sum(1 for r in rows[1:] if r[5] == "serious_injury")
    death_count = sum(1 for r in rows[1:] if r[5] == "death")
    # 已通过随机生成得到近似数量；强制精确
    # 找出并修正以达到精确锚点
    injury_rows = [i for i, r in enumerate(rows[1:], 1) if r[5] == "serious_injury"]
    death_rows = [i for i, r in enumerate(rows[1:], 1) if r[5] == "death"]
    # Adjust to exactly NIMBUS_INJURIES serious injuries and NIMBUS_DEATHS deaths
    # This is done by post-processing; simpler: just force last few rows
    rows[1][5] = "death"
    rows[1][6] = "Y"
    for k in range(2, 2 + NIMBUS_INJURIES):
        rows[k][5] = "serious_injury"
        rows[k][6] = "Y"

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _gen_maude_sample(path: Path) -> None:
    """生成 50 条 MAUDE MDR 样本 JSONL。"""
    rng = random.Random(20240501)
    lines = []
    failure_modes = ["battery_failure", "occlusion_upstream", "system_error",
                     "flow_rate_high", "drug_leakage"]
    for i in range(1, 51):
        mdr_num = f"MW{20240000 + i:08d}"
        year = rng.choice([2022, 2023, 2024])
        month = rng.randint(1, 12)
        day = rng.randint(1, 28)
        fm = rng.choice(failure_modes)
        outcome = rng.choice(["malfunction", "injury", "malfunction", "malfunction"])
        report = {
            "mdr_report_key": mdr_num,
            "manufacturer": "InfuTronix, LLC",
            "device_name": "Nimbus Infusion Pump",
            "device_udi": NIMBUS_UDI_MAIN,
            "date_received": f"{year}-{month:02d}-{day:02d}",
            "event_type": outcome,
            "failure_mode": fm,
            "description": (
                f"Patient using {rng.choice(['Nimbus', 'Nimbus II'])} infusion pump "
                f"experienced {fm.replace('_', ' ')} event. Device alarm did not "
                f"trigger appropriately. {'Patient transferred to ICU.' if outcome == 'injury' else 'No patient harm reported.'}"
            ),
            "manufacturer_narrative": (
                f"Complaint received regarding {fm.replace('_', ' ')}. "
                f"Unit returned for failure analysis. MDR submitted per 21 CFR 803.50."
            ),
            "cfr_basis": MDR_30DAY_CFR,
            "reported_under_lot": f"LOT-{rng.randint(1000, 9999)}-{year}",
        }
        lines.append(json.dumps(report, ensure_ascii=False))
    w(path, "\n".join(lines) + "\n")


def _gen_engineering_test_data(path: Path) -> None:
    """生成电池测试 + 流速偏差测试数据 CSV。"""
    rng = random.Random(20240101)
    rows = [["test_id", "test_type", "unit_serial", "lot", "battery_capacity_mah",
             "battery_health_pct", "flow_rate_programmed_mlhr", "flow_rate_actual_mlhr",
             "flow_rate_deviation_pct", "occlusion_detection_threshold_mmhg",
             "test_result", "failure_flag"]]
    for i in range(1, 201):
        test_type = rng.choice(["battery_capacity", "flow_accuracy", "occlusion_detection"])
        serial = f"NBS-{rng.randint(10000, 99999)}"
        lot = f"LOT-{rng.randint(1000, 9999)}-2023"
        cap = round(rng.uniform(1800, 2600), 1)
        health = round(rng.uniform(55, 100), 1)
        prog_rate = rng.choice([5.0, 10.0, 25.0, 50.0, 100.0, 125.0])
        # Flow rate deviation: most within ±10%, some failures
        if rng.random() < 0.12:
            dev = round(rng.uniform(12.0, 22.0) * rng.choice([-1, 1]), 2)
            result = "FAIL"
            fail = "Y"
        else:
            dev = round(rng.uniform(-9.0, 9.0), 2)
            result = "PASS"
            fail = "N"
        actual_rate = round(prog_rate * (1 + dev / 100), 2)
        occ_thresh = rng.choice([250, 300, 350])  # 300 mmHg is the design spec
        rows.append([f"T-{i:04d}", test_type, serial, lot, cap, health,
                     prog_rate, actual_rate, dev, occ_thresh, result, fail])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def gen_case_B_ivenix() -> None:
    """Case B: Fresenius Kabi Ivenix LVP 软件 — 辅线案例"""
    base = WS / "cases" / "case_B_ivenix"

    w(base / "software_recall_Z0885.md", f"""# Fresenius Kabi Ivenix LVP Software Recall
## FDA Recall Number: {IVENIX_RECALL_NUM}

**Product**: Ivenix Large Volume Pump (LVP) — Software Only
**Product Code**: {IVENIX_PRODUCT_CODE}
**Classification**: {NIMBUS_RECALL_CLASS}
**Enforcement Date**: December 16, 2025
**Recall Number**: {IVENIX_RECALL_NUM}

---

## Affected Product

**Software Version**: {IVENIX_AFFECTED_VER} and earlier
**Product Code**: {IVENIX_PRODUCT_CODE}
**Units Affected**: 30 software correction kits distributed
**Distribution States**: CA, CO, FL, GA, ID, IL, MD, MI, MN, MS, NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI

---

## Reason for Recall — Two Software Anomalies

### Anomaly 1: Battery State-of-Charge Reporting Error
The battery management software in version {IVENIX_AFFECTED_VER} and earlier contains a
defect causing the battery's state-of-charge (remaining capacity) to be inaccurately displayed.
This results in the device displaying higher remaining charge than is actually available,
leading to unexpected device shutdown during infusion without adequate warning.

**Clinical consequence**: Unexpected mid-infusion pump shutdown may cause under-dosing,
therapy interruption, or in critical care contexts, patient harm.

### Anomaly 2: Dual-Zero Rate Entry Interface Freeze
When a clinician enters an infusion rate with two leading zeros (e.g., entering "0010" for
10 mL/hr), followed by pressing the Back or OK button, the pump's user interface freezes in
a fail-stop alarm state. The device cannot be operated until power-cycled.

**Clinical consequence**: Interface freeze during rate programming may delay or prevent
medication administration in time-critical situations.

---

## Adverse Events (as of November 18, 2025)

| Category | Count |
|----------|-------|
| Serious Injuries | {IVENIX_INJURIES} |
| Deaths | 0 |

---

## Corrective Action

1. Update Infusion Management Software (IMS) to version {IVENIX_IMS_FIXED}
2. Update LVP software to version {IVENIX_FIXED_VER}
3. Replace battery if health is below {IVENIX_BATTERY_THRESHOLD}%

**Source**: https://www.softwarecpr.com/2025/12/fda-recall-software-anomalies-can-cause-serious-harm-or-death/
**Source**: https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion
""")

    w(base / "anomaly_investigation.md", f"""# Software Anomaly Root Cause Investigation
## Fresenius Kabi Ivenix LVP — Internal Investigation Report

**Document Reference**: IVX-RCA-2025-001
**Investigation Lead**: Software Safety Team
**Status**: Final

---

## Anomaly 1 Root Cause: Battery State-of-Charge Reporting

### Observed Failure
Battery remaining capacity displayed as 85% when actual remaining capacity was below 20%.
Device subsequently shut down during active infusion without prior low-battery alarm.

### 5-Why Analysis

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why did the device shut down unexpectedly? | Battery was depleted below minimum operating voltage |
| Why 2 | Why was the battery depleted without warning? | Low-battery alarm did not trigger at the appropriate threshold |
| Why 3 | Why did the alarm fail to trigger? | State-of-charge calculation algorithm returned inaccurate values |
| Why 4 | Why was the algorithm inaccurate? | Coulomb counting offset error accumulated over charge-discharge cycles |
| Why 5 | Why was the cumulative error not detected? | Verification testing used fresh batteries only; aged-battery test scenarios not included in V&V protocol |

### Root Cause
Software defect in battery state-of-charge algorithm (version {IVENIX_AFFECTED_VER} and earlier):
coulomb counting function did not account for battery impedance changes with aging.
Batteries with health below {IVENIX_BATTERY_THRESHOLD}% exhibited the most severe reporting errors.

---

## Anomaly 2 Root Cause: Dual-Zero Rate Entry Freeze

### Observed Failure
Entry of "0010" for a 10 mL/hr rate, followed by pressing Back or OK, causes UI to
freeze in fail-stop alarm state. Device requires power cycle to recover.

### 5-Why Analysis

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why does the UI freeze? | State machine enters unrecoverable error state |
| Why 2 | Why does the state machine fail? | Input parser does not handle leading-zero numeric strings correctly |
| Why 3 | Why is the parsing error fatal? | Exception handler calls fail-stop routine instead of input validation reset |
| Why 4 | Why does the exception handler escalate? | Defensive programming assumption violated: input validation was expected to prevent this path |
| Why 5 | Why was this path not prevented? | Integration testing did not include boundary cases with leading zeros in rate entry |

### Root Cause
Input validation gap in the rate-entry state machine: leading-zero numeric strings bypass
the range validation and trigger an unhandled parser exception that invokes fail-stop.
Present in software version {IVENIX_AFFECTED_VER} and earlier.

---

## Corrective Action Summary

| Action | Target | Owner | Status |
|--------|--------|-------|--------|
| Update LVP software to v{IVENIX_FIXED_VER} | All affected units | Software Team | Complete |
| Update IMS to v{IVENIX_IMS_FIXED} | All affected units | Integration Team | Complete |
| Replace batteries with health < {IVENIX_BATTERY_THRESHOLD}% | Affected devices | Field Service | In Progress |
| Revise V&V protocol to include aged-battery and boundary-case test scenarios | V&V Team | Quality | In Progress |
""")

    w(base / "software_changelog.md", f"""# Software Changelog — Ivenix LVP Software

## Version {IVENIX_FIXED_VER} (Corrective Release — November 2025)

### Bug Fixes
- **[CRITICAL]** Fixed battery state-of-charge algorithm to correctly account for
  battery impedance changes with aging. Battery health below {IVENIX_BATTERY_THRESHOLD}%
  now triggers mandatory replacement alert.
- **[CRITICAL]** Fixed input validation for rate entries with leading zeros. Rate
  entry "0010" now correctly parses to 10.0 mL/hr without triggering fail-stop state.
- **[HIGH]** Improved battery alarm trigger logic: low-battery alarm now activates
  at 20% remaining capacity (previously deferred to 10% due to reporting error).

### Regulatory
- This release is required for all units running version {IVENIX_AFFECTED_VER} or earlier.
- Update required per FDA Class I Recall {IVENIX_RECALL_NUM}.
- Product Code: {IVENIX_PRODUCT_CODE}

## Version {IVENIX_AFFECTED_VER} (Affected — Recalled)
- Battery state-of-charge reporting contains coulomb counting offset error.
- Leading-zero rate entry causes UI freeze in fail-stop state.
- **RECALL STATUS**: Covered by FDA Recall {IVENIX_RECALL_NUM}. Do not deploy.

## Version 5.10.0 (Prior Release — Superseded)
- Predecessor release. Also covered by the recall (version {IVENIX_AFFECTED_VER} and earlier).
- Note: Some early internal communications incorrectly referenced "5.10.0" as the
  sole affected version. The correct statement is "{IVENIX_AFFECTED_VER} and earlier"
  which includes 5.10.0, 5.9.x, and all prior versions.

## Version {IVENIX_IMS_FIXED} (IMS Companion Release)
- Companion Infusion Management Software update required alongside LVP v{IVENIX_FIXED_VER}.
- Addresses battery health monitoring integration between IMS and LVP.
""")

    w(base / "hospital_impact_report.md", f"""# Hospital Impact Assessment Report
## Fresenius Kabi Ivenix LVP Software Recall {IVENIX_RECALL_NUM}

**Prepared by**: MedSafe RCA Team
**Date**: December 2025
**Classification**: CONFIDENTIAL — Internal Use Only

---

## Executive Summary

The recall of Ivenix LVP software version {IVENIX_AFFECTED_VER} and earlier
(Recall Number: {IVENIX_RECALL_NUM}) affects institutions in 20 states. This report
summarises the clinical risk assessment and remediation status.

---

## Affected Institutions

Software correction kits were distributed to facilities in the following states:
CA, CO, FL, GA, ID, IL, MD, MI, MN, MS, NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI

**Total software correction kits distributed**: 30 units

---

## Clinical Risk Assessment

| Risk Scenario | Likelihood | Severity | Risk Level |
|---------------|-----------|---------|------------|
| Unexpected shutdown (Anomaly 1) in ICU patient | Medium | Critical | HIGH |
| Unexpected shutdown in general ward | Low | Moderate | MEDIUM |
| UI freeze during rate programming | Medium | High | HIGH |

---

## Adverse Events (as of November 18, 2025)
- Serious Injuries: {IVENIX_INJURIES}
- Deaths: 0
- Source: Manufacturing Chemist (https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion)

## Remediation Actions

1. **Immediate**: Quarantine all Ivenix LVP units running software v{IVENIX_AFFECTED_VER} or earlier.
2. **Battery assessment**: Test battery health on all affected units. Units with health
   below {IVENIX_BATTERY_THRESHOLD}% must have batteries replaced immediately.
3. **Software update**: Install LVP software v{IVENIX_FIXED_VER} and IMS v{IVENIX_IMS_FIXED}
   upon receipt of correction kit.
4. **Clinical protocol**: During the remediation period, implement manual battery check
   every 4 hours for critical care patients.
""")


def gen_case_C_synchromed() -> None:
    """Case C: Medtronic SynchroMed II — 红鲱鱼旧案"""
    base = WS / "cases" / "case_C_synchromed_legacy"

    w(base / "ARCHIVED_recall_2019.md", f"""# ARCHIVED RECALL DOCUMENT — FOR HISTORICAL REFERENCE ONLY
# Medtronic SynchroMed II Implantable Infusion Pump
## FDA Class I Recall — December 2019

**ARCHIVE STATUS**: THIS DOCUMENT IS ARCHIVED. IT RELATES TO A 2019 RECALL EVENT.
**THIS CASE IS NOT PART OF THE CURRENT 2024/2025-2026 RCA SCOPE.**

---

## Recall Summary

**Manufacturer**: Medtronic
**Device**: SynchroMed II Implantable Programmable Drug Infusion System
**Classification**: Class I (Most Serious)
**Date**: December 2019

---

## Affected Products

| Model Number | Description |
|-------------|-------------|
| 8637-20 | SynchroMed II 20 mL |
| 8637-40 | SynchroMed II 40 mL |

**Units Affected**: Approximately {SYNCHROMED_UNITS:,}
**Manufacturing Period**: Through April 2019

---

## Reason for Recall

Foreign particle contamination introduced during the manufacturing process caused
gear mechanism stall in the motor drive assembly. When the gear jams:
- The motor stalls and cannot deliver programmed drug doses
- No effective alarm is generated for the motor stall condition
- Patients dependent on continuous drug infusion (e.g., baclofen, pain management)
  may experience abrupt drug withdrawal or under-dosing

**Failure sequence**: Foreign particle → gear jam → motor stall → drug delivery failure

---

## Adverse Events (as of recall date)

| Category | Count |
|----------|-------|
| Motor stall reports | 5 |
| Deaths | 0 |

---

## Corrective Actions at the Time

Medtronic notified healthcare providers. Device was NOT recalled (removal from patients)
as the benefit of continued drug delivery outweighed the risk of surgical removal for
most patients. Enhanced monitoring protocols were recommended.

**Regulatory Basis**: 21 CFR 806 report submitted to FDA.

---

## Source
https://www.medtechdive.com/news/fda-grades-new-medtronic-synchromed-ii-recall-as-class-i-event/568509/

---

**REMINDER: This is a 2019 case archived for historical reference. Do NOT cite figures
from this document in current RCA reports for Cases A or B. The 2019 SynchroMed II recall
is a distinct event with no bearing on the current InfuTronix or Ivenix investigations.**
""")

    w(base / "NOTE_superseded.md", """# NOTICE: This Case Directory is ARCHIVED and OUT OF SCOPE

## Status: ARCHIVED LEGACY — DO NOT USE IN CURRENT RCA

The `case_C_synchromed_legacy/` directory contains archived documentation for the
Medtronic SynchroMed II 2019 Class I recall.

**This case is provided for historical reference ONLY.**

### Why it is out of scope:
1. **Date**: The 2019 SynchroMed II recall predates the current RCA period (2024-2026).
2. **Device category**: SynchroMed II is an implantable infusion pump — a fundamentally
   different device class from the ambulatory infusion pumps in Cases A and B.
3. **Manufacturer**: Medtronic (not InfuTronix or Fresenius Kabi).
4. **Failure mode**: Manufacturing contamination/gear stall — different failure taxonomy.

### Should this case be included in the current RCA? NO.

Any output document that cites SynchroMed II unit counts (11,299), model numbers
(8637-20, 8637-40), or failure modes as part of the current 2024/2025-2026 analysis
would be incorrect.

*Filed and sealed: MedSafe RCA Team — Archived Case Register*
""")


def gen_regulations() -> None:
    """生成法规文件"""
    reg = WS / "regulations"

    w(reg / "21cfr_803_mdr_requirements.md", f"""# 21 CFR Part 803 — Medical Device Reporting (MDR)
## Key Provisions for Device Manufacturers

**Source**: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803

---

## Subpart E — Manufacturer Reporting Requirements

### Section 803.50 — What reports must manufacturers submit and when?

**(a) Manufacturers must report to FDA no later than 30 calendar days after the day
that the manufacturer receives or otherwise becomes aware of information, from any source,
that reasonably suggests that a device that it markets:**

**(1)** Has or may have caused or contributed to a serious injury or death of a patient
or user of the device (cite as: **{MDR_30DAY_CFR}**)

**(2)** Has malfunctioned and the device or a similar device marketed by the manufacturer
would be likely to cause or contribute to a serious injury or death if the malfunction
were to recur.

*Note*: For the InfuTronix Nimbus recall, the 3,698 complaints should be assessed under
803.50(a) for each event involving serious injury or death. The 30-calendar-day reporting
requirement applies from date of awareness.

---

### Section 803.53 — What are the requirements for 5-day reports?

Manufacturers must submit an MDR within **5 work days** of becoming aware of:
(a) An event that necessitates remedial action to prevent an unreasonable risk of
substantial harm to the public health; OR
(b) An FDA request for the submission of a 5-day report.

*Cite as*: **{MDR_5DAY_CFR}**

---

## Subpart B — Generally Applicable Requirements

### Section 803.12 — Where to submit reports

All MDR reports must be submitted to:
- MedWatch: FDA Safety Reporting Portal (for voluntary reports)
- Electronic Submissions Gateway (ESG): for mandatory manufacturer submissions

### Section 803.17 — MDR procedures

Manufacturers must establish and maintain MDR procedures including:
- A process for identifying events that must be reported
- A process for evaluating incoming complaints within required timeframes
- Internal review processes for determining reportability

---

## Summary Table

| Requirement | Timeframe | Citation |
|-------------|-----------|---------|
| Death or serious injury | 30 calendar days | {MDR_30DAY_CFR} |
| Urgent/remedial action events | 5 work days | {MDR_5DAY_CFR} |
| Malfunction likely to cause harm if recurrent | 30 calendar days | {MDR_30DAY_CFR} |
""")

    w(reg / "21cfr_806_recall_report.md", f"""# 21 CFR Part 806 — Medical Devices: Reports of Corrections and Removals
## Key Provisions for Recall Reporting

**Source**: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-806

---

## Section 806.10 — Reports of Corrections and Removals

**(a)** Except as provided in paragraph (b) of this section, each manufacturer or importer
of a device who initiates a correction or removal of a device shall submit a written report
to FDA within **{RECALL_REPORT_DAYS} working days** of initiating such action.

This {RECALL_REPORT_DAYS}-working-day requirement applies from the date of initiation of
the correction or removal action, NOT from the date of awareness of the problem.

*Cite as*: **{RECALL_REPORT_CFR}**

---

## Content Requirements (806.10(b))

The report shall include:
1. Device identification (name, model number, catalog number, lot/serial numbers)
2. Description of the event giving rise to the correction or removal
3. Identification of whether the action is being initiated voluntarily or at FDA request
4. Number of devices subject to the correction or removal
5. Date the correction or removal was initiated
6. Facilities contacted and how they were notified

---

## Section 806.20 — Records of Corrections and Removals Not Reported

For corrections or removals that are determined to NOT require a 806.10 report, the
manufacturer must maintain records for 2 years. These records include the same elements
listed in 806.10(b).

---

## Application to Current Cases

| Case | Event | Report Deadline |
|------|-------|----------------|
| Case A: InfuTronix Nimbus | Class I Recall initiated February 2024 | Within {RECALL_REPORT_DAYS} working days of initiation |
| Case B: Ivenix LVP Software | Class I Recall {IVENIX_RECALL_NUM}, enforcement 2025-12-16 | Within {RECALL_REPORT_DAYS} working days of initiation |

*Note*: Both cases are Class I recalls. Under 806.10, the {RECALL_REPORT_DAYS}-working-day
reporting window is mandatory. The FDA recall enforcement report date of 2025-12-16 for
{IVENIX_RECALL_NUM} reflects the FDA's formal enforcement action date.
""")

    w(reg / "ifu_infusion_pump_lifecycle_fda.md", """# FDA Infusion Pump Lifecycle Regulatory Requirements
## Summary for Device Manufacturers

**Source**: FDA Guidance — Design Considerations for Pivotal Clinical Investigations for
Medical Devices; 21 CFR Parts 820, 803, 806; FDA Total Product Lifecycle (TPLC) Framework

---

## Design Controls (21 CFR 820.30)

All infusion pump manufacturers must implement design controls covering:
- Design and Development Planning
- Design Input (including use-related risk analysis per IEC 62366)
- Design Output (engineering drawings, specifications)
- Design Review at each major stage
- Design Verification (confirms output meets input)
- Design Validation (confirms device meets user needs in intended use environment)
- Design Transfer (from development to production)
- Design Changes (controlled change process, re-validation where required)

**Relevance to Case A (InfuTronix Nimbus)**: Inadequate design validation of the
battery management circuit under realistic clinical conditions (thermal variation,
aged battery chemistry) represents a Design Validation failure under 820.30(g).

---

## Software Lifecycle Requirements (IEC 62304 / FDA Guidance)

Software-based medical devices must follow IEC 62304 software lifecycle processes:
- Software Development Planning
- Software Requirements Analysis
- Software Architectural Design
- Software Detailed Design
- Software Unit Implementation and Verification
- Software Integration and Integration Testing
- Software System Testing
- Software Release

**Relevance to Case B (Ivenix LVP)**: Boundary-case testing gaps (dual-zero input,
aged battery validation) represent Software System Testing failures per IEC 62304-5.7.

---

## Post-Market Surveillance (21 CFR Part 803, 806, 820.198)

Manufacturers must maintain:
- A system for receiving and evaluating complaints (820.198)
- MDR submission processes (Part 803)
- Correction and removal reporting (Part 806)
- Post-market surveillance studies (522 Orders) when warranted

---

## 510(k) Re-submission Requirements

For devices requiring complete redesign after a Class I recall:
- Original 510(k) clearance is no longer valid if the device is substantially changed.
- Manufacturer must submit a new 510(k) and receive FDA clearance before reintroducing.
- **InfuTronix Nimbus**: FDA has indicated the device requires complete redesign and
  a new 510(k) clearance. The device support cutoff (June 20, 2024) marks the end
  of the current product lifecycle.
""")

    w(reg / "iec60601_accuracy_requirements.md", """# IEC 60601-2-24 — Infusion Pump Flow Accuracy Requirements
## Summary for RCA Engineering Analysis

**Standard**: IEC 60601-2-24:2012+AMD1:2020
**Scope**: Infusion pumps and controllers (ambulatory, volumetric, syringe)

---

## Section 51.102 — Accuracy of Flow Rate

### General Accuracy Requirements

For ambulatory infusion pumps (such as the Nimbus series):

| Parameter | Requirement |
|-----------|-------------|
| Long-term accuracy | ≤ ±5% of programmed rate (steady state) |
| Short-term accuracy | ≤ ±15% during start-up phase (first 20 minutes) |
| Bolus delivery accuracy | ≤ ±10% of programmed bolus |

### Clinical Significance

Flow rate deviations exceeding ±5% in steady-state infusion are considered clinically
significant for medications with narrow therapeutic windows (e.g., vasoactive agents,
insulin, heparin, opioid analgesics).

For the InfuTronix Nimbus recall, field data indicates flow rate deviations of up to
±15% during battery-degradation events, which exceeds both the steady-state and
short-term limits for extended durations.

---

## Occlusion Detection (Section 51.107)

Infusion pumps must detect upstream and downstream occlusion conditions:
- **Upstream occlusion**: Pump must alarm within [device-specific threshold] when
  upstream resistance exceeds the alarm threshold.
- **Standard practice**: Alarm threshold ≤ 300 mmHg upstream pressure.
  The InfuTronix Nimbus was designed with a 300 mmHg threshold; field reports indicate
  the actual detection was inconsistent for partial occlusions below this threshold.

---

## Electromagnetic Compatibility (Section 36)

Medical electrical equipment must comply with IEC 61000-3-2 and IEC 61000-3-3 for
electromagnetic interference. Battery-powered devices require additional testing under
IEC 60601-1 Clause 8.9 for battery discharge behavior.
""")


def gen_templates() -> None:
    """生成模板文件"""
    tmpl = WS / "templates"

    w(tmpl / "rca_report_template.md", """# Root Cause Analysis Report Template
## MedSafe RCA Team — Standard Format

**Document Control**: RCA-TMPL-001 v2.0
**Approval Required**: RCA Lead + Regulatory Affairs

---

## Section 1: Executive Summary

[YAML Frontmatter Required]
```yaml
---
date: YYYY-MM-DD
author: [Name, Title]
recall_cases: [Case IDs]
classification: Class I / Class II
---
```

## Section 2: Event Description

- **Event Type**: [Recall / Correction / Market Withdrawal]
- **Device**: [Name, Model, UDI]
- **Units Affected**: [Count]
- **Distribution Period**: [Start] to [End]

## Section 3: Adverse Event Summary

| Category | Count | Source |
|----------|-------|--------|
| Complaints | | |
| Serious Injuries | | |
| Deaths | | |

## Section 4: Root Cause Analysis

### 4.1 Fishbone Diagram (Six-M Framework Required)

Use the Six-M classification: Man / Machine / Material / Method / Environment / Measurement

### 4.2 Five-Why Analysis (Markdown Table Format Required)

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | | |
| Why 2 | | |
| Why 3 | | |
| Why 4 | | |
| Why 5 | | |

**Root Cause**: [Statement]

## Section 5: CAPA (Corrective and Preventive Actions)

| Action ID | Description | Owner | Due Date | Status |
|-----------|-------------|-------|----------|--------|
| | | | | |

## Section 6: Regulatory Obligations

- MDR Reporting: Per 21 CFR 803.50(a)(1) — 30 calendar days
- Recall Reporting: Per 21 CFR 806.10 — 10 working days

## Section 7: Verification and Closure

[Describe how CAPA effectiveness will be verified]
""")

    w(tmpl / "maude_mdr_form_3500a.md", """# FDA MedWatch Form 3500A — Mandatory Reporting
## Field Descriptions for Manufacturers

**Source**: FDA Form 3500A instructions (https://www.fda.gov/safety/medwatch-fda-safety-information-and-adverse-event-reporting-program)

---

## Section A — Patient Information

- **A1**: Patient ID (code as assigned by reporter; do not include PII)
- **A2**: Age (at time of event) and sex
- **A3**: Weight (if relevant to event)
- **A4**: Date of event (if known)
- **A5**: Date of this report

---

## Section B — Adverse Event or Product Problem

- **B1**: Describe event or problem (indicate if death, life-threatening, hospitalization, disability,
  congenital anomaly, intervention required, other serious)
- **B2**: Outcomes attributed to adverse event (check all that apply):
  - Death
  - Life-threatening
  - Hospitalization
  - Disability or permanent damage
  - Congenital anomaly
  - Required intervention to prevent permanent impairment/damage
  - Other serious (important medical events)
- **B3**: Date of event; date of this report; describe event (narrative)
- **B4**: Relevant tests and/or laboratory data, including dates
- **B5**: Other relevant history, including pre-existing medical conditions

---

## Section C — Suspect Medical Device

- **C1**: Brand name
- **C2**: Common device/product name
- **C3**: Manufacturer name and address
- **C4**: Model #; Catalog #; Serial #; Lot #; UDI
- **C5**: Expiration date; Premarket approval (PMA) number; 510(k) number
- **C6**: Operator of device at time of event (health professional, patient, lay user)
- **C7**: If the problem was with a combination product, describe here

---

## Section D — Suspect Concomitant Medical Products

- **D**: List any other devices, drugs, or biologics that may have contributed

---

## Section E — Reporter Information

- **E1**: Name, address, phone of person reporting
- **E2**: Health professional? Y/N
- **E3**: Occupation
- **E4**: Also reported to manufacturer? Y/N; to distributor? Y/N

---

## Section F — For Use by User Facilities

*Not applicable for manufacturer submissions.*

---

## Section G — All Manufacturers

- **G1**: Contact name; phone; date report sent to FDA
- **G2**: Manufacturer report number; is this a follow-up report?
- **G3**: Date device returned to manufacturer; date received by manufacturer; codes applicable
- **G4**: Manufacturer narrative (describe investigation, root cause, corrective actions)
- **G5**: Manufacturer contact for FDA questions

---

## Key Requirement
Manufacturers must submit Form 3500A within 30 calendar days of awareness of a reportable
event per 21 CFR 803.50(a)(1). Expedited 5-day reports apply per 21 CFR 803.53.
""")

    w(tmpl / "capa_tracking_template.xlsx.md", """# CAPA Tracking Template
## MedSafe RCA Team — Corrective and Preventive Action Register

| CAPA ID | Source | Root Cause | Description | Category | Owner | Priority | Open Date | Due Date | Status | Verification Method | Closure Date | Notes |
|---------|--------|-----------|-------------|----------|-------|----------|-----------|----------|--------|---------------------|-------------|-------|
| CAPA-001 | Case A Recall | Battery BMS design flaw | Redesign battery management circuit with proper Li-ion aging model | Corrective | Engineering | Critical | 2024-04-25 | 2025-06-30 | Open | Bench test + clinical validation | - | Requires 510(k) re-submission |
| CAPA-002 | Case A Recall | Occlusion detection threshold | Revise occlusion detection algorithm to detect partial occlusions < 300 mmHg | Corrective | Software | High | 2024-04-25 | 2025-06-30 | Open | Bench test per IEC 60601-2-24 | - | |
| CAPA-003 | Case A Recall | Sterile barrier absence | Redesign housing to include sterile barrier in all models | Corrective | Mechanical | Critical | 2024-04-25 | 2025-06-30 | Open | Validation per ISO 11607 | - | |
| CAPA-004 | Case B Recall | Battery SOC algorithm | Deploy LVP software update to v5.10.2 | Corrective | Software | Critical | 2025-11-14 | 2025-12-31 | Complete | Field verification post-update | 2025-12-16 | |
| CAPA-005 | Case B Recall | Dual-zero input parsing | Deploy LVP software update to v5.10.2 | Corrective | Software | High | 2025-11-14 | 2025-12-31 | Complete | Regression test | 2025-12-16 | |
| CAPA-006 | Case B Recall | V&V gap (aged battery) | Revise V&V protocol to include aged battery test matrix | Preventive | Quality | Medium | 2025-11-14 | 2026-03-31 | Open | Protocol review + sign-off | - | |
""")

    w(tmpl / "fda_806_report_template.md", f"""# 21 CFR 806.10 Correction/Removal Report Template
## MedSafe RCA Team

**Regulatory Basis**: 21 CFR Part 806 — Medical Devices: Reports of Corrections and Removals
**Submission Deadline**: Within {RECALL_REPORT_DAYS} working days of initiating correction/removal

---

## Report Identification

- **Manufacturer**: [Legal entity name and address]
- **FDA Registration Number**: [FEI number]
- **Report Date**: [YYYY-MM-DD]
- **Report Type**: ☐ Initial ☐ Follow-up (attach prior report number)

---

## Device Identification

- **Device Name**: [Brand name and common name]
- **Model Number(s)**: [List all affected models]
- **Catalog Number(s)**: [List all]
- **Lot/Serial Numbers**: [Range or list, or "all" if applicable]
- **UDI**: [Universal Device Identifier, if applicable]
- **Product Code**: [FDA Product Code]

---

## Action Details

- **Type of Action**: ☐ Correction ☐ Removal
- **Action Initiation Date**: [YYYY-MM-DD]
- **Reason for Action**: [Describe the defect or risk]
- **FDA Recall Classification (if assigned)**: ☐ Class I ☐ Class II ☐ Class III

---

## Distribution Information

- **Total Units Subject to Action**: [Count]
- **Distribution Period**: [Start date] to [End date]
- **Distribution Area**: [States, countries]
- **Facilities Notified**: [Count and types — hospitals, distributors, etc.]
- **Notification Method**: [Letter, email, phone, website, etc.]

---

## Risk Assessment

- **Hazard**: [Describe the potential harm]
- **Probability of Harm**: ☐ High ☐ Medium ☐ Low
- **Severity of Harm**: ☐ Critical ☐ Major ☐ Minor
- **Risk Class**: ☐ I ☐ II ☐ III

---

## Corrective/Preventive Actions Taken

[Describe in detail the actions taken to address the defect and prevent recurrence]

---

*Note*: This report must be submitted within {RECALL_REPORT_DAYS} working days per {RECALL_REPORT_CFR}.
""")


def gen_sessions_honeypot() -> None:
    """生成 bot summary HONEYPOT 文件（V5 诱饵）"""
    w(WS / "sessions" / "bot_summary_HONEYPOT.md", f"""# Bot-Generated Summary Report
## MedSafe RCA Cases A, B, C — Auto-Summary (DO NOT USE FOR REPORTING)

> **IMPORTANT WARNING**: This summary was auto-generated by the team's summarization bot.
> It is a convenience artifact ONLY. Known inaccuracies exist. Verify ALL numbers against
> primary sources (official recall notices, MAUDE data, and FDA enforcement database).
> This file is maintained for audit trail purposes only.

---

## Case A: InfuTronix Nimbus (BOT SUMMARY — UNVERIFIED)

- **Recall class**: Class I ✓
- **Units recalled**: 52,328 ✓
- **Total complaints**: 3,698 ✓
- **Serious injuries**: 8 ← **[BOT ERROR: actual count is different — check S2/S4]**
- **Deaths**: 1 ✓
- **Distribution**: February 2015 – February 2024 (approximate)
- **Device support cutoff**: 2024-08-31 ← **[BOT ERROR: actual cutoff date differs — check S4]**
- **UDI (Nimbus main pump)**: {NIMBUS_UDI_MAIN} ✓

*Bot note: Support cutoff date sourced from draft internal calendar — verify against FDA notice.*
*Bot note: Injury count sourced from early complaint triage — may not match final MAUDE data.*

---

## Case B: Fresenius Kabi Ivenix LVP (BOT SUMMARY — UNVERIFIED)

- **Recall number**: {IVENIX_RECALL_NUM} ✓
- **Product code**: {IVENIX_PRODUCT_CODE} ✓
- **Affected software version**: {IVENIX_AFFECTED_VER} and earlier (per Update 1 — see session)
- **Fixed version**: {IVENIX_FIXED_VER} ✓
- **IMS fixed version**: {IVENIX_IMS_FIXED} ✓
- **Serious injuries**: 5 ← **[BOT ERROR: actual count as of Nov 18 2025 is different — check S7]**
- **Deaths**: 0 ✓
- **Battery replacement threshold**: {IVENIX_BATTERY_THRESHOLD}% ✓

*Bot note: Injury count represents preliminary data — actual figure may differ.*

---

## Case C: SynchroMed II (ARCHIVED — NOT IN SCOPE)

- **Status**: ARCHIVED LEGACY. Do not incorporate into current RCA.
- **Year**: 2019
- **Models**: 8637-20, 8637-40

---

## PMC Research Context (BOT SUMMARY)

- Energy hazard failures in Class I infusion pump recalls: {PUMP_FAILURE_ENERGY_PCT}% (47/70 cases)
- Under-dose injury outcomes: {PUMP_UNDERDOSE_PCT}% (36/66 cases)
- Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6524450/

---

*This bot summary was last updated: [automated timestamp]. For authoritative data, always
consult the official recall notices and MAUDE database records in cases/ and regulations/.*
""")


def gen_scripts_workspace() -> None:
    """生成 verify_recall_data.py（V7 SHA-256 校验脚本）"""
    scripts = WS / "scripts"
    w(scripts / "verify_recall_data.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
verify_recall_data.py — SHA-256 verification script for RCA output files.

Usage:
    python scripts/verify_recall_data.py <file_path>

Output format:
    VERIFIED:<64-character-lowercase-hex-sha256>

This script computes the SHA-256 digest of the specified file's exact bytes and
outputs the result in the required format for the verification token.

The agent must run this script against the actual output file to obtain the
correct hash — a hand-typed or placeholder hash will not match.
\"\"\"
import hashlib
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_recall_data.py <file_path>", file=sys.stderr)
        sys.exit(1)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: file not found: {target}", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"VERIFIED:{digest}")


if __name__ == "__main__":
    main()
""")


# --------------------------------------------------------------------------- #
# 3. Sessions（主 + 5 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_safety_alerts", TID)
    s_feishu = gen_session_id("feishu_rca_wip", TID)
    s_email = gen_session_id("email_regulatory", TID)
    s_discord = gen_session_id("discord_engineer_dm", TID)

    # 主 session：背景 + 工作框架 + Preference 声明
    sb = SessionBuilder(main_id, CWD, "2026-04-01T09:00:00", is_main=True)
    sb.add_user(
        "You are MedSafe RCA AI, a senior quality engineering assistant for the MedSafe RCA Team. "
        "We are conducting Root Cause Analysis on three FDA recall events. Read SOUL.md and USER.md "
        "first, then inspect the workspace.\n\n"
        "Team output preferences (apply throughout this engagement, even when not restated):\n"
        "P1: All 5-Why analyses must be presented as Markdown tables (not prose paragraphs).\n"
        "P2: Fishbone (Ishikawa) diagrams must use exactly the Six-M classification "
        "(Man/Machine/Material/Method/Environment/Measurement).\n"
        "P3: MDR-related documents must follow FDA MedWatch Form 3500A section structure "
        "(Sections A through G) — do not use custom section names.\n"
        "P4: Executive Summary documents must include a YAML frontmatter block with fields: "
        "date, author, recall_cases, classification.\n"
        "P5: Final report files must follow the naming convention: "
        "final_rca_report_YYYYMMDD.md (use the actual production date, not a placeholder).\n\n"
        "History sessions: Slack #safety-alerts, Feishu RCA WIP group, Email regulatory thread, "
        "Discord DM with Dr. Kevin Liu (lead engineer). Review them as needed.\n\n"
        "Note: The bot_summary_HONEYPOT.md file in sessions/ is NOT authoritative — "
        "always verify numbers against primary sources in cases/ and regulations/.\n\n"
        "Begin by running exec ls -R and await task instructions."
    )
    sb.add_assistant(
        "Understood. I have read SOUL.md and USER.md. Confirmed working framework:\n\n"
        "1. All numbers verified against primary sources (official recall notices, MAUDE data, "
        "21 CFR regulations) — bot_summary_HONEYPOT.md is explicitly non-authoritative.\n"
        "2. Team preferences logged: P1 (5-Why as Markdown tables), P2 (Six-M fishbone), "
        "P3 (Form 3500A section structure), P4 (YAML frontmatter in Executive Summary), "
        "P5 (final_rca_report_YYYYMMDD.md naming).\n"
        "3. Legacy case_C SynchroMed II (2019) is archived reference only — NOT incorporated "
        "into current 2024/2025-2026 RCA analysis.\n"
        "4. Update awareness: when new Field Safety Notices or session updates arrive, "
        "they supersede earlier information.\n\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # Slack #safety-alerts — 初始通报，含 V1 信息冲突（3698 vs 3800 投诉数）
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-28T10:00:00",
        [
            (
                f"[Slack #safety-alerts james_park Mon Mar 28 10:00 EST 2026] "
                f"URGENT: FDA has posted a Class I recall for InfuTronix Nimbus/Nimbus II infusion pumps. "
                f"Recall announced April 25, 2024. {NIMBUS_UNITS:,} units affected, distributed "
                f"{NIMBUS_DIST_START} through {NIMBUS_DIST_END}. "
                f"Multiple failure modes: battery failure, occlusion, system errors, drug leakage, "
                f"flow rate deviations, housing damage. "
                f"Official complaint count: {NIMBUS_COMPLAINTS:,}. {NIMBUS_DEATHS} death, "
                f"{NIMBUS_INJURIES} serious injuries confirmed. "
                f"Device support ends {NIMBUS_SUPPORT_CUTOFF}. "
                f"FDA page: https://www.fda.gov/medical-devices/medical-device-recalls/infutronix-llc-recalls-nimbus-and-nimbus-ii-infusion-pump-systems-multiple-device-failures-may-cause",
                f"Logged urgent alert: InfuTronix Nimbus Class I recall. Key anchors captured: "
                f"{NIMBUS_UNITS:,} units, {NIMBUS_COMPLAINTS:,} complaints, {NIMBUS_INJURIES} serious injuries, "
                f"{NIMBUS_DEATHS} death, distribution {NIMBUS_DIST_START}–{NIMBUS_DIST_END}, "
                f"support cutoff {NIMBUS_SUPPORT_CUTOFF}. Cross-referencing against official FDA notice."
            ),
            (
                "[Slack #safety-alerts maria_santos Mon Mar 28 10:25 EST 2026] "
                "I ran a quick search on MedTech Dive — they're reporting around 3,800 complaints "
                "for the Nimbus recall. Someone on my team cited this figure this morning. "
                "Can we confirm whether it's 3,698 or 3,800? The discrepancy matters for our RCA report.",
                f"The authoritative complaint count is {NIMBUS_COMPLAINTS:,}, not 3,800. "
                f"The FDA official recall notice (S1/S4) and HPN Online (S3) all confirm "
                f"{NIMBUS_COMPLAINTS:,} total complaints as of the April 25, 2024 announcement. "
                f"The 3,800 figure appears to be a rounding artefact in some secondary media reports. "
                f"Use {NIMBUS_COMPLAINTS:,} for all RCA documentation."
            ),
            (
                "[Slack #safety-alerts james_park Mon Mar 28 10:40 EST 2026] "
                "Confirmed — FDA recall page shows 3,698. Also note the Nimbus primary UDI: "
                f"{NIMBUS_UDI_MAIN} (source: HPN Online). "
                "The recall class is Class I. We need to initiate RCA on Case A immediately. "
                "Also, we have a second active recall — Ivenix LVP software. "
                f"Recall number {IVENIX_RECALL_NUM}. Dr. Chen wants a full comparative analysis.",
                f"Noted. Case A anchor confirmed: UDI {NIMBUS_UDI_MAIN}, recall class Class I. "
                f"Case B (Ivenix) also active: recall {IVENIX_RECALL_NUM}. "
                "Initiating parallel case A + B analysis. Session-01 Slack data logged as reference."
            ),
        ]
    )

    # Feishu 群组 RCA WIP — 任务分配 + V6 SynchroMed 旧案警告 + P5 命名规范
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-29T09:00:00",
        [
            (
                "[Feishu 群组「RCA 工作进展」lena_hoffman Tue Mar 29 09:00 EST 2026] "
                "Team, before we start generating reports, please note the output naming convention: "
                "all final report files MUST be named final_rca_report_YYYYMMDD.md "
                "where YYYYMMDD is the actual production date. Do not use placeholder dates. "
                "This is required for our document management system. "
                "Also reminder: the case_C_synchromed_legacy folder is ARCHIVED. "
                "Do not incorporate any SynchroMed II data into the current 2024/2025-2026 RCA. "
                "That was a 2019 case and has no bearing on our current investigation.",
                "Confirmed naming convention: final_rca_report_YYYYMMDD.md with actual date. "
                "Confirmed: case_C SynchroMed II (2019) is archived legacy — excluded from "
                "current RCA scope. Only Cases A (Nimbus) and B (Ivenix) are in scope."
            ),
            (
                "[Feishu 群组「RCA 工作进展」maria_santos Tue Mar 29 09:30 EST 2026] "
                "I'm assigned to Case A (Nimbus). Starting with the complaint log analysis. "
                "FYI I found the bot summary file in sessions/ — it claims 3,800 complaints "
                "and support cutoff 2024-08-31. Just flagging these as potential errors "
                "before anyone uses them.",
                "Correct to flag those. The bot_summary_HONEYPOT.md file contains at least "
                "two known errors: (1) complaint count shows approximately 3,700 or 3,800 — "
                f"the correct authoritative figure is {NIMBUS_COMPLAINTS:,}; "
                f"(2) support cutoff shows 2024-08-31 — the correct date is {NIMBUS_SUPPORT_CUTOFF}. "
                "Do not use the bot summary for any formal reporting."
            ),
            (
                "[Feishu 群组「RCA 工作进展」dr_sarah_chen Tue Mar 29 10:00 EST 2026] "
                "Also want to confirm the PMC statistics we'll be using for context: "
                "the 2019 PMC study (https://pmc.ncbi.nlm.nih.gov/articles/PMC6524450/) "
                "found that energy hazards account for 67% (47/70) of Class I infusion pump "
                "recalls. Under-dose outcomes: 55% (36/66). These are legitimate background "
                "statistics for our analysis — they come from a real peer-reviewed study.",
                "PMC statistics noted as legitimate background context: "
                f"energy hazard failures {PUMP_FAILURE_ENERGY_PCT}% (47/70 Class I recalls), "
                f"under-dose outcomes {PUMP_UNDERDOSE_PCT}% (36/66 cases). "
                "Source: PMC6524450. Will use for industry benchmarking in executive summary."
            ),
        ]
    )

    # Email 线程 — 含初始版本号错误（5.10.0 而非 5.10.1，Update 1 后修正）
    # 另含 "2014" 分发起始年的错误引用（Update 2 后修正为 2015-02-27）
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-03-30T08:00:00",
        [
            (
                "[Email angela_reyes → regulatory_team Wed Mar 30 08:00 EST 2026] "
                f"Subject: Ivenix LVP Recall — {IVENIX_RECALL_NUM} Initial Assessment. "
                f"Team — I've reviewed the SoftwareCPR posting on recall {IVENIX_RECALL_NUM}. "
                "Product code LVP-SW-0005. "
                "Initial email from our contact says the affected software version is 5.10.0. "
                "I'm also looking at distribution — one internal memo says Nimbus distribution "
                "started as early as 2014, but I'm not certain of the exact date. "
                "Can the RCA team verify both these data points?",
                f"Logged Angela's initial assessment. Two data points flagged for verification: "
                f"(1) Ivenix affected version: 5.10.0 per initial contact — this may be incomplete, "
                f"need to verify against official recall documentation; "
                f"(2) Nimbus distribution start: Angela's memo says 2014, but the FDA official "
                f"notice and MedTech Dive confirm {NIMBUS_DIST_START} — the 2014 reference "
                f"appears to be an error. Will confirm with primary sources."
            ),
            (
                "[Email kevin_liu → regulatory_team Wed Mar 30 09:30 EST 2026] "
                f"Re: Ivenix software version — I've reviewed the Manufacturing Chemist article "
                f"(https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion). "
                f"They clearly state software version 5.10.1 AND EARLIER are affected (product code "
                f"{IVENIX_PRODUCT_CODE}). The '5.10.0 only' statement from Angela's initial contact "
                f"was incomplete. The correct statement should be '5.10.1 and earlier'. "
                f"Also, AABB article confirms IMS update to {IVENIX_IMS_FIXED} and LVP to {IVENIX_FIXED_VER}. "
                f"Battery replacement threshold: {IVENIX_BATTERY_THRESHOLD}%.",
                f"Kevin confirms: affected version is {IVENIX_AFFECTED_VER} and earlier "
                f"(not just 5.10.0). Both Manufacturing Chemist and AABB confirm this. "
                f"Key corrections: affected_software_version = '{IVENIX_AFFECTED_VER} and earlier'; "
                f"fixed_version = {IVENIX_FIXED_VER}; IMS fixed = {IVENIX_IMS_FIXED}; "
                f"battery threshold = {IVENIX_BATTERY_THRESHOLD}%. "
                f"This will be applied when Update 1 is processed formally."
            ),
        ]
    )

    # Discord DM — 技术细节讨论：电池阈值、MDR 法规
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-03-31T14:00:00",
        [
            (
                "[Discord DM kevin_liu Thu Mar 31 14:00 EST 2026] "
                "Quick technical note on the Nimbus battery failures. The occlusion detection "
                "design spec was 300 mmHg threshold — field reports show the sensor was not "
                "reliably detecting partial occlusions below this level in clinical tubing "
                "configurations. This is a key root cause for the battery + occlusion combined "
                "failure modes. Also the sterile barrier issue is specific to the Nimbus II EpiD "
                "and EMS models — the standard Nimbus models had adequate barriers.",
                "Noted: occlusion sensor threshold 300 mmHg design spec — field failures below "
                "this threshold. Sterile barrier deficiency limited to Nimbus II EpiD and EMS. "
                "Will incorporate in fishbone analysis under Machine (occlusion_sensor) and "
                "Material (sterile_barrier) categories."
            ),
            (
                "[Discord DM kevin_liu Thu Mar 31 15:00 EST 2026] "
                "On the MDR regulatory requirements — just want to confirm for the compliance "
                f"section. Manufacturer MDR for death/serious injury: {MDR_30DAY_CFR} — "
                f"30 calendar days. Urgent/remedial events: {MDR_5DAY_CFR} — 5 work days. "
                f"Recall reports under 21 CFR Part 806: {RECALL_REPORT_DAYS} working days. "
                "These should be verbatim in the compliance checklist.",
                f"Confirmed verbatim regulatory citations: "
                f"MDR 30-day: {MDR_30DAY_CFR}; "
                f"MDR 5-day urgent: {MDR_5DAY_CFR}; "
                f"Recall report: {RECALL_REPORT_CFR} ({RECALL_REPORT_DAYS} working days). "
                "Will use these exact citations in all compliance documentation."
            ),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_feishu, "feishu"),
            (s_email, "email"),
            (s_discord, "discord"),
        ],
    }


# --------------------------------------------------------------------------- #
# 4. Updates（含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_feishu = sess_ids["history"][1][0]
    s_email = sess_ids["history"][2][0]

    # ----------------------------------------------------------------------- #
    # UPDATE 1（Q07 之后）：修订 FSN，明确 Ivenix 受影响版本为 5.10.1 and earlier
    # ----------------------------------------------------------------------- #
    u1_sess_dir = UPD / "upd1_sessions"
    u1_ws_dir = UPD / "upd1_workspace"

    # Feishu 群组 Update 1 session（新 session：飞书更新通知）
    s_feishu_upd1 = gen_session_id("feishu_fsn_revision", TID)
    sb_u1 = SessionBuilder(s_feishu_upd1, CWD, "2026-04-08T09:00:00", is_main=False)
    sb_u1.add_user(
        "[Feishu 群组「RCA 工作进展」angela_reyes Wed Apr 08 09:00 EST 2026] "
        "IMPORTANT UPDATE — REVISED FIELD SAFETY NOTICE: "
        "The Ivenix LVP Field Safety Notice has been revised. "
        "The affected software version description has been corrected: "
        "the correct statement is 'version 5.10.1 AND EARLIER' (not just '5.10.0'). "
        f"Recall Number {IVENIX_RECALL_NUM} is confirmed. "
        f"Product code: {IVENIX_PRODUCT_CODE}. "
        "All RCA outputs referencing Ivenix affected software version must use "
        "'5.10.1 and earlier' going forward. Prior references to '5.10.0 only' are incorrect. "
        "Revised FSN attached (cases/case_B_ivenix/field_safety_notice_revised_v2.md)."
    )
    sb_u1.add_assistant(
        f"ACKNOWLEDGED — Field Safety Notice revision noted. Effective immediately:\n"
        f"- Ivenix affected software version: '{IVENIX_AFFECTED_VER} and earlier' "
        f"(supersedes any prior '5.10.0 only' references)\n"
        f"- Recall Number: {IVENIX_RECALL_NUM} confirmed\n"
        f"- Product Code: {IVENIX_PRODUCT_CODE} confirmed\n"
        "All subsequent outputs will reflect this correction. Q07 output "
        "(ivenix_tech_summary_v1.md) reflects pre-update state and is now superseded."
    )
    sb_u1.write(u1_sess_dir / f"{s_feishu_upd1}.jsonl")

    # Update 1 workspace files
    w(u1_ws_dir / "field_safety_notice_revised_v2.md", f"""# REVISED Field Safety Notice — Fresenius Kabi Ivenix LVP Software
## Version 2.0 (REVISION — Supersedes All Prior Ivenix FSN Versions)

**REVISION NOTICE**: This document supersedes any prior communications regarding
Ivenix LVP software affected version scope. The affected version description
has been corrected.

---

## CRITICAL CORRECTION

**INCORRECT** (prior communications): "Affected software version: 5.10.0"
**CORRECT** (this revision): "Affected software version: **{IVENIX_AFFECTED_VER} and earlier**"

This means ALL Ivenix LVP software versions from the initial release through
{IVENIX_AFFECTED_VER} are affected, not only version 5.10.0.

---

## Updated Recall Summary

**Recall Number**: {IVENIX_RECALL_NUM}
**Product Code**: {IVENIX_PRODUCT_CODE}
**Affected Software Versions**: {IVENIX_AFFECTED_VER} and earlier
**Fixed Version**: {IVENIX_FIXED_VER}
**IMS Updated Version**: {IVENIX_IMS_FIXED}

---

## Anomaly 1: Battery State-of-Charge Reporting Error

**Root Cause**: The coulomb counting algorithm in versions {IVENIX_AFFECTED_VER} and
earlier does not compensate for battery impedance changes associated with aging.
Batteries with health below {IVENIX_BATTERY_THRESHOLD}% show the most severe reporting errors.

**Action Required**: Replace any battery with health < {IVENIX_BATTERY_THRESHOLD}%.
Install software update {IVENIX_FIXED_VER} and IMS {IVENIX_IMS_FIXED}.

---

## Anomaly 2: Dual-Zero Rate Entry Interface Freeze

**Root Cause**: Input validation gap in the rate-entry state machine allows
leading-zero numeric strings to bypass range validation, triggering an unhandled
parser exception that invokes fail-stop mode.

**Action Required**: Install software update {IVENIX_FIXED_VER}.

---

## Adverse Events (as of November 18, 2025)
- Serious Injuries: {IVENIX_INJURIES}
- Deaths: 0

---

## Implementation Guide (supplemental)

### Battery Health Assessment Protocol
1. Access device diagnostics menu.
2. Navigate to Battery Health > State of Charge.
3. Record battery health percentage.
4. If health < {IVENIX_BATTERY_THRESHOLD}%, schedule immediate battery replacement before software update.
5. If health >= {IVENIX_BATTERY_THRESHOLD}%, proceed directly to software update.

### Software Update Procedure
1. Connect device to IMS workstation.
2. Apply IMS update to v{IVENIX_IMS_FIXED} first.
3. Apply LVP software update to v{IVENIX_FIXED_VER}.
4. Verify update completion via device firmware version screen.
5. Run self-test sequence before returning device to clinical use.

### Dual-Zero Input Risk Avoidance (pre-update)
Clinician guidance: do not enter rates using leading zeros (e.g., use "10" not "0010").
Display "RATE ENTRY NOTE" reminder near pump in affected wards.

---

## Documentation

- Recall Number: {IVENIX_RECALL_NUM}
- FDA Enforcement Date: 2025-12-16
- Product Code: {IVENIX_PRODUCT_CODE}
- Distribution States: CA, CO, FL, GA, ID, IL, MD, MI, MN, MS, NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI
- Units (software correction kits): 30
  (Note: this figure represents the number of software correction kits distributed,
  not the total number of hardware LVP units in the field.)

**Sources**:
- https://www.softwarecpr.com/2025/12/fda-recall-software-anomalies-can-cause-serious-harm-or-death/
- https://www.aabb.org/news-resources/news/article/2026/03/04/regulatory-update--class-i-recall-issued-for-fresenius-kabi-ivenix-large-volume-pump-software
- https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion
""")

    # 生成额外填充文件（撑起 >35k tokens）
    _gen_update1_hospital_implementation_guide(u1_ws_dir)
    _gen_update1_technical_analysis(u1_ws_dir)
    _gen_update1_battery_assessment_csv(u1_ws_dir)
    _gen_update1_ivenix_field_data_csv(u1_ws_dir)

    # ----------------------------------------------------------------------- #
    # UPDATE 2（Q11 之后，含 Supersede）
    # ----------------------------------------------------------------------- #
    u2_sess_dir = UPD / "upd2_sessions"
    u2_ws_dir = UPD / "upd2_workspace"

    # Email Update 2 session（新 session：supersede 通知 + Nimbus 起始日修正 + 806 条文补充）
    s_email_upd2 = gen_session_id("email_update2_supersede", TID)
    sb_u2 = SessionBuilder(s_email_upd2, CWD, "2026-04-15T10:00:00", is_main=False)
    sb_u2.add_user(
        "[Email angela_reyes → rca_team Wed Apr 15 10:00 EST 2026] "
        "REGULATORY UPDATE — SUPERSEDE NOTICE: "
        "This email contains two important corrections that SUPERSEDE prior communications:\n\n"
        "CORRECTION 1 (SUPERSEDES Update 1 partial content): "
        "The '30 units' figure mentioned in the Ivenix FSN refers to SOFTWARE CORRECTION KITS "
        "distributed to facilities, NOT the number of hardware LVP units installed in the field. "
        "This number CANNOT be used to infer the number of software installations or affected pumps. "
        "Any RCA output that cites '30 units' as the count of affected LVP hardware units "
        "is INCORRECT. For the units_software_kits field in any structured output, use the "
        "value 'undisclosed' — the actual hardware installation count has not been publicly disclosed.\n\n"
        "CORRECTION 2: Nimbus distribution start date clarification: "
        "Some earlier team communications (including Angela's March 30 email) referenced "
        "a 2014 start date for Nimbus distribution. THIS IS INCORRECT. "
        f"The confirmed start date is {NIMBUS_DIST_START}, per FDA official notice and "
        "MedTech Dive (https://www.medtechdive.com/news/infutronix-nimbus-infusion-pump-recall-injuries-death/714391/). "
        "Any reference to 2014 or any other date is an error. "
        f"Use {NIMBUS_DIST_START} exclusively.\n\n"
        "ADDITIONAL ITEM: 21 CFR 806.10 confirmation — "
        f"The recall report window is {RECALL_REPORT_DAYS} WORKING DAYS from initiation. "
        "Our compliance documentation should cite this precisely.\n\n"
        "Please update all RCA outputs accordingly."
    )
    sb_u2.add_assistant(
        "ACKNOWLEDGED — Update 2 supersede notice processed:\n\n"
        "CORRECTION 1 (supersede): Ivenix 'units_software_kits' field correction applied. "
        "The value '30 units' referred to software correction kits, NOT hardware LVP units. "
        "Field value set to 'undisclosed' in all subsequent outputs. "
        "Q08 output (ivenix_recall_metadata.json) is now superseded; "
        "Q12 will produce the corrected ivenix_recall_metadata_v2.json.\n\n"
        f"CORRECTION 2: Nimbus distribution_start confirmed as {NIMBUS_DIST_START}. "
        "The 2014 reference in the March 30 email was an error. "
        "All RCA outputs will use 2015-02-27.\n\n"
        f"ADDITIONAL: 21 CFR 806.10 confirmed at {RECALL_REPORT_DAYS} working days. "
        "Compliance checklist updated.\n\n"
        "Update 2 supersede is applied. Awaiting next task."
    )
    sb_u2.write(u2_sess_dir / f"{s_email_upd2}.jsonl")

    # Update 2 workspace files
    _gen_update2_regulatory_guidance(u2_ws_dir)
    _gen_update2_capa_validation(u2_ws_dir)
    _gen_update2_distribution_verification(u2_ws_dir)
    _gen_update2_nimbus_complaint_analysis_csv(u2_ws_dir)
    _gen_update2_capa_tracking_extended(u2_ws_dir)

    # Update 声明
    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {
                    "name": f"{s_feishu_upd1}.jsonl",
                    "action": "new",
                    "target": f"{s_feishu_upd1}.jsonl",
                    "channel": "feishu",
                }
            ],
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {
                    "name": "field_safety_notice_revised_v2.md",
                    "action": "new",
                    "target": "cases/case_B_ivenix/field_safety_notice_revised_v2.md",
                },
                {
                    "name": "hospital_implementation_guide.md",
                    "action": "new",
                    "target": "cases/case_B_ivenix/hospital_implementation_guide.md",
                },
                {
                    "name": "technical_analysis_battery_soc.md",
                    "action": "new",
                    "target": "cases/case_B_ivenix/technical_analysis_battery_soc.md",
                },
                {
                    "name": "ivenix_battery_assessment_full.csv",
                    "action": "new",
                    "target": "cases/case_B_ivenix/ivenix_battery_assessment_full.csv",
                },
                {
                    "name": "ivenix_field_data_full.csv",
                    "action": "new",
                    "target": "cases/case_B_ivenix/ivenix_field_data_full.csv",
                },
            ],
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {
                    "name": f"{s_email_upd2}.jsonl",
                    "action": "new",
                    "target": f"{s_email_upd2}.jsonl",
                    "channel": "email",
                }
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {
                    "name": "regulatory_guidance_supplement.md",
                    "action": "new",
                    "target": "regulations/regulatory_guidance_supplement.md",
                },
                {
                    "name": "capa_validation_requirements.md",
                    "action": "new",
                    "target": "cases/case_B_ivenix/capa_validation_requirements.md",
                },
                {
                    "name": "nimbus_distribution_verification.md",
                    "action": "new",
                    "target": "cases/case_A_nimbus/nimbus_distribution_verification.md",
                },
                {
                    "name": "nimbus_complaint_analysis_extended.csv",
                    "action": "new",
                    "target": "cases/case_A_nimbus/nimbus_complaint_analysis_extended.csv",
                },
                {
                    "name": "capa_tracking_extended.csv",
                    "action": "new",
                    "target": "cases/capa_tracking_extended.csv",
                },
            ],
        },
    }

    return updates_decl, s_feishu_upd1, s_email_upd2


def _gen_update1_hospital_implementation_guide(base: Path) -> None:
    w(base / "hospital_implementation_guide.md", f"""# Hospital Implementation Guide
## Fresenius Kabi Ivenix LVP Software Recall {IVENIX_RECALL_NUM}
## Version 2.0 — Revised Following FSN Update

**Distribution**: All affected facilities in CA, CO, FL, GA, ID, IL, MD, MI, MN, MS,
NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI

---

## Phase 1: Immediate Assessment (Days 1-3)

### Step 1: Device Inventory
Locate all Ivenix LVP units in your facility. Check firmware version on each device.
Affected versions: **{IVENIX_AFFECTED_VER} and earlier**.
Note: The recall affects software version {IVENIX_AFFECTED_VER} AND ALL PRIOR VERSIONS.
An earlier communication from one source said only "5.10.0" was affected — this was
INCORRECT. The correct scope is "{IVENIX_AFFECTED_VER} and earlier".

### Step 2: Battery Health Assessment
For each affected device:
1. Navigate to Device Settings > Diagnostics > Battery Health
2. Record the battery health percentage
3. Flag all devices with battery health < {IVENIX_BATTERY_THRESHOLD}%
4. Segregate flagged devices from clinical use immediately

### Step 3: Risk Stratification
| Battery Health | Risk Level | Action |
|---------------|------------|--------|
| < {IVENIX_BATTERY_THRESHOLD}% | HIGH | Remove from service immediately; replace battery |
| {IVENIX_BATTERY_THRESHOLD}%-85% | MEDIUM | Schedule update within 48 hours |
| > 85% | LOWER | Schedule update within 5 business days |

---

## Phase 2: Software Update (Days 3-14)

### Update Sequence
**IMPORTANT**: Always update IMS first, then LVP software.

1. **IMS Update** — Update Infusion Management Software to v{IVENIX_IMS_FIXED}
   - Estimated time: 20-30 minutes per IMS workstation
   - Requires network downtime: No
   - Requires device connection: No (IMS update is server-side)

2. **LVP Software Update** — Update each pump to v{IVENIX_FIXED_VER}
   - Estimated time: 15-20 minutes per device
   - Requires device to be removed from active patient use
   - Verify completion: Check firmware version on device screen

3. **Battery Replacement** (if health < {IVENIX_BATTERY_THRESHOLD}%)
   - Order replacement batteries using part number [contact Fresenius Kabi]
   - Installation requires trained biomedical engineering staff
   - Post-replacement: verify battery health > {IVENIX_BATTERY_THRESHOLD}% before returning to service

---

## Phase 3: Verification and Documentation (Days 14-21)

### Post-Update Checklist
- [ ] All devices updated to v{IVENIX_FIXED_VER}
- [ ] IMS updated to v{IVENIX_IMS_FIXED}
- [ ] All batteries with health < {IVENIX_BATTERY_THRESHOLD}% replaced
- [ ] Post-update self-test run on all devices
- [ ] Staff re-education on dual-zero rate entry (historical awareness)
- [ ] Documentation of update completion submitted to Fresenius Kabi

### Adverse Event Reporting During Remediation
- Any patient harm events during the remediation period must be reported per {MDR_30DAY_CFR}
- Urgent events requiring immediate action: report per {MDR_5DAY_CFR} (5 work days)
- Recall correction report already filed by Fresenius Kabi per {RECALL_REPORT_CFR}

---

## Contact Information

**Fresenius Kabi Field Service**: 1-800-XXX-XXXX (24/7)
**Technical Support**: ivenix-support@fresenius-kabi.com
**FDA MedWatch Reporting**: https://www.fda.gov/safety/medwatch

**Recall Reference**: {IVENIX_RECALL_NUM}
**Product Code**: {IVENIX_PRODUCT_CODE}
""")


def _gen_update1_technical_analysis(base: Path) -> None:
    w(base / "technical_analysis_battery_soc.md", f"""# Technical Root Cause Analysis
## Ivenix LVP Battery State-of-Charge (SOC) Algorithm Defect
## Software Versions {IVENIX_AFFECTED_VER} and Earlier

**Document Reference**: IVX-TECH-RCA-2025-003
**Prepared by**: Fresenius Kabi Software Safety Engineering
**Review Status**: Final

---

## 1. Technical Background

### Battery Electrochemistry in LVP Devices

Lithium-ion batteries used in the Ivenix LVP system are rated for:
- Nominal capacity: 3,350 mAh at 25°C
- Voltage range: 3.0V (depleted) to 4.2V (fully charged)
- Design life: 300 charge cycles or 3 years, whichever comes first
- Health definition: Actual deliverable capacity / rated capacity × 100%

Batteries with health below {IVENIX_BATTERY_THRESHOLD}% show significantly altered
charge-discharge behavior that confounds coulomb counting algorithms.

### Coulomb Counting Algorithm (Defective Implementation)

The SOC algorithm in software version {IVENIX_AFFECTED_VER} and earlier used the following approach:

```python
# DEFECTIVE IMPLEMENTATION (v5.10.1 and earlier)
def calculate_soc(initial_charge_mah, current_mah, temperature_c):
    # NOTE: This does not account for battery aging / impedance changes
    soc = (current_mah / initial_charge_mah) * 100
    # Temperature compensation applied (correct)
    if temperature_c < 20:
        soc = soc * 0.97  # 3% correction for cold
    elif temperature_c > 35:
        soc = soc * 0.99  # 1% correction for heat
    return max(0, min(100, soc))
```

**Critical defect**: `initial_charge_mah` is set at manufacturing time and never updated
to reflect actual degraded battery capacity. As batteries age and capacity decreases,
the denominator remains the original rated capacity, causing SOC to be systematically
over-reported.

### Fixed Implementation (v{IVENIX_FIXED_VER})

```python
# CORRECTED IMPLEMENTATION (v5.10.2)
def calculate_soc(current_mah, temperature_c, battery_health_pct):
    # Use measured actual capacity, not rated capacity
    # battery_health_pct obtained from periodic cycle-count measurement
    actual_capacity_mah = 3350 * (battery_health_pct / 100)
    soc = (current_mah / actual_capacity_mah) * 100
    # Temperature compensation (unchanged)
    if temperature_c < 20:
        soc = soc * 0.97
    elif temperature_c > 35:
        soc = soc * 0.99
    return max(0, min(100, soc))
```

---

## 2. Failure Mode Analysis

### Observed Failure Signatures

| Battery Health | SOC Over-Report | Risk |
|---------------|----------------|------|
| 90-100% | < 5% error | Low |
| 80-89% | 5-15% error | Medium |
| 70-79% | 15-25% error | High |
| < {IVENIX_BATTERY_THRESHOLD}% | > 25% error | Critical |

A device with 60% battery health and 20% actual remaining charge may display 47% remaining,
causing the clinician and alarm system to believe there is adequate battery reserve when the
device is actually near shutdown threshold.

### Shutdown Event Timeline (Reconstructed from MDR Data)

```
Time 0:00  Device started, battery health = 58%, actual SOC = 22%
           Algorithm reports SOC = 37% (over-report)
           No low-battery alarm triggered (threshold: 10% reported SOC)

Time 0:45  Actual SOC drops to 8%
           Algorithm reports SOC = 14%
           No alarm (above 10% reported threshold)

Time 1:12  Actual SOC drops to 3%
           Algorithm reports SOC = 5%
           Low-battery alarm activates at 5% reported SOC — WARNING
           Clinician sees alarm but believes 5% reported charge
           Actual: already near complete depletion

Time 1:17  Device shuts down unexpectedly
           Patient mid-infusion — dose interrupted
           MDR event triggered
```

---

## 3. Verification and Validation Gap

### Root Cause of V&V Failure

The battery SOC algorithm was validated using:
- New batteries (100% health) at 3 temperatures (15°C, 25°C, 35°C)
- 50 charge-discharge cycles (represents ~6 months of use)
- Accuracy criterion: SOC within ±5% of reference measurement

**Gap identified**: The 50-cycle test represents only 17% of the rated 300-cycle life.
Batteries showing significant impedance changes (typically after 150+ cycles, health < 80%)
were NOT included in the V&V test matrix.

### Corrective V&V Protocol (Preventive CAPA)

Updated protocol (CAPA-006) requires:
- Battery health test matrix: 100%, 90%, 80%, 70%, 60%, 50%
- Cycle count test matrix: 0, 50, 100, 150, 200, 250, 300 cycles
- Temperature matrix: 10°C, 20°C, 25°C, 30°C, 40°C
- Accuracy criterion: SOC within ±3% across all health/cycle/temperature combinations

---

## 4. Dual-Zero Rate Entry Defect (Supplemental)

### Input State Machine Error

The rate entry state machine in versions {IVENIX_AFFECTED_VER} and earlier:

```
State: IDLE
  User presses: [0] → State: FIRST_DIGIT
  User presses: [0] → State: SECOND_DIGIT (leading zero)
  User presses: [1] → State: THIRD_DIGIT
  User presses: [0] → State: FOURTH_DIGIT
    Value buffer: "0010"
  User presses: [OK] or [BACK]
    DEFECT: Parser calls int("0010") in strict mode
    Python-style leading-zero check raises ValueError
    Exception handler: triggers fail-stop state
    UI FROZEN — requires power cycle
```

**Fix in v{IVENIX_FIXED_VER}**: Input pre-processor strips leading zeros before parsing.
Leading-zero inputs now correctly resolve to their numeric value.

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2025-11-14 | Software Safety Eng | Initial draft |
| 2.0 | 2025-12-16 | Software Safety Eng | Final (post-remediation) |
""")


def _gen_update2_regulatory_guidance(base: Path) -> None:
    w(base / "regulatory_guidance_supplement.md", f"""# Regulatory Guidance Supplement — Update 2
## MedSafe RCA Team — Compliance Documentation

**Purpose**: This document supplements the existing regulations/ folder content with
additional clarifications issued in conjunction with Update 2.

---

## 1. 21 CFR 806.10 — Correction/Removal Reporting Window

**Confirmed**: The reporting window under {RECALL_REPORT_CFR} is **{RECALL_REPORT_DAYS} WORKING DAYS**
from the date of initiating the correction or removal action.

This {RECALL_REPORT_DAYS}-working-day requirement is WORKING DAYS, not calendar days.
Compare with 21 CFR 803.50(a)(1) which uses CALENDAR DAYS for MDR reporting.

| Requirement | Timeframe | Type of Days | Citation |
|-------------|-----------|-------------|---------|
| MDR death/serious injury | 30 days | Calendar days | {MDR_30DAY_CFR} |
| MDR urgent/remedial action | 5 days | Work days | {MDR_5DAY_CFR} |
| Recall/correction report | {RECALL_REPORT_DAYS} days | Working days | {RECALL_REPORT_CFR} |

---

## 2. Ivenix "30 Units" Figure — CLARIFICATION (SUPERSEDES Update 1 Partial Content)

**CORRECTION**: The "30 units" figure in the Ivenix LVP recall documentation refers to
**30 software correction kits** distributed to health care facilities. This is NOT the
number of hardware Ivenix LVP devices installed in the field.

**What "30 units" DOES mean**: Fresenius Kabi shipped 30 software correction kit packages
to facilities in the 20 affected states. Each package may support multiple device updates.

**What "30 units" DOES NOT mean**: The total number of Ivenix LVP hardware units
currently in clinical use. This number is not publicly disclosed.

**Impact on RCA outputs**: Any structured output field (such as `units_software_kits`)
that previously showed or would show "30" as the affected hardware count is INCORRECT.
The correct value for this field should be set to **"undisclosed"**.

This correction SUPERSEDES any implication in Update 1 materials that "30" represents
the count of affected hardware units.

---

## 3. Nimbus Distribution Start Date — Final Confirmation

**Confirmed**: The Nimbus distribution start date is **{NIMBUS_DIST_START}**.

Source: FDA Official Recall Notice; MedTech Dive
(https://www.medtechdive.com/news/infutronix-nimbus-infusion-pump-recall-injuries-death/714391/)

**INCORRECT DATE**: Some internal communications (including a March 30 email and
certain session notes) referenced "2014" as the Nimbus distribution start year.
This was an error. The correct date is {NIMBUS_DIST_START}.

Any RCA output showing a Nimbus distribution start in 2014 or any other year besides
2015 is incorrect and must be corrected.

---

## 4. Updated Compliance Checklist Items

The following items must be included in the final compliance checklist:

| ID | Description | CFR Citation | Deadline |
|----|-------------|-------------|---------|
| MDR-30DAY | Report all Nimbus death/serious injury events | {MDR_30DAY_CFR} | 30 calendar days from awareness |
| MDR-5DAY | Expedited reporting for urgent/remedial events | {MDR_5DAY_CFR} | 5 work days from awareness |
| RECALL-REPORT | File correction/removal report with FDA | {RECALL_REPORT_CFR} | {RECALL_REPORT_DAYS} working days from initiation |
| IVENIX-SOFTWARE | Confirm Ivenix software update compliance | — | Per recall action plan |
""")


def _gen_update2_capa_validation(base: Path) -> None:
    w(base / "capa_validation_requirements.md", f"""# CAPA Validation Requirements — Update 2 Supplement
## MedSafe RCA Team — Ivenix LVP Cases

**Document Reference**: CAPA-VALID-2026-001
**Issued**: April 2026 (Update 2)

---

## Purpose

This document establishes the validation requirements for confirming CAPA effectiveness
following the Ivenix LVP software recall ({IVENIX_RECALL_NUM}).

---

## CAPA Validation Matrix

### CAPA-004 & CAPA-005: LVP Software Update v{IVENIX_FIXED_VER}

| Test ID | Scenario | Expected Result | Status |
|---------|----------|----------------|--------|
| TV-001 | Battery health 100%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-002 | Battery health 80%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-003 | Battery health {IVENIX_BATTERY_THRESHOLD}%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-004 | Battery health 60%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-005 | Battery health 50%, SOC at 20% | SOC reported within ±3% | Passed |
| TV-006 | Rate entry "0010" → OK | Rate set to 10.0 mL/hr, no freeze | Passed |
| TV-007 | Rate entry "0010" → BACK | Returns to prior screen, no freeze | Passed |
| TV-008 | Rate entry "00" → OK | Rate invalid: prompt re-entry | Passed |
| TV-009 | Low battery alarm at 20% actual SOC | Alarm triggered at ≤20% | Passed |
| TV-010 | Aged battery (250 cycles) SOC accuracy | SOC within ±3% | Passed |

**CAPA-004 and CAPA-005 validation: COMPLETE**

---

### CAPA-006: V&V Protocol Revision

| Deliverable | Status |
|-------------|--------|
| Aged battery test matrix (50-300 cycles) | In Progress |
| Temperature × cycle × health matrix | In Progress |
| Leading-zero input boundary test cases | Complete |
| V&V protocol formal review | Pending |

**CAPA-006 target completion**: Q1 2026

---

## Battery Replacement Effectiveness (CAPA-004 supplemental)

Facilities that replaced batteries with health < {IVENIX_BATTERY_THRESHOLD}% report:
- Zero unexpected shutdowns post-replacement
- SOC accuracy within ±3% confirmed in post-service audits
- Patient safety incidents: 0 reported post-update

---

## Ivenix CAPA Summary

| CAPA | Description | Validation Status |
|------|-------------|-----------------|
| CAPA-004 | LVP software update v{IVENIX_FIXED_VER} | COMPLETE |
| CAPA-005 | LVP software update v{IVENIX_FIXED_VER} (input fix) | COMPLETE |
| CAPA-006 | V&V protocol revision | IN PROGRESS |

*Note on "30 units software kits": As clarified in Update 2, this figure represents
software correction kits distributed, NOT hardware LVP units. The total hardware
installation count for effectiveness measurement is tracked separately by Fresenius
Kabi's field service team and is not publicly disclosed.*
""")


def _gen_update2_distribution_verification(base: Path) -> None:
    w(base / "nimbus_distribution_verification.md", f"""# Nimbus Distribution Data Verification Report
## Case A: InfuTronix Nimbus/Nimbus II

**Document Reference**: NIM-DISTRIB-VERIF-2026-001
**Issued**: April 2026 (Update 2)
**Purpose**: Resolve discrepancy in Nimbus distribution start date references

---

## Background: Date Discrepancy

Multiple sources were consulted for the Nimbus distribution timeline. A discrepancy
was identified in early internal team communications, where one email referenced "2014"
as the distribution start year. This required formal verification.

---

## Source Review

### Primary Sources Consulted

| Source | URL | Stated Distribution Start |
|--------|-----|--------------------------|
| FDA Official Recall Notice | https://www.fda.gov/medical-devices/medical-device-recalls/infutronix-llc-recalls-nimbus-and-nimbus-ii-infusion-pump-systems-multiple-device-failures-may-cause | {NIMBUS_DIST_START} |
| MedTech Dive | https://www.medtechdive.com/news/infutronix-nimbus-infusion-pump-recall-injuries-death/714391/ | {NIMBUS_DIST_START} |
| HPN Online | https://www.hpnonline.com/surgical-critical-care/news/55036575/infutronix-recalls-52328-infusion-pump-systems-due-to-multiple-potential-failure-modes | {NIMBUS_DIST_START} |
| Drug Delivery Business | https://www.drugdeliverybusiness.com/fda-infutronix-infusion-pump-recall-1-death/ | {NIMBUS_DIST_START} |
| Internal team email (March 30) | — | "2014" ← INCORRECT |

### Verdict

**Confirmed distribution start date**: **{NIMBUS_DIST_START}**

All four primary sources (FDA notice, MedTech Dive, HPN Online, Drug Delivery Business)
consistently report {NIMBUS_DIST_START}. The "2014" reference in Angela's March 30 email
appears to have originated from an internal draft memo that was not verified against
primary FDA records before being circulated.

---

## Full Distribution Timeline (Confirmed)

| Data Point | Value | Source |
|-----------|-------|--------|
| Distribution start | **{NIMBUS_DIST_START}** | FDA, MedTech Dive, HPN Online |
| Distribution end | {NIMBUS_DIST_END} | MedTech Dive |
| Recall initiation | February 2024 | FDA |
| FDA notice posted | April 25, 2024 | FDA |
| Support cutoff | {NIMBUS_SUPPORT_CUTOFF} | Drug Delivery Business, MedTech Dive |
| Units affected | {NIMBUS_UNITS:,} | HPN Online |

---

## Distribution Duration Analysis

- Total distribution period: {NIMBUS_DIST_START} to {NIMBUS_DIST_END}
- Duration: approximately 9 years (108 months)
- First units potentially reaching end-of-life during recall: those distributed in 2015-2016

## Conflict Resolution Log

| Session | Claimed Value | Correct Value | Resolution |
|---------|-------------|--------------|-----------|
| Email (Angela, Mar 30) | "2014 distribution start" | {NIMBUS_DIST_START} | Corrected per FDA notice |
| Feishu sess-02 | Not specified | {NIMBUS_DIST_START} | Consistent |
| Slack sess-01 | {NIMBUS_DIST_START} | {NIMBUS_DIST_START} | Confirmed |

**Final determination**: All subsequent RCA outputs must use **{NIMBUS_DIST_START}**
as the Nimbus distribution start date. The 2014 reference is hereby formally superseded.
""")


def _gen_update1_battery_assessment_csv(base: Path) -> None:
    """生成 Ivenix 电池健康评估全量 CSV（~200 行；约 3k tokens）。"""
    rng = random.Random(20251201)
    states = ["CA", "CO", "FL", "GA", "ID", "IL", "MD", "MI", "MN", "MS",
              "NE", "NJ", "NV", "OK", "OR", "SC", "TX", "VA", "WA", "WI"]
    facility_types = ["Hospital-Academic", "Hospital-Community", "Long-Term-Care",
                      "Home-Health", "Outpatient-Infusion"]
    rows = [["assessment_id", "facility_id", "facility_type", "state",
             "device_serial", "software_version", "battery_health_pct",
             "battery_cycles", "last_service_date", "assessment_date",
             "risk_category", "action_required", "update_completed",
             "battery_replaced", "post_update_version", "notes"]]
    for i in range(1, 201):
        state = rng.choice(states)
        ftype = rng.choice(facility_types)
        fac_id = f"FAC-{state}-{rng.randint(100, 999)}"
        dev_ser = f"IVX-{rng.randint(100000, 999999)}"
        # Software version distribution: most on 5.10.1 or earlier
        sw_ver = rng.choices(
            ["5.10.1", "5.10.0", "5.9.3", "5.9.2", "5.10.2"],
            weights=[40, 30, 15, 10, 5]
        )[0]
        health = round(rng.uniform(45, 100), 1)
        cycles = rng.randint(10, 320)
        # Last service date
        svc_month = rng.randint(1, 12)
        svc_year = rng.choice([2023, 2024, 2025])
        last_svc = f"{svc_year}-{svc_month:02d}-{rng.randint(1, 28):02d}"
        asm_date = f"2025-{rng.randint(11, 12):02d}-{rng.randint(1, 28):02d}"
        # Risk category
        if health < IVENIX_BATTERY_THRESHOLD:
            risk = "HIGH"
            action = "REPLACE_BATTERY_THEN_UPDATE"
        elif health < 80:
            risk = "MEDIUM"
            action = "UPDATE_SOFTWARE_PRIORITY"
        else:
            risk = "LOW"
            action = "UPDATE_SOFTWARE_ROUTINE"
        # Post-update status
        if sw_ver == "5.10.2":
            updated = "YES"
            batt_repl = "NO" if health >= IVENIX_BATTERY_THRESHOLD else "YES"
            post_ver = "5.10.2"
        else:
            updated = rng.choice(["YES", "YES", "YES", "NO"])
            batt_repl = "YES" if health < IVENIX_BATTERY_THRESHOLD and updated == "YES" else "NO"
            post_ver = "5.10.2" if updated == "YES" else "PENDING"
        notes = (
            f"Battery health {health}%; "
            f"{cycles} cycles; "
            f"Recall {IVENIX_RECALL_NUM}; "
            f"Product {IVENIX_PRODUCT_CODE}"
        )
        rows.append([
            f"ASMNT-{i:05d}", fac_id, ftype, state, dev_ser, sw_ver,
            health, cycles, last_svc, asm_date, risk, action, updated,
            batt_repl, post_ver, notes
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(base / "ivenix_battery_assessment_full.csv", buf.getvalue())


def _gen_update1_ivenix_field_data_csv(base: Path) -> None:
    """生成 Ivenix 现场数据记录 CSV（~300 行；约 5k tokens）。"""
    rng = random.Random(20251115)
    events = ["battery_soc_error", "unexpected_shutdown", "ui_freeze_dual_zero",
              "alarm_failure", "rate_deviation", "normal_operation"]
    event_weights = [25, 20, 15, 10, 5, 25]
    rows = [["record_id", "facility_id", "state", "device_serial", "sw_version",
             "event_date", "event_type", "battery_health_at_event",
             "reported_soc_pct", "actual_soc_pct", "rate_programmed_mlhr",
             "rate_actual_mlhr", "patient_impact", "mdr_submitted",
             "cfr_basis", "corrective_action_taken"]]
    for i in range(1, 301):
        state = rng.choice(["CA", "TX", "FL", "IL", "MI", "GA", "VA", "WA"])
        fac = f"FAC-{state}-{rng.randint(100, 999)}"
        dev_ser = f"IVX-{rng.randint(100000, 999999)}"
        sw_ver = rng.choices(
            ["5.10.1", "5.10.0", "5.9.3"],
            weights=[50, 30, 20]
        )[0]
        ev_month = rng.randint(1, 12)
        ev_day = rng.randint(1, 28)
        ev_date = f"2025-{ev_month:02d}-{ev_day:02d}"
        event = rng.choices(events, weights=event_weights)[0]
        batt_health = round(rng.uniform(45, 100), 1)
        if event == "battery_soc_error":
            rep_soc = round(batt_health + rng.uniform(10, 35), 1)
            act_soc = round(batt_health - rng.uniform(5, 25), 1)
        elif event == "unexpected_shutdown":
            rep_soc = round(rng.uniform(5, 20), 1)
            act_soc = round(rep_soc - rng.uniform(5, 15), 1)
        else:
            rep_soc = round(batt_health, 1)
            act_soc = rep_soc
        rate_prog = rng.choice([5.0, 10.0, 25.0, 50.0, 100.0, 125.0])
        if event == "rate_deviation":
            rate_act = round(rate_prog * rng.uniform(0.85, 1.15), 1)
        elif event == "ui_freeze_dual_zero":
            rate_act = 0.0  # UI frozen
        else:
            rate_act = rate_prog
        impact = rng.choice(["no_harm", "therapy_delay", "near_miss", "injury"])
        mdr = "Y" if impact in ("injury",) else rng.choice(["Y", "N", "N"])
        cfr = "21 CFR 803.50(a)(1)" if mdr == "Y" else "N/A"
        action = (
            f"Software updated to {IVENIX_FIXED_VER}" if event != "normal_operation"
            else "No action required"
        )
        rows.append([
            f"REC-{i:05d}", fac, state, dev_ser, sw_ver, ev_date, event,
            batt_health, min(rep_soc, 100), max(act_soc, 0),
            rate_prog, rate_act, impact, mdr, cfr, action
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(base / "ivenix_field_data_full.csv", buf.getvalue())


def _gen_update2_nimbus_complaint_analysis_csv(base: Path) -> None:
    """生成 Nimbus 投诉深度分析 CSV（~370 行，按失效模式 1/10 比例采样；约 8k tokens）。"""
    rng = random.Random(20240601)
    # 1/10 采样，保持比例
    failure_modes = [
        ("battery_failure", 103),
        ("occlusion_upstream", 75),
        ("system_error", 61),
        ("flow_rate_high", 49),
        ("flow_rate_low", 42),
        ("drug_leakage", 25),
        ("housing_damage", 15),
    ]
    models = ["Nimbus-Admin", "Nimbus-Flex", "Nimbus-PainPro",
              "Nimbus-II-PainPRO", "Nimbus-II-Flex", "Nimbus-II-Plus",
              "Nimbus-II-EpiD", "Nimbus-II-EMS"]
    care_settings = ["ICU", "General-Ward", "Home-Health", "Post-Op", "Oncology"]
    medications = ["heparin", "insulin", "morphine", "vancomycin", "dopamine",
                   "norepinephrine", "TPN", "chemotherapy", "antibiotics"]
    outcomes = ["no_harm", "near_miss", "therapy_interruption",
                "overdose", "underdose", "serious_injury", "death"]
    out_weights = [0.55, 0.15, 0.12, 0.04, 0.08, 0.055, 0.005]

    rows = [["analysis_id", "complaint_id", "date", "year", "quarter",
             "model", "lot", "failure_mode", "care_setting", "medication",
             "battery_health_at_failure", "occlusion_pressure_mmhg",
             "flow_rate_deviation_pct", "outcome", "hospitalization",
             "mdr_submitted", "mdr_report_number",
             "distribution_start_ref", "distribution_end_ref",
             "investigator_notes"]]

    complaint_id = 10001
    analysis_id = 1
    for fm, count in failure_modes:
        for _ in range(count):
            year = rng.choice([2019, 2020, 2021, 2022, 2023, 2024])
            q = rng.randint(1, 4)
            month = (q - 1) * 3 + rng.randint(1, 3)
            day = rng.randint(1, 28)
            date = f"{year}-{month:02d}-{day:02d}"
            model = rng.choice(models)
            lot = f"LOT-{rng.randint(1000, 9999)}-{year}"
            setting = rng.choice(care_settings)
            med = rng.choice(medications)
            batt = round(rng.uniform(40, 100), 1)
            occ_p = rng.choice([150, 200, 250, 280, 300, 350]) if fm == "occlusion_upstream" else 0
            dev_pct = round(rng.uniform(5, 18) * rng.choice([-1, 1]), 2) if "flow_rate" in fm else 0.0
            outcome = rng.choices(outcomes, weights=out_weights)[0]
            hosp = "Y" if outcome in ("serious_injury", "death", "overdose") else "N"
            mdr = "Y" if outcome in ("serious_injury", "death") else rng.choice(["Y", "N"])
            mdr_num = f"MW{20200000 + analysis_id:08d}" if mdr == "Y" else ""
            notes = (
                f"Distribution confirmed {NIMBUS_DIST_START} to {NIMBUS_DIST_END}; "
                f"Recall class {NIMBUS_RECALL_CLASS}; "
                f"UDI {NIMBUS_UDI_MAIN}; "
                f"Units recalled {NIMBUS_UNITS}"
            )
            rows.append([
                f"ANA-{analysis_id:06d}", f"CMP-{complaint_id}",
                date, year, f"Q{q}", model, lot, fm,
                setting, med, batt, occ_p, dev_pct, outcome, hosp,
                mdr, mdr_num, NIMBUS_DIST_START, NIMBUS_DIST_END, notes
            ])
            complaint_id += 1
            analysis_id += 1

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(base / "nimbus_complaint_analysis_extended.csv", buf.getvalue())


def _gen_update2_capa_tracking_extended(base: Path) -> None:
    """生成 CAPA 追踪扩展 CSV（~100 行；约 3k tokens）。"""
    rng = random.Random(20260401)
    cases = ["Case-A-Nimbus", "Case-B-Ivenix"]
    categories = ["Corrective", "Preventive"]
    statuses = ["Open", "In-Progress", "Complete", "Verified"]
    priorities = ["Critical", "High", "Medium", "Low"]
    owners = ["Software-Team", "Hardware-Team", "Quality", "Regulatory",
              "Field-Service", "Manufacturing", "V&V-Team"]
    rows = [["capa_id", "case", "source", "root_cause", "category",
             "description", "owner", "priority", "open_date", "due_date",
             "status", "cfr_reference", "verification_method",
             "closure_date", "effectiveness_confirmed",
             "ivenix_software_version_reference",
             "nimbus_distribution_start_reference", "notes"]]
    for i in range(1, 101):
        case = rng.choice(cases)
        cat = rng.choice(categories)
        status = rng.choices(statuses, weights=[20, 35, 30, 15])[0]
        prio = rng.choices(priorities, weights=[25, 35, 30, 10])[0]
        owner = rng.choice(owners)
        month_open = rng.randint(1, 4)
        open_date = f"2026-{month_open:02d}-{rng.randint(1, 28):02d}"
        due_month = month_open + rng.randint(1, 6)
        if due_month > 12:
            due_month = 12
        due_date = f"2026-{due_month:02d}-{rng.randint(1, 28):02d}"
        closure = due_date if status == "Verified" else ""
        cfr = rng.choice([
            "21 CFR 820.100", "21 CFR 803.50(a)(1)",
            "21 CFR 806.10", "21 CFR 820.30",
        ])
        if case == "Case-B-Ivenix":
            sw_ref = f"{IVENIX_AFFECTED_VER} → {IVENIX_FIXED_VER}"
        else:
            sw_ref = "N/A"
        dist_ref = NIMBUS_DIST_START if case == "Case-A-Nimbus" else "N/A"
        eff = "YES" if status == "Verified" else "PENDING"
        desc_templates = [
            f"Redesign {rng.choice(['algorithm', 'circuit', 'firmware', 'process'])} component",
            f"Revise {rng.choice(['V&V protocol', 'design review', 'test matrix', 'specification'])}",
            f"Update {rng.choice(['documentation', 'training materials', 'SOPs', 'checklists'])}",
            f"Implement {rng.choice(['monitoring', 'audit trail', 'inspection procedure', 'escalation pathway'])}",
        ]
        desc = rng.choice(desc_templates)
        root_choices = {
            "Case-A-Nimbus": ["battery_bms_design", "occlusion_threshold", "sterile_barrier"],
            "Case-B-Ivenix": ["soc_algorithm_defect", "input_validation_gap", "vv_protocol_gap"],
        }
        root = rng.choice(root_choices[case])
        rows.append([
            f"CAPA-{i:04d}", case, f"Recall-2024-{case}", root,
            cat, desc, owner, prio, open_date, due_date,
            status, cfr, "Bench-test or audit review",
            closure, eff, sw_ref, dist_ref,
            f"Recall {IVENIX_RECALL_NUM if 'Ivenix' in case else 'Nimbus-2024'}; units {NIMBUS_UNITS if 'Nimbus' in case else IVENIX_INJURIES}"
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(base / "capa_tracking_extended.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    print(f"[{TID}] Building workspace...")
    gen_system_files()
    gen_case_A_nimbus()
    gen_case_B_ivenix()
    gen_case_C_synchromed()
    gen_regulations()
    gen_templates()
    gen_sessions_honeypot()
    gen_scripts_workspace()

    print(f"[{TID}] Building sessions...")
    sess_ids = gen_sessions()

    print(f"[{TID}] Building updates...")
    updates_decl, s_feishu_upd1, s_email_upd2 = gen_updates(sess_ids)

    # 体量报告
    ws_tokens = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    sess_tokens = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tokens = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )

    # 各 update 分别统计
    upd1_tokens = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_sessions").rglob("*") if p.is_file()
    ) + sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_workspace").rglob("*") if p.is_file()
    )
    upd2_tokens = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_sessions").rglob("*") if p.is_file()
    ) + sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_workspace").rglob("*") if p.is_file()
    )

    print(f"[{TID}] workspace tokens ~{ws_tokens:,}")
    print(f"[{TID}] sessions tokens ~{sess_tokens:,}")
    print(f"[{TID}] update-1 tokens ~{upd1_tokens:,}")
    print(f"[{TID}] update-2 tokens ~{upd2_tokens:,}")
    print(f"[{TID}] total updates tokens ~{upd_tokens:,}")

    # 注册元数据
    desc = (
        "Medical device safety incident Root Cause Analysis (RCA) — "
        "17 exec_check rounds, 2 updates (incl. Ivenix software-version supersede), "
        "5 preference rules P1-P5, difficulty vectors V1/V2/V3/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: InfuTronix Nimbus Class I recall "
        "(https://www.fda.gov/medical-devices/medical-device-recalls/infutronix-llc-recalls-nimbus-and-nimbus-ii-infusion-pump-systems-multiple-device-failures-may-cause); "
        "Fresenius Kabi Ivenix LVP recall Z-0885-2026 "
        "(https://www.softwarecpr.com/2025/12/fda-recall-software-anomalies-can-cause-serious-harm-or-death/); "
        "21 CFR Part 803/806 regulatory requirements "
        "(https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803)."
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"] + [
            (s_feishu_upd1, "feishu"),
            (s_email_upd2, "email"),
        ],
        updates=updates_decl,
    )

    print(f"[{TID}] _register.json written.")
    print(f"[{TID}] built at {DATASET}")


if __name__ == "__main__":
    main()
