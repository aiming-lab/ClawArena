#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_eng2.py — 生成 ClawArena 真实数据集场景 eng2（NYC 出租车数据 pipeline 迁移与质检）。

题材与锚点取材真实（NYC TLC Open Data / Azure 文档 / MTA congestion pricing），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

幂等：每次运行先清空 eng2 的 workspace/state/updates 后重建，再注册进数据集。
questions.json 与 check 脚本由 eval/eng2/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_eng2.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id,
    init_dataset, register_scenario,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "eng2"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# 真实字段（NYC TLC Yellow Taxi 数据字典，verbatim）
FIELDS = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
    "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "extra", "mta_tax", "improvement_surcharge",
    "tip_amount", "tolls_amount", "total_amount", "congestion_surcharge", "airport_fee",
]
BOROUGHS = ["EWR", "Queens", "Bronx", "Manhattan", "Staten Island", "Brooklyn"]


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. 系统文件（OpenClaw agent 启动文件）
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Data Engineering AI assistant supporting Alice Chen, Data Engineering Lead,
on the migration of NYC TLC Yellow Taxi trip data into a Bronze/Silver/Gold lakehouse.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical field definitions and dataset-level
   statistics live in `data/reference/dataset_profile.json` and `docs/data_dictionary_excerpt.md`.
   Auto-generated summaries (e.g. files named `*_BOT_*` / `BOT_SUMMARY_*`) are convenience
   artefacts and are NOT authoritative — verify any number against the profile or the raw data.

2. **Verbatim field names**: Always reference official column names exactly as they appear in
   the data dictionary (e.g. `tpep_pickup_datetime`, never `pickup_datetime`). Renaming or
   abbreviating a field is a defect.

3. **Output schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"` — the lakehouse registry keys artefacts by it and rejects untagged files.

4. **Reproducibility**: Prefer re-runnable scripts under `scripts/` and `pipeline/` over
   one-off hand calculations, so that every headline number has a single source of truth.

5. **Temporal awareness**: Migration decisions arrive incrementally. When an operations notice
   or a corrected rule supersedes an earlier instruction, the later instruction wins — revisit
   and revise prior outputs rather than stacking contradictory logic.

6. **Schema discipline**: Quality reports follow a fixed field order. Pipeline scripts carry the
   standard interpreter + encoding header. Do not improvise schema shapes.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Alice Chen** — Data Engineering Lead. Owns the Yellow Taxi lakehouse migration.
  Prefers reproducible scripts, four-decimal numeric formatting, and verbatim official
  field names. Terse, precise, reviews by skimming JSON shapes.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Bob Martins | Data Engineer | Slack #data-engineering | Implements ingest/clean; coordinates with the TLC vendor team by email |
| Carol Diaz | Product Manager | Feishu DM | Owns reporting requirements; wants payment-type × borough pivots |
| Dave Okoye | Data Scientist | Discord #code-review | Sometimes quotes the auto-generated BOT summary — double-check his numbers |
| Eve Larsson | QA Engineer | Discord #code-review | Validates against the NYC Open Data API; authoritative on dataset stats |

## Channels
- **Slack #data-engineering**: schema migration discussion (Alice, Bob, Carol)
- **Email (Bob ↔ TLC vendor team)**: VendorID provenance questions
- **Feishu DM (Carol → agent)**: reporting requirements
- **Discord #code-review (Dave, Eve)**: code review + dataset-stat disputes
""")
    w(WS / "IDENTITY.md", """# Identity

You are **DataOps AI**, a data-engineering assistant deployed to support Alice Chen during the
migration of NYC TLC Yellow Taxi trip data into a Bronze/Silver/Gold lakehouse (DuckDB + Parquet).

You help author and validate ingestion, cleaning, enrichment and aggregation logic; produce
field-level data-quality reports; reconcile conflicting instructions from Slack/Email/Feishu/Discord;
and generate stakeholder-readable migration artefacts. Source data and reference files under
`data/` are read-only inputs; you create your deliverables under `output/`, `pipeline/`, and `scripts/`.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to `ls`, run scripts, and to **write your deliverable files** |

## Rules
- Source inputs under `data/` (and `docs/`, `pipeline/config/`) are **read-only** — do not modify them.
- You DO create new deliverable files under `output/`, `pipeline/bronze|silver|gold/`, and `scripts/`
  using `exec` (e.g. heredoc / python). That is the expected way to complete tasks.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
