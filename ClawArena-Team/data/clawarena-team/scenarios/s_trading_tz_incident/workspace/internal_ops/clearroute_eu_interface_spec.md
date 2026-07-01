# ClearRoute EU — Interface Specification for External Participants
## Version: 5.4
## Effective Date: 2026-01-01
## Issuing Authority: ClearRoute EU Technology and Operations

---

## Introduction

This interface specification defines the technical requirements for external
participants (including FinClear Asia Pte. Ltd.) connecting to ClearRoute EU's
settlement infrastructure. Compliance with all requirements in this document is
mandatory for maintaining participant status.

---

## Section 1: Connectivity Requirements

ClearRoute EU accepts settlement instructions via the ClearRoute Settlement
Protocol (CSP) over TLS 1.3. All participants must maintain connectivity to
both the primary endpoint (Frankfurt) and the disaster recovery endpoint (Amsterdam).

---

## Section 2: Message Format Requirements

### Section 2.1: General Principles

All messages must be formatted as structured key-value pairs per the CSP message
format specification. Field names are case-sensitive. Unknown fields will be
rejected.

### Section 2.2: Character Encoding

All messages must be encoded in UTF-8. Non-ASCII characters in free-text fields
must be escaped as Unicode code points.

---

## Section 3: Timestamp Requirements

### Section 3.1: Timestamp Format

All timestamp fields in ClearRoute EU settlement instructions must use the
ISO-8601 format: `YYYY-MM-DDTHH:MM:SSZ` where the trailing 'Z' denotes UTC.

Formats with explicit UTC offset notation (e.g., `+00:00`) are also accepted
but must express the UTC offset only. Timestamps with non-UTC offsets (e.g.,
`+08:00`, `+09:00`, `-04:00`) are NOT accepted and will cause the settlement
instruction to be rejected.

### Section 3.2.1: UTC Mandate (CRITICAL)

**All settlement instruction timestamps submitted to ClearRoute EU MUST be
expressed in Coordinated Universal Time (UTC). ClearRoute EU does not perform
timezone conversion on received timestamps. Any timestamp that appears to
represent a non-UTC time (e.g., by carrying an offset that is not +00:00) will
be treated as received, potentially causing incorrect settlement window assessment.**

This section (3.2.1) is the authoritative regulatory basis for the UTC requirement.
Participants found to submit non-UTC timestamps that result in settlement failures
are solely responsible for the consequences under the ClearRoute EU Rulebook.

**Practical implication:** If a participant's dispatch adapter is misconfigured to
apply a non-zero UTC offset (e.g., `tz_offset_applied="+08:00"`), the resulting
timestamps will be interpreted by ClearRoute EU as being 8 hours later than the
actual event time. This will cause orders dispatched after approximately 08:00 UTC
to appear to arrive after the 17:00 CET/CEST cut-off window.

### Section 3.2.2: DST Handling

ClearRoute EU's cut-off window is defined in local time (17:00 CET/CEST daily).
External participants are responsible for understanding when DST transitions affect
the UTC equivalent of the cut-off window:

| Period | Local Cut-Off | UTC Equivalent |
|---|---|---|
| Winter (CET, UTC+1) | 17:00 CET | 16:00 UTC |
| Summer (CEST, UTC+2) | 17:00 CEST | 15:00 UTC |

ClearRoute EU applies the cut-off in local time internally; received UTC timestamps
are converted to local time for cut-off assessment.

---

## Section 4: Settlement Window

ClearRoute EU operates a T+2 settlement cycle for equity instruments. The daily
settlement window closes at 17:00 CET/CEST. Instructions received after the cut-off
will be queued for the following business day's settlement window.

Instructions that arrive after cut-off due to participant-side timezone errors
(such as incorrect UTC offset in dispatch messages) are the sole responsibility
of the submitting participant. ClearRoute EU will not reprocess such instructions
without explicit request from the participant and confirmation from the competent authority.

---

## Section 5: Rejection Codes

| Code | Description | Likely Cause |
|---|---|---|
| TIMESTAMP_AFTER_CUTOFF | Submitted timestamp after daily cut-off | Late submission or incorrect UTC offset |
| INVALID_TIMESTAMP_FORMAT | Timestamp not in ISO-8601 UTC format | Format error in dispatch adapter |
| UNKNOWN_ORDER_ID | Order ID not found in ClearRoute EU records | Reference mismatch |
| DUPLICATE_INSTRUCTION | Settlement instruction already received | Retry without deduplication |

---

## Section 6: Participant Responsibilities

Participants are solely responsible for:
1. Ensuring dispatch adapter configuration applies UTC (tz_offset_applied="+00:00").
2. Monitoring dispatch message timestamps for correctness before submission.
3. Implementing automated assertion checks on timezone configuration.
4. Notifying ClearRoute EU of any known timestamp errors within 2 hours of detection.
5. Reporting settlement failure incidents to the competent authority per applicable rules.

---

provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
