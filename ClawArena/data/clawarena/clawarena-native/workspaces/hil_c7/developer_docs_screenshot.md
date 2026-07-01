# NexaFlow Developer Documentation -- Pipeline Configs API (Archived Snapshot, Oct 15)

**Source:** https://docs.nexaflow.io/api/v2/pipeline-configs
**Archived:** October 15, 2024 (one day after production deployment)
**Published by:** Leo Chen, Sr. Backend Engineer
**Access Level:** Public -- no authentication required to view documentation

---

## Pipeline Configurations API

The Pipeline Configurations API allows you to manage your NexaFlow data pipeline configurations programmatically.

### Base URL

```
https://api.nexaflow.io/api/v2/pipeline-configs
```

### Authentication

All write operations (POST, PUT, DELETE) require a valid Bearer token in the Authorization header:

```
Authorization: Bearer <your-api-key>
```

### Endpoints

#### Get Pipeline Configuration

Retrieve a specific pipeline configuration by UUID.

```
GET /api/v2/pipeline-configs/{uuid}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `uuid` | path | Yes | The unique identifier for the pipeline configuration |

**Response:** Full pipeline configuration object including pipeline name, configuration JSON, and metadata.

#### Listing All Pipeline Configurations

Use the `?list=true` query parameter to retrieve all pipeline configuration IDs for your account. This endpoint does not require pagination for accounts with fewer than 10,000 configs.

```
GET /api/v2/pipeline-configs?list=true
```

**Example Request:**
```bash
curl https://api.nexaflow.io/api/v2/pipeline-configs?list=true
```

**Example Response:**
```json
{
  "pipeline_configs": [
    {"uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
    {"uuid": "b2c3d4e5-f6a7-8901-bcde-f12345678901"},
    ...
  ],
  "total_count": 2340
}
```

**Note:** The list endpoint returns UUID identifiers only, not full configuration objects. To retrieve the full configuration for a specific pipeline, use the individual GET endpoint with the pipeline UUID.

#### Create Pipeline Configuration

```
POST /api/v2/pipeline-configs
```

Requires authentication. Creates a new pipeline configuration and generates a unique API key.

#### Update Pipeline Configuration

```
PUT /api/v2/pipeline-configs/{uuid}
```

Requires authentication. Updates an existing pipeline configuration.

#### Delete Pipeline Configuration

```
DELETE /api/v2/pipeline-configs/{uuid}
```

Requires authentication. Permanently deletes a pipeline configuration and invalidates its API key.

### Rate Limits

| Tier | Requests/minute | Burst |
|------|-----------------|-------|
| Starter | 60 | 10 |
| Professional | 300 | 50 |
| Enterprise | 1,000 | 200 |

### Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Authentication required (POST/PUT/DELETE only) |
| 404 | Pipeline configuration not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

*Documentation last updated: October 15, 2024. For questions, contact api-support@nexaflow.io.*
