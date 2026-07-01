# BayLDA Supervisory Letter — DSAR Compliance Guidance

**Reference**: BayLDA-GS-2025-0042
**Date**: 2025-05-01
**Addressee**: Data Controllers Processing EU Personal Data (General Guidance)
**Subject**: Clarification of Art. 12(3) GDPR — Data Subject Access Request Response Deadlines

---

## 1. Summary of Guidance

The Bavarian State Office for Data Protection Supervision (Bayerisches Landesamt für
Datenschutzaufsicht, BayLDA) issues this guidance letter to clarify the correct calculation
of response deadlines for Data Subject Requests (DSRs) under Art. 12(3) GDPR.

**Key point**: The response deadline is **1 calendar month**, computed as exactly **30 calendar days**
from the date of receipt of the request. This calculation is not subject to internal
reinterpretation as a "business month", "extended complex request period", or any other
extended calculation.

---

## 2. Applicable Legal Framework

### Art. 12(3) GDPR (verbatim):

> "The controller shall provide information on action taken on a request under Articles 15
> to 22 to the data subject without undue delay and in any event within **one month** of
> receipt of the request."

> "That period may be extended by two further months where necessary, taking into account
> the complexity and number of the requests. The controller shall inform the data subject
> of any such extension within one month of receipt of the request, together with the
> reasons for the delay."

### Key clarifications:

1. **"One month" = 30 calendar days** from date of receipt. The calculation follows
   calendar days, not business days or working days.

2. **Extension conditions**: Extension of up to 2 further months is only permissible where:
   - The request is genuinely complex (e.g., involves multiple systems, requires extensive
     data compilation), OR
   - There are numerous simultaneous requests from the same data subject

3. **Extension notification**: If extending, the data subject must be informed **within the
   initial 1-month period** (30 days), stating the reasons for extension.

