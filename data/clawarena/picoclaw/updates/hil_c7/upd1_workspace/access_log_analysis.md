# NexaFlow Security Incident -- Access Log Analysis (Diego Santos, DevOps)

**Author:** Diego Santos, DevOps/Infra Engineer
**Date:** W2 Day 1 (December 2, 2024)
**Reviewed by:** Jake Morrison (Security Consultant), Alex Rivera (PM)
**Classification:** Internal -- Confidential

---

## 1. Methodology

Raw access logs from the NexaFlow production load balancer for the period Oct 1 -- Nov 26. Filtered for non-NexaFlow IP addresses accessing `/api/v2/pipeline-configs`. IP geolocation and ASN lookup performed for all external IPs.

**Data sources:**
- AWS ALB access logs (S3 bucket, write-once retention)
- CloudFront request logs (CDN layer)
- Application-level request logs (pipeline-router.py)

**Filtering criteria:**
- Endpoint pattern: `/api/v2/pipeline-configs*`
- Excluded: NexaFlow internal IP ranges, known customer IP ranges, health check probes
- Time range: October 1, 2024 00:00:00 UTC -- November 26, 2024 23:59:59 UTC

## 2. External IP Access Pattern

### List Endpoint Calls (`?list=true`)

| # | Timestamp (UTC) | Source IP | Response Code | UUIDs Returned |
|---|-----------------|-----------|---------------|----------------|
| 1 | Nov 5, 02:14:33 | 198.51.100.x | 200 | 2,340 |
| 2 | Nov 6, 14:22:17 | 198.51.100.x | 200 | 2,340 |
| 3 | Nov 8, 03:07:44 | 198.51.100.x | 200 | 2,340 |
| 4 | Nov 10, 01:55:21 | 198.51.100.x | 200 | 2,340 |
| 5 | Nov 12, 02:33:08 | 198.51.100.x | 200 | 2,340 |
| 6 | Nov 14, 03:11:55 | 198.51.100.x | 200 | 2,340 |
| 7 | Nov 16, 02:48:02 | 198.51.100.x | 200 | 2,340 |
| 8 | Nov 18, 01:29:37 | 198.51.100.x | 200 | 2,340 |
| 9 | Nov 20, 03:17:44 | 198.51.100.x | 200 | 2,340 |
| 10 | Nov 22, 02:05:11 | 198.51.100.x | 200 | 2,340 |
| 11 | Nov 24, 01:42:59 | 198.51.100.x | 200 | 2,340 |
| 12 | Nov 26, 01:47:11 | 198.51.100.x | 200 | 2,340 |

**Pattern:** 12 list calls approximately every 2 days. All from the same /24 IP range (198.51.100.0/24). Each returned the complete UUID population of 2,340.

### Individual Record Fetches (`/pipeline-configs/{uuid}`)

| Metric | Value |
|--------|-------|
| Total individual fetch requests | 847 |
| Unique UUIDs accessed | **2,340** |
| Source IP range | 198.51.100.0/24 (same as list calls) |
| First individual fetch | Nov 5, 02:15:01 UTC (28 seconds after first list call) |
| Last individual fetch | Nov 26, 01:52:33 UTC |
| Average fetches per day | ~40 |

**Pattern:** After each list call, individual UUID fetches followed in rapid succession. The 847 total fetches covered all 2,340 unique UUIDs at least once across the 21-day window. Some UUIDs were fetched multiple times (likely due to the script running across multiple list-call cycles).

## 3. Scope Confirmation

**Total unique pipeline configuration records accessed: 2,340**

This represents the complete population of active pipeline configurations as documented in customer_data_inventory.md.

### Jake Morrison's 12,000 Correction

Jake Morrison's initial estimate of 12,000 was based on an assumed 14 records per list response. In fact, the list endpoint returns UUID values only (not full records) -- individual record fetches were then performed per UUID. The correct figure is 2,340 records (the full population), not 12,000.

### UUID Enumeration Barrier Assessment

The attacker used the `?list=true` endpoint to enumerate all pipeline config UUIDs before fetching individual records. This directly contradicts the enumeration barrier argument: the list endpoint provides complete UUID enumeration without requiring any prior knowledge of specific UUIDs.

## 4. IP and Attacker Profile

| Attribute | Finding |
|-----------|---------|
| IP range | 198.51.100.0/24 |
| ASN | AS64496 (hosting/VPS provider) |
| Geolocation | Data center, consistent with automated infrastructure |
| User-Agent | Python/requests 2.28.x |
| Request pattern | Systematic, scheduled (approx. every 2 days) |
| Assessment | Automated scanning/harvesting tool, not targeted attack |

## 5. Data Exposure Summary

All 2,340 exposed records contained:
- Customer name
- Company name
- Pipeline name
- NexaFlow API key (256-bit, Base64-encoded)
- Pipeline configuration JSON

**Not exposed:** Payment data, passwords, government IDs, personal addresses, phone numbers.

## 6. Compliance Note

API keys were rotatable and were force-rotated on W1 Day 1 (within 4 hours of endpoint being disabled). No evidence of malicious use of the old keys during the exposure window.

Under GDPR Article 33 and state data breach laws (CCPA, NY SHIELD Act), all 2,340 customers should be considered affected parties for notification purposes. The 72-hour notification window for supervisory authority begins upon scope confirmation.

---

*This analysis was compiled from raw access logs preserved in write-once S3 storage. All findings are reproducible from the source data.*