""")


# --------------------------------------------------------------------------- #
# 2. reference 数据（真实锚点）
# --------------------------------------------------------------------------- #
def gen_reference() -> None:
    # 2.1 taxi_zone_lookup.csv — 真实结构：265 行，LocationID 1-265，6 个 Borough 枚举
    rng = random.Random(2023)
    rows = [["LocationID", "Borough", "Zone", "service_zone"]]
    rows.append(["1", "EWR", "Newark Airport", "EWR"])
    zone_words = ["Park", "Heights", "Hill", "Bay", "Village", "Harbor", "Gardens",
                  "Square", "Point", "Beach", "Terminal", "Junction", "Corners", "Yards"]
    for loc in range(2, 265):
        if loc in (132, 138):           # JFK / LaGuardia 真实为 Airports service zone
            boro, sz = "Queens", "Airports"
        else:
            boro = rng.choice(["Queens", "Bronx", "Manhattan", "Staten Island", "Brooklyn"])
            sz = "Yellow Zone" if boro == "Manhattan" else "Boro Zone"
        zone = f"{rng.choice(['North','South','East','West','Central','Upper','Lower'])} {rng.choice(zone_words)}"
        rows.append([str(loc), boro, zone, sz])
    rows.append(["265", "Unknown", "NV", "N/A"])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "data" / "reference" / "taxi_zone_lookup.csv", buf.getvalue())

    # 2.2 dataset_profile.json — 全量数据集统计（真实 NYC Open Data columns.json 锚点，权威源）
    wj(WS / "data" / "reference" / "dataset_profile.json", {
        "dataset": "2023 Yellow Taxi Trip Data",
        "source_url": "https://data.cityofnewyork.us/Transportation/2023-Yellow-Taxi-Trip-Data/4b4i-vvec",
        "total_rows": 38310226,
        "fields": {
            "passenger_count": {"null_count": 1309356, "type": "number"},
            "RatecodeID": {"null_count": 1309356, "type": "number", "valid_values": [1, 2, 3, 4, 5, 6]},
            "store_and_fwd_flag": {"null_count": 1309356, "type": "text"},
            "congestion_surcharge": {"null_count": 1309356, "type": "number"},
            "airport_fee": {"null_count": 1309356, "type": "number"},
            "fare_amount": {"min": -1087.30, "max": 386983.63, "type": "number"},
            "trip_distance": {"min": 0.0, "max": 345729.44, "type": "number"},
            "tpep_pickup_datetime": {"min": "1970-01-20", "max": "2024-01-03", "type": "timestamp"},
        },
        "payment_type_enum": {"1": "Credit card", "2": "Cash", "3": "No charge",
                              "4": "Dispute", "5": "Unknown", "6": "Voided trip"},
        "ratecode_enum": {"1": "Standard", "2": "JFK", "3": "Newark",
                          "4": "Nassau/Westchester", "5": "Negotiated", "6": "Group ride"},
        "note": "Authoritative dataset-level statistics. Verify any quoted number against this file.",
    })

    # 2.3 vendor_registry.json — VendorID=6 初始 status=audit_only（update2 改 test_account）
    wj(WS / "data" / "reference" / "vendor_registry.json", {
        "vendors": {
            "1": {"name": "Creative Mobile Technologies, LLC", "status": "production"},
            "2": {"name": "Curb Mobility, LLC", "status": "production"},
            "6": {"name": "Myle Technologies Inc (sandbox)", "status": "audit_only",
                  "exclude_from_silver": False,
                  "note": "Per Slack 2024 discussion, retained for audit sampling."},
        },
        "valid_production_vendor_ids": [1, 2],
        "schema_version": "1.0",
    })


# --------------------------------------------------------------------------- #
# 3. 合成采样 CSV（确定性；注入真实质量问题，锚点可机检）
# --------------------------------------------------------------------------- #
def _dt(y, m, d, h, mi):
    return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{mi:02d}:00"


def gen_sample_csv(path: Path, n_per_month: int = 260, seed: int = 42) -> dict:
    """生成全年 12 月采样行。返回注入锚点计数供自检。"""
    rng = random.Random(seed)
    rows = [list(FIELDS)]
    stats = {"neg_fare": 0, "future_ts": 0, "null_passenger": 0, "vendor6": 0, "min_fare": 0.0}
    for month in range(1, 13):
        for _ in range(n_per_month):
            vid = rng.choices([1, 2, 6], weights=[60, 35, 5])[0]
            day = rng.randint(1, 28)
            h = rng.randint(0, 23)
            mi = rng.randint(0, 59)
            year = 2023
            # 注入未来年份时间戳异常（约 0.5%）
            if rng.random() < 0.006:
                year = rng.choice([2088, 2084])
                stats["future_ts"] += 1
            pu = _dt(year, month, day, h, mi)
            do = _dt(year, month, day, min(h + 1, 23), mi)
            # passenger_count null（约 3.4%，对齐真实比例量级）
            if rng.random() < 0.034:
                pax = ""
                stats["null_passenger"] += 1
            else:
                pax = str(rng.choices([1, 2, 3, 4, 5], weights=[78, 10, 6, 3, 3])[0])
            dist = round(rng.uniform(0.4, 18.0), 2)
            rate = rng.choices([1, 2, 3, 4, 5], weights=[88, 5, 2, 2, 3])[0]
            puloc = rng.randint(1, 265)
            doloc = rng.randint(1, 265)
            ptype = rng.choices([1, 2, 3, 4], weights=[78, 16, 3, 3])[0]
            fare = round(rng.triangular(3.0, 40.0, 11.0), 2)   # 均值 ~18，对齐真实 NYC 2023 avg fare
            # 注入负 fare（约 1.2%）
            if rng.random() < 0.012:
                fare = -round(rng.uniform(2.5, 60.0), 2)
                stats["neg_fare"] += 1
            extra = round(rng.choice([0.0, 0.5, 1.0]), 2)
            mta = 0.50
            imp = 0.30
            tip = round(rng.uniform(0, 12), 2) if ptype == 1 else 0.0
            tolls = round(rng.choice([0.0, 0.0, 6.55]), 2)
            cong = round(rng.choice([0.0, 2.50]), 2)
            airport = round(rng.choice([0.0, 0.0, 1.25]), 2)
            total = round(max(fare, 0) + extra + mta + imp + tip + tolls + cong + airport, 2)
            if vid == 6:
                stats["vendor6"] += 1
            rows.append([vid, pu, do, pax, dist, rate, rng.choice(["N", "Y"]),
                         puloc, doloc, ptype, fare, extra, mta, imp, tip, tolls,
                         total, cong, airport])
    # 强制一行 fare_amount == -1087.30（Q5 min_observed_fare ≤ -1087 锚点）
    anchor = [2, _dt(2023, 3, 15, 14, 30), _dt(2023, 3, 15, 15, 0), "1", 2.5, 1, "N",
              161, 237, 1, -1087.30, 0.0, 0.50, 0.30, 0.0, 0.0, -1085.70, 2.50, 0.0]
    rows.append(anchor)
    stats["neg_fare"] += 1
    stats["min_fare"] = -1087.30
    # 保证至少一行 2088（Q6 future_year_examples 含 2088）
    rows.append([1, _dt(2088, 7, 4, 10, 0), _dt(2088, 7, 4, 10, 30), "2", 5.0, 1, "N",
                 100, 200, 2, 18.0, 0.0, 0.50, 0.30, 0.0, 0.0, 18.80, 0.0, 0.0])
    stats["future_ts"] += 1
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())
    stats["total_rows"] = len(rows) - 1
    return stats


# --------------------------------------------------------------------------- #
# 4. schema / 规则 / 诱饵 / 文档
# --------------------------------------------------------------------------- #
def gen_configs_and_docs() -> None:
    w(WS / "pipeline" / "config" / "schema_v1.yaml", """# Yellow Taxi schema — v1 (legacy, pre-2022)
