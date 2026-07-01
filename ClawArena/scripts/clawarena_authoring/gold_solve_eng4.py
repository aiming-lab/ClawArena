#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_eng4.py — eng4 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_eng4.py
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
WS_SRC = DS / "openclaw" / "workspaces" / "eng4"
UPD = DS / "openclaw" / "updates" / "eng4"
SCRIPTS = DS / "eval" / "eng4" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/eng4_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply Update 1 workspace files
    ep_after_src = UPD / "upd1_workspace" / "explain_plans"
    ep_after_dst = GOLD / "reports" / "explain_plans"
    ep_after_dst.mkdir(parents=True, exist_ok=True)
    for f in ep_after_src.glob("*.json"):
        shutil.copy(f, ep_after_dst / f.name)
    shutil.copy(
        UPD / "upd1_workspace" / "slow_query_report_week2.md",
        GOLD / "reports" / "slow_query_report_week2.md",
    )
    # Apply Update 2 workspace files
    ep_upd2_src = UPD / "upd2_workspace" / "explain_plans"
    if ep_upd2_src.exists():
        for f in ep_upd2_src.glob("*.json"):
            shutil.copy(f, ep_after_dst / f.name)
    shutil.copy(
        UPD / "upd2_workspace" / "slow_query_report_week3.md",
        GOLD / "reports" / "slow_query_report_week3.md",
    )
    shutil.copy(
        UPD / "upd2_workspace" / "recommended_settings_v2.conf",
        GOLD / "configs" / "recommended_settings_v2.conf",
    )
    return GOLD


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


def _wjl(p: Path, entries: list):
    """Write JSON Lines file (one JSON object per line)."""
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(e, ensure_ascii=False) for e in entries]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_pgstat_csv(ws: Path) -> list[dict]:
    csv_path = ws / "reports" / "pgstatstatements_snapshot.csv"
    with csv_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_explain_json(ws: Path, fname: str) -> dict | None:
    p = ws / "reports" / "explain_plans" / fname
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, list) and data:
        return data[0]
    return data


def get_plan_node(explain_entry: dict) -> dict:
    """Extract the top-level Plan node from an EXPLAIN JSON entry."""
    plan = explain_entry.get("Plan") or {}
    return plan


