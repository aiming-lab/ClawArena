# Customer Incident Ticket — CX-001 (Customer Alpha)
**Ticket ID:** CUST-INC-2026-0001
**Filed:** 2026-03-28T05:30:00+08:00 (HKT)
**Filed by:** Trading Operations Team, Customer Alpha Capital Management
**Contact:** ops-trading@customer-alpha.hk
**Urgency:** High

---

## Incident Description

Customer Alpha Capital Management is filing this urgent incident ticket to report
the failure of 312 equity orders to achieve settlement under the expected T+2
settlement cycle. These orders were executed via FinClear Asia on the afternoon of
2026-03-27 Hong Kong Time (HKT) and were expected to settle on 2026-03-29.

**All timestamps in this ticket are expressed in HKT (UTC+8 / Hong Kong Time).**
To convert to UTC, subtract 8 hours from all stated times.

---

## Timeline of Events (HKT)

| Event | HKT Timestamp | UTC Equivalent |
|---|---|---|
| First affected order matched | 2026-03-28T01:25:00+08:00 (HKT) | 2026-03-27T17:25:00Z |
| Last affected order matched | 2026-03-28T15:10:00+08:00 (HKT) | 2026-03-28T07:10:00Z |
| FinClear Asia dispatch window for affected orders | 2026-03-28T01:23:00+08:00 onward | 2026-03-27T17:23:00Z onward |
| Customer Alpha notified of settlement failure | 2026-03-28T18:45:00+08:00 (HKT) | 2026-03-28T10:45:00Z |

---

## Affected Securities and Order Counts

| Security | Symbol | Orders Affected | Approximate Loss (USD) |
|---|---|---|---|
| Singapore Exchange Equity Fund | SGEX | 78 | 62,400 |
| Hong Kong Financial Index | HKFIN | 91 | 71,200 |
| Japan Bank ETF | JPNBK | 43 | 34,750 |
| Australia Holdings | AUHLD | 38 | 30,100 |
| Taiwan Semiconductor | TWSMC | 29 | 23,600 |
| Korea Securities | KRSEC | 18 | 14,400 |
| China Technology | CNTECH | 15 | 11,400 |
| **Total** | — | **312** | **247,850** |

---

## Customer Statement

Customer Alpha's trading desk noticed the anomaly when settlement confirmations
failed to arrive by 09:00 HKT (01:00 UTC) on 2026-03-29. The treasury operations
team queried the ClearRoute EU portal and found all 312 orders listed as
TIMESTAMP_AFTER_CUTOFF rejected.

Customer Alpha does not use the UTC label for its internal timestamps; all internal
systems run on Hong Kong Time (HKT, UTC+8). The UTC equivalents provided in this
ticket were computed by Customer Alpha's operations team by subtracting 8 hours
from all HKT values. We request FinClear Asia to verify these conversions against
your matching engine records.

We estimate total loss from delayed settlement at USD 247,850.40 based on
mark-to-market adverse price movement between intended settlement date and the
next available settlement date.

---

## Requested Actions

1. Confirm root cause of the settlement failure and provide an official incident report.
2. Resubmit all 312 failed orders for settlement at the earliest available date.
3. Provide compensation calculation for adverse price movement during the settlement delay.
4. File a preliminary regulatory report with the competent authority as required.

---

## Additional Context

Customer Alpha has an active ISDA Master Agreement and a Prime Brokerage Agreement
with FinClear Asia dated 2024-09-01. All settlement obligations under those
agreements were met on our side; the failure originated with the dispatch adapter
timezone misconfiguration on the FinClear Asia side.


subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
