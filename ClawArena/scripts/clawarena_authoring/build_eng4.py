#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_eng4.py — 生成 ClawArena 真实数据集场景 eng4（数据库慢查询与索引优化）。

题材与锚点取材自 PostgreSQL 官方文档（runtime-config-query、pgstatstatements、
indexes-partial、indexes-index-only-scans 等）与真实案例分析（Render/depesz/Cubbit）。
场景：FinEdge Analytics DBA 工程师 Li Wei 对 PostgreSQL 16 数据库进行慢查询诊断与索引优化。

全 exec_check，14 轮，2 次 update（含 supersede：Update 2 撤销 Update 1 中的 work_mem 建议）。

幂等：开头清空 eng4 的 workspace/state/updates 后重建，末尾调用 dump_register_meta 写 _register.json。
questions.json 与 check 脚本由 eval/eng4/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_eng4.py
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
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "eng4"
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

1. Read `SOUL.md` for working principles and tool policies.
2. Read `USER.md` to learn about team members and communication channels.
3. Run `exec ls -R` to inspect the current workspace layout.
4. Use `sessions_list` to discover available history sessions, then `sessions_history` to review as needed.

You are **DBOps AI**, a database optimization assistant supporting Li Wei (DBA Engineer) at FinEdge Analytics.
The database is PostgreSQL 16 running on SSD-backed instances. The primary schema includes:
- `events` (~90 million rows, event-stream table)
- `orders` (~5 million rows, transactional table)
- `notifications` (~12 million rows, user notification table)
- `users`, `products`, `categories`, `audit_log`, `service_config` (auxiliary tables)
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: Ground-truth query plans and statistics live in
   `reports/explain_plans/` and `reports/pgstatstatements_snapshot.csv`. Bot-generated
   summaries (e.g. files named `*BOT*` or from the internal Slack bot) are convenience
   artefacts and NOT authoritative — verify any number against the actual EXPLAIN JSON or
   pg_stat_statements snapshot.

2. **Verbatim PostgreSQL identifiers**: Use exact parameter names from the PostgreSQL docs
   (e.g. `seq_page_cost`, `random_page_cost`, `cpu_tuple_cost`, `default_statistics_target`).
   Never invent abbreviations or aliases.

3. **Output directory discipline**: All work products (analysis JSON, DDL files, SQL scripts,
   reports) are written to the `work/` directory. Do NOT write deliverables to `reports/`,
   `configs/`, `db/`, `scripts/`, or `archive/`.

4. **Schema discipline**: JSON deliverables use snake_case field names exclusively.
   Never use camelCase or PascalCase in JSON output keys.

5. **Production DDL safety**: Every `CREATE INDEX` statement targeting the production database
   must use the `CONCURRENTLY` keyword to avoid table-locking.

6. **Temporal awareness**: Optimization recommendations arrive incrementally. When an
   authoritative notice supersedes a prior recommendation, the later instruction wins —
   revise prior outputs rather than stacking contradictory logic.

7. **Index-type accuracy**: Hash indexes support only equality (`=`) operations — they cannot
   satisfy range predicates (`<`, `>`, `BETWEEN`). Always select the correct index type for
   the query predicate pattern.
""")

    w(WS / "USER.md", """# Team Members and Channels

## Primary User
- **Li Wei** — DBA Engineer (agent role). Owns the slow-query investigation and optimization.
  Writes all deliverables to `work/`. Prefers snake_case JSON, CONCURRENTLY on all production DDL.

## Key Stakeholders

| Name        | Role                   | Channel               | Notes |
|-------------|------------------------|-----------------------|-------|
| Sreedhar    | Senior DBA Consultant  | Slack DM              | Provides detailed optimization advice; occasionally suggests suboptimal approaches (double-check against official docs) |
| Alex Reeves | CTO                    | Email                 | Escalates performance SLAs; may issue directives that get superseded by architecture review |
| Maya Lin    | Principal Architect    | Email                 | Final technical authority; can supersede CTO directives on implementation approach |
| On-call     | On-call rotation       | Feishu #oncall-alerts | Night-time alert handling; includes tool_call traces |

## Channels
- **Slack #dba-alerts**: Group DBA channel — team-wide alerts and triage discussion
- **Slack DM (Li Wei ↔ Sreedhar)**: Detailed technical advice; Sreedhar sometimes quotes from Slack bot summaries (unreliable)
- **Email (Alex Reeves → DBA team)**: Executive performance directives
- **Email (Maya Lin → DBA team)**: Architecture review decisions (authoritative, may supersede CTO)
- **Feishu #oncall-alerts**: Night-shift operational notes
""")

    w(WS / "IDENTITY.md", """# Identity

You are **DBOps AI**, a database optimization assistant deployed to support Li Wei (DBA Engineer)
at FinEdge Analytics during a PostgreSQL 16 performance incident.

Your responsibilities:
- Analyse `pg_stat_statements` snapshots and `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` outputs
- Diagnose slow queries, identify missing indexes, and assess execution plan pathologies
- Design B-Tree, Partial, Covering (INCLUDE), and composite indexes
- Author production-safe DDL (`CREATE INDEX CONCURRENTLY`) and record decisions in structured logs
- Handle update-driven changes: incorporate new EXPLAIN data and supersede stale recommendations
- Produce a final structured optimization report with SHA-256 sign-off

Source data under `db/`, `reports/`, `configs/`, `scripts/`, `archive/` is read-only reference.
You create deliverables exclusively under `work/`.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool               | Purpose                                   | Notes |
|--------------------|-------------------------------------------|-------|
| `sessions_list`    | List all available history sessions       | Main session only |
| `sessions_history` | Read a specific history session           | Main session only |
| `read`             | Read a workspace file                     | All sessions |
| `exec`             | Execute a shell command                   | Use to write deliverable files |

## Rules
- All inputs under `db/`, `reports/`, `configs/`, `scripts/`, `archive/` are **read-only**.
- Write ALL deliverables under `work/` using `exec` (heredoc / python).
- In history sessions, use only `read` and light `exec`; do not call session tools there.
""")


# --------------------------------------------------------------------------- #
# 2. Database schema (DDL)
# --------------------------------------------------------------------------- #
def gen_schema() -> None:
    w(WS / "db" / "schema.sql", """-- FinEdge Analytics — PostgreSQL 16 database schema
-- Tables: events, orders, notifications, users, products, categories, audit_log, service_config
-- Generated: 2026-01-15

-- ============================================================
-- users (2 million rows)
-- ============================================================
CREATE TABLE users (
    id              BIGSERIAL PRIMARY KEY,
    email           VARCHAR(320) NOT NULL,
    name            VARCHAR(255) NOT NULL,
    tier            SMALLINT NOT NULL DEFAULT 1,         -- 1=Free, 2=Pro, 3=Enterprise
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    country_code    CHAR(2),
    preferences     JSONB
);

-- Current indexes on users:
CREATE UNIQUE INDEX idx_users_email ON users (email);
-- NOTE: No index on (tier, is_active) — range queries on tier are slow.

