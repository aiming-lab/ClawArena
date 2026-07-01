# QA Alert — Contamination Check Complete

**From:** QA Lead (Ming Li)
**Date:** 2026-05-24
**Pipeline:** varcall-2026q2

## Summary

The contamination screening is complete for all 127 samples. Results are in
`reports/contamination_check.csv`.

## Key Finding

**9 samples** exceeded the 5% contamination threshold and are flagged as FAIL:

| Sample ID | Contamination % |
|---|---|
| SAMPLE-0041 | 7.2% |
| SAMPLE-0117 | 12.4% |
| SAMPLE-0203 | 9.8% |
| SAMPLE-0298 | 15.1% |
| SAMPLE-0361 | 6.3% |
| SAMPLE-0449 | 11.7% |
| SAMPLE-0512 | 8.5% |
| SAMPLE-0637 | 18.7% |
| SAMPLE-0759 | 5.8% |

These samples must be excluded from the rerun cohort.

**Note:** An automated pipeline summary was posted to `ai_summaries/pipeline_bot.md`
with an early estimate of 3 failed samples — that estimate was based on a
partial log scrape and is **incorrect**. Please use this QA alert and the
CSV file as the authoritative source.

## Recommendation

Proceed with `partial_rerun_excluding_failed` for the remaining 118 samples.

— Ming Li, QA Lead
