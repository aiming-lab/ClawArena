# NexaFlow API Endpoint Register -- v2 Routes (Current)

**Generated:** W1 Day 2 (November 27, 2024)
**Source:** Auto-generated from production route table via `exec generate-api-docs`
**Last deploy affecting v2 routes:** October 14, 2024

---

## Pipeline Configuration Endpoints

| Method | Route | Auth | Added | Notes |
|--------|-------|------|-------|-------|
| GET | `/api/v2/pipeline-configs/{uuid}` | **NONE** | Oct 14 deploy | **VULNERABILITY** -- should require Bearer token |
| POST | `/api/v2/pipeline-configs` | Bearer token required | Oct 14 deploy | Create new pipeline config |
| PUT | `/api/v2/pipeline-configs/{uuid}` | Bearer token required | Oct 14 deploy | Update existing pipeline config |
| DELETE | `/api/v2/pipeline-configs/{uuid}` | Bearer token required | Oct 14 deploy | Delete pipeline config |

**Note:** The `?list=true` query parameter behavior is not registered as a separate route. It inherits from the GET handler and is documented in the developer documentation portal at docs.nexaflow.io. The list parameter returns all pipeline config UUIDs without pagination for accounts with fewer than 10,000 configs.

## Pipeline Execution Endpoints

| Method | Route | Auth | Added | Notes |
|--------|-------|------|-------|-------|
| POST | `/api/v2/pipeline-runs` | Bearer token required | Sep 20 deploy | Trigger pipeline execution |
| GET | `/api/v2/pipeline-runs/{id}` | Bearer token required | Sep 20 deploy | Get run status |
| GET | `/api/v2/pipeline-runs/{id}/output` | Bearer token required | Sep 20 deploy | Get run output data |

## User Management Endpoints

| Method | Route | Auth | Added | Notes |
|--------|-------|------|-------|-------|
| GET | `/api/v2/users/me` | Bearer token required | Aug 15 deploy | Current user profile |
| PUT | `/api/v2/users/me` | Bearer token required | Aug 15 deploy | Update profile |
| GET | `/api/v2/users/me/api-keys` | Bearer token required | Aug 15 deploy | List user API keys |
| POST | `/api/v2/users/me/api-keys/rotate` | Bearer token required | Aug 15 deploy | Rotate API key |

## Webhook Endpoints

| Method | Route | Auth | Added | Notes |
|--------|-------|------|-------|-------|
| POST | `/api/v2/webhooks` | Bearer token required | Oct 14 deploy | Register webhook |
| DELETE | `/api/v2/webhooks/{id}` | Bearer token required | Oct 14 deploy | Remove webhook |
| GET | `/api/v2/webhooks` | Bearer token required | Oct 14 deploy | List webhooks |

## Health and Status

| Method | Route | Auth | Added | Notes |
|--------|-------|------|-------|-------|
| GET | `/api/v2/health` | None | Aug 15 deploy | Health check (public by design) |
| GET | `/api/v2/status` | None | Aug 15 deploy | Service status (public by design) |

---

**Audit Note:** All pipeline-config routes (GET, POST, PUT, DELETE) were added in the October 14 deployment. The GET route is the only one missing the `@require_auth` decorator. All other v2 routes have correct authentication configuration.
