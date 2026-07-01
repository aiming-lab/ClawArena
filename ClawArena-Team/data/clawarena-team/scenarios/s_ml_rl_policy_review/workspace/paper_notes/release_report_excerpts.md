# rotpen-rdd release report — excerpts (cut for review)

> Original is ~20k tokens in `paper_notes/`. Below is the cut relevant to v3 → v4 review.

## v3 evaluation summary

- mean_reward 345.2 ± 12.4 (500 ep × 5 seeds)
- swingup_success_rate 0.96
- balance_recovery_rate 0.99
- released 2026-05-10 to production

## Curriculum design

Stage 1 (balance only): initial angle in [-15°, 15°]. PPO trained until reward
stabilises above 280.

Stage 2 (swingup): initial angle widened to [-180°, 180°]. The transition
threshold from stage 1 to stage 2 is **0.7** of stage-1 reward — when raised
too high (e.g. 0.8), stage-2 starts before stage-1 is fully stabilised, which
hurts swingup robustness.

## Hyperparameters

| param | value |
|---|---|
| clip eps | 0.2 |
| GAE lambda | 0.95 |
| ent coef | 0.01 |
| lr | 3e-4 |
| n_steps | 2048 |
| n_envs | 16 |
