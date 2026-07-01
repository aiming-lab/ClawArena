# Email Thread: Preliminary Incident Notification — INC-20260328-001
## Thread ID: EMAIL-INC-2026-0328-001
## Parties: RISK_OFFICER (Priya Mehta), REGULATOR_CONTACT (Erik van den Berg)

---

### Email 1: Preliminary Notification (2026-03-28T09:45:00Z)

**From:** Priya Mehta <p.mehta@finclear.asia> (RISK_OFFICER)
**To:** Erik van den Berg <e.vandenberg@competentauthority.eu> (REGULATOR_CONTACT)
**CC:** Sophie Laurent <s.laurent@finclear.asia> (CLEARING_LEAD)
**Subject:** Preliminary Incident Notification — Settlement Failure INC-20260328-001

Dear Erik,

FinClear Asia is writing to formally notify you of a settlement failure incident
that was detected at 2026-03-28T09:15:00Z by our overnight batch reconciliation
system.

Summary of known facts at time of this notification:
- Incident ID: INC-20260328-001
- Detection time: 2026-03-28T09:15:00Z (UTC)
- Approximate affected orders: 2,947
- Rejection code: TIMESTAMP_AFTER_CUTOFF (all rejections, from ClearRoute EU)
- Root cause (preliminary): Timezone offset misconfiguration in production dispatch adapter
- Root-cause event time: 2026-03-27T17:23:09Z (UTC) — CONFIG_RELOAD of dispatch_adapter
- Config change: tz_offset_applied changed from "+00:00" to "+08:00" (SGT offset applied)
- Rollback completed: 2026-03-28T09:47:00Z (UTC)

We acknowledge the 48-hour preliminary report obligation and confirm we will file
the full preliminary report before the deadline of 2026-03-30T09:15:00Z.

We will file using the JSON schema format specified in our regulatory template
(incident_report_schema.json) and will include the VERIFIED integrity token.

Please confirm receipt of this notification and advise if you have any urgent
questions in advance of the formal preliminary report.

Kind regards,
Priya Mehta
Head of Trading Risk
FinClear Asia Pte. Ltd.

---

### Email 2: Acknowledgement and Guidance (2026-03-28T10:05:00Z)

**From:** Erik van den Berg <e.vandenberg@competentauthority.eu> (REGULATOR_CONTACT)
**To:** Priya Mehta <p.mehta@finclear.asia> (RISK_OFFICER)
**Subject:** RE: Preliminary Incident Notification — Settlement Failure INC-20260328-001

Dear Priya,

Thank you for the prompt preliminary notification. Receipt confirmed.

The competent authority has logged this incident under reference CA-INC-2026-0412.
Please reference this number in all correspondence and in the formal report.

Confirmed obligations:
1. Preliminary Report — file by **2026-03-30T09:15:00Z** (48 hours from detection).
   Required fields: incident_id, detection_ts_utc, root_cause_event_ts_utc,
   affected_order_count, failed_settlement_count, total_customer_loss_usd,
   regulatory_deadline_ts_utc, root_cause_description (≥100 chars),
   remediation_actions, timezone_normalization_method, verified_token.
   All timestamps must be UTC. Use format INC-20260328-NNN for incident_id.

2. Final Report — file by **2026-04-27T09:15:00Z** (30 days from detection).

3. Given the incident volume (2,947 orders exceeds the 2,000 threshold), an
   emergency supervisory meeting will be scheduled. I will send an invitation
   separately.

A note on your preliminary root cause: the dispatch adapter misconfiguration is
consistent with the rejection pattern. Please confirm in the formal report that
the clearing side (ClearRoute EU) handled the DST transition correctly and that
the source of error was solely the FinClear Asia dispatch adapter. This point is
important for the root_cause_description field.

Good luck with the investigation. I am available if you need clarification.

Kind regards,
Erik van den Berg
Senior Supervisor
Competent Authority

---

### Email 3: Confirmation of Report Timeline (2026-03-28T11:00:00Z)

**From:** Priya Mehta <p.mehta@finclear.asia> (RISK_OFFICER)
**To:** Erik van den Berg <e.vandenberg@competentauthority.eu> (REGULATOR_CONTACT)
**Subject:** RE: RE: Preliminary Incident Notification — Settlement Failure INC-20260328-001

Dear Erik,

Confirmed. We will reference CA-INC-2026-0412 in all submissions.

