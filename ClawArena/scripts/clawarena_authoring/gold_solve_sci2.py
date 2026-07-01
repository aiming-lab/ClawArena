#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sci2.py — sci2 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的正确产物，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再用 >= 4 个反例（错误产物）断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_sci2.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sci2"
UPD = DS / "openclaw" / "updates" / "sci2"
SCRIPTS = DS / "eval" / "sci2" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sci2_gold_ws")

# 真实锚点
NIMBUS_UNITS = 52328
NIMBUS_COMPLAINTS = 3698
NIMBUS_INJURIES = 6
NIMBUS_DEATHS = 1
NIMBUS_DIST_START = "2015-02-27"
NIMBUS_DIST_END = "2024-02-29"
NIMBUS_SUPPORT_CUTOFF = "2024-06-20"
NIMBUS_UDI_MAIN = "00817170020000"

IVENIX_RECALL_NUM = "Z-0885-2026"
IVENIX_AFFECTED_VER = "5.10.1"
IVENIX_FIXED_VER = "5.10.2"
IVENIX_IMS_FIXED = "5.2.2"
IVENIX_PRODUCT_CODE = "LVP-SW-0005"
IVENIX_INJURIES = 2
IVENIX_BATTERY_THRESHOLD = 70

MDR_30DAY_CFR = "21 CFR 803.50(a)(1)"
MDR_5DAY_CFR = "21 CFR 803.53"
RECALL_REPORT_CFR = "21 CFR 806.10"
RECALL_REPORT_DAYS = 10


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 update workspace 文件
    for name, target in [
        ("field_safety_notice_revised_v2.md", "cases/case_B_ivenix/field_safety_notice_revised_v2.md"),
        ("hospital_implementation_guide.md", "cases/case_B_ivenix/hospital_implementation_guide.md"),
        ("technical_analysis_battery_soc.md", "cases/case_B_ivenix/technical_analysis_battery_soc.md"),
    ]:
        src = UPD / "upd1_workspace" / name
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    for name, target in [
        ("regulatory_guidance_supplement.md", "regulations/regulatory_guidance_supplement.md"),
        ("capa_validation_requirements.md", "cases/case_B_ivenix/capa_validation_requirements.md"),
        ("nimbus_distribution_verification.md", "cases/case_A_nimbus/nimbus_distribution_verification.md"),
    ]:
        src = UPD / "upd2_workspace" / name
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
    return GOLD


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def solve(ws: Path) -> None:
    out = ws / "rca_outputs"
    out.mkdir(exist_ok=True)

    # -------- Q1: Nimbus recall metadata --------
    _wj(out / "nimbus_recall_metadata.json", {
        "manufacturer": "InfuTronix, LLC",
        "recall_class": "Class I",
        "units_recalled": NIMBUS_UNITS,
        "complaints": NIMBUS_COMPLAINTS,
        "serious_injuries": NIMBUS_INJURIES,
        "deaths": NIMBUS_DEATHS,
        "distribution_start": NIMBUS_DIST_START,
        "distribution_end": NIMBUS_DIST_END,
        "support_cutoff": NIMBUS_SUPPORT_CUTOFF,
        "udi_main": NIMBUS_UDI_MAIN,
    })

    # -------- Q2: HONEYPOT flags --------
    _wj(out / "honeypot_flags.json", {
        "flagged_errors": [
            {
                "field": "ivenix_injuries",
                "honeypot_value": "5",
                "correct_value": "2",
                "evidence_source": "Manufacturing Chemist (S7): 2 serious injuries as of Nov 18 2025",
            },
            {
                "field": "nimbus_support_cutoff",
                "honeypot_value": "2024-08-31",
                "correct_value": "2024-06-20",
                "evidence_source": "Drug Delivery Business (S4): support deadline June 20 2024",
            },
        ]
    })

    # -------- Q3: 5-Why analysis (加难: wordcount>=600, BMS mention, >=3 Why rows) --------
    _w(out / "nimbus_5why.md", """# Nimbus Infusion Pump Recall — 5-Why Root Cause Analysis

## Overview

This 5-Why analysis addresses the primary failure modes identified in the InfuTronix
Nimbus/Nimbus II recall (Class I, 2024): Battery Management System (BMS) circuit design flaw
leading to battery failure, occlusion detection failure due to an inadequate algorithm threshold,
and sterile barrier deficiency in specific device configurations. Each root cause chain is
presented in Markdown table format per team preference P1, satisfying the minimum 600-word
requirement for regulatory submission documentation.

---

## Chain 1: Battery Management System (BMS) Failure

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why did patients experience unexpected pump shutdowns during infusion? | The battery depleted below minimum operating voltage during active infusion therapy |
| Why 2 | Why did the battery deplete without adequate warning? | The Battery Management System (BMS) failed to trigger the low-battery alarm at the correct threshold because the state-of-charge was misreported |
| Why 3 | Why did the BMS misreport state-of-charge? | The BMS circuit's battery capacity measurement algorithm did not account for Li-ion cell aging and cumulative impedance change — coulomb counting offset accumulated over charge-discharge cycles |
| Why 4 | Why was Li-ion aging not incorporated in the BMS circuit design? | The BMS design specification did not include aged-battery scenarios in the hardware validation test matrix — only fresh batteries were used in V&V testing |
| Why 5 | Why was the design validation protocol incomplete? | Root cause: **BMS circuit design flaw** — the design requirements specification failed to mandate Li-ion battery aging simulation, leaving the algorithm unvalidated for aged-cell conditions typical of long-term medical device use |

**Root Cause 1**: Battery Management System (BMS) circuit design deficiency — the BMS
circuit specification and design validation did not account for Li-ion battery aging behavior
across the device lifecycle. This resulted in premature battery depletion without appropriate
alarm triggering, leading to unexpected device shutdown during active patient infusion therapy.

---

## Chain 2: Occlusion Detection Failure

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why did partial upstream occlusions go undetected by the device? | The occlusion sensor alarm threshold was set at 300 mmHg — below this pressure, no alarm triggered even with clinically significant occlusions |
| Why 2 | Why was the 300 mmHg threshold insufficient for clinical use? | Clinical tubing configurations create partial occlusions at pressures below 300 mmHg that are nonetheless clinically significant and can cause drug delivery failure |
| Why 3 | Why was the 300 mmHg threshold selected without accounting for clinical partial occlusions? | Design analysis was conducted using standard bench test tubing only, not representative clinical tubing configurations from real-world use environments |
| Why 4 | Why were clinical tubing configurations not included in design analysis? | The use-related risk analysis (per IEC 62366) did not enumerate the full range of clinical tubing setups, leaving key partial occlusion scenarios unvalidated |
| Why 5 | Why was the use-related risk analysis incomplete for this scenario? | Root cause: **Occlusion detection algorithm validation gap** — insufficient representation of clinical use conditions in the design validation protocol; the risk analysis boundary conditions were too narrow |

**Root Cause 2**: Occlusion detection algorithm threshold (300 mmHg) was validated exclusively
against bench conditions. Clinical partial occlusions below this threshold were not detected,
creating a patient safety risk for drug delivery failure, particularly in ambulatory pump
configurations where lower-pressure occlusions can develop gradually.

---

## Chain 3: Sterile Barrier Deficiency

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why did microbial contamination pathways exist in certain device configurations? | Nimbus II EpiD and EMS models lacked an adequate sterile barrier between the drug pathway and the electronics compartment |
| Why 2 | Why was the sterile barrier absent in these specific configurations? | The housing geometry redesigned for Nimbus II EpiD and EMS models did not accommodate the barrier layer used in the original Nimbus design |
| Why 3 | Why was the housing geometry redesign allowed without the sterile barrier? | The design review for EpiD/EMS variants did not identify the sterile barrier omission as a patient safety risk |
| Why 4 | Why did the design review miss this critical gap? | Cross-functional design review team for the EpiD/EMS variants did not include an infection control specialist — the review was conducted purely by mechanical and electrical engineers |
| Why 5 | Why was the review team composition incomplete for EpiD/EMS? | Root cause: **Sterile barrier design review gap** — the design review process did not systematically mandate infection control expertise for all device variant reviews, only for entirely new device families |

**Root Cause 3**: Absence of sterile barrier in Nimbus II EpiD and EMS configurations
enabled microbial contamination of the drug delivery pathway. This was a design oversight
traceable to incomplete cross-functional design review, where infection control expertise
was not present for variant-level design changes.

---

## Summary of Root Causes

| Root Cause | Category | CAPA Priority |
|-----------|---------|--------------|
| BMS circuit design flaw — Li-ion aging not modeled | Machine/Design | Critical |
| Occlusion detection algorithm validation gap — threshold 300 mmHg insufficient | Machine/Method | High |
| Sterile barrier absence in EpiD/EMS models | Material/Design | Critical |

All three root causes require complete device redesign and new 510(k) clearance per FDA guidance.
InfuTronix has committed to this path with a device support cutoff date of 2024-06-20, after
which no software updates, technical support, or replacement parts will be provided.
""")

    # -------- Q4: Regulatory obligations (加难: all four keys required) --------
    _wj(out / "regulatory_obligations.json", {
        "mdr_30day_cfr": MDR_30DAY_CFR,          # "21 CFR 803.50(a)(1)"
        "mdr_5day_cfr": MDR_5DAY_CFR,            # "21 CFR 803.53"
        "recall_report_cfr": RECALL_REPORT_CFR,   # "21 CFR 806.10"
        "recall_report_deadline_days": RECALL_REPORT_DAYS,  # 10
    })

    # -------- Q5: Fishbone JSON (Six-M) --------
    _wj(out / "nimbus_fishbone.json", {
        "device": "InfuTronix Nimbus/Nimbus II",
        "categories": {
            "Man": {
                "causes": [
                    "Insufficient clinical training on device failure symptoms",
                    "Delayed alarm recognition in clinical environment",
                    "Incomplete incoming inspection by hospital biomedical engineering",
                ]
            },
            "Machine": {
                "causes": [
                    "battery_failure: BMS circuit design flaw — inadequate Li-ion aging model",
                    "occlusion_sensor: Algorithm threshold (300 mmHg) insufficient for clinical partial occlusion detection",
                    "System error: unrecoverable firmware state requiring device reset",
                    "Flow rate deviation: drug delivery outside programmed range during battery degradation",
                ]
            },
            "Material": {
                "causes": [
                    "sterile_barrier: Absence of sterile barrier between drug pathway and electronics in Nimbus II EpiD/EMS",
                    "Substandard Li-ion cell chemistry specification for medical high-current demand",
                    "Tubing material incompatibility under partial occlusion conditions",
                ]
            },
            "Method": {
                "causes": [
                    "Incomplete design validation protocol — battery aging not included",
                    "Use-related risk analysis limited to bench conditions only",
                    "Missing incoming quality control test for battery capacity under load",
                ]
            },
            "Environment": {
                "causes": [
                    "High ambient temperature variability in clinical environments accelerating battery degradation",
                    "Humidity exposure affecting electronic connections",
                ]
            },
            "Measurement": {
                "causes": [
                    "Battery state-of-charge measurement not accounting for aged cell impedance",
                    "Occlusion pressure measurement calibration drift > 5% in field conditions",
                    "Flow rate accuracy measurement tolerance not verified under battery-degraded conditions",
                ]
            },
        },
        "root_causes": [
            "battery_failure: BMS circuit design flaw",
            "occlusion_sensor: detection threshold validation gap",
            "sterile_barrier: absent in EpiD/EMS configurations",
        ],
    })

    # -------- Q6: Failure mode stats CSV --------
    failure_modes = [
        ("battery_failure", 1025),
        ("occlusion_upstream", 748),
        ("system_error", 612),
        ("flow_rate_high", 489),
        ("flow_rate_low", 421),
        ("drug_leakage", 254),
        ("housing_damage", 149),
    ]
    total_count = sum(c for _, c in failure_modes)
    csv_rows = [["failure_mode", "count", "pct_of_total"]]
    for fm, cnt in failure_modes:
        pct = round(100.0 * cnt / total_count, 2)
        csv_rows.append([fm, str(cnt), f"{pct:.2f}"])
    csv_txt = "\n".join(",".join(row) for row in csv_rows) + "\n"
    _w(out / "failure_mode_stats.csv", csv_txt)

    # -------- Q7: Ivenix tech summary v1 (pre-update state) --------
    _w(out / "ivenix_tech_summary_v1.md", f"""# Ivenix LVP Software Recall — Technical Summary v1
## Pre-Update State (Before FSN Revision)

**Recall Number**: {IVENIX_RECALL_NUM}
**Product Code**: {IVENIX_PRODUCT_CODE}
**Status**: Based on initial session information (pre-Update 1)

---

## Summary Based on Initial Session Data

Based on information available in the initial email session (sess-03), the Ivenix
LVP software recall was initially described with the following parameters:

- **Recall Number**: {IVENIX_RECALL_NUM}
- **Product Code**: {IVENIX_PRODUCT_CODE}
- **Affected Software Version (initial session reference)**: 5.10.0
  (Note: Angela's initial email stated '5.10.0 only' — this was subsequently
  corrected by Update 1 to '{IVENIX_AFFECTED_VER} and earlier')
- **Fixed Version**: {IVENIX_FIXED_VER}
- **IMS Fixed Version**: {IVENIX_IMS_FIXED}

## Two Software Anomalies

The Ivenix recall involves two distinct software anomalies:

### Anomaly 1: Battery State-of-Charge Reporting Error
Inaccurate battery remaining capacity display leads to unexpected device shutdown
during infusion. Batteries with health below {IVENIX_BATTERY_THRESHOLD}% are most affected.

### Anomaly 2: Dual-Zero Rate Entry Interface Freeze
Entering a rate with two leading zeros (e.g., "0010") followed by Back/OK causes
the UI to freeze in fail-stop alarm state, requiring power cycle to recover.

## Status Note

This v1 summary captures the pre-Update 1 state. The affected version description
was subsequently corrected. See ivenix_recall_metadata.json (post-Update 1) for
the authoritative version.
""")

    # -------- Q8: Ivenix recall metadata (post-Update 1) --------
    _wj(out / "ivenix_recall_metadata.json", {
        "recall_number": IVENIX_RECALL_NUM,
        "affected_software_version": f"{IVENIX_AFFECTED_VER} and earlier",
        "product_code": IVENIX_PRODUCT_CODE,
        "fixed_version": IVENIX_FIXED_VER,
        "ims_fixed_version": IVENIX_IMS_FIXED,
        "injuries": IVENIX_INJURIES,
        "battery_threshold_pct": IVENIX_BATTERY_THRESHOLD,
        "anomaly_1": "Battery state-of-charge reporting error causing unexpected shutdown",
        "anomaly_2": "Dual-zero rate entry causes UI freeze in fail-stop alarm state",
        "units_software_kits": "30",
    })

    # -------- Q9: CAPA comparison --------
    _wj(out / "capa_comparison.json", {
        "case_A": {
            "root_cause_category": "hardware_design",
            "capa_actions": [
                "Complete redesign of battery management circuit with Li-ion aging model",
                "Revise occlusion detection algorithm threshold and validation protocol",
                "Add sterile barrier to all pump housing configurations",
                "Submit new 510(k) clearance application",
            ],
        },
        "case_B": {
            "root_cause_category": "software_anomaly",
            "capa_actions": [
                f"Update LVP software to v{IVENIX_FIXED_VER}",
                f"Update IMS to v{IVENIX_IMS_FIXED}",
                f"Replace batteries with health below {IVENIX_BATTERY_THRESHOLD}%",
                "Revise V&V protocol to include aged-battery and boundary-case test scenarios",
            ],
        },
    })

    # -------- Q10: Case C assessment --------
    _wj(out / "case_C_assessment.json", {
        "status": "ARCHIVED_LEGACY",
        "reason": (
            "The SynchroMed II 2019 recall is a legacy archived case. "
            "It involves a different manufacturer (Medtronic), different device class "
            "(implantable infusion pump), different failure mode (foreign particle/gear stall), "
            "and occurred in 2019 — outside the 2024/2025-2026 RCA scope."
        ),
        "should_include_in_current_rca": False,
        "affected_models": ["8637-20", "8637-40"],
        "units": 11299,
    })

    # -------- Q11: MAUDE MDR summary --------
    _w(out / "nimbus_mdr_summary.md", f"""# Nimbus Recall MAUDE MDR Summary
## FDA MedWatch Form 3500A — Manufacturer Report
## InfuTronix Nimbus/Nimbus II Infusion Pump Systems

**Report Type**: Mandatory Manufacturer MDR (Form 3500A)
**Regulatory Basis**: 21 CFR 803.50(a)(1) — 30 calendar days from awareness
**Report Status**: Summary for RCA Documentation

---

## Section A — Patient Information

- A1: Patient IDs de-identified per reporting requirements
- A2: Age range affected: Pediatric to geriatric (all age groups using infusion therapy)
- A3: Weight: Not uniformly captured in complaint log
- A4: Date of events: Multiple events from 2019-2024 (see complaint_log_2019_2023.csv)
- A5: Date of this summary: April 2026

---

## Section B — Adverse Event Description

- **B1 Event types identified** (from {NIMBUS_COMPLAINTS:,} complaint records):
  - Battery failure events with unexpected device shutdown during infusion
  - Upstream occlusion events with missed alarm activation
  - System errors requiring device reset during therapy
  - Drug leakage events
  - Flow rate deviations (high and low)
  - Housing damage affecting sterile barrier integrity

- **B2 Reported outcomes**:
  - Deaths: {NIMBUS_DEATHS}
  - Serious injuries (e.g., seizure, shock, organ failure): {NIMBUS_INJURIES}
  - Patient discomfort/near-miss events: Reported in complaints
  - Device malfunction without patient harm: Majority of complaints

- **B3 Event narrative (representative)**:
  Patient received infusion via Nimbus II Flex pump (Lot LOT-XXXX-2022). During
  administration, the pump displayed no alarm, yet delivery rate had deviated beyond
  clinical threshold. Patient experienced adverse response consistent with flow rate
  deviation. Device returned for failure analysis. Root cause attributed to battery
  management failure per engineering investigation. MDR submitted per 21 CFR 803.50(a)(1)
  within 30 calendar days of awareness.

- **B4 Relevant tests**: Engineering failure analysis of returned units; battery discharge
  testing; occlusion pressure measurement; flow accuracy verification per IEC 60601-2-24.

- **B5 Relevant history**: Multiple prior complaints with similar failure modes received
  prior to recall initiation. Cumulative complaint data triggered recall threshold per
  FDA Class I criteria.

---

## Section C — Suspect Medical Device

- **C1 Brand name**: Nimbus / Nimbus II Infusion Pump System
- **C2 Common name**: Ambulatory Infusion Pump
- **C3 Manufacturer**: InfuTronix, LLC
- **C4 Affected models**: Nimbus Administration Set, Nimbus Flex, Nimbus PainPro (Halo),
  Nimbus II PainPRO, Nimbus II Flex, Nimbus II Plus, Nimbus II EpiD, Nimbus II EMS
  - UDI (Nimbus main pump): {NIMBUS_UDI_MAIN}
  - Distribution period: {NIMBUS_DIST_START} to {NIMBUS_DIST_END}
  - Units recalled: {NIMBUS_UNITS:,}
- **C5 Premarket clearance**: 510(k) clearance required after complete redesign
- **C6 Operator**: Health professionals (nurses, pharmacists, home health clinicians)
- **C7 Combination product**: Not applicable

---

## Section D — Suspect Concomitant Products

No concomitant products identified as contributing to the adverse events. Failures were
attributable to the infusion pump device itself based on engineering analysis.

---

## Section E — Reporter Information

- **E1 Reporter**: InfuTronix, LLC Quality and Regulatory Affairs department
- **E2 Health professional**: Yes (reporting through Quality/Regulatory)
- **E3 Occupation**: Medical Device Manufacturer — Regulatory Affairs
- **E4 Also reported to**: FDA MedWatch (mandatory); Healthcare facilities notified
  via Field Safety Notice

---

## Section F — User Facility (N/A for Manufacturer Submission)

Not applicable. This is a manufacturer mandatory MDR submission.

---

## Section G — Manufacturer Information

- **G1 Manufacturer contact**: InfuTronix Quality & Regulatory Affairs
  Report submitted to FDA within required timeframe.
- **G2 Manufacturer report number**: InfuTronix MDR batch — submitted under Class I recall
- **G3 Device return**: Units returned per recall action plan. Date received by manufacturer
  per facility return instructions.
- **G4 Manufacturer narrative**: InfuTronix conducted a comprehensive failure investigation
  identifying battery management circuit design flaw, occlusion detection algorithm
  threshold insufficiency, and sterile barrier absence as primary root causes. The device
  requires complete redesign and new 510(k) clearance. Device support terminated
  {NIMBUS_SUPPORT_CUTOFF}. All complaints assessed for MDR reportability per
  21 CFR 803.50(a)(1) (30 calendar days) and 21 CFR 803.53 (5 work days for urgent events).
- **G5 FDA contact for questions**: InfuTronix Regulatory Affairs, recall@infutronix.com

---

## MDR Reporting Summary

| Requirement | Timeframe | Citation | Applied |
|-------------|-----------|---------|---------|
| Death or serious injury | 30 calendar days | 21 CFR 803.50(a)(1) | Yes — all {NIMBUS_DEATHS + NIMBUS_INJURIES} events reported |
| Urgent/remedial events | 5 work days | 21 CFR 803.53 | Yes — as applicable |
| Recall report | {RECALL_REPORT_DAYS} working days | {RECALL_REPORT_CFR} | Yes — submitted at recall initiation |

**Total complaints assessed**: {NIMBUS_COMPLAINTS:,}
**MDR-qualifying events**: {NIMBUS_DEATHS + NIMBUS_INJURIES} (deaths + serious injuries)
**Reporting compliance**: All events reported within required timeframes per 21 CFR 803.50(a)(1).
""")

    # -------- Q12: Ivenix recall metadata v2 (post-Update 2 supersede) --------
    _wj(out / "ivenix_recall_metadata_v2.json", {
        "recall_number": IVENIX_RECALL_NUM,
        "affected_software_version": f"{IVENIX_AFFECTED_VER} and earlier",
        "product_code": IVENIX_PRODUCT_CODE,
        "fixed_version": IVENIX_FIXED_VER,
        "ims_fixed_version": IVENIX_IMS_FIXED,
        "injuries": IVENIX_INJURIES,
        "battery_threshold_pct": IVENIX_BATTERY_THRESHOLD,
        "anomaly_1": "Battery state-of-charge reporting error causing unexpected shutdown",
        "anomaly_2": "Dual-zero rate entry causes UI freeze in fail-stop alarm state",
        "units_software_kits": "undisclosed",
        "units_software_kits_note": (
            "Supersede (Update 2): The '30 units' figure referred to software correction kits, "
            "NOT hardware LVP units. Actual hardware installation count is undisclosed."
        ),
    })

    # -------- Q13: Distribution timeline --------
    _wj(out / "distribution_timeline.json", {
        "manufacturer": "InfuTronix, LLC",
        "distribution_start": NIMBUS_DIST_START,
        "distribution_end": NIMBUS_DIST_END,
        "support_cutoff": NIMBUS_SUPPORT_CUTOFF,
        "evidence_source": (
            "FDA Official Recall Notice; MedTech Dive "
            "(https://www.medtechdive.com/news/infutronix-nimbus-infusion-pump-recall-injuries-death/714391/)"
        ),
        "conflicts_resolved": [
            {
                "session": "Email (angela_reyes, March 30 2026)",
                "claimed_value": "2014 (unspecified distribution start year)",
                "resolution": (
                    f"Incorrect. Confirmed {NIMBUS_DIST_START} per FDA notice, MedTech Dive, "
                    "HPN Online, and Drug Delivery Business (all consistent). "
                    "The 2014 reference in the email was sourced from an unverified internal draft memo. "
                    "Update 2 formally superseded this error."
                ),
            }
        ],
    })

    # -------- Q14: Executive summary --------
    _w(out / "executive_summary.md", f"""---
date: "2026-04-20"
author: "MedSafe RCA Team"
recall_cases: ["Case A: InfuTronix Nimbus", "Case B: Fresenius Kabi Ivenix LVP"]
classification: "Class I"
---

# Executive Summary — MedSafe Root Cause Analysis
## FDA Class I Recall Investigation: Cases A and B

---

## Overview

The MedSafe RCA Team has completed a comprehensive root cause analysis of two active
FDA Class I recalls affecting infusion pump systems used in clinical settings:

- **Case A**: InfuTronix Nimbus/Nimbus II Infusion Pump Systems (hardware)
- **Case B**: Fresenius Kabi Ivenix LVP Software ({IVENIX_RECALL_NUM}) (software)

A third case (Case C: Medtronic SynchroMed II 2019) was reviewed and determined
to be archived legacy material outside the current RCA scope.

---

## Case A: InfuTronix Nimbus Recall

**Recall Class**: Class I (Most Serious)
**Units Recalled**: {NIMBUS_UNITS:,} infusion pump systems
**Distribution Period**: {NIMBUS_DIST_START} to {NIMBUS_DIST_END}
**Device Support Cutoff**: {NIMBUS_SUPPORT_CUTOFF}

### Adverse Events

| Category | Count |
|----------|-------|
| Total Complaints | {NIMBUS_COMPLAINTS:,} |
| Serious Injuries | {NIMBUS_INJURIES} |
| Deaths | {NIMBUS_DEATHS} |

### Root Causes Identified

1. **Battery Management System design flaw** — Li-ion aging not accounted for in BMS circuit design
2. **Occlusion detection algorithm validation gap** — 300 mmHg threshold insufficient for clinical conditions
3. **Sterile barrier absence** — Nimbus II EpiD/EMS configurations lack adequate sterile barrier

### Path Forward

Complete device redesign and new 510(k) clearance required. Device support terminated {NIMBUS_SUPPORT_CUTOFF}.

---

## Case B: Fresenius Kabi Ivenix LVP Software Recall

**Recall Class**: Class I
**Recall Number**: {IVENIX_RECALL_NUM}
**Affected Software**: {IVENIX_AFFECTED_VER} and earlier (Product Code: {IVENIX_PRODUCT_CODE})
**Fixed Versions**: LVP {IVENIX_FIXED_VER} + IMS {IVENIX_IMS_FIXED}

### Adverse Events (as of Nov 18, 2025)

| Category | Count |
|----------|-------|
| Serious Injuries | {IVENIX_INJURIES} |
| Deaths | 0 |

### Root Causes Identified

1. **Anomaly 1**: Battery SOC coulomb counting algorithm defect — does not account for aging
2. **Anomaly 2**: Input validation gap — dual-zero rate entry triggers fail-stop via unhandled exception

### Corrective Actions

Software updates deployed: LVP {IVENIX_FIXED_VER} + IMS {IVENIX_IMS_FIXED}. Battery replacement
required for units with health below {IVENIX_BATTERY_THRESHOLD}%.

---

## Regulatory Compliance Status

| Requirement | Citation | Status |
|-------------|---------|--------|
| MDR reporting (death/injury) | 21 CFR 803.50(a)(1) | Completed within 30 calendar days |
| Recall report | 21 CFR 806.10 | Completed within 10 working days |

---

## Key Differences: Hardware vs. Software Failure

| Dimension | Case A (Hardware) | Case B (Software) |
|-----------|------------------|------------------|
| Root cause category | hardware_design | software_anomaly |
| Remediation | Complete device redesign + new 510(k) | Software update patch |
| Complexity | High — multi-year redesign | Moderate — patch deployable within weeks |
| Ongoing support | Terminated {NIMBUS_SUPPORT_CUTOFF} | Active, updated to {IVENIX_FIXED_VER} |

---

## Case C: SynchroMed II (Archived — Not in Scope)

The 2019 Medtronic SynchroMed II recall is archived legacy material. It involves a
different manufacturer, device class, failure mode, and time period. It has no bearing
on this 2024/2025-2026 RCA investigation.
""")

    # -------- Q15: Final report (P5 naming) --------
    # 使用固定测试日期 20260420
    final_report_name = "final_rca_report_20260420.md"
    _w(out / final_report_name, f"""# Final Root Cause Analysis Report
## MedSafe RCA Team — Cases A and B

**Report Date**: 2026-04-20
**Classification**: Class I Recall Investigation

---

## 1. Scope

This final report consolidates the RCA findings for:
- Case A: InfuTronix Nimbus/Nimbus II (Class I recall, 2024)
- Case B: Fresenius Kabi Ivenix LVP Software (Class I recall {IVENIX_RECALL_NUM}, 2025-2026)

Case C (Medtronic SynchroMed II, 2019) is excluded as archived legacy material.

---

## 2. Case A: Nimbus Recall Summary

**Units**: {NIMBUS_UNITS:,} | **Complaints**: {NIMBUS_COMPLAINTS:,} | **Deaths**: {NIMBUS_DEATHS}

Root causes: battery_failure (BMS design flaw), occlusion_sensor (threshold validation gap),
sterile_barrier (absent in EpiD/EMS models).

CAPA: Complete device redesign + new 510(k). Support cutoff: {NIMBUS_SUPPORT_CUTOFF}.

---

## 3. Case B: Ivenix LVP Software Recall Summary

**Recall**: {IVENIX_RECALL_NUM} | **Affected**: {IVENIX_AFFECTED_VER} and earlier | **Injuries**: {IVENIX_INJURIES}

Root causes: Battery SOC algorithm defect (Anomaly 1), dual-zero input parsing bug (Anomaly 2).

CAPA: LVP software updated to {IVENIX_FIXED_VER}, IMS to {IVENIX_IMS_FIXED}. Battery replacement
threshold: {IVENIX_BATTERY_THRESHOLD}%.

---

## 4. Regulatory Compliance

All Class I recall reporting obligations met:
- MDR: per 21 CFR 803.50(a)(1) (30 calendar days)
- Recall reports: per 21 CFR 806.10 (10 working days)

---

## 5. Lessons Learned

1. Medical device V&V must include aged-component scenarios (not just new-component baseline)
2. Software input validation must cover boundary conditions (leading zeros, edge cases)
3. Cross-functional design reviews must include infection control expertise for all device variants

---

*Report prepared by MedSafe RCA Team. All data sourced from FDA official recall notices,
MAUDE database, and authoritative regulatory documents.*
""")

    # -------- Q16: SHA-256 verification token --------
    meta_path = out / "nimbus_recall_metadata.json"
    digest = hashlib.sha256(meta_path.read_bytes()).hexdigest()
    _w(out / "verification_token.txt", f"VERIFIED:{digest}\n")

    # -------- Q17: Compliance checklist (加难: >=10 items required; NIMBUS-CAPA + HONEYPOT-FLAGS mandatory) --------
    _wj(out / "compliance_checklist.json", {
        "items": [
            {
                "id": "MDR-30DAY",
                "description": "Report all Nimbus death and serious injury events to FDA within 30 calendar days of awareness",
                "status": "COMPLETE",
                "evidence_file": "nimbus_mdr_summary.md",
                "cfr_citation": MDR_30DAY_CFR,
            },
            {
                "id": "MDR-5DAY",
                "description": "Submit expedited 5-work-day report for events requiring immediate remedial action",
                "status": "COMPLETE",
                "evidence_file": "nimbus_mdr_summary.md",
                "cfr_citation": MDR_5DAY_CFR,
            },
            {
                "id": "RECALL-REPORT",
                "description": "File correction/removal report with FDA within 10 working days of initiating recall action",
                "status": "COMPLETE",
                "evidence_file": "regulatory_obligations.json",
                "cfr_citation": RECALL_REPORT_CFR,
            },
            {
                "id": "IVENIX-SOFTWARE",
                "description": "Confirm Ivenix LVP software update to v5.10.2 completed; verify units_software_kits corrected to undisclosed per Update 2 supersede",
                "status": "COMPLETE",
                "evidence_file": "ivenix_recall_metadata_v2.json",
                "cfr_citation": "",
            },
            {
                "id": "NIMBUS-CAPA",
                "description": "Initiate CAPA for battery BMS redesign, occlusion detection validation, and sterile barrier remediation",
                "status": "IN_PROGRESS",
                "evidence_file": "capa_comparison.json",
                "cfr_citation": "21 CFR 820.100",
            },
            {
                "id": "CASE-C-EXCLUSION",
                "description": "Confirm SynchroMed II 2019 (archived legacy) is excluded from current RCA scope",
                "status": "COMPLETE",
                "evidence_file": "case_C_assessment.json",
                "cfr_citation": "",
            },
            {
                "id": "DISTRIBUTION-DATES",
                "description": "Confirm Nimbus distribution start date as 2015-02-27 (supersedes erroneous 2014 reference)",
                "status": "COMPLETE",
                "evidence_file": "distribution_timeline.json",
                "cfr_citation": "",
            },
            {
                "id": "HONEYPOT-FLAGS",
                "description": "Document and discard inaccurate bot-generated summary data (ivenix injuries: 5→2; nimbus cutoff: 2024-08-31→2024-06-20)",
                "status": "COMPLETE",
                "evidence_file": "honeypot_flags.json",
                "cfr_citation": "",
            },
            {
                "id": "NIMBUS-UDI",
                "description": "Verify Nimbus main pump UDI 00817170020000 is correctly recorded in recall metadata",
                "status": "COMPLETE",
                "evidence_file": "nimbus_recall_metadata.json",
                "cfr_citation": "21 CFR 830",
            },
            {
                "id": "VERIFICATION-TOKEN",
                "description": "Generate SHA-256 verification token for nimbus_recall_metadata.json to ensure data integrity",
                "status": "COMPLETE",
                "evidence_file": "verification_token.txt",
                "cfr_citation": "",
            },
        ]
    })


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py"],
    "q2": ["check_q2.py"],
    "q3": ["check_q3.py", ("pref", "P1", "rca_outputs/nimbus_5why.md")],
    "q4": ["check_q4.py"],
    "q5": ["check_q5.py", ("pref", "P2", "rca_outputs/nimbus_fishbone.json")],
    "q6": ["check_q6.py"],
    "q7": ["check_q7.py"],
    "q8": ["check_q8.py"],
    "q9": ["check_q9.py"],
    "q10": ["check_q10.py"],
    "q11": ["check_q11.py", ("pref", "P3", "rca_outputs/nimbus_mdr_summary.md")],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py"],
    "q14": ["check_q14.py", ("pref", "P4", "rca_outputs/executive_summary.md")],
    "q15": ["check_q15.py"],
    "q16": ["check_q16.py"],
    "q17": ["check_q17.py"],
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