# Missing the 2022 airport_fee and the 2025 cbd_congestion_fee columns.
version: 1
fields:
  - {name: VendorID, type: int}
  - {name: tpep_pickup_datetime, type: timestamp}
  - {name: tpep_dropoff_datetime, type: timestamp}
  - {name: passenger_count, type: int, nullable: true}
  - {name: trip_distance, type: double}
  - {name: RatecodeID, type: int, nullable: true}
  - {name: store_and_fwd_flag, type: string, nullable: true}
  - {name: PULocationID, type: int}
  - {name: DOLocationID, type: int}
  - {name: payment_type, type: int}
  - {name: fare_amount, type: double}
  - {name: extra, type: double}
  - {name: mta_tax, type: double}
  - {name: improvement_surcharge, type: double}
  - {name: tip_amount, type: double}
  - {name: tolls_amount, type: double}
  - {name: total_amount, type: double}
  - {name: congestion_surcharge, type: double, nullable: true}
""")
    w(WS / "pipeline" / "config" / "schema_v2.yaml", """# Yellow Taxi schema — v2 (current, 2025+)
# Adds airport_fee (2022) and cbd_congestion_fee (2025-01-05 congestion pricing).
version: 2
fields:
  - {name: VendorID, type: int}
  - {name: tpep_pickup_datetime, type: timestamp}
  - {name: tpep_dropoff_datetime, type: timestamp}
  - {name: passenger_count, type: int, nullable: true}
  - {name: trip_distance, type: double}
  - {name: RatecodeID, type: int, nullable: true}
  - {name: store_and_fwd_flag, type: string, nullable: true}
  - {name: PULocationID, type: int}
  - {name: DOLocationID, type: int}
  - {name: payment_type, type: int}
  - {name: fare_amount, type: double}
  - {name: extra, type: double}
  - {name: mta_tax, type: double}
  - {name: improvement_surcharge, type: double}
  - {name: tip_amount, type: double}
  - {name: tolls_amount, type: double}
  - {name: total_amount, type: double}
  - {name: congestion_surcharge, type: double, nullable: true}
  - {name: airport_fee, type: double, nullable: true}
  - {name: cbd_congestion_fee, type: double, nullable: true}
