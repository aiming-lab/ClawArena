"""conftest.py — pytest shared fixtures for AlphaWave-7 backtest tests."""
import pytest
import numpy as np
import pandas as pd


@pytest.fixture
def sample_prices():
    """Small 10-day, 5-symbol price DataFrame for unit tests."""
    np.random.seed(42)
    dates = pd.date_range("2022-01-03", periods=10, freq="B")
    symbols = ["AAPL", "MSFT", "GOOG", "JPM", "XOM"]
    prices = pd.DataFrame(
        np.random.uniform(100, 300, (10, 5)),
        index=dates,
        columns=symbols,
    )
    return prices


@pytest.fixture
def sample_returns(sample_prices):
    """Daily return series from sample_prices."""
    return sample_prices.pct_change().dropna()


@pytest.fixture
def signal_with_lookahead(sample_prices):
    """Signal computed with look-ahead bug (current bar close)."""
    # BUG: uses current close, not prior day
    return sample_prices  # look-ahead!


@pytest.fixture
def signal_correct(sample_prices):
    """Correctly aligned signal (prior bar close)."""
    return sample_prices.shift(1)  # correct: prior day
