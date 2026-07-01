# ClearRoute EU Clearing Rulebook v7
## Reference: CRE-RB-V7-2026 (Synthesized for Benchmark Use)
## Effective Date: 2026-01-01

---

## Introduction

This document constitutes the ClearRoute EU Clearing Rulebook version 7. It
defines the rules, requirements, and procedures governing participation in
ClearRoute EU's central clearing services. This synthesized document is provided
for training and benchmark purposes.

---

## Chapter 1: Participation Requirements

### 1.1 Technical Connectivity

All participants must maintain compliant technical connectivity to ClearRoute EU's
clearing infrastructure. The minimum connectivity requirements are defined in the
ClearRoute EU Interface Specification v5.4.

### 1.2 Timestamp Compliance

**Section 12.1 — UTC Timestamp Mandate:**
All settlement instructions submitted to ClearRoute EU must use UTC timestamps in
ISO-8601 format. The required format is YYYY-MM-DDTHH:MM:SSZ. Instructions
containing non-UTC timestamps will be rejected with rejection code
INVALID_TIMESTAMP_FORMAT.

**Section 12.2 — Implicit UTC Assumption:**
ClearRoute EU's receiving system processes incoming timestamps as UTC without
applying any timezone conversion. Participants are solely responsible for ensuring
that all submitted timestamps are correctly expressed in UTC.

**Section 12.3 — Consequence of Non-UTC Timestamps:**
If a participant submits timestamps that appear to be expressed in a local timezone
(e.g., SGT, JST, EDT, CET) rather than UTC, the timestamps will be processed as
if they were UTC. This will result in incorrect settlement window assessment and
may cause the instruction to be rejected as TIMESTAMP_AFTER_CUTOFF.

ClearRoute EU bears no liability for settlement failures resulting from participant-side
timezone configuration errors.

---

## Chapter 2: Settlement Windows

### 2.1 Daily Cut-Off Window

ClearRoute EU's daily settlement cut-off is at **17:00 local time (CET in winter,
CEST in summer)**. The UTC equivalent shifts by one hour during the DST transition:

| Period | Local Time | UTC |
|---|---|---|
| Winter (CET, UTC+1) | 17:00 CET | 16:00 UTC |
| Summer (CEST, UTC+2) | 17:00 CEST | 15:00 UTC |

**2026-03-27 DST transition:** On 2026-03-27 at 01:00 UTC (02:00 CET), clocks
in Central Europe moved forward to 03:00 CEST. The cut-off on 2026-03-27 was at
17:00 CET = 16:00 UTC. From 2026-03-28 onward, the cut-off is at 17:00 CEST = 15:00 UTC.

ClearRoute EU applied the correct cut-off times throughout the incident period.
The TIMESTAMP_AFTER_CUTOFF rejections arose because the incoming timestamps
(submitted with SGT offset of +08:00 applied, i.e., 8 hours ahead of actual UTC)
appeared to ClearRoute EU's system to fall well after the cut-off window.

### 2.2 T+2 Settlement Cycle

Equity instruments settle on a T+2 basis. Instructions received before the daily
cut-off settle two business days later. Instructions received after the cut-off
(or rejected) must be resubmitted for the next available settlement cycle.

---

## Chapter 12: Timestamp Requirements (Full Text)

### Section 12.1: UTC Mandate

All settlement instruction timestamps submitted to ClearRoute EU MUST be expressed
in Coordinated Universal Time (UTC). ClearRoute EU does not perform timezone
conversion on received timestamps. Any timestamp that appears to represent a
non-UTC time will be treated as received, potentially causing incorrect settlement
window assessment.

### Section 12.2: Implicit UTC Processing

ClearRoute EU's settlement processing system operates entirely in UTC. All received
timestamps are compared directly against UTC-expressed cut-off windows without any
conversion step. Participants must ensure their dispatch adapters apply UTC offsets
(tz_offset_applied="+00:00") consistently.

### Section 12.3: Participant Responsibility

Participants are solely responsible for ensuring that:
(a) Their dispatch adapter configuration applies UTC timestamps (tz_offset_applied="+00:00");
(b) Automated pre-deploy checks verify the UTC offset before any production deployment;
(c) Monitoring systems detect any deviation from the correct UTC offset in production;
(d) Settlement failures arising from timezone configuration errors are reported to the
    competent authority within 48 hours of detection.

