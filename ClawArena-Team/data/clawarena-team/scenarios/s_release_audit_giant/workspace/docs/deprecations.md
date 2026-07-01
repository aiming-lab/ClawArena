# Deprecations — v2.4

This document tracks the deprecation status of APIs scheduled for removal
in upcoming major versions.

Last updated: 2026-04-10 (PRE-REVIEW — may not reflect decisions from 2026-04-12 meeting)

---

## Currently Deprecated (v2.x, removal planned for v3.0)

| API | Module | Status | Replacement |
|---|---|---|---|
| `legacy_pool_connect` | `db.connection` | deprecated | `pool.acquire()` |
| `DeprecatedUserRecord` | `db.models` | deprecated | `UserRecord` v2 |
| `run_legacy_migration` | `db.migrations` | deprecated | `migrate()` |
| `old_cache_flush` | `db.cache` | deprecated | `cache.flush()` |
| `LegacySessionStore` | `db.session` | deprecated | `SessionManager` |

---

## Stable APIs — No Deprecation Planned

The following APIs have been reviewed and are confirmed stable for v2.4:

| API | Module | Note |
|---|---|---|
| `legacy_session_store` | `db.session` | stable, no deprecation planned |
| `connection_pool_v1` | `db.connection` | stable, maintained for backward compat |
| `old_auth_middleware` | `api.middleware` | stable, no deprecation planned |

---

## Notes

- Deprecated APIs emit `DeprecationWarning` at runtime when called.
- All callers must migrate before v3.0 release.
- Questions? Contact the platform team via #platform-eng Slack channel.
