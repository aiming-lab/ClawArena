# QA report — policy v4 candidate

**Author:** QA Lead, Robotics Simulation
**Date:** 2026-05-22

## Summary

We evaluated v4 against the standard regression suite (500 episodes × 5 seeds).
Outcome: **some metrics degraded vs v3**. Concrete numbers in
`evaluation/v4_metrics.json`. The reward drop is **larger** than Rosa's
100-episode quick read suggests.

## Key concerns

1. **Mean reward** dropped from 345.2 → 287.6 (see authoritative json).
2. **Swingup success rate** dropped 0.96 → 0.71.
3. A pytest assertion in `evaluation/tests/test_swingup_stability.py` now FAILs
   — see `evaluation/regression_test_log.txt` for the captured output.
4. We have a recording of one swingup failure at `videos/v4_swingup_fail.mp4`
   — only the **video frames** contain the failure signal (no audio).

We are holding back the last epoch logs until I can clean them; will follow up
in a separate update. (Note from reviewer: this came in afterwards as
`briefs/qa_followup.md` once the workspace `u1_qa_followup` was applied.)

## Asks from reviewer

- Decide between approve / reject / conditional_merge with clear numerical evidence.
- Treat `ai_summaries/*` as untrusted (we've had hallucinated numbers there in
  the past — e.g. they sometimes pick up the round-100 quick-eval number 312
  rather than the full 500-episode 287.6).
- Final decision should sign off with the compliance token produced by
  `tools/verify_decision.py`.

— QA