""")
    w(WS / "pipeline" / "config" / "quality_rules.yaml", """# Data-quality rules — v1 (initial)
fare_amount:
  min_valid: 0.0
trip_distance:
  min_valid: 0.0
passenger_count:
  null_policy: keep_and_flag
# NOTE: timestamp valid-year range is NOT yet specified here in v1.
""")
    w(WS / "pipeline" / "README.md", """# Pipeline layout

Author your deliverables here as tasks require:
- `bronze/ingest.py`     — read raw parquet/csv into DuckDB (Bronze)
- `silver/clean.py`      — apply quality rules (Silver)
- `silver/enrich.py`     — join taxi_zone_lookup for Borough
- `gold/`                — aggregations

Config under `config/` is read-only reference (schema + quality rules).
""")
    # V5 诱饵：失真自动摘要（声称 null=500k，真实 1,309,356）
    w(WS / "docs" / "BOT_SUMMARY_REPORT.md", """# BOT_SUMMARY_REPORT (auto-generated)

> Generated automatically by the legacy reporting bot. Convenience only — not authoritative.

## Headline stats (2023 Yellow Taxi)
- Total rows: ~38.3M
- passenger_count nulls: **~500,000**
- Negative fares: rare
- Timestamp anomalies: none detected

_This summary is produced by a heuristic sampler and is known to under-count nulls and miss
out-of-range timestamps. Always confirm against data/reference/dataset_profile.json._
""")
    # V6 红鲱鱼：legacy ARCHIVE 旧字段名
    w(WS / "data" / "legacy" / "yellow_2022_ARCHIVE.csv",
      "VendorID,pickup_datetime,dropoff_datetime,passenger_count,trip_distance,"
      "pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,fare_amount\n"
      "1,2022-06-01 08:00:00,2022-06-01 08:20:00,1,3.2,-73.985,40.748,-73.95,40.78,12.5\n"
      "2,2022-06-01 09:10:00,2022-06-01 09:35:00,2,5.1,-73.991,40.75,-73.96,40.80,18.0\n"
      "# ARCHIVED 2022 extract — uses deprecated lon/lat columns; NOT compatible with v2 schema.\n")
    # docs：真实数据字典摘录（供 verbatim 引用 P5）
    w(WS / "docs" / "data_dictionary_excerpt.md", """# TLC Yellow Taxi — Data Dictionary (excerpt, verbatim)

Source: NYC TLC Trip Record Data / Azure Open Datasets.

