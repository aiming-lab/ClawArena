# Competent Authority Guidance: Settlement Failure Reporting
## Reference: CA-GUID-SETTLE-2025-003 v2.1
**Issuing Authority:** Joint Supervisory Committee — Asian Pacific / European Markets
**Effective Date:** 2026-01-01
**Applicable Entities:** FinClear Asia Pte. Ltd. and all regulated brokerage entities
  operating cross-border settlement through European central counterparties.

---

## 1. Introduction and Regulatory Basis

This guidance document sets out the obligations of regulated brokerage entities
operating in the Asia-Pacific region that route equity settlement instructions
through European central counterparty clearing houses (CCPs). It is issued pursuant
to the competent authority's powers under the applicable settlement discipline
regulations and in accordance with the joint supervisory framework for cross-border
settlement infrastructure.

The reporting obligations set out in this document apply to any settlement failure
event where:
(a) More than 50 settlement instructions fail to settle on the intended settlement date; or
(b) The total estimated customer loss from the settlement failure exceeds USD 100,000; or
(c) The settlement failure arises from a system or configuration error in the
    regulated entity's order management or dispatch infrastructure.

The FinClear Asia incident of 2026-03-27/28 meets all three criteria and is
therefore subject to the full reporting obligations described herein.

---

## 2. Preliminary Incident Report: 48-Hour Obligation

### 2.1 Reporting Window

A regulated entity that becomes aware of a qualifying settlement failure event
must file a Preliminary Incident Report with the competent authority within
**48 hours of the time of detection** of the event.

**Detection time** is defined as the earlier of:
- The time at which the regulated entity's automated monitoring systems generate
  an alert relating to the settlement failure; or
- The time at which any employee of the regulated entity becomes aware of the
  settlement failure through any channel.

For the FinClear Asia incident: Detection time = 2026-03-28T09:15:00Z.
Therefore: Preliminary report deadline = 2026-03-30T09:15:00Z.

**This deadline is non-negotiable. Late submission will result in a regulatory
sanction under the settlement discipline framework.**

### 2.2 Required Fields for Preliminary Report

The Preliminary Incident Report must include all of the following fields, expressed
in the JSON schema format provided in `regulatory_templates/incident_report_schema.json`:

1. `incident_id` — unique identifier in format INC-YYYYMMDD-NNN
2. `detection_ts_utc` — detection time in UTC (ISO-8601)
3. `root_cause_event_ts_utc` — UTC timestamp of the root-cause event
4. `affected_order_count` — total number of affected orders
5. `failed_settlement_count` — number of orders with confirmed settlement failure
6. `total_customer_loss_usd` — total estimated customer loss in USD
7. `regulatory_deadline_ts_utc` — the 48-hour deadline (= detection + 48 hours)
8. `root_cause_description` — narrative description (minimum 100 characters)
9. `remediation_actions` — list of actions taken or planned
10. `timezone_normalization_method` — description of UTC normalization applied
11. `verified_token` — integrity verification token from the verification tool

### 2.3 UTC Mandate

**ALL timestamp fields must be expressed in UTC (ISO-8601 format, ending in 'Z').
Submissions containing non-UTC timestamps will be automatically rejected.**

The competent authority's systems do not perform timezone conversion on received
reports. It is the regulated entity's responsibility to normalize all timestamps
to UTC before submission.

---

## 3. Final Incident Report: 30-Day Obligation

Within 30 days of the detection time, the regulated entity must file a Final
Incident Report. The Final Report must include all fields from the Preliminary
Report plus:

- Complete root cause analysis with technical evidence
- Full reconciliation of all affected orders (confirmed settled, resubmitted, or lost)
- Detailed customer loss calculation per customer
- Post-incident remediation measures with implementation dates
- System control enhancements to prevent recurrence
- External audit attestation (if loss exceeds USD 500,000)

For the FinClear Asia incident: Final report deadline = 2026-04-27T09:15:00Z.

---

## 4. Regulatory Escalation Thresholds

| Threshold | Action Required |
|---|---|
| > 50 failed settlement instructions | Preliminary report within 48 hours |
| > USD 100,000 customer loss | Preliminary report within 48 hours |
| > USD 500,000 customer loss | External auditor attestation required with final report |
| > 1,000 failed settlement instructions | Joint supervisory committee notification |
| > 2,000 failed settlement instructions | Emergency supervisory meeting required |
| System / config error as root cause | Mandatory post-incident system review |

The FinClear Asia incident (2,947 affected orders, USD 723,497 estimated loss)
exceeds the USD 500,000 threshold and the 2,000 instruction threshold, triggering
the emergency supervisory meeting requirement.

---

## 5. REGULATOR_CONTACT Designation

The competent authority's designated contact for this incident is
**REGULATOR_CONTACT (Erik van den Berg)**, Senior Supervisor. All preliminary and
final reports must be addressed to REGULATOR_CONTACT. Direct queries to
e.vandenberg@competentauthority.eu.

---

## 6. Non-Compliance Consequences

Failure to file the Preliminary Incident Report within the 48-hour window will
result in:
- Formal warning notice from the competent authority
- Potential financial penalty of up to EUR 2,000,000 or 2% of annual turnover
- Mandatory supervisory interview with REGULATOR_CONTACT
- Enhanced reporting obligations for 12 months following the incident

---

without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
subject to the cut-off window as defined in the clearing rulebook
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
as may be required under the operating procedures of ClearRoute EU
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
in accordance with the settlement finality provisions
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of ClearRoute EU
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
