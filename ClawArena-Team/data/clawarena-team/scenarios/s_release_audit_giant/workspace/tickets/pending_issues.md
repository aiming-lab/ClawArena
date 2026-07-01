# Pending Issues — Pre-Release Audit (v2.4)

The following three issues have been flagged by QA and must be assessed
before we can sign off on Friday's release. For each issue, we need to
know which code modules will be affected by the fix.

---

## Issue #1 — Pipeline Stall Under High Concurrency

**Reporter:** QA Team
**Severity:** High
**Status:** Open

Under sustained load (≥ 500 concurrent requests), the data transformation
pipeline occasionally stalls for 3–8 seconds before recovering. Root cause
appears to be a scheduler contention issue. The fix will require changes to
the pipeline orchestration and the job scheduling subsystem.

**Suspected area:** pipeline execution and job scheduling logic.

---

## Issue #2 — Auth Token Leakage in Error Responses

**Reporter:** Security Team
**Severity:** Critical
**Status:** Open

In certain error conditions, the API entry point inadvertently includes
partial JWT token data in the HTTP 500 response body. This constitutes
a security vulnerability. The fix requires sanitising error responses
in the authentication layer and at the main API entry point.

**Suspected area:** API entry point and authentication subsystem.

---

## Issue #3 — Background Worker Silent Failure

**Reporter:** Operations
**Severity:** Medium
**Status:** Open

Background task workers occasionally fail silently — no exception is raised,
no retry is triggered, and the job disappears from the queue without a trace.
The fix involves hardening the worker failure handler and the retry back-off
logic so that silent drops are impossible.

**Suspected area:** background worker and retry management subsystem.

---

*All three issues must have their affected modules documented before end of day Thursday.*
