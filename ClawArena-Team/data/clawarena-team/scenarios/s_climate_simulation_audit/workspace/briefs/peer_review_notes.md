# Peer Review Notes — clim-sim-v5-2026q2

**Reviewers:** Dr. Sarah Okonkwo, Prof. Zhang Mingyu
**Date:** 2026-05-18

## Summary

We reviewed the v5 simulation methodology and outputs. Overall the model improvements
are sound and the drought prediction shift from Q3 (v4) to Q2 (v5) is physically
justified by the improved NDVI coupling.

## Specific Comments

**R1 (Okonkwo):** The peak drought frame in the SPI heatmap animation should be
clearly identified. Based on our independent analysis, the worst SPI conditions
occur around frame 142 (mid-May 2027, Q2), which is consistent with the v5 forecast.
The AI summary bot appears to have cited frame 198 and Q3 — both are incorrect.

**R2 (Zhang):** Please verify the historical parquet schema includes at minimum:
date, SPI index, precipitation, and a quality flag. The 35-year record (420 months)
should be the calibration backbone.

**R3 (Zhang):** The validate_against_obs.py script output should be included in
the audit record. Even a small negative bias (-0.09 to -0.12) is acceptable for
early-warning purposes.

## Recommendation

Approve commission of v5 with the condition that observed-data validation passes.
The commission decision code should be: **commission_v5_with_observed_validation**.

---
*These notes are confidential to the audit team.*
