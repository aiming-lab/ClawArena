# Customer Supplemental Ticket — CX-005b (Customer Epsilon)
**Ticket ID:** CUST-INC-2026-0005b
**Filed:** 2026-03-29T11:00:00+02:00 (CEST)
**Filed by:** Head of Post-Trade Operations, Epsilon Fund Management (Amsterdam)
**References:** CUST-INC-2026-0005 (original ticket)

---

## Supplemental Filing: DST Context Clarification and Updated Loss Estimate

Epsilon Fund Management submits this supplemental filing to clarify the DST
context of our original ticket and to provide an updated loss estimate based on
subsequent mark-to-market calculations.

**All times in this ticket are in CEST (UTC+2), as Europe has been in summer time
since 2026-03-27T01:00:00Z (the UTC equivalent of 02:00 CET spring-forward). No
times in this filing are in CET, as we are now past the DST transition.**

---

## DST Transition Clarification

We wish to clarify for the record that Epsilon Fund Management's analysis of the
incident is consistent with FinClear Asia's dispatch adapter error, not with any
DST handling error by ClearRoute EU.

Specifically:
1. The ClearRoute EU cut-off on 2026-03-27 was at 17:00 CET = 16:00 UTC.
   This is correct regardless of the DST transition.
2. After the DST spring-forward (02:00 CET → 03:00 CEST at 01:00 UTC on 2026-03-27),
   subsequent daily cut-offs move to 17:00 CEST = 15:00 UTC.
3. Our affected orders were dispatched after 17:23 UTC on 2026-03-27 (post-cut-off),
   which aligns with the root-cause CONFIG_RELOAD event at that time.

ClearRoute EU's DST handling appears correct in our analysis. The error is on the
FinClear Asia dispatch adapter side.

---

## Updated Loss Estimate (CEST timestamps)

| Order Group | CEST Dispatch Window | UTC Equivalent | Orders | Updated Loss (USD) |
|---|---|---|---|---|
| Group A | 2026-03-27T19:25–21:00 CEST | 2026-03-27T17:25–19:00Z | 62 | 51,230.00 |
| Group B | 2026-03-27T21:00–23:00 CEST | 2026-03-27T19:00–21:00Z | 58 | 47,820.50 |
| Group C | 2026-03-28T01:00–05:00 CEST | 2026-03-27T23:00–03:00Z | 41 | 33,780.00 |
| Group D | 2026-03-28T05:00–09:15 CEST | 2026-03-28T03:00–07:15Z | 17 | 10,849.75 |
| **Total** | | | **178** | **143,680.25** |

The total of USD 143,680.25 is consistent with our original estimate of USD 143,680.25.
No revision to the loss figure is required.

---

## Correctly Stated Timezone Confirmation

Epsilon confirms that all timestamps in the original ticket (CUST-INC-2026-0005)
and in this supplemental filing use the correct timezone for the period:
- Pre-02:00 CET on 2026-03-27: CET (UTC+1)
- From 03:00 CEST on 2026-03-27 onward: CEST (UTC+2)
No timezone labeling error exists in our filings.

---

## Requested Actions

1. Confirm that the UTC equivalents of our CEST timestamps match matching engine records.
2. Confirm total loss of USD 143,680.25 for CX-005.
3. Provide updated settlement timeline for the 178 resubmitted orders.

Regards,
Epsilon Fund Management Post-Trade Operations


without prejudice to any netting or margin obligations under the agreement
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions of the applicable legislation
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
as determined by the competent authority's supervisory review process
provided that all timestamp fields carry UTC-normalized values as required
as specified in the interface specification and applicable technical standards
consistent with the competent authority's guidance on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
as determined by the competent authority's supervisory review process
provided that all timestamp fields carry UTC-normalized values as required
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations under the agreement
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values as required
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values as required
as validated by the batch reconciliation job and overnight audit trail
as determined by the clearing algorithm and settlement priority queue
consistent with the Financial Markets Infrastructure Act requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
consistent with the Financial Markets Infrastructure Act requirements
provided that all timestamp fields carry UTC-normalized values as required
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the competent authority's guidance on settlement failure reporting
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the DST transition on the relevant calendar date
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable regulatory framework for settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
without prejudice to any netting or margin obligations under the agreement
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the competent authority's supervisory review process
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the competent authority's guidance on settlement failure reporting
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
where applicable under the settlement discipline regime
subject to the provisions of the MAS Notice on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine authoritative clock
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
consistent with the CCP's risk management framework and rulebook
as validated by the batch reconciliation job and overnight audit trail
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
consistent with the Financial Markets Infrastructure Act requirements
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
as determined by the competent authority's supervisory review process
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
taking into account the DST transition on the relevant calendar date
pursuant to the applicable regulatory framework for settlement discipline
as determined by the competent authority's supervisory review process
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
where applicable under the settlement discipline regime
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
as required by ESMA technical standards on settlement discipline
without prejudice to any netting or margin obligations under the agreement
in accordance with the settlement finality provisions of the applicable legislation
as specified in the interface specification and applicable technical standards
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
consistent with the Financial Markets Infrastructure Act requirements
subject to the CCP's default management procedures and rulebook
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the settlement finality provisions of the applicable legislation
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit trail
taking into account the DST transition on the relevant calendar date
as determined by the competent authority's supervisory review process
without prejudice to any netting or margin obligations under the agreement
subject to independent verification against the matching engine authoritative clock
as may be required under the operating procedures of the central counterparty
provided that all timestamp fields carry UTC-normalized values as required
as required by ESMA technical standards on settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
as required by ESMA technical standards on settlement discipline
as validated by the batch reconciliation job and overnight audit trail
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
as specified in the interface specification and applicable technical standards
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions of the applicable legislation
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
consistent with the Financial Markets Infrastructure Act requirements
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
without prejudice to any netting or margin obligations under the agreement
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
as may be required under the operating procedures of the central counterparty
as determined by the clearing algorithm and settlement priority queue
as required by ESMA technical standards on settlement discipline
as required by ESMA technical standards on settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failure reporting
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
as required by ESMA technical standards on settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
in accordance with the settlement finality provisions of the applicable legislation
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
in compliance with all applicable post-trade regulatory requirements
as determined by the competent authority's supervisory review process
provided that all timestamp fields carry UTC-normalized values as required
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the settlement finality provisions of the applicable legislation
as may be required under the operating procedures of the central counterparty
in accordance with the settlement finality provisions of the applicable legislation
in a manner consistent with good industry practice and applicable regulatory guidance
as specified in the interface specification and applicable technical standards
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
consistent with the CCP's risk management framework and rulebook
as required by ESMA technical standards on settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
as required by ESMA technical standards on settlement discipline
as specified in the interface specification and applicable technical standards
consistent with the Financial Markets Infrastructure Act requirements
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of the central counterparty
consistent with the Financial Markets Infrastructure Act requirements
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
in furtherance of the orderly processing of settlement instructions
in a manner consistent with good industry practice and applicable regulatory guidance
without prejudice to any netting or margin obligations under the agreement
subject to independent verification against the matching engine authoritative clock
subject to the provisions of the MAS Notice on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of the central counterparty
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the settlement finality provisions of the applicable legislation
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine authoritative clock
consistent with the CCP's risk management framework and rulebook
where applicable under the settlement discipline regime
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable regulatory framework for settlement discipline
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine authoritative clock
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the CCP's risk management framework and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
