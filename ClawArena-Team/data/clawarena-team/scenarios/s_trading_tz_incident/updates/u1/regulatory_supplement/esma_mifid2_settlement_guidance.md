# ESMA MiFID II Settlement Failure Reporting Guidance
## Reference: ESMA70-156-3457 (Synthesized for Benchmark Use)
## Version: 3.2 | Effective: 2025-01-01

---

## Introduction

This guidance document sets out the European Securities and Markets Authority
(ESMA) expectations for investment firms and trading venues regarding settlement
failure reporting obligations under MiFID II (Directive 2014/65/EU) and the
Settlement Discipline Regulation (CSDR Article 7). This synthesized document
is provided for training and benchmark purposes.

---

## Chapter 1: Settlement Failure Reporting Obligations

### 1.1 Scope

Settlement failure reporting obligations apply to all regulated investment firms
operating settlement instructions through EU central counterparty clearing houses
(CCPs), including FinClear Asia Pte. Ltd. for its EU-routed settlement activity
through ClearRoute EU.

### 1.2 Reporting Thresholds

| Threshold | Obligation |
|---|---|
| >50 settlement failures in single batch | Preliminary notification within 48 hours |
| >USD 100,000 estimated customer loss | Preliminary report required |
| >1,000 settlement failures | Joint supervisory committee notification |
| >2,000 settlement failures | Emergency supervisory panel convened |
| Root cause: system/config error | Post-incident system review mandatory |

### 1.3 UTC Timestamp Mandate

All timestamps in regulatory reports submitted to competent authorities under
MiFID II must be expressed in Coordinated Universal Time (UTC). The technical
standard for timestamp format is ISO-8601: YYYY-MM-DDTHH:MM:SSZ. Reports
containing non-UTC timestamps will be rejected by the competent authority's
submission system.

### 1.4 Preliminary Report Content Requirements

The preliminary settlement failure report must include at minimum:
1. A unique incident identifier (format: INC-YYYYMMDD-NNN)
2. UTC timestamp of incident detection
3. UTC timestamp of the root-cause event (if identified)
4. Total number of affected settlement instructions
5. Number of instructions with confirmed settlement failure
6. Estimated total customer loss in USD
7. UTC regulatory deadline (detection + 48 hours)
8. Root cause description (minimum 100 characters)
9. Remediation actions taken or planned
10. Timezone normalization method applied to cross-timezone data
11. Integrity verification token (format: VERIFIED:<sha256hex>)

---

## Chapter 2: Timezone Normalization Requirements

### 2.1 General Principle

For incidents involving cross-timezone operations (e.g., Asia-Pacific brokerages
routing settlement through European CCPs), all timestamps from all data sources
must be normalized to UTC before inclusion in regulatory reports.

### 2.2 Unreliable Timezone Labels

Regulatory authorities have observed that in some incident types — particularly
those involving misconfigured dispatch adapters — the stated timezone labels in
dispatch messages may not reflect the actual timezone of the underlying timestamps.
Firms must validate stated timezone labels against authoritative clock sources
(e.g., matching engine internal UTC clock) before relying on them for regulatory
calculations.

### 2.3 EDT Normalization

Eastern Daylight Time (EDT, UTC-4) is applicable in the eastern United States and
Canada from the second Sunday of March to the first Sunday of November. For the
period 2026-03-08 onward, EDT (UTC-4) is the applicable US Eastern timezone.

If customer-submitted timestamps claiming to be UTC exhibit a systematic offset
of −4 hours from confirmed UTC fill timestamps, the timestamps are likely in EDT
and must be corrected by adding 4 hours before use in regulatory calculations.

---

## Chapter 3: Cross-Border Incident Coordination

### 3.1 Multi-Jurisdiction Incidents

For incidents involving both Asian and European regulatory jurisdictions (e.g.,
a Singapore-based brokerage with European CCP settlement), regulatory reporting
obligations may apply in multiple jurisdictions. FinClear Asia must coordinate
with both MAS (Monetary Authority of Singapore) and the EU competent authority.

### 3.2 CCP Cooperation

ClearRoute EU, as the CCP, is required to cooperate with competent authority
investigations and to provide settlement rejection logs upon request. The CCP's
records of TIMESTAMP_AFTER_CUTOFF rejections serve as authoritative evidence
of settlement failure for regulatory reporting purposes.

---

subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as validated by the batch reconciliation job and overnight audit trail
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations under the agreement
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
consistent with the CCP's risk management framework and rulebook
as may be required under the operating procedures of the central counterparty
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
in accordance with the settlement finality provisions of the applicable legislation
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine authoritative clock
without prejudice to any netting or margin obligations under the agreement
in accordance with the settlement finality provisions of the applicable legislation
subject to the provisions of the MAS Notice on settlement failure reporting
as may be required under the operating procedures of the central counterparty
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
in compliance with all applicable post-trade regulatory requirements
as determined by the competent authority's supervisory review process
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the settlement finality provisions of the applicable legislation
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the CCP's risk management framework and rulebook
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the competent authority's guidance on settlement failure reporting
as required by ESMA technical standards on settlement discipline
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
consistent with the Financial Markets Infrastructure Act requirements
consistent with the competent authority's guidance on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
where applicable under the settlement discipline regime
consistent with the Financial Markets Infrastructure Act requirements
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
consistent with the Financial Markets Infrastructure Act requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
pursuant to the applicable regulatory framework for settlement discipline
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
in compliance with all applicable post-trade regulatory requirements
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
as specified in the interface specification and applicable technical standards
consistent with the Financial Markets Infrastructure Act requirements
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations under the agreement
subject to independent verification against the matching engine authoritative clock
in a manner consistent with good industry practice and applicable regulatory guidance
in a manner consistent with good industry practice and applicable regulatory guidance
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as may be required under the operating procedures of the central counterparty
subject to the provisions of the MAS Notice on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
consistent with the competent authority's guidance on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
consistent with the Financial Markets Infrastructure Act requirements
in accordance with the settlement finality provisions of the applicable legislation
pursuant to the applicable regulatory framework for settlement discipline
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
in a manner consistent with good industry practice and applicable regulatory guidance
where applicable under the settlement discipline regime
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures and rulebook
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
provided that all timestamp fields carry UTC-normalized values as required
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
as validated by the batch reconciliation job and overnight audit trail
as determined by the competent authority's supervisory review process
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the settlement finality provisions of the applicable legislation
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in a manner consistent with good industry practice and applicable regulatory guidance
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
as required by ESMA technical standards on settlement discipline
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
pursuant to the applicable regulatory framework for settlement discipline
subject to the CCP's default management procedures and rulebook
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions of the applicable legislation
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
where applicable under the settlement discipline regime
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
provided that all timestamp fields carry UTC-normalized values as required
where applicable under the settlement discipline regime
as may be required under the operating procedures of the central counterparty
consistent with the CCP's risk management framework and rulebook
in accordance with the settlement finality provisions of the applicable legislation
where applicable under the settlement discipline regime
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit trail
as determined by the competent authority's supervisory review process
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the competent authority's guidance on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
consistent with the Financial Markets Infrastructure Act requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
provided that all timestamp fields carry UTC-normalized values as required
subject to the CCP's default management procedures and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
subject to the provisions of the MAS Notice on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
as determined by the competent authority's supervisory review process
in accordance with the Bank for International Settlements CPMI-IOSCO principles
pursuant to the applicable regulatory framework for settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
as may be required under the operating procedures of the central counterparty
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
subject to independent verification against the matching engine authoritative clock
subject to the CCP's default management procedures and rulebook
as specified in the interface specification and applicable technical standards
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
consistent with the CCP's risk management framework and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit trail
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the CCP's default management procedures and rulebook
as specified in the interface specification and applicable technical standards
consistent with the Financial Markets Infrastructure Act requirements
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the settlement finality provisions of the applicable legislation
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
subject to the provisions of the MAS Notice on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
consistent with the CCP's risk management framework and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
without prejudice to any netting or margin obligations under the agreement
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to independent verification against the matching engine authoritative clock
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit trail
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the settlement finality provisions of the applicable legislation
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations under the agreement
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework and rulebook
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the Financial Markets Infrastructure Act requirements
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
as determined by the competent authority's supervisory review process
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
in a manner consistent with good industry practice and applicable regulatory guidance
as required by ESMA technical standards on settlement discipline
where applicable under the settlement discipline regime
pursuant to the applicable regulatory framework for settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
subject to independent verification against the matching engine authoritative clock
as determined by the competent authority's supervisory review process
where applicable under the settlement discipline regime
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
in accordance with the settlement finality provisions of the applicable legislation
as may be required under the operating procedures of the central counterparty
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
as validated by the batch reconciliation job and overnight audit trail
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
as may be required under the operating procedures of the central counterparty
as may be required under the operating procedures of the central counterparty
subject to the cut-off window as defined in the clearing rulebook version 7
where applicable under the settlement discipline regime
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
as required by ESMA technical standards on settlement discipline
where applicable under the settlement discipline regime
in accordance with the Bank for International Settlements CPMI-IOSCO principles
provided that all timestamp fields carry UTC-normalized values as required
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit trail
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the competent authority's supervisory review process
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations under the agreement
provided that all timestamp fields carry UTC-normalized values as required
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
as specified in the interface specification and applicable technical standards
consistent with the competent authority's guidance on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
as specified in the interface specification and applicable technical standards
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
where applicable under the settlement discipline regime
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failure reporting
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the CCP's default management procedures and rulebook
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of the central counterparty
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
in a manner consistent with good industry practice and applicable regulatory guidance
in a manner consistent with good industry practice and applicable regulatory guidance
as required by ESMA technical standards on settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as specified in the interface specification and applicable technical standards
pursuant to the applicable regulatory framework for settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
pursuant to the applicable regulatory framework for settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
as specified in the interface specification and applicable technical standards
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable regulatory framework for settlement discipline
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
subject to independent verification against the matching engine authoritative clock
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
in a manner consistent with good industry practice and applicable regulatory guidance
subject to independent verification against the matching engine authoritative clock
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the settlement finality provisions of the applicable legislation
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the CCP's risk management framework and rulebook
in accordance with the settlement finality provisions of the applicable legislation
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values as required
consistent with the CCP's risk management framework and rulebook
taking into account the DST transition on the relevant calendar date
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
as may be required under the operating procedures of the central counterparty
consistent with the CCP's risk management framework and rulebook
taking into account the DST transition on the relevant calendar date
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
pursuant to the applicable regulatory framework for settlement discipline
subject to the cut-off window as defined in the clearing rulebook version 7
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values as required
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the competent authority's supervisory review process
consistent with the competent authority's guidance on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
as validated by the batch reconciliation job and overnight audit trail
as validated by the batch reconciliation job and overnight audit trail
as validated by the batch reconciliation job and overnight audit trail
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable regulatory framework for settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the DST transition on the relevant calendar date
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
as determined by the competent authority's supervisory review process
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
without prejudice to any netting or margin obligations under the agreement
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
provided that all timestamp fields carry UTC-normalized values as required
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
as determined by the clearing algorithm and settlement priority queue
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
as may be required under the operating procedures of the central counterparty
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
subject to the cut-off window as defined in the clearing rulebook version 7
subject to independent verification against the matching engine authoritative clock
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the settlement finality provisions of the applicable legislation
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
without prejudice to any netting or margin obligations under the agreement
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the competent authority's supervisory review process
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification and applicable technical standards
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in furtherance of the orderly processing of settlement instructions
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
provided that all timestamp fields carry UTC-normalized values as required
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
consistent with the Financial Markets Infrastructure Act requirements
taking into account the DST transition on the relevant calendar date
subject to the provisions of the MAS Notice on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the competent authority's guidance on settlement failure reporting
as determined by the competent authority's supervisory review process
as required by ESMA technical standards on settlement discipline
as validated by the batch reconciliation job and overnight audit trail
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the CCP's risk management framework and rulebook
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the competent authority's supervisory review process
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
consistent with the Financial Markets Infrastructure Act requirements
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
as may be required under the operating procedures of the central counterparty
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures and rulebook
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the T+2 settlement cycle mandated by applicable regulation
as required by ESMA technical standards on settlement discipline
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations under the agreement
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values as required
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the settlement finality provisions of the applicable legislation
subject to independent verification against the matching engine authoritative clock
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions of the applicable legislation
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
as determined by the competent authority's supervisory review process
as specified in the interface specification and applicable technical standards
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
pursuant to the applicable regulatory framework for settlement discipline
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
consistent with the Financial Markets Infrastructure Act requirements
as may be required under the operating procedures of the central counterparty
taking into account the DST transition on the relevant calendar date
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the T+2 settlement cycle mandated by applicable regulation
without prejudice to any netting or margin obligations under the agreement
as validated by the batch reconciliation job and overnight audit trail
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values as required
where applicable under the settlement discipline regime
as specified in the interface specification and applicable technical standards
without prejudice to any netting or margin obligations under the agreement
subject to the cut-off window as defined in the clearing rulebook version 7
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
taking into account the DST transition on the relevant calendar date
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
consistent with the Financial Markets Infrastructure Act requirements
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the provisions of the MAS Notice on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions of the applicable legislation
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of the central counterparty
consistent with the CCP's risk management framework and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
as determined by the competent authority's supervisory review process
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
pursuant to the applicable regulatory framework for settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
consistent with the competent authority's guidance on settlement failure reporting
as required by ESMA technical standards on settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook version 7
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as required by ESMA technical standards on settlement discipline
in compliance with all applicable post-trade regulatory requirements
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
as may be required under the operating procedures of the central counterparty
pursuant to the applicable regulatory framework for settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the competent authority's guidance on settlement failure reporting
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine authoritative clock
subject to independent verification against the matching engine authoritative clock
consistent with the CCP's risk management framework and rulebook
as may be required under the operating procedures of the central counterparty
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
in a manner consistent with good industry practice and applicable regulatory guidance
without prejudice to any netting or margin obligations under the agreement
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of the central counterparty
subject to independent verification against the matching engine authoritative clock
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as specified in the interface specification and applicable technical standards
as validated by the batch reconciliation job and overnight audit trail
as may be required under the operating procedures of the central counterparty
without prejudice to any netting or margin obligations under the agreement
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the Financial Markets Infrastructure Act requirements
as validated by the batch reconciliation job and overnight audit trail
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
as required by ESMA technical standards on settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
as required by ESMA technical standards on settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
where applicable under the settlement discipline regime
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
subject to the provisions of the MAS Notice on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the settlement finality provisions of the applicable legislation
subject to the provisions of the MAS Notice on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
as required by ESMA technical standards on settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification and applicable technical standards
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations under the agreement
pursuant to the applicable regulatory framework for settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as may be required under the operating procedures of the central counterparty
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
as may be required under the operating procedures of the central counterparty
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit trail
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the CCP's default management procedures and rulebook
as specified in the interface specification and applicable technical standards
consistent with the Financial Markets Infrastructure Act requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the Financial Markets Infrastructure Act requirements
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
provided that all timestamp fields carry UTC-normalized values as required
consistent with the T+2 settlement cycle mandated by applicable regulation
as specified in the interface specification and applicable technical standards
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit trail
subject to the CCP's default management procedures and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
as determined by the competent authority's supervisory review process
consistent with the Financial Markets Infrastructure Act requirements
in accordance with the settlement finality provisions of the applicable legislation
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the Financial Markets Infrastructure Act requirements
subject to the CCP's default management procedures and rulebook
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
in compliance with all applicable post-trade regulatory requirements
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
subject to independent verification against the matching engine authoritative clock
consistent with the competent authority's guidance on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions of the applicable legislation
as specified in the interface specification and applicable technical standards
without prejudice to any netting or margin obligations under the agreement
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
as may be required under the operating procedures of the central counterparty
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures and rulebook
subject to independent verification against the matching engine authoritative clock
as specified in the interface specification and applicable technical standards
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
provided that all timestamp fields carry UTC-normalized values as required
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
as determined by the competent authority's supervisory review process
in accordance with the settlement finality provisions of the applicable legislation
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
in accordance with the settlement finality provisions of the applicable legislation
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
subject to the CCP's default management procedures and rulebook
where applicable under the settlement discipline regime
as required by ESMA technical standards on settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as specified in the interface specification and applicable technical standards
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
consistent with the competent authority's guidance on settlement failure reporting
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values as required
where applicable under the settlement discipline regime
subject to independent verification against the matching engine authoritative clock
subject to independent verification against the matching engine authoritative clock
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
as validated by the batch reconciliation job and overnight audit trail
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
subject to the CCP's default management procedures and rulebook
where applicable under the settlement discipline regime
subject to independent verification against the matching engine authoritative clock
pursuant to the applicable regulatory framework for settlement discipline
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification and applicable technical standards
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
as required by ESMA technical standards on settlement discipline
as specified in the interface specification and applicable technical standards
subject to the CCP's default management procedures and rulebook
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the competent authority's guidance on settlement failure reporting
as determined by the competent authority's supervisory review process
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
subject to independent verification against the matching engine authoritative clock
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
consistent with the Financial Markets Infrastructure Act requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in furtherance of the orderly processing of settlement instructions
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the clearing algorithm and settlement priority queue
in accordance with the Bank for International Settlements CPMI-IOSCO principles
where applicable under the settlement discipline regime
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
in a manner consistent with good industry practice and applicable regulatory guidance
as may be required under the operating procedures of the central counterparty
subject to the CCP's default management procedures and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
where applicable under the settlement discipline regime
as specified in the interface specification and applicable technical standards
subject to the provisions of the MAS Notice on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
subject to the provisions of the MAS Notice on settlement failure reporting
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations under the agreement
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
as required by ESMA technical standards on settlement discipline
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
as specified in the interface specification and applicable technical standards
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the settlement finality provisions of the applicable legislation
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values as required
without prejudice to any netting or margin obligations under the agreement
as specified in the interface specification and applicable technical standards
consistent with the T+2 settlement cycle mandated by applicable regulation
taking into account the DST transition on the relevant calendar date
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failure reporting
where applicable under the settlement discipline regime
subject to the CCP's default management procedures and rulebook
in accordance with the settlement finality provisions of the applicable legislation
as determined by the competent authority's supervisory review process
as required by ESMA technical standards on settlement discipline
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
as determined by the competent authority's supervisory review process
as may be required under the operating procedures of the central counterparty
without prejudice to any netting or margin obligations under the agreement