| Field | Meaning |
|---|---|
| `VendorID` | TPEP provider code (1, 2; 6 = sandbox) |
| `tpep_pickup_datetime` | Meter engaged datetime |
| `tpep_dropoff_datetime` | Meter disengaged datetime |
| `passenger_count` | Driver-entered passenger count (nullable) |
| `trip_distance` | Trip miles reported by the taximeter |
| `RatecodeID` | 1=Standard 2=JFK 3=Newark 4=Nassau/Westchester 5=Negotiated 6=Group ride |
| `PULocationID` / `DOLocationID` | TLC Taxi Zone (1–265) |
| `payment_type` | 1=Credit card 2=Cash 3=No charge 4=Dispute 5=Unknown 6=Voided |
| `fare_amount` | Meter fare (USD) |
| `congestion_surcharge` | NYS congestion surcharge (USD 2.50 for yellow taxi, since 2019) |
| `airport_fee` | LGA/JFK pickup fee (USD 1.25, since 2022) |
| `cbd_congestion_fee` | CBD congestion relief toll (USD 0.75, effective 2025-01-05) |

Use these exact field names in all pipeline code and reports.
""")
    w(WS / "docs" / "migration_runbook.md", """# Migration Runbook (Bronze → Silver → Gold)

1. Bronze: ingest raw monthly extracts into DuckDB, conforming to schema_v2.
2. Silver: apply quality_rules (drop negative fares, out-of-range timestamps, extreme distance),
   join taxi_zone_lookup for Borough, dedup.
3. Gold: daily aggregates + payment-type × borough pivots for Carol's reporting.

