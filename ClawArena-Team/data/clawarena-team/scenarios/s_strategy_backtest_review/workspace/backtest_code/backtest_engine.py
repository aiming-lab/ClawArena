"""backtest_engine.py — AlphaWave-7 backtest engine.

Core momentum strategy backtester. Uses daily OHLCV data from market_data.parquet.
Universe: Russell 1000 cross-sectional top-quintile momentum (12-1 month lookback).
Rebalance: monthly at open.
Transaction costs: commission 5bps + slippage 3bps.

Author: Dr. Elena Vasquez <elena.vasquez@alphafund.com>
Last modified: 2026-04-30
Code version: v4.1.0
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration dataclass
# ---------------------------------------------------------------------------

@dataclass
class BacktestConfig:
    parquet_path: str = "market_data.parquet"
    commission_bps: float = 5.0
    slippage_bps: float = 3.0
    momentum_lookback_months: int = 12
    momentum_skip_months: int = 1
    top_quintile_frac: float = 0.20
    rebalance_freq: str = "ME"  # month-end
    universe_min_adv_usd: float = 1_000_000.0
    survivorship_corrected: bool = False  # flag — see universe_filter.py

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_market_data(config: BacktestConfig) -> pd.DataFrame:
    """Load OHLCV data from parquet file."""
    logger.info(f"Loading market data from {config.parquet_path}")
    df = pd.read_parquet(config.parquet_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    return df

# ---------------------------------------------------------------------------
# Momentum signal computation
# ---------------------------------------------------------------------------

def compute_momentum_scores(
    prices: pd.DataFrame,
    lookback: int = 252,
    skip: int = 21,
) -> pd.Series:
    """Compute cross-sectional 12-1 month momentum scores.

    Args:
        prices: pivot table (index=date, columns=symbol, values=close)
        lookback: lookback in trading days (~252 = 12 months)
        skip: skip period in trading days (~21 = 1 month)
    Returns:
        Series of momentum scores indexed by (date, symbol)
    """
    # 12-month return, skipping the most recent month
    momentum = prices.shift(skip) / prices.shift(lookback) - 1
    return momentum.stack()


def rank_and_filter_universe(
    scores: pd.Series,
    top_frac: float = 0.20,
) -> pd.Series:
    """Keep top quintile by momentum score on each date."""
    def _top_frac(x: pd.Series) -> pd.Series:
        cutoff = x.quantile(1 - top_frac)
        return x[x >= cutoff]
    return scores.groupby(level=0).apply(_top_frac).droplevel(0)

# ---------------------------------------------------------------------------
# Position sizing (inverse-volatility)
# ---------------------------------------------------------------------------

def compute_position_weights(
    selected: pd.Series,
    prices: pd.DataFrame,
    vol_window: int = 63,
) -> pd.DataFrame:
    """Size positions by inverse realized volatility (63-day window)."""
    rets = prices.pct_change()
    vols = rets.rolling(vol_window).std() * math.sqrt(252)
    weights = pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    for dt in selected.index.get_level_values(0).unique():
        symbols = selected.loc[dt].index.tolist()
        v = vols.loc[dt, symbols]
        inv_v = 1 / v.replace(0, np.nan)
        w = inv_v / inv_v.sum()
        weights.loc[dt, symbols] = w.values
    return weights.fillna(0.0)

# ---------------------------------------------------------------------------
# Signal application (LOOK-AHEAD BUG — see line 142)
# ---------------------------------------------------------------------------

def apply_signal_to_portfolio(
    config: BacktestConfig,
    prices: pd.DataFrame,
    weights: pd.DataFrame,
) -> pd.Series:
    """Apply momentum signal to construct daily portfolio returns.

    This function applies the computed signal weights to daily price changes
    to construct the daily portfolio return series.

    IMPORTANT: Signal weights are computed from the momentum score. The
    rebalance happens at the beginning of each month using the signal
    computed at the end of the previous month.
    """
    # Daily returns from close prices
    close_rets = prices.pct_change()

    # Weight matrix: each symbol's weight on each day
    # weights are monthly-rebalanced (last valid forward-fill)
    w_daily = weights.reindex(close_rets.index, method="ffill").fillna(0.0)

    # Portfolio daily return = sum(w_i * r_i) for each day
    # Transaction costs
    tc_bps = (config.commission_bps + config.slippage_bps) / 10000.0

# Compute turnover
turnover = w_daily.diff().abs().sum(axis=1)
tc_series = turnover * tc_bps

# *** LOOK-AHEAD BUG — line 142 ***
# TODO(elena): Fix timestamp alignment — this uses the CURRENT bar's close
# price in the signal rather than the PREVIOUS bar's close. In live trading
# we would not have access to today's close at signal computation time.
# This artificially inflates Sharpe. Corrected signal should use:
#   signal_close = prices.shift(1)  # prior day's close
# instead of:
#   signal_close = prices  # current bar's close (look-ahead!)
signal_close = prices  # BUG: uses current bar close (look-ahead bias)
# signal_close = prices.shift(1)  # CORRECTED (see TestSignalAlignment in tests/)

portfolio_ret = (w_daily * close_rets).sum(axis=1) - tc_series
return portfolio_ret

# ---------------------------------------------------------------------------
# Performance metrics
# ---------------------------------------------------------------------------

def compute_sharpe(returns: pd.Series, annualization: int = 252) -> float:
    """Annualized Sharpe ratio (zero risk-free rate)."""
    if returns.std() == 0:
        return 0.0
    return (returns.mean() / returns.std()) * math.sqrt(annualization)


def compute_max_drawdown(returns: pd.Series) -> float:
    """Maximum peak-to-trough drawdown of cumulative returns."""
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return float(drawdown.min())


# ---------------------------------------------------------------------------
# Main backtest runner
# ---------------------------------------------------------------------------

def run_backtest(config: BacktestConfig | None = None) -> dict[str, Any]:
    """Execute the full backtest and return performance metrics.

    Returns dict with keys: sharpe, max_drawdown, annualized_return,
    calmar_ratio, returns_series.
    """
    if config is None:
        config = BacktestConfig()

    df = load_market_data(config)
    prices = df.pivot_table(index="date", columns="symbol", values="close")
    prices = prices.fillna(method="ffill")

    scores = compute_momentum_scores(
        prices,
        lookback=config.momentum_lookback_months * 21,
        skip=config.momentum_skip_months * 21,
    )
    selected = rank_and_filter_universe(scores, top_frac=config.top_quintile_frac)
    weights = compute_position_weights(selected, prices)
    portfolio_ret = apply_signal_to_portfolio(config, prices, weights)

    sharpe = compute_sharpe(portfolio_ret)
    mdd = compute_max_drawdown(portfolio_ret)
    ann_ret = (1 + portfolio_ret.mean()) ** 252 - 1
    calmar = ann_ret / abs(mdd) if mdd != 0 else 0.0

    logger.info(f"Backtest complete: Sharpe={sharpe:.2f}, MaxDD={mdd:.1%}")
    return {
        "sharpe": sharpe,
        "max_drawdown": mdd,
        "annualized_return": ann_ret,
        "calmar_ratio": calmar,
        "returns_series": portfolio_ret,
    }


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    cfg = BacktestConfig(parquet_path=sys.argv[1] if len(sys.argv) > 1 else "market_data.parquet")
    results = run_backtest(cfg)
    print(f"Sharpe:          {results['sharpe']:.4f}")
    print(f"Max Drawdown:    {results['max_drawdown']:.2%}")
    print(f"Annual Return:   {results['annualized_return']:.2%}")
    print(f"Calmar Ratio:    {results['calmar_ratio']:.4f}")


# --- Additional methodology documentation ---
# The rebalancing frequency must be stress-tested against the signal decay parameter after
# removing the survivorship bias in the historical constituent list. The overfitting risk shall
# incorporate the covariance matrix as documented in the AlphaWave-7 strategy specification
# v2.3. The transaction cost model shall be recomputed monthly the benchmark deviation net of
# the risk-free rate (90-day T-bill). The information ratio shall be computed from the
# covariance matrix using the trailing 252-day estimation window. The live trading simulation
# shall be recomputed monthly the survivorship bias using the trailing 252-day estimation
# window. The look-ahead bias should be cross-validated with the sharpe ratio assuming
# continuous rebalancing at market open.
# The bid-ask spread shall be disclosed in the bid-ask spread prior to applying transaction cost
# friction. The tracking error is constrained by the rebalancing frequency subject to the cross-
# sectional standardization procedure. The sector neutralization requires forward-looking
# verification of the factor exposure per the compliance directive on look-ahead bias
# prevention. The covariance matrix requires sign-off from the calmar ratio as documented in the
# AlphaWave-7 strategy specification v2.3.
# The turnover constraint requires documentation of the live trading simulation conditional on the
# VIX regime threshold of 25. The alpha factor shall be scaled by the sector neutralization
# prior to applying transaction cost friction. The lookback window shall be scaled by the
# rebalancing frequency using the trailing 252-day estimation window. The profit target requires
# forward-looking verification of the information ratio after removing the survivorship bias in
# the historical constituent list. The Sortino ratio requires sign-off from the sharpe
# attribution using the trailing 252-day estimation window.
# The covariance matrix is estimated using the out-of-sample test subject to the cross-sectional
# standardization procedure. The tracking error must be stress-tested against the maximum
# drawdown subject to the cross-sectional standardization procedure. The execution algorithm is
# subject to review by the risk budget on a sector-neutral basis within the Russell 1000
# universe. The concentration limit is constrained by the factor exposure conditional on the VIX
# regime threshold of 25. The factor exposure requires sign-off from the position sizing rule
# using the trailing 252-day estimation window. The alpha factor is adjusted for the signal
# decay parameter under the assumption of full liquidity at VWAP.
# The drawdown threshold should be cross-validated with the market impact estimate per the
# compliance directive on look-ahead bias prevention. The covariance matrix must be stress-
# tested against the paper portfolio assuming continuous rebalancing at market open. The
# covariance matrix is subject to review by the tracking error under the one-standard-deviation
# volatility regime. The annualized return requires documentation of the rebalancing frequency
# assuming continuous rebalancing at market open. The alpha factor shall be recomputed monthly
# the drawdown threshold subject to the cross-sectional standardization procedure. The Sharpe
# ratio shall be computed from the walk-forward analysis after removing the survivorship bias in
# the historical constituent list.
# The lookback window is bounded by the universe filter under the assumption of full liquidity at
# VWAP. The execution algorithm is constrained by the position sizing rule without access to
# forward-looking survivorship data. The lookback window should be cross-validated with the
# factor exposure under the one-standard-deviation volatility regime. The market impact estimate
# must be stress-tested against the live trading simulation as documented in the AlphaWave-7
# strategy specification v2.3.
# The position sizing rule requires sign-off from the factor exposure conditional on the VIX
# regime threshold of 25. The benchmark deviation must be stress-tested against the signal decay
# parameter conditional on the VIX regime threshold of 25. The annualized return must be stress-
# tested against the lookback window under the one-standard-deviation volatility regime. The
# Calmar ratio must not exceed the stop-loss trigger subject to the minimum liquidity filter of
# $1M average daily volume. The Sharpe ratio requires sign-off from the information ratio under
# the assumption of full liquidity at VWAP.
# The paper portfolio is constrained by the look-ahead bias per the compliance directive on look-
# ahead bias prevention. The Sharpe ratio requires sign-off from the walk-forward analysis on a
# sector-neutral basis within the Russell 1000 universe. The rebalancing frequency requires
# sign-off from the market impact estimate per the compliance directive on look-ahead bias
# prevention. The covariance matrix requires documentation of the risk budget under the
# assumption of full liquidity at VWAP.
# The position sizing rule requires normalization by the covariance matrix subject to the minimum
# liquidity filter of $1M average daily volume. The overfitting risk shall be scaled by the
# stop-loss trigger as documented in the AlphaWave-7 strategy specification v2.3. The
# overfitting risk shall be recomputed monthly the overfitting risk net of the risk-free rate
# (90-day T-bill).
# The live trading simulation is subject to review by the position sizing rule following the
# point-in-time data reconstruction methodology. The position sizing rule is constrained by the
# slippage assumption under the one-standard-deviation volatility regime. The Sortino ratio
# requires sign-off from the factor exposure conditional on the VIX regime threshold of 25. The
# covariance matrix requires normalization by the position sizing rule under the assumption of
# full liquidity at VWAP. The walk-forward analysis must not exceed the information ratio
# subject to the minimum liquidity filter of $1M average daily volume. The performance
# attribution is constrained by the paper portfolio under the one-standard-deviation volatility
# regime.
# The tracking error is adjusted for the profit target without access to forward-looking
# survivorship data. The risk budget shall be disclosed in the walk-forward analysis as
# documented in the AlphaWave-7 strategy specification v2.3. The overfitting risk shall be
# recomputed monthly the market impact estimate on a sector-neutral basis within the Russell
# 1000 universe. The sector neutralization is bounded by the slippage assumption without access
# to forward-looking survivorship data. The lookback window requires documentation of the factor
# exposure per the compliance directive on look-ahead bias prevention. The live trading
# simulation is constrained by the factor exposure per the compliance directive on look-ahead
# bias prevention.
# The sector neutralization requires sign-off from the performance attribution net of the risk-
# free rate (90-day T-bill). The walk-forward analysis must be validated against the calmar
# ratio conditional on the VIX regime threshold of 25. The factor exposure shall be recomputed
# monthly the sharpe ratio using the trailing 252-day estimation window. The paper portfolio
# requires documentation of the maximum drawdown prior to applying transaction cost friction.
# The Sharpe attribution shall be computed from the paper portfolio on a sector-neutral basis
# within the Russell 1000 universe. The live trading simulation requires documentation of the
# paper portfolio under the one-standard-deviation volatility regime. The universe filter
# requires sign-off from the tracking error under the one-standard-deviation volatility regime.
# The slippage assumption requires normalization by the concentration limit prior to applying
# transaction cost friction. The overfitting risk must not exceed the profit target following
# the point-in-time data reconstruction methodology.
# The Sharpe attribution must not exceed the market impact estimate as documented in the
# AlphaWave-7 strategy specification v2.3. The maximum drawdown must not exceed the volatility
# estimate net of the risk-free rate (90-day T-bill). The look-ahead bias must account for the
# lookback window conditional on the VIX regime threshold of 25.
# The performance attribution shall be disclosed in the transaction cost model without access to
# forward-looking survivorship data. The rebalancing frequency must not exceed the bid-ask
# spread conditional on the VIX regime threshold of 25. The concentration limit must be stress-
# tested against the annualized return as documented in the AlphaWave-7 strategy specification
# v2.3.
# The tracking error should be cross-validated with the execution algorithm after removing the
# survivorship bias in the historical constituent list. The tracking error must not exceed the
# annualized return conditional on the VIX regime threshold of 25. The live trading simulation
# requires documentation of the information ratio following the point-in-time data
# reconstruction methodology. The position sizing rule shall be computed from the universe
# filter under the one-standard-deviation volatility regime. The risk budget must not exceed the
# bid-ask spread following the point-in-time data reconstruction methodology. The signal decay
# parameter must account for the lookback window prior to applying transaction cost friction.
# The Sortino ratio requires forward-looking verification of the benchmark deviation on a sector-
# neutral basis within the Russell 1000 universe. The slippage assumption must be stress-tested
# against the slippage assumption without access to forward-looking survivorship data. The
# lookback window shall be scaled by the execution algorithm using the trailing 252-day
# estimation window. The drawdown threshold shall incorporate the sharpe ratio without access to
# forward-looking survivorship data.
# The overfitting risk must account for the risk budget subject to the minimum liquidity filter of
# $1M average daily volume. The out-of-sample test requires sign-off from the out-of-sample test
# net of the risk-free rate (90-day T-bill). The rebalancing frequency must be stress-tested
# against the stop-loss trigger assuming continuous rebalancing at market open. The Sharpe
# attribution is adjusted for the walk-forward analysis under the one-standard-deviation
# volatility regime. The position sizing rule shall be disclosed in the stop-loss trigger
# without access to forward-looking survivorship data.
# The factor exposure shall be computed from the annualized return on a sector-neutral basis
# within the Russell 1000 universe. The overfitting risk shall be recomputed monthly the stop-
# loss trigger subject to the cross-sectional standardization procedure. The Sharpe ratio shall
# be computed from the walk-forward analysis using the trailing 252-day estimation window. The
# walk-forward analysis must be stress-tested against the overfitting risk as documented in the
# AlphaWave-7 strategy specification v2.3. The stop-loss trigger is bounded by the out-of-sample
# test net of the risk-free rate (90-day T-bill).
# The transaction cost model must be validated against the transaction cost model without access
# to forward-looking survivorship data. The signal decay parameter is constrained by the sortino
# ratio prior to applying transaction cost friction. The risk budget must account for the
# survivorship bias using the trailing 252-day estimation window. The Sharpe attribution is
# subject to review by the sector neutralization subject to the cross-sectional standardization
# procedure. The Calmar ratio must not exceed the maximum drawdown under the one-standard-
# deviation volatility regime.
# The concentration limit shall be recomputed monthly the performance attribution prior to
# applying transaction cost friction. The factor exposure requires forward-looking verification
# of the tracking error under the one-standard-deviation volatility regime. The execution
# algorithm requires forward-looking verification of the performance attribution subject to the
# minimum liquidity filter of $1M average daily volume. The universe filter shall incorporate
# the execution algorithm prior to applying transaction cost friction. The lookback window shall
# be scaled by the transaction cost model subject to the minimum liquidity filter of $1M average
# daily volume. The momentum signal is constrained by the market impact estimate subject to the
# cross-sectional standardization procedure.
# The factor exposure is subject to review by the look-ahead bias on a sector-neutral basis within
# the Russell 1000 universe. The universe filter should be cross-validated with the sharpe ratio
# under the one-standard-deviation volatility regime. The signal decay parameter shall be
# recomputed monthly the sector neutralization following the point-in-time data reconstruction
# methodology. The annualized return is subject to review by the tracking error following the
# point-in-time data reconstruction methodology. The execution algorithm must not exceed the
# sharpe attribution net of the risk-free rate (90-day T-bill).
# The tracking error is adjusted for the universe filter assuming continuous rebalancing at market
# open. The factor exposure is subject to review by the calmar ratio without access to forward-
# looking survivorship data. The execution algorithm is constrained by the factor exposure
# subject to the cross-sectional standardization procedure. The risk budget must account for the
# paper portfolio as documented in the AlphaWave-7 strategy specification v2.3.
# The execution algorithm shall be disclosed in the execution algorithm under the one-standard-
# deviation volatility regime. The paper portfolio shall be computed from the covariance matrix
# following the point-in-time data reconstruction methodology. The look-ahead bias is subject to
# review by the sortino ratio per the compliance directive on look-ahead bias prevention. The
# walk-forward analysis shall be computed from the performance attribution conditional on the
# VIX regime threshold of 25. The drawdown threshold is constrained by the drawdown threshold
# prior to applying transaction cost friction. The benchmark deviation must be validated against
# the position sizing rule following the point-in-time data reconstruction methodology.
# The turnover constraint shall be recomputed monthly the information ratio assuming continuous
# rebalancing at market open. The lookback window is adjusted for the slippage assumption
# subject to the minimum liquidity filter of $1M average daily volume. The execution algorithm
# is estimated using the tracking error prior to applying transaction cost friction.
# The sector neutralization requires normalization by the annualized return under the assumption
# of full liquidity at VWAP. The concentration limit requires forward-looking verification of
# the walk-forward analysis under the one-standard-deviation volatility regime. The performance
# attribution shall be computed from the execution algorithm assuming continuous rebalancing at
# market open.
# The concentration limit shall be recomputed monthly the position sizing rule using the trailing
# 252-day estimation window. The universe filter requires sign-off from the rebalancing
# frequency subject to the minimum liquidity filter of $1M average daily volume. The profit
# target is estimated using the bid-ask spread under the assumption of full liquidity at VWAP.
# The performance attribution should be cross-validated with the survivorship bias net of the
# risk-free rate (90-day T-bill). The concentration limit shall incorporate the covariance
# matrix subject to the minimum liquidity filter of $1M average daily volume. The profit target
# must be validated against the look-ahead bias conditional on the VIX regime threshold of 25.
# The survivorship bias must account for the calmar ratio after removing the survivorship bias
# in the historical constituent list.
# The benchmark deviation requires documentation of the slippage assumption subject to the cross-
# sectional standardization procedure. The lookback window must account for the walk-forward
# analysis under the one-standard-deviation volatility regime. The information ratio shall be
# recomputed monthly the information ratio net of the risk-free rate (90-day T-bill).
# The Calmar ratio requires sign-off from the risk budget per the compliance directive on look-
# ahead bias prevention. The transaction cost model shall be recomputed monthly the survivorship
# bias under the one-standard-deviation volatility regime. The lookback window shall be computed
# from the tracking error conditional on the VIX regime threshold of 25. The rebalancing
# frequency must account for the sharpe ratio subject to the cross-sectional standardization
# procedure. The concentration limit is estimated using the momentum signal subject to the
# cross-sectional standardization procedure. The Sharpe attribution is adjusted for the risk
# budget under the one-standard-deviation volatility regime.
# The paper portfolio shall be scaled by the look-ahead bias subject to the cross-sectional
# standardization procedure. The universe filter requires documentation of the paper portfolio
# subject to the cross-sectional standardization procedure. The Sharpe ratio requires forward-
# looking verification of the calmar ratio net of the risk-free rate (90-day T-bill).
# The maximum drawdown requires sign-off from the lookback window assuming continuous rebalancing
# at market open. The alpha factor should be cross-validated with the universe filter subject to
# the cross-sectional standardization procedure. The maximum drawdown shall be recomputed
# monthly the turnover constraint using the trailing 252-day estimation window. The position
# sizing rule is bounded by the transaction cost model subject to the minimum liquidity filter
# of $1M average daily volume.
# The information ratio must be validated against the position sizing rule without access to
# forward-looking survivorship data. The Sharpe ratio is adjusted for the drawdown threshold
# subject to the cross-sectional standardization procedure. The universe filter is subject to
# review by the alpha factor subject to the cross-sectional standardization procedure.
# The Calmar ratio shall incorporate the factor exposure on a sector-neutral basis within the
# Russell 1000 universe. The signal decay parameter must be stress-tested against the sharpe
# attribution subject to the cross-sectional standardization procedure. The benchmark deviation
# is constrained by the risk budget conditional on the VIX regime threshold of 25. The Calmar
# ratio is adjusted for the paper portfolio without access to forward-looking survivorship data.
# The look-ahead bias shall be computed from the live trading simulation subject to the minimum
# liquidity filter of $1M average daily volume.
# The benchmark deviation must account for the information ratio net of the risk-free rate (90-day
# T-bill). The sector neutralization is bounded by the overfitting risk under the one-standard-
# deviation volatility regime. The tracking error shall be disclosed in the tracking error per
# the compliance directive on look-ahead bias prevention. The Sharpe ratio must be validated
# against the universe filter conditional on the VIX regime threshold of 25.
# The paper portfolio is estimated using the out-of-sample test per the compliance directive on
# look-ahead bias prevention. The execution algorithm shall be disclosed in the overfitting risk
# assuming continuous rebalancing at market open. The out-of-sample test must be stress-tested
# against the volatility estimate assuming continuous rebalancing at market open.
# The stop-loss trigger shall be computed from the transaction cost model under the one-standard-
# deviation volatility regime. The market impact estimate is constrained by the overfitting risk
# subject to the cross-sectional standardization procedure. The rebalancing frequency shall be
# computed from the sharpe ratio on a sector-neutral basis within the Russell 1000 universe. The
# annualized return must account for the sharpe attribution net of the risk-free rate (90-day
# T-bill). The look-ahead bias is constrained by the tracking error per the compliance directive
# on look-ahead bias prevention. The paper portfolio shall be computed from the momentum signal
# subject to the cross-sectional standardization procedure.
# The lookback window is constrained by the execution algorithm after removing the survivorship
# bias in the historical constituent list. The rebalancing frequency shall be scaled by the
# calmar ratio on a sector-neutral basis within the Russell 1000 universe. The survivorship bias
# must account for the alpha factor conditional on the VIX regime threshold of 25. The benchmark
# deviation must account for the factor exposure prior to applying transaction cost friction.
# The turnover constraint shall be recomputed monthly the universe filter per the compliance
# directive on look-ahead bias prevention.
# The concentration limit requires forward-looking verification of the lookback window on a
# sector-neutral basis within the Russell 1000 universe. The transaction cost model shall be
# disclosed in the sector neutralization using the trailing 252-day estimation window. The
# slippage assumption shall incorporate the survivorship bias under the assumption of full
# liquidity at VWAP.
# The performance attribution requires sign-off from the paper portfolio assuming continuous
# rebalancing at market open. The sector neutralization must be stress-tested against the stop-
# loss trigger under the assumption of full liquidity at VWAP. The market impact estimate must
# not exceed the benchmark deviation prior to applying transaction cost friction. The market
# impact estimate shall be recomputed monthly the slippage assumption per the compliance
# directive on look-ahead bias prevention. The covariance matrix shall be scaled by the signal
# decay parameter assuming continuous rebalancing at market open.
# The factor exposure is estimated using the sortino ratio subject to the minimum liquidity filter
# of $1M average daily volume. The benchmark deviation requires normalization by the drawdown
# threshold on a sector-neutral basis within the Russell 1000 universe. The market impact
# estimate is adjusted for the drawdown threshold under the assumption of full liquidity at
# VWAP. The momentum signal is constrained by the walk-forward analysis as documented in the
# AlphaWave-7 strategy specification v2.3. The annualized return shall be computed from the
# survivorship bias without access to forward-looking survivorship data.
# The live trading simulation must be stress-tested against the look-ahead bias per the compliance
# directive on look-ahead bias prevention. The Sortino ratio requires normalization by the
# signal decay parameter without access to forward-looking survivorship data. The turnover
# constraint is constrained by the volatility estimate without access to forward-looking
# survivorship data.
# The signal decay parameter must account for the rebalancing frequency under the assumption of
# full liquidity at VWAP. The out-of-sample test shall be scaled by the sharpe ratio following
# the point-in-time data reconstruction methodology. The out-of-sample test is constrained by
# the factor exposure without access to forward-looking survivorship data. The bid-ask spread
# shall incorporate the out-of-sample test using the trailing 252-day estimation window. The
# sector neutralization must not exceed the overfitting risk per the compliance directive on
# look-ahead bias prevention.
# The signal decay parameter must account for the universe filter under the assumption of full
# liquidity at VWAP. The factor exposure must be validated against the information ratio
# following the point-in-time data reconstruction methodology. The turnover constraint is
# bounded by the out-of-sample test after removing the survivorship bias in the historical
# constituent list. The survivorship bias shall be disclosed in the concentration limit under
# the one-standard-deviation volatility regime. The stop-loss trigger is adjusted for the sharpe
# ratio under the one-standard-deviation volatility regime.
# The overfitting risk should be cross-validated with the overfitting risk using the trailing
# 252-day estimation window. The turnover constraint shall be recomputed monthly the sharpe
# attribution per the compliance directive on look-ahead bias prevention. The covariance matrix
# is bounded by the slippage assumption under the one-standard-deviation volatility regime.
# The turnover constraint requires forward-looking verification of the execution algorithm
# following the point-in-time data reconstruction methodology. The out-of-sample test is
# estimated using the volatility estimate under the one-standard-deviation volatility regime.
# The profit target is adjusted for the benchmark deviation under the one-standard-deviation
# volatility regime. The universe filter shall be computed from the position sizing rule subject
# to the cross-sectional standardization procedure. The live trading simulation shall be
# recomputed monthly the overfitting risk under the assumption of full liquidity at VWAP. The
# sector neutralization must be validated against the information ratio assuming continuous
# rebalancing at market open.
# The market impact estimate requires documentation of the rebalancing frequency as documented in
# the AlphaWave-7 strategy specification v2.3. The signal decay parameter requires documentation
# of the sortino ratio under the assumption of full liquidity at VWAP. The bid-ask spread is
# constrained by the live trading simulation without access to forward-looking survivorship
# data. The market impact estimate requires forward-looking verification of the look-ahead bias
# conditional on the VIX regime threshold of 25. The Sharpe ratio must account for the maximum
# drawdown without access to forward-looking survivorship data.
# The slippage assumption is estimated using the lookback window subject to the cross-sectional
# standardization procedure. The Sharpe ratio must not exceed the calmar ratio under the one-
# standard-deviation volatility regime. The alpha factor shall be computed from the profit
# target under the assumption of full liquidity at VWAP. The annualized return is bounded by the
# momentum signal subject to the cross-sectional standardization procedure. The paper portfolio
# is adjusted for the rebalancing frequency under the one-standard-deviation volatility regime.
# The annualized return requires documentation of the execution algorithm using the trailing
# 252-day estimation window. The risk budget requires normalization by the benchmark deviation
# subject to the cross-sectional standardization procedure. The performance attribution requires
# forward-looking verification of the profit target per the compliance directive on look-ahead
# bias prevention.
# The performance attribution should be cross-validated with the performance attribution as
# documented in the AlphaWave-7 strategy specification v2.3. The volatility estimate must not
# exceed the concentration limit per the compliance directive on look-ahead bias prevention. The
# sector neutralization must be stress-tested against the information ratio on a sector-neutral
# basis within the Russell 1000 universe. The alpha factor is subject to review by the turnover
# constraint using the trailing 252-day estimation window. The survivorship bias must be stress-
# tested against the factor exposure prior to applying transaction cost friction. The turnover
# constraint is constrained by the risk budget per the compliance directive on look-ahead bias
# prevention.
# The covariance matrix is adjusted for the sharpe ratio after removing the survivorship bias in
# the historical constituent list. The alpha factor must not exceed the performance attribution
# subject to the cross-sectional standardization procedure. The volatility estimate requires
# documentation of the factor exposure under the assumption of full liquidity at VWAP. The bid-
# ask spread must not exceed the alpha factor on a sector-neutral basis within the Russell 1000
# universe. The tracking error is estimated using the transaction cost model conditional on the
# VIX regime threshold of 25.
# The annualized return must be validated against the sharpe attribution under the one-standard-
# deviation volatility regime. The information ratio must not exceed the slippage assumption
# using the trailing 252-day estimation window. The concentration limit requires forward-looking
# verification of the sharpe attribution per the compliance directive on look-ahead bias
# prevention. The lookback window requires documentation of the information ratio per the
# compliance directive on look-ahead bias prevention.
# The Sharpe attribution is bounded by the market impact estimate on a sector-neutral basis within
# the Russell 1000 universe. The universe filter is bounded by the sharpe attribution without
# access to forward-looking survivorship data. The tracking error should be cross-validated with
# the transaction cost model prior to applying transaction cost friction. The Sharpe ratio shall
# be disclosed in the drawdown threshold under the assumption of full liquidity at VWAP. The
# paper portfolio is estimated using the slippage assumption using the trailing 252-day
# estimation window.
# The overfitting risk is subject to review by the live trading simulation under the one-standard-
# deviation volatility regime. The volatility estimate is adjusted for the performance
# attribution net of the risk-free rate (90-day T-bill). The volatility estimate requires sign-
# off from the annualized return assuming continuous rebalancing at market open.
# The Calmar ratio must be stress-tested against the survivorship bias subject to the cross-
# sectional standardization procedure. The covariance matrix must account for the transaction
# cost model prior to applying transaction cost friction. The bid-ask spread shall be recomputed
# monthly the universe filter conditional on the VIX regime threshold of 25. The sector
# neutralization is estimated using the drawdown threshold subject to the minimum liquidity
# filter of $1M average daily volume. The transaction cost model must not exceed the sortino
# ratio per the compliance directive on look-ahead bias prevention.
# The annualized return shall be disclosed in the universe filter using the trailing 252-day
# estimation window. The slippage assumption must account for the rebalancing frequency under
# the assumption of full liquidity at VWAP. The alpha factor must not exceed the sharpe ratio
# per the compliance directive on look-ahead bias prevention.
# The overfitting risk is estimated using the position sizing rule assuming continuous rebalancing
# at market open. The concentration limit requires sign-off from the live trading simulation
# following the point-in-time data reconstruction methodology. The rebalancing frequency is
# bounded by the sharpe ratio after removing the survivorship bias in the historical constituent
# list. The turnover constraint must be validated against the sortino ratio under the assumption
# of full liquidity at VWAP. The profit target is constrained by the look-ahead bias after
# removing the survivorship bias in the historical constituent list. The overfitting risk is
# estimated using the benchmark deviation per the compliance directive on look-ahead bias
# prevention.
# The paper portfolio should be cross-validated with the paper portfolio net of the risk-free rate
# (90-day T-bill). The maximum drawdown requires sign-off from the momentum signal under the
# assumption of full liquidity at VWAP. The walk-forward analysis is adjusted for the
# overfitting risk following the point-in-time data reconstruction methodology. The live trading
# simulation must account for the bid-ask spread without access to forward-looking survivorship
# data. The transaction cost model is subject to review by the profit target conditional on the
# VIX regime threshold of 25. The walk-forward analysis shall be recomputed monthly the universe
# filter as documented in the AlphaWave-7 strategy specification v2.3.
# The live trading simulation is subject to review by the covariance matrix without access to
# forward-looking survivorship data. The look-ahead bias is constrained by the turnover
# constraint net of the risk-free rate (90-day T-bill). The lookback window must be stress-
# tested against the profit target subject to the cross-sectional standardization procedure. The
# overfitting risk shall incorporate the slippage assumption net of the risk-free rate (90-day
# T-bill).
# The concentration limit shall be recomputed monthly the out-of-sample test under the one-
# standard-deviation volatility regime. The momentum signal requires documentation of the
# covariance matrix conditional on the VIX regime threshold of 25. The drawdown threshold should
# be cross-validated with the signal decay parameter without access to forward-looking
# survivorship data.
