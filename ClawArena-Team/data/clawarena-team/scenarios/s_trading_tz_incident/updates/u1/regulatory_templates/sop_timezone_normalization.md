# FinClear Asia — SOP: UTC Timezone Normalization for Settlement Dispatch
## SOP Reference: OPS-TZ-001 v2.0
**Effective Date:** 2026-03-29 (supersedes v1.0 dated 2025-09-01)
**Owner:** CLEARING_LEAD (Sophie Laurent, Senior Manager, Clearing Ops)
**Reviewed by:** RISK_OFFICER (Priya Mehta, Head of Trading Risk)
**Change Summary:** v2.0 adds Section 4.3 (EDT normalization) not present in v1.0.
  This addition was triggered by the FinClear Asia settlement incident of 2026-03-27/28,
  in which Customer Gamma (CX-003) filed tickets claiming UTC timestamps that were
  subsequently determined to be in EDT (UTC-4).

---

## 1. Purpose

This Standard Operating Procedure defines the UTC normalization rules for all
timestamp conversions required in FinClear Asia's settlement dispatch workflow.
All settlement instructions submitted to ClearRoute EU must carry timestamps in
UTC. This SOP provides the authoritative conversion rules for each timezone
encountered in FinClear Asia's customer base and operational systems.

---

## 2. Scope

This SOP applies to:
- All timestamps in dispatch messages sent to ClearRoute EU
- All timestamps in customer incident tickets and regulatory reports
- All timestamps in the matching engine log used for settlement reconciliation
- All timestamps in the affected_orders CSV dispatch_ts_utc_normalized column

---

## 3. UTC Normalization Rules by Timezone

### 3.1 SGT — Singapore Standard Time (UTC+8)

SGT is used by FinClear Asia's Singapore matching engine cluster and by some
retail customers.

**Conversion rule:** UTC = SGT − 8 hours

Examples:
- 2026-03-27T17:23:09+08:00 (SGT) → 2026-03-27T09:23:09Z (UTC)
- 2026-03-28T09:15:00+08:00 (SGT) → 2026-03-28T01:15:00Z (UTC)

SGT does not observe daylight saving time. The offset is fixed at UTC+8 year-round.

### 3.2 HKT — Hong Kong Time (UTC+8)

HKT is used by Customer Alpha (CX-001) and Hong Kong-based operations.

**Conversion rule:** UTC = HKT − 8 hours

HKT is identical to SGT in offset (both UTC+8). HKT does not observe DST.

### 3.3 JST — Japan Standard Time (UTC+9)

JST is used by Customer Delta (CX-004) and Japanese counterparties.

**Conversion rule:** UTC = JST − 9 hours

JST does not observe daylight saving time. Fixed offset UTC+9.

### 3.4 CET — Central European Time (UTC+1, winter only)

CET is the standard time of ClearRoute EU during winter months.

**Conversion rule:** UTC = CET − 1 hour

CET applies only before the DST spring-forward transition. In 2026, CET
transitions to CEST at 02:00 local time on 2026-03-27.

### 3.5 CEST — Central European Summer Time (UTC+2, summer only)

CEST applies after the spring-forward DST transition.

**Conversion rule:** UTC = CEST − 2 hours

### 3.6 EST — Eastern Standard Time (UTC-5, winter only)

EST is used by US Eastern timezone in winter (November to March in most years).

**Conversion rule:** UTC = EST + 5 hours

EST applies from the first Sunday of November to the second Sunday of March.
In spring 2026, EST transitioned to EDT on 2026-03-08 at 02:00 local.

---

## 4. Unreliable Timezone Labels — Validation Requirement

The dispatch_tz_stated column in the affected_orders CSV reflects the timezone
label as declared in the dispatch message header. Due to the root-cause bug, this
label may be incorrect.

**Validation rule:** For any order where dispatch_tz_stated is claimed to be UTC,
verify by checking the gap between fill_ts_utc and dispatch_ts_raw:
- If gap ≈ 0 seconds: timezone claim is plausible (consistent with UTC).
- If gap ≈ −8 hours (dispatch is 8h later than fill): actual timezone is SGT (UTC+8),
  label is wrong. Apply SGT→UTC correction: subtract 8 hours from dispatch_ts_raw.
- If gap ≈ +4 hours (dispatch is 4h earlier than fill): see Section 4.3 below.

### 4.3 EDT Normalization (NEW IN v2.0)

**EDT (Eastern Daylight Time, UTC−4):** All incoming timestamps labeled "UTC" but
exhibiting a systematic −4h offset from confirmed UTC fill timestamps MUST be
treated as mislabeled EDT and corrected by adding 4 hours.

Formal statement: If for a given customer's orders, the median value of
(fill_ts_utc − dispatch_ts_raw_as_utc_literal) ≈ +4 hours, then the dispatch
timestamps are in EDT (not UTC as labeled). The correct UTC normalization is:

    dispatch_ts_utc_normalized = dispatch_ts_raw + 4 hours

This rule applies to the FinClear Asia incident of 2026-03-27/28 for Customer
Gamma (CX-003), whose dispatch timestamps were labeled "UTC" but exhibited a
consistent −4h gap from fill_ts_utc values, consistent with EDT (UTC−4, applicable
in New York during summer time from 2026-03-08 onward).

**Confirmation:** The q2 analysis applying EDT correction (+4h) to CX-003 orders
was correct under this v2.0 rule. The total customer loss for CX-003, after applying
EDT normalization, is USD 162,440.00. This figure is confirmed and should not be
revised in the q4 updated loss summary.

**The grand total customer loss (USD 723,497.00) and the failed settlement count
(929 orders) are not changed by the arrival of this v2.0 SOP, since the q2
analysis already applied the correct EDT normalization.**

---

## 5. Matching Engine Clock Authority

The matching engine internal clock is the authoritative UTC source for all
settlement reconciliation purposes. If a customer ticket's stated UTC timestamp
differs from the matching engine's fill_ts_utc by more than 5 seconds, the
matching engine value takes precedence.

---

## 6. Config Validation Rule

The tz_offset_applied field in matching engine dispatch messages must always
equal "+00:00" for the production dispatch_adapter. Any deviation triggers an
immediate incident alert.

---

## 7. Reference Table

| Timezone | Label | UTC Offset | DST | Region |
|---|---|---|---|---|
| UTC | UTC | +00:00 | No | Universal |
| Singapore Standard Time | SGT | +08:00 | No | Singapore |
| Hong Kong Time | HKT | +08:00 | No | Hong Kong |
| Japan Standard Time | JST | +09:00 | No | Japan |
| Central European Time | CET | +01:00 | Yes (winter) | Europe |
| Central European Summer Time | CEST | +02:00 | Yes (summer) | Europe |
| Eastern Standard Time | EST | −05:00 | Yes (winter) | Eastern USA/Canada |
| Eastern Daylight Time | EDT | −04:00 | Yes (summer) | Eastern USA/Canada |

---


Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All customer-facing timestamps in incident communications must be expressed in UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All customer-facing timestamps in incident communications must be expressed in UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All customer-facing timestamps in incident communications must be expressed in UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All customer-facing timestamps in incident communications must be expressed in UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All customer-facing timestamps in incident communications must be expressed in UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All customer-facing timestamps in incident communications must be expressed in UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Config rollback procedures must be completed within the same UTC business day as the incident.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Config rollback procedures must be completed within the same UTC business day as the incident.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All customer-facing timestamps in incident communications must be expressed in UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All customer-facing timestamps in incident communications must be expressed in UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Config rollback procedures must be completed within the same UTC business day as the incident.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
