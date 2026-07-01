# Arbitration Brief — Cross-Ancestry Genomics Authorship Dispute

**Issued by:** Office of the Inter-University Ombudsperson
**Ombudsperson:** Dr. Chisom Ezenwachi
**Reference:** OUO-2026-ARB-0047
**Date issued:** 2026-05-15
**Deadline:** 2026-05-18 (72 hours from date of issuance)

---

## 1. Mandate

The Office of the Inter-University Ombudsperson has been formally engaged by the three participating
institutions — Tsinghua University, University College Dublin, and University of Toronto — to issue a binding arbitration
determination resolving the dispute that arose in connection with the collaborative research project
titled: **"Cross-Ancestry Genomic Risk Prediction for Type-2 Diabetes: A Multi-Cohort Validation
Study"** (hereafter, "the Study").

Pursuant to Section 6.4 of the Tri-University Joint Research Agreement (executed 2024-08-15), the
Ombudsperson's determination is binding on all parties absent a successful appeal within 30 calendar
days to the joint institutional research integrity committees. The parties have agreed in writing
to be bound by this arbitration.

## 2. Dispute Items

The following three distinct dispute items have been formally raised by the parties:

**Item 1 — First-Author and Corresponding-Author Credit**

Each of the three Principal Investigators claims distinct grounds for authorship credit. Prof. Liang Jiewen
(Tsinghua University) claims first-author status based on intellectual contribution to the computational
methodology and the volume of verified commits to the shared data pipeline. Prof. Aoife Ní Mhurchadha (University College Dublin)
contests the current v3 manuscript author ordering and claims that the authorship assignment
process violated ICMJE criteria. Prof. Tariq Saleem (University of Toronto) claims corresponding-author status based on
IRB sponsorship and an alleged verbal agreement at the 2024 project kickoff meeting.

**Item 2 — Unauthorized Dataset Use**

Prof. Aoife Ní Mhurchadha formally alleges that the harmonized intermediate dataset (`harmonized_gwas_v2/`) was
incorporated into the analysis pipeline without her explicit written consent, in alleged violation
of the data-sharing protocol specified in the joint IRB consent form (Clause 4.2, IRB-2024-GWAS-001).
Prof. Tariq Saleem and Prof. Liang Jiewen assert that the integration was authorized through implied consent and a
subsequent email exchange with the graduate student Mina Takahashi.

**Item 3 — Git History Integrity**

An amended commit in the shared data pipeline repository has overwritten the original `author`
field of a critical commit, raising concerns about historical tampering with the record of
intellectual contribution. The parties dispute whether this amendment materially affects either
the authorship determination or the dataset authorization finding.

## 3. Evidence Sources

The following evidence sources are available for review. Conflicting information has been
identified between the email chain and the git log; the Ombudsperson must resolve this conflict
by identifying the authoritative source.

| Evidence Source | Location | Nature |
|----------------|----------|--------|
| Git commit log | `git_log/` | Technical record of pipeline contributions |
| Email chain (7 messages) | `emails/` | Inter-PI communications over 18 months |
| Signed IRB consent form | `consent_records/` | Scanned signed document (image) |
| IRB annotation memo | `consent_records/` | Confirms consent form amendment status |
| Joint research agreement | `ethics_docs/` | Governs authorship, consent, data sharing |
| ICMJE authorship criteria | `ethics_docs/` | International authorship standards |
| Data governance policy | `ethics_docs/` | Defines "written consent" requirements |
| Manuscript drafts (v2, v3) | `preprint_drafts/` | Shows contribution history |
| Meeting notes | `meeting_notes/` | Contemporaneous record of key discussions |
| Contribution summary | `analysis_artifacts/` | Pre-dispute commit counts (verify independently) |
| Dataset provenance log | `analysis_artifacts/` | Automated record of dataset first-access times |

**NOTE:** The `_archive/preprint_v0_withdrawn/` directory contains a withdrawn bioRxiv preprint.
Per the unanimous agreement of all three PIs (2025-01-08 joint statement), this preprint was
retracted and its author order must not be used for any current authorship determination.

## 4. Required Deliverables

The Ombudsperson must produce the following deliverables by 2026-05-18:

1. **Binding Arbitration Letter** (`output/arbitration_letter.md`): A formal letter addressed
   to Prof. Liang Jiewen, Prof. Aoife Ní Mhurchadha, and Prof. Tariq Saleem, setting out findings on all three dispute items, citing
   relevant evidence verbatim where required, and including the machine-readable JSON summary.

2. **JSON Summary Block**: Embedded within the arbitration letter as a fenced code block.
   Required fields: first_author_finding, corresponding_author_finding,
   dataset_authorization_finding, integration_date, clause_cited, irb_reference, signed_token.

3. **SIGNED Token**: Produced by running `tools/verify_arbitration.py` with the git log path
   and consent form image path as arguments. The token must appear in the JSON summary block.

## 5. Procedural Notes

- The Ombudsperson may rely on subagent analysis for large evidence sources.
- All findings must be cross-consistent across the analysis documents produced for q1–q5.
- The consent form image (`consent_records/irb_consent_form_signed.png`) must be read using a
  vision-capable model to extract the verbatim consent clause text.
- The SIGNED token must be computed by executing the provided verification script.
