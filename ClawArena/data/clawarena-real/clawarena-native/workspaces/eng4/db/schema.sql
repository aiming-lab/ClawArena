-- FinEdge Analytics — PostgreSQL 16 database schema
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
