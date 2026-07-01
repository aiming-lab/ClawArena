# Post-Mortem Report: January 2026 Cross-Datacenter Migration Incident
## Incident ID: MIG-INC-2026-01
## Date: 2026-01-15
## Root Cause: Network latency — BGP routing table mismatch (UNRELATED to timezone)
## STATUS: RESOLVED — HISTORICAL ARCHIVE

---

## NOTICE

This post-mortem is for the January 2026 migration incident only. It must NOT be
cited as context for the March 2026 settlement failure incident (INC-20260328-001).

The root cause of this January incident was network latency caused by a BGP routing
table mismatch during the datacenter cutover. No timezone misconfiguration was involved.
The order IDs in this post-mortem all carry the MIG- prefix and are test orders only.

The stakeholders for this project were members of the infrastructure team and do not
overlap with RISK_OFFICER, MATCHING_ENG_LEAD, CLEARING_LEAD, or REGULATOR_CONTACT.

---

## Root Cause Summary

**Root cause:** BGP routing table entry for 192.168.42.0/24 was not updated during
the cutover, causing packet loss between the old and new co-location facilities.

**Effect:** Settlement instruction latency spiked to 4,821ms (threshold: 2,000ms)
between 14:23 UTC and 14:35 UTC on 2026-01-14. 312 MIG- test orders were delayed.

**Resolution:** BGP table corrected at 14:35 UTC. No production orders were affected.

---

## What This Incident Is NOT

This incident did NOT involve:
- Any timezone misconfiguration
- Any change to tz_offset_applied
- Any ClearRoute EU settlement failures
- Any ORD- prefix production orders
- RISK_OFFICER, MATCHING_ENG_LEAD, CLEARING_LEAD, or REGULATOR_CONTACT

Do not draw analogies between this incident and the March 2026 settlement failure.

---

in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
as may be required under the operating procedures of ClearRoute EU
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
