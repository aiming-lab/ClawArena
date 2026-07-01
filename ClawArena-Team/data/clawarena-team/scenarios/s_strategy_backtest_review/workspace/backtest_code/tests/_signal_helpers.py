"""_signal_helpers.py — local test helpers for the AlphaWave-7 backtest suite.

Small pure-pandas helpers used by test_signal.py (signal alignment / momentum /
transaction-cost unit tests). Kept local to the test package so the suite runs
standalone from the workspace sandbox.
"""
from __future__ import annotations


def _lookahead_check_helper(prices, use_lookahead: bool = True):
    """Return signal with or without look-ahead bias."""
    if use_lookahead:
        return prices              # current bar (look-ahead)
    return prices.shift(1)         # prior bar (correct)


def _compute_momentum_simple(prices, lookback: int = 252, skip: int = 21):
    """Simple 12-1 style momentum score."""
    return prices.shift(skip) / prices.shift(lookback) - 1


def _get_commission_bps() -> float:
    return 5.0


def _get_slippage_bps() -> float:
    return 3.0
