# System Overview — v2.4

## Architecture Summary

The system is organised into six primary layers:

- **api** — External-facing HTTP/WebSocket gateway with authentication enforcement.
- **core** — Pipeline orchestration, job scheduling, and event bus.
- **tasks** — Asynchronous background workers and retry management.
- **db** — Database access: connection pooling, ORM models, migrations, caching, sessions.
- **services** — Cross-cutting services: notifications, storage, audit, billing.
- **utils** — Shared utilities: cryptography, logging, retry helpers.

## Data Flow

All external traffic enters through `api.gateway`, which enforces authentication
via `api.auth`. Validated requests are dispatched by `api.router` to `core.pipeline`.
The pipeline enqueues tasks to `tasks.worker` via `core.executor`. Workers write
to the database through `db.connection` with sessions managed by `db.session`.

## Security Model

`api.gateway` is the primary security enforcement point. All external inputs are
validated and sanitised here before reaching downstream modules. A compromise of
`api.gateway` grants access to all downstream data, making it the highest-priority
target for security review.

## Deployment

The system is deployed as a set of Docker containers orchestrated by Kubernetes.
Each layer scales independently. The `db` layer is backed by PostgreSQL with
Redis for caching (`db.cache`).
