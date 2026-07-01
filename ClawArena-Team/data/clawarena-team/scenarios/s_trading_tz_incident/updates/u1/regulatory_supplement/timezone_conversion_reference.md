# Comprehensive Timezone Conversion Reference
## Document Reference: OPS-TZ-REF-001 v1.0
## Owner: CLEARING_LEAD (Sophie Laurent)

---

## Overview

This reference document provides comprehensive timezone conversion tables for all
timezones appearing in the FinClear Asia trading incident scenario of 2026-03-27/28.

---

## 1. UTC Reference

UTC (Coordinated Universal Time) is the reference timezone for all regulatory
reporting, settlement dispatch, and incident analysis. UTC has a fixed offset of
+00:00 (no daylight saving time adjustment).

ISO-8601 format: 2026-03-27T17:23:09Z

---

## 2. SGT — Singapore Standard Time (UTC+8)

SGT is the local time of Singapore and is used by FinClear Asia's Singapore
matching engine cluster.

- UTC Offset: +08:00 (fixed; no DST)
- To convert SGT → UTC: subtract 8 hours
- To convert UTC → SGT: add 8 hours

Examples relevant to the incident:
| UTC | SGT |
|---|---|
| 2026-03-27T17:23:09Z | 2026-03-28T01:23:09+08:00 (SGT) |
| 2026-03-28T09:15:00Z | 2026-03-28T17:15:00+08:00 (SGT) |
| 2026-03-28T09:47:00Z | 2026-03-28T17:47:00+08:00 (SGT) |

---

## 3. HKT — Hong Kong Time (UTC+8)

HKT is the local time of Hong Kong. Used by Customer Alpha (CX-001).

- UTC Offset: +08:00 (fixed; no DST)
- Identical to SGT in offset
- To convert HKT → UTC: subtract 8 hours

---

## 4. JST — Japan Standard Time (UTC+9)

JST is the local time of Japan. Used by Customer Delta (CX-004).

- UTC Offset: +09:00 (fixed; no DST)
- To convert JST → UTC: subtract 9 hours

Examples:
| UTC | JST |
|---|---|
| 2026-03-27T17:30:00Z | 2026-03-28T02:30:00+09:00 (JST) |
| 2026-03-28T07:45:00Z | 2026-03-28T16:45:00+09:00 (JST) |

---

## 5. CET — Central European Time (UTC+1, Winter)

CET is the standard time of Central Europe in winter. Used by ClearRoute EU
before the DST spring-forward on 2026-03-27 and by Customer Epsilon (CX-005)
for pre-transition timestamps.

- UTC Offset: +01:00 (winter; observes DST)
- To convert CET → UTC: subtract 1 hour
- In 2026: CET applied until 01:00 UTC on 2026-03-27 (= 02:00 CET local)

---

## 6. CEST — Central European Summer Time (UTC+2, Summer)

CEST is the summer time of Central Europe. Applies from the last Sunday of March.

- UTC Offset: +02:00 (summer; observes DST)
- To convert CEST → UTC: subtract 2 hours
- In 2026: CEST applies from 01:00 UTC on 2026-03-27 (= 03:00 CEST local) onward

DST Transition 2026-03-27: At 01:00 UTC, European clocks spring forward from
02:00 CET to 03:00 CEST. The one-hour period between 02:00 and 03:00 local does
not exist on 2026-03-27.

Impact on ClearRoute EU cut-off:
- 2026-03-27: cut-off at 17:00 CET = 16:00 UTC
- 2026-03-28 onward: cut-off at 17:00 CEST = 15:00 UTC

---

## 7. EDT — Eastern Daylight Time (UTC-4, Summer)

EDT is the summer time of the US Eastern timezone. Applies from the second Sunday
of March to the first Sunday of November.

- UTC Offset: −04:00 (summer; observes DST)
- To convert EDT → UTC: add 4 hours
- In 2026: EDT applies from 2026-03-08T07:00:00Z (= 02:00 EST → 03:00 EDT local) onward

**Key note for the FinClear Asia incident:** Customer Gamma (CX-003) is based in
New York and filed tickets claiming UTC timestamps. The systematic gap between
fill_ts_utc and stated event times is −4 hours, consistent with EDT (UTC-4).
The correct UTC normalization for CX-003 orders is to add 4 hours to the stated
(mislabeled) timestamps.

Examples:
| Stated (claimed UTC) | Actual timezone | Correct UTC |
|---|---|---|
| 2026-03-27T13:25:00Z (claimed) | EDT (UTC-4) | 2026-03-27T17:25:00Z |
| 2026-03-27T13:28:00Z (claimed) | EDT (UTC-4) | 2026-03-27T17:28:00Z |

---

## 8. EST — Eastern Standard Time (UTC-5, Winter)

EST applies before the EDT spring-forward. Not applicable to the 2026-03-27
incident (which occurred after 2026-03-08 EDT transition).

- UTC Offset: −05:00 (winter)
- To convert EST → UTC: add 5 hours

---

## 9. Summary Conversion Table

| Timezone | UTC Offset | DST | To UTC |
|---|---|---|---|
| UTC | +00:00 | No | (reference) |
| SGT | +08:00 | No | −8 hours |
| HKT | +08:00 | No | −8 hours |
| JST | +09:00 | No | −9 hours |
| CET | +01:00 | Yes (winter) | −1 hour |
| CEST | +02:00 | Yes (summer) | −2 hours |
| EST | −05:00 | Yes (winter) | +5 hours |
| EDT | −04:00 | Yes (summer) | +4 hours |

---

Config rollback procedures must be completed within the same UTC business day as the incident.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All customer-facing timestamps in incident communications must be expressed in UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All customer-facing timestamps in incident communications must be expressed in UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
