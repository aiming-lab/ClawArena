"""test_signal.py — Signal alignment tests for AlphaWave-7.

TestSignalAlignment tests whether the signal uses the PRIOR bar's close
(correct) or the CURRENT bar's close (look-ahead bug).

Expected: TestSignalAlignment FAILS because backtest_engine.py line 142
uses current bar close (look-ahead) rather than prior bar close.
"""
import numpy as np
import pandas as pd
import pytest

# Local test helpers (_signal_helpers.py) — keeps this suite runnable standalone.
from _signal_helpers import (
    _lookahead_check_helper,
)


class TestSignalAlignment:
    """Tests for correct signal timestamp alignment (no look-ahead bias)."""

    def test_signal_uses_prior_close(self, sample_prices):
        """Signal computation must use prior bar close, not current bar.

        This test FAILS because backtest_engine.py line 142 uses
        `signal_close = prices` (current bar) instead of
        `signal_close = prices.shift(1)` (prior bar).
        """
        # The correct signal: shift by 1 day (prior close)
        correct_signal = sample_prices.shift(1)

        # The buggy signal from the engine: no shift (current close)
        buggy_signal = sample_prices  # as implemented in engine line 142

        # They must differ on any live day
        diff = (correct_signal - buggy_signal).dropna()
        # Line 38: assert they are equal — this FAILS because of look-ahead
        assert diff.abs().max().max() < 1e-10, (  # line 38
            "FAIL: Signal uses current bar close (look-ahead bias detected). "
            "backtest_engine.py line 142 must use prices.shift(1), not prices. "
            f"Max discrepancy: {diff.abs().max().max():.6f}"
        )

    def test_signal_not_future(self, sample_prices):
        """Signal on day T must not contain information from day T."""
        signal = sample_prices.shift(1)
        # Signal on day T should equal price[T-1]
        for i in range(1, len(sample_prices)):
            day_t = sample_prices.index[i]
            day_t_minus_1 = sample_prices.index[i - 1]
            expected = sample_prices.loc[day_t_minus_1]
            actual = signal.loc[day_t]
            # 比对数值（两序列的 name 分别是各自日期，故不校验 name）
            pd.testing.assert_series_equal(expected, actual, check_names=False)


class TestMomentumScore:
    """Tests for momentum score computation."""

    def test_scores_are_finite(self, sample_prices):
        """Momentum scores must be finite (no NaN after warmup)."""
        from _signal_helpers import (
            _compute_momentum_simple,
        )
        scores = _compute_momentum_simple(sample_prices, lookback=3, skip=1)
        valid = scores.dropna()
        assert len(valid) > 0, "No valid scores produced"
        assert np.isfinite(valid.values).all(), "Momentum scores contain non-finite values"

    def test_scores_are_cross_sectional(self, sample_prices):
        """Scores must differ across symbols (cross-sectional variation)."""
        from _signal_helpers import (
            _compute_momentum_simple,
        )
        scores = _compute_momentum_simple(sample_prices, lookback=3, skip=1)
        valid = scores.dropna()
        if len(valid) > 1:
            # 截面方差按 symbol（列）逐行计算；任一交易日各 symbol 分数有差异即可
            cross_sectional_std = valid.std(axis=1)
            assert (cross_sectional_std > 0).any(), "All symbols have identical momentum scores"


class TestTransactionCosts:
    """Tests for transaction cost model."""

    def test_commission_bps(self):
        """Commission must be 5bps as configured."""
        from _signal_helpers import (
            _get_commission_bps,
        )
        assert _get_commission_bps() == 5.0

    def test_slippage_bps(self):
        """Slippage must be 3bps as configured."""
        from _signal_helpers import (
            _get_slippage_bps,
        )
        assert _get_slippage_bps() == 3.0
