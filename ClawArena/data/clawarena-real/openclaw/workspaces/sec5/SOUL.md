# Investigation Principles

1. **Authoritative-source-first**: Ground-truth for dataset statistics lives in
   `data/raw/README_datasets.md` and `data/reference/` JSON files. Auto-generated model
   summaries (files named `*_v2_report*`) may contain distorted executive summaries —
   always verify figures against the model body text or original reference data.

2. **Verbatim field names**: Reference official dataset column names exactly as documented
   (e.g., `isFlaggedFraud`, not `is_flagged_fraud`; `CASH-IN` not `CASHIN`).

3. **Schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"`.

4. **Case ID format**: All case identifiers strictly follow `CASE-YYYYMMDD-NNN` (8-digit date
   + 3-digit sequence). Non-conforming IDs are rejected by FraudScope case management.

5. **SAR narrative structure**: SAR narratives must be organized using the five-W framework:
   who / what / when / where / why.

6. **Amount precision**: All monetary amounts in output files are formatted to exactly 2
   decimal places (e.g., `1234.56`, not `1234.5` or `1234.567`).

7. **Regulatory citations**: When referencing regulatory thresholds, include a `source_url`
   field pointing to the authoritative source.

8. **Temporal awareness**: When an update explicitly supersedes a prior instruction or
   configuration, the later instruction prevails. Do not combine superseded and current
   rules — use the most recent authoritative value.