def solve(ws: Path) -> None:
    work = ws / "work"
    work.mkdir(exist_ok=True)

    # ------------------------------------------------------------------ #
    # Q1: Top-5 slow queries from pgstatstatements_snapshot.csv
    # ------------------------------------------------------------------ #
    rows = load_pgstat_csv(ws)
    slow = []
    for r in rows:
        try:
            met = float(r.get("mean_exec_time") or 0)
            if met > 500:
                slow.append({
                    "queryid": int(r["queryid"]),
                    "query_preview": str(r.get("query") or "")[:80],
                    "mean_exec_time_ms": round(met, 2),
                    "calls": int(r.get("calls") or 0),
                })
        except (ValueError, TypeError):
            pass
    slow.sort(key=lambda x: x["mean_exec_time_ms"], reverse=True)
    top5 = slow[:5]
    _wj(work / "slow_queries_top5.json", top5)

    # ------------------------------------------------------------------ #
    # Q2: Query-001 EXPLAIN analysis
    # ------------------------------------------------------------------ #
    q001_entry = load_explain_json(ws, "query_001_before.json")
    assert q001_entry is not None, "query_001_before.json not found"
    plan = get_plan_node(q001_entry)
    node_type = plan.get("Node Type", "Seq Scan")
    total_cost = float(plan.get("Total Cost", 2876543.20))
    plan_rows = int(plan.get("Plan Rows", 450))
    actual_rows = int(plan.get("Actual Rows", 24891))
    error_pct = round(abs(plan_rows - actual_rows) / max(actual_rows, 1) * 100, 2)
    q001_analysis = {
        "node_type": node_type,
        "total_cost": total_cost,
        "plan_rows": plan_rows,
        "actual_rows": actual_rows,
        "scan_type": node_type,
        "rows_estimate_error_pct": error_pct,
    }
    _wj(work / "q001_analysis.json", q001_analysis)

    # ------------------------------------------------------------------ #
    # Q3: Index recommendation for Query-001
    # ------------------------------------------------------------------ #
    _wj(work / "q001_index_recommendation.json", {
        "table_name": "events",
        "index_type": "btree",
        "columns": ["service_id", "created_at"],
        "where_clause": None,
        "rationale": (
            "Query-001 filters events by service_id (equality) and created_at (range). "
            "A composite B-Tree index on (service_id, created_at DESC) supports both predicates. "
            "Hash indexes support only = equality and cannot satisfy range queries on created_at. "
            "Reference: https://www.postgresql.org/docs/current/indexes-types.html (Index Types). "
            "High-selectivity column service_id placed first per composite index best practice. "
            "Source: https://www.postgresql.org/docs/current/using-explain.html"
        ),
    })

    # ------------------------------------------------------------------ #
    # Q4: DDL batch + optimization log
    # ------------------------------------------------------------------ #
    ddl_batch1 = """\
-- Batch 1: High-priority index creation (production-safe with CONCURRENTLY)
-- Reference: https://stormatics.tech/blogs/fixing-orm-slowness-by-80-with-strategic-postgresql-indexing

-- Query-001, Q-006: Composite index on events (service_id, created_at)
CREATE INDEX CONCURRENTLY idx_events_service_created ON events (service_id, created_at DESC);

-- Query-006: Composite index on events (service_id, event_type, created_at)
CREATE INDEX CONCURRENTLY idx_events_service_type_created ON events (service_id, event_type, created_at DESC);

-- Query-003: Partial index on events.status='active'
CREATE INDEX CONCURRENTLY idx_events_status_active ON events (status) WHERE status = 'active';

-- Query-002, Query-010: Index on orders.service_id
CREATE INDEX CONCURRENTLY idx_orders_service_id ON orders (service_id);

-- Query-004: Composite partial index on notifications (user_id, is_read) for unread queries
CREATE INDEX CONCURRENTLY idx_notifications_user_unread ON notifications (user_id, is_read) WHERE is_read = FALSE;

-- Query-007: Partial index on orders.billed IS NOT TRUE
CREATE INDEX CONCURRENTLY idx_orders_unbilled ON orders (order_nr) WHERE billed IS NOT TRUE;
"""
    _w(work / "index_ddl_batch1.sql", ddl_batch1)

    import datetime
    log_entries = [
        {
            "timestamp": "2026-01-20T02:00:00Z",
            "action": "create_index",
            "ddl": "CREATE INDEX CONCURRENTLY idx_events_service_created ON events (service_id, created_at DESC)",
            "rationale": "Fix Query-001: Seq Scan on events due to missing composite index on (service_id, created_at)",
        },
        {
            "timestamp": "2026-01-20T02:05:00Z",
            "action": "create_index",
            "ddl": "CREATE INDEX CONCURRENTLY idx_events_service_type_created ON events (service_id, event_type, created_at DESC)",
            "rationale": "Fix Query-006: Composite index for (service_id, event_type, created_at) filter",
        },
        {
            "timestamp": "2026-01-20T02:10:00Z",
            "action": "create_index",
            "ddl": "CREATE INDEX CONCURRENTLY idx_events_status_active ON events (status) WHERE status = 'active'",
            "rationale": "Fix Query-003: Partial index to avoid full-table COUNT for status='active'",
        },
        {
            "timestamp": "2026-01-20T02:15:00Z",
            "action": "create_index",
            "ddl": "CREATE INDEX CONCURRENTLY idx_orders_service_id ON orders (service_id)",
            "rationale": "Fix Query-002: Hash Join slow due to missing service_id index on orders",
        },
        {
            "timestamp": "2026-01-20T02:20:00Z",
            "action": "create_index",
            "ddl": "CREATE INDEX CONCURRENTLY idx_notifications_user_unread ON notifications (user_id, is_read) WHERE is_read = FALSE",
            "rationale": "Fix Query-004: Composite partial index for unread notification queries",
        },
        {
            "timestamp": "2026-01-20T02:25:00Z",
            "action": "create_index",
            "ddl": "CREATE INDEX CONCURRENTLY idx_orders_unbilled ON orders (order_nr) WHERE billed IS NOT TRUE",
            "rationale": "Fix Query-007: Partial index for unbilled order queries",
        },
    ]
    _wjl(work / "optimization_log.jsonl", log_entries)

    # ------------------------------------------------------------------ #
    # Q5: Archive review
    # ------------------------------------------------------------------ #
    _wj(work / "archive_review.json", {
        "is_outdated": True,
        "outdated_recommendations": [
            {
                "original_text": "CREATE INDEX idx_events_status_hash ON events (status) USING HASH",
                "reason_outdated": (
                    "Hash indexes in PostgreSQL support ONLY equality (=) operations. "
                    "They cannot satisfy range predicates (<, >, BETWEEN), ORDER BY, or GROUP BY. "
                    "Our events.status queries include WHERE status != 'deleted' and GROUP BY status, "
                    "which require B-Tree. Reference: https://www.postgresql.org/docs/current/indexes-types.html"
                ),
            },
            {
                "original_text": "CREATE INDEX idx_orders_billed_hash ON orders (billed) USING HASH",
                "reason_outdated": (
                    "Hash index on billed cannot support WHERE billed IS NOT TRUE (range/nullable predicate). "
                    "A Partial B-Tree index WHERE billed IS NOT TRUE is the correct approach. "
                    "Reference: https://www.postgresql.org/docs/current/indexes-types.html"
                ),
            },
            {
                "original_text": "work_mem = 256MB",
                "reason_outdated": (
                    "The work_mem=256MB recommendation was superseded by the architect. "
                    "A global increase is unsafe (max_connections × work_mem = large memory pressure). "
                    "The correct fix for Query-010 is CREATE STATISTICS."
                ),
            },
        ],
        "valid_recommendations": [
            "CREATE INDEX ON events (created_at) — B-Tree for range queries (already exists)",
            "Increase default_statistics_target for high-cardinality columns",
        ],
    })

    # ------------------------------------------------------------------ #
    # Q6: Query-004 statistics analysis
    # n_distinct = -0.23 (from seed_stats.sql), correlation = 0.12
    # ------------------------------------------------------------------ #
    q004_entry = load_explain_json(ws, "query_004_before.json")
    assert q004_entry is not None, "query_004_before.json not found"
    plan4 = get_plan_node(q004_entry)
    actual_rows4 = int(plan4.get("Actual Rows", 3421))
    plan_rows4 = int(plan4.get("Plan Rows", 1))
    notif_total = 12000000
    _wj(work / "q004_stats_analysis.json", {
        "table_name": "notifications",
        "column_name": "is_read",
        "n_distinct": -0.23,
        "correlation": 0.12,
        "estimated_selectivity": round(plan_rows4 / notif_total, 8),
        "actual_selectivity": round(actual_rows4 / notif_total, 8),
        "diagnosis": "stale_statistics",
    })

    # ------------------------------------------------------------------ #
    # Q7: Before/after comparison for Q1-Q9
    # ------------------------------------------------------------------ #
    query_pairs = [
        ("query_001", "query_001_before.json", "query_001_after.json"),
        ("query_002", "query_002_before.json", "query_002_after.json"),
        ("query_003", "query_003_before.json", "query_003_after.json"),
        ("query_004", "query_004_before.json", "query_004_after.json"),
        ("query_005", "query_005_before.json", "query_005_after.json"),
        ("query_006", "query_006_before.json", "query_006_after.json"),
        ("query_007", "query_007_before.json", "query_007_after.json"),
        ("query_008", "query_008_before.json", "query_008_after.json"),
        ("query_009", "query_009_before.json", "query_009_after.json"),
    ]
    results = []
    for qid, before_f, after_f in query_pairs:
        before_entry = load_explain_json(ws, before_f)
        after_entry = load_explain_json(ws, after_f)
        if before_entry is None or after_entry is None:
            continue
        bp = get_plan_node(before_entry)
        ap = get_plan_node(after_entry)
        bef_cost = float(bp.get("Total Cost", 0))
        aft_cost = float(ap.get("Total Cost", 0))
        crp = round((bef_cost - aft_cost) / max(bef_cost, 0.001) * 100, 2)
        bef_time = float(before_entry.get("Execution Time") or bp.get("Actual Total Time") or 0)
        aft_time = float(after_entry.get("Execution Time") or ap.get("Actual Total Time") or 0)
        results.append({
            "query_id": qid,
            "before_node_type": bp.get("Node Type", ""),
            "after_node_type": ap.get("Node Type", ""),
            "before_total_cost": bef_cost,
            "after_total_cost": aft_cost,
            "cost_reduction_pct": crp,
            "before_actual_time_ms": bef_time,
            "after_actual_time_ms": aft_time,
        })
    _wj(work / "optimization_comparison.json", {"results": results})

    # ------------------------------------------------------------------ #
    # Q8: Query-010 join analysis (has_disk_spill=true, initial rec=increase_work_mem)
    # ------------------------------------------------------------------ #
    q010_entry = load_explain_json(ws, "query_010_before.json")
    # Q8 writes initial state; Q10 will overwrite recommendation
    if q010_entry is not None:
        plan10 = get_plan_node(q010_entry)
        # Drill into nested plan to find Hash Join node
        def find_hash_join(node):
            if isinstance(node, dict):
                if node.get("Node Type") == "Hash Join":
                    return node
                for v in node.values():
                    r = find_hash_join(v)
                    if r:
                        return r
            elif isinstance(node, list):
                for item in node:
                    r = find_hash_join(item)
                    if r:
                        return r
            return None
        hj_node = find_hash_join(plan10) or plan10
        batches = int(hj_node.get("Batches") or hj_node.get("Hash Batches") or 8)
        sort_method = str(hj_node.get("Sort Method") or "")
        has_disk = batches > 1 or "external" in sort_method.lower()
        _wj(work / "q010_join_analysis.json", {
            "join_type": "Hash Join",
            "hash_batches": batches,
            "has_disk_spill": has_disk,
            "spill_size_kb": 491520 if has_disk else 0,
            "recommendation": "increase_work_mem",  # Q8 initial; overwritten in Q10
        })
    else:
        # Fallback using known values from BRIEF
        _wj(work / "q010_join_analysis.json", {
            "join_type": "Hash Join",
            "hash_batches": 8,
            "has_disk_spill": True,
            "spill_size_kb": 491520,
            "recommendation": "increase_work_mem",
        })

    # ------------------------------------------------------------------ #
    # Q9: Partial index for Query-011
    # ------------------------------------------------------------------ #
    _w(work / "q011_partial_index.sql", """\
-- q011_partial_index.sql
-- Partial Index for Query-011: unbilled orders queries
-- Reference: https://www.postgresql.org/docs/current/indexes-partial.html
-- Official example: CREATE INDEX orders_unbilled_index ON orders(order_nr) WHERE billed IS NOT TRUE

CREATE INDEX CONCURRENTLY idx_orders_q011_unbilled
    ON orders (order_nr, created_at)
    WHERE billed IS NOT TRUE;
""")
    _w(work / "q011_partial_index_rationale.md", """\
# Partial Index Rationale for Query-011

## Query
```sql
SELECT order_nr, amount_cents FROM orders WHERE billed IS NOT TRUE ORDER BY created_at LIMIT 5000
```

## Why a Partial Index?

A full B-Tree index on `orders(billed)` would index all 5 million rows (both TRUE and FALSE).
Since approximately 44% of orders are not yet billed, a standard index would still be large and
provide limited benefit over a sequential scan for 44% of 5M = 2.2M rows.

A Partial Index with `WHERE billed IS NOT TRUE` indexes ONLY the ~2.2M unbilled rows,
making it significantly smaller and faster for queries that specifically target unbilled records.

## Reference

PostgreSQL official documentation on Partial Indexes:
https://www.postgresql.org/docs/current/indexes-partial.html

The official example from the docs:
```sql
CREATE INDEX orders_unbilled_index ON orders (order_nr) WHERE billed IS NOT TRUE;
```

This exact pattern applies to our Query-011. The partial predicate must match the query
WHERE clause for the planner to use the index.

## Expected Improvement

- Before: Seq Scan on 5M rows, actual_rows=89,234, cost=98,432.11
- After: Index Scan on partial index (~2.2M rows), estimated cost ~1,234.55
""")

    # ------------------------------------------------------------------ #
    # Q10: Apply supersede — change recommendation to create_statistics
    # ------------------------------------------------------------------ #
    _wj(work / "q010_join_analysis.json", {
        "join_type": "Hash Join",
        "hash_batches": 8,
        "has_disk_spill": True,
        "spill_size_kb": 491520,
        "recommendation": "create_statistics",
    })
    _w(work / "q010_create_statistics.sql", """\
-- q010_create_statistics.sql
-- CREATE STATISTICS for Query-010 optimization (replaces work_mem=256MB directive)
-- Architect's supersede: do NOT modify global work_mem
-- Reference: https://www.postgresql.org/docs/current/planner-stats.html
-- Reference: https://render.com/blog/postgresql-slow-query-to-fast-via-stats

CREATE STATISTICS finedge_events_service_stats (dependencies)
    ON service_id, created_at
    FROM events;

-- After creating the statistics, run ANALYZE to populate them:
-- ANALYZE events;

-- This enables the planner to understand the functional dependency between
-- service_id and created_at in the events table, allowing it to choose
-- a more efficient join algorithm for Query-010 instead of a full Hash Join
-- that spills to disk.
""")

    # ------------------------------------------------------------------ #
    # Q11: Covering index for Query-012
    # ------------------------------------------------------------------ #
    _w(work / "q012_covering_index.sql", """\
-- q012_covering_index.sql
-- Covering Index with INCLUDE clause for Query-012
-- Reference: https://www.postgresql.org/docs/current/indexes-index-only-scans.html
-- Syntax: CREATE INDEX tab_x_y ON tab(x) INCLUDE (y) — B-Tree, GiST, SP-GiST support INCLUDE
-- GIN does NOT support Index-Only Scan

CREATE INDEX CONCURRENTLY idx_users_email_covering
    ON users (email)
    INCLUDE (name, updated_at);

-- This enables Index Only Scan for queries like:
-- SELECT u.email, u.name, u.updated_at FROM users WHERE u.email = $1
-- Eliminates heap fetches for name and updated_at columns.
""")

    # ------------------------------------------------------------------ #
    # Q12: Scan type summary (total_queries=12)
    # ------------------------------------------------------------------ #
    # Build distribution from all 12 explain files
    all_queries = [
        "query_001_after.json", "query_002_after.json", "query_003_after.json",
        "query_004_after.json", "query_005_after.json", "query_006_after.json",
        "query_007_after.json", "query_008_after.json", "query_009_after.json",
        "query_010_before.json", "query_011_before.json", "query_012_before.json",
    ]
    query_ids_12 = [
        "query_001", "query_002", "query_003", "query_004", "query_005", "query_006",
        "query_007", "query_008", "query_009", "query_010", "query_011", "query_012",
    ]
    scan_dist: dict = {}
    seq_scan_remaining = []

    def to_snake(s: str) -> str:
        """Convert 'Index Only Scan' -> 'index_only_scan' for snake_case key storage."""
        return s.lower().replace(" ", "_")

    for i, (fname, qid) in enumerate(zip(all_queries, query_ids_12)):
        entry = load_explain_json(ws, fname)
        if entry is None:
            scan_dist["unknown"] = scan_dist.get("unknown", 0) + 1
            continue
        plan_node = get_plan_node(entry)
        nt = plan_node.get("Node Type", "Unknown")
        nt_key = to_snake(nt)
        scan_dist[nt_key] = scan_dist.get(nt_key, 0) + 1
        if "seq_scan" in nt_key:
            seq_scan_remaining.append(qid)
    _wj(work / "scan_type_summary.json", {
        "total_queries": 12,
        "scan_type_distribution": scan_dist,
        "seq_scan_remaining": seq_scan_remaining,
    })

    # ------------------------------------------------------------------ #
    # Q13: ANALYZE plan for notifications
    # ------------------------------------------------------------------ #
    _wj(work / "analyze_plan.json", {
        "tables_need_analyze": [
            {
                "table_name": "notifications",
                "reason": "Bulk DELETE of 3.2M rows on 2026-01-28 left stale statistics. "
                          "n_dead_tup=2,345,678 (19.5% of live rows). "
                          "last_autovacuum=2026-01-10 (22 days ago) — autovacuum did not trigger post-bulk-delete. "
                          "Stale statistics cause planner to underestimate row counts.",
                "last_autovacuum": "2026-01-10 01:30:00+00",
                "n_dead_tup": 2345678,
            }
        ]
    })
    _w(work / "run_analyze.sh", """\
#!/bin/bash
# run_analyze.sh
# Manually ANALYZE tables with stale statistics after bulk operations
# Reference: https://www.postgresql.org/docs/current/planner-stats.html

set -euo pipefail

PGCONN="${PGCONN:-postgres://localhost:5432/finedge_prod}"

echo "Running ANALYZE on tables with stale statistics..."

psql "$PGCONN" <<'SQL'
-- notifications: 3.2M rows deleted on 2026-01-28; last_autovacuum 22 days ago
ANALYZE notifications;

-- Also run ANALYZE events to populate new CREATE STATISTICS
ANALYZE events;

-- Check updated stats
SELECT relname, last_autoanalyze, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE relname IN ('notifications', 'events')
ORDER BY relname;
SQL

echo "ANALYZE complete."
""")

    # ------------------------------------------------------------------ #
    # Q14: Final optimization report + SHA-256 sign-off
    # ------------------------------------------------------------------ #
    # Load optimization_log.jsonl to get indexes_created count
    log_txt = (work / "optimization_log.jsonl").read_text(encoding="utf-8")
    log_entries_loaded = [json.loads(l) for l in log_txt.splitlines() if l.strip()]
    indexes_created_ddls = [e["ddl"] for e in log_entries_loaded if e.get("ddl")]

    final_report = {
        "total_queries_optimized": 12,
        "work_mem_modified": False,
        "indexes_created": indexes_created_ddls,
        "statistics_created": [
            "CREATE STATISTICS finedge_events_service_stats (dependencies) ON service_id, created_at FROM events"
        ],
        "seq_scan_remaining_count": len(seq_scan_remaining),
        "optimization_summary": {
            "batch_1_queries": ["query_001", "query_002", "query_003", "query_004",
                                "query_005", "query_006", "query_007"],
            "batch_2_queries": ["query_008", "query_009", "query_011", "query_012"],
            "statistics_fix": ["query_010"],
            "supersede_applied": "CTO work_mem=256MB directive superseded by Principal Architect Maya Lin; CREATE STATISTICS used instead",
        },
    }
    report_path = work / "final_optimization_report.json"
    _wj(report_path, final_report)

    # Compute SHA-256 of the exact bytes of final_optimization_report.json
    digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    _w(work / "signoff.txt", f"VERIFIED:{digest}\n")


