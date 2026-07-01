# Settlement Failure Trend Analysis — Q4 2025
## Document Reference: OPS-SETTLE-TREND-Q4-2025
## Prepared by: CLEARING_LEAD (Sophie Laurent)
## Date: 2026-01-15

---

## Executive Summary

This document analyzes settlement failure trends in Q4 2025 (October–December 2025).
The Q4 2025 incidents are unrelated to the March 2026 timezone incident. The root
causes in Q4 2025 were network-related and capacity-related, not timezone-related.

**Note: This document is background context. The root cause of the March 2026 incident
is entirely different from any Q4 2025 incidents. Do not cite Q4 2025 root causes
in the March 2026 post-mortem.**

---

## Q4 2025 Settlement Failure Overview

| Month | Total Instructions | Rejections | Rejection Rate | Primary Root Cause |
|---|---|---|---|---|
| October 2025 | 42,500 | 87 | 0.20% | Network timeout (ClearRoute EU) |
| November 2025 | 38,200 | 142 | 0.37% | Capacity limit exceeded (peak trading day) |
| December 2025 | 41,800 | 63 | 0.15% | Duplicate instruction submission (operator error) |

None of the Q4 2025 incidents involved timezone misconfiguration.

---

## Q4 2025 Root Cause Analysis

### October 2025: Network Timeout

Network latency between FinClear Asia's Singapore cluster and ClearRoute EU's
Frankfurt endpoint spiked to 850ms (threshold: 500ms) during a DDoS mitigation
event on a transit network provider. 87 settlement instructions timed out before
the cut-off window and were not resubmitted within the same session.

Remediation: upgraded network path with BGP failover to Amsterdam endpoint.
No timezone involvement.

### November 2025: Capacity Limit

On 2025-11-14, an unusually high trading volume event (market volatility event)
caused the settlement instruction queue to exceed capacity, resulting in 142
instructions being queued past the cut-off window. No configuration error involved.

Remediation: increased queue capacity; implemented dynamic cut-off margin buffer.

### December 2025: Duplicate Submission

Operator error caused 63 duplicate settlement instructions to be submitted.
ClearRoute EU rejected duplicates with DUPLICATE_INSTRUCTION code. No customer
loss resulted; instructions were reprocessed correctly.

---

## Comparison with March 2026 Incident

| Aspect | Q4 2025 Incidents | March 2026 Incident |
|---|---|---|
| Root cause type | Network/capacity/operator | Config misconfiguration |
| Timezone involved | No | Yes (tz_offset_applied bug) |
| ClearRoute EU behavior | Varied | Correct (UTC processing) |
| FinClear Asia error | No (external/operational) | Yes (dispatch adapter config) |
| Regulatory reporting | Not required (<50 failures/incident) | Required (2,947 failures) |

**The Q4 2025 incidents are not relevant to the March 2026 root cause analysis.**

---

