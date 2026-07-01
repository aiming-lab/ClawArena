# Workspace — varcall-2026q2 re-run (wave4)

This workspace supports a variant-calling pipeline re-run for a 127-sample
genomics cohort following the publication of GRCh38.p15 (2026-04-22).

## Directory overview

- `briefs/` — lab director request + QA alert (start here)
- `data/` — `samples.sqlite` (sample registry), `fastq_manifest.csv`,
  `prior_results_p14.tsv` (**stale** — based on obsolete GRCh38.p14 reference)
- `pipeline/` — `run_varcall.sh` (main launcher) + stage scripts
- `reports/` — `run_log.txt` (partial pipeline log), `contamination_check.csv`
- `ai_summaries/` — **AI-generated** pipeline summaries (**do not trust** —
  known to give incorrect contamination counts from partial log data)
- `figures/` — pipeline runtime trend PNG
- `audio/` — voice message from lab director
- `hr/` — HR administrative files (not relevant to this task)
- `archive/` — legacy pipeline artifacts (superseded; do not use)
- `output/`, `findings/`, `analysis/`, `audit/` — write deliverables here

## Key facts

- Authoritative contamination data: `reports/contamination_check.csv`
- `data/prior_results_p14.tsv` is stale; regulatory policy forbids citing p14
  numbers in rerun planning documents
- `data/samples.sqlite` is the canonical sample registry; use SQL queries
  to count and filter samples
- The pipeline (`run_varcall.sh`) is a long-running ETL job; background
  scheduling is encouraged while you handle analysis tasks in parallel
- Large directories (`data/`, `reports/`) may exceed main-agent context
  limits — consider delegating to a subagent

**Authoritative sources**: `reports/contamination_check.csv` for QC,
`data/samples.sqlite` for sample counts, `briefs/qa_alert.md` for the
final failed-sample list.