def _wj_neg(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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

    # 反例抽样（>= 4 个）
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    out = ws / "rca_outputs"

    # 反例1: Q1 投诉数用诱饵 3800
    _wj_neg(out / "nimbus_recall_metadata.json", {
        "manufacturer": "InfuTronix, LLC",
        "recall_class": "Class I",
        "units_recalled": 52328,
        "complaints": 3800,  # 诱饵数字
        "serious_injuries": 6,
        "deaths": 1,
        "distribution_start": "2015-02-27",
        "distribution_end": "2024-02-29",
        "support_cutoff": "2024-06-20",
        "udi_main": "00817170020000",
    })
    ok, _ = run_check("check_q1.py", ws); probes += 1; caught += (not ok)
    print(f"  q1 complaint=3800 (decoy) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例2: Q8 使用旧版本 5.10.0（Update 1 前的错误）
    _wj_neg(out / "ivenix_recall_metadata.json", {
        "recall_number": "Z-0885-2026",
        "affected_software_version": "5.10.0",  # Update 1 前的错误版本
        "product_code": "LVP-SW-0005",
        "fixed_version": "5.10.2",
        "ims_fixed_version": "5.2.2",
        "injuries": 2,
        "battery_threshold_pct": 70,
        "anomaly_1": "Battery error",
        "anomaly_2": "Dual-zero freeze",
        "units_software_kits": "30",
    })
    ok, _ = run_check("check_q8.py", ws); probes += 1; caught += (not ok)
    print(f"  q8 affected_version=5.10.0 (pre-update error) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例3: Q12 保留 "30" 而非 "undisclosed"（未识别 supersede）
    _wj_neg(out / "ivenix_recall_metadata_v2.json", {
        "recall_number": "Z-0885-2026",
        "affected_software_version": "5.10.1 and earlier",
        "product_code": "LVP-SW-0005",
        "fixed_version": "5.10.2",
        "ims_fixed_version": "5.2.2",
        "injuries": 2,
        "battery_threshold_pct": 70,
        "anomaly_1": "Battery error",
        "anomaly_2": "Dual-zero freeze",
        "units_software_kits": "30",  # 未处理 supersede
    })
    ok, _ = run_check("check_q12.py", ws); probes += 1; caught += (not ok)
    print(f"  q12 units_software_kits=30 (supersede not applied) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例4: Q13 使用 2014 年错误分发起始日
    _wj_neg(out / "distribution_timeline.json", {
        "manufacturer": "InfuTronix, LLC",
        "distribution_start": "2014-02-01",  # 错误年份
        "distribution_end": "2024-02-29",
        "support_cutoff": "2024-06-20",
        "evidence_source": "Internal memo (unverified)",
        "conflicts_resolved": [],
    })
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 distribution_start=2014 (incorrect year) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例5: Q16 占位符哈希
    (out / "verification_token.txt").write_text("VERIFIED:" + "0" * 64 + "\n", encoding="utf-8")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例6: Q10 将 SynchroMed 旧案标为在范围内
    _wj_neg(out / "case_C_assessment.json", {
        "status": "ACTIVE",
        "reason": "Including for comprehensive analysis",
        "should_include_in_current_rca": True,  # 错误：应为 false
        "affected_models": ["8637-20", "8637-40"],
        "units": 11299,
    })
    ok, _ = run_check("check_q10.py", ws); probes += 1; caught += (not ok)
    print(f"  q10 should_include=true (red herring accepted) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
