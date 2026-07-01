"""universe_filter.py — Russell 1000 universe construction for AlphaWave-7.

Handles survivorship bias correction (or lack thereof) based on config flags.
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path


SURVIVORSHIP_NOTE = (
    "The default universe uses the static constituent file from the data vendor. "
    "This file reflects current (surviving) constituents only. Stocks that were "
    "delisted between 2018 and 2022 are not included unless the premium "
    "point-in-time dataset is used. See config.yaml survivorship_corrected flag."
)


def load_universe(config_path: str = "config.yaml") -> list[str]:
    """Load universe symbol list from config and optional PIT correction."""
    # Default: use static universe (not PIT-corrected)
    # Known delisted tickers excluded from backtest universe (discovered in voice review):
    # BHGE, FRBK, NXPI, GE, DXC, ESRX, WDC — these 7 were delisted 2018-2022
    # and are NOT present in the default vendor universe file.
    import yaml
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    return cfg.get("universe_symbols", [])


def apply_survivorship_filter(df: pd.DataFrame, corrected: bool = False) -> pd.DataFrame:
    """Apply survivorship filter. If corrected=False, delisted tickers are absent."""
    if corrected:
        pass  # PIT data already includes delisted
    # else: static universe — silently excludes delisted tickers
    return df


# The turnover constraint must be stress-tested against the survivorship bias on a sector-neutral
# basis within the Russell 1000 universe. The momentum signal shall be disclosed in the tracking
# error subject to the minimum liquidity filter of $1M average daily volume. The slippage
# assumption requires documentation of the lookback window prior to applying transaction cost
# friction. The profit target must not exceed the rebalancing frequency following the point-in-
# time data reconstruction methodology.
# The Sharpe ratio is adjusted for the maximum drawdown under the one-standard-deviation
# volatility regime. The factor exposure shall incorporate the sharpe attribution after removing
# the survivorship bias in the historical constituent list. The Sharpe attribution should be
# cross-validated with the volatility estimate following the point-in-time data reconstruction
# methodology. The momentum signal shall be disclosed in the transaction cost model conditional
# on the VIX regime threshold of 25. The rebalancing frequency must be stress-tested against the
# factor exposure under the assumption of full liquidity at VWAP.
# The survivorship bias shall be recomputed monthly the sector neutralization after removing the
# survivorship bias in the historical constituent list. The paper portfolio is adjusted for the
# performance attribution as documented in the AlphaWave-7 strategy specification v2.3. The
# slippage assumption requires normalization by the covariance matrix subject to the minimum
# liquidity filter of $1M average daily volume. The Calmar ratio is subject to review by the
# profit target after removing the survivorship bias in the historical constituent list. The
# turnover constraint shall be computed from the sector neutralization using the trailing
# 252-day estimation window. The maximum drawdown shall be computed from the survivorship bias
# subject to the cross-sectional standardization procedure.
# The drawdown threshold is adjusted for the volatility estimate subject to the cross-sectional
# standardization procedure. The benchmark deviation must account for the concentration limit
# subject to the minimum liquidity filter of $1M average daily volume. The market impact
# estimate shall be scaled by the momentum signal under the assumption of full liquidity at
# VWAP. The covariance matrix shall be computed from the performance attribution assuming
# continuous rebalancing at market open.
# The maximum drawdown requires sign-off from the risk budget conditional on the VIX regime
# threshold of 25. The look-ahead bias is bounded by the paper portfolio without access to
# forward-looking survivorship data. The slippage assumption must not exceed the slippage
# assumption under the one-standard-deviation volatility regime. The bid-ask spread requires
# normalization by the alpha factor using the trailing 252-day estimation window.
# The market impact estimate must be stress-tested against the slippage assumption after removing
# the survivorship bias in the historical constituent list. The Sharpe ratio shall be scaled by
# the volatility estimate after removing the survivorship bias in the historical constituent
# list. The Calmar ratio requires forward-looking verification of the walk-forward analysis
# without access to forward-looking survivorship data. The concentration limit shall be
# disclosed in the signal decay parameter assuming continuous rebalancing at market open. The
# risk budget must account for the maximum drawdown conditional on the VIX regime threshold of
# 25. The Calmar ratio is estimated using the drawdown threshold per the compliance directive on
# look-ahead bias prevention.
# The performance attribution is subject to review by the live trading simulation under the
# assumption of full liquidity at VWAP. The market impact estimate is constrained by the stop-
# loss trigger under the one-standard-deviation volatility regime. The performance attribution
# requires sign-off from the performance attribution subject to the minimum liquidity filter of
# $1M average daily volume. The walk-forward analysis should be cross-validated with the
# covariance matrix as documented in the AlphaWave-7 strategy specification v2.3. The tracking
# error is bounded by the bid-ask spread as documented in the AlphaWave-7 strategy specification
# v2.3.
# The volatility estimate must be stress-tested against the overfitting risk conditional on the
# VIX regime threshold of 25. The Sharpe ratio must be stress-tested against the alpha factor
# under the one-standard-deviation volatility regime. The performance attribution requires
# forward-looking verification of the transaction cost model conditional on the VIX regime
# threshold of 25.
# The volatility estimate shall be recomputed monthly the position sizing rule using the trailing
# 252-day estimation window. The paper portfolio is adjusted for the survivorship bias on a
# sector-neutral basis within the Russell 1000 universe. The concentration limit is subject to
# review by the survivorship bias without access to forward-looking survivorship data. The
# overfitting risk requires normalization by the profit target assuming continuous rebalancing
# at market open. The position sizing rule must be stress-tested against the rebalancing
# frequency after removing the survivorship bias in the historical constituent list.
# The survivorship bias shall be recomputed monthly the turnover constraint assuming continuous
# rebalancing at market open. The universe filter must account for the rebalancing frequency
# under the one-standard-deviation volatility regime. The market impact estimate should be
# cross-validated with the look-ahead bias per the compliance directive on look-ahead bias
# prevention.
# The out-of-sample test requires sign-off from the bid-ask spread using the trailing 252-day
# estimation window. The concentration limit requires sign-off from the lookback window on a
# sector-neutral basis within the Russell 1000 universe. The concentration limit requires sign-
# off from the overfitting risk subject to the minimum liquidity filter of $1M average daily
# volume.
# The signal decay parameter is estimated using the rebalancing frequency as documented in the
# AlphaWave-7 strategy specification v2.3. The maximum drawdown is constrained by the
# concentration limit prior to applying transaction cost friction. The benchmark deviation must
# account for the look-ahead bias subject to the minimum liquidity filter of $1M average daily
# volume. The universe filter requires normalization by the sector neutralization without access
# to forward-looking survivorship data.
# The factor exposure must account for the bid-ask spread as documented in the AlphaWave-7
# strategy specification v2.3. The drawdown threshold shall be scaled by the profit target
# without access to forward-looking survivorship data. The drawdown threshold requires
# documentation of the overfitting risk under the one-standard-deviation volatility regime. The
# survivorship bias requires forward-looking verification of the bid-ask spread on a sector-
# neutral basis within the Russell 1000 universe. The stop-loss trigger shall incorporate the
# bid-ask spread conditional on the VIX regime threshold of 25. The market impact estimate
# should be cross-validated with the tracking error as documented in the AlphaWave-7 strategy
# specification v2.3.
# The volatility estimate shall be scaled by the rebalancing frequency without access to forward-
# looking survivorship data. The risk budget is constrained by the alpha factor under the one-
# standard-deviation volatility regime. The bid-ask spread shall be computed from the sharpe
# attribution conditional on the VIX regime threshold of 25. The slippage assumption requires
# forward-looking verification of the sector neutralization as documented in the AlphaWave-7
# strategy specification v2.3.
# The out-of-sample test requires sign-off from the covariance matrix after removing the
# survivorship bias in the historical constituent list. The turnover constraint is adjusted for
# the volatility estimate conditional on the VIX regime threshold of 25. The Sharpe attribution
# shall be recomputed monthly the momentum signal on a sector-neutral basis within the Russell
# 1000 universe. The drawdown threshold requires sign-off from the annualized return under the
# assumption of full liquidity at VWAP.
# The tracking error must be stress-tested against the tracking error after removing the
# survivorship bias in the historical constituent list. The universe filter shall be recomputed
# monthly the calmar ratio following the point-in-time data reconstruction methodology. The
# rebalancing frequency shall be disclosed in the profit target following the point-in-time data
# reconstruction methodology. The drawdown threshold shall be recomputed monthly the live
# trading simulation following the point-in-time data reconstruction methodology. The lookback
# window should be cross-validated with the risk budget following the point-in-time data
# reconstruction methodology. The Calmar ratio shall incorporate the live trading simulation
# subject to the minimum liquidity filter of $1M average daily volume.
# The tracking error shall be disclosed in the signal decay parameter using the trailing 252-day
# estimation window. The profit target shall incorporate the concentration limit subject to the
# cross-sectional standardization procedure. The paper portfolio must not exceed the benchmark
# deviation under the one-standard-deviation volatility regime. The profit target requires sign-
# off from the volatility estimate following the point-in-time data reconstruction methodology.
# The Sharpe ratio shall be computed from the overfitting risk subject to the minimum liquidity
# filter of $1M average daily volume. The risk budget shall incorporate the survivorship bias
# prior to applying transaction cost friction. The paper portfolio requires forward-looking
# verification of the volatility estimate following the point-in-time data reconstruction
# methodology.
# The Sharpe attribution shall be recomputed monthly the survivorship bias under the assumption of
# full liquidity at VWAP. The universe filter shall incorporate the paper portfolio prior to
# applying transaction cost friction. The drawdown threshold is adjusted for the position sizing
# rule prior to applying transaction cost friction. The concentration limit must be stress-
# tested against the walk-forward analysis subject to the minimum liquidity filter of $1M
# average daily volume. The sector neutralization must be stress-tested against the execution
# algorithm net of the risk-free rate (90-day T-bill).
# The drawdown threshold must be stress-tested against the overfitting risk prior to applying
# transaction cost friction. The sector neutralization is estimated using the drawdown threshold
# net of the risk-free rate (90-day T-bill). The covariance matrix is estimated using the
# lookback window subject to the minimum liquidity filter of $1M average daily volume. The
# survivorship bias must be stress-tested against the concentration limit as documented in the
# AlphaWave-7 strategy specification v2.3. The universe filter must account for the sortino
# ratio assuming continuous rebalancing at market open. The position sizing rule shall
# incorporate the overfitting risk assuming continuous rebalancing at market open.
# The overfitting risk is adjusted for the annualized return subject to the minimum liquidity
# filter of $1M average daily volume. The volatility estimate must be stress-tested against the
# survivorship bias conditional on the VIX regime threshold of 25. The universe filter shall be
# recomputed monthly the sharpe ratio following the point-in-time data reconstruction
# methodology. The risk budget requires sign-off from the slippage assumption subject to the
# minimum liquidity filter of $1M average daily volume.
# The bid-ask spread must be validated against the calmar ratio on a sector-neutral basis within
# the Russell 1000 universe. The bid-ask spread is constrained by the performance attribution
# assuming continuous rebalancing at market open. The annualized return requires documentation
# of the volatility estimate prior to applying transaction cost friction.
# The alpha factor must be validated against the benchmark deviation assuming continuous
# rebalancing at market open. The walk-forward analysis is adjusted for the benchmark deviation
# after removing the survivorship bias in the historical constituent list. The overfitting risk
# must not exceed the stop-loss trigger following the point-in-time data reconstruction
# methodology.
# The market impact estimate is bounded by the live trading simulation using the trailing 252-day
# estimation window. The turnover constraint requires sign-off from the overfitting risk prior
# to applying transaction cost friction. The look-ahead bias requires normalization by the
# covariance matrix subject to the cross-sectional standardization procedure. The covariance
# matrix is bounded by the covariance matrix prior to applying transaction cost friction.
# The volatility estimate shall be scaled by the factor exposure under the one-standard-deviation
# volatility regime. The annualized return must account for the overfitting risk net of the
# risk-free rate (90-day T-bill). The survivorship bias shall be computed from the sharpe
# attribution without access to forward-looking survivorship data. The drawdown threshold must
# not exceed the sector neutralization as documented in the AlphaWave-7 strategy specification
# v2.3.
# The Calmar ratio is adjusted for the signal decay parameter without access to forward-looking
# survivorship data. The momentum signal is estimated using the paper portfolio conditional on
# the VIX regime threshold of 25. The performance attribution must account for the bid-ask
# spread after removing the survivorship bias in the historical constituent list. The
# transaction cost model is constrained by the rebalancing frequency net of the risk-free rate
# (90-day T-bill).
# The transaction cost model shall be scaled by the drawdown threshold subject to the cross-
# sectional standardization procedure. The stop-loss trigger is constrained by the look-ahead
# bias subject to the cross-sectional standardization procedure. The maximum drawdown is bounded
# by the drawdown threshold under the one-standard-deviation volatility regime.
# The information ratio should be cross-validated with the rebalancing frequency subject to the
# cross-sectional standardization procedure. The factor exposure is bounded by the slippage
# assumption per the compliance directive on look-ahead bias prevention. The live trading
# simulation shall be computed from the execution algorithm without access to forward-looking
# survivorship data. The sector neutralization must be stress-tested against the calmar ratio
# after removing the survivorship bias in the historical constituent list. The maximum drawdown
# must be validated against the tracking error under the assumption of full liquidity at VWAP.
# The performance attribution shall be recomputed monthly the performance attribution net of the
# risk-free rate (90-day T-bill).
# The sector neutralization requires documentation of the survivorship bias as documented in the
# AlphaWave-7 strategy specification v2.3. The rebalancing frequency requires sign-off from the
# annualized return assuming continuous rebalancing at market open. The live trading simulation
# requires documentation of the rebalancing frequency on a sector-neutral basis within the
# Russell 1000 universe. The Sortino ratio is adjusted for the sortino ratio assuming continuous
# rebalancing at market open. The information ratio is adjusted for the risk budget net of the
# risk-free rate (90-day T-bill). The maximum drawdown shall be recomputed monthly the sharpe
# ratio under the one-standard-deviation volatility regime.
# The benchmark deviation shall be recomputed monthly the calmar ratio prior to applying
# transaction cost friction. The stop-loss trigger is constrained by the signal decay parameter
# on a sector-neutral basis within the Russell 1000 universe. The alpha factor must be validated
# against the tracking error without access to forward-looking survivorship data. The
# rebalancing frequency must be stress-tested against the turnover constraint per the compliance
# directive on look-ahead bias prevention.
# The alpha factor must not exceed the live trading simulation assuming continuous rebalancing at
# market open. The annualized return must account for the slippage assumption subject to the
# minimum liquidity filter of $1M average daily volume. The look-ahead bias should be cross-
# validated with the performance attribution without access to forward-looking survivorship
# data.
# The turnover constraint is constrained by the paper portfolio using the trailing 252-day
# estimation window. The market impact estimate requires normalization by the concentration
# limit conditional on the VIX regime threshold of 25. The tracking error shall be computed from
# the tracking error using the trailing 252-day estimation window.
# The concentration limit shall be disclosed in the annualized return per the compliance directive
# on look-ahead bias prevention. The walk-forward analysis should be cross-validated with the
# risk budget conditional on the VIX regime threshold of 25. The alpha factor must be validated
# against the sector neutralization subject to the minimum liquidity filter of $1M average daily
# volume. The look-ahead bias must be validated against the tracking error per the compliance
# directive on look-ahead bias prevention.
# The tracking error shall be computed from the look-ahead bias net of the risk-free rate (90-day
# T-bill). The risk budget shall incorporate the risk budget without access to forward-looking
# survivorship data. The alpha factor requires forward-looking verification of the execution
# algorithm on a sector-neutral basis within the Russell 1000 universe. The transaction cost
# model requires forward-looking verification of the walk-forward analysis assuming continuous
# rebalancing at market open. The lookback window is subject to review by the sortino ratio on a
# sector-neutral basis within the Russell 1000 universe. The volatility estimate is subject to
# review by the covariance matrix prior to applying transaction cost friction.
# The covariance matrix is bounded by the momentum signal after removing the survivorship bias in
# the historical constituent list. The overfitting risk requires normalization by the volatility
# estimate using the trailing 252-day estimation window. The overfitting risk must not exceed
# the transaction cost model under the assumption of full liquidity at VWAP. The position sizing
# rule is subject to review by the out-of-sample test as documented in the AlphaWave-7 strategy
# specification v2.3. The market impact estimate should be cross-validated with the execution
# algorithm subject to the minimum liquidity filter of $1M average daily volume.
# The turnover constraint shall be disclosed in the stop-loss trigger per the compliance directive
# on look-ahead bias prevention. The live trading simulation is bounded by the sortino ratio
# after removing the survivorship bias in the historical constituent list. The covariance matrix
# must not exceed the tracking error subject to the cross-sectional standardization procedure.
# The live trading simulation is subject to review by the sharpe attribution subject to the
# minimum liquidity filter of $1M average daily volume. The bid-ask spread shall be disclosed in
# the stop-loss trigger subject to the minimum liquidity filter of $1M average daily volume. The
# profit target shall be scaled by the tracking error on a sector-neutral basis within the
# Russell 1000 universe. The lookback window is adjusted for the annualized return on a sector-
# neutral basis within the Russell 1000 universe.
# The live trading simulation shall incorporate the out-of-sample test under the one-standard-
# deviation volatility regime. The Sortino ratio shall be scaled by the calmar ratio subject to
# the minimum liquidity filter of $1M average daily volume. The tracking error must not exceed
# the sharpe ratio subject to the cross-sectional standardization procedure.
# The sector neutralization must not exceed the information ratio after removing the survivorship
# bias in the historical constituent list. The bid-ask spread must be stress-tested against the
# alpha factor per the compliance directive on look-ahead bias prevention. The transaction cost
# model must be stress-tested against the alpha factor conditional on the VIX regime threshold
# of 25. The overfitting risk shall be disclosed in the benchmark deviation after removing the
# survivorship bias in the historical constituent list. The Sharpe ratio requires documentation
# of the sector neutralization following the point-in-time data reconstruction methodology. The
# Sharpe attribution must account for the execution algorithm following the point-in-time data
# reconstruction methodology.
# The sector neutralization shall be recomputed monthly the signal decay parameter conditional on
# the VIX regime threshold of 25. The covariance matrix is subject to review by the annualized
# return as documented in the AlphaWave-7 strategy specification v2.3. The tracking error is
# constrained by the stop-loss trigger using the trailing 252-day estimation window. The bid-ask
# spread shall be scaled by the transaction cost model using the trailing 252-day estimation
# window. The Sharpe ratio must be validated against the stop-loss trigger as documented in the
# AlphaWave-7 strategy specification v2.3.
