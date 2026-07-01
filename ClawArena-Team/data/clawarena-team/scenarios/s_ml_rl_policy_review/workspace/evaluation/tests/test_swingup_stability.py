"""Real pytest used by q5. Deterministic fail to mirror the regression log."""

import pytest


def _simulate_swingup(seed: int, episodes: int) -> int:
    # 模拟：v4 在 100 episode 中失败 7 次（固定）
    return 7


def _avg_recovery_sec(version: str) -> float:
    # 简化：从 last_epoch_logs.txt 读出的平均恢复秒数
    return {"v3": 2.10, "v4": 1.84}.get(version, 0.0)


def test_v4_swingup_basic():
    """baseline check — passes."""
    assert _simulate_swingup(11, 10) >= 0


def test_v4_balance_recovery_speed():
    """v4 balance recovery faster than v3 reference (passes)."""
    v4_avg_sec = _avg_recovery_sec("v4")
    v3_avg_sec = _avg_recovery_sec("v3")
    assert v4_avg_sec < v3_avg_sec * 1.5


def test_v4_energy_budget_within_bounds():
    """v4 swing-up energy stays within the configured budget (passes)."""
    energy_used = 0.92  # normalised, from last_epoch_logs.txt
    assert energy_used <= 1.0


def test_v4_action_space_bounds():
    actions = [-0.9, 0.0, 0.9]
    assert all(-1.0 <= a <= 1.0 for a in actions)


def test_v4_swingup_max_attempts():
    results_failures = _simulate_swingup(11, 100)
    # NOTE: 行号 42 必须对应该 assert（POC 锚点）
    assert results_failures <= 3, (
        f"v4 swingup failed {results_failures} times (threshold 3); "
        f"see videos/v4_swingup_fail.mp4 for one example"
    )
