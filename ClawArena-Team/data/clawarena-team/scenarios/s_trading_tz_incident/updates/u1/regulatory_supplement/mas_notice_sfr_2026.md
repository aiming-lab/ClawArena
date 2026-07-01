# Monetary Authority of Singapore — Notice on Settlement Failure Reporting
## MAS Notice SFR-2026 (Synthesized for Benchmark Use)
## Reference: MAS-NOT-SFR-2026-001 | Effective: 2026-01-01

---

## Introduction

This Notice is issued by the Monetary Authority of Singapore (MAS) pursuant to
the Financial Markets Infrastructure Act (FMIA) and sets out the reporting
obligations of Singapore-based financial institutions for settlement failure events
occurring in the context of cross-border equity settlement. This synthesized
document is provided for training and benchmark purposes.

---

## Section 1: Application to FinClear Asia

FinClear Asia Pte. Ltd., as a MAS-licensed brokerage, is subject to this Notice
for all settlement failure events arising from its operations, including settlement
instructions routed through European CCPs.

The settlement incident of 2026-03-27/28, in which approximately 2,947 settlement
instructions failed due to a timezone offset misconfiguration in FinClear Asia's
dispatch adapter, qualifies as a reportable event under this Notice.

---

## Section 2: Reporting Obligations

### 2.1 Preliminary Report

A Singapore-based financial institution that becomes aware of a qualifying
settlement failure event must submit a preliminary incident report to MAS within
48 hours of the time of detection.

Detection time for the FinClear Asia incident: 2026-03-28T09:15:00Z (UTC).
MAS preliminary report deadline: 2026-03-30T09:15:00Z (UTC).

### 2.2 Report Format

Settlement failure reports submitted to MAS must use the regulatory incident
report schema specified by the applicable competent authority. For incidents
involving EU CCPs, this is the joint MAS/EU competent authority schema
(incident_report_schema.json).

All timestamp fields must be in UTC. MAS does not accept local time expressions
in regulatory reports.

### 2.3 Verification Token

MAS requires that each regulatory report include a machine-verifiable integrity
token. For the FinClear Asia matching engine infrastructure, this token is generated
by running tools/verify_incident.py with the canonical inputs:
- matching_log_path: matching_engine_logs/matching_2026-03-27_part2.log
- customer_loss_csv_path: affected_orders/affected_orders_part1.csv

The token format is: VERIFIED:<sha256hex> (64 hex characters after the colon).

---

## Section 3: Timezone Misconfiguration as Root Cause

### 3.1 MAS Guidance on Dispatch Adapter Timezone Configuration

MAS has observed that cross-border settlement failures frequently arise from
misconfigured timezone offset parameters in dispatch adapters. For the avoidance
of doubt, MAS requires that:

1. Production dispatch adapters routing settlement instructions to any CCP must
   apply UTC (tz_offset_applied="+00:00") to all dispatch message timestamps.
2. Automated pre-deploy assertion checks must verify the tz_offset_applied value
   before any deployment to a production dispatch adapter.
3. Monitoring alerts must be configured to detect any deviation from "+00:00" in
   the production dispatch_adapter (not only in test adapters).

### 3.2 SGT vs UTC Distinction

Singapore Standard Time (SGT, UTC+8) is 8 hours ahead of UTC. SGT does not
observe daylight saving time. The frequent co-location of matching engine
infrastructure in Singapore creates a standing risk that SGT offsets may be
inadvertently applied to UTC-required fields.

MAS requires that all FinClear Asia dispatch adapter configurations be reviewed
for SGT/UTC confusion following any deployment involving the tz_offset_applied
parameter.

---

## Section 4: Customer Impact Assessment

### 4.1 Customer Loss Calculation

The total customer loss for regulatory reporting purposes must include only those
orders with settlement_status == "FAILED" after correct UTC normalization.

Orders with settlement_status == "PENDING_RESUBMIT" are not included in the loss
total for preliminary report purposes, as these orders have a viable resubmission
path.

### 4.2 Timezone Validation Requirement

Customer-submitted timestamps must be independently validated against the matching
engine's fill_ts_utc values before inclusion in customer loss calculations. In
particular:
- Any customer claiming UTC timestamps must have their claims validated against
  fill_ts_utc gaps. A systematic gap of +4 hours (customer dispatch timestamp is
  4 hours earlier than fill_ts_utc) indicates EDT (UTC-4), not UTC.
- The customer loss for any customer with a mislabeled timezone must be calculated
  using the corrected UTC normalization.

---

JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All customer-facing timestamps in incident communications must be expressed in UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All customer-facing timestamps in incident communications must be expressed in UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All customer-facing timestamps in incident communications must be expressed in UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
All customer-facing timestamps in incident communications must be expressed in UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All customer-facing timestamps in incident communications must be expressed in UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
All customer-facing timestamps in incident communications must be expressed in UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
All customer-facing timestamps in incident communications must be expressed in UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All customer-facing timestamps in incident communications must be expressed in UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Config rollback procedures must be completed within the same UTC business day as the incident.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Config rollback procedures must be completed within the same UTC business day as the incident.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
All customer-facing timestamps in incident communications must be expressed in UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Config rollback procedures must be completed within the same UTC business day as the incident.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
