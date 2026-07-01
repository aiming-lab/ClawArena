# CISG Damages and Force Majeure Analysis
## Prepared by: TechCo Legal Team
## Sources: CISG-online.org (https://cisg-online.org/cisg-article-by-article/part-3/art.-74-cisg),
##           Wikipedia Hadley v Baxendale (https://en.wikipedia.org/wiki/Hadley_v_Baxendale)

---

## I. CISG Applicability to the VendorX MSA

### Background
VendorX Solutions Ltd. is incorporated in the Netherlands. The Netherlands is a CISG
Contracting State. TechCo is incorporated in the United States (Delaware), also a
Contracting State. Under CISG Article 1, the Convention applies to contracts of sale
of goods between parties whose places of business are in different Contracting States.

**Critical issue**: CISG applies primarily to sales of "goods". Whether SaaS software
services constitute "goods" under CISG is contested:
- Majority view: Pure service contracts are excluded from CISG.
- Minority view: Hybrid software/service contracts may be subject to CISG.

### MSA §12.3 CISG Exclusion
MSA v2.3 §12.3 explicitly excludes CISG: "The parties expressly agree to exclude the
application of the United Nations Convention on Contracts for the International Sale
of Goods (CISG) to this Agreement."

**Feishu Group Discussion Conflict (V1)**: There is a factual dispute in the Feishu
group about whether §12.3 effectively excludes CISG:
- Finance (Kevin): "CISG is excluded — §12.3 is clear."
- IT/Technical team: "The exclusion may not hold if VendorX argues the SaaS service
  is a 'sale of goods' under Netherlands law. CISG may still apply."
- Legal: "Standard practice is to include an explicit exclusion. §12.3 is valid.
  CISG is excluded."

**Legal team's authoritative position**: The §12.3 exclusion is valid and effective.
CISG does not apply to this Agreement. However, the analysis below is provided for
completeness in case CISG is later found applicable.

---

## II. CISG Article 74 — Damages

### Verbatim Text
"Damages for breach of contract by one party consist of a sum equal to the loss,
including loss of profit, suffered by the other party as a consequence of the breach.
Such damages may not exceed the loss which the party in breach foresaw or ought to
have foreseen at the time of the conclusion of the contract, in the light of the facts
and matters of which he then knew or ought to have known, as a possible consequence
of the breach of contract."

### Key Principles
1. **Full damages**: Including loss of profit (explicitly stated).
2. **Foreseeability cap**: Damages capped at what the breaching party "foresaw or ought
   to have foreseen at the time of the conclusion of the contract."
3. **Single provision**: Article 74 has no subsections — it is a single paragraph.

### Comparison with Hadley v Baxendale
The CISG Art.74 foreseeability cap mirrors the principle from Hadley v Baxendale
[1854] EWHC J70; 9 Exch 341, particularly Rule 2 (special consequential damages
known to both parties at contract formation).

---

## III. CISG Article 79 — Force Majeure / Exemption

### Key Elements Required

CISG Art.79 exempts a party from liability if it proves ALL of the following:
(a) **Impediment beyond control**: The failure was due to an impediment beyond the
    party's control; AND
(b) **Not reasonably foreseeable at conclusion**: The party could not reasonably be
    expected to have taken the impediment into account at the time of the conclusion
    of the contract; AND
(c) **Could not avoid or overcome**: The party could not avoid or overcome the
    impediment or its consequences.

### Notification Requirement
Under CISG Art.79(4), the exempted party must notify the other party of the impediment
and its effect on performance. Failure to notify results in liability for damages
resulting from non-receipt of notice.

---
*This memo is prepared for internal legal use only.*