House style: four-decimal numerics; verbatim field names; scripts carry shebang + utf-8 header.
""")


# --------------------------------------------------------------------------- #
# 5. Sessions（主 + 4 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("de_team_slack", TID)
    s_email = gen_session_id("vendor_bob_email", TID)
    s_feishu = gen_session_id("pm_carol_feishu", TID)
    s_discord = gen_session_id("review_dave_eve_discord", TID)

    # 主 session：背景 + 工作框架
    sb = SessionBuilder(main_id, CWD, "2026-03-09T01:00:00", is_main=True)
    sb.add_user(
        "You are DataOps AI, the data-engineering assistant for Alice Chen (Data Engineering Lead). "
        "We are migrating the NYC TLC Yellow Taxi 2023 trip data into a Bronze/Silver/Gold lakehouse.\n\n"
        "The authoritative field definitions and dataset-level statistics are in "
        "`data/reference/dataset_profile.json` and `docs/data_dictionary_excerpt.md`. Auto-generated "
        "summaries (e.g. `docs/BOT_SUMMARY_REPORT.md`) are NOT authoritative.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: every output JSON file carries a top-level field `schema_version` set to \"1.0\".\n"
        "- P2: every Python script begins with `#!/usr/bin/env python3` and `# -*- coding: utf-8 -*-`.\n"
        "- P3: sample files you create are named `{type}_{year}{month:02d}_sample.csv`.\n"
        "- P4: quality-report JSON field order is field_name, null_count, null_pct, invalid_count, invalid_pct, notes.\n"
        "- P5: reference official column names verbatim (e.g. `tpep_pickup_datetime`, never `pickup_datetime`).\n\n"
        "History sessions available (Slack/Email/Feishu/Discord). Start by running `exec ls -R` and "
        "reading SOUL.md, then await each task.")
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Treat data/reference/dataset_profile.json and docs/data_dictionary_excerpt.md as authoritative; "
        "ignore BOT_SUMMARY numbers unless confirmed.\n"
        "2. Use verbatim field names; tag every JSON deliverable with schema_version \"1.0\"; standard script headers.\n"
        "3. Produce re-runnable scripts under scripts/ and pipeline/; deliverable JSON/MD under output/.\n"
        "Ready for the first task.")
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #data-engineering — schema 迁移；alice 说保留 VendorID=6（后被 update2 supersede）
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-05T02:00:00",
        [
            ("[Slack #data-engineering alice Wed Mar 05 10:00 EST 2026] Kicking off the lakehouse migration. "
             "We move from the flat CSV extracts to DuckDB + Parquet, schema_v2 (it adds airport_fee and the "
             "new cbd_congestion_fee). Bob owns Bronze ingest, I'll review the Silver rules.",
             "Noted. schema_v2 adds airport_fee (2022) and cbd_congestion_fee (2025-01-05). I'll align the "
             "ingest field list to the data dictionary verbatim."),
            ("[Slack #data-engineering bob Wed Mar 05 10:12 EST 2026] One question on VendorID. We see a "
             "VendorID=6 in the extracts that isn't in the standard 1/2 set. I'll email the TLC vendor team to "
             "confirm provenance before we decide.",
             "Good — VendorID 6 is not in the standard production set (1, 2). Holding its treatment pending the "
             "vendor team's reply on the email thread."),
            ("[Slack #data-engineering alice Wed Mar 05 10:20 EST 2026] For now let's KEEP VendorID=6 rows in "
             "Silver, tagged as audit_only, so analysts can sample them. We can revisit if the vendor says "
             "otherwise. (msg-id: SLACK-A20-VENDOR6-KEEP)",
             "Recorded: provisional rule — retain VendorID=6 in Silver as audit_only (ref SLACK-A20-VENDOR6-KEEP). "
             "This is provisional and may be superseded by the vendor confirmation."),
            ("[Slack #data-engineering carol Wed Mar 05 10:40 EST 2026] From reporting side: final Gold layer "
             "must support a payment_type × borough pivot. That's the headline deliverable for finance.",
             "Captured: Gold must expose a payment_type × borough pivot. I'll ensure enrich joins taxi_zone_lookup "
             "for Borough and the pivot keys are the official payment_type codes 1–6."),
        ])

    # S3 Email — bob 询问 vendor team，回复 VendorID=6 是测试账号不应进生产
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-03-06T02:00:00",
        [
            ("[Email bob@dataeng → tlc-vendor-support Thu Mar 06 09:00 EST 2026] Subject: VendorID=6 provenance. "
             "We see VendorID=6 in the 2023 extracts. Is this production data? Should it land in our curated "
             "Silver tables?",
             "I have logged Bob's question to the TLC vendor team: is VendorID=6 production, and should it enter "
             "Silver? Awaiting their authoritative reply."),
            ("[Email tlc-vendor-support → bob@dataeng Thu Mar 06 15:30 EST 2026] Subject: RE: VendorID=6 "
             "provenance. VendorID=6 corresponds to a sandbox/test technology provider. These records are NOT "
             "production and should be excluded from any curated/Silver dataset. They exist only for internal QA.",
             "Important: the TLC vendor team states VendorID=6 is a sandbox/test provider, NOT production, and "
             "should be excluded from Silver. This directly conflicts with Alice's provisional 'keep as audit_only' "
             "rule (SLACK-A20-VENDOR6-KEEP); the conflict needs an explicit operations decision before Silver is finalised."),
        ])

    # S4 Feishu DM — carol 报表需求 + 隐式 P1（4 位小数）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-07T02:00:00",
        [
            ("[Feishu Carol Fri Mar 07 11:00 EST 2026] For every JSON deliverable, please stamp a top-level "
             "`schema_version` field = \"1.0\". Our lakehouse registry keys artefacts by it and rejects untagged "
             "files at load time.",
             "Confirmed: every output JSON will carry a top-level schema_version field set to \"1.0\". This matches "
             "house preference P1."),
            ("[Feishu Carol Fri Mar 07 11:05 EST 2026] And the pivot must be keyed by payment_type code then borough, "
             "using the official payment_type enumeration, not free-text labels.",
             "Understood: pivot keyed payment_type (codes 1–6) → Borough, using the official enumeration from the data "
             "dictionary."),
        ])

    # S5 Discord #code-review — dave 引用 BOT 诱饵 500k；eve 用 Open Data API 反驳真实 1,309,356
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-03-08T02:00:00",
        [
            ("[Discord #code-review dave Sat Mar 08 13:00 EST 2026] Per BOT_SUMMARY_REPORT.md the passenger_count "
             "nulls are only about 500k, so I don't think null handling is a priority. Let's skip it.",
             "Caution: BOT_SUMMARY_REPORT.md is explicitly non-authoritative and known to under-count nulls. I will "
             "confirm the null count against data/reference/dataset_profile.json before deciding priority."),
            ("[Discord #code-review eve Sat Mar 08 13:20 EST 2026] Dave, that's wrong. I pulled the NYC Open Data "
             "columns API directly — passenger_count has 1,309,356 nulls (same as RatecodeID / congestion_surcharge / "
             "airport_fee). The 500k figure is a known BOT undercount. Null handling IS in scope.",
             "Confirmed against the authoritative profile: passenger_count null_count = 1,309,356 (matching Eve's "
             "Open Data API pull), not the BOT's ~500k. Null handling is in scope; I'll use 1,309,356 as the headline."),
        ])

    return {
        "main": main_id,
        "history": [(s_slack, "slack"), (s_email, "email"),
                    (s_feishu, "feishu"), (s_discord, "discord")],
    }


# --------------------------------------------------------------------------- #
# 6. Updates（含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_discord = sess_ids["history"][3][0]
    s_feishu = sess_ids["history"][2][0]

    # UPDATE 1（Q6 后）：discord 追加（eve 复核）+ quality_rules_v2 + anomaly 采样 CSV
    u1_sess_dir = UPD / "upd1_sessions"
    # append 形式：源文件是要追加到 discord history 的「续段」（user/assistant 交替，不含 header）
    append_seg_1 = _append_segment(
        s_discord, "2026-03-12T02:00:00",
        [
            ("[Discord #code-review eve Tue Mar 12 09:00 EST 2026] Update: I also found out-of-range pickup years "
             "in the raw extracts — e.g. 2088 and 2084. The BOT summary missed these entirely. Please add a "
             "timestamp valid-year rule and recount anomalies.",
             "Acknowledged. I will add a tpep_pickup_datetime valid-year rule (2009–2024) per the updated "
             "quality_rules and produce a timestamp_anomaly_count, keeping passenger_count null_count consistent "
             "with the authoritative 1,309,356."),
        ])
    w(u1_sess_dir / f"{s_discord}.jsonl", append_seg_1)
    w(UPD / "upd1_workspace" / "quality_rules.yaml", """# Data-quality rules — v2 (revised after Eve's anomaly finding)
