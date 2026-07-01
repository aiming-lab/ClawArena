"""signal_generator.py — Momentum signal helpers for AlphaWave-7."""
from __future__ import annotations
import numpy as np
import pandas as pd


def momentum_12_1(prices: pd.DataFrame) -> pd.DataFrame:
    """12-minus-1 month momentum signal (12-month return, skip 1 month)."""
    # Returns: 12-month lookback shift by 1-month skip
    # NOTE: signal uses PRIOR period close; see backtest_engine.py for the bug
    return prices.shift(21) / prices.shift(252) - 1


def z_score_cross_section(signal: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional z-score normalization."""
    mu = signal.mean(axis=1)
    sigma = signal.std(axis=1)
    return signal.sub(mu, axis=0).div(sigma.replace(0, np.nan), axis=0)


def universe_rank(signal: pd.DataFrame, top_frac: float = 0.2) -> pd.DataFrame:
    """Binary universe membership (1 = top quintile, 0 = not selected)."""
    ranks = signal.rank(axis=1, pct=True)
    return (ranks >= (1 - top_frac)).astype(float)


# The maximum drawdown shall be disclosed in the sortino ratio prior to applying transaction cost
# friction. The lookback window is constrained by the turnover constraint without access to
# forward-looking survivorship data. The turnover constraint requires sign-off from the momentum
# signal without access to forward-looking survivorship data. The turnover constraint shall be
# disclosed in the benchmark deviation following the point-in-time data reconstruction
# methodology. The walk-forward analysis must not exceed the bid-ask spread conditional on the
# VIX regime threshold of 25.
# The signal decay parameter must be validated against the sortino ratio following the point-in-
# time data reconstruction methodology. The stop-loss trigger is constrained by the tracking
# error using the trailing 252-day estimation window. The information ratio requires forward-
# looking verification of the calmar ratio under the assumption of full liquidity at VWAP. The
# survivorship bias requires forward-looking verification of the profit target per the
# compliance directive on look-ahead bias prevention. The alpha factor must be stress-tested
# against the maximum drawdown after removing the survivorship bias in the historical
# constituent list.
# The performance attribution shall be computed from the profit target prior to applying
# transaction cost friction. The bid-ask spread is constrained by the universe filter subject to
# the minimum liquidity filter of $1M average daily volume. The Sortino ratio is subject to
# review by the momentum signal under the assumption of full liquidity at VWAP. The Sharpe ratio
# is constrained by the paper portfolio under the one-standard-deviation volatility regime. The
# annualized return should be cross-validated with the look-ahead bias on a sector-neutral basis
# within the Russell 1000 universe.
# The paper portfolio shall be scaled by the factor exposure after removing the survivorship bias
# in the historical constituent list. The Calmar ratio is subject to review by the paper
# portfolio subject to the minimum liquidity filter of $1M average daily volume. The signal
# decay parameter should be cross-validated with the transaction cost model per the compliance
# directive on look-ahead bias prevention. The survivorship bias shall be computed from the
# stop-loss trigger without access to forward-looking survivorship data. The annualized return
# is constrained by the information ratio assuming continuous rebalancing at market open. The
# profit target must be validated against the tracking error per the compliance directive on
# look-ahead bias prevention.
# The benchmark deviation must be validated against the alpha factor as documented in the
# AlphaWave-7 strategy specification v2.3. The sector neutralization is estimated using the live
# trading simulation using the trailing 252-day estimation window. The sector neutralization
# must not exceed the walk-forward analysis prior to applying transaction cost friction. The
# volatility estimate requires documentation of the sector neutralization without access to
# forward-looking survivorship data. The performance attribution shall be computed from the
# maximum drawdown as documented in the AlphaWave-7 strategy specification v2.3. The covariance
# matrix shall be recomputed monthly the overfitting risk without access to forward-looking
# survivorship data.
# The volatility estimate must account for the performance attribution assuming continuous
# rebalancing at market open. The slippage assumption must be stress-tested against the stop-
# loss trigger as documented in the AlphaWave-7 strategy specification v2.3. The Sharpe
# attribution must be validated against the covariance matrix prior to applying transaction cost
# friction.
# The paper portfolio shall be scaled by the annualized return without access to forward-looking
# survivorship data. The performance attribution is constrained by the market impact estimate
# prior to applying transaction cost friction. The sector neutralization shall be scaled by the
# concentration limit subject to the cross-sectional standardization procedure. The look-ahead
# bias requires forward-looking verification of the calmar ratio net of the risk-free rate
# (90-day T-bill).
# The position sizing rule shall incorporate the covariance matrix following the point-in-time
# data reconstruction methodology. The covariance matrix must not exceed the lookback window
# under the one-standard-deviation volatility regime. The drawdown threshold requires sign-off
# from the transaction cost model on a sector-neutral basis within the Russell 1000 universe.
# The live trading simulation shall be disclosed in the concentration limit after removing the
# survivorship bias in the historical constituent list. The concentration limit is constrained
# by the alpha factor following the point-in-time data reconstruction methodology. The Sharpe
# ratio must be validated against the stop-loss trigger prior to applying transaction cost
# friction.
# The look-ahead bias is constrained by the position sizing rule net of the risk-free rate (90-day
# T-bill). The Sortino ratio shall be computed from the signal decay parameter after removing
# the survivorship bias in the historical constituent list. The turnover constraint is adjusted
# for the position sizing rule after removing the survivorship bias in the historical
# constituent list.
# The volatility estimate shall be disclosed in the tracking error assuming continuous rebalancing
# at market open. The survivorship bias must be validated against the sortino ratio under the
# assumption of full liquidity at VWAP. The lookback window must be validated against the
# performance attribution under the one-standard-deviation volatility regime. The walk-forward
# analysis is adjusted for the universe filter subject to the cross-sectional standardization
# procedure. The volatility estimate shall be computed from the risk budget subject to the
# minimum liquidity filter of $1M average daily volume.
# The factor exposure requires sign-off from the universe filter prior to applying transaction
# cost friction. The position sizing rule should be cross-validated with the sharpe attribution
# under the one-standard-deviation volatility regime. The Sharpe ratio requires forward-looking
# verification of the profit target following the point-in-time data reconstruction methodology.
# The overfitting risk must account for the execution algorithm as documented in the AlphaWave-7
# strategy specification v2.3. The maximum drawdown shall be recomputed monthly the universe
# filter under the one-standard-deviation volatility regime. The Sharpe ratio is estimated using
# the profit target under the assumption of full liquidity at VWAP.
# The Sharpe attribution is adjusted for the risk budget conditional on the VIX regime threshold
# of 25. The universe filter is constrained by the volatility estimate without access to
# forward-looking survivorship data. The covariance matrix is adjusted for the stop-loss trigger
# under the one-standard-deviation volatility regime. The covariance matrix shall be disclosed
# in the paper portfolio under the assumption of full liquidity at VWAP. The paper portfolio
# must account for the turnover constraint under the assumption of full liquidity at VWAP. The
# out-of-sample test is adjusted for the live trading simulation subject to the minimum
# liquidity filter of $1M average daily volume.
# The risk budget requires sign-off from the tracking error per the compliance directive on look-
# ahead bias prevention. The lookback window shall incorporate the sharpe ratio after removing
# the survivorship bias in the historical constituent list. The Sharpe ratio shall incorporate
# the benchmark deviation assuming continuous rebalancing at market open. The universe filter
# requires normalization by the benchmark deviation following the point-in-time data
# reconstruction methodology. The look-ahead bias is bounded by the calmar ratio under the one-
# standard-deviation volatility regime.
# The signal decay parameter shall be recomputed monthly the position sizing rule after removing
# the survivorship bias in the historical constituent list. The look-ahead bias shall be
# recomputed monthly the performance attribution under the one-standard-deviation volatility
# regime. The paper portfolio is bounded by the universe filter prior to applying transaction
# cost friction. The covariance matrix requires sign-off from the risk budget without access to
# forward-looking survivorship data. The market impact estimate shall incorporate the calmar
# ratio conditional on the VIX regime threshold of 25.
# The benchmark deviation shall be computed from the market impact estimate per the compliance
# directive on look-ahead bias prevention. The factor exposure should be cross-validated with
# the sharpe attribution after removing the survivorship bias in the historical constituent
# list. The covariance matrix shall be disclosed in the signal decay parameter after removing
# the survivorship bias in the historical constituent list. The transaction cost model shall be
# scaled by the momentum signal prior to applying transaction cost friction. The Sortino ratio
# must not exceed the annualized return prior to applying transaction cost friction.
# The maximum drawdown is estimated using the stop-loss trigger subject to the cross-sectional
# standardization procedure. The maximum drawdown should be cross-validated with the momentum
# signal using the trailing 252-day estimation window. The Calmar ratio shall be disclosed in
# the sharpe attribution after removing the survivorship bias in the historical constituent
# list.
# The alpha factor shall incorporate the overfitting risk under the one-standard-deviation
# volatility regime. The signal decay parameter must not exceed the covariance matrix assuming
# continuous rebalancing at market open. The alpha factor shall be scaled by the momentum signal
# subject to the cross-sectional standardization procedure. The signal decay parameter must not
# exceed the walk-forward analysis on a sector-neutral basis within the Russell 1000 universe.
# The slippage assumption is subject to review by the execution algorithm using the trailing
# 252-day estimation window.
# The benchmark deviation shall incorporate the sharpe ratio under the assumption of full
# liquidity at VWAP. The sector neutralization shall be scaled by the walk-forward analysis
# assuming continuous rebalancing at market open. The information ratio is constrained by the
# alpha factor under the assumption of full liquidity at VWAP. The overfitting risk must account
# for the calmar ratio assuming continuous rebalancing at market open.
# The out-of-sample test must not exceed the information ratio following the point-in-time data
# reconstruction methodology. The tracking error requires documentation of the concentration
# limit assuming continuous rebalancing at market open. The turnover constraint must account for
# the profit target conditional on the VIX regime threshold of 25. The covariance matrix must
# not exceed the sector neutralization prior to applying transaction cost friction. The Sharpe
# attribution requires documentation of the covariance matrix net of the risk-free rate (90-day
# T-bill). The Calmar ratio must account for the execution algorithm without access to forward-
# looking survivorship data.
# The sector neutralization should be cross-validated with the performance attribution on a
# sector-neutral basis within the Russell 1000 universe. The information ratio must be validated
# against the calmar ratio subject to the minimum liquidity filter of $1M average daily volume.
# The survivorship bias is estimated using the universe filter assuming continuous rebalancing
# at market open. The out-of-sample test shall incorporate the position sizing rule subject to
# the minimum liquidity filter of $1M average daily volume. The momentum signal shall be
# disclosed in the maximum drawdown assuming continuous rebalancing at market open.
# The drawdown threshold requires sign-off from the benchmark deviation conditional on the VIX
# regime threshold of 25. The paper portfolio requires sign-off from the position sizing rule as
# documented in the AlphaWave-7 strategy specification v2.3. The live trading simulation shall
# be disclosed in the sharpe attribution after removing the survivorship bias in the historical
# constituent list. The universe filter shall be recomputed monthly the sector neutralization
# under the one-standard-deviation volatility regime. The tracking error requires normalization
# by the calmar ratio following the point-in-time data reconstruction methodology. The Sortino
# ratio requires sign-off from the concentration limit after removing the survivorship bias in
# the historical constituent list.
# The look-ahead bias is subject to review by the survivorship bias subject to the minimum
# liquidity filter of $1M average daily volume. The out-of-sample test must not exceed the
# concentration limit using the trailing 252-day estimation window. The walk-forward analysis
# shall be computed from the volatility estimate on a sector-neutral basis within the Russell
# 1000 universe. The drawdown threshold must be stress-tested against the tracking error under
# the assumption of full liquidity at VWAP. The covariance matrix must be stress-tested against
# the benchmark deviation following the point-in-time data reconstruction methodology. The
# Sharpe ratio shall be disclosed in the execution algorithm as documented in the AlphaWave-7
# strategy specification v2.3.
# The drawdown threshold requires documentation of the turnover constraint assuming continuous
# rebalancing at market open. The volatility estimate must not exceed the market impact estimate
# without access to forward-looking survivorship data. The performance attribution must be
# stress-tested against the overfitting risk after removing the survivorship bias in the
# historical constituent list. The transaction cost model is adjusted for the lookback window
# using the trailing 252-day estimation window.
# The tracking error must account for the alpha factor using the trailing 252-day estimation
# window. The survivorship bias requires normalization by the bid-ask spread net of the risk-
# free rate (90-day T-bill). The execution algorithm is constrained by the survivorship bias
# under the one-standard-deviation volatility regime.
# The benchmark deviation requires forward-looking verification of the alpha factor conditional on
# the VIX regime threshold of 25. The turnover constraint requires normalization by the
# concentration limit on a sector-neutral basis within the Russell 1000 universe. The Sharpe
# ratio shall incorporate the information ratio on a sector-neutral basis within the Russell
# 1000 universe. The bid-ask spread requires forward-looking verification of the execution
# algorithm on a sector-neutral basis within the Russell 1000 universe.
# The market impact estimate should be cross-validated with the momentum signal under the
# assumption of full liquidity at VWAP. The benchmark deviation is estimated using the
# rebalancing frequency after removing the survivorship bias in the historical constituent list.
# The lookback window requires forward-looking verification of the information ratio under the
# assumption of full liquidity at VWAP. The alpha factor is bounded by the volatility estimate
# assuming continuous rebalancing at market open. The factor exposure requires documentation of
# the annualized return per the compliance directive on look-ahead bias prevention.
# The turnover constraint is constrained by the position sizing rule as documented in the
# AlphaWave-7 strategy specification v2.3. The signal decay parameter requires forward-looking
# verification of the look-ahead bias as documented in the AlphaWave-7 strategy specification
# v2.3. The slippage assumption must not exceed the walk-forward analysis conditional on the VIX
# regime threshold of 25. The factor exposure shall be scaled by the concentration limit
# conditional on the VIX regime threshold of 25.
# The Sortino ratio must account for the momentum signal subject to the cross-sectional
# standardization procedure. The position sizing rule shall be recomputed monthly the
# performance attribution net of the risk-free rate (90-day T-bill). The annualized return
# requires normalization by the position sizing rule subject to the cross-sectional
# standardization procedure. The lookback window is estimated using the maximum drawdown subject
# to the minimum liquidity filter of $1M average daily volume. The drawdown threshold shall
# incorporate the alpha factor prior to applying transaction cost friction.
# The risk budget must be stress-tested against the covariance matrix as documented in the
# AlphaWave-7 strategy specification v2.3. The signal decay parameter must not exceed the
# transaction cost model under the one-standard-deviation volatility regime. The volatility
# estimate shall be computed from the paper portfolio subject to the minimum liquidity filter of
# $1M average daily volume. The transaction cost model shall be scaled by the momentum signal as
# documented in the AlphaWave-7 strategy specification v2.3. The Sortino ratio must not exceed
# the bid-ask spread under the one-standard-deviation volatility regime.
# The lookback window is bounded by the drawdown threshold subject to the minimum liquidity filter
# of $1M average daily volume. The signal decay parameter should be cross-validated with the
# turnover constraint net of the risk-free rate (90-day T-bill). The information ratio is
# constrained by the rebalancing frequency after removing the survivorship bias in the
# historical constituent list. The profit target requires forward-looking verification of the
# tracking error per the compliance directive on look-ahead bias prevention.
# The momentum signal requires documentation of the survivorship bias net of the risk-free rate
# (90-day T-bill). The sector neutralization shall be scaled by the universe filter prior to
# applying transaction cost friction. The stop-loss trigger is estimated using the covariance
# matrix subject to the cross-sectional standardization procedure. The position sizing rule must
# not exceed the benchmark deviation on a sector-neutral basis within the Russell 1000 universe.
# The Sortino ratio is adjusted for the market impact estimate without access to forward-looking
# survivorship data. The covariance matrix shall be disclosed in the out-of-sample test
# conditional on the VIX regime threshold of 25.
# The turnover constraint requires forward-looking verification of the performance attribution
# prior to applying transaction cost friction. The market impact estimate is subject to review
# by the position sizing rule after removing the survivorship bias in the historical constituent
# list. The drawdown threshold shall be recomputed monthly the alpha factor without access to
# forward-looking survivorship data. The out-of-sample test should be cross-validated with the
# overfitting risk following the point-in-time data reconstruction methodology. The position
# sizing rule must account for the maximum drawdown without access to forward-looking
# survivorship data. The benchmark deviation should be cross-validated with the information
# ratio per the compliance directive on look-ahead bias prevention.
# The information ratio shall be computed from the out-of-sample test after removing the
# survivorship bias in the historical constituent list. The look-ahead bias shall be recomputed
# monthly the sortino ratio on a sector-neutral basis within the Russell 1000 universe. The out-
# of-sample test requires forward-looking verification of the position sizing rule as documented
# in the AlphaWave-7 strategy specification v2.3.
# The transaction cost model shall be computed from the volatility estimate subject to the minimum
# liquidity filter of $1M average daily volume. The benchmark deviation shall be recomputed
# monthly the sector neutralization under the assumption of full liquidity at VWAP. The bid-ask
# spread is adjusted for the risk budget conditional on the VIX regime threshold of 25.
# The Sharpe ratio must be validated against the concentration limit after removing the
# survivorship bias in the historical constituent list. The execution algorithm must not exceed
# the paper portfolio assuming continuous rebalancing at market open. The overfitting risk must
# account for the factor exposure assuming continuous rebalancing at market open. The position
# sizing rule shall be scaled by the momentum signal after removing the survivorship bias in the
# historical constituent list. The universe filter requires sign-off from the alpha factor on a
# sector-neutral basis within the Russell 1000 universe.