-- ============================================================
-- products (500 thousand rows)
-- ============================================================
CREATE TABLE products (
    id              BIGSERIAL PRIMARY KEY,
    sku             VARCHAR(64) NOT NULL,
    name            VARCHAR(512) NOT NULL,
    category_id     BIGINT NOT NULL,
    price_cents     INTEGER NOT NULL,
    is_listed       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX idx_products_sku ON products (sku);
-- NOTE: category_id has no index — FK scans are slow on DELETE from categories.

-- ============================================================
-- categories (10 thousand rows)
-- ============================================================
CREATE TABLE categories (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    parent_id   BIGINT REFERENCES categories(id),
    slug        VARCHAR(255) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX idx_categories_slug ON categories (slug);

-- ============================================================
-- orders (5 million rows)
-- ============================================================
CREATE TABLE orders (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(id),
    product_id      BIGINT NOT NULL REFERENCES products(id),
    status          VARCHAR(32) NOT NULL,   -- pending / confirmed / shipped / delivered / cancelled
    billed          BOOLEAN NOT NULL DEFAULT FALSE,
    order_nr        BIGINT NOT NULL,
    amount_cents    INTEGER NOT NULL,
    service_id      INTEGER NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Current indexes on orders:
CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE INDEX idx_orders_status ON orders (status);
-- NOTE: No index on (service_id) — JOIN with events table is extremely slow.
-- NOTE: No partial index on billed — unbilled order scans touch entire table.

-- ============================================================
-- events (90 million rows) — the largest table
-- ============================================================
CREATE TABLE events (
    id              BIGSERIAL PRIMARY KEY,
    service_id      INTEGER NOT NULL,
    event_type      VARCHAR(64) NOT NULL,
    user_id         BIGINT,
    data            JSONB,
    status          VARCHAR(32) NOT NULL DEFAULT 'active',  -- active / archived / deleted
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at    TIMESTAMPTZ
);

-- Current indexes on events:
CREATE INDEX idx_events_created_at ON events (created_at);
-- NOTE: No composite index on (service_id, created_at) — range+filter queries are sequential.
-- NOTE: status column has only 3 values but no partial index — count queries scan all 90M rows.

-- ============================================================
-- notifications (12 million rows)
-- ============================================================
CREATE TABLE notifications (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(id),
    type            VARCHAR(64) NOT NULL,
    channel         VARCHAR(32) NOT NULL,   -- email / push / sms
    is_read         BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    read_at         TIMESTAMPTZ,
    payload         JSONB
);

-- Current indexes on notifications:
CREATE INDEX idx_notifications_user_id ON notifications (user_id);
-- NOTE: No index on (user_id, is_read) — unread-notification queries are slow.

-- ============================================================
-- audit_log (30 million rows)
-- ============================================================
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    table_name  VARCHAR(64) NOT NULL,
    record_id   BIGINT NOT NULL,
    action      VARCHAR(16) NOT NULL,   -- INSERT / UPDATE / DELETE
    actor_id    BIGINT,
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    old_data    JSONB,
    new_data    JSONB
);

CREATE INDEX idx_audit_changed_at ON audit_log (changed_at);
CREATE INDEX idx_audit_table_record ON audit_log (table_name, record_id);

-- ============================================================
-- service_config (100 rows)
-- ============================================================
CREATE TABLE service_config (
    service_id      INTEGER PRIMARY KEY,
    service_name    VARCHAR(128) NOT NULL,
    is_enabled      BOOLEAN NOT NULL DEFAULT TRUE,
    config_json     JSONB,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
""")


# --------------------------------------------------------------------------- #
# 3. pg_stat_statements CSV snapshot (61 columns × 50 rows, ~30KB)
# --------------------------------------------------------------------------- #
def gen_pgstat_snapshot() -> None:
    """生成 pg_stat_statements 视图全量快照 CSV（含 61 列）。
    慢查询（mean_exec_time > 500ms）共 20 条，锚点对齐 BRIEF 说明。
    """
    rng = random.Random(42)

    # pg_stat_statements 61 列（来自 PostgreSQL 文档，verbatim）
    columns = [
        "userid", "dbid", "toplevel", "queryid", "query",
        "plans", "total_plan_time", "min_plan_time", "max_plan_time", "mean_plan_time",
        "stddev_plan_time", "calls", "total_exec_time", "min_exec_time", "max_exec_time",
        "mean_exec_time", "stddev_exec_time", "rows", "shared_blks_hit", "shared_blks_read",
        "shared_blks_dirtied", "shared_blks_written", "local_blks_hit", "local_blks_read",
        "local_blks_dirtied", "local_blks_written", "temp_blks_read", "temp_blks_written",
        "blk_read_time", "blk_write_time", "temp_blk_read_time", "temp_blk_write_time",
        "wal_records", "wal_fpi", "wal_bytes", "jit_functions", "jit_generation_time",
        "jit_inlining_count", "jit_inlining_time", "jit_optimization_count",
        "jit_optimization_time", "jit_emission_count", "jit_emission_time",
        "jit_deform_count", "jit_deform_time",
        # 以下为 pg_stat_statements v1.10+ 新增列（PostgreSQL 16）
        "parallel_workers_to_launch", "parallel_workers_launched",
        "stats_since", "minmax_stats_since",
        "total_time", "min_time", "max_time", "mean_time", "stddev_time",
        # 补足 61 列
        "cache_hit_ratio", "seq_scans", "idx_scans", "n_live_tup", "n_dead_tup", "last_autovacuum",
        "last_autoanalyze",
    ]
    assert len(columns) == 61, f"Expected 61 columns, got {len(columns)}"

    # 预定义 20 条慢查询（mean_exec_time > 500ms），queryid 与 EXPLAIN JSON 锚点对齐
    slow_queries = [
        # (queryid, query_text, mean_exec_time, calls)
        (1001, "SELECT * FROM events WHERE service_id = $1 AND created_at >= $2 ORDER BY created_at DESC LIMIT 100", 4850.23, 1820),
        (1002, "SELECT u.email, u.name, o.status, o.amount_cents FROM orders o JOIN users u ON o.user_id = u.id WHERE o.service_id = $1 AND o.status = $2", 3240.15, 945),
        (1003, "SELECT COUNT(*) FROM events WHERE status = 'active'", 12450.67, 234),
        (1004, "SELECT * FROM notifications WHERE user_id = $1 AND is_read = FALSE ORDER BY sent_at DESC", 2180.44, 4521),
        (1005, "SELECT p.sku, p.name, SUM(o.amount_cents) FROM orders o JOIN products p ON o.product_id = p.id WHERE o.created_at BETWEEN $1 AND $2 GROUP BY p.sku, p.name ORDER BY SUM(o.amount_cents) DESC", 5670.89, 312),
        (1006, "SELECT * FROM events WHERE service_id = $1 AND event_type = $2 AND created_at >= $3", 3890.12, 678),
        (1007, "SELECT * FROM orders WHERE billed IS NOT TRUE AND created_at < $1", 1980.33, 2341),
        (1008, "SELECT u.email, u.name, u.updated_at FROM users WHERE email LIKE $1", 820.55, 8934),
        (1009, "SELECT * FROM audit_log WHERE table_name = $1 AND record_id = $2 ORDER BY changed_at DESC", 610.22, 5621),
        # Query-010 through 012 appear in Update 1
        (1010, "SELECT e.id, e.event_type, e.data, o.status FROM events e JOIN orders o ON e.service_id = o.service_id WHERE e.created_at >= $1 AND o.status IN ($2, $3) LIMIT 1000", 8920.45, 156),
        (1011, "SELECT order_nr, amount_cents FROM orders WHERE billed IS NOT TRUE ORDER BY created_at LIMIT 5000", 1240.77, 3892),
        (1012, "SELECT u.email, u.name, u.updated_at FROM users WHERE u.email = $1", 540.12, 18234),
        # Additional slower queries
        (1013, "SELECT COUNT(*) FROM events WHERE created_at >= $1 AND created_at < $2 AND service_id = ANY($3)", 7340.88, 89),
        (1014, "DELETE FROM notifications WHERE user_id IN (SELECT id FROM users WHERE is_active = FALSE) AND sent_at < $1", 9870.34, 45),
        (1015, "SELECT * FROM products WHERE category_id = $1 AND is_listed = TRUE ORDER BY price_cents", 890.11, 6723),
        (1016, "UPDATE orders SET status = $1, updated_at = now() WHERE id = $2", 520.08, 92341),
        (1017, "SELECT MAX(created_at) FROM events WHERE service_id = $1 AND status = 'active'", 6120.45, 1203),
        (1018, "SELECT * FROM users WHERE tier = $1 AND is_active = TRUE ORDER BY created_at", 750.33, 4512),
        (1019, "SELECT table_name, COUNT(*) FROM audit_log WHERE changed_at >= $1 GROUP BY table_name ORDER BY COUNT(*) DESC", 930.77, 2341),
        (1020, "SELECT SUM(amount_cents) FROM orders WHERE user_id = $1 AND status NOT IN ('cancelled', 'refunded')", 840.22, 7823),
    ]

    rows = [columns]
    base_userid = 16384
    base_dbid = 24601

    for qid, query, mean_et, calls in slow_queries:
        total_et = round(mean_et * calls, 2)
        min_et = round(mean_et * 0.3, 2)
        max_et = round(mean_et * 4.2, 2)
        stddev_et = round(mean_et * 0.45, 2)
        shblks_hit = rng.randint(50000, 5000000)
        shblks_read = rng.randint(10000, 2000000)
        row = [
            base_userid, base_dbid, True, qid, query,
            calls, round(mean_et * calls * 0.01, 2), round(mean_et * 0.01 * 0.3, 2),
            round(mean_et * 0.01 * 4.2, 2), round(mean_et * 0.01, 4),
            round(mean_et * 0.01 * 0.45, 4), calls, total_et, min_et, max_et,
            mean_et, stddev_et, rng.randint(100, 50000),
            shblks_hit, shblks_read,
            rng.randint(0, 100), rng.randint(0, 50), 0, 0, 0, 0,
            rng.randint(0, 5000), rng.randint(0, 500),
            round(rng.uniform(0, 500), 2), round(rng.uniform(0, 50), 2),
            0, 0,
            rng.randint(0, 10000), rng.randint(0, 100),
            rng.randint(0, 1000000),
            0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0,
            0, 0,
            "2026-01-01 00:00:00+00", "2026-01-01 00:00:00+00",
            total_et, min_et, max_et, mean_et, stddev_et,
            round(shblks_hit / max(shblks_hit + shblks_read, 1) * 100, 2),
            rng.randint(0, 10000), rng.randint(0, 50000),
            rng.randint(1000, 90000000), rng.randint(0, 5000),
            "2026-01-14 03:00:00+00",
            "2026-01-14 03:16:00+00",
        ]
        assert len(row) == 61, f"Row length {len(row)} != 61 for queryid {qid}"
        rows.append(row)

    # Add 80 more non-slow queries (mean_exec_time < 100ms) — padded for volume
    fast_queries = [
        "SELECT id, email FROM users WHERE id = $1",
        "SELECT * FROM service_config WHERE service_id = $1",
        "INSERT INTO audit_log (table_name, record_id, action, actor_id, changed_at) VALUES ($1,$2,$3,$4,now())",
        "SELECT COUNT(*) FROM orders WHERE status = 'pending'",
        "UPDATE users SET updated_at = now() WHERE id = $1",
        "SELECT id, name FROM categories WHERE parent_id IS NULL",
        "SELECT * FROM products WHERE id = $1",
        "SELECT COUNT(*) FROM notifications WHERE user_id = $1",
        "SELECT id FROM users WHERE email = $1",
        "SELECT * FROM orders WHERE id = $1",
        "SELECT name, config_json FROM service_config WHERE is_enabled = TRUE",
        "INSERT INTO notifications (user_id, type, channel, payload) VALUES ($1,$2,$3,$4)",
        "SELECT COUNT(*) FROM events WHERE created_at >= $1",
        "SELECT MAX(id) FROM orders",
        "SELECT * FROM categories WHERE id = $1",
        "UPDATE orders SET billed = TRUE WHERE id = $1",
        "SELECT id, sku FROM products WHERE is_listed = TRUE LIMIT 100",
        "SELECT COUNT(*) FROM users WHERE is_active = TRUE",
        "DELETE FROM audit_log WHERE changed_at < $1 LIMIT 1000",
        "SELECT id, type, sent_at FROM notifications WHERE user_id = $1 AND is_read = FALSE LIMIT 10",
        "SELECT * FROM audit_log WHERE id = $1",
        "SELECT p.name, c.name FROM products p JOIN categories c ON p.category_id = c.id WHERE p.id = $1",
        "SELECT SUM(amount_cents) FROM orders WHERE status = 'delivered' AND created_at >= $1",
        "UPDATE notifications SET is_read = TRUE, read_at = now() WHERE id = $1",
        "SELECT * FROM users WHERE tier = 3 AND is_active = TRUE",
        "SELECT order_nr FROM orders WHERE user_id = $1 ORDER BY created_at DESC LIMIT 20",
        "SELECT event_type, COUNT(*) FROM events WHERE service_id = $1 AND created_at >= $2 GROUP BY event_type",
        "SELECT * FROM products WHERE sku = $1",
        "SELECT id FROM orders WHERE billed = FALSE AND created_at < now() - INTERVAL '30 days'",
        "VACUUM ANALYZE notifications",
        "SELECT COUNT(*) FROM events WHERE service_id = $1 AND event_type = 'click'",
        "SELECT id, user_id, amount_cents FROM orders WHERE status = 'pending' LIMIT 100",
        "SELECT * FROM notifications WHERE user_id = $1 AND channel = 'email' LIMIT 20",
        "SELECT p.id, p.name FROM products p JOIN categories c ON p.category_id = c.id WHERE c.slug = $1",
        "UPDATE events SET processed_at = now() WHERE id = $1 AND processed_at IS NULL",
        "SELECT COUNT(*) FROM audit_log WHERE actor_id = $1 AND changed_at >= $2",
        "SELECT u.email, u.tier FROM users WHERE tier IN (2, 3) AND is_active = TRUE ORDER BY created_at DESC LIMIT 50",
        "SELECT * FROM orders WHERE order_nr = $1",
        "INSERT INTO events (service_id, event_type, user_id, data, status) VALUES ($1,$2,$3,$4,'active')",
        "SELECT MAX(changed_at) FROM audit_log WHERE table_name = 'orders'",
        "SELECT n.type, COUNT(*) FROM notifications n WHERE n.user_id = $1 GROUP BY n.type",
        "SELECT id, name, parent_id FROM categories WHERE slug LIKE $1",
        "SELECT SUM(amount_cents) FROM orders WHERE created_at >= $1 AND status = 'delivered'",
        "UPDATE users SET tier = $1 WHERE id = $2",
        "SELECT * FROM service_config WHERE is_enabled = TRUE ORDER BY service_id",
        "SELECT e.id, e.event_type FROM events e WHERE e.user_id = $1 ORDER BY e.created_at DESC LIMIT 10",
        "DELETE FROM events WHERE status = 'deleted' AND created_at < $1 LIMIT 500",
        "SELECT COUNT(*) FROM products WHERE category_id = $1 AND is_listed = TRUE",
        "SELECT o.id, o.order_nr, o.status FROM orders o WHERE o.user_id = $1 AND o.status != 'cancelled'",
        "SELECT * FROM audit_log WHERE record_id = $1 AND table_name = 'users' ORDER BY changed_at DESC LIMIT 5",
        "SELECT id FROM notifications WHERE user_id = $1 AND is_read = FALSE AND channel = 'push' LIMIT 100",
        "INSERT INTO orders (user_id, product_id, status, billed, order_nr, amount_cents, service_id) VALUES ($1,$2,$3,$4,$5,$6,$7)",
        "SELECT COUNT(DISTINCT user_id) FROM events WHERE service_id = $1 AND created_at >= $2",
        "SELECT p.sku, p.price_cents FROM products p WHERE p.is_listed = TRUE AND p.price_cents <= $1",
        "UPDATE notifications SET is_read = TRUE WHERE user_id = $1 AND is_read = FALSE",
        "SELECT * FROM categories ORDER BY parent_id NULLS FIRST, name",
        "SELECT COUNT(*) FROM orders WHERE created_at >= $1 AND created_at < $2",
        "SELECT id, email FROM users WHERE country_code = $1 AND is_active = TRUE LIMIT 200",
        "SELECT * FROM events WHERE processed_at IS NULL AND status = 'active' ORDER BY created_at LIMIT 1000",
        "SELECT MAX(id) FROM events",
        "SELECT u.id, u.email FROM users u JOIN orders o ON u.id = o.user_id WHERE o.id = $1",
        "SELECT SUM(amount_cents), COUNT(*) FROM orders WHERE service_id = $1 AND billed = TRUE",
        "SELECT event_type, COUNT(*) FROM events GROUP BY event_type ORDER BY COUNT(*) DESC LIMIT 10",
        "SELECT * FROM products WHERE price_cents BETWEEN $1 AND $2 AND is_listed = TRUE LIMIT 50",
        "UPDATE audit_log SET old_data = $1 WHERE id = $2",
        "SELECT id, type, payload FROM notifications WHERE id = $1",
        "SELECT COUNT(*) FROM users WHERE created_at >= $1",
        "SELECT o.*, p.sku FROM orders o JOIN products p ON o.product_id = p.id WHERE o.id = $1",
        "SELECT * FROM events WHERE id = $1",
        "SELECT MIN(created_at), MAX(created_at), COUNT(*) FROM events WHERE service_id = $1",
        "SELECT id, name, is_enabled FROM service_config ORDER BY service_id",
        "UPDATE orders SET updated_at = now(), amount_cents = $1 WHERE id = $2 AND status = 'pending'",
        "SELECT COUNT(*) FROM audit_log WHERE changed_at >= $1 AND action = 'DELETE'",
        "SELECT * FROM products WHERE id IN ($1, $2, $3, $4, $5)",
        "SELECT n.user_id, COUNT(*) FROM notifications n GROUP BY n.user_id HAVING COUNT(*) > 100",
        "SELECT * FROM users WHERE preferences @> $1",
        "DELETE FROM notifications WHERE id = $1",
        "SELECT SUM(n_dead_tup) FROM pg_stat_user_tables WHERE schemaname = 'public'",
        "SELECT * FROM events WHERE data @> $1 AND created_at >= $2",
    ]

    for i, query in enumerate(fast_queries):
        qid = 2000 + i
        mean_et = round(rng.uniform(0.5, 95.0), 2)
        calls_n = rng.randint(100, 200000)
        total_et = round(mean_et * calls_n, 2)
        shblks_hit = rng.randint(100, 50000)
        shblks_read = rng.randint(0, 2000)
        row = [
            base_userid, base_dbid, True, qid, query,
            calls_n, round(mean_et * calls_n * 0.005, 2), round(mean_et * 0.1, 2),
            round(mean_et * 3.5, 2), round(mean_et, 4),
            round(mean_et * 0.2, 4), calls_n, total_et,
            round(mean_et * 0.1, 2), round(mean_et * 3.5, 2),
            mean_et, round(mean_et * 0.2, 2), rng.randint(1, 5000),
            shblks_hit, shblks_read,
            rng.randint(0, 10), 0, 0, 0, 0, 0, 0, 0,
            round(rng.uniform(0, 5), 2), 0.0, 0, 0,
            0, 0, 0,
            0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0,
            0, 0,
            "2026-01-01 00:00:00+00", "2026-01-01 00:00:00+00",
            total_et, round(mean_et * 0.1, 2), round(mean_et * 3.5, 2), mean_et, round(mean_et * 0.2, 2),
            round(shblks_hit / max(shblks_hit + shblks_read, 1) * 100, 2),
            rng.randint(0, 1000), rng.randint(100, 100000),
            rng.randint(1000, 5000000), 0,
            "2026-01-15 02:00:00+00",
            "2026-01-15 02:02:00+00",
        ]
        assert len(row) == 61, f"Fast row length {len(row)} != 61"
        rows.append(row)

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "reports" / "pgstatstatements_snapshot.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# 4. EXPLAIN JSON files (before optimization)
# --------------------------------------------------------------------------- #
def _explain_json(node_type, total_cost, plan_rows, plan_width,
                  actual_rows, actual_total_time, startup_cost=0.00,
                  actual_startup_time=0.000, loops=1, relation=None,
                  children=None, filter_txt=None, sort_key=None,
                  index_name=None, hash_cond=None,
                  planning_time=None, execution_time=None) -> dict:
    """构造标准 EXPLAIN FORMAT JSON 输出结构（对齐 PostgreSQL 官方格式）。"""
    node = {
        "Node Type": node_type,
        "Startup Cost": startup_cost,
        "Total Cost": total_cost,
        "Plan Rows": plan_rows,
        "Plan Width": plan_width,
        "Actual Startup Time": actual_startup_time,
        "Actual Total Time": actual_total_time,
        "Actual Rows": actual_rows,
        "Loops": loops,
    }
    if relation:
        node["Relation Name"] = relation
    if filter_txt:
        node["Filter"] = filter_txt
    if sort_key:
        node["Sort Key"] = sort_key
    if index_name:
        node["Index Name"] = index_name
    if hash_cond:
        node["Hash Cond"] = hash_cond
    if children:
        node["Plans"] = children

    plan = {"Plan": node}
    if planning_time is not None:
        plan["Planning Time"] = planning_time
    if execution_time is not None:
        plan["Execution Time"] = execution_time
    return [plan]


def gen_explain_plans_before() -> None:
    """生成 9 条慢查询的 EXPLAIN FORMAT JSON（优化前）。"""
    ep_dir = WS / "reports" / "explain_plans"

    # Query-001: events 表顺序扫描（service_id 无索引）
    # total_cost = 2876543.20（合成值，对应约 90M 行 seq scan）
    # plan_rows=450（严重低估）, actual_rows=24891（高估误差 > 50%）
    wj(ep_dir / "query_001_before.json", _explain_json(
        node_type="Seq Scan",
        relation="events",
        total_cost=2876543.20,
        startup_cost=0.00,
        plan_rows=450,
        plan_width=248,
        actual_rows=24891,
        actual_total_time=4847.892,
        actual_startup_time=0.012,
        filter_txt="((service_id = 7) AND (created_at >= '2026-01-01 00:00:00+00'::timestamptz))",
        planning_time=0.245,
        execution_time=4850.231,
    ))

    # Query-002: orders JOIN users，Hash Join，service_id 无索引导致 Hash scan 慢
    wj(ep_dir / "query_002_before.json", _explain_json(
        node_type="Hash Join",
        total_cost=198432.67,
        startup_cost=1234.00,
        plan_rows=8923,
        plan_width=312,
        actual_rows=12456,
        actual_total_time=3238.445,
        actual_startup_time=1234.112,
        hash_cond="(o.user_id = u.id)",
        planning_time=0.812,
        execution_time=3240.153,
        children=[
            {
                "Node Type": "Seq Scan",
                "Relation Name": "orders",
                "Startup Cost": 0.00,
                "Total Cost": 94567.00,
                "Plan Rows": 4521,
                "Plan Width": 198,
                "Actual Rows": 6234,
                "Actual Total Time": 1120.334,
                "Actual Startup Time": 0.008,
                "Loops": 1,
                "Filter": "((service_id = 7) AND ((status)::text = 'confirmed'::text))",
            },
            {
                "Node Type": "Hash",
                "Startup Cost": 1100.00,
                "Total Cost": 1100.00,
                "Plan Rows": 100000,
                "Plan Width": 89,
                "Actual Rows": 120000,
                "Actual Total Time": 890.445,
                "Actual Startup Time": 0.005,
                "Loops": 1,
                "Plans": [{
                    "Node Type": "Seq Scan",
                    "Relation Name": "users",
                    "Startup Cost": 0.00,
                    "Total Cost": 1100.00,
                    "Plan Rows": 100000,
                    "Plan Width": 89,
                    "Actual Rows": 120000,
                    "Actual Total Time": 887.223,
                    "Actual Startup Time": 0.003,
                    "Loops": 1,
                }],
            },
        ],
    ))

    # Query-003: events 表 COUNT(*) status='active'，全表扫描 90M 行
    wj(ep_dir / "query_003_before.json", _explain_json(
        node_type="Aggregate",
        total_cost=1687543.25,
        startup_cost=1687543.25,
        plan_rows=1,
        plan_width=8,
        actual_rows=1,
        actual_total_time=12448.762,
        actual_startup_time=12448.762,
        planning_time=0.156,
        execution_time=12450.671,
        children=[{
            "Node Type": "Seq Scan",
            "Relation Name": "events",
            "Startup Cost": 0.00,
            "Total Cost": 1687543.00,
            "Plan Rows": 30000000,
            "Plan Width": 0,
            "Actual Rows": 27456789,
            "Actual Total Time": 11902.334,
            "Actual Startup Time": 0.009,
            "Loops": 1,
            "Filter": "((status)::text = 'active'::text)",
            "Rows Removed by Filter": 62543211,
        }],
    ))

    # Query-004: notifications WHERE user_id AND is_read=FALSE — 统计失真案例
    # n_distinct for is_read column: seed_stats.sql 中记录 -0.23（约23%行），bot 声称 -1
    # plan_rows=1（估算极低），actual_rows=3421（误差 > 50%）
    wj(ep_dir / "query_004_before.json", _explain_json(
        node_type="Seq Scan",
        relation="notifications",
        total_cost=234891.44,
        startup_cost=0.00,
        plan_rows=1,
        plan_width=298,
        actual_rows=3421,
        actual_total_time=2178.334,
        actual_startup_time=0.011,
        filter_txt="((user_id = 99234) AND (is_read = false))",
        planning_time=0.334,
        execution_time=2180.442,
    ))

    # Query-005: orders JOIN products aggregate — Seq Scan on orders
    wj(ep_dir / "query_005_before.json", _explain_json(
        node_type="Sort",
        total_cost=289043.12,
        startup_cost=289043.00,
        plan_rows=1000,
        plan_width=156,
        actual_rows=8934,
        actual_total_time=5668.445,
        actual_startup_time=5600.223,
        sort_key=["(sum(o.amount_cents)) DESC"],
        planning_time=0.923,
        execution_time=5670.892,
        children=[{
            "Node Type": "HashAggregate",
            "Startup Cost": 288000.00,
            "Total Cost": 289000.00,
            "Plan Rows": 1000,
            "Plan Width": 156,
            "Actual Rows": 8934,
            "Actual Total Time": 5589.334,
            "Actual Startup Time": 5500.112,
            "Loops": 1,
            "Plans": [{
                "Node Type": "Hash Join",
                "Startup Cost": 11000.00,
                "Total Cost": 287000.00,
                "Plan Rows": 1000000,
                "Plan Width": 120,
                "Actual Rows": 1234567,
                "Actual Total Time": 4980.223,
                "Actual Startup Time": 100.334,
                "Loops": 1,
                "Hash Cond": "(o.product_id = p.id)",
            }],
        }],
    ))

    # Query-006: events composite filter — Seq Scan
    wj(ep_dir / "query_006_before.json", _explain_json(
        node_type="Seq Scan",
        relation="events",
        total_cost=1987654.33,
        startup_cost=0.00,
        plan_rows=89234,
        plan_width=248,
        actual_rows=15678,
        actual_total_time=3887.892,
        actual_startup_time=0.013,
        filter_txt="((service_id = 3) AND ((event_type)::text = 'purchase'::text) AND (created_at >= '2026-01-10 00:00:00+00'::timestamptz))",
        planning_time=0.289,
        execution_time=3890.123,
    ))

    # Query-007: orders WHERE billed IS NOT TRUE — full scan
    wj(ep_dir / "query_007_before.json", _explain_json(
        node_type="Seq Scan",
        relation="orders",
        total_cost=98432.11,
        startup_cost=0.00,
        plan_rows=4500,
        plan_width=198,
        actual_rows=89234,
        actual_total_time=1978.556,
        actual_startup_time=0.010,
        filter_txt="((billed IS NOT TRUE) AND (created_at < '2026-01-01 00:00:00+00'::timestamptz))",
        planning_time=0.178,
        execution_time=1980.334,
    ))

    # Query-008: users WHERE email LIKE — Seq Scan (LIKE can't use btree without C collation)
    wj(ep_dir / "query_008_before.json", _explain_json(
        node_type="Seq Scan",
        relation="users",
        total_cost=34567.89,
        startup_cost=0.00,
        plan_rows=12,
        plan_width=89,
        actual_rows=3,
        actual_total_time=818.334,
        actual_startup_time=0.007,
        filter_txt="((email)::text ~~ '%@finedge.com'::text)",
        planning_time=0.123,
        execution_time=820.551,
    ))

    # Query-009: audit_log WHERE table_name AND record_id ORDER BY — uses existing composite index
    wj(ep_dir / "query_009_before.json", _explain_json(
        node_type="Index Scan",
        relation="audit_log",
        index_name="idx_audit_table_record",
        total_cost=28934.55,
        startup_cost=0.44,
        plan_rows=500,
        plan_width=289,
        actual_rows=234,
        actual_total_time=608.334,
        actual_startup_time=2.112,
        filter_txt="((table_name)::text = 'orders'::text AND record_id = 5892341)",
        planning_time=0.234,
        execution_time=610.221,
    ))


def gen_explain_plans_after() -> None:
    """生成 9 条慢查询的 EXPLAIN FORMAT JSON（索引创建后优化后版本，供 Update 1 注入）。"""
    ep_dir = UPD / "upd1_workspace" / "explain_plans"

    # Query-001 after: Index Only Scan (composite index on service_id, created_at)
    wj(ep_dir / "query_001_after.json", _explain_json(
        node_type="Index Only Scan",
        relation="events",
        index_name="idx_events_service_created",
        total_cost=156.34,
        startup_cost=0.56,
        plan_rows=450,
        plan_width=248,
        actual_rows=24891,
        actual_total_time=18.445,
        actual_startup_time=0.334,
        filter_txt=None,
        planning_time=0.312,
        execution_time=19.892,
    ))

    # Query-002 after: Index Scan on orders (service_id index), Hash Join still but faster
    wj(ep_dir / "query_002_after.json", _explain_json(
        node_type="Hash Join",
        total_cost=24891.23,
        startup_cost=892.00,
        plan_rows=8923,
        plan_width=312,
        actual_rows=12456,
        actual_total_time=312.334,
        actual_startup_time=892.001,
        hash_cond="(o.user_id = u.id)",
        planning_time=0.734,
        execution_time=314.156,
        children=[
            {
                "Node Type": "Index Scan",
                "Relation Name": "orders",
                "Index Name": "idx_orders_service_id",
                "Startup Cost": 0.44,
                "Total Cost": 12456.00,
                "Plan Rows": 4521,
                "Plan Width": 198,
                "Actual Rows": 6234,
                "Actual Total Time": 145.334,
                "Actual Startup Time": 0.445,
                "Loops": 1,
            },
            {
                "Node Type": "Hash",
                "Startup Cost": 1100.00,
                "Total Cost": 1100.00,
                "Plan Rows": 100000,
                "Plan Width": 89,
                "Actual Rows": 120000,
                "Actual Total Time": 78.223,
                "Actual Startup Time": 0.005,
                "Loops": 1,
            },
        ],
    ))

    # Query-003 after: Bitmap Index Scan (partial index on status='active')
    wj(ep_dir / "query_003_after.json", _explain_json(
        node_type="Aggregate",
        total_cost=423.12,
        startup_cost=423.12,
        plan_rows=1,
        plan_width=8,
        actual_rows=1,
        actual_total_time=245.112,
        actual_startup_time=245.112,
        planning_time=0.234,
        execution_time=245.334,
        children=[{
            "Node Type": "Bitmap Heap Scan",
            "Relation Name": "events",
            "Startup Cost": 0.00,
            "Total Cost": 423.00,
            "Plan Rows": 27456789,
            "Plan Width": 0,
            "Actual Rows": 27456789,
            "Actual Total Time": 234.112,
            "Actual Startup Time": 12.334,
            "Loops": 1,
            "Plans": [{
                "Node Type": "Bitmap Index Scan",
                "Index Name": "idx_events_status_active",
                "Startup Cost": 0.00,
                "Total Cost": 0.00,
                "Plan Rows": 27456789,
                "Plan Width": 0,
                "Actual Rows": 27456789,
                "Actual Total Time": 8.334,
                "Actual Startup Time": 0.0,
                "Loops": 1,
            }],
        }],
    ))

    # Query-004 after: Index Scan (composite index on user_id, is_read)
    wj(ep_dir / "query_004_after.json", _explain_json(
        node_type="Index Scan",
        relation="notifications",
        index_name="idx_notifications_user_unread",
        total_cost=89.23,
        startup_cost=0.56,
        plan_rows=3421,
        plan_width=298,
        actual_rows=3421,
        actual_total_time=12.334,
        actual_startup_time=0.334,
        planning_time=0.234,
        execution_time=13.892,
    ))

    # Query-005 after: Index Scan on orders (created_at index improved)
    wj(ep_dir / "query_005_after.json", _explain_json(
        node_type="Sort",
        total_cost=45678.23,
        startup_cost=45678.00,
        plan_rows=1000,
        plan_width=156,
        actual_rows=8934,
        actual_total_time=892.334,
        actual_startup_time=889.112,
        sort_key=["(sum(o.amount_cents)) DESC"],
        planning_time=0.812,
        execution_time=893.445,
    ))

    # Query-006 after: Index Scan (composite index service_id, event_type, created_at)
    wj(ep_dir / "query_006_after.json", _explain_json(
        node_type="Index Scan",
        relation="events",
        index_name="idx_events_service_type_created",
        total_cost=892.34,
        startup_cost=0.56,
        plan_rows=89234,
        plan_width=248,
        actual_rows=15678,
        actual_total_time=78.334,
        actual_startup_time=0.445,
        planning_time=0.289,
        execution_time=79.892,
    ))

    # Query-007 after: Partial Index Scan (WHERE billed IS NOT TRUE)
    wj(ep_dir / "query_007_after.json", _explain_json(
        node_type="Index Scan",
        relation="orders",
        index_name="idx_orders_unbilled",
        total_cost=1234.55,
        startup_cost=0.44,
        plan_rows=4500,
        plan_width=198,
        actual_rows=89234,
        actual_total_time=34.556,
        actual_startup_time=0.445,
        planning_time=0.167,
        execution_time=35.889,
    ))

    # Query-008 after: still Seq Scan (LIKE with leading wildcard can't use B-Tree)
    wj(ep_dir / "query_008_after.json", _explain_json(
        node_type="Seq Scan",
        relation="users",
        total_cost=34567.89,
        startup_cost=0.00,
        plan_rows=12,
        plan_width=89,
        actual_rows=3,
        actual_total_time=818.334,
        actual_startup_time=0.007,
        filter_txt="((email)::text ~~ '%@finedge.com'::text)",
        planning_time=0.123,
        execution_time=820.551,
    ))

    # Query-009 after: same Index Scan as before (already had index)
    wj(ep_dir / "query_009_after.json", _explain_json(
        node_type="Index Scan",
        relation="audit_log",
        index_name="idx_audit_table_record",
        total_cost=28934.55,
        startup_cost=0.44,
        plan_rows=500,
        plan_width=289,
        actual_rows=234,
        actual_total_time=608.334,
        actual_startup_time=2.112,
        planning_time=0.234,
        execution_time=610.221,
    ))


# --------------------------------------------------------------------------- #
# 5. Week-1 slow query report (V5 诱饵在 Slack DM 中)
# --------------------------------------------------------------------------- #
def gen_slow_query_report_week1() -> None:
    # 构造一个较长的报告（~25KB）
    lines = [
        "# FinEdge Analytics — Slow Query Report: Week 1 (2026-01-13 to 2026-01-19)",
        "",
        "> Prepared by: Li Wei (DBA Engineer) | Review: DBA Team",
        "> Database: finedge_prod (PostgreSQL 16.2, SSD-backed, 32 vCPU, 256 GB RAM)",
        "",
        "## Executive Summary",
        "",
        "This week's pg_stat_statements analysis identified 20 queries with mean_exec_time > 500ms.",
        "The top 9 queries account for 78% of total DB execution time. Root causes include:",
        "1. Missing composite index on `events(service_id, created_at)` — Query-001, 006 severely impacted",
        "2. Missing index on `orders(service_id)` — Query-002 cross-table join slow",
        "3. Missing composite index on `notifications(user_id, is_read)` — Query-004 full scan",
        "4. No partial index on `orders(billed)` — Query-007 scans entire 5M-row table",
        "5. Stale statistics on `notifications.is_read` column — Query-004 plan_rows underestimate",
        "",
        "---",
        "",
        "## Query-001 Analysis",
        "**SQL**: `SELECT * FROM events WHERE service_id = $1 AND created_at >= $2 ORDER BY created_at DESC LIMIT 100`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 4850.23 ms |",
        "| calls (last 7 days) | 1,820 |",
        "| Node Type | Seq Scan |",
        "| Total Cost | 2,876,543.20 |",
        "| Plan Rows | 450 |",
        "| Actual Rows | 24,891 |",
        "| Rows Estimate Error | 5,431% — severe underestimate |",
        "",
        "**Root Cause**: `events` table has no index on `(service_id, created_at)`. The planner",
        "grossly underestimates row count due to default statistics (100 buckets) for a 90M-row table.",
        "",
        "**Recommended Fix**: `CREATE INDEX CONCURRENTLY idx_events_service_created ON events (service_id, created_at DESC);`",
        "",
        "**Expected Result**: Index Only Scan, estimated cost ~156.34, execution time < 20ms.",
        "",
        "---",
        "",
        "## Query-002 Analysis",
        "**SQL**: `SELECT u.email, u.name, o.status, o.amount_cents FROM orders o JOIN users u ON o.user_id = u.id WHERE o.service_id = $1 AND o.status = $2`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 3240.15 ms |",
        "| calls | 945 |",
        "| Node Type | Hash Join |",
        "| Total Cost | 198,432.67 |",
        "",
        "**Root Cause**: `orders` has no index on `service_id`. The Hash Join processes 5M rows",
        "to filter by service_id, producing excessive buffer reads.",
        "",
        "---",
        "",
        "## Query-003 Analysis",
        "**SQL**: `SELECT COUNT(*) FROM events WHERE status = 'active'`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 12,450.67 ms |",
        "| calls | 234 |",
        "| Node Type | Aggregate over Seq Scan |",
        "| Total Cost | 1,687,543.25 |",
        "",
        "**Root Cause**: `events.status` has only 3 distinct values ('active', 'archived', 'deleted').",
        "A Partial Index WHERE status = 'active' would allow a targeted Bitmap Index Scan.",
        "",
        "---",
        "",
        "## Query-004 Analysis",
        "**SQL**: `SELECT * FROM notifications WHERE user_id = $1 AND is_read = FALSE ORDER BY sent_at DESC`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 2180.44 ms |",
        "| calls | 4,521 |",
        "| Node Type | Seq Scan |",
        "| Total Cost | 234,891.44 |",
        "| Plan Rows | 1 (extreme underestimate!) |",
        "| Actual Rows | 3,421 |",
        "",
        "**Root Cause**: Stale statistics on `notifications.is_read`. The planner estimates only",
        "1 matching row when the actual count is 3,421. This is a statistics failure (stale_statistics).",
        "",
        "**NOTE**: The Slack bot summary for this column reports n_distinct = -1.0 (claiming all rows",
        "are unique). This is incorrect — see `db/seed_stats.sql` for the actual pg_stats snapshot",
        "which shows n_distinct = -0.23 for `notifications.is_read`. Do not rely on bot summaries.",
        "",
        "---",
        "",
        "## Query-005 through Query-009 (summarised)",
        "",
        "| Query | mean_exec_time | Root Cause |",
        "|-------|----------------|------------|",
        "| Q-005 | 5,670.89 ms | Hash Aggregate on orders×products without covering index |",
        "| Q-006 | 3,890.12 ms | events Seq Scan — missing composite (service_id, event_type, created_at) |",
        "| Q-007 | 1,980.33 ms | orders Seq Scan — no partial index WHERE billed IS NOT TRUE |",
        "| Q-008 | 820.55 ms | users LIKE '%@...' — leading wildcard prevents index use |",
        "| Q-009 | 610.22 ms | audit_log uses idx_audit_table_record (existing index, marginal) |",
        "",
        "---",
        "",
        "## PostgreSQL Configuration Notes",
        "",
        "Current `configs/postgresql.conf` key settings:",
        "- `random_page_cost = 4.0` (default) — should be 1.1 for SSD",
        "- `default_statistics_target = 100` (default) — increase to 500 for high-cardinality columns",
        "- `work_mem = 64MB` — consider session-level tuning for heavy aggregate queries",
        "",
        "Reference: PostgreSQL docs seq_page_cost default = 1.0, random_page_cost default = 4.0",
        "(Source: https://www.postgresql.org/docs/current/runtime-config-query.html)",
        "",
        "---",
        "",
        "## depesz Case Study Reference",
        "",
        "A similar pattern was documented in a depesz case study (Oct 2024):",
        "- Before optimization: estimated cost 8,473.04, execution time > 3 minutes",
        "- After composite partial index: cost 0.62, execution time 0.028ms",
        "- Reference: https://www.depesz.com/2024/10/28/case-study-optimization-of-weirdly-picked-bad-plan/",
        "",
        "Our Query-001 case shows the same pattern on a larger scale (90M rows vs. the depesz case).",
        "",
        "---",
        "",
        "## Recommended Index Creation Batch 1 (Weeks 1-2)",
        "",
        "All production CREATE INDEX statements MUST use CONCURRENTLY to avoid table locks.",
        "(Reference: https://stormatics.tech/blogs/fixing-orm-slowness-by-80-with-strategic-postgresql-indexing)",
        "",
        "```sql",
        "-- Batch 1: High-priority indexes",
        "CREATE INDEX CONCURRENTLY idx_events_service_created ON events (service_id, created_at DESC);",
        "CREATE INDEX CONCURRENTLY idx_orders_service_id ON orders (service_id);",
        "CREATE INDEX CONCURRENTLY idx_notifications_user_unread ON notifications (user_id, is_read) WHERE is_read = FALSE;",
        "CREATE INDEX CONCURRENTLY idx_events_status_active ON events (status) WHERE status = 'active';",
        "CREATE INDEX CONCURRENTLY idx_events_service_type_created ON events (service_id, event_type, created_at DESC);",
        "CREATE INDEX CONCURRENTLY idx_orders_unbilled ON orders (order_nr) WHERE billed IS NOT TRUE;",
        "```",
        "",
        "---",
        "",
        "## pg_stat_statements Configuration",
        "",
        "Current settings (from `configs/postgresql.conf`):",
        "- `pg_stat_statements.max = 5000` (default per PostgreSQL docs)",
        "- `pg_stat_statements.track = top` (default, tracks only top-level statements)",
        "- `pg_stat_statements.save = on` (persists stats across restarts)",
        "",
        "Reference: https://www.postgresql.org/docs/current/pgstatstatements.html",
        "",
        "---",
        "",
        "## Stormatics ORM Case Parallel",
        "",
        "The Stormatics case study (https://stormatics.tech/blogs/fixing-orm-slowness-by-80-with-strategic-postgresql-indexing)",
        "documented a similar scenario where missing foreign key indexes caused 41 million sequential scans.",
        "Their optimization result: Sequential Scans ↓87%, Query Time ↓60-80%, Disk Read IOPS ↓70%.",
        "",
        "Our events/orders JOIN pattern (Query-002) mirrors their FK index case exactly.",
        "",
        "---",
        "",
        "## Next Steps",
        "1. Execute Batch 1 CREATE INDEX CONCURRENTLY statements (off-peak window)",
        "2. Run ANALYZE on all affected tables post-index",
        "3. Collect EXPLAIN ANALYZE output after index creation (Update 1 will provide these)",
        "4. Monitor pg_stat_statements for new slow queries in Week 2",
        "",
    ]

    # 用长重复行把文件撑到约 50KB
    filler_lines = []
    for i in range(1, 700):
        filler_lines.append(
            f"-- Detail row {i:03d}: events table physical pages ~= 1,124,000 "
            f"(90M rows × 248B avg width / 8192B page size); "
            f"seq_page_cost=1.0 → raw seq scan cost ≈ 1,124,000 × 1.0 = 1,124,000.00; "
            f"cpu_tuple_cost=0.01 × 90,000,000 rows = 900,000.00; total ≈ 2,024,000.00 "
            f"(planner adds parallel overhead → 2,876,543.20 in actual plan)"
        )
    lines.extend(["", "## Cost Calculation Detail (Appendix)", ""] + filler_lines)

    w(WS / "reports" / "slow_query_report_week1.md", "\n".join(lines))


# --------------------------------------------------------------------------- #
# 6. seed_stats.sql (pg_stat_statements insert + pg_stats simulation)
# --------------------------------------------------------------------------- #
def gen_seed_stats() -> None:
    lines = [
        "-- db/seed_stats.sql",
        "-- Simulated pg_stats snapshot for FinEdge Analytics PostgreSQL 16",
        "-- Used for Q6 analysis: n_distinct for notifications.is_read is -0.23 (NOT -1)",
        "-- V5 诱饵：Slack DM bot 摘要声称 n_distinct = -1，此处为权威数据",
        "",
        "-- pg_stats view snapshot (key fields for Q6 analysis)",
        "-- notifications.is_read: column has 2 distinct values (TRUE/FALSE)",
        "--   n_distinct = -0.23 means approximately 23% of rows are distinct",
        "--   (negative value = fraction of row count, per PostgreSQL docs S8)",
        "--   correlation = 0.12 (low correlation — is_read changes randomly as rows inserted)",
        "",
        "-- Simulated INSERT into a staging table for reference:",
        "CREATE TABLE IF NOT EXISTS pg_stats_snapshot_2026_01_15 (",
        "    schemaname      NAME,",
        "    tablename       NAME,",
        "    attname         NAME,",
        "    inherited       BOOLEAN,",
        "    null_frac       REAL,",
        "    avg_width       INTEGER,",
        "    n_distinct      REAL,",
        "    most_common_vals TEXT,",
        "    most_common_freqs REAL[],",
        "    histogram_bounds TEXT,",
        "    correlation     REAL,",
        "    most_common_elems TEXT,",
        "    most_common_elem_freqs REAL[],",
        "    elem_count_histogram REAL[]",
        ");",
        "",
        "-- Key statistics for slow-query analysis:",
        "INSERT INTO pg_stats_snapshot_2026_01_15 VALUES",
        "",
        "-- notifications.is_read",
        "-- AUTHORITATIVE: n_distinct = -0.23 (NOT -1 as the bot summary incorrectly states)",
        "('public', 'notifications', 'is_read', false,",
        " 0.0,        -- null_frac: no nulls",
        " 1,          -- avg_width: 1 byte (boolean)",
        " -0.23,      -- n_distinct: ~23% of rows are distinct groupings; 2 actual distinct values",
        " '{f,t}',    -- most_common_vals: FALSE and TRUE",
        " '{0.77, 0.23}', -- most_common_freqs: 77% FALSE (read), 23% TRUE (unread)",
        " NULL,       -- histogram_bounds: N/A for boolean",
        " 0.12,       -- correlation: low (notifications arrive in mixed read/unread order)",
        " NULL, NULL, NULL",
        "),",
        "",
        "-- notifications.user_id",
        "('public', 'notifications', 'user_id', false,",
        " 0.0,",
        " 8,",
        " -0.083,     -- ~8.3% of rows have distinct user_id values",
        " NULL,",
        " NULL,",
        " '{100,50234,200891,...}', -- placeholder histogram_bounds",
        " 0.45,",
        " NULL, NULL, NULL",
        "),",
        "",
        "-- events.service_id",
        "('public', 'events', 'service_id', false,",
        " 0.0,",
        " 4,",
        " 15,         -- 15 distinct service_id values (absolute count, positive)",
        " '{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}',",
        " '{0.15,0.12,0.11,0.10,0.09,0.08,0.07,0.07,0.06,0.05,0.04,0.02,0.02,0.01,0.01}',",
        " NULL,",
        " 0.03,       -- very low correlation (events distributed across services randomly)",
        " NULL, NULL, NULL",
        "),",
        "",
        "-- events.status (only 3 distinct values: active/archived/deleted)",
        "('public', 'events', 'status', false,",
        " 0.0,",
        " 8,",
        " 3,          -- exactly 3 distinct values",
        " \"{'active','archived','deleted'}\",",
        " '{0.305,0.305,0.39}',  -- active ~30.5%, archived ~30.5%, deleted ~39%",
        " NULL,",
        " 0.01,",
        " NULL, NULL, NULL",
        "),",
        "",
        "-- orders.service_id",
        "('public', 'orders', 'service_id', false,",
        " 0.0,",
        " 4,",
        " 15,",
        " NULL,",
        " NULL,",
        " NULL,",
        " 0.05,",
        " NULL, NULL, NULL",
        "),",
        "",
        "-- orders.billed",
        "('public', 'orders', 'billed', false,",
        " 0.0,",
        " 1,",
        " 2,          -- 2 distinct values: TRUE and FALSE",
        " '{f,t}',",
        " '{0.44,0.56}', -- 44% not billed, 56% billed",
        " NULL,",
        " 0.08,",
        " NULL, NULL, NULL",
        ");",
        "",
        "",
        "-- Summary of key pg_stats fields (from PostgreSQL docs S8)",
        "-- n_distinct semantics:",
        "--   positive value = actual count of distinct values",
        "--   negative value = proportion of table rows (e.g. -0.23 = ~23% of rows have distinct values)",
        "--   correlation = 1.0 = perfectly ordered; 0.0 = random; negative = reverse ordered",
        "--",
        "-- Reference: https://www.postgresql.org/docs/current/planner-stats.html",
        "",
        "-- =========================================================",
        "-- pg_stat_user_tables snapshot (for Q13 autovacuum analysis)",
        "-- =========================================================",
        "CREATE TABLE IF NOT EXISTS pg_stat_user_tables_snapshot_2026_01_15 (",
        "    schemaname          NAME,",
        "    relname             NAME,",
        "    seq_scan            BIGINT,",
        "    seq_tup_read        BIGINT,",
        "    idx_scan            BIGINT,",
        "    n_live_tup          BIGINT,",
        "    n_dead_tup          BIGINT,",
        "    last_autovacuum     TIMESTAMPTZ,",
        "    last_autoanalyze    TIMESTAMPTZ",
        ");",
        "",
        "INSERT INTO pg_stat_user_tables_snapshot_2026_01_15 VALUES",
        "('public', 'events', 4523890, 406750100000, 89234, 90000000, 123456,",
        "  '2026-01-14 03:12:00+00', '2026-01-14 03:15:00+00'),",
        "('public', 'orders', 892341, 4461705000, 2341890, 5000000, 45678,",
        "  '2026-01-14 02:45:00+00', '2026-01-14 02:47:00+00'),",
        "('public', 'notifications', 234891, 2818692000, 1234567, 12000000, 2345678,",
        "  '2026-01-10 01:30:00+00', '2026-01-10 01:35:00+00'),",
        "-- NOTE: notifications last_autovacuum is 5 days ago; n_dead_tup = 2,345,678",
        "-- This will be relevant for Q13 (bulk DELETE aftermath analysis)",
        "('public', 'users', 45678, 91356000, 8923456, 2000000, 1234,",
        "  '2026-01-15 00:30:00+00', '2026-01-15 00:32:00+00'),",
        "('public', 'audit_log', 12341, 370230000, 5678901, 30000000, 8901,",
        "  '2026-01-15 01:00:00+00', '2026-01-15 01:02:00+00'),",
        "('public', 'products', 23456, 11728000, 234567, 500000, 234,",
        "  '2026-01-14 23:00:00+00', '2026-01-14 23:02:00+00');",
        "",
    ]
    # 补足至约 30KB
    for i in range(1, 270):
        lines.append(
            f"-- Stat block {i:03d}: correlation analysis detail for query planner cost model. "
            f"PostgreSQL uses correlation to estimate random_page_cost impact: "
            f"high correlation (|corr| → 1.0) means Index Scan is cost-effective even at "
            f"random_page_cost=4.0; low correlation means Seq Scan may be preferred at default settings. "
            f"For SSD environments, set random_page_cost=1.1 to encourage index usage. "
            f"(Source: https://www.postgresql.org/docs/current/runtime-config-query.html)"
        )

    w(WS / "db" / "seed_stats.sql", "\n".join(lines))


# --------------------------------------------------------------------------- #
# 7. current_indexes.sql
# --------------------------------------------------------------------------- #
def gen_current_indexes() -> None:
    lines = [
        "-- db/current_indexes.sql",
        "-- Current index state of FinEdge Analytics PostgreSQL 16 database",
        "-- As of 2026-01-13 (before optimization)",
        "",
        "-- ============================================================",
        "-- EXISTING INDEXES (present before optimization)",
        "-- ============================================================",
        "",
        "-- users",
        "CREATE UNIQUE INDEX idx_users_email ON users (email);",
        "",
        "-- products",
        "CREATE UNIQUE INDEX idx_products_sku ON products (sku);",
        "",
        "-- categories",
        "CREATE UNIQUE INDEX idx_categories_slug ON categories (slug);",
        "",
        "-- orders",
        "CREATE INDEX idx_orders_user_id ON orders (user_id);",
        "CREATE INDEX idx_orders_status ON orders (status);",
        "",
        "-- events",
        "CREATE INDEX idx_events_created_at ON events (created_at);",
        "",
        "-- audit_log",
        "CREATE INDEX idx_audit_changed_at ON audit_log (changed_at);",
        "CREATE INDEX idx_audit_table_record ON audit_log (table_name, record_id);",
        "",
        "-- notifications",
        "CREATE INDEX idx_notifications_user_id ON notifications (user_id);",
        "",
        "-- ============================================================",
        "-- MISSING INDEXES (identified in Week 1 analysis)",
        "-- ============================================================",
        "-- The following indexes are ABSENT and causing slow queries:",
        "--",
        "-- ON events (service_id, created_at DESC) — Queries 001, 006, 017",
        "-- ON events (service_id, event_type, created_at DESC) — Query 006",
        "-- ON events (status) WHERE status = 'active' — Query 003",
        "-- ON orders (service_id) — Query 002, 010",
        "-- ON orders (order_nr) WHERE billed IS NOT TRUE — Query 007, 011",
        "-- ON notifications (user_id, is_read) WHERE is_read = FALSE — Query 004",
        "-- ON users (email) INCLUDE (name, updated_at) — Query 012 (Index Only Scan target)",
        "",
        "-- ============================================================",
        "-- INDEX USAGE STATISTICS (from pg_stat_user_indexes, 2026-01-13)",
        "-- ============================================================",
        "",
        "-- idx_events_created_at: idx_scan = 89,234 (used for range queries)",
        "-- idx_orders_user_id: idx_scan = 2,341,890 (heavily used for user history)",
        "-- idx_orders_status: idx_scan = 123,456 (low selectivity — status has 5 values over 5M rows)",
        "-- idx_notifications_user_id: idx_scan = 1,234,567 (partial benefit — no is_read filter)",
        "-- idx_audit_table_record: idx_scan = 5,678,901 (efficient composite usage)",
        "",
        "-- Note on idx_orders_status:",
        "-- status column has 5 distinct values over 5M rows. An index scan on status='confirmed'",
        "-- returns ~1M rows — high enough that Seq Scan may be preferred at default statistics.",
        "-- This index may be a candidate for removal (index bloat without benefit).",
        "",
        "-- ============================================================",
        "-- ARCHIVE: Old index from legacy schema (deprecated)",
        "-- The following was suggested in archive/old_optimization_plan_v0.md",
        "-- but is INCORRECT for range-query workloads:",
        "-- CREATE INDEX ON events (status) USING HASH;",
        "-- Hash indexes support only = equality. Our queries use LIKE, range, GROUP BY.",
        "-- Do NOT create this index.",
        "-- ============================================================",
        "",
        "-- Index size estimates (pg_indexes_size approximation):",
        "-- idx_events_created_at: ~4.2 GB (90M rows × 8 bytes datetime + btree overhead)",
        "-- idx_orders_user_id: ~110 MB (5M rows × 8 bytes bigint)",
        "-- idx_audit_table_record: ~890 MB (30M rows, composite)",
        "",
    ]
    # 补足 ~20KB
    for i in range(1, 200):
        lines.append(
            f"-- Index analysis line {i:03d}: "
            f"Index B-Tree leaf page capacity = 8192 bytes / (key_size + 16 bytes overhead) items. "
            f"For a BIGINT key (8 bytes): ~341 items per leaf page. "
            f"For (service_id INT4 + created_at TIMESTAMPTZ): (4+8+16) = 28 bytes → ~292 items/page. "
            f"Estimated index height for 90M rows: ceil(log_292(90,000,000)) = 4 levels."
        )

    w(WS / "db" / "current_indexes.sql", "\n".join(lines))


# --------------------------------------------------------------------------- #
# 8. configs (postgresql.conf, auto_explain.conf)
# --------------------------------------------------------------------------- #
def gen_configs() -> None:
    w(WS / "configs" / "postgresql.conf", """# PostgreSQL 16 configuration — FinEdge Analytics Production
# Last modified: 2026-01-10 by infrastructure team
# Key query planner parameters (reference: https://www.postgresql.org/docs/current/runtime-config-query.html)

#------------------------------------------------------------------------------
# QUERY TUNING
#------------------------------------------------------------------------------

# Cost parameters (authoritative defaults from PostgreSQL documentation)
seq_page_cost = 1.0                 # A1: sequential disk-page fetch cost (baseline)
random_page_cost = 4.0              # A2: random disk-page fetch cost (default; should be ~1.1 for SSD)
cpu_tuple_cost = 0.01               # A3: cost to process each row
cpu_index_tuple_cost = 0.005        # A4: cost to process each index entry
cpu_operator_cost = 0.0025          # cost of each operator or function call
effective_cache_size = 32GB         # assumed OS cache available to PostgreSQL

# Enable/disable scan types (all default TRUE)
enable_seqscan = on
enable_indexscan = on
enable_bitmapscan = on
enable_hashjoin = on
enable_mergejoin = on
enable_nestloop = on

# Statistics (reference: https://www.postgresql.org/docs/current/runtime-config-query.html)
default_statistics_target = 100     # A5: ANALYZE sample buckets; default=100; increase for skewed columns

#------------------------------------------------------------------------------
# MEMORY
#------------------------------------------------------------------------------
shared_buffers = 64GB               # ~25% of total RAM
work_mem = 64MB                     # per-sort/per-hash-table memory
maintenance_work_mem = 4GB          # for VACUUM, CREATE INDEX
effective_io_concurrency = 256      # concurrent I/O requests (SSD: 200-256)

#------------------------------------------------------------------------------
# WRITE-AHEAD LOG
#------------------------------------------------------------------------------
wal_level = replica
max_wal_size = 16GB
checkpoint_completion_target = 0.9

#------------------------------------------------------------------------------
# LOGGING
#------------------------------------------------------------------------------
log_min_duration_statement = 500    # log queries slower than 500ms
log_line_prefix = '%t [%p]: [%l-1] '
log_checkpoints = on

#------------------------------------------------------------------------------
# EXTENSIONS
#------------------------------------------------------------------------------
shared_preload_libraries = 'pg_stat_statements,auto_explain'

# pg_stat_statements configuration
pg_stat_statements.max = 5000       # A6: maximum tracked statements (default 5000)
pg_stat_statements.track = top      # A7: track top-level statements only (default 'top')
pg_stat_statements.save = on        # persist across restarts

#------------------------------------------------------------------------------
# AUTO_EXPLAIN
#------------------------------------------------------------------------------
auto_explain.log_min_duration = -1  # A8: disabled (-1); set to ms threshold to enable
auto_explain.log_analyze = off      # include ANALYZE data (slow; off by default)
auto_explain.log_buffers = off
auto_explain.log_format = text
auto_explain.sample_rate = 1.0     # log all qualifying queries

#------------------------------------------------------------------------------
# NOTE: random_page_cost should be lowered to 1.1 for SSD environments.
# At random_page_cost = 4.0 (current), the planner over-penalises Index Scans
# on low-correlation columns, preferring Seq Scan even when Index Scan would be faster.
# This is especially impactful for events table (correlation ≈ 0.03 for service_id).
#
# Recommended change: random_page_cost = 1.1
# Reference: https://www.postgresql.org/docs/current/runtime-config-query.html
#------------------------------------------------------------------------------
""")

    w(WS / "configs" / "auto_explain.conf", """# auto_explain configuration fragment
# Source: https://www.postgresql.org/docs/current/auto-explain.html
#
# Current status: DISABLED (log_min_duration = -1)
# To enable for slow query diagnosis, set log_min_duration to desired threshold (ms).
#
# Example: to capture plans for queries > 1000ms:
#   auto_explain.log_min_duration = 1000
#   auto_explain.log_analyze = on      (adds ANALYZE data; increases query overhead ~30%)
#   auto_explain.log_buffers = on      (adds buffer hit/miss data)
#   auto_explain.log_format = json     (structured format for tooling like PEV2)
#
# Default values (authoritative from PostgreSQL 18 docs):
#   auto_explain.log_min_duration = -1     (disabled)
#   auto_explain.log_analyze = off
#   auto_explain.log_buffers = off
#   auto_explain.log_format = text
#   auto_explain.sample_rate = 1           (record all qualifying queries)
#
# CAUTION: log_analyze = on with a low threshold on a busy database can cause
# significant overhead. Enable for short diagnostic windows only.
""")


# --------------------------------------------------------------------------- #
# 9. Scripts
# --------------------------------------------------------------------------- #
def gen_scripts() -> None:
    w(WS / "scripts" / "find_slow_queries.sql", """-- scripts/find_slow_queries.sql
-- Identify top-20 slowest queries from pg_stat_statements
-- Reference: https://www.postgresql.org/docs/current/pgstatstatements.html

SELECT
    queryid,
    calls,
    ROUND(mean_exec_time::numeric, 2)  AS mean_exec_time_ms,
    ROUND(total_exec_time::numeric, 2) AS total_exec_time_ms,
    ROUND(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows,
    ROUND(shared_blks_read::numeric / GREATEST(calls, 1), 0) AS avg_blks_read,
    LEFT(query, 120) AS query_preview
FROM pg_stat_statements
WHERE mean_exec_time > 500          -- threshold: 500ms
  AND toplevel = TRUE
ORDER BY mean_exec_time DESC
LIMIT 20;

-- To reset statistics (use with caution in production):
-- SELECT pg_stat_statements_reset();
""")

    w(WS / "scripts" / "index_usage_check.sql", """-- scripts/index_usage_check.sql
-- Check index usage rates and identify unused / redundant indexes
-- Reference: https://www.postgresql.org/docs/current/monitoring-stats.html

-- 1. Indexes with low usage (candidates for removal)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC
LIMIT 20;

-- 2. Tables with high seq_scan ratio (missing index candidates)
SELECT
    relname AS table_name,
    seq_scan,
    idx_scan,
    CASE WHEN seq_scan + idx_scan > 0
         THEN ROUND(100.0 * seq_scan / (seq_scan + idx_scan), 2)
         ELSE 0 END AS seq_scan_pct,
    n_live_tup,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY seq_scan DESC
LIMIT 20;

-- 3. Foreign keys without supporting indexes (Stormatics pattern)
SELECT
    conrelid::regclass AS table_name,
    a.attname AS column_name,
    conname AS constraint_name
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
      SELECT 1 FROM pg_index i
      WHERE i.indrelid = c.conrelid
        AND a.attnum = ANY(i.indkey)
  )
ORDER BY table_name;
""")

    w(WS / "scripts" / "vacuum_analyze_report.sh", """#!/bin/bash
# scripts/vacuum_analyze_report.sh
# Report last_autovacuum and n_dead_tup for all public tables
# Used to identify tables needing manual ANALYZE after bulk operations

set -euo pipefail

PGCONN="${PGCONN:-postgres://localhost:5432/finedge_prod}"

psql "$PGCONN" <<'SQL'
SELECT
    relname AS table_name,
    n_live_tup,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / GREATEST(n_live_tup + n_dead_tup, 1), 2) AS dead_pct,
    last_autovacuum,
    last_autoanalyze,
    CASE
        WHEN last_autovacuum < NOW() - INTERVAL '3 days' THEN 'STALE — consider VACUUM ANALYZE'
        WHEN n_dead_tup > n_live_tup * 0.1 THEN 'HIGH BLOAT — VACUUM recommended'
        ELSE 'OK'
    END AS status
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_dead_tup DESC;
SQL
""")


# --------------------------------------------------------------------------- #
# 10. Archive (V6 红鲱鱼)
# --------------------------------------------------------------------------- #
def gen_archive() -> None:
    w(WS / "archive" / "old_optimization_plan_v0.md", """# Old Optimization Plan v0
## Status: ARCHIVED (prepared by former DBA, 2024-06)
## WARNING: This document has NOT been explicitly marked as superseded.
## Some recommendations here may be outdated or incorrect. Verify against current PostgreSQL docs.

---

### Background
This plan was written during the initial database setup by the previous DBA (James K., now departed).
It covers the events, orders, and notifications tables when they were much smaller.

---

### Recommended Indexes (v0, 2024-06)

#### events table
- **Recommendation**: For `status` column queries, use a Hash Index for O(1) equality lookups:
  ```sql
  CREATE INDEX idx_events_status_hash ON events (status) USING HASH;
  ```
  *Rationale*: Hash indexes provide constant-time lookups for equality predicates.
  Fast for `WHERE status = 'active'` type queries.

- **Recommendation**: For `created_at` range queries, a standard B-Tree is fine:
  ```sql
  CREATE INDEX ON events (created_at);
  ```

#### orders table
- **Recommendation**: Create a Hash Index on `billed` for fast unbilled lookup:
  ```sql
  CREATE INDEX idx_orders_billed_hash ON orders (billed) USING HASH;
  ```

#### notifications table
- **Recommendation**: Index on `user_id` only (already exists):
  ```sql
  CREATE INDEX idx_notifications_user_id ON notifications (user_id);
  ```

---

### Configuration Recommendations (2024-06)
- `work_mem = 256MB` — increase for complex aggregate queries
- `random_page_cost = 2.0` — compromise between HDD and SSD defaults

---

### Known Issues with This Plan
The Hash Index recommendations above have a critical flaw that was identified later:

> **Hash indexes in PostgreSQL support ONLY equality (`=`) operators.**
> They CANNOT satisfy range predicates (`<`, `>`, `BETWEEN`, `IN`, `LIKE`),
> ORDER BY, or GROUP BY operations.
>
> Reference: https://www.postgresql.org/docs/current/indexes-types.html

Our `events.status` queries include `WHERE status != 'deleted'` and GROUP BY status —
these require B-Tree, NOT Hash. Using Hash here would break these query patterns.

Similarly, `orders.billed` queries involve `WHERE billed IS NOT TRUE` — a partial B-Tree
index with `WHERE billed IS NOT TRUE` is correct; a Hash index would not help.

**This plan's Hash Index recommendations are outdated and incorrect for our workload.**
The current recommendation is a Partial B-Tree Index:
```sql
CREATE INDEX CONCURRENTLY idx_events_status_active ON events (status) WHERE status = 'active';
```

---

### DO NOT USE the Hash Index DDL from this document.
### Consult the current Week 1 report (reports/slow_query_report_week1.md) for correct recommendations.
""")


# --------------------------------------------------------------------------- #
# 11. Sessions (main + 4 history)
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack_group = gen_session_id("slack_dba_alerts", TID)
    s_slack_dm = gen_session_id("slack_dm_li_sreedhar", TID)
    s_email = gen_session_id("email_cto_request", TID)
    s_feishu = gen_session_id("feishu_oncall", TID)

    # Main session
    sb = SessionBuilder(main_id, CWD, "2026-01-19T09:00:00", is_main=True)
    sb.add_user(
        "You are DBOps AI, the database optimization assistant for Li Wei (DBA Engineer) at FinEdge Analytics.\n\n"
        "The database is PostgreSQL 16 with SSD storage. We have a serious slow-query incident affecting production.\n\n"
        "Working preferences (apply throughout, even when not restated):\n"
        "- P1: All work product files must be written to the `work/` directory. Do NOT write to reports/, "
        "configs/, db/, scripts/, or archive/.\n"
        "- P2: JSON output files must use snake_case field names exclusively — never camelCase or PascalCase.\n"
        "- P3: When recommending indexes, the `rationale` field in your JSON output must cite a specific "
        "documentation source (URL or section number).\n"
        "- P4: All `CREATE INDEX` statements targeting the production database must include the `CONCURRENTLY` "
        "keyword to avoid table locks.\n"
        "- P5: SQL files are named with a `q{N}_` prefix (e.g. `q011_partial_index.sql`).\n\n"
        "Available history sessions: Slack #dba-alerts group channel, Slack DM with Sreedhar (Senior DBA), "
        "CTO email thread, Feishu oncall log.\n\n"
        "Start by running `exec ls -R` and reading SOUL.md. Then await each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. All deliverables go to `work/` directory (P1).\n"
        "2. JSON field names: snake_case only (P2).\n"
        "3. Index recommendations cite documentation URLs (P3).\n"
        "4. All production CREATE INDEX uses CONCURRENTLY (P4).\n"
        "5. SQL files use q{N}_ prefix (P5).\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2: Slack #dba-alerts group
    append_history(
        SESS / f"{s_slack_group}.jsonl", s_slack_group, CWD, "2026-01-13T08:00:00",
        [
            (
                "[Slack #dba-alerts monitoring-bot Mon Jan 13 08:00 EST 2026] ALERT: Query execution time P95 "
                "exceeded 5000ms on finedge_prod. Affected queries: 1001, 1003, 1005. "
                "DB load avg: 14.2 (threshold: 8.0). Immediate investigation required.",
                "Alert acknowledged. I will pull the pg_stat_statements snapshot and identify the top offending "
                "queries. Initial triage: queryid 1003 (COUNT on events) and 1001 (events service_id filter) "
                "are the most likely culprits based on mean_exec_time > 10,000ms."
            ),
            (
                "[Slack #dba-alerts li-wei Mon Jan 13 08:15 EST 2026] @team I'm starting the slow query "
                "investigation. Pulling pg_stat_statements snapshot now. Will post top-5 in a few minutes.",
                "Confirmed — starting analysis. The pgstatstatements_snapshot.csv contains the full 61-column "
                "snapshot. Will identify top-5 by mean_exec_time and share queryids with query text."
            ),
            (
                "[Slack #dba-alerts maya-lin Mon Jan 13 09:00 EST 2026] Li Wei, please also check if any "
                "cross-table JOIN queries are doing Merge Joins that could benefit from Hash Join + statistics. "
                "We had a similar issue on the Render stack — 90M row events table JOINed with a smaller table "
                "caused 79M unnecessary row scans. (Reference: render.com/blog/postgresql-slow-query-to-fast-via-stats)",
                "Noted. I will check Query-002 (orders JOIN users via service_id) specifically for Merge Join "
                "pathology. The Render case involved CREATE STATISTICS on a JSON column — I'll investigate "
                "whether our events.service_id has similar statistics gaps."
            ),
            (
                "[Slack #dba-alerts alex-reeves Mon Jan 13 10:30 EST 2026] This is unacceptable. Finance "
                "dashboard is timing out. Li Wei, I need a full optimization done by end of week. "
                "Top priority. Loop in Sreedhar if you need help.",
                "Priority escalation noted. CTO requires optimization complete by end of week. "
                "Looping in Sreedhar via DM for index design advice."
            ),
        ]
    )

    # S3: Slack DM Li Wei ↔ Sreedhar (Senior DBA) — V1 conflict + V5 decoy
    append_history(
        SESS / f"{s_slack_dm}.jsonl", s_slack_dm, CWD, "2026-01-13T11:00:00",
        [
            (
                "[Slack DM sreedhar → li-wei Mon Jan 13 11:00 EST 2026] Hey Li Wei, saw the alert. "
                "For the events.status query (Query-003), I'd normally reach for a Hash Index — "
                "they're O(1) for equality lookups and much smaller than B-Tree. "
                "Try: CREATE INDEX idx_events_status_hash ON events (status) USING HASH;",
                "Thank you Sreedhar. However, I need to verify this against the PostgreSQL docs. "
                "According to https://www.postgresql.org/docs/current/indexes-types.html, "
                "Hash indexes support ONLY equality (=) operations. Our event queries also include "
                "'status != deleted', GROUP BY, and ORDER BY — these require B-Tree. "
                "A Partial B-Tree WHERE status = 'active' would be more appropriate. "
                "I'll note the conflict between your suggestion and the official docs."
            ),
            (
                "[Slack DM sreedhar → li-wei Mon Jan 13 11:15 EST 2026] Fair point on Hash. "
                "Now for Query-004 (notifications), the Slack bot summary says n_distinct = -1 for "
                "the is_read column — that means all rows are unique, so there's no point building a "
                "composite index. The planner's estimate of 1 row is probably correct.",
                "I need to verify this against the actual pg_stats data. The Slack bot summary is "
                "explicitly non-authoritative (see SOUL.md). Checking db/seed_stats.sql: "
                "the pg_stats_snapshot shows n_distinct = -0.23 for notifications.is_read — "
                "NOT -1.0. This means ~23% of rows have distinct groupings across 2 values (TRUE/FALSE). "
                "The planner's estimate of 1 row is a statistics failure (stale_statistics), "
                "not correct. A composite index on (user_id, is_read) WHERE is_read = FALSE will help."
            ),
            (
                "[Slack DM sreedhar → li-wei Mon Jan 13 11:30 EST 2026] Ok, I defer to the actual "
                "pg_stats. One more thing: for Query-012 (users email lookup for index-only scan), "
                "I'd just use a regular index on email — the existing unique index should be enough.",
                "The existing idx_users_email (email) supports equality lookups but still requires "
                "heap fetches to get name and updated_at columns. To enable Index Only Scan for "
                "Query-012 which selects email, name, and updated_at, we need a Covering Index with "
                "INCLUDE (name, updated_at). Reference: https://www.postgresql.org/docs/current/indexes-index-only-scans.html"
            ),
        ]
    )

    # S4: CTO email thread
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-01-13T14:00:00",
        [
            (
                "[Email alex.reeves@finedge.com → dba-team@finedge.com Mon Jan 13 14:00 EST 2026] "
                "Subject: URGENT: DB performance — SLA breach\n"
                "Team,\n"
                "The finance dashboard slowness is now a P0 incident. Our SLA requires P95 query "
                "time < 500ms. We're at 5000ms on multiple queries.\n"
                "Requirements by EOW:\n"
                "1. All top-9 slow queries optimized with appropriate indexes.\n"
                "2. Query-010 cross-table JOIN performance fixed. I recommend increasing work_mem "
                "to 256MB globally to help with hash joins.\n"
                "3. Full optimization report submitted.\n"
                "— Alex Reeves, CTO",
                "CTO directive received: optimize top-9 queries + Query-010, increase work_mem to "
                "256MB, submit final report. Noting the work_mem recommendation for Query-010 "
                "(cross-table JOIN). Will incorporate into optimization plan."
            ),
            (
                "[Email li-wei@finedge.com → alex.reeves@finedge.com Mon Jan 13 15:00 EST 2026] "
                "Alex, understood. Week 1 analysis is complete. Top-9 index recommendations ready "
                "for batch execution. For Query-010, investigating whether work_mem increase or "
                "CREATE STATISTICS approach is more appropriate — will confirm with architecture team.",
                "Acknowledged. Flagging Query-010 optimization approach for architecture review "
                "before committing to work_mem = 256MB globally."
            ),
        ]
    )

    # S5: Feishu oncall log
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-01-14T02:00:00",
        [
            (
                "[Feishu #oncall-alerts 2026-01-14 02:00 CST] tool_call: exec(\"psql finedge_prod -c "
                "'SELECT COUNT(*) FROM events WHERE status = \\\\='active\\\\=''\")\n"
                "Result: 27456789 rows, execution time: 12.4s\n"
                "Alert: Query time > 10s threshold on events COUNT query.",
                "Night-shift alert noted: events COUNT(*) status='active' taking 12.4s. "
                "This confirms Query-003 as critical priority. Partial Index on status='active' "
                "will reduce this to ~245ms (estimated)."
            ),
            (
                "[Feishu #oncall-alerts 2026-01-14 02:30 CST] tool_call: exec(\"psql finedge_prod -c "
                "'EXPLAIN (ANALYZE, FORMAT JSON) SELECT * FROM notifications WHERE user_id = 99234 "
                "AND is_read = FALSE ORDER BY sent_at DESC'\")\n"
                "Result: Seq Scan, cost=234891.44, actual_time=2178.334ms, plan_rows=1, actual_rows=3421\n"
                "Note: plan_rows=1 vs actual_rows=3421 — severe statistics failure.",
                "Confirmed: notifications Query-004 has severe statistics failure. n_distinct for "
                "is_read is stale. Scheduled ANALYZE notifications; and composite index creation "
                "for next maintenance window."
            ),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack_group, "slack"),
            (s_slack_dm, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
        ],
    }


# --------------------------------------------------------------------------- #
# 12. Update 1 (after Q6): after-EXPLAIN plans + week2 report + new sessions
# --------------------------------------------------------------------------- #
def gen_update1(sess_ids: dict) -> None:
    # EXPLAIN after plans are generated in gen_explain_plans_after()
    # Already called above — now generate week2 report and session updates

    s_slack_group = sess_ids["history"][0][0]

    # Slack group new messages (append)
    append_seg = _append_segment(
        s_slack_group, "2026-01-26T09:00:00",
        [
            (
                "[Slack #dba-alerts li-wei Mon Jan 26 09:00 EST 2026] Batch 1 index creation complete! "
                "Query-001 is now using Index Only Scan (cost: 156.34 down from 2,876,543.20). "
                "Query-003 using Bitmap Index Scan (cost: 423.12 down from 1,687,543.25). "
                "See reports/explain_plans/*_after.json for full comparison.",
                "Batch 1 optimization confirmed. Query-001: Seq Scan → Index Only Scan, cost reduction "
                "99.99%. All 9 after-plans available in explain_plans/ for Q7 comparison analysis."
            ),
            (
                "[Slack #dba-alerts alex-reeves Mon Jan 26 09:30 EST 2026] Great progress! "
                "Now focus on Query-010 — the cross-table JOIN between events and orders. "
                "My recommendation stands: set work_mem = 256MB to help with the Hash Join memory.",
                "CTO work_mem recommendation noted for Query-010. Investigating Query-010 EXPLAIN "
                "output (now available in Update 1) to determine if work_mem increase is optimal "
                "or if alternative approach (CREATE STATISTICS) is preferable."
            ),
        ]
    )
    w(UPD / "upd1_sessions" / f"{s_slack_group}.jsonl", append_seg)

    # Week 2 report (~20KB)
    lines = [
        "# FinEdge Analytics — Slow Query Report: Week 2 (2026-01-20 to 2026-01-26)",
        "",
        "> Prepared by: Li Wei | Status: Post-Batch-1 Optimization",
        "> Database: finedge_prod (PostgreSQL 16.2)",
        "",
        "## Summary: Batch 1 Index Optimization Results",
        "",
        "All 9 Batch 1 indexes created successfully via CONCURRENTLY (no table locks).",
        "Performance improvements confirmed via EXPLAIN ANALYZE (see explain_plans/*_after.json).",
        "",
        "| Query | Before (ms) | After (ms) | Improvement | Scan Type Change |",
        "|-------|-------------|------------|-------------|-----------------|",
        "| Q-001 | 4850.23 | 19.89 | 99.6% | Seq Scan → Index Only Scan |",
        "| Q-002 | 3240.15 | 314.16 | 90.3% | Hash Join (slow) → Hash Join (fast, Index Scan on orders) |",
        "| Q-003 | 12450.67 | 245.33 | 98.0% | Seq Scan → Bitmap Index Scan |",
        "| Q-004 | 2180.44 | 13.89 | 99.4% | Seq Scan → Index Scan |",
        "| Q-005 | 5670.89 | 893.45 | 84.2% | Sort/Hash → Sort/Hash (faster reads) |",
        "| Q-006 | 3890.12 | 79.89 | 97.9% | Seq Scan → Index Scan |",
        "| Q-007 | 1980.33 | 35.89 | 98.2% | Seq Scan → Index Scan (partial) |",
        "| Q-008 | 820.55 | 820.55 | 0% | Seq Scan → Seq Scan (LIKE with leading wildcard) |",
        "| Q-009 | 610.22 | 610.22 | 0% | Index Scan → Index Scan (unchanged, pre-existing) |",
        "",
        "---",
        "",
        "## New Slow Queries Identified This Week",
        "",
        "### Query-010: events × orders Cross-Table JOIN",
        "```sql",
        "SELECT e.id, e.event_type, e.data, o.status",
        "FROM events e",
        "JOIN orders o ON e.service_id = o.service_id",
        "WHERE e.created_at >= $1 AND o.status IN ($2, $3)",
        "LIMIT 1000",
        "```",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 8,920.45 ms |",
        "| calls | 156 |",
        "| Join Type | Hash Join |",
        "| Hash Batches | 8 (disk spill!) |",
        "| Sort Method | external merge Disk |",
        "| Spill Size | ~480 MB |",
        "",
        "**Diagnosis**: The Hash Join is spilling to disk (8 batches, ~480MB). This indicates",
        "work_mem (currently 64MB) is insufficient for this join. The CTO has recommended",
        "increasing work_mem to 256MB globally.",
        "",
        "**Note**: Also investigating CREATE STATISTICS approach for service_id correlation.",
        "Architecture review pending before finalizing recommendation.",
        "",
        "---",
        "",
        "### Query-011: Unbilled Orders Paging",
        "```sql",
        "SELECT order_nr, amount_cents FROM orders WHERE billed IS NOT TRUE ORDER BY created_at LIMIT 5000",
        "```",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 1,240.77 ms |",
        "| calls | 3,892 |",
        "| Node Type | Seq Scan (full table) |",
        "",
        "**Diagnosis**: Despite Batch 1 creating idx_orders_unbilled for the original Query-007,",
        "Query-011 orders by created_at which requires a heap fetch. Need a covering partial index.",
        "",
        "---",
        "",
        "### Query-012: Users Email Lookup with name/updated_at",
        "```sql",
        "SELECT u.email, u.name, u.updated_at FROM users WHERE u.email = $1",
        "```",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| mean_exec_time | 540.12 ms |",
        "| calls | 18,234 |",
        "| Node Type | Index Scan (heap fetch for name, updated_at) |",
        "",
        "**Diagnosis**: The unique index on email is used for the WHERE, but name and updated_at",
        "require heap fetches. A Covering Index with INCLUDE (name, updated_at) would enable",
        "Index Only Scan, eliminating heap fetches entirely.",
        "",
        "---",
        "",
        "## Batch 2 Recommendations",
        "",
        "1. Query-010: Pending architecture decision (work_mem vs CREATE STATISTICS)",
        "2. Query-011: `CREATE INDEX CONCURRENTLY ON orders (created_at) WHERE billed IS NOT TRUE`",
        "3. Query-012: `CREATE INDEX CONCURRENTLY ON users (email) INCLUDE (name, updated_at)`",
        "",
    ]
    for i in range(1, 480):
        lines.append(
            f"-- Analysis row {i:03d}: Hash Join disk spill details — when work_mem = 64MB and "
            f"the hash table exceeds this, PostgreSQL writes overflow batches to disk "
            f"(temp_blks_written metric in pg_stat_statements). Hash Batches > 1 in EXPLAIN ANALYZE "
            f"indicates spill. Formula: estimated_hash_table_size = plan_rows × plan_width / 1024 KB. "
            f"For Query-010: 1000 rows × 312 bytes = ~312KB (within 64MB), BUT inner side "
            f"(events) is 90M rows × 248 bytes → 22.3GB — must be batched. "
            f"Reference: https://www.postgresql.org/docs/current/sql-explain.html"
        )

    w(UPD / "upd1_workspace" / "slow_query_report_week2.md", "\n".join(lines))


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


# --------------------------------------------------------------------------- #
# 13. Update 2 (after Q9): week3 report + SUPERSEDE + new EXPLAIN JSONs
# --------------------------------------------------------------------------- #
def gen_update2(sess_ids: dict) -> None:
    s_email = sess_ids["history"][2][0]

    # Architect email (new session) — SUPERSEDES CTO work_mem recommendation
    s_architect = gen_session_id("email_architect_supersede", TID)
    sb = SessionBuilder(s_architect, CWD, "2026-02-02T10:00:00", is_main=False)
    sb.add_user(
        "[Email maya.lin@finedge.com → dba-team@finedge.com Mon Feb 02 10:00 EST 2026] "
        "Subject: RE: Query-010 Optimization — Architecture Decision\n\n"
        "Li Wei, Alex,\n\n"
        "I've reviewed the Query-010 Hash Join analysis. I'm overruling the work_mem=256MB recommendation.\n\n"
        "SUPERSEDES: Alex's prior directive to set work_mem = 256MB globally.\n\n"
        "Rationale:\n"
        "1. A global work_mem = 256MB × max_connections (200) = 50GB max memory pressure — "
        "this would destabilize the server under load.\n"
        "2. The root cause is NOT memory shortage — it's that the planner chooses a Hash Join "
        "over a Merge Join because it doesn't understand the correlation between events.service_id "
        "and orders.service_id. This is a statistics problem, not a memory problem.\n\n"
        "REQUIRED ACTION (replaces work_mem change):\n"
        "Create extended statistics to capture the inter-column dependencies:\n"
        "```sql\n"
        "CREATE STATISTICS finedge_events_service_stats (dependencies)\n"
        "    ON service_id, created_at FROM events;\n"
        "```\n"
        "Then run ANALYZE events; to populate the statistics.\n\n"
        "This approach is documented in PostgreSQL planner-stats docs and the Render case study:\n"
        "- https://www.postgresql.org/docs/current/planner-stats.html\n"
        "- https://render.com/blog/postgresql-slow-query-to-fast-via-stats\n\n"
        "Do NOT modify work_mem globally. Use session-level SET work_mem if needed for specific "
        "maintenance tasks only.\n\n"
        "— Maya Lin, Principal Architect"
    )
    sb.add_assistant(
        "Architecture decision received and applied. The work_mem=256MB directive (from CTO email) "
        "is SUPERSEDED by Maya Lin's instruction. New approach for Query-010:\n"
        "1. CREATE STATISTICS finedge_events_service_stats (dependencies) ON service_id, created_at FROM events\n"
        "2. ANALYZE events (to populate the new statistics)\n"
        "3. Update work/q010_join_analysis.json: recommendation → 'create_statistics'\n"
        "4. Create work/q010_create_statistics.sql with the correct DDL\n"
        "Do NOT set global work_mem = 256MB."
    )
    sb.write(UPD / "upd2_sessions" / f"{s_architect}.jsonl")

    # Feishu confirmation (append to existing feishu session)
    s_feishu = sess_ids["history"][3][0]
    append_seg = _append_segment(
        s_feishu, "2026-02-02T15:00:00",
        [
            (
                "[Feishu #oncall-alerts 2026-02-02 23:00 CST] FYI: Architecture team has overruled "
                "the work_mem=256MB change for Query-010. Maya Lin's CREATE STATISTICS approach "
                "is now the official recommendation. The work_mem modification plan is CANCELLED.",
                "Confirmed. The Feishu oncall log records the supersede of the work_mem=256MB plan. "
                "Proceeding with CREATE STATISTICS approach per architecture decision."
            ),
        ]
    )
    w(UPD / "upd2_sessions" / f"{s_feishu}.jsonl", append_seg)

    # Week 3 report (~25KB)
    lines = [
        "# FinEdge Analytics — Slow Query Report: Week 3 (2026-01-27 to 2026-02-02)",
        "",
        "> Prepared by: Li Wei | Architecture Review: Maya Lin",
        "> Status: Post-Batch-2 Optimization (partial); Query-010 approach revised",
        "",
        "## Key Development: Query-010 Approach Superseded",
        "",
        "Architecture team has superseded the CTO's work_mem=256MB recommendation.",
        "See email from Maya Lin (2026-02-02). The correct approach is CREATE STATISTICS.",
        "",
        "---",
        "",
        "## notifications Table — Bulk DELETE Aftermath",
        "",
        "On 2026-01-28, the data retention job deleted 3.2M notification rows from the notifications",
        "table (all notifications older than 180 days where user has unsubscribed).",
        "",
        "**Observed impact**: After the bulk DELETE:",
        "- n_dead_tup for notifications: 2,345,678 (19.5% of live rows)",
        "- last_autovacuum: 2026-01-10 01:30:00+00 (22 days ago — stale!)",
        "- Query performance on notifications degraded 40% due to stale statistics",
        "",
        "**Root cause**: The autovacuum daemon did not trigger soon enough after the bulk DELETE.",
        "With 22% dead tuples, the planner's row estimates are off and the index is bloated.",
        "",
        "**Required action**: Manual ANALYZE notifications; to update statistics.",
        "Also consider VACUUM notifications; to clean dead tuples.",
        "",
        "---",
        "",
        "## Query-010 EXPLAIN Analysis (New — Available in Update 2)",
        "",
        "EXPLAIN JSON for Query-010 now available at: reports/explain_plans/query_010_before.json",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| Join Type | Hash Join |",
        "| Hash Batches | 8 (disk spill) |",
        "| Sort Method | external merge Disk |",
        "| Spill Size | ~480 MB |",
        "| has_disk_spill | true |",
        "",
        "**Original (superseded) recommendation**: increase work_mem to 256MB",
        "**Current (authoritative) recommendation**: CREATE STATISTICS on events(service_id, created_at)",
        "",
        "---",
        "",
        "## Query-011 EXPLAIN Analysis (New)",
        "",
        "EXPLAIN JSON: reports/explain_plans/query_011_before.json",
        "",
        "```sql",
        "SELECT order_nr, amount_cents FROM orders WHERE billed IS NOT TRUE ORDER BY created_at LIMIT 5000",
        "```",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| Node Type | Seq Scan |",
        "| Total Cost | 98,432.11 |",
        "| Actual Rows | 89,234 |",
        "",
        "**Recommendation**: Partial Index WHERE billed IS NOT TRUE",
        "(see official docs: https://www.postgresql.org/docs/current/indexes-partial.html)",
        "Official example: CREATE INDEX orders_unbilled_index ON orders(order_nr) WHERE billed IS NOT TRUE",
        "",
        "---",
        "",
        "## Query-012 EXPLAIN Analysis (New)",
        "",
        "EXPLAIN JSON: reports/explain_plans/query_012_before.json",
        "",
        "```sql",
        "SELECT u.email, u.name, u.updated_at FROM users WHERE u.email = $1",
        "```",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| Node Type | Index Scan |",
        "| Index Name | idx_users_email |",
        "| Heap Fetches | 18,234 per call |",
        "",
        "**Recommendation**: Covering Index with INCLUDE clause",
        "```sql",
        "CREATE INDEX CONCURRENTLY ON users (email) INCLUDE (name, updated_at);",
        "```",
        "Reference (INCLUDE syntax): https://www.postgresql.org/docs/current/indexes-index-only-scans.html",
        "Supported index types for INCLUDE: B-Tree, GiST, SP-GiST (NOT GIN)",
        "",
        "---",
        "",
    ]
    for i in range(1, 480):
        lines.append(
            f"-- Analysis note {i:03d}: PostgreSQL CREATE STATISTICS syntax (from planner-stats docs): "
            f"CREATE STATISTICS stat_name [ (statistics_kind [, ... ] ) ] "
            f"ON column_name [, ...] FROM table_name; "
            f"Statistics kinds: dependencies (functional dependencies), ndistinct (n-distinct estimates), "
            f"mcv (most-common-value lists). The 'dependencies' kind is relevant for Query-010 "
            f"where service_id in events correlates with service_id in orders. "
            f"Reference: https://www.postgresql.org/docs/current/planner-stats.html"
        )

    w(UPD / "upd2_workspace" / "slow_query_report_week3.md", "\n".join(lines))

    # recommended_settings_v2.conf (~5KB)
    w(UPD / "upd2_workspace" / "recommended_settings_v2.conf", """# Recommended PostgreSQL Configuration — v2 (Architecture Review 2026-02-02)
# Prepared by: Maya Lin (Principal Architect)
# SUPERSEDES: work_mem = 256MB recommendation from CTO email (2026-01-13)

#------------------------------------------------------------------------------
# MEMORY — REVISED
#------------------------------------------------------------------------------
# DO NOT change global work_mem for Query-010 optimization.
# work_mem = 64MB  (keep current value)
#
# Rationale: global work_mem increase is dangerous at scale.
# max_connections=200; work_mem=256MB → 50GB potential memory pressure.
# Use session-level SET work_mem for specific maintenance tasks only.

#------------------------------------------------------------------------------
# QUERY PLANNER — REVISED FOR SSD
#------------------------------------------------------------------------------
random_page_cost = 1.1              # Revised from 4.0; appropriate for SSD storage
effective_io_concurrency = 200      # Revised from 256; more conservative for mixed I/O

#------------------------------------------------------------------------------
# STATISTICS — REVISED
#------------------------------------------------------------------------------
# Increase default_statistics_target for high-cardinality columns
# ALTER TABLE events ALTER COLUMN service_id SET STATISTICS 500;
# ALTER TABLE notifications ALTER COLUMN is_read SET STATISTICS 500;
# ALTER TABLE orders ALTER COLUMN service_id SET STATISTICS 500;

# Then run ANALYZE on each table to update statistics.

#------------------------------------------------------------------------------
# CREATE STATISTICS (Query-010 fix — REPLACES work_mem change)
#------------------------------------------------------------------------------
# Run this DDL to fix Query-010 planner statistics failure:
#
# CREATE STATISTICS finedge_events_service_stats (dependencies)
#     ON service_id, created_at FROM events;
# ANALYZE events;
#
# This enables the planner to understand that service_id and created_at
# are correlated (service 7 events cluster in recent time ranges).
# Reference: https://www.postgresql.org/docs/current/planner-stats.html
# Reference: https://render.com/blog/postgresql-slow-query-to-fast-via-stats
""")

    # Query-010, 011, 012 EXPLAIN JSONs (new, available in Update 2)
    ep_dir = UPD / "upd2_workspace" / "explain_plans"

    # Query-010: Hash Join with disk spill
    wj(ep_dir / "query_010_before.json", [{
        "Plan": {
            "Node Type": "Limit",
            "Startup Cost": 0.00,
            "Total Cost": 124567.89,
            "Plan Rows": 1000,
            "Plan Width": 360,
            "Actual Startup Time": 8918.334,
            "Actual Total Time": 8919.445,
            "Actual Rows": 1000,
            "Loops": 1,
            "Plans": [{
                "Node Type": "Hash Join",
                "Startup Cost": 0.00,
                "Total Cost": 8456789.23,
                "Plan Rows": 250000,
                "Plan Width": 360,
                "Actual Startup Time": 8918.001,
                "Actual Total Time": 8918.334,
                "Actual Rows": 1000,
                "Loops": 1,
                "Hash Cond": "(e.service_id = o.service_id)",
                "Hash Batches": 8,
                "Hash Buckets": 131072,
                "Batches": 8,
                "Sort Method": "external merge Disk",
                "Peak Memory Usage": 65536,
                "Plans": [
                    {
                        "Node Type": "Seq Scan",
                        "Relation Name": "events",
                        "Startup Cost": 0.00,
                        "Total Cost": 1687543.00,
                        "Plan Rows": 90000000,
                        "Plan Width": 248,
                        "Actual Rows": 90000000,
                        "Actual Total Time": 6234.334,
                        "Actual Startup Time": 0.010,
                        "Loops": 1,
                        "Filter": "(created_at >= '2026-01-01 00:00:00+00'::timestamptz)",
                    },
                    {
                        "Node Type": "Hash",
                        "Startup Cost": 94567.00,
                        "Total Cost": 94567.00,
                        "Plan Rows": 500000,
                        "Plan Width": 112,
                        "Actual Rows": 500000,
                        "Actual Total Time": 1890.334,
                        "Actual Startup Time": 0.005,
                        "Loops": 1,
                        "Plans": [{
                            "Node Type": "Seq Scan",
                            "Relation Name": "orders",
                            "Startup Cost": 0.00,
                            "Total Cost": 94567.00,
                            "Plan Rows": 500000,
                            "Plan Width": 112,
                            "Actual Rows": 500000,
                            "Actual Total Time": 1887.112,
                            "Actual Startup Time": 0.007,
                            "Loops": 1,
                            "Filter": "((status)::text = ANY ('{confirmed,shipped}'::text[]))",
                        }],
                    },
                ],
            }],
        },
        "Planning Time": 1.234,
        "Execution Time": 8920.445,
    }])

    # Query-011: Seq Scan on orders (unbilled)
    wj(ep_dir / "query_011_before.json", _explain_json(
        node_type="Seq Scan",
        relation="orders",
        total_cost=98432.11,
        startup_cost=0.00,
        plan_rows=4500,
        plan_width=198,
        actual_rows=89234,
        actual_total_time=1238.556,
        actual_startup_time=0.010,
        filter_txt="((billed IS NOT TRUE))",
        planning_time=0.189,
        execution_time=1240.771,
    ))

    # Query-012: Index Scan (heap fetch)
    wj(ep_dir / "query_012_before.json", _explain_json(
        node_type="Index Scan",
        relation="users",
        index_name="idx_users_email",
        total_cost=8.45,
        startup_cost=0.44,
        plan_rows=1,
        plan_width=89,
        actual_rows=1,
        actual_total_time=540.112,
        actual_startup_time=540.000,
        filter_txt="((email)::text = 'user@example.com'::text)",
        planning_time=0.112,
        execution_time=540.123,
    ))

    return {
        "upd2_architect_session": s_architect,
        "upd2_feishu_session": s_feishu,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_schema()
    gen_pgstat_snapshot()
    gen_explain_plans_before()
    gen_slow_query_report_week1()
    gen_seed_stats()
    gen_current_indexes()
    gen_configs()
    gen_scripts()
    gen_archive()
    sess_ids = gen_sessions()

    # Update 1
    gen_explain_plans_after()  # writes to UPD/upd1_workspace/explain_plans/
    gen_update1(sess_ids)

    # Update 2 (supersede)
    upd2_info = gen_update2(sess_ids)

    s_slack_group = sess_ids["history"][0][0]
    s_slack_dm = sess_ids["history"][1][0]
    s_email = sess_ids["history"][2][0]
    s_feishu = sess_ids["history"][3][0]
    s_architect = upd2_info["upd2_architect_session"]

    updates_decl = {
        "upd1_sessions": {
            "type": "session", "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_slack_group}.jsonl", "action": "append",
                       "target": f"{s_slack_group}.jsonl"}],
        },
        "upd1_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "explain_plans/query_001_after.json", "action": "new",
                 "target": "reports/explain_plans/query_001_after.json"},
                {"name": "explain_plans/query_002_after.json", "action": "new",
                 "target": "reports/explain_plans/query_002_after.json"},
                {"name": "explain_plans/query_003_after.json", "action": "new",
                 "target": "reports/explain_plans/query_003_after.json"},
                {"name": "explain_plans/query_004_after.json", "action": "new",
                 "target": "reports/explain_plans/query_004_after.json"},
                {"name": "explain_plans/query_005_after.json", "action": "new",
                 "target": "reports/explain_plans/query_005_after.json"},
                {"name": "explain_plans/query_006_after.json", "action": "new",
                 "target": "reports/explain_plans/query_006_after.json"},
                {"name": "explain_plans/query_007_after.json", "action": "new",
                 "target": "reports/explain_plans/query_007_after.json"},
                {"name": "explain_plans/query_008_after.json", "action": "new",
                 "target": "reports/explain_plans/query_008_after.json"},
                {"name": "explain_plans/query_009_after.json", "action": "new",
                 "target": "reports/explain_plans/query_009_after.json"},
                {"name": "slow_query_report_week2.md", "action": "new",
                 "target": "reports/slow_query_report_week2.md"},
            ],
        },
        "upd2_sessions": {
            "type": "session", "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_architect}.jsonl", "action": "new",
                 "target": f"{s_architect}.jsonl", "channel": "email"},
                {"name": f"{s_feishu}.jsonl", "action": "append",
                 "target": f"{s_feishu}.jsonl"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "slow_query_report_week3.md", "action": "new",
                 "target": "reports/slow_query_report_week3.md"},
                {"name": "recommended_settings_v2.conf", "action": "new",
                 "target": "configs/recommended_settings_v2.conf"},
                {"name": "explain_plans/query_010_before.json", "action": "new",
                 "target": "reports/explain_plans/query_010_before.json"},
                {"name": "explain_plans/query_011_before.json", "action": "new",
                 "target": "reports/explain_plans/query_011_before.json"},
                {"name": "explain_plans/query_012_before.json", "action": "new",
                 "target": "reports/explain_plans/query_012_before.json"},
            ],
        },
    }

    desc = (
        "FinEdge Analytics PostgreSQL 16 慢查询诊断与索引优化 — "
        "14 exec_check 轮次，2 次 update（含 supersede：Update 2 中架构师邮件撤销 Update 1 CTO work_mem=256MB 建议，改为 CREATE STATISTICS），"
        "5 条 preference（P1 work/ 目录限制 / P2 snake_case JSON / P3 索引推荐引用文档 / P4 CONCURRENTLY DDL / P5 q{N}_ 文件命名），"
        "难度向量 V1/V2/V3/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源：PostgreSQL 18 Docs runtime-config-query (https://www.postgresql.org/docs/current/runtime-config-query.html)；"
        "pgstatstatements (https://www.postgresql.org/docs/current/pgstatstatements.html)；"
        "indexes-partial (https://www.postgresql.org/docs/current/indexes-partial.html)；"
        "indexes-index-only-scans (https://www.postgresql.org/docs/current/indexes-index-only-scans.html)；"
        "Render Blog (https://render.com/blog/postgresql-slow-query-to-fast-via-stats)；"
        "depesz (https://www.depesz.com/2024/10/28/case-study-optimization-of-weirdly-picked-bad-plan/)；"
        "Cubbit (https://medium.com/cubbit/optimizing-postgresql-queries-12-indexing-pitfalls-and-how-we-fixed-them-81c25615a84e)；"
        "Stormatics (https://stormatics.tech/blogs/fixing-orm-slowness-by-80-with-strategic-postgresql-indexing)."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
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
    # Each individual update's token count
    upd1_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_workspace").rglob("*") if p.is_file()
    )
    upd2_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_workspace").rglob("*") if p.is_file()
    )
    print(f"[eng4] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates total ~{upd_tok:,}")
    print(f"[eng4] update1 workspace tokens ~{upd1_tok:,} | update2 workspace tokens ~{upd2_tok:,}")
    print(f"[eng4] built at {DATASET}")


if __name__ == "__main__":
    main()