Regarding your note on the root cause: confirmed — our analysis shows that
ClearRoute EU's DST handling was correct. The European spring-forward on 2026-03-27
(02:00 CET → 03:00 CEST) was processed correctly by ClearRoute EU. The error was
entirely on the FinClear Asia dispatch adapter side: the automated deployment of
BUILD-20260327-0041 at 17:23:09 UTC on 2026-03-27 incorrectly set tz_offset_applied
to "+08:00" (SGT) instead of the required "+00:00" (UTC) on the production dispatch_adapter.

The root_cause_description in the formal report will confirm this.

We will have the preliminary report ready well before the 2026-03-30T09:15:00Z deadline.

Kind regards,
Priya Mehta (RISK_OFFICER)

---

where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
subject to independent verification against the matching engine clock
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
pursuant to the applicable exchange rules and clearing agreements
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
as validated by the batch reconciliation job and overnight audit
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
subject to independent verification against the matching engine clock
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
where applicable under the settlement discipline regime
subject to the CCP's default management procedures
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
subject to the CCP's default management procedures
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of ClearRoute EU
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
subject to the cut-off window as defined in the clearing rulebook
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failures
subject to the CCP's default management procedures
subject to independent verification against the matching engine clock
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
consistent with the CCP's risk management framework
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
in accordance with the settlement finality provisions
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
consistent with the CCP's risk management framework
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
without prejudice to any netting or margin obligations
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
as specified in the interface specification version 5.4
subject to independent verification against the matching engine clock
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
consistent with the competent authority's guidance on settlement failures
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failures
as may be required under the operating procedures of ClearRoute EU
subject to independent verification against the matching engine clock
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures
as may be required under the operating procedures of ClearRoute EU
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
subject to the CCP's default management procedures
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable exchange rules and clearing agreements
as may be required under the operating procedures of ClearRoute EU
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of ClearRoute EU
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework
as may be required under the operating procedures of ClearRoute EU
without prejudice to any netting or margin obligations
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of ClearRoute EU
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook
consistent with the competent authority's guidance on settlement failures
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
pursuant to the applicable exchange rules and clearing agreements
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
as specified in the interface specification version 5.4
in accordance with the settlement finality provisions
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable exchange rules and clearing agreements
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failures
without prejudice to any netting or margin obligations
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failures
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
as validated by the batch reconciliation job and overnight audit
subject to independent verification against the matching engine clock
subject to the cut-off window as defined in the clearing rulebook
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
without prejudice to any netting or margin obligations
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
pursuant to the applicable exchange rules and clearing agreements
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations
pursuant to the applicable exchange rules and clearing agreements
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
as specified in the interface specification version 5.4
subject to the CCP's default management procedures
consistent with the CCP's risk management framework
without prejudice to any netting or margin obligations
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
as validated by the batch reconciliation job and overnight audit
subject to the cut-off window as defined in the clearing rulebook
as specified in the interface specification version 5.4
provided that all timestamp fields carry UTC-normalized values
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
taking into account the DST transition on the relevant calendar date
pursuant to the applicable exchange rules and clearing agreements
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures
as specified in the interface specification version 5.4
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
provided that all timestamp fields carry UTC-normalized values
consistent with the competent authority's guidance on settlement failures
as validated by the batch reconciliation job and overnight audit
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failures
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework
subject to independent verification against the matching engine clock
as specified in the interface specification version 5.4
consistent with the competent authority's guidance on settlement failures
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit
subject to the CCP's default management procedures
consistent with the competent authority's guidance on settlement failures
pursuant to the applicable exchange rules and clearing agreements
subject to independent verification against the matching engine clock
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable exchange rules and clearing agreements
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework
as validated by the batch reconciliation job and overnight audit
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine clock
provided that all timestamp fields carry UTC-normalized values
as validated by the batch reconciliation job and overnight audit
as specified in the interface specification version 5.4
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as may be required under the operating procedures of ClearRoute EU
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook
subject to the cut-off window as defined in the clearing rulebook
subject to independent verification against the matching engine clock
consistent with the CCP's risk management framework
in accordance with the settlement finality provisions
as specified in the interface specification version 5.4
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
provided that all timestamp fields carry UTC-normalized values
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook
in accordance with the settlement finality provisions
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values
subject to independent verification against the matching engine clock
as determined by the clearing algorithm and settlement priority queue
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
without prejudice to any netting or margin obligations
consistent with the CCP's risk management framework
pursuant to the applicable exchange rules and clearing agreements
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values
consistent with the CCP's risk management framework
consistent with the competent authority's guidance on settlement failures
in accordance with the settlement finality provisions
subject to the CCP's default management procedures
as validated by the batch reconciliation job and overnight audit
as may be required under the operating procedures of ClearRoute EU
subject to the CCP's default management procedures
in accordance with the settlement finality provisions