# --------------------------------------------------------------------------- #
# Run checks
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1,P2", "work/slow_queries_top5.json")],
    "q2": ["check_q2.py", ("pref", "P1,P2", "work/q001_analysis.json")],
    "q3": ["check_q3.py", ("pref", "P1,P2,P3", "work/q001_index_recommendation.json")],
    "q4": ["check_q4.py", ("pref", "P1,P4", "work/index_ddl_batch1.sql")],
    "q5": ["check_q5.py", ("pref", "P1,P2", "work/archive_review.json")],
    "q6": ["check_q6.py", ("pref", "P1,P2", "work/q004_stats_analysis.json")],
    "q7": ["check_q7.py", ("pref", "P1,P2", "work/optimization_comparison.json")],
    "q8": ["check_q8.py", ("pref", "P1,P2", "work/q010_join_analysis.json")],
    "q9": ["check_q9.py", ("pref", "P1,P4,P5", "work/q011_partial_index.sql")],
    "q10": ["check_q10.py", ("pref", "P1", "work/q010_create_statistics.sql")],
    "q11": ["check_q11.py", ("pref", "P1,P4", "work/q012_covering_index.sql")],
    "q12": ["check_q12.py", ("pref", "P1,P2", "work/scan_type_summary.json")],
    "q13": ["check_q13.py"],
    "q14": ["check_q14.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    last = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""
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
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ------------------------------------------------------------------ #
    # Negative probes
    # ------------------------------------------------------------------ #
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Probe 1: Q6 — use bot-decoy n_distinct=-1 instead of correct -0.23
    _wj(ws / "work" / "q004_stats_analysis.json", {
        "table_name": "notifications",
        "column_name": "is_read",
        "n_distinct": -1.0,
        "correlation": 0.12,
        "estimated_selectivity": 0.0000001,
        "actual_selectivity": 0.000285,
        "diagnosis": "stale_statistics",
    })
    ok, _ = run_check("check_q6.py", ws); probes += 1; caught += (not ok)
    print(f"  q6 bot-decoy n_distinct=-1.0 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore
    _wj(ws / "work" / "q004_stats_analysis.json", {
        "table_name": "notifications",
        "column_name": "is_read",
        "n_distinct": -0.23,
        "correlation": 0.12,
        "estimated_selectivity": round(1 / 12000000, 8),
        "actual_selectivity": round(3421 / 12000000, 8),
        "diagnosis": "stale_statistics",
    })

    # Probe 2: Q3 — use hash index type (wrong for range query)
    _wj(ws / "work" / "q001_index_recommendation.json", {
        "table_name": "events",
        "index_type": "hash",
        "columns": ["service_id"],
        "where_clause": None,
        "rationale": "Hash indexes are O(1) for equality https://www.postgresql.org/docs/current/indexes-types.html",
    })
    ok, _ = run_check("check_q3.py", ws); probes += 1; caught += (not ok)
    print(f"  q3 hash index type -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore
    _wj(ws / "work" / "q001_index_recommendation.json", {
        "table_name": "events",
        "index_type": "btree",
        "columns": ["service_id", "created_at"],
        "where_clause": None,
        "rationale": "B-Tree required for range queries. https://www.postgresql.org/docs/current/indexes-types.html",
    })

    # Probe 3: Q10 — wrong recommendation (increase_work_mem not superseded)
    _wj(ws / "work" / "q010_join_analysis.json", {
        "join_type": "Hash Join",
        "hash_batches": 8,
        "has_disk_spill": True,
        "spill_size_kb": 491520,
        "recommendation": "increase_work_mem",
    })
    ok, _ = run_check("check_q10.py", ws); probes += 1; caught += (not ok)
    print(f"  q10 increase_work_mem (not superseded) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore
    _wj(ws / "work" / "q010_join_analysis.json", {
        "join_type": "Hash Join",
        "hash_batches": 8,
        "has_disk_spill": True,
        "spill_size_kb": 491520,
        "recommendation": "create_statistics",
    })

    # Probe 4: Q14 — placeholder hash in signoff
    report_path = ws / "work" / "final_optimization_report.json"
    _w(ws / "work" / "signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q14.py", ws); probes += 1; caught += (not ok)
    print(f"  q14 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore signoff
    digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    _w(ws / "work" / "signoff.txt", f"VERIFIED:{digest}\n")

    # Probe 5: Q1 — wrong array length (4 instead of 5)
    orig_top5 = json.loads((ws / "work" / "slow_queries_top5.json").read_text())
    _wj(ws / "work" / "slow_queries_top5.json", orig_top5[:4])
    ok, _ = run_check("check_q1.py", ws); probes += 1; caught += (not ok)
    print(f"  q1 array length 4 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore
    _wj(ws / "work" / "slow_queries_top5.json", orig_top5)

    # Probe 6: Q5 — is_outdated=false
    _wj(ws / "work" / "archive_review.json", {
        "is_outdated": False,
        "outdated_recommendations": [],
        "valid_recommendations": ["Use Hash indexes for status column"],
    })
    ok, _ = run_check("check_q5.py", ws); probes += 1; caught += (not ok)
    print(f"  q5 is_outdated=false -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore
    _wj(ws / "work" / "archive_review.json", {
        "is_outdated": True,
        "outdated_recommendations": [
            {
                "original_text": "CREATE INDEX idx_events_status_hash ON events (status) USING HASH",
                "reason_outdated": "Hash indexes support only = equality, not range queries. https://www.postgresql.org/docs/current/indexes-types.html",
            }
        ],
        "valid_recommendations": [],
    })

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
