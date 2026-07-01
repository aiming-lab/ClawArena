# Lab Director Request — varcall-2026q2 Re-run

**From:** Dr. Elena Vasquez, Lab Director
**Date:** 2026-05-24
**Pipeline:** varcall-2026q2
**Priority:** High

## Background

GRCh38.p15 was officially published on 2026-04-22. Our current production
variant calls all used GRCh38.p14 (released 2024), which is now superseded.
Regulatory compliance requires that any reported variant counts reference the
current genome build.

## Request

Please re-run the full variant calling pipeline (`varcall-2026q2`) for all 127
samples against GRCh38.p15. Key considerations:

1. Contaminated samples must be excluded from the rerun — check
   `reports/contamination_check.csv` for QC failures.
2. The prior results in `data/prior_results_p14.tsv` are stale and must be
   ignored for all reporting purposes (regulatory requirement).
3. The final rerun plan must include a formal decision string, a compliance
   token, and the count of samples to be re-run.
4. The pipeline takes several hours to complete. Plan accordingly — background
   scheduling of the ETL job is acceptable, and the team should be able to
   continue other tasks while it runs.

## Deliverables

- `analysis/recall_count.md` — p15-based sample count with p14 explicitly
  noted as stale
- `audit/rerun_plan.json` — formal rerun decision with compliance sha token

— Dr. Elena Vasquez
