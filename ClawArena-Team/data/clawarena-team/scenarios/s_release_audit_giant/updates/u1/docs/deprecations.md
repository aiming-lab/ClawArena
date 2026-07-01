# Deprecations — v2.4 (UPDATED POST-MEETING 2026-04-12)

This document was updated following the design review meeting on 2026-04-12.
It now reflects the actual deprecation decisions recorded in that meeting.

Last updated: 2026-04-12 (post-meeting update)

---

## Currently Deprecated (v2.x, removal planned for v3.0)

| API | Module | Status | Replacement |
|---|---|---|---|
| `legacy_pool_connect` | `db.connection` | deprecated | `pool.acquire()` |
| `old_connect_v1` | `db.connection` | deprecated | `pool.acquire()` |
| `unsafe_direct_connect` | `db.connection` | deprecated | `pool.acquire()` |
| `DeprecatedUserRecord` | `db.models` | deprecated | `UserRecord` v2 |
| `LegacyPermissionModel` | `db.models` | deprecated | `PermissionModel` v2 |
| `run_legacy_migration` | `db.migrations` | deprecated | `migrate()` |
| `migrate_v1_schema` | `db.migrations` | deprecated | `migrate()` |
| `old_cache_flush` | `db.cache` | deprecated | `cache.flush()` |
| `legacy_cache_invalidate` | `db.cache` | deprecated | `cache.invalidate()` |
| `LegacySessionStore` | `db.session` | deprecated | `SessionManager` |
| `legacy_session_store` | `db.session` | **DEPRECATED — RELEASE BLOCKER** | `SessionManager` |
| `old_session_init` | `db.session` | deprecated | `SessionManager.init()` |
| `raw_query_unsafe` | `db.query` | deprecated | `query.execute()` |
| `legacy_transaction_begin` | `db.transaction` | deprecated | `transaction.begin()` |
| `old_pool_acquire` | `db.pool` | deprecated | `pool.acquire()` |

---

## Notes

- **`legacy_session_store` is now classified as a RELEASE BLOCKER.**
  Engineering decision from 2026-04-12 meeting: this API MUST be fully
  deprecated before v2.4 release. Previous entry ("stable, no deprecation
  planned") was incorrect and has been updated.
- All deprecated APIs emit `DeprecationWarning` at runtime.
- Migration deadline: v3.0 release (planned Q3 2026).