4. **No blanket extensions**: Extensions for categories of requests (e.g., "all AI-related
   requests" or "all requests involving system migrations") are NOT permissible. Each
   extension must be assessed on a case-by-case basis.

---

## 3. Common Compliance Errors

BayLDA has observed the following compliance errors in recent investigations:

### Error A: Incorrect deadline calculation

INCORRECT: Starting the 1-month clock from the date the DPO first reviews the request
(rather than the date of receipt by the organisation).

CORRECT: The clock starts from the date the request is **received** by any means
(email, post, online form, in-person). Acknowledgement of receipt does not restart the clock.

### Error B: Blanket extension policies

INCORRECT: Internal policy documents stating that "requests involving AI systems may be
extended by 3 months by default."

CORRECT: Each extension requires individual assessment of complexity and number, documented
per Art. 12(3), with notification to the data subject within the initial 30-day period.

### Error C: Business days vs calendar days

INCORRECT: Calculating "1 month" as 22 business days or excluding weekends and public holidays.

CORRECT: Calendar days including weekends and public holidays. The 30-day calculation is
a firm deadline.

---

## 4. VeritasCloud GmbH — Specific Guidance

BayLDA notes the following regarding VeritasCloud GmbH's DSAR practices:

1. The internal guidance document circulated by the CTO's office on DSAR timelines
   references a "3-month extension for AI-related complex requests." This interpretation
   is INCORRECT and SUPERSEDED by this letter.

2. All DSAR deadlines must be recalculated using exactly 30 calendar days from the
   receipt date. Historical and current overdue requests must be addressed immediately.

3. BayLDA expects a corrected DSAR compliance report to be provided within 30 days
   of this letter.

---

## 5. Enforcement Context

For reference, GDPR Art. 12-22 violations fall under Art. 83(5) (Tier 2), which provides
for fines of up to EUR 20,000,000 or 4% of total worldwide annual turnover, whichever
is higher.

Recent enforcement actions by EU DPAs regarding DSAR response delays:
- AEPD (Spain): EUR 200,000 fine for systematic DSAR response delays (2024)
- CNIL (France): EUR 150,000 fine for failure to respond to DSAR within deadline (2023)
- ICO (UK/post-Brexit): GBP 100,000 fine for ignoring DSAR entirely (2024)

---

## 6. Legal Memorandum — Supplementary Analysis

### 6.1 Case Law Analysis

The Court of Justice of the European Union (CJEU) has interpreted "one month" uniformly
across EU legislation as calendar months, consistent with the Brussels I Regulation
(Regulation (EU) 1215/2012) procedural calendar, which defines monthly time limits as
running to the same day of the following calendar month.

Example: Request received 2025-02-10 → deadline 2025-03-10 (same day, next calendar month),
not 2025-02-10 + 30 business days = 2025-04-01.

However, for operational clarity and to avoid disputes about "same day" calculations
(e.g., received January 31 → February 28/29?), BayLDA recommends the safe calculation:
**30 calendar days from receipt** (slightly more conservative than "same day next month"
for months with 31 days, but ensures compliance).

### 6.2 DSAR vs SAR (UK)

Note: The UK ICO uses "one calendar month" under the UK GDPR, which aligns with the
EU calculation. Post-Brexit UK DSAR handling is not within BayLDA's remit, but the
principle is consistent.

---

## Annex 1: Reference Case — DSAR Enforcement Action 001

**Case Reference**: EDPB-ENF-2024-0001
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 50,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-02. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 2: Reference Case — DSAR Enforcement Action 002

**Case Reference**: EDPB-ENF-2024-0002
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 100,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-03. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 3: Reference Case — DSAR Enforcement Action 003

**Case Reference**: EDPB-ENF-2024-0003
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 150,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-04. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 4: Reference Case — DSAR Enforcement Action 004

**Case Reference**: EDPB-ENF-2024-0004
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 200,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-05. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 5: Reference Case — DSAR Enforcement Action 005

**Case Reference**: EDPB-ENF-2024-0005
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 250,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-06. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 6: Reference Case — DSAR Enforcement Action 006

**Case Reference**: EDPB-ENF-2024-0006
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 300,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-07. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 7: Reference Case — DSAR Enforcement Action 007

**Case Reference**: EDPB-ENF-2024-0007
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 350,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-08. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 8: Reference Case — DSAR Enforcement Action 008

**Case Reference**: EDPB-ENF-2024-0008
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 400,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-09-09. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 9: Reference Case — DSAR Enforcement Action 009

**Case Reference**: EDPB-ENF-2024-0009
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 450,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-10-10. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 10: Reference Case — DSAR Enforcement Action 010

**Case Reference**: EDPB-ENF-2024-0010
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 500,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-11-11. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 11: Reference Case — DSAR Enforcement Action 011

**Case Reference**: EDPB-ENF-2024-0011
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 550,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-12-12. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 12: Reference Case — DSAR Enforcement Action 012

**Case Reference**: EDPB-ENF-2024-0012
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 600,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-01-13. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 13: Reference Case — DSAR Enforcement Action 013

**Case Reference**: EDPB-ENF-2024-0013
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 650,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-14. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 14: Reference Case — DSAR Enforcement Action 014

**Case Reference**: EDPB-ENF-2024-0014
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 700,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-15. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 15: Reference Case — DSAR Enforcement Action 015

**Case Reference**: EDPB-ENF-2024-0015
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 750,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-16. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 16: Reference Case — DSAR Enforcement Action 016

**Case Reference**: EDPB-ENF-2024-0016
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 800,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-17. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 17: Reference Case — DSAR Enforcement Action 017

**Case Reference**: EDPB-ENF-2024-0017
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 850,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-18. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 18: Reference Case — DSAR Enforcement Action 018

**Case Reference**: EDPB-ENF-2024-0018
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 900,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-19. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 19: Reference Case — DSAR Enforcement Action 019

**Case Reference**: EDPB-ENF-2024-0019
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 950,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-20. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 20: Reference Case — DSAR Enforcement Action 020

**Case Reference**: EDPB-ENF-2024-0020
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,000,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-09-21. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 21: Reference Case — DSAR Enforcement Action 021

**Case Reference**: EDPB-ENF-2024-0021
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,050,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-10-22. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 22: Reference Case — DSAR Enforcement Action 022

**Case Reference**: EDPB-ENF-2024-0022
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,100,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-11-23. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 23: Reference Case — DSAR Enforcement Action 023

**Case Reference**: EDPB-ENF-2024-0023
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,150,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-12-24. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 24: Reference Case — DSAR Enforcement Action 024

**Case Reference**: EDPB-ENF-2024-0024
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,200,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-01-25. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 25: Reference Case — DSAR Enforcement Action 025

**Case Reference**: EDPB-ENF-2024-0025
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,250,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-26. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 26: Reference Case — DSAR Enforcement Action 026

**Case Reference**: EDPB-ENF-2024-0026
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,300,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-27. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 27: Reference Case — DSAR Enforcement Action 027

**Case Reference**: EDPB-ENF-2024-0027
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,350,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-28. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 28: Reference Case — DSAR Enforcement Action 028

**Case Reference**: EDPB-ENF-2024-0028
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,400,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-01. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 29: Reference Case — DSAR Enforcement Action 029

**Case Reference**: EDPB-ENF-2024-0029
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,450,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-02. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 30: Reference Case — DSAR Enforcement Action 030

**Case Reference**: EDPB-ENF-2024-0030
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,500,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-03. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 31: Reference Case — DSAR Enforcement Action 031

**Case Reference**: EDPB-ENF-2024-0031
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,550,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-04. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 32: Reference Case — DSAR Enforcement Action 032

**Case Reference**: EDPB-ENF-2024-0032
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,600,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-09-05. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 33: Reference Case — DSAR Enforcement Action 033

**Case Reference**: EDPB-ENF-2024-0033
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,650,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-10-06. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 34: Reference Case — DSAR Enforcement Action 034

**Case Reference**: EDPB-ENF-2024-0034
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,700,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-11-07. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 35: Reference Case — DSAR Enforcement Action 035

**Case Reference**: EDPB-ENF-2024-0035
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,750,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-12-08. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 36: Reference Case — DSAR Enforcement Action 036

**Case Reference**: EDPB-ENF-2024-0036
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,800,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-01-09. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 37: Reference Case — DSAR Enforcement Action 037

**Case Reference**: EDPB-ENF-2024-0037
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,850,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-10. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 38: Reference Case — DSAR Enforcement Action 038

**Case Reference**: EDPB-ENF-2024-0038
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 1,900,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-11. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 39: Reference Case — DSAR Enforcement Action 039

**Case Reference**: EDPB-ENF-2024-0039
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 1,950,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-12. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 40: Reference Case — DSAR Enforcement Action 040

**Case Reference**: EDPB-ENF-2024-0040
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,000,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-13. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 41: Reference Case — DSAR Enforcement Action 041

**Case Reference**: EDPB-ENF-2024-0041
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,050,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-14. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 42: Reference Case — DSAR Enforcement Action 042

**Case Reference**: EDPB-ENF-2024-0042
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,100,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-15. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 43: Reference Case — DSAR Enforcement Action 043

**Case Reference**: EDPB-ENF-2024-0043
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,150,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-16. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 44: Reference Case — DSAR Enforcement Action 044

**Case Reference**: EDPB-ENF-2024-0044
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,200,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-09-17. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 45: Reference Case — DSAR Enforcement Action 045

**Case Reference**: EDPB-ENF-2024-0045
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,250,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-10-18. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 46: Reference Case — DSAR Enforcement Action 046

**Case Reference**: EDPB-ENF-2024-0046
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,300,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-11-19. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 47: Reference Case — DSAR Enforcement Action 047

**Case Reference**: EDPB-ENF-2024-0047
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,350,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-12-20. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 48: Reference Case — DSAR Enforcement Action 048

**Case Reference**: EDPB-ENF-2024-0048
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,400,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-01-21. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 49: Reference Case — DSAR Enforcement Action 049

**Case Reference**: EDPB-ENF-2024-0049
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,450,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-22. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 50: Reference Case — DSAR Enforcement Action 050

**Case Reference**: EDPB-ENF-2024-0050
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,500,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-23. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 51: Reference Case — DSAR Enforcement Action 051

**Case Reference**: EDPB-ENF-2024-0051
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,550,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-24. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 52: Reference Case — DSAR Enforcement Action 052

**Case Reference**: EDPB-ENF-2024-0052
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,600,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-25. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 53: Reference Case — DSAR Enforcement Action 053

**Case Reference**: EDPB-ENF-2024-0053
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,650,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-26. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 54: Reference Case — DSAR Enforcement Action 054

**Case Reference**: EDPB-ENF-2024-0054
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,700,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-27. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 55: Reference Case — DSAR Enforcement Action 055

**Case Reference**: EDPB-ENF-2024-0055
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,750,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-28. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 56: Reference Case — DSAR Enforcement Action 056

**Case Reference**: EDPB-ENF-2024-0056
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,800,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-09-01. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 57: Reference Case — DSAR Enforcement Action 057

**Case Reference**: EDPB-ENF-2024-0057
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,850,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-10-02. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 58: Reference Case — DSAR Enforcement Action 058

**Case Reference**: EDPB-ENF-2024-0058
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 2,900,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-11-03. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 59: Reference Case — DSAR Enforcement Action 059

**Case Reference**: EDPB-ENF-2024-0059
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 2,950,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-12-04. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 60: Reference Case — DSAR Enforcement Action 060

**Case Reference**: EDPB-ENF-2024-0060
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,000,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-01-05. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 61: Reference Case — DSAR Enforcement Action 061

**Case Reference**: EDPB-ENF-2024-0061
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,050,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-06. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 62: Reference Case — DSAR Enforcement Action 062

**Case Reference**: EDPB-ENF-2024-0062
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,100,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-07. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 63: Reference Case — DSAR Enforcement Action 063

**Case Reference**: EDPB-ENF-2024-0063
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,150,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-08. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 64: Reference Case — DSAR Enforcement Action 064

**Case Reference**: EDPB-ENF-2024-0064
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,200,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-09. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 65: Reference Case — DSAR Enforcement Action 065

**Case Reference**: EDPB-ENF-2024-0065
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,250,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-10. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 66: Reference Case — DSAR Enforcement Action 066

**Case Reference**: EDPB-ENF-2024-0066
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,300,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-11. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 67: Reference Case — DSAR Enforcement Action 067

**Case Reference**: EDPB-ENF-2024-0067
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,350,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-12. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 68: Reference Case — DSAR Enforcement Action 068

**Case Reference**: EDPB-ENF-2024-0068
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,400,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-09-13. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 69: Reference Case — DSAR Enforcement Action 069

**Case Reference**: EDPB-ENF-2024-0069
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,450,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-10-14. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 70: Reference Case — DSAR Enforcement Action 070

**Case Reference**: EDPB-ENF-2024-0070
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,500,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-11-15. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 71: Reference Case — DSAR Enforcement Action 071

**Case Reference**: EDPB-ENF-2024-0071
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,550,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-12-16. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 72: Reference Case — DSAR Enforcement Action 072

**Case Reference**: EDPB-ENF-2024-0072
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,600,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-01-17. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 73: Reference Case — DSAR Enforcement Action 073

**Case Reference**: EDPB-ENF-2024-0073
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,650,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-02-18. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 74: Reference Case — DSAR Enforcement Action 074

**Case Reference**: EDPB-ENF-2024-0074
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,700,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-03-19. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 75: Reference Case — DSAR Enforcement Action 075

**Case Reference**: EDPB-ENF-2024-0075
**DPA**: CNIL
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,750,000
**Violation Period**: 2024

**Facts**: Data subject submitted access request on
2024-04-20. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Systematic pattern.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 76: Reference Case — DSAR Enforcement Action 076

**Case Reference**: EDPB-ENF-2024-0076
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,800,000
**Violation Period**: 2023

**Facts**: Data subject submitted erasure request on
2024-05-21. Controller failed to respond within
30 calendar days deadline.
Extension was applied without case-by-case assessment.

**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 77: Reference Case — DSAR Enforcement Action 077

**Case Reference**: EDPB-ENF-2024-0077
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,850,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-06-22. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Identical fact pattern to current backlog.

## Annex 78: Reference Case — DSAR Enforcement Action 078

**Case Reference**: EDPB-ENF-2024-0078
**DPA**: AEPD
**Violation**: Art. 12(3) — DSAR response delay and incomplete response
**Fine Amount**: EUR 3,900,000
**Violation Period**: 2023

**Facts**: Data subject submitted access request on
2024-07-23. Controller failed to respond within
30 calendar days deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: Cooperation with DPA.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

## Annex 79: Reference Case — DSAR Enforcement Action 079

**Case Reference**: EDPB-ENF-2024-0079
**DPA**: BayLDA
**Violation**: Art. 12(3) — DSAR response delay or incomplete response
**Fine Amount**: EUR 3,950,000
**Violation Period**: 2024

**Facts**: Data subject submitted erasure request on
2024-08-24. Controller failed to respond within
1 calendar month deadline.


**DPA Finding**: Violation of Art. 12(3) confirmed. Controller could not demonstrate
individual assessment of complexity justifying extension.

**Mitigating factors**: None noted.
**Aggravating factors**: Organisational negligence.

**Corrective order**: Implement individualised DSAR tracking system; submit compliance
report within 30 days; train DPO and data subject rights team on Art. 12(3).

**Relevance to VeritasCloud**: Comparable violation type.

---

## 7. Contact Information

**BayLDA Supervisory Contact**:
Bayerisches Landesamt für Datenschutzaufsicht
Promenade 18, 91522 Ansbach
Tel: +49 (0)981 180093-0
Email: poststelle@lda.bayern.de
Web: www.lda.bayern.de

*This letter constitutes official guidance from BayLDA. Controllers must implement
the guidance within 30 days of receipt. Questions should be directed to the
BayLDA supervisory helpline.*

---

*BayLDA-GS-2025-0042 | 2025-05-01 | Official Supervisory Guidance*
