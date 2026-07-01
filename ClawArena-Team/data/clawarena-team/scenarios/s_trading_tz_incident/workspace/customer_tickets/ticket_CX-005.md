# Customer Incident Ticket — CX-005 (Customer Epsilon)
**Ticket ID:** CUST-INC-2026-0005
**Filed:** 2026-03-28T12:30:00+02:00 (CEST)
**Filed by:** Head of Post-Trade Operations, Epsilon Fund Management (Amsterdam)
**Contact:** posttrade@epsilonfund.nl
**Urgency:** High

---

## Incident Description

Epsilon Fund Management (Amsterdam) files this formal incident report regarding
178 failed settlement instructions on 2026-03-27 and 2026-03-28.

**All times in this ticket are in CET/CEST (Central European Time / Summer Time).
On 2026-03-27, European clocks moved forward at 02:00 CET to 03:00 CEST (UTC+2).
Times before 02:00 local on 2026-03-27 are CET (UTC+1); times from 03:00 onward
are CEST (UTC+2). We have indicated the relevant timezone for each timestamp.**

---

## Timeline (CET/CEST)

| Event | Local Timestamp | TZ | UTC Equivalent |
|---|---|---|---|
| First affected order dispatched | 2026-03-27T19:25:00+02:00 | CEST | 2026-03-27T17:25:00Z |
| ClearRoute EU cut-off window (2026-03-27) | 2026-03-27T17:00:00+01:00 | CET | 2026-03-27T16:00:00Z |
| DST spring-forward | 2026-03-27T02:00:00+01:00 → 03:00 CEST | — | 2026-03-27T01:00:00Z |
| Epsilon notified of failure | 2026-03-28T11:15:00+02:00 | CEST | 2026-03-28T09:15:00Z |

---

## DST Note

We are aware that the DST transition on 2026-03-27 complicates timezone analysis.
For the avoidance of doubt: ClearRoute EU's cut-off window on 2026-03-27 was at
17:00 CET (not CEST), which equals 16:00 UTC. However, ClearRoute EU's records
indicate that our settlement instructions were timestamped as arriving after this
cut-off. We believe the issue originates on the dispatch side, not with ClearRoute
EU's DST handling, based on our independent analysis of the dispatch log timestamps.

---

## Affected Orders

Total failed orders: **178**
Total estimated loss: **USD 143,680.25**

Securities: SGEX (38), HKFIN (35), JPNBK (28), AUHLD (25), TWSMC (22),
KRSEC (18), CNTECH (12).

---

## Requested Actions

1. Provide the exact UTC timestamp of the root-cause event in the matching engine log.
2. Confirm that Epsilon's CET/CEST timestamps have been correctly converted to UTC.
3. Resubmit all 178 failed settlement instructions.
4. Provide the preliminary regulatory report filing reference.


without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