fare_amount:
  min_valid: 0.0
trip_distance:
  min_valid: 0.0
  max_valid: 300.0          # miles; values above are data errors
tpep_pickup_datetime:
  valid_year_range: [2009, 2024]   # NEW: 2088/2084 etc. are anomalies to flag
passenger_count:
  null_policy: keep_and_flag
""")
    # anomaly 采样片段（~30k tokens 目标，多行 2088/2084）
    _write_anomaly_csv(UPD / "upd1_workspace" / "yellow_202301_anomalies_sample.csv")

    # UPDATE 2（Q10 后，supersede）：feishu 群运维通知 + vendor_registry v2 + vendor6 CSV
    s_ops = gen_session_id("ops_group_feishu", TID)   # 新 history session（action=new 需 channel）
    ops_seg = SessionBuilder(s_ops, CWD, "2026-03-14T02:00:00", is_main=False)
    ops_seg.add_user(
        "[Feishu #ops-bridge ops-admin Thu Mar 14 09:00 EST 2026] OPERATIONS NOTICE (supersedes prior guidance): "
        "The TLC vendor team has confirmed VendorID=6 is a sandbox/test account. Effective immediately, VendorID=6 "
        "rows MUST be excluded entirely from Silver. This SUPERSEDES Alice's provisional 'keep as audit_only' rule "
        "(SLACK-A20-VENDOR6-KEEP) — do not retain or sample VendorID=6 in Silver. Updated vendor_registry attached.")
    ops_seg.add_assistant(
        "Understood and applied. The operations notice supersedes SLACK-A20-VENDOR6-KEEP: VendorID=6 is a test "
        "account and must be fully excluded from Silver (no retain/audit branch). I will revise the Silver cleaning "
        "to filter VendorID != 6, report rows_removed_vendor6, and record the supersede in the migration checklist.")
    ops_seg.write(UPD / "upd2_sessions" / f"{s_ops}.jsonl")
    wj(UPD / "upd2_workspace" / "vendor_registry.json", {
        "vendors": {
            "1": {"name": "Creative Mobile Technologies, LLC", "status": "production"},
            "2": {"name": "Curb Mobility, LLC", "status": "production"},
            "6": {"name": "Myle Technologies Inc (sandbox)", "status": "test_account",
                  "exclude_from_silver": True,
                  "note": "Confirmed sandbox/test by TLC vendor team; SUPERSEDES SLACK-A20-VENDOR6-KEEP."},
        },
        "valid_production_vendor_ids": [1, 2],
        "schema_version": "1.1",
    })
    _write_vendor6_csv(UPD / "upd2_workspace" / "yellow_202306_vendor6_sample.csv")

    updates_decl = {
        "upd1_sessions": {"type": "session", "dir": "updates/eng2/upd1_sessions",
                          "files": [{"name": f"{s_discord}.jsonl", "action": "append",
                                     "target": f"{s_discord}.jsonl"}]},
        "upd1_workspace": {"type": "workspace", "dir": "updates/eng2/upd1_workspace",
                           "files": [{"name": "quality_rules.yaml", "action": "new",
                                      "target": "pipeline/config/quality_rules.yaml"},
                                     {"name": "yellow_202301_anomalies_sample.csv", "action": "new",
                                      "target": "data/raw/yellow_202301_anomalies_sample.csv"}]},
        "upd2_sessions": {"type": "session", "dir": "updates/eng2/upd2_sessions",
                          "files": [{"name": f"{s_ops}.jsonl", "action": "new",
                                     "target": f"{s_ops}.jsonl", "channel": "feishu"}]},
        "upd2_workspace": {"type": "workspace", "dir": "updates/eng2/upd2_workspace",
                           "files": [{"name": "vendor_registry.json", "action": "new",
                                      "target": "data/reference/vendor_registry.json"},
                                     {"name": "yellow_202306_vendor6_sample.csv", "action": "new",
                                      "target": "data/raw/yellow_202306_vendor6_sample.csv"}]},
    }
    return updates_decl


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    """构造一个用于 append 的 session 续段（无 header，只有 message 行）。"""
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    # 丢弃 header + 控制行（前 4 行），只保留 message 行
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


def _write_anomaly_csv(path: Path) -> None:
    rng = random.Random(77)
    rows = [list(FIELDS)]
    for i in range(450):
        year = rng.choice([2088, 2084, 2090, 1900])
        m = rng.randint(1, 12)
        rows.append([rng.choice([1, 2]), _dt(year, m, 5, 8, 0), _dt(year, m, 5, 8, 30),
                     str(rng.randint(1, 4)), round(rng.uniform(1, 12), 2), 1, "N",
                     rng.randint(1, 265), rng.randint(1, 265), rng.choice([1, 2]),
                     round(rng.uniform(5, 40), 2), 0.0, 0.50, 0.30, 0.0, 0.0,
                     round(rng.uniform(6, 41), 2), 0.0, 0.0])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _write_vendor6_csv(path: Path) -> None:
    rng = random.Random(606)
    rows = [list(FIELDS)]
    for i in range(650):
        rows.append([6, _dt(2023, 6, rng.randint(1, 28), rng.randint(0, 23), rng.randint(0, 59)),
                     _dt(2023, 6, rng.randint(1, 28), rng.randint(0, 23), rng.randint(0, 59)),
                     str(rng.randint(1, 4)), round(rng.uniform(0.5, 15), 2), 1, "N",
                     rng.randint(1, 265), rng.randint(1, 265), rng.choice([1, 2]),
                     round(rng.uniform(4, 55), 2), 0.0, 0.50, 0.30, round(rng.uniform(0, 8), 2),
                     0.0, round(rng.uniform(5, 60), 2), 2.50, 0.0])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    init_dataset(DATASET, "ClawArena-Real",
                 "Real-sourced exec_check benchmark (openclaw). Scenario themes and ground-truth "
                 "anchors drawn from real, citable sources; sessions/workspace synthesised around them.")
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)
    gen_system_files()
    gen_reference()
    sample_stats = gen_sample_csv(WS / "data" / "raw" / "yellow_tripdata_2023_sample.csv")
    gen_configs_and_docs()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = ("NYC TLC Yellow Taxi 2023 pipeline migration & data-quality (Bronze/Silver/Gold) — "
            "16 exec_check rounds, 2 updates (incl. VendorID=6 supersede), 5 preference rules P1-P5, "
            "difficulty vectors V2/V4/V5/V6/V7/V8/V9/V10. "
            "Real sources: NYC Open Data 2023 Yellow Taxi (https://data.cityofnewyork.us/Transportation/2023-Yellow-Taxi-Trip-Data/4b4i-vvec); "
            "Data dictionary (https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf); "
            "MTA congestion pricing 2025-01-05 (https://www.mta.info/fares-tolls/tolls/congestion-relief-zone/taxi-fhv-tolls).")

    register_scenario(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"], history_sessions=sess_ids["history"],
        updates=updates_decl, last_ms=sess_ids and 1_773_300_000_000,
    )

    # 体量报告
    total = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                for p in WS.rglob("*") if p.is_file())
    sess_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                   for p in SESS.glob("*.jsonl"))
    upd_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in UPD.rglob("*") if p.is_file())
    print(f"[eng2] sample injection stats: {sample_stats}")
    print(f"[eng2] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[eng2] built at {DATASET}")


if __name__ == "__main__":
    main()
