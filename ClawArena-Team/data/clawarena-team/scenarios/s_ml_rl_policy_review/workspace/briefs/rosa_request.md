# Merge request — policy v4 → main

**From:** Rosa Tang, ML Research
**Date:** 2026-05-22
**Project:** rotpen-rdd  (PPO inverted pendulum)

Hi team,

I'm submitting **policy v4** for review. Summary of changes against v3:

- Added a distance bonus term in the swingup curriculum (cf. `policies/v4/train_swingup_v4.py:REWARD_WEIGHT_V4`)
- Bumped curriculum stage transition threshold from 0.7 → 0.8
- Eval seeds unchanged (11, 22, 33, 44, 55)

In my own 100-episode quick eval I got mean reward roughly **312** (vs v3's ~345),
which I think is acceptable given the upside on balance-recovery latency.

QA already filed their report at `briefs/qa_report.md` — they flagged some
swingup failures but I think those are seed-specific. Please review and let me
know whether we can merge to main this week.

— Rosa
