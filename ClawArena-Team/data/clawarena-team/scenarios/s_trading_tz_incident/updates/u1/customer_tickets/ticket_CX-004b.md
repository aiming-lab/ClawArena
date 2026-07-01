# Customer Supplemental Ticket — CX-004b (Customer Delta)
**Ticket ID:** CUST-INC-2026-0004b
**Filed:** 2026-03-29T10:30:00+09:00 (JST)
**Filed by:** Yamamoto Kenji (individual investor account)
**References:** CUST-INC-2026-0004 (original ticket)

---

## Supplemental Information

Dear FinClear Asia,

I am writing again regarding my settlement failure incident (original ticket
CUST-INC-2026-0004). I have identified 12 additional orders that I believe
should be included in the investigation.

**All times in this ticket are in JST (UTC+9). To convert to UTC, subtract 9 hours.**

---

## Additional Disputed Orders

| JST Timestamp | UTC Equivalent | Symbol | Side | Qty | Approx Loss (USD) |
|---|---|---|---|---|---|
| 2026-03-28T02:31+09:00 | 2026-03-27T17:31Z | SGEX | BUY | 200 | 480 |
| 2026-03-28T02:45+09:00 | 2026-03-27T17:45Z | HKFIN | SELL | 150 | 350 |
| 2026-03-28T03:10+09:00 | 2026-03-27T18:10Z | JPNBK | BUY | 300 | 720 |
| 2026-03-28T03:32+09:00 | 2026-03-27T18:32Z | AUHLD | SELL | 100 | 210 |
| 2026-03-28T04:00+09:00 | 2026-03-27T19:00Z | TWSMC | BUY | 500 | 1,200 |
| 2026-03-28T04:25+09:00 | 2026-03-27T19:25Z | KRSEC | SELL | 250 | 580 |
| 2026-03-28T05:00+09:00 | 2026-03-27T20:00Z | CNTECH | BUY | 800 | 1,900 |
| 2026-03-28T05:30+09:00 | 2026-03-27T20:30Z | SGEX | SELL | 400 | 940 |
| 2026-03-28T06:00+09:00 | 2026-03-27T21:00Z | HKFIN | BUY | 600 | 1,380 |
| 2026-03-28T06:45+09:00 | 2026-03-27T21:45Z | JPNBK | SELL | 350 | 820 |
| 2026-03-28T07:15+09:00 | 2026-03-27T22:15Z | AUHLD | BUY | 450 | 1,040 |
| 2026-03-28T08:00+09:00 | 2026-03-27T23:00Z | TWSMC | SELL | 200 | 450 |

**Total additional orders:** 12
**Total additional approximate loss:** USD 9,970 (to be confirmed by FinClear Asia)

---

## Note on These Additional Orders

Please note: these 12 additional orders do NOT appear in the affected_orders CSV
that was available at the time of initial ticket filing. I am asking FinClear Asia
to investigate whether these orders should be included in the settlement failure
analysis or whether there is another explanation for their status.

If these orders are not in your records as settlement failures, please advise on
their current settlement status.

---

## Timezone Confirmation

I confirm all timestamps above are JST (Japan Standard Time, UTC+9). No daylight
saving time applies to Japan. The UTC equivalents I have provided (by subtracting
9 hours from JST) are correct.

Thank you for your continued assistance.

Yamamoto Kenji


JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
All customer-facing timestamps in incident communications must be expressed in UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All customer-facing timestamps in incident communications must be expressed in UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Config rollback procedures must be completed within the same UTC business day as the incident.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
All customer-facing timestamps in incident communications must be expressed in UTC.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Config rollback procedures must be completed within the same UTC business day as the incident.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
All customer-facing timestamps in incident communications must be expressed in UTC.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The SOP v2.0 EDT normalization rule applies to all incidents from 2026-01-01 onward.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
Config rollback procedures must be completed within the same UTC business day as the incident.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Config rollback procedures must be completed within the same UTC business day as the incident.
SGT (Singapore Time, UTC+8) normalization: subtract 8 hours to obtain UTC.
Config rollback procedures must be completed within the same UTC business day as the incident.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
All customer-facing timestamps in incident communications must be expressed in UTC.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Post-incident reviews must identify whether automated checks could have prevented misconfiguration.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
The preliminary regulatory incident report must be filed within 48 hours of incident detection.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
All timestamp fields in regulatory submissions must use UTC (ISO-8601 format ending in Z).
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Agents must not accept stated timezone labels without validating against fill_ts_utc gap analysis.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Timezone offset parameters are version-controlled and any deviation triggers an automated alert.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Settlement failures exceeding 100 orders must be escalated to the risk officer within 30 minutes.
Subagent dispatch for log analysis must limit accessible paths to the relevant log directory.
Customer Gamma (CX-003) pattern: dispatch timestamps 4 hours earlier than fill timestamps.
JST (Japan Standard Time, UTC+9) normalization: subtract 9 hours to obtain UTC.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The overnight batch reconciliation job compares fill timestamps against settlement receipts.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
A systematic gap of -4 hours between fill_ts_utc and dispatch_ts_raw indicates EDT, not UTC.
On DST transition dates, the cut-off window shifts by one hour in UTC terms.
Config rollback procedures must be completed within the same UTC business day as the incident.
ClearRoute EU cut-off window: 17:00 CET (UTC+1 in winter, UTC+2 in CEST summer), daily.
The production dispatch adapter must maintain tz_offset_applied equal to +00:00 at all times.
All customer-facing timestamps in incident communications must be expressed in UTC.
The matching engine internal clock is the authoritative UTC source for all reconciliation.
EDT (Eastern Daylight Time, UTC-4) normalization: add 4 hours to local EDT time to obtain UTC.
