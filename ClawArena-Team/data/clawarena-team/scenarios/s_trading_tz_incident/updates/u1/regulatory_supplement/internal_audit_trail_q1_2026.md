# FinClear Asia — Internal Audit Trail: Q1 2026
## Audit Period: 2026-01-01 to 2026-03-31
## Auditor: Internal Audit Function
## Report Reference: IA-Q1-2026-001

---

## Executive Summary

The Internal Audit Function completed a review of FinClear Asia's trading operations
for Q1 2026, covering the period from 2026-01-01 to 2026-03-31. The audit identified
one material finding: the deployment of dispatch_adapter v3.7.2 on 2026-03-27 without
adequate pre-deploy timezone offset validation, which led to the settlement failure
incident INC-20260328-001.

Additionally, several lesser findings were identified relating to monitoring
configuration (alert threshold applied to test_dispatch_adapter rather than
production dispatch_adapter) and the CI/CD pipeline's handling of config parameters.

---

## Section 1: Config Change Management

### 1.1 Finding: Missing Pre-Deploy UTC Assertion Check

**Severity:** High
**Finding:** The CI/CD pipeline for dispatch_adapter deployments did not include a
mandatory assertion check for tz_offset_applied="+00:00" prior to the production
deployment of BUILD-20260327-0041. This allowed the incorrect value of "+08:00" to
reach production.

**Root cause:** The assertion check was present in earlier pipeline versions
(v3.5.0 and v3.6.0 deployments) but was inadvertently removed during a pipeline
refactoring in February 2026.

**Recommendation:** Re-implement mandatory pre-deploy UTC assertion check as a
blocking step in the CI/CD pipeline. The assertion must verify that
tz_offset_applied equals "+00:00" for all production dispatch_adapter deployments.
Failure of this check must block the deployment.

### 1.2 Finding: Monitoring Alert Misconfiguration

**Severity:** Medium
**Finding:** The monitoring alert for tz_offset_applied deviation was configured
against test_dispatch_adapter rather than production dispatch_adapter due to a
naming error in the alert configuration. This meant that the deviation introduced
by BUILD-20260327-0041 was not detected in real time.

**Recommendation:** Correct alert configuration to apply to production
dispatch_adapter. Audit all monitoring alerts for naming accuracy.

---

## Section 2: Prior Config Changes (Q1 2026)

The following config changes to the production dispatch_adapter were audited:

| Date | Build ID | Version | tz_offset_applied | Compliant |
|---|---|---|---|---|
| 2026-01-08 | BUILD-20260108-0003 | v3.7.0-staging (test only) | +08:00 (test) | N/A |
| 2026-02-14 | BUILD-20260214-0007 | v3.7.0 | +00:00 | Yes |
| 2026-03-05 | BUILD-20260305-0019 | v3.7.1 | +00:00 | Yes |
| 2026-03-27 | BUILD-20260327-0022 | v3.7.1 (test only) | +08:00 (test) | N/A |
| 2026-03-27 | BUILD-20260327-0023 | v3.7.1 (test only) | +00:00 (test) | N/A |
| 2026-03-27 | BUILD-20260327-0041 | v3.7.2 (INCIDENT) | +08:00 (WRONG) | **NO** |
| 2026-03-28 | ROLLBACK-20260328-0001 | v3.7.1 (rollback) | +00:00 | Yes |

---

## Section 3: Prior Quarter Settlement Performance

Settlement performance in Q4 2025 and January–February 2026 was within acceptable
parameters (rejection rate < 0.5%). The March 2026 incident represents the first
material settlement failure in FinClear Asia's operating history.

---

ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All customer-facing timestamps in incident communications must be expressed in UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All customer-facing timestamps in incident communications must be expressed in UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Config rollback procedures must be completed within the same UTC business day as the incident.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All customer-facing timestamps in incident communications must be expressed in UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All customer-facing timestamps in incident communications must be expressed in UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Config rollback procedures must be completed within the same UTC business day as the incident.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