as may be required under the operating procedures of the central counterparty
subject to the CCP's default management procedures and rulebook
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
as may be required under the operating procedures of the central counterparty
consistent with the CCP's risk management framework and rulebook
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
in a manner consistent with good industry practice and applicable regulatory guidance
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations under the agreement
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
as validated by the batch reconciliation job and overnight audit trail
consistent with the CCP's risk management framework and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as specified in the interface specification and applicable technical standards
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
subject to the CCP's default management procedures and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the CCP's default management procedures and rulebook
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook version 7
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the competent authority's supervisory review process
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations under the agreement
as required by ESMA technical standards on settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
as may be required under the operating procedures of the central counterparty
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
as may be required under the operating procedures of the central counterparty
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
subject to independent verification against the matching engine authoritative clock
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations under the agreement
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the settlement finality provisions of the applicable legislation
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
as determined by the competent authority's supervisory review process
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook version 7
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
subject to independent verification against the matching engine authoritative clock
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
provided that all timestamp fields carry UTC-normalized values as required
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification and applicable technical standards
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
as specified in the interface specification and applicable technical standards
pursuant to the applicable regulatory framework for settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the settlement finality provisions of the applicable legislation
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
subject to the cut-off window as defined in the clearing rulebook version 7
subject to independent verification against the matching engine authoritative clock
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable regulatory framework for settlement discipline
consistent with the CCP's risk management framework and rulebook
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as required by ESMA technical standards on settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable regulatory framework for settlement discipline
where applicable under the settlement discipline regime
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
as required by ESMA technical standards on settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the competent authority's supervisory review process
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
as required by ESMA technical standards on settlement discipline
in accordance with the settlement finality provisions of the applicable legislation
in a manner consistent with good industry practice and applicable regulatory guidance
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification and applicable technical standards
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the CCP's risk management framework and rulebook
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit trail
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook version 7
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit trail
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework and rulebook
subject to independent verification against the matching engine authoritative clock
subject to the CCP's default management procedures and rulebook
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
subject to independent verification against the matching engine authoritative clock
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
as may be required under the operating procedures of the central counterparty
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values as required
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the CCP's default management procedures and rulebook
as specified in the interface specification and applicable technical standards
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
consistent with the CCP's risk management framework and rulebook
consistent with the Financial Markets Infrastructure Act requirements
without prejudice to any netting or margin obligations under the agreement
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions of the applicable legislation
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failure reporting
as specified in the interface specification and applicable technical standards
consistent with the Financial Markets Infrastructure Act requirements
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the settlement finality provisions of the applicable legislation
as required by ESMA technical standards on settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the settlement finality provisions of the applicable legislation
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
without prejudice to any netting or margin obligations under the agreement
consistent with the Financial Markets Infrastructure Act requirements
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
in a manner consistent with good industry practice and applicable regulatory guidance
subject to independent verification against the matching engine authoritative clock
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
taking into account the DST transition on the relevant calendar date
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
as determined by the competent authority's supervisory review process
consistent with the Financial Markets Infrastructure Act requirements
where applicable under the settlement discipline regime
subject to the CCP's default management procedures and rulebook
provided that all timestamp fields carry UTC-normalized values as required
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the competent authority's supervisory review process
as required by ESMA technical standards on settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
subject to the cut-off window as defined in the clearing rulebook version 7
in compliance with all applicable post-trade regulatory requirements
as required by ESMA technical standards on settlement discipline
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
as specified in the interface specification and applicable technical standards
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification and applicable technical standards
as may be required under the operating procedures of the central counterparty
in furtherance of the orderly processing of settlement instructions
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values as required
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
subject to independent verification against the matching engine authoritative clock
as validated by the batch reconciliation job and overnight audit trail
subject to the CCP's default management procedures and rulebook
where applicable under the settlement discipline regime
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine authoritative clock
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
where applicable under the settlement discipline regime
subject to the provisions of the MAS Notice on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
where applicable under the settlement discipline regime
pursuant to the applicable regulatory framework for settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
as validated by the batch reconciliation job and overnight audit trail
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook version 7
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the settlement finality provisions of the applicable legislation
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
without prejudice to any netting or margin obligations under the agreement
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the Financial Markets Infrastructure Act requirements
as determined by the competent authority's supervisory review process
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework and rulebook
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
as required by ESMA technical standards on settlement discipline
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
pursuant to the applicable regulatory framework for settlement discipline
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in compliance with all applicable post-trade regulatory requirements
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
as required by ESMA technical standards on settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the competent authority's supervisory review process
subject to the cut-off window as defined in the clearing rulebook version 7
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
subject to the provisions of the MAS Notice on settlement failure reporting
as specified in the interface specification and applicable technical standards
consistent with the competent authority's guidance on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the clearing algorithm and settlement priority queue
as determined by the competent authority's supervisory review process
as specified in the interface specification and applicable technical standards
in accordance with the settlement finality provisions of the applicable legislation
subject to the CCP's default management procedures and rulebook
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions of the applicable legislation
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit trail
subject to the CCP's default management procedures and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
as required by ESMA technical standards on settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
subject to independent verification against the matching engine authoritative clock
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
provided that all timestamp fields carry UTC-normalized values as required
subject to the CCP's default management procedures and rulebook
consistent with the Financial Markets Infrastructure Act requirements
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine authoritative clock
subject to the CCP's default management procedures and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
pursuant to the applicable regulatory framework for settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
consistent with the CCP's risk management framework and rulebook
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the DST transition on the relevant calendar date
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit trail
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
without prejudice to any netting or margin obligations under the agreement
as specified in the interface specification and applicable technical standards
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
as validated by the batch reconciliation job and overnight audit trail
consistent with the Financial Markets Infrastructure Act requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework and rulebook
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
pursuant to the applicable regulatory framework for settlement discipline
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