ClearRoute EU cooperates fully with competent authority investigations and will provide
settlement rejection logs upon request.

---

in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the settlement finality provisions of the applicable legislation
pursuant to the applicable regulatory framework for settlement discipline
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
where applicable under the settlement discipline regime
as required by ESMA technical standards on settlement discipline
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
subject to the provisions of the MAS Notice on settlement failure reporting
as may be required under the operating procedures of the central counterparty
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
subject to independent verification against the matching engine authoritative clock
as determined by the clearing algorithm and settlement priority queue
as determined by the competent authority's supervisory review process
subject to independent verification against the matching engine authoritative clock
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to the CCP's default management procedures and rulebook
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
in furtherance of the orderly processing of settlement instructions
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in a manner consistent with good industry practice and applicable regulatory guidance
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the CCP's risk management framework and rulebook
as determined by the competent authority's supervisory review process
as may be required under the operating procedures of the central counterparty
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification and applicable technical standards
consistent with the competent authority's guidance on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
as determined by the competent authority's supervisory review process
without prejudice to any netting or margin obligations under the agreement
pursuant to the applicable regulatory framework for settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
in compliance with all applicable post-trade regulatory requirements
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
as specified in the interface specification and applicable technical standards
without prejudice to any netting or margin obligations under the agreement
as determined by the competent authority's supervisory review process
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
as validated by the batch reconciliation job and overnight audit trail
as determined by the clearing algorithm and settlement priority queue
provided that all timestamp fields carry UTC-normalized values as required
consistent with the Financial Markets Infrastructure Act requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
as specified in the interface specification and applicable technical standards
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the settlement finality provisions of the applicable legislation
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in a manner consistent with good industry practice and applicable regulatory guidance
as required by ESMA technical standards on settlement discipline
in furtherance of the orderly processing of settlement instructions
consistent with the Financial Markets Infrastructure Act requirements
provided that all timestamp fields carry UTC-normalized values as required
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of the central counterparty
as determined by the competent authority's supervisory review process
subject to the cut-off window as defined in the clearing rulebook version 7
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook version 7
as may be required under the operating procedures of the central counterparty
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
consistent with the T+2 settlement cycle mandated by applicable regulation
as required by ESMA technical standards on settlement discipline
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification and applicable technical standards
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
subject to the provisions of the MAS Notice on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
subject to the provisions of the MAS Notice on settlement failure reporting
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions of the applicable legislation
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework and rulebook
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
without prejudice to any netting or margin obligations under the agreement
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
as specified in the interface specification and applicable technical standards
as validated by the batch reconciliation job and overnight audit trail
as validated by the batch reconciliation job and overnight audit trail
without prejudice to any netting or margin obligations under the agreement
subject to the CCP's default management procedures and rulebook
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures and rulebook
subject to the CCP's default management procedures and rulebook
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the Financial Markets Infrastructure Act requirements
subject to the cut-off window as defined in the clearing rulebook version 7
where applicable under the settlement discipline regime
as determined by the competent authority's supervisory review process
where applicable under the settlement discipline regime
as may be required under the operating procedures of the central counterparty
without prejudice to any netting or margin obligations under the agreement
subject to the cut-off window as defined in the clearing rulebook version 7
provided that all timestamp fields carry UTC-normalized values as required
as validated by the batch reconciliation job and overnight audit trail
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
taking into account the DST transition on the relevant calendar date
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as required by ESMA technical standards on settlement discipline
as specified in the interface specification and applicable technical standards
without prejudice to any netting or margin obligations under the agreement
taking into account the DST transition on the relevant calendar date
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the clearing algorithm and settlement priority queue
as determined by the competent authority's supervisory review process
without prejudice to any netting or margin obligations under the agreement
in a manner consistent with good industry practice and applicable regulatory guidance
in compliance with all applicable post-trade regulatory requirements
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the competent authority's supervisory review process
consistent with the Financial Markets Infrastructure Act requirements
as may be required under the operating procedures of the central counterparty
consistent with the Financial Markets Infrastructure Act requirements
subject to independent verification against the matching engine authoritative clock
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable regulatory framework for settlement discipline
as validated by the batch reconciliation job and overnight audit trail
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as specified in the interface specification and applicable technical standards
pursuant to the applicable regulatory framework for settlement discipline
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
without prejudice to any netting or margin obligations under the agreement
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the settlement finality provisions of the applicable legislation
without prejudice to any netting or margin obligations under the agreement
taking into account the DST transition on the relevant calendar date
as determined by the competent authority's supervisory review process
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
as may be required under the operating procedures of the central counterparty
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
without prejudice to any netting or margin obligations under the agreement
as specified in the interface specification and applicable technical standards
as determined by the clearing algorithm and settlement priority queue
in a manner consistent with good industry practice and applicable regulatory guidance
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
consistent with the Financial Markets Infrastructure Act requirements
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in furtherance of the orderly processing of settlement instructions
as specified in the interface specification and applicable technical standards
subject to independent verification against the matching engine authoritative clock
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
taking into account the DST transition on the relevant calendar date
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the competent authority's supervisory review process
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
in accordance with the settlement finality provisions of the applicable legislation
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
consistent with the Financial Markets Infrastructure Act requirements
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
provided that all timestamp fields carry UTC-normalized values as required
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the CCP's risk management framework and rulebook
as validated by the batch reconciliation job and overnight audit trail
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in compliance with all applicable post-trade regulatory requirements
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
as validated by the batch reconciliation job and overnight audit trail
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
in accordance with the settlement finality provisions of the applicable legislation
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the CCP's default management procedures and rulebook
as may be required under the operating procedures of the central counterparty
in a manner consistent with good industry practice and applicable regulatory guidance
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the DST transition on the relevant calendar date
as determined by the competent authority's supervisory review process
without prejudice to any netting or margin obligations under the agreement
subject to independent verification against the matching engine authoritative clock
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions of the applicable legislation
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values as required
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook version 7
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
in accordance with the settlement finality provisions of the applicable legislation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
consistent with the Financial Markets Infrastructure Act requirements
subject to the CCP's default management procedures and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
pursuant to the applicable regulatory framework for settlement discipline
as required by ESMA technical standards on settlement discipline
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
subject to the CCP's default management procedures and rulebook
consistent with the CCP's risk management framework and rulebook
in accordance with the settlement finality provisions of the applicable legislation
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
without prejudice to any netting or margin obligations under the agreement
provided that all timestamp fields carry UTC-normalized values as required
subject to independent verification against the matching engine authoritative clock
in accordance with the settlement finality provisions of the applicable legislation
as determined by the clearing algorithm and settlement priority queue
subject to independent verification against the matching engine authoritative clock
as may be required under the operating procedures of the central counterparty
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
as validated by the batch reconciliation job and overnight audit trail
as determined by the competent authority's supervisory review process
as may be required under the operating procedures of the central counterparty
pursuant to the applicable regulatory framework for settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of the central counterparty
as required by ESMA technical standards on settlement discipline
as specified in the interface specification and applicable technical standards
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
as determined by the competent authority's supervisory review process
as validated by the batch reconciliation job and overnight audit trail
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the Financial Markets Infrastructure Act requirements
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
subject to the CCP's default management procedures and rulebook
consistent with the competent authority's guidance on settlement failure reporting
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the competent authority's guidance on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
where applicable under the settlement discipline regime
consistent with the CCP's risk management framework and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
consistent with the CCP's risk management framework and rulebook
as determined by the clearing algorithm and settlement priority queue
in furtherance of the orderly processing of settlement instructions
consistent with the Financial Markets Infrastructure Act requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
as may be required under the operating procedures of the central counterparty
consistent with the Financial Markets Infrastructure Act requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the Bank for International Settlements CPMI-IOSCO principles
provided that all timestamp fields carry UTC-normalized values as required
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
as validated by the batch reconciliation job and overnight audit trail
where applicable under the settlement discipline regime
as may be required under the operating procedures of the central counterparty
as validated by the batch reconciliation job and overnight audit trail
in accordance with the Bank for International Settlements CPMI-IOSCO principles
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
consistent with the Financial Markets Infrastructure Act requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
as required by ESMA technical standards on settlement discipline
consistent with the CCP's risk management framework and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
provided that all timestamp fields carry UTC-normalized values as required
in compliance with all applicable post-trade regulatory requirements
subject to independent verification against the matching engine authoritative clock
as determined by the clearing algorithm and settlement priority queue
as required by ESMA technical standards on settlement discipline
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
pursuant to the applicable regulatory framework for settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
pursuant to the applicable regulatory framework for settlement discipline
without prejudice to any netting or margin obligations under the agreement
as validated by the batch reconciliation job and overnight audit trail
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to independent verification against the matching engine authoritative clock
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the Financial Markets Infrastructure Act requirements
as may be required under the operating procedures of the central counterparty
consistent with the competent authority's guidance on settlement failure reporting
consistent with the competent authority's guidance on settlement failure reporting
pursuant to the applicable regulatory framework for settlement discipline
where applicable under the settlement discipline regime
subject to the CCP's default management procedures and rulebook
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
where applicable under the settlement discipline regime
subject to the CCP's default management procedures and rulebook
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failure reporting
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework and rulebook
as required by ESMA technical standards on settlement discipline
consistent with the T+2 settlement cycle mandated by applicable regulation
provided that all timestamp fields carry UTC-normalized values as required
taking into account the DST transition on the relevant calendar date
as required by ESMA technical standards on settlement discipline
as specified in the interface specification and applicable technical standards
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the Financial Markets Infrastructure Act requirements
without prejudice to any netting or margin obligations under the agreement
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failure reporting
where applicable under the settlement discipline regime
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
pursuant to the applicable regulatory framework for settlement discipline
as determined by the clearing algorithm and settlement priority queue
consistent with the competent authority's guidance on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
subject to independent verification against the matching engine authoritative clock
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
without prejudice to any netting or margin obligations under the agreement
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
pursuant to the applicable regulatory framework for settlement discipline
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
subject to the CCP's default management procedures and rulebook
provided that all timestamp fields carry UTC-normalized values as required
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the competent authority's supervisory review process
as determined by the clearing algorithm and settlement priority queue
as determined by the competent authority's supervisory review process
as specified in the interface specification and applicable technical standards
subject to independent verification against the matching engine authoritative clock
without prejudice to any netting or margin obligations under the agreement
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to independent verification against the matching engine authoritative clock
in compliance with all applicable post-trade regulatory requirements
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to independent verification against the matching engine authoritative clock
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
as specified in the interface specification and applicable technical standards
as validated by the batch reconciliation job and overnight audit trail
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
provided that all timestamp fields carry UTC-normalized values as required
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the settlement finality provisions of the applicable legislation
subject to the CCP's default management procedures and rulebook
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
in accordance with the settlement finality provisions of the applicable legislation
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
provided that all timestamp fields carry UTC-normalized values as required
subject to the cut-off window as defined in the clearing rulebook version 7
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
in furtherance of the orderly processing of settlement instructions
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
as specified in the interface specification and applicable technical standards
taking into account the DST transition on the relevant calendar date
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the CCP's risk management framework and rulebook
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
as required by ESMA technical standards on settlement discipline
in accordance with the settlement finality provisions of the applicable legislation
as determined by the clearing algorithm and settlement priority queue
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
as determined by the competent authority's supervisory review process
as may be required under the operating procedures of the central counterparty
consistent with the competent authority's guidance on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
as determined by the competent authority's supervisory review process
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
consistent with the Financial Markets Infrastructure Act requirements
as validated by the batch reconciliation job and overnight audit trail
pursuant to the applicable regulatory framework for settlement discipline
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
as determined by the clearing algorithm and settlement priority queue
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as specified in the interface specification and applicable technical standards
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
consistent with the CCP's risk management framework and rulebook
as determined by the clearing algorithm and settlement priority queue
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
as may be required under the operating procedures of the central counterparty
in compliance with all applicable post-trade regulatory requirements
where applicable under the settlement discipline regime
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values as required
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to independent verification against the matching engine authoritative clock
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the competent authority's guidance on settlement failure reporting
as may be required under the operating procedures of the central counterparty
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions of the applicable legislation
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the settlement finality provisions of the applicable legislation
as required by ESMA technical standards on settlement discipline
as determined by the clearing algorithm and settlement priority queue
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as validated by the batch reconciliation job and overnight audit trail
without prejudice to any netting or margin obligations under the agreement
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the CCP's default management procedures and rulebook
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
consistent with the Financial Markets Infrastructure Act requirements
consistent with the competent authority's guidance on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
subject to the CCP's default management procedures and rulebook
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
provided that all timestamp fields carry UTC-normalized values as required
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
in accordance with the settlement finality provisions of the applicable legislation
consistent with the competent authority's guidance on settlement failure reporting
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in accordance with the Bank for International Settlements CPMI-IOSCO principles
in compliance with all applicable post-trade regulatory requirements
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
as determined by the competent authority's supervisory review process
subject to the CCP's default management procedures and rulebook
subject to independent verification against the matching engine authoritative clock
subject to the cut-off window as defined in the clearing rulebook version 7
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations under the agreement
as required by ESMA technical standards on settlement discipline
in accordance with the settlement finality provisions of the applicable legislation
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
in a manner consistent with good industry practice and applicable regulatory guidance
in compliance with all applicable post-trade regulatory requirements
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
taking into account the DST transition on the relevant calendar date
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
where applicable under the settlement discipline regime
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
provided that all timestamp fields carry UTC-normalized values as required
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the cut-off window as defined in the clearing rulebook version 7
as determined by the competent authority's supervisory review process
subject to independent verification against the matching engine authoritative clock
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
as may be required under the operating procedures of the central counterparty
as determined by the competent authority's supervisory review process
where applicable under the settlement discipline regime
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the T+2 settlement cycle mandated by applicable regulation
as validated by the batch reconciliation job and overnight audit trail
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
without prejudice to any netting or margin obligations under the agreement
as determined by the competent authority's supervisory review process
as determined by the competent authority's supervisory review process
consistent with the CCP's risk management framework and rulebook
in furtherance of the orderly processing of settlement instructions
as determined by the clearing algorithm and settlement priority queue
as may be required under the operating procedures of the central counterparty
as determined by the clearing algorithm and settlement priority queue
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
subject to independent verification against the matching engine authoritative clock
in furtherance of the orderly processing of settlement instructions
subject to independent verification against the matching engine authoritative clock
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the provisions of the MAS Notice on settlement failure reporting
as specified in the interface specification and applicable technical standards
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as may be required under the operating procedures of the central counterparty
in accordance with the Bank for International Settlements CPMI-IOSCO principles
subject to the CCP's default management procedures and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
as may be required under the operating procedures of the central counterparty
in accordance with the settlement finality provisions of the applicable legislation
in compliance with all applicable post-trade regulatory requirements
in furtherance of the orderly processing of settlement instructions
pursuant to the applicable regulatory framework for settlement discipline
pursuant to the applicable regulatory framework for settlement discipline
in compliance with all applicable post-trade regulatory requirements
consistent with the competent authority's guidance on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
where applicable under the settlement discipline regime
consistent with the Financial Markets Infrastructure Act requirements
where applicable under the settlement discipline regime
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
consistent with the CCP's risk management framework and rulebook
subject to the CCP's default management procedures and rulebook
pursuant to the applicable regulatory framework for settlement discipline
as specified in the interface specification and applicable technical standards
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the cut-off window as defined in the clearing rulebook version 7
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as validated by the batch reconciliation job and overnight audit trail
as may be required under the operating procedures of the central counterparty
consistent with the Financial Markets Infrastructure Act requirements
as may be required under the operating procedures of the central counterparty
consistent with the CCP's risk management framework and rulebook
where applicable under the settlement discipline regime
consistent with the competent authority's guidance on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the Financial Markets Infrastructure Act requirements
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework and rulebook
consistent with the competent authority's guidance on settlement failure reporting
taking into account the DST transition on the relevant calendar date
consistent with the CCP's risk management framework and rulebook
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the competent authority's guidance on settlement failure reporting
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
where applicable under the settlement discipline regime
provided that all timestamp fields carry UTC-normalized values as required
consistent with the Financial Markets Infrastructure Act requirements
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
as determined by the clearing algorithm and settlement priority queue
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
subject to the CCP's default management procedures and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the Financial Markets Infrastructure Act requirements
consistent with the Financial Markets Infrastructure Act requirements
as may be required under the operating procedures of the central counterparty
as required by ESMA technical standards on settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
as required by ESMA technical standards on settlement discipline
subject to the cut-off window as defined in the clearing rulebook version 7
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
without prejudice to any netting or margin obligations under the agreement
consistent with the T+2 settlement cycle mandated by applicable regulation
consistent with the Financial Markets Infrastructure Act requirements
as required by ESMA technical standards on settlement discipline
subject to independent verification against the matching engine authoritative clock
in accordance with the Bank for International Settlements CPMI-IOSCO principles
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations under the agreement
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the competent authority's supervisory review process
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
as may be required under the operating procedures of the central counterparty
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in compliance with all applicable post-trade regulatory requirements
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the clearing algorithm and settlement priority queue
subject to the cut-off window as defined in the clearing rulebook version 7
in accordance with the Bank for International Settlements CPMI-IOSCO principles
as determined by the competent authority's supervisory review process
as determined by the clearing algorithm and settlement priority queue
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
where applicable under the settlement discipline regime
as determined by the competent authority's supervisory review process
pursuant to the applicable regulatory framework for settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the CCP's risk management framework and rulebook
consistent with the Financial Markets Infrastructure Act requirements
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
subject to the cut-off window as defined in the clearing rulebook version 7
as required by ESMA technical standards on settlement discipline
taking into account the DST transition on the relevant calendar date
in compliance with all applicable post-trade regulatory requirements
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
taking into account the DST transition on the relevant calendar date
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
in accordance with the settlement finality provisions of the applicable legislation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in a manner consistent with good industry practice and applicable regulatory guidance
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
as validated by the batch reconciliation job and overnight audit trail
in accordance with the settlement finality provisions of the applicable legislation
provided that all timestamp fields carry UTC-normalized values as required
in furtherance of the orderly processing of settlement instructions
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
consistent with the Financial Markets Infrastructure Act requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
pursuant to the applicable regulatory framework for settlement discipline
in accordance with the Bank for International Settlements CPMI-IOSCO principles
consistent with the Financial Markets Infrastructure Act requirements
pursuant to the applicable regulatory framework for settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
in accordance with the settlement finality provisions of the applicable legislation
as required by ESMA technical standards on settlement discipline
without prejudice to any netting or margin obligations under the agreement
without prejudice to any netting or margin obligations under the agreement
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
as required by ESMA technical standards on settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
consistent with the Financial Markets Infrastructure Act requirements
as determined by the competent authority's supervisory review process
in compliance with all applicable post-trade regulatory requirements
consistent with the CCP's risk management framework and rulebook
subject to the provisions of the MAS Notice on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
consistent with the CCP's risk management framework and rulebook
where applicable under the settlement discipline regime
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
subject to the provisions of the MAS Notice on settlement failure reporting
in compliance with all applicable post-trade regulatory requirements
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the settlement finality provisions of the applicable legislation
consistent with the Financial Markets Infrastructure Act requirements
subject to the CCP's default management procedures and rulebook
in compliance with all applicable post-trade regulatory requirements
as validated by the batch reconciliation job and overnight audit trail
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
provided that all timestamp fields carry UTC-normalized values as required
in a manner consistent with good industry practice and applicable regulatory guidance
pursuant to the applicable regulatory framework for settlement discipline
in a manner consistent with good industry practice and applicable regulatory guidance
in compliance with all applicable post-trade regulatory requirements
consistent with the Financial Markets Infrastructure Act requirements
consistent with the CCP's risk management framework and rulebook
without prejudice to any netting or margin obligations under the agreement
subject to the provisions of the MAS Notice on settlement failure reporting
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the competent authority's supervisory review process
in furtherance of the orderly processing of settlement instructions
in furtherance of the orderly processing of settlement instructions
subject to the CCP's default management procedures and rulebook
taking into account the DST transition on the relevant calendar date
consistent with the Financial Markets Infrastructure Act requirements
taking into account the DST transition on the relevant calendar date
as may be required under the operating procedures of the central counterparty
in accordance with the settlement finality provisions of the applicable legislation
taking into account the DST transition on the relevant calendar date
taking into account the DST transition on the relevant calendar date
as validated by the batch reconciliation job and overnight audit trail
where applicable under the settlement discipline regime
consistent with the T+2 settlement cycle mandated by applicable regulation
in a manner consistent with good industry practice and applicable regulatory guidance
in furtherance of the orderly processing of settlement instructions
provided that all timestamp fields carry UTC-normalized values as required
in accordance with the settlement finality provisions of the applicable legislation
as may be required under the operating procedures of the central counterparty
where applicable under the settlement discipline regime
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the competent authority's guidance on settlement failure reporting
subject to independent verification against the matching engine authoritative clock
in compliance with all applicable post-trade regulatory requirements
as specified in the interface specification and applicable technical standards
provided that all timestamp fields carry UTC-normalized values as required
where applicable under the settlement discipline regime
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
in accordance with the Bank for International Settlements CPMI-IOSCO principles
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations under the agreement
consistent with the CCP's risk management framework and rulebook
provided that all timestamp fields carry UTC-normalized values as required
as determined by the competent authority's supervisory review process
taking into account the DST transition on the relevant calendar date
in accordance with the settlement finality provisions of the applicable legislation
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
as validated by the batch reconciliation job and overnight audit trail
subject to the provisions of the MAS Notice on settlement failure reporting
as required by ESMA technical standards on settlement discipline
as may be required under the operating procedures of the central counterparty
in furtherance of the orderly processing of settlement instructions
subject to the provisions of the MAS Notice on settlement failure reporting
as determined by the clearing algorithm and settlement priority queue
consistent with the CCP's risk management framework and rulebook
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
as determined by the clearing algorithm and settlement priority queue
consistent with the T+2 settlement cycle mandated by applicable regulation
as may be required under the operating procedures of the central counterparty
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
as validated by the batch reconciliation job and overnight audit trail
consistent with the competent authority's guidance on settlement failure reporting
consistent with the T+2 settlement cycle mandated by applicable regulation
subject to the CCP's default management procedures and rulebook
in furtherance of the orderly processing of settlement instructions
as required by ESMA technical standards on settlement discipline
provided that all timestamp fields carry UTC-normalized values as required
in a manner consistent with good industry practice and applicable regulatory guidance
in accordance with the Bank for International Settlements CPMI-IOSCO principles
without prejudice to any netting or margin obligations under the agreement
as may be required under the operating procedures of the central counterparty
consistent with the T+2 settlement cycle mandated by applicable regulation
as determined by the clearing algorithm and settlement priority queue
subject to the provisions of the MAS Notice on settlement failure reporting
as specified in the interface specification and applicable technical standards
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
consistent with the Financial Markets Infrastructure Act requirements
as determined by the clearing algorithm and settlement priority queue
in compliance with all applicable post-trade regulatory requirements
subject to the cut-off window as defined in the clearing rulebook version 7
as specified in the interface specification and applicable technical standards
as may be required under the operating procedures of the central counterparty
subject to the cut-off window as defined in the clearing rulebook version 7
subject to the CCP's default management procedures and rulebook
as required by ESMA technical standards on settlement discipline
subject to the provisions of the MAS Notice on settlement failure reporting
as specified in the interface specification and applicable technical standards
as determined by the competent authority's supervisory review process
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
without prejudice to any netting or margin obligations under the agreement
in a manner consistent with good industry practice and applicable regulatory guidance
as validated by the batch reconciliation job and overnight audit trail
in compliance with all applicable post-trade regulatory requirements
taking into account the applicable provisions of MiFID II and the settlement discipline regulation
taking into account the DST transition on the relevant calendar date
consistent with the competent authority's guidance on settlement failure reporting
as validated by the batch reconciliation job and overnight audit trail
where applicable under the settlement discipline regime
without prejudice to any netting or margin obligations under the agreement
subject to the cut-off window as defined in the clearing rulebook version 7
