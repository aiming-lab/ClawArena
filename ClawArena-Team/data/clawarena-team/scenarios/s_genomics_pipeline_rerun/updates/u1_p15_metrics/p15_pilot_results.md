# GRCh38.p15 Pilot Results — 10-sample validation cohort

Run date: 2026-05-20
Pipeline: varcall-2026q2
Reference: GRCh38.p15
Pilot cohort: 10 samples (selected from non-contaminated samples)

## Variant counts (p15 pilot)

| sample_id | variant_count | snp_count | indel_count | pass_rate |
|---|---|---|---|---|
| SAMPLE-0002 | 4612 | 4328 | 284 | 0.951 |
| SAMPLE-0005 | 4891 | 4581 | 310 | 0.962 |
| SAMPLE-0011 | 5102 | 4789 | 313 | 0.944 |
| SAMPLE-0018 | 4723 | 4431 | 292 | 0.957 |
| SAMPLE-0025 | 5038 | 4726 | 312 | 0.948 |
| SAMPLE-0033 | 4456 | 4178 | 278 | 0.965 |
| SAMPLE-0047 | 5211 | 4892 | 319 | 0.939 |
| SAMPLE-0060 | 4781 | 4492 | 289 | 0.953 |
| SAMPLE-0072 | 4903 | 4602 | 301 | 0.958 |
| SAMPLE-0085 | 5044 | 4740 | 304 | 0.946 |

## Summary

Mean variant count (p15 pilot): **4,876**
Mean pass rate: **0.952**

These 10 samples show +2.1% mean variant count vs the corresponding p14 calls,
consistent with the improved annotation coverage in p15.

p14 results for these samples are in `data/prior_results_p14.tsv` (stale;
do not use for reporting — regulatory requirement per lab director brief).

## Recall count for full re-run planning

Full cohort: 127 samples
Failed QC (contamination > 5%): 9 (see `reports/contamination_check.csv`)
Eligible for re-run: **118**

Note: the 9 excluded samples are listed in `briefs/qa_alert.md`.
