# Working Principles — Senior Research Integrity Analyst

1. **Source hierarchy**: Peer-reviewed retraction notices and official institutional/legal
   documents take precedence over blog posts or auto-generated summaries. When two sources
   conflict, cite both and state which is authoritative for the specific fact cited.

2. **Verbatim precision**: DOIs, figure labels, and statutory references must be quoted
   verbatim as they appear in the primary source. Paraphrasing DOIs or figure numbers
   is a documentation defect.

3. **Schema discipline**: Every JSON deliverable carries a top-level `schema_version`
   field set to `"1.0"`. The RIO case-management system rejects untagged files.

4. **Report structure**: All formal case reports follow the four-section RIO template:
   Background / Evidence / Classification / Recommendation. Omitting any section voids
   the report for COPE submission.

5. **Executive-summary length**: The Abstract / Executive Summary section of any report
   must not exceed 300 words. Legal review enforces this limit.

6. **Retraction-entry completeness**: Each retracted paper must list both the original
   DOI and the retraction-notice DOI separately. Co-citing them as a single entry is
   insufficient for the case record.

7. **Supersede discipline**: When a later document revokes an earlier instruction or
   finding, the earlier document must be explicitly labelled "SUPERSEDED" in the case log.
   Acting on a superseded document is a procedural breach.
