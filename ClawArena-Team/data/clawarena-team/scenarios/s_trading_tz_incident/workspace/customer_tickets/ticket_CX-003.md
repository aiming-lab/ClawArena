# Customer Incident Ticket — CX-003 (Customer Gamma)
**Ticket ID:** CUST-INC-2026-0003
**Filed:** 2026-03-28T09:05:00Z
**Filed by:** Head of Settlement Operations, Gamma Investments LLC (New York)
**Contact:** settlement-ops@gammainv.com
**Urgency:** High

---

## Incident Description

Gamma Investments LLC hereby files a formal incident report concerning the failure
of 203 equity settlement instructions on 2026-03-27 and 2026-03-28. We operate
from our New York office.

**All timestamps in this ticket are UTC.**

We expect FinClear Asia to process this report using the UTC timestamps as
provided. No timezone conversion is necessary on the recipient's side.

---

## Timeline of Events (stated as UTC)

| Event | Stated UTC Timestamp | Notes |
|---|---|---|
| First affected order matched | 2026-03-27T13:25:00Z | Gamma's first post-incident order |
| Order batch submitted to FinClear Asia platform | 2026-03-27T13:28:00Z | Batch of 203 orders submitted |
| Last affected order matched | 2026-03-28T05:10:00Z | Final order in the batch |
| Gamma notified of settlement failure | 2026-03-28T09:05:00Z | Notification received from FinClear Asia |

---

## Stated Sequence of Events

At 13:25 UTC on 2026-03-27, Gamma's trading desk submitted a batch of 203 equity
orders to the FinClear Asia platform. All orders were confirmed as received at
approximately 13:28 UTC. The orders covered seven securities: SGEX, HKFIN, JPNBK,
AUHLD, TWSMC, KRSEC, and CNTECH.

At 09:05 UTC on 2026-03-28, Gamma received a settlement failure notification
indicating all 203 orders were rejected with the code TIMESTAMP_AFTER_CUTOFF.

We have verified internally that our platform clock runs on UTC and that our order
timestamps are accurate to within one second of UTC. We therefore cannot account
for any timestamp offset in the dispatch messages. We expect FinClear Asia to
investigate and confirm the timestamps we have provided are consistent with your
records. We assert that all timestamps in this ticket are UTC with no offset applied.

---

## Affected Orders Summary

Total failed settlement orders: **203**
Approximate total loss (mark-to-market): **USD 162,440.00**

| Symbol | Orders | Approx Loss (USD) |
|---|---|---|
| SGEX | 41 | 33,200 |
| HKFIN | 38 | 30,750 |
| JPNBK | 32 | 25,900 |
| AUHLD | 28 | 22,650 |
| TWSMC | 27 | 21,840 |
| KRSEC | 22 | 17,800 |
| CNTECH | 15 | 10,300 |
| **Total** | **203** | **162,440** |

---

## Requested Actions

1. Confirm that the UTC timestamps provided in this ticket match your matching engine records.
2. Identify and disclose the root cause of the settlement failure.
3. Resubmit all 203 failed orders for settlement without delay.
4. Provide regulatory filing reference number once the preliminary report is filed.

---

## Additional Context

Gamma Investments LLC is an institutional investor operating under SEC registration.
Our trading systems are synchronized to NTP servers and display times in UTC only.
We have no local timezone configured in our order management system; all timestamps
are expressed in UTC as a matter of firm policy.

Note for FinClear Asia operations: please do not convert our timestamps — they are
already in UTC. Any conversion would introduce errors.


in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
in compliance with all applicable post-trade regulatory requirements
