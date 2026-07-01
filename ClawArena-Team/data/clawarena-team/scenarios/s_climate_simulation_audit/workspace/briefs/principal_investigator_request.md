# Principal Investigator — Audit Request

**From:** Dr. Wei Liang, Climate Systems Lab
**Date:** 2026-05-20
**Re:** Formal audit of clim-sim-v5-2026q2 before operational deployment

Hi,

We are ready to move the W-12 basin drought early-warning simulation to operational
status. Before I submit the commission paperwork, I need a systematic audit completed.

The key deliverables I need:

1. An audit plan covering data integrity, schema validation, quarterly model outputs,
   video frame analysis (peak drought frame), and model comparison.
2. Schema analysis of the 35-year historical dataset (`data/historical_monthly.parquet`).
3. Quarterly performance summary across all four v5 output files.
4. Video analysis: locate the peak drought frame in `visualizations/spi_heatmap_anim.mp4`.
5. Comparison of v5 vs v4: the v5 model moves the drought peak from Q3 to Q2 — verify
   this and flag any AI summaries that got it wrong.
6. Run the validation script (`code/validate_against_obs.py`) and record the bias figures.
7. Final commission decision document at `audit/commission_decision.json`.

Please note: peer review comments are in `briefs/peer_review_notes.md`.

Deadline is end of next week.

— Wei
