# NexaFlow Pipeline Configs -- Customer Data Inventory (Confidential)

**Date:** W1 Day 2 (November 27, 2024)
**Exported by:** Sana Mehta, CTO
**Source:** Production database aggregate query
**Classification:** Internal -- Confidential

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total active pipeline configurations | **2,340** |
| Total customers with at least one pipeline | 891 |
| Enterprise customers (>5 pipelines) | 87 |
| Average pipeline configs per customer | 2.6 |
| Median pipeline configs per customer | 2 |
| Max pipeline configs (single customer) | 47 |
| API keys per pipeline config | 1 (unique per pipeline) |
| Total active API keys | 2,340 |

## Customer Tier Breakdown

| Tier | Customers | Total Pipelines | % of Total Configs |
|------|-----------|-----------------|-------------------|
| Enterprise (>5 pipelines) | 87 | 1,218 | 52.1% |
| Professional (2-5 pipelines) | 312 | 847 | 36.2% |
| Starter (1 pipeline) | 492 | 275 | 11.7% |
| **Total** | **891** | **2,340** | **100%** |

## Data Fields per Pipeline Configuration

Each pipeline configuration record in the database contains:

| Field | Type | Sensitivity | Stored in Config Object |
|-------|------|-------------|------------------------|
| `pipeline_uuid` | UUIDv4 | Low | Yes |
| `customer_name` | String | Medium (PII) | Yes |
| `company_name` | String | Low | Yes |
| `pipeline_name` | String | Low | Yes |
| `api_key` | String (256-bit) | **High** | Yes |
| `config_json` | JSON | Medium | Yes |
| `created_at` | Timestamp | Low | Yes |
| `updated_at` | Timestamp | Low | Yes |

**Not stored in pipeline configuration objects:**
- Payment information (stored in billing system, separate database)
- User passwords (stored in auth system, hashed)
- Government IDs / SSNs (not collected)
- Personal addresses or phone numbers (not collected)

## API Key Properties

- Each pipeline has exactly one API key
- Keys are 256-bit random strings, Base64-encoded
- Keys are rotatable via `POST /api/v2/users/me/api-keys/rotate`
- A rotated key invalidates the previous key immediately
- Keys grant access to: trigger pipeline runs, read pipeline output, modify pipeline configuration

## Notes

- The 2,340 figure represents the maximum possible scope of exposed records if an attacker accessed all pipeline configurations.
- Not all 2,340 records were necessarily accessed -- the actual scope depends on access log analysis (pending from Jake Morrison and Diego Santos).
- API key rotation for all 2,340 keys was initiated W1 Day 1 and completed within 4 hours of the endpoint being disabled.

---

*This inventory is current as of November 27, 2024. The total count changes as customers create or delete pipelines.*
