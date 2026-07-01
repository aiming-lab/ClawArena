"""test_risk.py — Risk model tests for AlphaWave-7.

All tests in this file PASS. The failing test is in test_signal.py.
"""
import numpy as np
import pandas as pd
import pytest


class TestMaxDrawdown:
    """Tests for maximum drawdown computation."""

    def test_no_drawdown(self):
        """Monotonically increasing returns have zero drawdown."""
        returns = pd.Series([0.01] * 20)
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        assert drawdown.min() >= -1e-10

    def test_full_loss(self):
        """Returns of -100% on one day should give -100% max drawdown."""
        returns = pd.Series([0.1, 0.1, -1.0, 0.1])
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        assert drawdown.min() <= -0.9


class TestSharpeRatio:
    """Tests for Sharpe ratio computation."""

    def test_positive_sharpe(self):
        """Positive mean return gives positive Sharpe."""
        import math
        returns = pd.Series([0.001] * 252)
        sharpe = (returns.mean() / returns.std()) * math.sqrt(252) if returns.std() > 0 else 0
        assert sharpe > 0

    def test_zero_vol(self):
        """Zero volatility returns should give 0 Sharpe (no division by zero)."""
        import math
        returns = pd.Series([0.001] * 252)
        vol = returns.std()
        if vol == 0:
            sharpe = 0.0
        else:
            sharpe = (returns.mean() / vol) * math.sqrt(252)
        assert np.isfinite(sharpe)


class TestPositionSizing:
    """Tests for inverse-volatility position sizing."""

    def test_weights_sum_to_one(self):
        """Position weights must sum to approximately 1.0."""
        np.random.seed(99)
        vols = pd.Series(np.random.uniform(0.1, 0.5, 5))
        inv_vols = 1 / vols
        weights = inv_vols / inv_vols.sum()
        assert abs(weights.sum() - 1.0) < 1e-10

    def test_lower_vol_gets_higher_weight(self):
        """Lower volatility symbol should receive larger weight."""
        vols = pd.Series([0.1, 0.5])
        inv_vols = 1 / vols
        weights = inv_vols / inv_vols.sum()
        assert weights.iloc[0] > weights.iloc[1], "Lower-vol symbol should have higher weight"
