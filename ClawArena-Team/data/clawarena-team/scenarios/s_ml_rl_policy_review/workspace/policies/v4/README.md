# rotpen-rdd policy v4 (candidate)

Submitted: 2026-05-22 by Rosa Tang.

Diff against v3:

- New REWARD_WEIGHT_V4 = 1.5 in the swingup curriculum's last stage
- Curriculum stage threshold 0.7 → 0.8
- Otherwise identical hyperparameters

`policy_v4.zip.placeholder` stands in for the 18.7 MiB weights file. Real eval
ran the actual weights.

**Open questions for the reviewer**: does the swingup reward shaping create a
reward-hack incentive that explains the variance spike? See QA's report and
the v4_swingup_fail recording.
