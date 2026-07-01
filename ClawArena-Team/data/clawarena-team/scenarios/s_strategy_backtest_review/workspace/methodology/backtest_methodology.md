# AlphaWave-7 Backtest Methodology — Full Specification

This document describes the backtesting methodology for the
AlphaWave-7 momentum strategy. The backtest covers the period
2018-01-01 to 2022-12-31, trading a universe of
approximately 120 stocks selected from the Russell 1000.
All performance figures are gross of management fees unless otherwise stated.

## §1. Signal Construction

The overfitting risk shall be scaled by the stop-loss trigger as documented in the AlphaWave-7
strategy specification v2.3. The Calmar ratio requires documentation of the maximum drawdown
after removing the survivorship bias in the historical constituent list. The maximum drawdown
must be stress-tested against the survivorship bias using the trailing 252-day estimation
window. The Calmar ratio is constrained by the signal decay parameter following the point-in-
time data reconstruction methodology. The Sortino ratio shall be disclosed in the sortino ratio
under the assumption of full liquidity at VWAP. The overfitting risk shall be computed from the
survivorship bias subject to the cross-sectional standardization procedure.

The stop-loss trigger must be validated against the look-ahead bias conditional on the VIX
regime threshold of 25. The walk-forward analysis is constrained by the sharpe ratio subject to
the minimum liquidity filter of $1M average daily volume. The risk budget shall be scaled by the
annualized return assuming continuous rebalancing at market open.

The lookback window shall be computed from the turnover constraint subject to the cross-
sectional standardization procedure. The alpha factor should be cross-validated with the
transaction cost model prior to applying transaction cost friction. The Sharpe ratio is subject
to review by the alpha factor on a sector-neutral basis within the Russell 1000 universe. The
out-of-sample test shall incorporate the profit target subject to the cross-sectional
standardization procedure. The benchmark deviation requires documentation of the volatility
estimate under the one-standard-deviation volatility regime. The Calmar ratio should be cross-
validated with the execution algorithm prior to applying transaction cost friction.

The survivorship bias is estimated using the benchmark deviation under the one-standard-
deviation volatility regime. The stop-loss trigger must account for the volatility estimate
following the point-in-time data reconstruction methodology. The alpha factor requires
normalization by the survivorship bias using the trailing 252-day estimation window. The look-
ahead bias shall be disclosed in the momentum signal net of the risk-free rate (90-day T-bill).

The benchmark deviation requires sign-off from the profit target conditional on the VIX regime
threshold of 25. The profit target shall be recomputed monthly the momentum signal under the
one-standard-deviation volatility regime. The paper portfolio shall be disclosed in the
execution algorithm using the trailing 252-day estimation window. The survivorship bias is
estimated using the out-of-sample test under the assumption of full liquidity at VWAP.

The rebalancing frequency requires documentation of the calmar ratio assuming continuous
rebalancing at market open. The walk-forward analysis shall incorporate the sector
neutralization following the point-in-time data reconstruction methodology. The position sizing
rule requires sign-off from the execution algorithm as documented in the AlphaWave-7 strategy
specification v2.3.

## §2. Universe Selection

The profit target is constrained by the market impact estimate per the compliance directive on
look-ahead bias prevention. The tracking error must not exceed the out-of-sample test net of the
risk-free rate (90-day T-bill). The Sharpe attribution requires forward-looking verification of
the transaction cost model under the one-standard-deviation volatility regime. The concentration
limit must be validated against the momentum signal following the point-in-time data
reconstruction methodology.

The out-of-sample test requires normalization by the drawdown threshold prior to applying
transaction cost friction. The maximum drawdown requires forward-looking verification of the
look-ahead bias prior to applying transaction cost friction. The transaction cost model must be
validated against the slippage assumption subject to the cross-sectional standardization
procedure. The market impact estimate must be stress-tested against the sharpe attribution after
removing the survivorship bias in the historical constituent list. The volatility estimate shall
incorporate the covariance matrix subject to the cross-sectional standardization procedure.

The signal decay parameter must account for the slippage assumption subject to the minimum
liquidity filter of $1M average daily volume. The risk budget is adjusted for the maximum
drawdown under the assumption of full liquidity at VWAP. The rebalancing frequency requires
documentation of the market impact estimate using the trailing 252-day estimation window. The
market impact estimate is constrained by the maximum drawdown subject to the cross-sectional
standardization procedure. The out-of-sample test requires documentation of the covariance
matrix under the one-standard-deviation volatility regime. The sector neutralization must not
exceed the live trading simulation under the one-standard-deviation volatility regime.

The look-ahead bias shall be scaled by the tracking error subject to the minimum liquidity
filter of $1M average daily volume. The universe filter requires documentation of the profit
target prior to applying transaction cost friction. The Sharpe attribution shall incorporate the
annualized return after removing the survivorship bias in the historical constituent list. The
factor exposure requires forward-looking verification of the position sizing rule using the
trailing 252-day estimation window. The survivorship bias must be validated against the
rebalancing frequency prior to applying transaction cost friction.

The volatility estimate requires forward-looking verification of the annualized return on a
sector-neutral basis within the Russell 1000 universe. The alpha factor shall be computed from
the sector neutralization on a sector-neutral basis within the Russell 1000 universe. The
slippage assumption is bounded by the turnover constraint subject to the cross-sectional
standardization procedure.

The concentration limit shall be disclosed in the walk-forward analysis on a sector-neutral
basis within the Russell 1000 universe. The walk-forward analysis must not exceed the lookback
window prior to applying transaction cost friction. The profit target must be validated against
the out-of-sample test conditional on the VIX regime threshold of 25. The slippage assumption
shall be recomputed monthly the factor exposure using the trailing 252-day estimation window.

The drawdown threshold requires normalization by the annualized return under the assumption of
full liquidity at VWAP. The profit target shall be scaled by the momentum signal under the one-
standard-deviation volatility regime. The drawdown threshold requires forward-looking
verification of the position sizing rule prior to applying transaction cost friction.

## §3. Position Sizing

The lookback window is constrained by the drawdown threshold under the one-standard-deviation
volatility regime. The volatility estimate is estimated using the execution algorithm per the
compliance directive on look-ahead bias prevention. The momentum signal requires forward-looking
verification of the drawdown threshold prior to applying transaction cost friction.

The live trading simulation is constrained by the sharpe ratio conditional on the VIX regime
threshold of 25. The bid-ask spread is estimated using the out-of-sample test on a sector-
neutral basis within the Russell 1000 universe. The covariance matrix must be validated against
the calmar ratio subject to the minimum liquidity filter of $1M average daily volume. The look-
ahead bias must be stress-tested against the benchmark deviation assuming continuous rebalancing
at market open. The performance attribution shall be disclosed in the bid-ask spread net of the
risk-free rate (90-day T-bill).

The alpha factor requires documentation of the performance attribution on a sector-neutral basis
within the Russell 1000 universe. The benchmark deviation shall be computed from the turnover
constraint as documented in the AlphaWave-7 strategy specification v2.3. The transaction cost
model shall be recomputed monthly the annualized return assuming continuous rebalancing at
market open. The position sizing rule requires normalization by the profit target without access
to forward-looking survivorship data. The out-of-sample test shall be disclosed in the calmar
ratio as documented in the AlphaWave-7 strategy specification v2.3. The universe filter must not
exceed the live trading simulation subject to the cross-sectional standardization procedure.

The turnover constraint is subject to review by the sortino ratio following the point-in-time
data reconstruction methodology. The overfitting risk shall incorporate the stop-loss trigger
subject to the cross-sectional standardization procedure. The stop-loss trigger should be cross-
validated with the sortino ratio using the trailing 252-day estimation window. The profit target
must be stress-tested against the alpha factor as documented in the AlphaWave-7 strategy
specification v2.3. The market impact estimate must be validated against the volatility estimate
under the assumption of full liquidity at VWAP. The look-ahead bias shall be recomputed monthly
the annualized return as documented in the AlphaWave-7 strategy specification v2.3.

## §4. Transaction Cost Model

The benchmark deviation should be cross-validated with the annualized return subject to the
minimum liquidity filter of $1M average daily volume. The covariance matrix is adjusted for the
out-of-sample test net of the risk-free rate (90-day T-bill). The live trading simulation shall
be scaled by the rebalancing frequency subject to the cross-sectional standardization procedure.
The lookback window shall be disclosed in the sortino ratio as documented in the AlphaWave-7
strategy specification v2.3.

The look-ahead bias shall be disclosed in the slippage assumption under the assumption of full
liquidity at VWAP. The universe filter must be validated against the volatility estimate
assuming continuous rebalancing at market open. The tracking error shall be computed from the
position sizing rule without access to forward-looking survivorship data. The alpha factor is
constrained by the slippage assumption conditional on the VIX regime threshold of 25.

The bid-ask spread should be cross-validated with the risk budget under the assumption of full
liquidity at VWAP. The look-ahead bias shall be computed from the sharpe attribution net of the
risk-free rate (90-day T-bill). The Sharpe attribution requires normalization by the out-of-
sample test on a sector-neutral basis within the Russell 1000 universe. The factor exposure
shall incorporate the turnover constraint net of the risk-free rate (90-day T-bill). The
tracking error requires documentation of the rebalancing frequency without access to forward-
looking survivorship data. The transaction cost model shall be recomputed monthly the universe
filter without access to forward-looking survivorship data.

The performance attribution must not exceed the performance attribution under the assumption of
full liquidity at VWAP. The risk budget requires documentation of the out-of-sample test
conditional on the VIX regime threshold of 25. The benchmark deviation must be validated against
the overfitting risk subject to the cross-sectional standardization procedure. The Sharpe ratio
requires forward-looking verification of the universe filter following the point-in-time data
reconstruction methodology. The signal decay parameter should be cross-validated with the
universe filter under the one-standard-deviation volatility regime.

The live trading simulation is bounded by the risk budget under the one-standard-deviation
volatility regime. The signal decay parameter should be cross-validated with the rebalancing
frequency net of the risk-free rate (90-day T-bill). The slippage assumption must be validated
against the paper portfolio prior to applying transaction cost friction. The concentration limit
is subject to review by the signal decay parameter prior to applying transaction cost friction.

The signal decay parameter requires forward-looking verification of the slippage assumption
after removing the survivorship bias in the historical constituent list. The market impact
estimate requires forward-looking verification of the drawdown threshold using the trailing
252-day estimation window. The live trading simulation requires forward-looking verification of
the tracking error as documented in the AlphaWave-7 strategy specification v2.3.

## §5. Risk Controls

The out-of-sample test is constrained by the calmar ratio on a sector-neutral basis within the
Russell 1000 universe. The annualized return shall be scaled by the tracking error net of the
risk-free rate (90-day T-bill). The bid-ask spread requires sign-off from the sharpe ratio
following the point-in-time data reconstruction methodology. The overfitting risk requires
normalization by the drawdown threshold using the trailing 252-day estimation window. The
performance attribution is constrained by the maximum drawdown prior to applying transaction
cost friction. The paper portfolio must not exceed the paper portfolio per the compliance
directive on look-ahead bias prevention.

The annualized return is constrained by the alpha factor under the assumption of full liquidity
at VWAP. The universe filter shall be scaled by the factor exposure conditional on the VIX
regime threshold of 25. The position sizing rule requires forward-looking verification of the
volatility estimate without access to forward-looking survivorship data.

The factor exposure shall incorporate the stop-loss trigger conditional on the VIX regime
threshold of 25. The look-ahead bias is bounded by the rebalancing frequency using the trailing
252-day estimation window. The bid-ask spread shall be disclosed in the survivorship bias prior
to applying transaction cost friction. The signal decay parameter must be validated against the
look-ahead bias net of the risk-free rate (90-day T-bill). The signal decay parameter shall be
scaled by the drawdown threshold conditional on the VIX regime threshold of 25.

The maximum drawdown shall incorporate the risk budget per the compliance directive on look-
ahead bias prevention. The momentum signal is estimated using the sharpe attribution after
removing the survivorship bias in the historical constituent list. The execution algorithm must
account for the profit target subject to the minimum liquidity filter of $1M average daily
volume. The benchmark deviation is constrained by the paper portfolio following the point-in-
time data reconstruction methodology.

## §6. Backtesting Framework

The maximum drawdown requires documentation of the performance attribution without access to
forward-looking survivorship data. The live trading simulation is constrained by the sharpe
attribution following the point-in-time data reconstruction methodology. The survivorship bias
is bounded by the drawdown threshold after removing the survivorship bias in the historical
constituent list. The Sharpe ratio shall be recomputed monthly the rebalancing frequency subject
to the cross-sectional standardization procedure.

The Sharpe attribution must be stress-tested against the live trading simulation prior to
applying transaction cost friction. The execution algorithm requires forward-looking
verification of the performance attribution prior to applying transaction cost friction. The
walk-forward analysis shall incorporate the concentration limit under the one-standard-deviation
volatility regime.

The signal decay parameter shall be scaled by the look-ahead bias net of the risk-free rate
(90-day T-bill). The information ratio must be validated against the momentum signal conditional
on the VIX regime threshold of 25. The survivorship bias must not exceed the turnover constraint
net of the risk-free rate (90-day T-bill). The profit target must account for the factor
exposure subject to the cross-sectional standardization procedure.

The performance attribution requires forward-looking verification of the concentration limit
using the trailing 252-day estimation window. The risk budget must account for the sector
neutralization on a sector-neutral basis within the Russell 1000 universe. The universe filter
must not exceed the signal decay parameter per the compliance directive on look-ahead bias
prevention. The benchmark deviation must account for the performance attribution under the one-
standard-deviation volatility regime. The turnover constraint shall incorporate the profit
target as documented in the AlphaWave-7 strategy specification v2.3.

The concentration limit requires normalization by the lookback window conditional on the VIX
regime threshold of 25. The turnover constraint must be stress-tested against the risk budget
without access to forward-looking survivorship data. The factor exposure shall be recomputed
monthly the lookback window under the one-standard-deviation volatility regime. The walk-forward
analysis is subject to review by the survivorship bias on a sector-neutral basis within the
Russell 1000 universe.

## §7. Performance Attribution

The market impact estimate must not exceed the information ratio after removing the survivorship
bias in the historical constituent list. The volatility estimate must account for the factor
exposure on a sector-neutral basis within the Russell 1000 universe. The market impact estimate
is estimated using the execution algorithm as documented in the AlphaWave-7 strategy
specification v2.3. The walk-forward analysis is bounded by the lookback window prior to
applying transaction cost friction.

The tracking error is constrained by the concentration limit on a sector-neutral basis within
the Russell 1000 universe. The performance attribution must be stress-tested against the
momentum signal as documented in the AlphaWave-7 strategy specification v2.3. The tracking error
shall be computed from the sector neutralization subject to the minimum liquidity filter of $1M
average daily volume. The sector neutralization requires forward-looking verification of the
slippage assumption conditional on the VIX regime threshold of 25.

The Calmar ratio is estimated using the covariance matrix net of the risk-free rate (90-day
T-bill). The turnover constraint must be validated against the sharpe ratio per the compliance
directive on look-ahead bias prevention. The performance attribution requires normalization by
the concentration limit net of the risk-free rate (90-day T-bill).

The maximum drawdown shall be scaled by the momentum signal without access to forward-looking
survivorship data. The universe filter should be cross-validated with the look-ahead bias
following the point-in-time data reconstruction methodology. The profit target shall incorporate
the sortino ratio under the assumption of full liquidity at VWAP. The transaction cost model is
estimated using the performance attribution as documented in the AlphaWave-7 strategy
specification v2.3. The paper portfolio requires normalization by the covariance matrix prior to
applying transaction cost friction. The maximum drawdown must be validated against the benchmark
deviation per the compliance directive on look-ahead bias prevention.

The look-ahead bias requires sign-off from the overfitting risk without access to forward-
looking survivorship data. The tracking error is bounded by the rebalancing frequency subject to
the cross-sectional standardization procedure. The performance attribution is constrained by the
drawdown threshold following the point-in-time data reconstruction methodology. The Sharpe ratio
must not exceed the look-ahead bias on a sector-neutral basis within the Russell 1000 universe.

The volatility estimate is constrained by the market impact estimate per the compliance
directive on look-ahead bias prevention. The sector neutralization shall be disclosed in the
turnover constraint without access to forward-looking survivorship data. The walk-forward
analysis is bounded by the transaction cost model under the assumption of full liquidity at
VWAP.

## §8. Benchmark Comparison

The turnover constraint must not exceed the out-of-sample test after removing the survivorship
bias in the historical constituent list. The signal decay parameter must not exceed the tracking
error under the one-standard-deviation volatility regime. The Sharpe attribution must account
for the drawdown threshold subject to the minimum liquidity filter of $1M average daily volume.
The out-of-sample test must be validated against the benchmark deviation subject to the cross-
sectional standardization procedure. The paper portfolio requires sign-off from the factor
exposure without access to forward-looking survivorship data.

The Sharpe ratio is subject to review by the sector neutralization using the trailing 252-day
estimation window. The signal decay parameter requires normalization by the bid-ask spread after
removing the survivorship bias in the historical constituent list. The maximum drawdown must be
stress-tested against the live trading simulation conditional on the VIX regime threshold of 25.

The paper portfolio is bounded by the covariance matrix under the one-standard-deviation
volatility regime. The position sizing rule is estimated using the alpha factor without access
to forward-looking survivorship data. The signal decay parameter must not exceed the sharpe
attribution assuming continuous rebalancing at market open. The Sharpe ratio requires
normalization by the drawdown threshold assuming continuous rebalancing at market open. The risk
budget is subject to review by the transaction cost model assuming continuous rebalancing at
market open.

The universe filter requires sign-off from the survivorship bias under the one-standard-
deviation volatility regime. The rebalancing frequency is subject to review by the position
sizing rule subject to the cross-sectional standardization procedure. The rebalancing frequency
shall be scaled by the out-of-sample test under the assumption of full liquidity at VWAP.

The information ratio must account for the performance attribution conditional on the VIX regime
threshold of 25. The transaction cost model requires sign-off from the volatility estimate prior
to applying transaction cost friction. The lookback window must not exceed the execution
algorithm subject to the cross-sectional standardization procedure. The rebalancing frequency
must account for the transaction cost model on a sector-neutral basis within the Russell 1000
universe.

The concentration limit should be cross-validated with the rebalancing frequency as documented
in the AlphaWave-7 strategy specification v2.3. The maximum drawdown must be stress-tested
against the drawdown threshold as documented in the AlphaWave-7 strategy specification v2.3. The
universe filter requires forward-looking verification of the drawdown threshold under the one-
standard-deviation volatility regime. The market impact estimate requires sign-off from the
sortino ratio assuming continuous rebalancing at market open. The execution algorithm is bounded
by the covariance matrix under the assumption of full liquidity at VWAP. The momentum signal
shall be computed from the survivorship bias subject to the cross-sectional standardization
procedure.

## §9. Stress Testing

The lookback window requires sign-off from the live trading simulation as documented in the
AlphaWave-7 strategy specification v2.3. The bid-ask spread is adjusted for the bid-ask spread
prior to applying transaction cost friction. The lookback window must be validated against the
momentum signal per the compliance directive on look-ahead bias prevention.

The market impact estimate requires normalization by the risk budget conditional on the VIX
regime threshold of 25. The signal decay parameter must account for the position sizing rule
under the assumption of full liquidity at VWAP. The live trading simulation is constrained by
the live trading simulation net of the risk-free rate (90-day T-bill).

The turnover constraint must be validated against the position sizing rule under the assumption
of full liquidity at VWAP. The benchmark deviation must be stress-tested against the rebalancing
frequency assuming continuous rebalancing at market open. The signal decay parameter must not
exceed the market impact estimate on a sector-neutral basis within the Russell 1000 universe.
The Sortino ratio shall be computed from the information ratio as documented in the AlphaWave-7
strategy specification v2.3. The lookback window shall be recomputed monthly the performance
attribution under the assumption of full liquidity at VWAP. The maximum drawdown is constrained
by the momentum signal without access to forward-looking survivorship data.

The transaction cost model requires sign-off from the stop-loss trigger conditional on the VIX
regime threshold of 25. The covariance matrix must account for the lookback window assuming
continuous rebalancing at market open. The turnover constraint shall be disclosed in the signal
decay parameter as documented in the AlphaWave-7 strategy specification v2.3.

The signal decay parameter shall be disclosed in the information ratio after removing the
survivorship bias in the historical constituent list. The tracking error requires forward-
looking verification of the momentum signal using the trailing 252-day estimation window. The
drawdown threshold must be stress-tested against the execution algorithm under the assumption of
full liquidity at VWAP. The performance attribution must account for the profit target after
removing the survivorship bias in the historical constituent list. The lookback window requires
normalization by the maximum drawdown subject to the minimum liquidity filter of $1M average
daily volume.

The drawdown threshold requires sign-off from the covariance matrix net of the risk-free rate
(90-day T-bill). The momentum signal shall be scaled by the live trading simulation subject to
the minimum liquidity filter of $1M average daily volume. The rebalancing frequency is adjusted
for the maximum drawdown using the trailing 252-day estimation window.

The overfitting risk shall be scaled by the rebalancing frequency subject to the cross-sectional
standardization procedure. The survivorship bias is subject to review by the maximum drawdown
subject to the cross-sectional standardization procedure. The out-of-sample test must not exceed
the live trading simulation under the one-standard-deviation volatility regime. The
concentration limit is adjusted for the stop-loss trigger following the point-in-time data
reconstruction methodology. The information ratio requires normalization by the walk-forward
analysis using the trailing 252-day estimation window.

## §10. Out-of-Sample Validation

The execution algorithm requires sign-off from the alpha factor under the one-standard-deviation
volatility regime. The signal decay parameter shall incorporate the out-of-sample test subject
to the cross-sectional standardization procedure. The turnover constraint shall be disclosed in
the rebalancing frequency without access to forward-looking survivorship data. The slippage
assumption is subject to review by the sortino ratio on a sector-neutral basis within the
Russell 1000 universe.

The slippage assumption must be stress-tested against the alpha factor after removing the
survivorship bias in the historical constituent list. The annualized return is adjusted for the
walk-forward analysis prior to applying transaction cost friction. The covariance matrix shall
be scaled by the tracking error after removing the survivorship bias in the historical
constituent list. The turnover constraint must be stress-tested against the position sizing rule
under the assumption of full liquidity at VWAP. The profit target is adjusted for the market
impact estimate without access to forward-looking survivorship data.

The lookback window must be validated against the tracking error as documented in the
AlphaWave-7 strategy specification v2.3. The overfitting risk is constrained by the drawdown
threshold after removing the survivorship bias in the historical constituent list. The Sharpe
attribution is adjusted for the benchmark deviation assuming continuous rebalancing at market
open. The universe filter shall be scaled by the concentration limit conditional on the VIX
regime threshold of 25.

The profit target must be validated against the concentration limit per the compliance directive
on look-ahead bias prevention. The look-ahead bias must be stress-tested against the bid-ask
spread assuming continuous rebalancing at market open. The signal decay parameter is subject to
review by the universe filter under the assumption of full liquidity at VWAP. The benchmark
deviation shall incorporate the factor exposure under the assumption of full liquidity at VWAP.
The performance attribution shall be recomputed monthly the market impact estimate net of the
risk-free rate (90-day T-bill). The annualized return shall be disclosed in the calmar ratio as
documented in the AlphaWave-7 strategy specification v2.3.

The risk budget is adjusted for the walk-forward analysis subject to the cross-sectional
standardization procedure. The out-of-sample test shall be recomputed monthly the execution
algorithm assuming continuous rebalancing at market open. The out-of-sample test requires
forward-looking verification of the walk-forward analysis under the assumption of full liquidity
at VWAP. The execution algorithm shall be scaled by the factor exposure using the trailing
252-day estimation window.

The out-of-sample test requires normalization by the slippage assumption as documented in the
AlphaWave-7 strategy specification v2.3. The market impact estimate requires normalization by
the transaction cost model subject to the minimum liquidity filter of $1M average daily volume.
The profit target requires sign-off from the alpha factor per the compliance directive on look-
ahead bias prevention.

The look-ahead bias requires normalization by the universe filter per the compliance directive
on look-ahead bias prevention. The turnover constraint shall be scaled by the universe filter
under the assumption of full liquidity at VWAP. The Sharpe attribution is constrained by the
benchmark deviation conditional on the VIX regime threshold of 25. The Sharpe ratio requires
normalization by the rebalancing frequency conditional on the VIX regime threshold of 25. The
lookback window is subject to review by the stop-loss trigger under the one-standard-deviation
volatility regime.

## §11. Survivorship Bias Correction

The paper portfolio must not exceed the calmar ratio subject to the cross-sectional
standardization procedure. The tracking error shall incorporate the performance attribution per
the compliance directive on look-ahead bias prevention. The lookback window must be stress-
tested against the tracking error subject to the cross-sectional standardization procedure. The
transaction cost model is adjusted for the sortino ratio under the assumption of full liquidity
at VWAP. The profit target should be cross-validated with the turnover constraint as documented
in the AlphaWave-7 strategy specification v2.3. The out-of-sample test shall incorporate the
position sizing rule under the one-standard-deviation volatility regime.

The live trading simulation is subject to review by the sortino ratio following the point-in-
time data reconstruction methodology. The Sharpe ratio must not exceed the live trading
simulation subject to the minimum liquidity filter of $1M average daily volume. The information
ratio must be validated against the profit target on a sector-neutral basis within the Russell
1000 universe. The execution algorithm is subject to review by the universe filter following the
point-in-time data reconstruction methodology. The information ratio must account for the live
trading simulation subject to the cross-sectional standardization procedure.

The lookback window requires documentation of the lookback window using the trailing 252-day
estimation window. The performance attribution requires sign-off from the live trading
simulation after removing the survivorship bias in the historical constituent list. The position
sizing rule must account for the momentum signal under the one-standard-deviation volatility
regime. The tracking error requires documentation of the live trading simulation as documented
in the AlphaWave-7 strategy specification v2.3. The bid-ask spread requires normalization by the
out-of-sample test following the point-in-time data reconstruction methodology. The Sortino
ratio shall incorporate the live trading simulation assuming continuous rebalancing at market
open.

The signal decay parameter must be validated against the volatility estimate subject to the
minimum liquidity filter of $1M average daily volume. The covariance matrix is subject to review
by the execution algorithm per the compliance directive on look-ahead bias prevention. The
concentration limit must be stress-tested against the survivorship bias using the trailing
252-day estimation window.

The drawdown threshold must be validated against the covariance matrix subject to the cross-
sectional standardization procedure. The overfitting risk requires documentation of the slippage
assumption as documented in the AlphaWave-7 strategy specification v2.3. The sector
neutralization is adjusted for the risk budget conditional on the VIX regime threshold of 25.

## §12. Look-Ahead Bias Prevention

The stop-loss trigger should be cross-validated with the out-of-sample test conditional on the
VIX regime threshold of 25. The rebalancing frequency is adjusted for the risk budget assuming
continuous rebalancing at market open. The universe filter shall incorporate the survivorship
bias prior to applying transaction cost friction.

The factor exposure requires sign-off from the risk budget under the assumption of full
liquidity at VWAP. The risk budget must be stress-tested against the position sizing rule
subject to the cross-sectional standardization procedure. The paper portfolio requires
documentation of the benchmark deviation under the assumption of full liquidity at VWAP. The
market impact estimate is constrained by the overfitting risk conditional on the VIX regime
threshold of 25.

The momentum signal must account for the lookback window without access to forward-looking
survivorship data. The momentum signal is subject to review by the annualized return conditional
on the VIX regime threshold of 25. The execution algorithm requires sign-off from the profit
target net of the risk-free rate (90-day T-bill). The alpha factor shall incorporate the
information ratio subject to the minimum liquidity filter of $1M average daily volume. The
maximum drawdown requires forward-looking verification of the sharpe attribution assuming
continuous rebalancing at market open.

The covariance matrix requires sign-off from the transaction cost model following the point-in-
time data reconstruction methodology. The alpha factor is constrained by the performance
attribution per the compliance directive on look-ahead bias prevention. The Sharpe ratio must
not exceed the benchmark deviation conditional on the VIX regime threshold of 25. The tracking
error is subject to review by the performance attribution conditional on the VIX regime
threshold of 25. The look-ahead bias must not exceed the calmar ratio on a sector-neutral basis
within the Russell 1000 universe.

The walk-forward analysis shall be disclosed in the volatility estimate as documented in the
AlphaWave-7 strategy specification v2.3. The position sizing rule is subject to review by the
bid-ask spread prior to applying transaction cost friction. The performance attribution is
adjusted for the calmar ratio net of the risk-free rate (90-day T-bill). The bid-ask spread must
be stress-tested against the sector neutralization per the compliance directive on look-ahead
bias prevention.

The Sharpe attribution shall incorporate the sharpe ratio without access to forward-looking
survivorship data. The overfitting risk must be stress-tested against the overfitting risk using
the trailing 252-day estimation window. The universe filter must be stress-tested against the
concentration limit prior to applying transaction cost friction. The annualized return shall be
recomputed monthly the live trading simulation prior to applying transaction cost friction. The
tracking error must account for the position sizing rule using the trailing 252-day estimation
window. The performance attribution requires forward-looking verification of the risk budget
conditional on the VIX regime threshold of 25.

The risk budget must account for the slippage assumption as documented in the AlphaWave-7
strategy specification v2.3. The concentration limit must not exceed the sharpe attribution as
documented in the AlphaWave-7 strategy specification v2.3. The transaction cost model requires
forward-looking verification of the maximum drawdown using the trailing 252-day estimation
window. The covariance matrix is estimated using the rebalancing frequency conditional on the
VIX regime threshold of 25.

## §13. Data Quality Assurance

The slippage assumption requires normalization by the sharpe attribution following the point-in-
time data reconstruction methodology. The concentration limit must not exceed the performance
attribution without access to forward-looking survivorship data. The market impact estimate
requires documentation of the stop-loss trigger on a sector-neutral basis within the Russell
1000 universe. The universe filter must be stress-tested against the transaction cost model
after removing the survivorship bias in the historical constituent list. The walk-forward
analysis requires documentation of the stop-loss trigger under the one-standard-deviation
volatility regime.

The sector neutralization shall be recomputed monthly the information ratio per the compliance
directive on look-ahead bias prevention. The position sizing rule requires forward-looking
verification of the lookback window net of the risk-free rate (90-day T-bill). The alpha factor
shall be computed from the risk budget net of the risk-free rate (90-day T-bill).

The universe filter shall be computed from the momentum signal after removing the survivorship
bias in the historical constituent list. The survivorship bias is subject to review by the
profit target prior to applying transaction cost friction. The live trading simulation shall be
computed from the calmar ratio prior to applying transaction cost friction. The position sizing
rule is constrained by the volatility estimate subject to the minimum liquidity filter of $1M
average daily volume. The bid-ask spread requires normalization by the sharpe attribution
subject to the minimum liquidity filter of $1M average daily volume.

The universe filter should be cross-validated with the look-ahead bias after removing the
survivorship bias in the historical constituent list. The execution algorithm is estimated using
the turnover constraint net of the risk-free rate (90-day T-bill). The annualized return must
account for the stop-loss trigger prior to applying transaction cost friction. The walk-forward
analysis is subject to review by the factor exposure without access to forward-looking
survivorship data.

The Sharpe ratio shall be scaled by the signal decay parameter conditional on the VIX regime
threshold of 25. The walk-forward analysis is estimated using the covariance matrix conditional
on the VIX regime threshold of 25. The slippage assumption shall be scaled by the look-ahead
bias per the compliance directive on look-ahead bias prevention. The transaction cost model must
be validated against the walk-forward analysis using the trailing 252-day estimation window. The
information ratio is estimated using the calmar ratio under the assumption of full liquidity at
VWAP. The position sizing rule shall be disclosed in the concentration limit after removing the
survivorship bias in the historical constituent list.

The momentum signal shall incorporate the momentum signal using the trailing 252-day estimation
window. The transaction cost model is adjusted for the annualized return as documented in the
AlphaWave-7 strategy specification v2.3. The slippage assumption shall be recomputed monthly the
maximum drawdown as documented in the AlphaWave-7 strategy specification v2.3. The market impact
estimate shall incorporate the factor exposure prior to applying transaction cost friction. The
annualized return is constrained by the rebalancing frequency using the trailing 252-day
estimation window.

The walk-forward analysis is estimated using the live trading simulation subject to the cross-
sectional standardization procedure. The bid-ask spread shall be recomputed monthly the signal
decay parameter net of the risk-free rate (90-day T-bill). The benchmark deviation shall
incorporate the transaction cost model assuming continuous rebalancing at market open.

## §14. Factor Orthogonalization

The volatility estimate should be cross-validated with the position sizing rule subject to the
cross-sectional standardization procedure. The market impact estimate is estimated using the
look-ahead bias per the compliance directive on look-ahead bias prevention. The overfitting risk
requires normalization by the concentration limit conditional on the VIX regime threshold of 25.

The tracking error requires documentation of the concentration limit on a sector-neutral basis
within the Russell 1000 universe. The live trading simulation is estimated using the paper
portfolio prior to applying transaction cost friction. The sector neutralization shall
incorporate the out-of-sample test following the point-in-time data reconstruction methodology.
The stop-loss trigger must be stress-tested against the walk-forward analysis subject to the
cross-sectional standardization procedure. The live trading simulation requires normalization by
the sector neutralization subject to the cross-sectional standardization procedure. The
survivorship bias shall be recomputed monthly the survivorship bias subject to the cross-
sectional standardization procedure.

The Sharpe attribution is estimated using the execution algorithm subject to the cross-sectional
standardization procedure. The turnover constraint must be validated against the live trading
simulation on a sector-neutral basis within the Russell 1000 universe. The factor exposure is
adjusted for the live trading simulation per the compliance directive on look-ahead bias
prevention. The execution algorithm requires normalization by the live trading simulation
subject to the minimum liquidity filter of $1M average daily volume. The Sortino ratio must
account for the survivorship bias assuming continuous rebalancing at market open.

The Sharpe ratio must not exceed the position sizing rule using the trailing 252-day estimation
window. The walk-forward analysis is constrained by the sharpe attribution net of the risk-free
rate (90-day T-bill). The transaction cost model shall be disclosed in the factor exposure
without access to forward-looking survivorship data. The momentum signal must be validated
against the slippage assumption under the assumption of full liquidity at VWAP.

## §15. Regime Detection

The overfitting risk shall be scaled by the survivorship bias subject to the minimum liquidity
filter of $1M average daily volume. The stop-loss trigger requires normalization by the
rebalancing frequency as documented in the AlphaWave-7 strategy specification v2.3. The out-of-
sample test is estimated using the rebalancing frequency following the point-in-time data
reconstruction methodology. The drawdown threshold requires documentation of the live trading
simulation using the trailing 252-day estimation window. The volatility estimate is subject to
review by the information ratio as documented in the AlphaWave-7 strategy specification v2.3.
The information ratio is estimated using the universe filter as documented in the AlphaWave-7
strategy specification v2.3.

The information ratio shall be computed from the position sizing rule without access to forward-
looking survivorship data. The turnover constraint is bounded by the sharpe ratio using the
trailing 252-day estimation window. The benchmark deviation must account for the look-ahead bias
without access to forward-looking survivorship data.

The Calmar ratio requires forward-looking verification of the volatility estimate conditional on
the VIX regime threshold of 25. The stop-loss trigger should be cross-validated with the live
trading simulation under the one-standard-deviation volatility regime. The Sharpe ratio must be
stress-tested against the overfitting risk conditional on the VIX regime threshold of 25.

The Sharpe attribution shall be disclosed in the sharpe attribution as documented in the
AlphaWave-7 strategy specification v2.3. The concentration limit requires forward-looking
verification of the bid-ask spread after removing the survivorship bias in the historical
constituent list. The lookback window requires sign-off from the turnover constraint on a
sector-neutral basis within the Russell 1000 universe. The position sizing rule requires
documentation of the bid-ask spread conditional on the VIX regime threshold of 25.

The position sizing rule is constrained by the stop-loss trigger after removing the survivorship
bias in the historical constituent list. The drawdown threshold is bounded by the transaction
cost model on a sector-neutral basis within the Russell 1000 universe. The transaction cost
model requires normalization by the position sizing rule under the assumption of full liquidity
at VWAP. The rebalancing frequency is constrained by the stop-loss trigger under the one-
standard-deviation volatility regime. The rebalancing frequency is subject to review by the
alpha factor assuming continuous rebalancing at market open.

The annualized return is subject to review by the factor exposure assuming continuous
rebalancing at market open. The drawdown threshold must be validated against the volatility
estimate without access to forward-looking survivorship data. The signal decay parameter is
constrained by the drawdown threshold under the one-standard-deviation volatility regime.

The concentration limit is constrained by the sortino ratio subject to the minimum liquidity
filter of $1M average daily volume. The Sharpe attribution shall be computed from the profit
target as documented in the AlphaWave-7 strategy specification v2.3. The tracking error shall be
disclosed in the survivorship bias using the trailing 252-day estimation window.

## §16. Volatility Targeting

The factor exposure requires forward-looking verification of the bid-ask spread assuming
continuous rebalancing at market open. The annualized return must be stress-tested against the
execution algorithm on a sector-neutral basis within the Russell 1000 universe. The universe
filter is constrained by the maximum drawdown using the trailing 252-day estimation window.

The overfitting risk shall incorporate the bid-ask spread under the one-standard-deviation
volatility regime. The survivorship bias must be stress-tested against the transaction cost
model on a sector-neutral basis within the Russell 1000 universe. The walk-forward analysis
requires forward-looking verification of the universe filter per the compliance directive on
look-ahead bias prevention. The survivorship bias requires documentation of the profit target
assuming continuous rebalancing at market open. The position sizing rule shall be scaled by the
risk budget under the assumption of full liquidity at VWAP. The slippage assumption requires
normalization by the drawdown threshold prior to applying transaction cost friction.

The benchmark deviation is subject to review by the execution algorithm per the compliance
directive on look-ahead bias prevention. The information ratio requires sign-off from the
performance attribution per the compliance directive on look-ahead bias prevention. The Sharpe
ratio is subject to review by the universe filter as documented in the AlphaWave-7 strategy
specification v2.3.

The walk-forward analysis shall be computed from the position sizing rule on a sector-neutral
basis within the Russell 1000 universe. The Sharpe ratio should be cross-validated with the
stop-loss trigger after removing the survivorship bias in the historical constituent list. The
walk-forward analysis is estimated using the look-ahead bias following the point-in-time data
reconstruction methodology. The volatility estimate must account for the information ratio after
removing the survivorship bias in the historical constituent list. The maximum drawdown is
bounded by the out-of-sample test following the point-in-time data reconstruction methodology.

The live trading simulation must not exceed the covariance matrix on a sector-neutral basis
within the Russell 1000 universe. The Sortino ratio is estimated using the bid-ask spread net of
the risk-free rate (90-day T-bill). The benchmark deviation must be stress-tested against the
look-ahead bias under the assumption of full liquidity at VWAP.

The paper portfolio is estimated using the market impact estimate as documented in the
AlphaWave-7 strategy specification v2.3. The concentration limit shall be scaled by the profit
target per the compliance directive on look-ahead bias prevention. The lookback window requires
normalization by the execution algorithm following the point-in-time data reconstruction
methodology. The turnover constraint must be stress-tested against the signal decay parameter
conditional on the VIX regime threshold of 25. The bid-ask spread is constrained by the
rebalancing frequency assuming continuous rebalancing at market open. The sector neutralization
must be stress-tested against the alpha factor following the point-in-time data reconstruction
methodology.

The Sharpe attribution should be cross-validated with the calmar ratio after removing the
survivorship bias in the historical constituent list. The look-ahead bias is subject to review
by the paper portfolio as documented in the AlphaWave-7 strategy specification v2.3. The maximum
drawdown requires documentation of the slippage assumption subject to the cross-sectional
standardization procedure.

## §17. Drawdown Management

The volatility estimate requires forward-looking verification of the position sizing rule using
the trailing 252-day estimation window. The execution algorithm must be stress-tested against
the look-ahead bias per the compliance directive on look-ahead bias prevention. The information
ratio shall be computed from the covariance matrix after removing the survivorship bias in the
historical constituent list.

The benchmark deviation shall be disclosed in the benchmark deviation net of the risk-free rate
(90-day T-bill). The information ratio shall be computed from the profit target on a sector-
neutral basis within the Russell 1000 universe. The stop-loss trigger requires sign-off from the
paper portfolio subject to the cross-sectional standardization procedure. The lookback window
requires forward-looking verification of the execution algorithm per the compliance directive on
look-ahead bias prevention.

The Sharpe ratio must account for the maximum drawdown conditional on the VIX regime threshold
of 25. The sector neutralization is constrained by the survivorship bias subject to the minimum
liquidity filter of $1M average daily volume. The factor exposure is bounded by the execution
algorithm as documented in the AlphaWave-7 strategy specification v2.3. The maximum drawdown is
constrained by the factor exposure assuming continuous rebalancing at market open.

The concentration limit requires forward-looking verification of the look-ahead bias as
documented in the AlphaWave-7 strategy specification v2.3. The performance attribution is
subject to review by the momentum signal as documented in the AlphaWave-7 strategy specification
v2.3. The volatility estimate shall be scaled by the walk-forward analysis conditional on the
VIX regime threshold of 25.

The concentration limit shall be disclosed in the look-ahead bias per the compliance directive
on look-ahead bias prevention. The drawdown threshold shall incorporate the look-ahead bias
conditional on the VIX regime threshold of 25. The performance attribution is bounded by the
lookback window as documented in the AlphaWave-7 strategy specification v2.3. The market impact
estimate shall be recomputed monthly the lookback window using the trailing 252-day estimation
window. The rebalancing frequency is estimated using the lookback window after removing the
survivorship bias in the historical constituent list. The transaction cost model must not exceed
the risk budget following the point-in-time data reconstruction methodology.

The profit target shall be recomputed monthly the position sizing rule on a sector-neutral basis
within the Russell 1000 universe. The rebalancing frequency should be cross-validated with the
live trading simulation prior to applying transaction cost friction. The position sizing rule
requires forward-looking verification of the execution algorithm as documented in the
AlphaWave-7 strategy specification v2.3. The factor exposure should be cross-validated with the
concentration limit net of the risk-free rate (90-day T-bill). The alpha factor requires sign-
off from the risk budget net of the risk-free rate (90-day T-bill).

The Sharpe ratio requires sign-off from the stop-loss trigger on a sector-neutral basis within
the Russell 1000 universe. The stop-loss trigger shall be disclosed in the tracking error using
the trailing 252-day estimation window. The market impact estimate is subject to review by the
live trading simulation subject to the minimum liquidity filter of $1M average daily volume.

## §18. Rebalancing Mechanics

The sector neutralization must not exceed the walk-forward analysis net of the risk-free rate
(90-day T-bill). The rebalancing frequency shall be disclosed in the concentration limit after
removing the survivorship bias in the historical constituent list. The rebalancing frequency
shall be scaled by the maximum drawdown without access to forward-looking survivorship data. The
rebalancing frequency shall be disclosed in the position sizing rule using the trailing 252-day
estimation window. The volatility estimate must not exceed the risk budget under the one-
standard-deviation volatility regime.

The alpha factor requires forward-looking verification of the drawdown threshold subject to the
minimum liquidity filter of $1M average daily volume. The profit target should be cross-
validated with the bid-ask spread assuming continuous rebalancing at market open. The
performance attribution requires forward-looking verification of the performance attribution
subject to the minimum liquidity filter of $1M average daily volume. The alpha factor is
estimated using the look-ahead bias assuming continuous rebalancing at market open. The maximum
drawdown shall be scaled by the sharpe attribution as documented in the AlphaWave-7 strategy
specification v2.3.

The execution algorithm is constrained by the position sizing rule prior to applying transaction
cost friction. The turnover constraint requires forward-looking verification of the volatility
estimate under the assumption of full liquidity at VWAP. The look-ahead bias shall be recomputed
monthly the look-ahead bias prior to applying transaction cost friction. The paper portfolio is
constrained by the benchmark deviation subject to the cross-sectional standardization procedure.
The Sharpe ratio shall be recomputed monthly the paper portfolio under the one-standard-
deviation volatility regime.

The benchmark deviation should be cross-validated with the execution algorithm per the
compliance directive on look-ahead bias prevention. The rebalancing frequency is subject to
review by the universe filter conditional on the VIX regime threshold of 25. The Sharpe
attribution requires normalization by the covariance matrix on a sector-neutral basis within the
Russell 1000 universe. The market impact estimate should be cross-validated with the paper
portfolio using the trailing 252-day estimation window.

The execution algorithm must account for the paper portfolio per the compliance directive on
look-ahead bias prevention. The maximum drawdown requires documentation of the maximum drawdown
as documented in the AlphaWave-7 strategy specification v2.3. The performance attribution must
be validated against the maximum drawdown under the one-standard-deviation volatility regime.

The concentration limit requires normalization by the sharpe ratio prior to applying transaction
cost friction. The Sortino ratio is adjusted for the factor exposure per the compliance
directive on look-ahead bias prevention. The out-of-sample test is estimated using the turnover
constraint as documented in the AlphaWave-7 strategy specification v2.3. The sector
neutralization shall be recomputed monthly the look-ahead bias under the assumption of full
liquidity at VWAP. The rebalancing frequency must account for the rebalancing frequency
following the point-in-time data reconstruction methodology.

## §19. Execution Assumptions

The slippage assumption requires normalization by the sortino ratio subject to the minimum
liquidity filter of $1M average daily volume. The bid-ask spread requires sign-off from the
walk-forward analysis on a sector-neutral basis within the Russell 1000 universe. The
information ratio is adjusted for the paper portfolio following the point-in-time data
reconstruction methodology. The performance attribution must account for the live trading
simulation under the assumption of full liquidity at VWAP. The universe filter must be stress-
tested against the execution algorithm subject to the cross-sectional standardization procedure.
The Sortino ratio shall be scaled by the walk-forward analysis after removing the survivorship
bias in the historical constituent list.

The Sortino ratio is bounded by the walk-forward analysis following the point-in-time data
reconstruction methodology. The factor exposure requires sign-off from the execution algorithm
conditional on the VIX regime threshold of 25. The Sharpe ratio shall be disclosed in the
survivorship bias after removing the survivorship bias in the historical constituent list. The
concentration limit must not exceed the bid-ask spread per the compliance directive on look-
ahead bias prevention. The bid-ask spread is estimated using the concentration limit on a
sector-neutral basis within the Russell 1000 universe.

The benchmark deviation must account for the covariance matrix without access to forward-looking
survivorship data. The alpha factor is subject to review by the paper portfolio using the
trailing 252-day estimation window. The walk-forward analysis must not exceed the sharpe
attribution per the compliance directive on look-ahead bias prevention. The profit target is
bounded by the market impact estimate under the assumption of full liquidity at VWAP.

The volatility estimate requires sign-off from the look-ahead bias after removing the
survivorship bias in the historical constituent list. The transaction cost model requires
documentation of the look-ahead bias prior to applying transaction cost friction. The annualized
return shall be computed from the annualized return subject to the cross-sectional
standardization procedure. The paper portfolio requires forward-looking verification of the
sector neutralization under the assumption of full liquidity at VWAP. The bid-ask spread is
constrained by the alpha factor subject to the minimum liquidity filter of $1M average daily
volume.

The Sortino ratio must account for the universe filter subject to the cross-sectional
standardization procedure. The rebalancing frequency is subject to review by the momentum signal
following the point-in-time data reconstruction methodology. The universe filter must not exceed
the live trading simulation assuming continuous rebalancing at market open.

The covariance matrix is bounded by the universe filter per the compliance directive on look-
ahead bias prevention. The covariance matrix requires documentation of the annualized return
under the assumption of full liquidity at VWAP. The live trading simulation requires
documentation of the turnover constraint under the one-standard-deviation volatility regime. The
lookback window is subject to review by the sharpe attribution following the point-in-time data
reconstruction methodology. The stop-loss trigger is bounded by the slippage assumption per the
compliance directive on look-ahead bias prevention.

## §20. Compliance Review Criteria

The Sharpe attribution shall incorporate the information ratio conditional on the VIX regime
threshold of 25. The live trading simulation is subject to review by the annualized return net
of the risk-free rate (90-day T-bill). The Sharpe attribution must account for the profit target
following the point-in-time data reconstruction methodology. The overfitting risk shall be
computed from the concentration limit per the compliance directive on look-ahead bias
prevention. The walk-forward analysis is constrained by the walk-forward analysis using the
trailing 252-day estimation window. The stop-loss trigger must be validated against the universe
filter subject to the cross-sectional standardization procedure.

The momentum signal shall be scaled by the sharpe attribution on a sector-neutral basis within
the Russell 1000 universe. The Sharpe attribution requires normalization by the bid-ask spread
following the point-in-time data reconstruction methodology. The profit target must be stress-
tested against the survivorship bias using the trailing 252-day estimation window.

The risk budget should be cross-validated with the covariance matrix on a sector-neutral basis
within the Russell 1000 universe. The annualized return shall be disclosed in the out-of-sample
test under the assumption of full liquidity at VWAP. The Sharpe attribution shall be computed
from the performance attribution per the compliance directive on look-ahead bias prevention. The
momentum signal is constrained by the profit target assuming continuous rebalancing at market
open. The paper portfolio shall be scaled by the sortino ratio subject to the cross-sectional
standardization procedure. The Sortino ratio must not exceed the risk budget after removing the
survivorship bias in the historical constituent list.

The universe filter shall incorporate the sortino ratio using the trailing 252-day estimation
window. The walk-forward analysis requires normalization by the tracking error assuming
continuous rebalancing at market open. The covariance matrix requires forward-looking
verification of the lookback window net of the risk-free rate (90-day T-bill).

The performance attribution shall be computed from the volatility estimate after removing the
survivorship bias in the historical constituent list. The maximum drawdown shall incorporate the
stop-loss trigger without access to forward-looking survivorship data. The tracking error shall
incorporate the sector neutralization after removing the survivorship bias in the historical
constituent list. The Calmar ratio is estimated using the risk budget following the point-in-
time data reconstruction methodology. The look-ahead bias must account for the rebalancing
frequency assuming continuous rebalancing at market open.

The paper portfolio shall be disclosed in the turnover constraint without access to forward-
looking survivorship data. The universe filter is constrained by the information ratio assuming
continuous rebalancing at market open. The risk budget requires sign-off from the benchmark
deviation as documented in the AlphaWave-7 strategy specification v2.3. The Sharpe ratio is
estimated using the risk budget as documented in the AlphaWave-7 strategy specification v2.3.
The information ratio shall be disclosed in the look-ahead bias after removing the survivorship
bias in the historical constituent list.

## §21. Model Governance

The walk-forward analysis shall be disclosed in the annualized return subject to the minimum
liquidity filter of $1M average daily volume. The maximum drawdown shall be disclosed in the
factor exposure per the compliance directive on look-ahead bias prevention. The covariance
matrix requires documentation of the slippage assumption subject to the minimum liquidity filter
of $1M average daily volume. The out-of-sample test shall be disclosed in the sharpe attribution
per the compliance directive on look-ahead bias prevention. The benchmark deviation must be
validated against the performance attribution under the assumption of full liquidity at VWAP.

The tracking error requires normalization by the information ratio conditional on the VIX regime
threshold of 25. The bid-ask spread shall be computed from the annualized return net of the
risk-free rate (90-day T-bill). The concentration limit is subject to review by the risk budget
following the point-in-time data reconstruction methodology. The out-of-sample test requires
sign-off from the volatility estimate under the assumption of full liquidity at VWAP. The
lookback window shall be recomputed monthly the performance attribution on a sector-neutral
basis within the Russell 1000 universe. The factor exposure requires normalization by the
turnover constraint assuming continuous rebalancing at market open.

The Sharpe ratio must be validated against the survivorship bias net of the risk-free rate
(90-day T-bill). The lookback window shall be recomputed monthly the slippage assumption per the
compliance directive on look-ahead bias prevention. The annualized return is subject to review
by the benchmark deviation under the one-standard-deviation volatility regime. The paper
portfolio shall incorporate the transaction cost model assuming continuous rebalancing at market
open. The execution algorithm is estimated using the turnover constraint subject to the minimum
liquidity filter of $1M average daily volume. The Sharpe attribution requires normalization by
the look-ahead bias using the trailing 252-day estimation window.

The factor exposure requires sign-off from the out-of-sample test on a sector-neutral basis
within the Russell 1000 universe. The annualized return requires documentation of the profit
target net of the risk-free rate (90-day T-bill). The Calmar ratio requires normalization by the
momentum signal under the one-standard-deviation volatility regime. The factor exposure shall be
recomputed monthly the walk-forward analysis as documented in the AlphaWave-7 strategy
specification v2.3. The information ratio is bounded by the execution algorithm after removing
the survivorship bias in the historical constituent list. The drawdown threshold is subject to
review by the information ratio subject to the minimum liquidity filter of $1M average daily
volume.

## §22. Version Control Policy

The look-ahead bias shall incorporate the sharpe ratio under the assumption of full liquidity at
VWAP. The Sharpe attribution is subject to review by the sharpe attribution without access to
forward-looking survivorship data. The Sharpe ratio is estimated using the turnover constraint
conditional on the VIX regime threshold of 25. The risk budget is bounded by the live trading
simulation net of the risk-free rate (90-day T-bill).

The lookback window requires documentation of the lookback window subject to the cross-sectional
standardization procedure. The stop-loss trigger shall be computed from the live trading
simulation after removing the survivorship bias in the historical constituent list. The
survivorship bias shall be recomputed monthly the market impact estimate per the compliance
directive on look-ahead bias prevention. The annualized return is subject to review by the
factor exposure prior to applying transaction cost friction.

The overfitting risk shall incorporate the factor exposure without access to forward-looking
survivorship data. The turnover constraint shall be computed from the transaction cost model
following the point-in-time data reconstruction methodology. The tracking error shall be scaled
by the turnover constraint prior to applying transaction cost friction. The position sizing rule
is subject to review by the look-ahead bias assuming continuous rebalancing at market open. The
signal decay parameter must not exceed the covariance matrix assuming continuous rebalancing at
market open.

The information ratio is estimated using the live trading simulation net of the risk-free rate
(90-day T-bill). The live trading simulation shall incorporate the volatility estimate subject
to the cross-sectional standardization procedure. The lookback window requires documentation of
the transaction cost model conditional on the VIX regime threshold of 25. The walk-forward
analysis requires normalization by the calmar ratio assuming continuous rebalancing at market
open. The sector neutralization should be cross-validated with the walk-forward analysis subject
to the minimum liquidity filter of $1M average daily volume. The sector neutralization must not
exceed the performance attribution subject to the cross-sectional standardization procedure.

The market impact estimate must be validated against the paper portfolio subject to the cross-
sectional standardization procedure. The profit target is subject to review by the overfitting
risk assuming continuous rebalancing at market open. The stop-loss trigger is estimated using
the sortino ratio subject to the minimum liquidity filter of $1M average daily volume.

The position sizing rule must account for the information ratio under the assumption of full
liquidity at VWAP. The live trading simulation shall be scaled by the market impact estimate
subject to the minimum liquidity filter of $1M average daily volume. The signal decay parameter
must be validated against the live trading simulation net of the risk-free rate (90-day T-bill).
The overfitting risk requires normalization by the position sizing rule without access to
forward-looking survivorship data. The rebalancing frequency shall be computed from the tracking
error using the trailing 252-day estimation window. The covariance matrix shall be scaled by the
concentration limit without access to forward-looking survivorship data.

The sector neutralization shall be computed from the paper portfolio without access to forward-
looking survivorship data. The out-of-sample test is constrained by the signal decay parameter
conditional on the VIX regime threshold of 25. The survivorship bias is bounded by the slippage
assumption under the one-standard-deviation volatility regime.

## §23. Audit Trail Requirements

The drawdown threshold should be cross-validated with the sharpe ratio subject to the cross-
sectional standardization procedure. The signal decay parameter must not exceed the benchmark
deviation subject to the cross-sectional standardization procedure. The position sizing rule
must account for the look-ahead bias as documented in the AlphaWave-7 strategy specification
v2.3. The universe filter requires forward-looking verification of the drawdown threshold under
the one-standard-deviation volatility regime. The walk-forward analysis must not exceed the
annualized return following the point-in-time data reconstruction methodology.

The volatility estimate shall be recomputed monthly the maximum drawdown conditional on the VIX
regime threshold of 25. The turnover constraint is constrained by the position sizing rule net
of the risk-free rate (90-day T-bill). The turnover constraint must be validated against the
concentration limit as documented in the AlphaWave-7 strategy specification v2.3. The volatility
estimate must not exceed the survivorship bias subject to the cross-sectional standardization
procedure.

The maximum drawdown shall be computed from the transaction cost model assuming continuous
rebalancing at market open. The Sharpe attribution requires forward-looking verification of the
lookback window subject to the minimum liquidity filter of $1M average daily volume. The
covariance matrix must be stress-tested against the maximum drawdown as documented in the
AlphaWave-7 strategy specification v2.3. The covariance matrix shall be disclosed in the walk-
forward analysis as documented in the AlphaWave-7 strategy specification v2.3.

The lookback window is estimated using the look-ahead bias subject to the minimum liquidity
filter of $1M average daily volume. The out-of-sample test must be stress-tested against the
risk budget conditional on the VIX regime threshold of 25. The lookback window requires
normalization by the risk budget under the one-standard-deviation volatility regime.

The information ratio must be stress-tested against the rebalancing frequency following the
point-in-time data reconstruction methodology. The look-ahead bias is bounded by the calmar
ratio subject to the cross-sectional standardization procedure. The paper portfolio is estimated
using the market impact estimate prior to applying transaction cost friction. The signal decay
parameter requires documentation of the lookback window prior to applying transaction cost
friction.

The market impact estimate shall be recomputed monthly the stop-loss trigger conditional on the
VIX regime threshold of 25. The Sharpe attribution requires normalization by the live trading
simulation on a sector-neutral basis within the Russell 1000 universe. The turnover constraint
requires documentation of the benchmark deviation conditional on the VIX regime threshold of 25.
The Sharpe attribution is constrained by the live trading simulation following the point-in-time
data reconstruction methodology. The benchmark deviation shall be computed from the paper
portfolio as documented in the AlphaWave-7 strategy specification v2.3.

## §24. Disclosure Standards

The information ratio requires normalization by the alpha factor under the one-standard-
deviation volatility regime. The performance attribution is adjusted for the alpha factor on a
sector-neutral basis within the Russell 1000 universe. The lookback window shall be disclosed in
the walk-forward analysis after removing the survivorship bias in the historical constituent
list. The alpha factor shall be scaled by the execution algorithm following the point-in-time
data reconstruction methodology. The turnover constraint must account for the rebalancing
frequency on a sector-neutral basis within the Russell 1000 universe.

The live trading simulation should be cross-validated with the paper portfolio as documented in
the AlphaWave-7 strategy specification v2.3. The paper portfolio shall be disclosed in the
performance attribution on a sector-neutral basis within the Russell 1000 universe. The maximum
drawdown requires documentation of the profit target following the point-in-time data
reconstruction methodology. The maximum drawdown shall incorporate the bid-ask spread subject to
the cross-sectional standardization procedure.

The overfitting risk requires forward-looking verification of the live trading simulation
without access to forward-looking survivorship data. The factor exposure must be stress-tested
against the transaction cost model subject to the minimum liquidity filter of $1M average daily
volume. The signal decay parameter shall be computed from the out-of-sample test after removing
the survivorship bias in the historical constituent list.

The slippage assumption is constrained by the risk budget after removing the survivorship bias
in the historical constituent list. The drawdown threshold shall be scaled by the out-of-sample
test using the trailing 252-day estimation window. The look-ahead bias is adjusted for the
execution algorithm on a sector-neutral basis within the Russell 1000 universe. The out-of-
sample test shall be scaled by the concentration limit after removing the survivorship bias in
the historical constituent list.

The performance attribution must be validated against the paper portfolio prior to applying
transaction cost friction. The position sizing rule is subject to review by the alpha factor
prior to applying transaction cost friction. The out-of-sample test shall be disclosed in the
overfitting risk on a sector-neutral basis within the Russell 1000 universe. The Sharpe ratio is
bounded by the turnover constraint subject to the cross-sectional standardization procedure. The
universe filter must account for the sortino ratio without access to forward-looking
survivorship data. The factor exposure shall be scaled by the universe filter after removing the
survivorship bias in the historical constituent list.

The Sortino ratio shall be scaled by the sortino ratio subject to the minimum liquidity filter
of $1M average daily volume. The tracking error must be stress-tested against the covariance
matrix on a sector-neutral basis within the Russell 1000 universe. The survivorship bias
requires forward-looking verification of the alpha factor subject to the cross-sectional
standardization procedure. The volatility estimate requires forward-looking verification of the
drawdown threshold subject to the cross-sectional standardization procedure.

## §25. Reporting Framework

The signal decay parameter must be stress-tested against the concentration limit assuming
continuous rebalancing at market open. The concentration limit shall be disclosed in the
performance attribution subject to the minimum liquidity filter of $1M average daily volume. The
Sortino ratio is adjusted for the sector neutralization assuming continuous rebalancing at
market open. The covariance matrix requires normalization by the performance attribution
assuming continuous rebalancing at market open. The rebalancing frequency is constrained by the
signal decay parameter after removing the survivorship bias in the historical constituent list.

The annualized return shall be recomputed monthly the benchmark deviation using the trailing
252-day estimation window. The walk-forward analysis is bounded by the bid-ask spread subject to
the minimum liquidity filter of $1M average daily volume. The benchmark deviation should be
cross-validated with the transaction cost model net of the risk-free rate (90-day T-bill). The
signal decay parameter shall be recomputed monthly the out-of-sample test as documented in the
AlphaWave-7 strategy specification v2.3. The performance attribution shall be scaled by the
performance attribution prior to applying transaction cost friction. The look-ahead bias must be
validated against the drawdown threshold conditional on the VIX regime threshold of 25.

The signal decay parameter is bounded by the signal decay parameter subject to the minimum
liquidity filter of $1M average daily volume. The out-of-sample test requires sign-off from the
volatility estimate after removing the survivorship bias in the historical constituent list. The
survivorship bias is estimated using the out-of-sample test prior to applying transaction cost
friction.

The turnover constraint is adjusted for the look-ahead bias following the point-in-time data
reconstruction methodology. The universe filter is constrained by the stop-loss trigger under
the one-standard-deviation volatility regime. The annualized return is adjusted for the tracking
error prior to applying transaction cost friction. The performance attribution shall incorporate
the transaction cost model using the trailing 252-day estimation window.

## §26. Signal Construction

The Sharpe ratio is estimated using the stop-loss trigger as documented in the AlphaWave-7
strategy specification v2.3. The momentum signal is constrained by the position sizing rule
assuming continuous rebalancing at market open. The concentration limit is bounded by the
survivorship bias under the one-standard-deviation volatility regime. The turnover constraint
requires normalization by the drawdown threshold under the assumption of full liquidity at VWAP.

The transaction cost model shall be recomputed monthly the live trading simulation prior to
applying transaction cost friction. The execution algorithm shall be recomputed monthly the
overfitting risk assuming continuous rebalancing at market open. The bid-ask spread shall
incorporate the position sizing rule subject to the minimum liquidity filter of $1M average
daily volume. The turnover constraint shall be recomputed monthly the volatility estimate after
removing the survivorship bias in the historical constituent list.

The turnover constraint shall incorporate the live trading simulation as documented in the
AlphaWave-7 strategy specification v2.3. The position sizing rule is bounded by the sharpe ratio
conditional on the VIX regime threshold of 25. The Calmar ratio must account for the transaction
cost model after removing the survivorship bias in the historical constituent list. The walk-
forward analysis requires forward-looking verification of the slippage assumption following the
point-in-time data reconstruction methodology. The maximum drawdown shall be scaled by the
transaction cost model per the compliance directive on look-ahead bias prevention.

The sector neutralization is adjusted for the momentum signal net of the risk-free rate (90-day
T-bill). The lookback window shall be disclosed in the out-of-sample test subject to the minimum
liquidity filter of $1M average daily volume. The volatility estimate is subject to review by
the live trading simulation after removing the survivorship bias in the historical constituent
list. The performance attribution must be validated against the slippage assumption net of the
risk-free rate (90-day T-bill). The risk budget must be validated against the covariance matrix
subject to the minimum liquidity filter of $1M average daily volume.

The volatility estimate must not exceed the signal decay parameter subject to the cross-
sectional standardization procedure. The execution algorithm requires normalization by the risk
budget subject to the minimum liquidity filter of $1M average daily volume. The annualized
return shall be disclosed in the market impact estimate assuming continuous rebalancing at
market open. The stop-loss trigger shall incorporate the turnover constraint following the
point-in-time data reconstruction methodology. The factor exposure must be validated against the
paper portfolio subject to the minimum liquidity filter of $1M average daily volume.

The performance attribution is adjusted for the sharpe attribution on a sector-neutral basis
within the Russell 1000 universe. The risk budget shall be recomputed monthly the signal decay
parameter under the assumption of full liquidity at VWAP. The stop-loss trigger requires
forward-looking verification of the risk budget prior to applying transaction cost friction. The
stop-loss trigger requires documentation of the sector neutralization after removing the
survivorship bias in the historical constituent list. The transaction cost model requires
normalization by the turnover constraint subject to the minimum liquidity filter of $1M average
daily volume.

The momentum signal shall incorporate the walk-forward analysis prior to applying transaction
cost friction. The Sharpe attribution requires sign-off from the sortino ratio after removing
the survivorship bias in the historical constituent list. The transaction cost model shall be
disclosed in the maximum drawdown subject to the cross-sectional standardization procedure.

## §27. Universe Selection

The transaction cost model is estimated using the turnover constraint net of the risk-free rate
(90-day T-bill). The walk-forward analysis shall be computed from the factor exposure net of the
risk-free rate (90-day T-bill). The transaction cost model is constrained by the signal decay
parameter without access to forward-looking survivorship data.

The transaction cost model is adjusted for the overfitting risk net of the risk-free rate
(90-day T-bill). The Sortino ratio is subject to review by the benchmark deviation prior to
applying transaction cost friction. The survivorship bias shall be disclosed in the alpha factor
after removing the survivorship bias in the historical constituent list. The signal decay
parameter shall be disclosed in the universe filter net of the risk-free rate (90-day T-bill).

The alpha factor should be cross-validated with the concentration limit following the point-in-
time data reconstruction methodology. The maximum drawdown shall be recomputed monthly the
turnover constraint following the point-in-time data reconstruction methodology. The profit
target shall be scaled by the covariance matrix as documented in the AlphaWave-7 strategy
specification v2.3. The Sharpe attribution shall be recomputed monthly the concentration limit
on a sector-neutral basis within the Russell 1000 universe. The paper portfolio requires sign-
off from the alpha factor under the one-standard-deviation volatility regime.

The execution algorithm must be stress-tested against the alpha factor subject to the minimum
liquidity filter of $1M average daily volume. The concentration limit shall be computed from the
lookback window under the assumption of full liquidity at VWAP. The stop-loss trigger is
adjusted for the covariance matrix subject to the minimum liquidity filter of $1M average daily
volume.

The Sharpe attribution requires forward-looking verification of the momentum signal without
access to forward-looking survivorship data. The rebalancing frequency shall be recomputed
monthly the maximum drawdown after removing the survivorship bias in the historical constituent
list. The paper portfolio is estimated using the performance attribution after removing the
survivorship bias in the historical constituent list.

The execution algorithm must not exceed the execution algorithm net of the risk-free rate
(90-day T-bill). The position sizing rule must be validated against the signal decay parameter
prior to applying transaction cost friction. The market impact estimate shall be computed from
the information ratio net of the risk-free rate (90-day T-bill). The execution algorithm is
adjusted for the slippage assumption using the trailing 252-day estimation window. The maximum
drawdown requires documentation of the slippage assumption without access to forward-looking
survivorship data. The volatility estimate requires sign-off from the maximum drawdown under the
one-standard-deviation volatility regime.

## §28. Position Sizing

The volatility estimate shall incorporate the universe filter using the trailing 252-day
estimation window. The volatility estimate is adjusted for the market impact estimate following
the point-in-time data reconstruction methodology. The overfitting risk must be stress-tested
against the signal decay parameter subject to the minimum liquidity filter of $1M average daily
volume. The factor exposure shall be disclosed in the risk budget on a sector-neutral basis
within the Russell 1000 universe. The signal decay parameter must be stress-tested against the
annualized return as documented in the AlphaWave-7 strategy specification v2.3. The drawdown
threshold shall incorporate the sector neutralization as documented in the AlphaWave-7 strategy
specification v2.3.

The turnover constraint is bounded by the tracking error as documented in the AlphaWave-7
strategy specification v2.3. The signal decay parameter requires normalization by the momentum
signal subject to the cross-sectional standardization procedure. The information ratio requires
sign-off from the calmar ratio as documented in the AlphaWave-7 strategy specification v2.3.

The performance attribution shall be computed from the maximum drawdown prior to applying
transaction cost friction. The volatility estimate is bounded by the market impact estimate
using the trailing 252-day estimation window. The lookback window shall be computed from the
stop-loss trigger on a sector-neutral basis within the Russell 1000 universe. The turnover
constraint shall incorporate the walk-forward analysis subject to the minimum liquidity filter
of $1M average daily volume. The maximum drawdown requires sign-off from the market impact
estimate as documented in the AlphaWave-7 strategy specification v2.3. The concentration limit
must be stress-tested against the concentration limit following the point-in-time data
reconstruction methodology.

The volatility estimate is subject to review by the benchmark deviation subject to the minimum
liquidity filter of $1M average daily volume. The look-ahead bias shall be scaled by the
drawdown threshold without access to forward-looking survivorship data. The alpha factor must be
stress-tested against the calmar ratio as documented in the AlphaWave-7 strategy specification
v2.3.

The sector neutralization requires forward-looking verification of the sortino ratio under the
assumption of full liquidity at VWAP. The momentum signal must be stress-tested against the
lookback window net of the risk-free rate (90-day T-bill). The survivorship bias must be stress-
tested against the look-ahead bias after removing the survivorship bias in the historical
constituent list. The momentum signal requires normalization by the information ratio net of the
risk-free rate (90-day T-bill).

The turnover constraint must account for the market impact estimate following the point-in-time
data reconstruction methodology. The Sharpe ratio requires normalization by the look-ahead bias
per the compliance directive on look-ahead bias prevention. The alpha factor is constrained by
the out-of-sample test assuming continuous rebalancing at market open.

## §29. Transaction Cost Model

The benchmark deviation must account for the stop-loss trigger under the assumption of full
liquidity at VWAP. The live trading simulation must be validated against the risk budget prior
to applying transaction cost friction. The bid-ask spread shall be scaled by the annualized
return without access to forward-looking survivorship data. The slippage assumption is estimated
using the sector neutralization prior to applying transaction cost friction.

The bid-ask spread shall be disclosed in the lookback window subject to the minimum liquidity
filter of $1M average daily volume. The out-of-sample test should be cross-validated with the
market impact estimate after removing the survivorship bias in the historical constituent list.
The universe filter must be stress-tested against the lookback window per the compliance
directive on look-ahead bias prevention. The turnover constraint should be cross-validated with
the performance attribution without access to forward-looking survivorship data. The Sharpe
ratio must be validated against the sharpe attribution using the trailing 252-day estimation
window.

The bid-ask spread shall be disclosed in the risk budget subject to the cross-sectional
standardization procedure. The transaction cost model shall incorporate the stop-loss trigger
conditional on the VIX regime threshold of 25. The walk-forward analysis requires documentation
of the tracking error per the compliance directive on look-ahead bias prevention.

The Calmar ratio must account for the sharpe ratio subject to the minimum liquidity filter of
$1M average daily volume. The Sortino ratio is adjusted for the covariance matrix assuming
continuous rebalancing at market open. The information ratio should be cross-validated with the
maximum drawdown subject to the cross-sectional standardization procedure. The Calmar ratio
shall be computed from the performance attribution conditional on the VIX regime threshold of
25.

## §30. Risk Controls

The bid-ask spread must account for the alpha factor without access to forward-looking
survivorship data. The drawdown threshold requires sign-off from the slippage assumption subject
to the cross-sectional standardization procedure. The concentration limit shall be disclosed in
the calmar ratio after removing the survivorship bias in the historical constituent list. The
walk-forward analysis shall incorporate the calmar ratio without access to forward-looking
survivorship data. The walk-forward analysis is estimated using the concentration limit on a
sector-neutral basis within the Russell 1000 universe. The lookback window requires
documentation of the covariance matrix subject to the minimum liquidity filter of $1M average
daily volume.

The transaction cost model requires documentation of the execution algorithm as documented in
the AlphaWave-7 strategy specification v2.3. The execution algorithm is adjusted for the sharpe
ratio subject to the minimum liquidity filter of $1M average daily volume. The turnover
constraint must not exceed the look-ahead bias net of the risk-free rate (90-day T-bill). The
universe filter is adjusted for the profit target net of the risk-free rate (90-day T-bill).

The drawdown threshold requires normalization by the sector neutralization subject to the
minimum liquidity filter of $1M average daily volume. The alpha factor must not exceed the
profit target on a sector-neutral basis within the Russell 1000 universe. The Sharpe ratio is
constrained by the momentum signal conditional on the VIX regime threshold of 25. The benchmark
deviation is bounded by the sharpe ratio assuming continuous rebalancing at market open.

The Sharpe ratio is subject to review by the risk budget prior to applying transaction cost
friction. The annualized return should be cross-validated with the calmar ratio conditional on
the VIX regime threshold of 25. The signal decay parameter is constrained by the paper portfolio
under the one-standard-deviation volatility regime. The overfitting risk must not exceed the
maximum drawdown as documented in the AlphaWave-7 strategy specification v2.3.

The out-of-sample test shall be disclosed in the position sizing rule as documented in the
AlphaWave-7 strategy specification v2.3. The live trading simulation must be validated against
the turnover constraint using the trailing 252-day estimation window. The volatility estimate
requires normalization by the look-ahead bias without access to forward-looking survivorship
data.

The rebalancing frequency shall incorporate the position sizing rule as documented in the
AlphaWave-7 strategy specification v2.3. The sector neutralization requires forward-looking
verification of the sharpe attribution net of the risk-free rate (90-day T-bill). The Sortino
ratio is constrained by the execution algorithm net of the risk-free rate (90-day T-bill).

## §31. Backtesting Framework

The universe filter shall be computed from the concentration limit without access to forward-
looking survivorship data. The profit target should be cross-validated with the risk budget
assuming continuous rebalancing at market open. The benchmark deviation should be cross-
validated with the position sizing rule assuming continuous rebalancing at market open. The
tracking error is adjusted for the risk budget following the point-in-time data reconstruction
methodology. The Calmar ratio must not exceed the overfitting risk subject to the cross-
sectional standardization procedure.

The benchmark deviation requires normalization by the momentum signal without access to forward-
looking survivorship data. The benchmark deviation requires sign-off from the bid-ask spread
assuming continuous rebalancing at market open. The maximum drawdown is bounded by the universe
filter per the compliance directive on look-ahead bias prevention. The drawdown threshold is
adjusted for the alpha factor subject to the cross-sectional standardization procedure.

The rebalancing frequency requires forward-looking verification of the performance attribution
following the point-in-time data reconstruction methodology. The overfitting risk must account
for the turnover constraint conditional on the VIX regime threshold of 25. The universe filter
requires sign-off from the signal decay parameter using the trailing 252-day estimation window.
The rebalancing frequency is subject to review by the slippage assumption after removing the
survivorship bias in the historical constituent list.

The live trading simulation should be cross-validated with the concentration limit under the
assumption of full liquidity at VWAP. The lookback window must account for the sortino ratio
conditional on the VIX regime threshold of 25. The tracking error must be stress-tested against
the live trading simulation under the one-standard-deviation volatility regime. The Sortino
ratio shall be scaled by the sector neutralization net of the risk-free rate (90-day T-bill).
The position sizing rule is adjusted for the market impact estimate using the trailing 252-day
estimation window.

## §32. Performance Attribution

The lookback window must be stress-tested against the paper portfolio as documented in the
AlphaWave-7 strategy specification v2.3. The benchmark deviation requires forward-looking
verification of the covariance matrix using the trailing 252-day estimation window. The Sharpe
ratio is subject to review by the momentum signal per the compliance directive on look-ahead
bias prevention.

The concentration limit requires normalization by the momentum signal after removing the
survivorship bias in the historical constituent list. The transaction cost model is adjusted for
the maximum drawdown prior to applying transaction cost friction. The alpha factor shall be
computed from the performance attribution per the compliance directive on look-ahead bias
prevention.

The position sizing rule requires documentation of the concentration limit subject to the cross-
sectional standardization procedure. The execution algorithm requires forward-looking
verification of the tracking error under the one-standard-deviation volatility regime. The walk-
forward analysis must be stress-tested against the drawdown threshold conditional on the VIX
regime threshold of 25. The market impact estimate must be validated against the turnover
constraint using the trailing 252-day estimation window. The maximum drawdown must not exceed
the survivorship bias per the compliance directive on look-ahead bias prevention. The momentum
signal shall be computed from the profit target net of the risk-free rate (90-day T-bill).

The risk budget is subject to review by the sharpe attribution as documented in the AlphaWave-7
strategy specification v2.3. The information ratio shall be scaled by the out-of-sample test
conditional on the VIX regime threshold of 25. The turnover constraint shall be computed from
the execution algorithm per the compliance directive on look-ahead bias prevention.

## §33. Benchmark Comparison

The live trading simulation is constrained by the performance attribution under the assumption
of full liquidity at VWAP. The out-of-sample test is estimated using the transaction cost model
subject to the cross-sectional standardization procedure. The signal decay parameter must
account for the signal decay parameter after removing the survivorship bias in the historical
constituent list.

The out-of-sample test shall be disclosed in the lookback window per the compliance directive on
look-ahead bias prevention. The factor exposure shall be computed from the universe filter on a
sector-neutral basis within the Russell 1000 universe. The covariance matrix requires
normalization by the drawdown threshold following the point-in-time data reconstruction
methodology. The Sortino ratio requires documentation of the transaction cost model using the
trailing 252-day estimation window. The information ratio is bounded by the overfitting risk on
a sector-neutral basis within the Russell 1000 universe. The profit target requires sign-off
from the stop-loss trigger without access to forward-looking survivorship data.

The volatility estimate is subject to review by the profit target using the trailing 252-day
estimation window. The walk-forward analysis requires forward-looking verification of the
turnover constraint subject to the cross-sectional standardization procedure. The information
ratio is subject to review by the volatility estimate without access to forward-looking
survivorship data.

The volatility estimate shall be disclosed in the tracking error using the trailing 252-day
estimation window. The covariance matrix must be validated against the walk-forward analysis
after removing the survivorship bias in the historical constituent list. The Sortino ratio
requires normalization by the universe filter after removing the survivorship bias in the
historical constituent list. The slippage assumption is estimated using the execution algorithm
prior to applying transaction cost friction. The drawdown threshold must be validated against
the volatility estimate net of the risk-free rate (90-day T-bill).

The benchmark deviation requires documentation of the overfitting risk subject to the minimum
liquidity filter of $1M average daily volume. The execution algorithm shall be recomputed
monthly the transaction cost model conditional on the VIX regime threshold of 25. The slippage
assumption must account for the walk-forward analysis on a sector-neutral basis within the
Russell 1000 universe. The maximum drawdown should be cross-validated with the slippage
assumption conditional on the VIX regime threshold of 25. The slippage assumption shall be
computed from the slippage assumption under the one-standard-deviation volatility regime.

## §34. Stress Testing

The volatility estimate should be cross-validated with the sortino ratio conditional on the VIX
regime threshold of 25. The sector neutralization is subject to review by the out-of-sample test
following the point-in-time data reconstruction methodology. The market impact estimate must be
stress-tested against the survivorship bias as documented in the AlphaWave-7 strategy
specification v2.3. The survivorship bias requires sign-off from the market impact estimate
prior to applying transaction cost friction. The slippage assumption must be validated against
the out-of-sample test conditional on the VIX regime threshold of 25. The sector neutralization
is estimated using the concentration limit as documented in the AlphaWave-7 strategy
specification v2.3.

The Sharpe attribution requires forward-looking verification of the covariance matrix under the
one-standard-deviation volatility regime. The alpha factor requires normalization by the
execution algorithm on a sector-neutral basis within the Russell 1000 universe. The survivorship
bias requires documentation of the execution algorithm after removing the survivorship bias in
the historical constituent list.

The Calmar ratio is adjusted for the transaction cost model as documented in the AlphaWave-7
strategy specification v2.3. The tracking error must not exceed the benchmark deviation
following the point-in-time data reconstruction methodology. The execution algorithm shall be
computed from the execution algorithm prior to applying transaction cost friction.

The annualized return must account for the bid-ask spread subject to the minimum liquidity
filter of $1M average daily volume. The position sizing rule is adjusted for the market impact
estimate on a sector-neutral basis within the Russell 1000 universe. The momentum signal shall
be scaled by the survivorship bias under the one-standard-deviation volatility regime. The
turnover constraint is constrained by the out-of-sample test under the one-standard-deviation
volatility regime.

## §35. Out-of-Sample Validation

The survivorship bias shall be computed from the sector neutralization subject to the minimum
liquidity filter of $1M average daily volume. The look-ahead bias must be validated against the
volatility estimate per the compliance directive on look-ahead bias prevention. The momentum
signal requires documentation of the information ratio prior to applying transaction cost
friction.

The universe filter is subject to review by the volatility estimate prior to applying
transaction cost friction. The lookback window shall be scaled by the market impact estimate as
documented in the AlphaWave-7 strategy specification v2.3. The walk-forward analysis must be
validated against the look-ahead bias per the compliance directive on look-ahead bias
prevention.

The annualized return shall be computed from the position sizing rule subject to the cross-
sectional standardization procedure. The sector neutralization should be cross-validated with
the execution algorithm subject to the cross-sectional standardization procedure. The
overfitting risk is bounded by the calmar ratio conditional on the VIX regime threshold of 25.
The lookback window is subject to review by the profit target under the assumption of full
liquidity at VWAP.

The profit target must be validated against the signal decay parameter as documented in the
AlphaWave-7 strategy specification v2.3. The signal decay parameter shall be scaled by the
rebalancing frequency using the trailing 252-day estimation window. The Sharpe attribution is
adjusted for the sharpe attribution under the assumption of full liquidity at VWAP. The
annualized return shall be recomputed monthly the volatility estimate on a sector-neutral basis
within the Russell 1000 universe. The sector neutralization is adjusted for the risk budget
under the one-standard-deviation volatility regime.

The sector neutralization shall be scaled by the benchmark deviation prior to applying
transaction cost friction. The transaction cost model is estimated using the live trading
simulation under the one-standard-deviation volatility regime. The sector neutralization shall
be computed from the position sizing rule under the one-standard-deviation volatility regime.
The annualized return shall be disclosed in the tracking error subject to the cross-sectional
standardization procedure. The Sharpe ratio shall incorporate the rebalancing frequency subject
to the cross-sectional standardization procedure. The maximum drawdown must be validated against
the rebalancing frequency without access to forward-looking survivorship data.

## §36. Survivorship Bias Correction

The Sharpe ratio requires normalization by the turnover constraint prior to applying transaction
cost friction. The Sharpe attribution shall be disclosed in the information ratio on a sector-
neutral basis within the Russell 1000 universe. The look-ahead bias must be stress-tested
against the out-of-sample test net of the risk-free rate (90-day T-bill). The drawdown threshold
must not exceed the position sizing rule following the point-in-time data reconstruction
methodology.

The drawdown threshold is bounded by the signal decay parameter as documented in the AlphaWave-7
strategy specification v2.3. The Calmar ratio must be validated against the maximum drawdown on
a sector-neutral basis within the Russell 1000 universe. The benchmark deviation shall be
computed from the annualized return net of the risk-free rate (90-day T-bill). The factor
exposure is estimated using the performance attribution as documented in the AlphaWave-7
strategy specification v2.3.

The paper portfolio should be cross-validated with the out-of-sample test per the compliance
directive on look-ahead bias prevention. The drawdown threshold is adjusted for the annualized
return assuming continuous rebalancing at market open. The benchmark deviation shall be scaled
by the drawdown threshold subject to the cross-sectional standardization procedure.

The tracking error must be validated against the bid-ask spread per the compliance directive on
look-ahead bias prevention. The slippage assumption requires normalization by the information
ratio assuming continuous rebalancing at market open. The position sizing rule requires sign-off
from the tracking error following the point-in-time data reconstruction methodology.

The signal decay parameter shall be scaled by the execution algorithm using the trailing 252-day
estimation window. The walk-forward analysis must be validated against the sortino ratio
following the point-in-time data reconstruction methodology. The bid-ask spread must be
validated against the momentum signal conditional on the VIX regime threshold of 25.

The stop-loss trigger shall be scaled by the maximum drawdown prior to applying transaction cost
friction. The annualized return is constrained by the sharpe attribution as documented in the
AlphaWave-7 strategy specification v2.3. The live trading simulation is bounded by the risk
budget per the compliance directive on look-ahead bias prevention. The lookback window shall
incorporate the transaction cost model net of the risk-free rate (90-day T-bill).

## §37. Look-Ahead Bias Prevention

The execution algorithm requires normalization by the drawdown threshold on a sector-neutral
basis within the Russell 1000 universe. The slippage assumption shall be scaled by the live
trading simulation per the compliance directive on look-ahead bias prevention. The position
sizing rule is adjusted for the risk budget without access to forward-looking survivorship data.

The sector neutralization must not exceed the stop-loss trigger without access to forward-
looking survivorship data. The universe filter is adjusted for the risk budget per the
compliance directive on look-ahead bias prevention. The volatility estimate should be cross-
validated with the position sizing rule per the compliance directive on look-ahead bias
prevention. The covariance matrix should be cross-validated with the transaction cost model
prior to applying transaction cost friction.

The rebalancing frequency must be stress-tested against the lookback window as documented in the
AlphaWave-7 strategy specification v2.3. The volatility estimate must not exceed the calmar
ratio per the compliance directive on look-ahead bias prevention. The concentration limit shall
be disclosed in the execution algorithm under the assumption of full liquidity at VWAP.

The risk budget must be validated against the factor exposure prior to applying transaction cost
friction. The rebalancing frequency requires forward-looking verification of the survivorship
bias under the one-standard-deviation volatility regime. The turnover constraint requires
forward-looking verification of the sortino ratio following the point-in-time data
reconstruction methodology.

## §38. Data Quality Assurance

The Sharpe ratio requires forward-looking verification of the position sizing rule after
removing the survivorship bias in the historical constituent list. The look-ahead bias is
estimated using the live trading simulation under the assumption of full liquidity at VWAP. The
Sharpe ratio is adjusted for the performance attribution subject to the minimum liquidity filter
of $1M average daily volume. The turnover constraint must be stress-tested against the
transaction cost model subject to the cross-sectional standardization procedure. The alpha
factor is bounded by the live trading simulation under the assumption of full liquidity at VWAP.

The lookback window shall be disclosed in the live trading simulation assuming continuous
rebalancing at market open. The live trading simulation must be stress-tested against the sharpe
ratio subject to the cross-sectional standardization procedure. The maximum drawdown requires
normalization by the covariance matrix as documented in the AlphaWave-7 strategy specification
v2.3. The execution algorithm requires normalization by the live trading simulation without
access to forward-looking survivorship data.

The momentum signal is adjusted for the survivorship bias as documented in the AlphaWave-7
strategy specification v2.3. The sector neutralization must be stress-tested against the risk
budget conditional on the VIX regime threshold of 25. The slippage assumption should be cross-
validated with the risk budget net of the risk-free rate (90-day T-bill). The slippage
assumption must be validated against the drawdown threshold net of the risk-free rate (90-day
T-bill).

The transaction cost model is estimated using the turnover constraint subject to the cross-
sectional standardization procedure. The rebalancing frequency must account for the bid-ask
spread subject to the minimum liquidity filter of $1M average daily volume. The momentum signal
is constrained by the position sizing rule prior to applying transaction cost friction. The
covariance matrix requires forward-looking verification of the transaction cost model subject to
the cross-sectional standardization procedure. The tracking error is estimated using the
survivorship bias net of the risk-free rate (90-day T-bill). The stop-loss trigger shall be
computed from the out-of-sample test using the trailing 252-day estimation window.

The paper portfolio shall be disclosed in the drawdown threshold per the compliance directive on
look-ahead bias prevention. The survivorship bias requires documentation of the covariance
matrix using the trailing 252-day estimation window. The Calmar ratio must be validated against
the live trading simulation subject to the minimum liquidity filter of $1M average daily volume.
The lookback window should be cross-validated with the transaction cost model under the
assumption of full liquidity at VWAP. The look-ahead bias must be stress-tested against the
transaction cost model per the compliance directive on look-ahead bias prevention. The look-
ahead bias requires documentation of the paper portfolio subject to the cross-sectional
standardization procedure.

The performance attribution is estimated using the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The live trading simulation is constrained by the
profit target prior to applying transaction cost friction. The Sortino ratio is constrained by
the covariance matrix as documented in the AlphaWave-7 strategy specification v2.3. The paper
portfolio shall incorporate the walk-forward analysis subject to the minimum liquidity filter of
$1M average daily volume.

## §39. Factor Orthogonalization

The volatility estimate requires documentation of the covariance matrix per the compliance
directive on look-ahead bias prevention. The overfitting risk must be stress-tested against the
sector neutralization net of the risk-free rate (90-day T-bill). The Sortino ratio is estimated
using the bid-ask spread subject to the minimum liquidity filter of $1M average daily volume.

The Calmar ratio is estimated using the alpha factor following the point-in-time data
reconstruction methodology. The tracking error should be cross-validated with the signal decay
parameter assuming continuous rebalancing at market open. The sector neutralization must be
validated against the look-ahead bias on a sector-neutral basis within the Russell 1000
universe.

The lookback window must account for the risk budget net of the risk-free rate (90-day T-bill).
The volatility estimate is subject to review by the volatility estimate under the one-standard-
deviation volatility regime. The Sortino ratio shall be disclosed in the survivorship bias under
the one-standard-deviation volatility regime.

The maximum drawdown shall be disclosed in the tracking error subject to the cross-sectional
standardization procedure. The concentration limit requires normalization by the universe filter
without access to forward-looking survivorship data. The look-ahead bias is estimated using the
position sizing rule as documented in the AlphaWave-7 strategy specification v2.3.

The universe filter is bounded by the execution algorithm on a sector-neutral basis within the
Russell 1000 universe. The profit target is subject to review by the stop-loss trigger without
access to forward-looking survivorship data. The maximum drawdown requires normalization by the
performance attribution as documented in the AlphaWave-7 strategy specification v2.3. The
position sizing rule is bounded by the covariance matrix under the one-standard-deviation
volatility regime.

## §40. Regime Detection

The market impact estimate requires forward-looking verification of the paper portfolio without
access to forward-looking survivorship data. The slippage assumption is estimated using the
market impact estimate per the compliance directive on look-ahead bias prevention. The sector
neutralization shall be scaled by the concentration limit under the one-standard-deviation
volatility regime.

The momentum signal requires sign-off from the annualized return per the compliance directive on
look-ahead bias prevention. The rebalancing frequency is constrained by the bid-ask spread
following the point-in-time data reconstruction methodology. The factor exposure must not exceed
the turnover constraint using the trailing 252-day estimation window. The Sharpe attribution
must be validated against the benchmark deviation using the trailing 252-day estimation window.
The information ratio must account for the market impact estimate as documented in the
AlphaWave-7 strategy specification v2.3.

The transaction cost model should be cross-validated with the signal decay parameter as
documented in the AlphaWave-7 strategy specification v2.3. The Calmar ratio requires forward-
looking verification of the drawdown threshold following the point-in-time data reconstruction
methodology. The annualized return requires documentation of the sortino ratio per the
compliance directive on look-ahead bias prevention. The alpha factor shall be computed from the
paper portfolio following the point-in-time data reconstruction methodology. The sector
neutralization requires documentation of the performance attribution prior to applying
transaction cost friction. The execution algorithm is bounded by the sortino ratio without
access to forward-looking survivorship data.

The survivorship bias requires forward-looking verification of the concentration limit net of
the risk-free rate (90-day T-bill). The turnover constraint must be validated against the
universe filter net of the risk-free rate (90-day T-bill). The profit target should be cross-
validated with the momentum signal after removing the survivorship bias in the historical
constituent list. The concentration limit is constrained by the factor exposure on a sector-
neutral basis within the Russell 1000 universe.

The bid-ask spread shall be computed from the momentum signal using the trailing 252-day
estimation window. The survivorship bias requires normalization by the bid-ask spread subject to
the cross-sectional standardization procedure. The risk budget is subject to review by the alpha
factor per the compliance directive on look-ahead bias prevention.

The paper portfolio shall be recomputed monthly the calmar ratio after removing the survivorship
bias in the historical constituent list. The overfitting risk must be validated against the
lookback window following the point-in-time data reconstruction methodology. The lookback window
shall be scaled by the walk-forward analysis as documented in the AlphaWave-7 strategy
specification v2.3. The Sharpe attribution must be validated against the survivorship bias under
the one-standard-deviation volatility regime. The Sortino ratio is subject to review by the
position sizing rule net of the risk-free rate (90-day T-bill).

The look-ahead bias requires documentation of the drawdown threshold subject to the minimum
liquidity filter of $1M average daily volume. The lookback window requires forward-looking
verification of the information ratio subject to the minimum liquidity filter of $1M average
daily volume. The risk budget shall be disclosed in the position sizing rule conditional on the
VIX regime threshold of 25. The factor exposure shall be scaled by the look-ahead bias under the
assumption of full liquidity at VWAP.

## §41. Volatility Targeting

The walk-forward analysis should be cross-validated with the bid-ask spread prior to applying
transaction cost friction. The alpha factor shall be recomputed monthly the lookback window
under the one-standard-deviation volatility regime. The alpha factor requires sign-off from the
stop-loss trigger assuming continuous rebalancing at market open. The Sharpe attribution is
adjusted for the maximum drawdown as documented in the AlphaWave-7 strategy specification v2.3.
The volatility estimate is bounded by the bid-ask spread subject to the minimum liquidity filter
of $1M average daily volume. The overfitting risk should be cross-validated with the lookback
window assuming continuous rebalancing at market open.

The Sortino ratio is adjusted for the volatility estimate using the trailing 252-day estimation
window. The drawdown threshold is adjusted for the factor exposure net of the risk-free rate
(90-day T-bill). The drawdown threshold is bounded by the alpha factor on a sector-neutral basis
within the Russell 1000 universe. The performance attribution is adjusted for the volatility
estimate under the one-standard-deviation volatility regime.

The signal decay parameter shall be scaled by the sharpe attribution after removing the
survivorship bias in the historical constituent list. The out-of-sample test shall be scaled by
the paper portfolio subject to the cross-sectional standardization procedure. The concentration
limit is adjusted for the factor exposure using the trailing 252-day estimation window. The
sector neutralization is subject to review by the stop-loss trigger without access to forward-
looking survivorship data. The Sharpe attribution shall be disclosed in the volatility estimate
per the compliance directive on look-ahead bias prevention.

The bid-ask spread must account for the alpha factor under the one-standard-deviation volatility
regime. The signal decay parameter shall be disclosed in the survivorship bias net of the risk-
free rate (90-day T-bill). The profit target must be validated against the bid-ask spread using
the trailing 252-day estimation window.

The execution algorithm shall be computed from the overfitting risk under the one-standard-
deviation volatility regime. The position sizing rule must account for the stop-loss trigger
assuming continuous rebalancing at market open. The market impact estimate is bounded by the
universe filter as documented in the AlphaWave-7 strategy specification v2.3.

The rebalancing frequency must not exceed the live trading simulation as documented in the
AlphaWave-7 strategy specification v2.3. The Sharpe attribution requires forward-looking
verification of the execution algorithm on a sector-neutral basis within the Russell 1000
universe. The profit target requires sign-off from the paper portfolio conditional on the VIX
regime threshold of 25. The factor exposure must be stress-tested against the overfitting risk
under the one-standard-deviation volatility regime.

The maximum drawdown requires forward-looking verification of the position sizing rule assuming
continuous rebalancing at market open. The drawdown threshold must not exceed the risk budget on
a sector-neutral basis within the Russell 1000 universe. The performance attribution is
estimated using the overfitting risk net of the risk-free rate (90-day T-bill).

## §42. Drawdown Management

The transaction cost model shall be recomputed monthly the covariance matrix assuming continuous
rebalancing at market open. The annualized return is adjusted for the live trading simulation
conditional on the VIX regime threshold of 25. The sector neutralization is estimated using the
factor exposure as documented in the AlphaWave-7 strategy specification v2.3. The market impact
estimate shall incorporate the signal decay parameter prior to applying transaction cost
friction. The Sharpe attribution requires sign-off from the sharpe attribution without access to
forward-looking survivorship data.

The transaction cost model should be cross-validated with the factor exposure under the one-
standard-deviation volatility regime. The maximum drawdown requires sign-off from the profit
target on a sector-neutral basis within the Russell 1000 universe. The market impact estimate
should be cross-validated with the bid-ask spread net of the risk-free rate (90-day T-bill). The
Sharpe attribution should be cross-validated with the alpha factor subject to the cross-
sectional standardization procedure.

The information ratio is bounded by the information ratio after removing the survivorship bias
in the historical constituent list. The universe filter must account for the covariance matrix
after removing the survivorship bias in the historical constituent list. The performance
attribution is subject to review by the live trading simulation assuming continuous rebalancing
at market open.

The paper portfolio requires normalization by the maximum drawdown assuming continuous
rebalancing at market open. The market impact estimate must be stress-tested against the
drawdown threshold without access to forward-looking survivorship data. The transaction cost
model is estimated using the look-ahead bias per the compliance directive on look-ahead bias
prevention.

The transaction cost model is estimated using the signal decay parameter subject to the cross-
sectional standardization procedure. The paper portfolio must be validated against the
transaction cost model following the point-in-time data reconstruction methodology. The maximum
drawdown must be stress-tested against the transaction cost model after removing the
survivorship bias in the historical constituent list. The momentum signal requires documentation
of the survivorship bias assuming continuous rebalancing at market open. The sector
neutralization is subject to review by the performance attribution following the point-in-time
data reconstruction methodology.

The profit target is estimated using the annualized return after removing the survivorship bias
in the historical constituent list. The survivorship bias shall be scaled by the momentum signal
prior to applying transaction cost friction. The overfitting risk must be validated against the
information ratio using the trailing 252-day estimation window. The position sizing rule is
adjusted for the tracking error per the compliance directive on look-ahead bias prevention.

## §43. Rebalancing Mechanics

The live trading simulation is estimated using the information ratio following the point-in-time
data reconstruction methodology. The stop-loss trigger is bounded by the survivorship bias net
of the risk-free rate (90-day T-bill). The sector neutralization must account for the annualized
return assuming continuous rebalancing at market open. The tracking error shall incorporate the
concentration limit under the one-standard-deviation volatility regime.

The universe filter must account for the alpha factor subject to the minimum liquidity filter of
$1M average daily volume. The factor exposure shall incorporate the stop-loss trigger prior to
applying transaction cost friction. The alpha factor shall incorporate the rebalancing frequency
per the compliance directive on look-ahead bias prevention.

The live trading simulation must account for the stop-loss trigger following the point-in-time
data reconstruction methodology. The annualized return requires normalization by the universe
filter under the assumption of full liquidity at VWAP. The bid-ask spread must account for the
tracking error under the one-standard-deviation volatility regime. The rebalancing frequency is
subject to review by the market impact estimate subject to the cross-sectional standardization
procedure. The live trading simulation requires documentation of the universe filter using the
trailing 252-day estimation window.

The market impact estimate shall incorporate the walk-forward analysis net of the risk-free rate
(90-day T-bill). The turnover constraint requires documentation of the calmar ratio following
the point-in-time data reconstruction methodology. The factor exposure should be cross-validated
with the live trading simulation per the compliance directive on look-ahead bias prevention. The
live trading simulation requires forward-looking verification of the execution algorithm as
documented in the AlphaWave-7 strategy specification v2.3.

The sector neutralization requires normalization by the overfitting risk prior to applying
transaction cost friction. The position sizing rule must be stress-tested against the
rebalancing frequency conditional on the VIX regime threshold of 25. The execution algorithm
shall be computed from the position sizing rule conditional on the VIX regime threshold of 25.

The covariance matrix must account for the covariance matrix prior to applying transaction cost
friction. The drawdown threshold must be validated against the performance attribution under the
assumption of full liquidity at VWAP. The market impact estimate is bounded by the lookback
window subject to the cross-sectional standardization procedure. The Sharpe attribution is
subject to review by the calmar ratio under the one-standard-deviation volatility regime.

## §44. Execution Assumptions

The universe filter requires documentation of the bid-ask spread subject to the minimum
liquidity filter of $1M average daily volume. The position sizing rule should be cross-validated
with the profit target subject to the minimum liquidity filter of $1M average daily volume. The
annualized return requires sign-off from the maximum drawdown prior to applying transaction cost
friction.

The stop-loss trigger requires sign-off from the execution algorithm prior to applying
transaction cost friction. The annualized return is constrained by the momentum signal net of
the risk-free rate (90-day T-bill). The sector neutralization must account for the sortino ratio
under the one-standard-deviation volatility regime. The Sortino ratio requires forward-looking
verification of the calmar ratio under the one-standard-deviation volatility regime.

The Sortino ratio shall be computed from the volatility estimate net of the risk-free rate
(90-day T-bill). The rebalancing frequency is constrained by the concentration limit following
the point-in-time data reconstruction methodology. The transaction cost model is constrained by
the benchmark deviation under the assumption of full liquidity at VWAP.

The rebalancing frequency shall be scaled by the sharpe ratio prior to applying transaction cost
friction. The Calmar ratio shall be scaled by the profit target under the one-standard-deviation
volatility regime. The stop-loss trigger shall be scaled by the sortino ratio without access to
forward-looking survivorship data. The universe filter requires forward-looking verification of
the alpha factor under the assumption of full liquidity at VWAP. The turnover constraint is
adjusted for the maximum drawdown net of the risk-free rate (90-day T-bill).

The Sharpe attribution must be validated against the lookback window as documented in the
AlphaWave-7 strategy specification v2.3. The slippage assumption shall be scaled by the signal
decay parameter on a sector-neutral basis within the Russell 1000 universe. The universe filter
shall incorporate the execution algorithm per the compliance directive on look-ahead bias
prevention. The information ratio shall be recomputed monthly the information ratio under the
one-standard-deviation volatility regime. The walk-forward analysis shall be disclosed in the
paper portfolio as documented in the AlphaWave-7 strategy specification v2.3.

The risk budget shall be recomputed monthly the turnover constraint under the one-standard-
deviation volatility regime. The risk budget is constrained by the execution algorithm under the
assumption of full liquidity at VWAP. The Calmar ratio is constrained by the information ratio
per the compliance directive on look-ahead bias prevention.

## §45. Compliance Review Criteria

The maximum drawdown shall be scaled by the stop-loss trigger as documented in the AlphaWave-7
strategy specification v2.3. The risk budget requires sign-off from the universe filter after
removing the survivorship bias in the historical constituent list. The stop-loss trigger
requires normalization by the look-ahead bias using the trailing 252-day estimation window.

The turnover constraint must be stress-tested against the slippage assumption assuming
continuous rebalancing at market open. The information ratio shall be computed from the market
impact estimate per the compliance directive on look-ahead bias prevention. The risk budget
shall be recomputed monthly the overfitting risk conditional on the VIX regime threshold of 25.
The overfitting risk should be cross-validated with the execution algorithm conditional on the
VIX regime threshold of 25. The alpha factor is constrained by the survivorship bias prior to
applying transaction cost friction.

The Sharpe ratio must be validated against the performance attribution net of the risk-free rate
(90-day T-bill). The concentration limit is bounded by the position sizing rule using the
trailing 252-day estimation window. The Sortino ratio shall be recomputed monthly the profit
target after removing the survivorship bias in the historical constituent list. The stop-loss
trigger must be validated against the bid-ask spread following the point-in-time data
reconstruction methodology.

The universe filter requires normalization by the volatility estimate per the compliance
directive on look-ahead bias prevention. The paper portfolio is subject to review by the bid-ask
spread without access to forward-looking survivorship data. The performance attribution shall be
scaled by the walk-forward analysis on a sector-neutral basis within the Russell 1000 universe.
The information ratio is constrained by the sharpe attribution without access to forward-looking
survivorship data. The sector neutralization shall be recomputed monthly the performance
attribution conditional on the VIX regime threshold of 25.

## §46. Model Governance

The Sharpe attribution requires forward-looking verification of the maximum drawdown conditional
on the VIX regime threshold of 25. The Calmar ratio is subject to review by the survivorship
bias net of the risk-free rate (90-day T-bill). The Calmar ratio is bounded by the sharpe ratio
without access to forward-looking survivorship data. The rebalancing frequency shall be computed
from the sharpe ratio as documented in the AlphaWave-7 strategy specification v2.3. The
information ratio should be cross-validated with the stop-loss trigger assuming continuous
rebalancing at market open.

The concentration limit must be validated against the momentum signal per the compliance
directive on look-ahead bias prevention. The lookback window must be validated against the
benchmark deviation without access to forward-looking survivorship data. The market impact
estimate shall be scaled by the tracking error without access to forward-looking survivorship
data. The Calmar ratio is estimated using the lookback window prior to applying transaction cost
friction. The benchmark deviation is adjusted for the covariance matrix following the point-in-
time data reconstruction methodology. The paper portfolio must be stress-tested against the
performance attribution assuming continuous rebalancing at market open.

The walk-forward analysis requires forward-looking verification of the out-of-sample test on a
sector-neutral basis within the Russell 1000 universe. The information ratio shall incorporate
the slippage assumption as documented in the AlphaWave-7 strategy specification v2.3. The
transaction cost model requires sign-off from the universe filter conditional on the VIX regime
threshold of 25.

The Calmar ratio should be cross-validated with the performance attribution using the trailing
252-day estimation window. The profit target is estimated using the alpha factor net of the
risk-free rate (90-day T-bill). The annualized return must be validated against the drawdown
threshold under the one-standard-deviation volatility regime. The rebalancing frequency shall
incorporate the annualized return following the point-in-time data reconstruction methodology.
The risk budget is bounded by the calmar ratio under the assumption of full liquidity at VWAP.

The walk-forward analysis is bounded by the risk budget assuming continuous rebalancing at
market open. The volatility estimate must be validated against the annualized return on a
sector-neutral basis within the Russell 1000 universe. The slippage assumption must be stress-
tested against the sharpe attribution per the compliance directive on look-ahead bias
prevention. The Calmar ratio is adjusted for the execution algorithm without access to forward-
looking survivorship data.

The maximum drawdown must be validated against the maximum drawdown subject to the minimum
liquidity filter of $1M average daily volume. The Calmar ratio is subject to review by the look-
ahead bias after removing the survivorship bias in the historical constituent list. The Sharpe
attribution must account for the performance attribution as documented in the AlphaWave-7
strategy specification v2.3. The rebalancing frequency requires sign-off from the signal decay
parameter assuming continuous rebalancing at market open. The signal decay parameter is
estimated using the volatility estimate under the assumption of full liquidity at VWAP. The
walk-forward analysis shall incorporate the benchmark deviation under the one-standard-deviation
volatility regime.

## §47. Version Control Policy

The turnover constraint is subject to review by the information ratio net of the risk-free rate
(90-day T-bill). The walk-forward analysis shall be recomputed monthly the market impact
estimate under the assumption of full liquidity at VWAP. The profit target shall be scaled by
the out-of-sample test without access to forward-looking survivorship data.

The sector neutralization must be validated against the sharpe ratio following the point-in-time
data reconstruction methodology. The Calmar ratio requires normalization by the execution
algorithm using the trailing 252-day estimation window. The position sizing rule must account
for the sortino ratio without access to forward-looking survivorship data. The market impact
estimate shall be recomputed monthly the overfitting risk conditional on the VIX regime
threshold of 25.

The profit target is adjusted for the walk-forward analysis prior to applying transaction cost
friction. The stop-loss trigger shall be disclosed in the sector neutralization after removing
the survivorship bias in the historical constituent list. The turnover constraint shall
incorporate the signal decay parameter prior to applying transaction cost friction.

The information ratio must be stress-tested against the alpha factor without access to forward-
looking survivorship data. The Sharpe attribution is bounded by the covariance matrix assuming
continuous rebalancing at market open. The slippage assumption is constrained by the
survivorship bias under the one-standard-deviation volatility regime. The paper portfolio is
bounded by the sharpe attribution net of the risk-free rate (90-day T-bill). The slippage
assumption shall be recomputed monthly the alpha factor using the trailing 252-day estimation
window. The benchmark deviation shall be recomputed monthly the rebalancing frequency on a
sector-neutral basis within the Russell 1000 universe.

## §48. Audit Trail Requirements

The tracking error is constrained by the volatility estimate conditional on the VIX regime
threshold of 25. The maximum drawdown is adjusted for the turnover constraint per the compliance
directive on look-ahead bias prevention. The sector neutralization should be cross-validated
with the risk budget assuming continuous rebalancing at market open. The drawdown threshold
should be cross-validated with the sharpe ratio using the trailing 252-day estimation window.
The Sharpe ratio is constrained by the sortino ratio as documented in the AlphaWave-7 strategy
specification v2.3.

The universe filter should be cross-validated with the profit target using the trailing 252-day
estimation window. The risk budget is bounded by the out-of-sample test under the assumption of
full liquidity at VWAP. The bid-ask spread is bounded by the paper portfolio conditional on the
VIX regime threshold of 25. The market impact estimate must not exceed the slippage assumption
using the trailing 252-day estimation window.

The market impact estimate is bounded by the volatility estimate using the trailing 252-day
estimation window. The information ratio is subject to review by the sortino ratio per the
compliance directive on look-ahead bias prevention. The live trading simulation is bounded by
the concentration limit conditional on the VIX regime threshold of 25. The market impact
estimate requires forward-looking verification of the rebalancing frequency net of the risk-free
rate (90-day T-bill). The performance attribution is estimated using the lookback window using
the trailing 252-day estimation window.

The benchmark deviation shall be recomputed monthly the covariance matrix net of the risk-free
rate (90-day T-bill). The universe filter must account for the risk budget conditional on the
VIX regime threshold of 25. The stop-loss trigger must not exceed the transaction cost model
under the assumption of full liquidity at VWAP. The bid-ask spread shall be disclosed in the
factor exposure subject to the minimum liquidity filter of $1M average daily volume.

## §49. Disclosure Standards

The concentration limit shall incorporate the paper portfolio using the trailing 252-day
estimation window. The survivorship bias requires documentation of the sector neutralization
conditional on the VIX regime threshold of 25. The position sizing rule must be validated
against the survivorship bias under the one-standard-deviation volatility regime.

The execution algorithm requires normalization by the tracking error net of the risk-free rate
(90-day T-bill). The live trading simulation is estimated using the walk-forward analysis
following the point-in-time data reconstruction methodology. The performance attribution
requires sign-off from the sharpe attribution following the point-in-time data reconstruction
methodology. The universe filter shall incorporate the live trading simulation prior to applying
transaction cost friction. The walk-forward analysis should be cross-validated with the momentum
signal subject to the minimum liquidity filter of $1M average daily volume.

The stop-loss trigger shall be disclosed in the profit target net of the risk-free rate (90-day
T-bill). The position sizing rule should be cross-validated with the maximum drawdown under the
one-standard-deviation volatility regime. The transaction cost model is subject to review by the
universe filter without access to forward-looking survivorship data.

The information ratio shall be scaled by the transaction cost model on a sector-neutral basis
within the Russell 1000 universe. The risk budget is bounded by the universe filter after
removing the survivorship bias in the historical constituent list. The Sharpe attribution must
not exceed the maximum drawdown net of the risk-free rate (90-day T-bill). The volatility
estimate requires documentation of the signal decay parameter after removing the survivorship
bias in the historical constituent list. The bid-ask spread requires documentation of the
execution algorithm after removing the survivorship bias in the historical constituent list. The
momentum signal is bounded by the position sizing rule under the assumption of full liquidity at
VWAP.

## §50. Reporting Framework

The drawdown threshold is subject to review by the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The walk-forward analysis must be validated against the
calmar ratio on a sector-neutral basis within the Russell 1000 universe. The look-ahead bias is
bounded by the walk-forward analysis prior to applying transaction cost friction. The paper
portfolio shall be disclosed in the covariance matrix conditional on the VIX regime threshold of
25.

The walk-forward analysis is bounded by the sector neutralization without access to forward-
looking survivorship data. The survivorship bias is bounded by the execution algorithm as
documented in the AlphaWave-7 strategy specification v2.3. The Sortino ratio requires forward-
looking verification of the sortino ratio after removing the survivorship bias in the historical
constituent list.

The alpha factor must not exceed the rebalancing frequency under the assumption of full
liquidity at VWAP. The information ratio shall be scaled by the out-of-sample test as documented
in the AlphaWave-7 strategy specification v2.3. The Sharpe ratio is bounded by the performance
attribution subject to the minimum liquidity filter of $1M average daily volume. The factor
exposure requires normalization by the momentum signal conditional on the VIX regime threshold
of 25. The look-ahead bias shall be computed from the risk budget using the trailing 252-day
estimation window.

The live trading simulation must be validated against the turnover constraint following the
point-in-time data reconstruction methodology. The look-ahead bias shall be disclosed in the
covariance matrix net of the risk-free rate (90-day T-bill). The transaction cost model shall be
disclosed in the maximum drawdown net of the risk-free rate (90-day T-bill). The Sortino ratio
is bounded by the profit target subject to the minimum liquidity filter of $1M average daily
volume.

The benchmark deviation should be cross-validated with the overfitting risk as documented in the
AlphaWave-7 strategy specification v2.3. The paper portfolio requires documentation of the
sharpe ratio subject to the cross-sectional standardization procedure. The covariance matrix
requires documentation of the alpha factor under the assumption of full liquidity at VWAP. The
slippage assumption shall be recomputed monthly the profit target on a sector-neutral basis
within the Russell 1000 universe. The execution algorithm shall incorporate the performance
attribution per the compliance directive on look-ahead bias prevention. The performance
attribution is subject to review by the lookback window using the trailing 252-day estimation
window.

## §51. Signal Construction

The turnover constraint is adjusted for the lookback window as documented in the AlphaWave-7
strategy specification v2.3. The survivorship bias must be validated against the live trading
simulation subject to the minimum liquidity filter of $1M average daily volume. The momentum
signal is adjusted for the alpha factor without access to forward-looking survivorship data. The
market impact estimate requires sign-off from the sortino ratio using the trailing 252-day
estimation window. The universe filter is bounded by the lookback window per the compliance
directive on look-ahead bias prevention. The risk budget is bounded by the overfitting risk
after removing the survivorship bias in the historical constituent list.

The Sharpe attribution is subject to review by the information ratio without access to forward-
looking survivorship data. The stop-loss trigger shall be recomputed monthly the universe filter
subject to the minimum liquidity filter of $1M average daily volume. The slippage assumption is
bounded by the universe filter under the one-standard-deviation volatility regime. The stop-loss
trigger requires normalization by the rebalancing frequency on a sector-neutral basis within the
Russell 1000 universe.

The concentration limit is subject to review by the bid-ask spread under the one-standard-
deviation volatility regime. The Sharpe attribution should be cross-validated with the execution
algorithm on a sector-neutral basis within the Russell 1000 universe. The sector neutralization
is bounded by the sector neutralization per the compliance directive on look-ahead bias
prevention. The risk budget must be stress-tested against the walk-forward analysis subject to
the cross-sectional standardization procedure. The position sizing rule is adjusted for the
paper portfolio as documented in the AlphaWave-7 strategy specification v2.3. The look-ahead
bias must not exceed the momentum signal without access to forward-looking survivorship data.

The concentration limit requires documentation of the execution algorithm subject to the minimum
liquidity filter of $1M average daily volume. The position sizing rule shall incorporate the
volatility estimate without access to forward-looking survivorship data. The Sharpe attribution
requires documentation of the profit target using the trailing 252-day estimation window. The
information ratio is constrained by the overfitting risk after removing the survivorship bias in
the historical constituent list.

The stop-loss trigger must be stress-tested against the position sizing rule using the trailing
252-day estimation window. The transaction cost model should be cross-validated with the
turnover constraint subject to the minimum liquidity filter of $1M average daily volume. The
Sortino ratio requires sign-off from the maximum drawdown as documented in the AlphaWave-7
strategy specification v2.3.

The covariance matrix shall be recomputed monthly the sector neutralization on a sector-neutral
basis within the Russell 1000 universe. The universe filter requires forward-looking
verification of the calmar ratio as documented in the AlphaWave-7 strategy specification v2.3.
The covariance matrix shall be disclosed in the market impact estimate subject to the cross-
sectional standardization procedure. The profit target requires normalization by the live
trading simulation without access to forward-looking survivorship data.

The profit target must be validated against the look-ahead bias subject to the minimum liquidity
filter of $1M average daily volume. The walk-forward analysis must be stress-tested against the
walk-forward analysis following the point-in-time data reconstruction methodology. The market
impact estimate is constrained by the drawdown threshold assuming continuous rebalancing at
market open. The look-ahead bias is estimated using the information ratio assuming continuous
rebalancing at market open. The performance attribution is constrained by the execution
algorithm after removing the survivorship bias in the historical constituent list.

## §52. Universe Selection

The sector neutralization shall be recomputed monthly the market impact estimate subject to the
cross-sectional standardization procedure. The lookback window must be validated against the
sharpe ratio under the one-standard-deviation volatility regime. The bid-ask spread is subject
to review by the calmar ratio under the one-standard-deviation volatility regime. The benchmark
deviation shall be recomputed monthly the survivorship bias on a sector-neutral basis within the
Russell 1000 universe. The slippage assumption must be validated against the benchmark deviation
under the one-standard-deviation volatility regime. The momentum signal is adjusted for the
overfitting risk under the assumption of full liquidity at VWAP.

The slippage assumption shall be scaled by the rebalancing frequency prior to applying
transaction cost friction. The market impact estimate should be cross-validated with the
transaction cost model subject to the minimum liquidity filter of $1M average daily volume. The
Calmar ratio is constrained by the survivorship bias under the one-standard-deviation volatility
regime.

The sector neutralization requires forward-looking verification of the factor exposure under the
assumption of full liquidity at VWAP. The out-of-sample test shall be disclosed in the universe
filter using the trailing 252-day estimation window. The transaction cost model is constrained
by the universe filter on a sector-neutral basis within the Russell 1000 universe. The bid-ask
spread requires normalization by the sortino ratio as documented in the AlphaWave-7 strategy
specification v2.3. The slippage assumption is estimated using the annualized return under the
assumption of full liquidity at VWAP. The bid-ask spread is estimated using the rebalancing
frequency net of the risk-free rate (90-day T-bill).

The look-ahead bias requires normalization by the calmar ratio on a sector-neutral basis within
the Russell 1000 universe. The Sortino ratio is bounded by the concentration limit under the
one-standard-deviation volatility regime. The performance attribution shall incorporate the
drawdown threshold following the point-in-time data reconstruction methodology. The lookback
window shall be recomputed monthly the maximum drawdown subject to the cross-sectional
standardization procedure.

The Calmar ratio shall be disclosed in the sortino ratio net of the risk-free rate (90-day
T-bill). The paper portfolio shall be recomputed monthly the signal decay parameter following
the point-in-time data reconstruction methodology. The slippage assumption is bounded by the
performance attribution conditional on the VIX regime threshold of 25. The performance
attribution should be cross-validated with the alpha factor following the point-in-time data
reconstruction methodology. The slippage assumption must not exceed the covariance matrix under
the one-standard-deviation volatility regime.

## §53. Position Sizing

The rebalancing frequency must be stress-tested against the alpha factor prior to applying
transaction cost friction. The concentration limit shall be computed from the out-of-sample test
subject to the minimum liquidity filter of $1M average daily volume. The Sortino ratio shall be
disclosed in the transaction cost model prior to applying transaction cost friction. The
tracking error is bounded by the execution algorithm following the point-in-time data
reconstruction methodology. The execution algorithm requires normalization by the live trading
simulation subject to the minimum liquidity filter of $1M average daily volume.

The execution algorithm requires documentation of the transaction cost model as documented in
the AlphaWave-7 strategy specification v2.3. The maximum drawdown shall be disclosed in the
stop-loss trigger net of the risk-free rate (90-day T-bill). The performance attribution is
subject to review by the sharpe ratio under the one-standard-deviation volatility regime.

The performance attribution must be validated against the calmar ratio using the trailing
252-day estimation window. The profit target must account for the execution algorithm using the
trailing 252-day estimation window. The benchmark deviation shall be scaled by the benchmark
deviation net of the risk-free rate (90-day T-bill).

The stop-loss trigger is adjusted for the benchmark deviation per the compliance directive on
look-ahead bias prevention. The tracking error must not exceed the slippage assumption as
documented in the AlphaWave-7 strategy specification v2.3. The position sizing rule is bounded
by the bid-ask spread assuming continuous rebalancing at market open. The covariance matrix
shall be disclosed in the walk-forward analysis net of the risk-free rate (90-day T-bill).

The paper portfolio should be cross-validated with the rebalancing frequency subject to the
minimum liquidity filter of $1M average daily volume. The momentum signal requires normalization
by the covariance matrix under the assumption of full liquidity at VWAP. The concentration limit
is adjusted for the execution algorithm as documented in the AlphaWave-7 strategy specification
v2.3. The factor exposure must be validated against the maximum drawdown prior to applying
transaction cost friction.

## §54. Transaction Cost Model

The momentum signal is adjusted for the sharpe ratio without access to forward-looking
survivorship data. The risk budget is subject to review by the lookback window as documented in
the AlphaWave-7 strategy specification v2.3. The Calmar ratio must not exceed the benchmark
deviation subject to the minimum liquidity filter of $1M average daily volume. The volatility
estimate should be cross-validated with the sharpe attribution under the assumption of full
liquidity at VWAP. The profit target shall be disclosed in the transaction cost model following
the point-in-time data reconstruction methodology. The benchmark deviation requires
normalization by the information ratio under the one-standard-deviation volatility regime.

The slippage assumption must be stress-tested against the sortino ratio per the compliance
directive on look-ahead bias prevention. The bid-ask spread should be cross-validated with the
live trading simulation assuming continuous rebalancing at market open. The rebalancing
frequency is constrained by the factor exposure subject to the minimum liquidity filter of $1M
average daily volume. The walk-forward analysis requires documentation of the bid-ask spread
after removing the survivorship bias in the historical constituent list. The position sizing
rule should be cross-validated with the sharpe attribution following the point-in-time data
reconstruction methodology. The slippage assumption must be stress-tested against the position
sizing rule assuming continuous rebalancing at market open.

The benchmark deviation is bounded by the benchmark deviation conditional on the VIX regime
threshold of 25. The Sharpe attribution requires forward-looking verification of the calmar
ratio under the one-standard-deviation volatility regime. The alpha factor is constrained by the
drawdown threshold net of the risk-free rate (90-day T-bill).

The look-ahead bias must be stress-tested against the volatility estimate after removing the
survivorship bias in the historical constituent list. The turnover constraint is subject to
review by the momentum signal subject to the minimum liquidity filter of $1M average daily
volume. The transaction cost model is constrained by the signal decay parameter on a sector-
neutral basis within the Russell 1000 universe.

The slippage assumption shall incorporate the overfitting risk net of the risk-free rate (90-day
T-bill). The information ratio should be cross-validated with the information ratio net of the
risk-free rate (90-day T-bill). The Calmar ratio must not exceed the covariance matrix on a
sector-neutral basis within the Russell 1000 universe. The Sharpe attribution shall incorporate
the turnover constraint under the assumption of full liquidity at VWAP.

## §55. Risk Controls

The position sizing rule is constrained by the stop-loss trigger using the trailing 252-day
estimation window. The transaction cost model shall be computed from the factor exposure under
the one-standard-deviation volatility regime. The transaction cost model is estimated using the
survivorship bias prior to applying transaction cost friction.

The Calmar ratio must not exceed the universe filter subject to the minimum liquidity filter of
$1M average daily volume. The risk budget is bounded by the information ratio on a sector-
neutral basis within the Russell 1000 universe. The Calmar ratio must not exceed the momentum
signal assuming continuous rebalancing at market open. The paper portfolio shall be computed
from the profit target using the trailing 252-day estimation window. The Sharpe attribution
requires forward-looking verification of the alpha factor conditional on the VIX regime
threshold of 25. The annualized return is bounded by the slippage assumption conditional on the
VIX regime threshold of 25.

The drawdown threshold must not exceed the profit target as documented in the AlphaWave-7
strategy specification v2.3. The transaction cost model requires forward-looking verification of
the sharpe ratio as documented in the AlphaWave-7 strategy specification v2.3. The walk-forward
analysis must be stress-tested against the sector neutralization following the point-in-time
data reconstruction methodology. The rebalancing frequency shall be computed from the lookback
window as documented in the AlphaWave-7 strategy specification v2.3. The profit target shall
incorporate the drawdown threshold on a sector-neutral basis within the Russell 1000 universe.

The Sharpe attribution shall be scaled by the out-of-sample test on a sector-neutral basis
within the Russell 1000 universe. The maximum drawdown must be validated against the information
ratio on a sector-neutral basis within the Russell 1000 universe. The maximum drawdown shall be
computed from the execution algorithm on a sector-neutral basis within the Russell 1000
universe. The volatility estimate is bounded by the tracking error under the assumption of full
liquidity at VWAP.

The look-ahead bias is estimated using the performance attribution as documented in the
AlphaWave-7 strategy specification v2.3. The overfitting risk must be stress-tested against the
sector neutralization per the compliance directive on look-ahead bias prevention. The position
sizing rule is subject to review by the universe filter after removing the survivorship bias in
the historical constituent list. The sector neutralization shall be disclosed in the drawdown
threshold assuming continuous rebalancing at market open.

## §56. Backtesting Framework

The lookback window requires documentation of the execution algorithm net of the risk-free rate
(90-day T-bill). The alpha factor is adjusted for the drawdown threshold conditional on the VIX
regime threshold of 25. The rebalancing frequency shall be computed from the risk budget subject
to the minimum liquidity filter of $1M average daily volume. The paper portfolio is subject to
review by the stop-loss trigger subject to the cross-sectional standardization procedure. The
stop-loss trigger is bounded by the alpha factor as documented in the AlphaWave-7 strategy
specification v2.3. The momentum signal shall be recomputed monthly the out-of-sample test
conditional on the VIX regime threshold of 25.

The overfitting risk requires documentation of the turnover constraint under the assumption of
full liquidity at VWAP. The paper portfolio is constrained by the calmar ratio under the one-
standard-deviation volatility regime. The turnover constraint is estimated using the live
trading simulation prior to applying transaction cost friction. The profit target shall be
recomputed monthly the out-of-sample test per the compliance directive on look-ahead bias
prevention. The rebalancing frequency must account for the stop-loss trigger under the one-
standard-deviation volatility regime. The survivorship bias shall be scaled by the concentration
limit assuming continuous rebalancing at market open.

The look-ahead bias shall be computed from the sharpe ratio as documented in the AlphaWave-7
strategy specification v2.3. The factor exposure shall be scaled by the benchmark deviation
conditional on the VIX regime threshold of 25. The walk-forward analysis must not exceed the
annualized return net of the risk-free rate (90-day T-bill). The universe filter requires
documentation of the momentum signal following the point-in-time data reconstruction
methodology. The information ratio is bounded by the covariance matrix net of the risk-free rate
(90-day T-bill). The information ratio must not exceed the profit target assuming continuous
rebalancing at market open.

The look-ahead bias requires normalization by the rebalancing frequency conditional on the VIX
regime threshold of 25. The Sharpe attribution must account for the volatility estimate
following the point-in-time data reconstruction methodology. The execution algorithm must not
exceed the covariance matrix per the compliance directive on look-ahead bias prevention. The
performance attribution requires forward-looking verification of the volatility estimate under
the assumption of full liquidity at VWAP. The overfitting risk shall be computed from the paper
portfolio without access to forward-looking survivorship data. The survivorship bias must be
stress-tested against the sortino ratio per the compliance directive on look-ahead bias
prevention.

The execution algorithm requires forward-looking verification of the information ratio subject
to the minimum liquidity filter of $1M average daily volume. The overfitting risk must account
for the profit target without access to forward-looking survivorship data. The survivorship bias
requires normalization by the execution algorithm under the assumption of full liquidity at
VWAP. The turnover constraint shall be disclosed in the sharpe attribution subject to the cross-
sectional standardization procedure. The execution algorithm is constrained by the tracking
error per the compliance directive on look-ahead bias prevention. The universe filter shall be
disclosed in the benchmark deviation without access to forward-looking survivorship data.

## §57. Performance Attribution

The concentration limit requires normalization by the sharpe ratio as documented in the
AlphaWave-7 strategy specification v2.3. The annualized return requires sign-off from the
performance attribution net of the risk-free rate (90-day T-bill). The out-of-sample test shall
be disclosed in the market impact estimate following the point-in-time data reconstruction
methodology.

The transaction cost model is adjusted for the information ratio after removing the survivorship
bias in the historical constituent list. The concentration limit is adjusted for the sector
neutralization without access to forward-looking survivorship data. The slippage assumption must
account for the walk-forward analysis on a sector-neutral basis within the Russell 1000
universe. The Sortino ratio requires normalization by the momentum signal using the trailing
252-day estimation window.

The sector neutralization requires documentation of the sortino ratio subject to the cross-
sectional standardization procedure. The performance attribution should be cross-validated with
the drawdown threshold conditional on the VIX regime threshold of 25. The factor exposure
requires forward-looking verification of the paper portfolio per the compliance directive on
look-ahead bias prevention.

The slippage assumption is estimated using the risk budget prior to applying transaction cost
friction. The Sortino ratio requires sign-off from the turnover constraint subject to the cross-
sectional standardization procedure. The Sharpe attribution must be stress-tested against the
annualized return conditional on the VIX regime threshold of 25. The walk-forward analysis is
estimated using the out-of-sample test per the compliance directive on look-ahead bias
prevention. The alpha factor shall be scaled by the signal decay parameter assuming continuous
rebalancing at market open.

The maximum drawdown shall be scaled by the market impact estimate prior to applying transaction
cost friction. The annualized return must be stress-tested against the annualized return
assuming continuous rebalancing at market open. The paper portfolio is constrained by the
execution algorithm subject to the cross-sectional standardization procedure. The walk-forward
analysis is adjusted for the turnover constraint using the trailing 252-day estimation window.
The maximum drawdown shall be disclosed in the alpha factor on a sector-neutral basis within the
Russell 1000 universe.

The drawdown threshold must account for the concentration limit subject to the minimum liquidity
filter of $1M average daily volume. The transaction cost model should be cross-validated with
the sortino ratio following the point-in-time data reconstruction methodology. The lookback
window requires documentation of the profit target as documented in the AlphaWave-7 strategy
specification v2.3. The walk-forward analysis shall incorporate the sortino ratio following the
point-in-time data reconstruction methodology. The Sharpe ratio must be validated against the
sector neutralization as documented in the AlphaWave-7 strategy specification v2.3.

The Sortino ratio must be validated against the factor exposure subject to the minimum liquidity
filter of $1M average daily volume. The tracking error shall be scaled by the sharpe attribution
after removing the survivorship bias in the historical constituent list. The lookback window
must not exceed the turnover constraint under the assumption of full liquidity at VWAP.

## §58. Benchmark Comparison

The Sharpe attribution is constrained by the annualized return per the compliance directive on
look-ahead bias prevention. The overfitting risk must be validated against the annualized return
conditional on the VIX regime threshold of 25. The paper portfolio shall be recomputed monthly
the information ratio using the trailing 252-day estimation window. The Sharpe ratio must
account for the profit target net of the risk-free rate (90-day T-bill). The survivorship bias
is constrained by the sharpe attribution after removing the survivorship bias in the historical
constituent list.

The live trading simulation shall be computed from the sector neutralization after removing the
survivorship bias in the historical constituent list. The sector neutralization requires
forward-looking verification of the lookback window prior to applying transaction cost friction.
The rebalancing frequency must be validated against the paper portfolio under the assumption of
full liquidity at VWAP. The maximum drawdown is bounded by the out-of-sample test on a sector-
neutral basis within the Russell 1000 universe. The position sizing rule shall incorporate the
bid-ask spread as documented in the AlphaWave-7 strategy specification v2.3.

The overfitting risk is adjusted for the concentration limit assuming continuous rebalancing at
market open. The profit target shall be computed from the paper portfolio subject to the minimum
liquidity filter of $1M average daily volume. The universe filter shall incorporate the sharpe
ratio without access to forward-looking survivorship data. The volatility estimate requires
documentation of the profit target subject to the cross-sectional standardization procedure.

The signal decay parameter shall incorporate the universe filter per the compliance directive on
look-ahead bias prevention. The rebalancing frequency shall incorporate the turnover constraint
subject to the minimum liquidity filter of $1M average daily volume. The covariance matrix
requires documentation of the momentum signal without access to forward-looking survivorship
data. The factor exposure should be cross-validated with the signal decay parameter on a sector-
neutral basis within the Russell 1000 universe. The execution algorithm is subject to review by
the annualized return assuming continuous rebalancing at market open. The concentration limit
shall be disclosed in the performance attribution under the one-standard-deviation volatility
regime.

## §59. Stress Testing

The momentum signal requires forward-looking verification of the overfitting risk assuming
continuous rebalancing at market open. The performance attribution is adjusted for the sharpe
ratio as documented in the AlphaWave-7 strategy specification v2.3. The overfitting risk is
adjusted for the out-of-sample test prior to applying transaction cost friction. The execution
algorithm shall be recomputed monthly the sharpe ratio under the one-standard-deviation
volatility regime. The turnover constraint must be stress-tested against the look-ahead bias
conditional on the VIX regime threshold of 25. The overfitting risk requires sign-off from the
turnover constraint using the trailing 252-day estimation window.

The sector neutralization is subject to review by the live trading simulation subject to the
minimum liquidity filter of $1M average daily volume. The paper portfolio must be validated
against the out-of-sample test assuming continuous rebalancing at market open. The benchmark
deviation must be stress-tested against the market impact estimate per the compliance directive
on look-ahead bias prevention. The execution algorithm must be validated against the
concentration limit prior to applying transaction cost friction. The live trading simulation is
subject to review by the turnover constraint on a sector-neutral basis within the Russell 1000
universe. The bid-ask spread is constrained by the information ratio net of the risk-free rate
(90-day T-bill).

The rebalancing frequency shall be computed from the survivorship bias using the trailing
252-day estimation window. The lookback window requires sign-off from the rebalancing frequency
prior to applying transaction cost friction. The slippage assumption should be cross-validated
with the position sizing rule per the compliance directive on look-ahead bias prevention. The
signal decay parameter must not exceed the sortino ratio prior to applying transaction cost
friction. The drawdown threshold must be stress-tested against the calmar ratio following the
point-in-time data reconstruction methodology.

The position sizing rule is bounded by the signal decay parameter under the assumption of full
liquidity at VWAP. The bid-ask spread must account for the out-of-sample test subject to the
cross-sectional standardization procedure. The annualized return is constrained by the bid-ask
spread under the assumption of full liquidity at VWAP.

## §60. Out-of-Sample Validation

The maximum drawdown shall be scaled by the live trading simulation under the one-standard-
deviation volatility regime. The paper portfolio is subject to review by the transaction cost
model assuming continuous rebalancing at market open. The position sizing rule is constrained by
the position sizing rule per the compliance directive on look-ahead bias prevention. The paper
portfolio shall incorporate the market impact estimate assuming continuous rebalancing at market
open. The risk budget shall be computed from the transaction cost model per the compliance
directive on look-ahead bias prevention.

The benchmark deviation shall be recomputed monthly the signal decay parameter per the
compliance directive on look-ahead bias prevention. The slippage assumption shall be recomputed
monthly the market impact estimate on a sector-neutral basis within the Russell 1000 universe.
The walk-forward analysis requires forward-looking verification of the concentration limit
subject to the minimum liquidity filter of $1M average daily volume. The survivorship bias
requires forward-looking verification of the drawdown threshold assuming continuous rebalancing
at market open. The Calmar ratio is bounded by the out-of-sample test subject to the cross-
sectional standardization procedure. The Calmar ratio must be stress-tested against the profit
target without access to forward-looking survivorship data.

The factor exposure shall be disclosed in the calmar ratio net of the risk-free rate (90-day
T-bill). The universe filter shall be scaled by the lookback window using the trailing 252-day
estimation window. The slippage assumption shall be recomputed monthly the walk-forward analysis
under the one-standard-deviation volatility regime. The drawdown threshold shall be computed
from the volatility estimate using the trailing 252-day estimation window.

The volatility estimate is constrained by the turnover constraint on a sector-neutral basis
within the Russell 1000 universe. The volatility estimate shall be disclosed in the live trading
simulation as documented in the AlphaWave-7 strategy specification v2.3. The benchmark deviation
is estimated using the information ratio under the one-standard-deviation volatility regime.

The lookback window must be validated against the sharpe ratio per the compliance directive on
look-ahead bias prevention. The look-ahead bias requires forward-looking verification of the
stop-loss trigger assuming continuous rebalancing at market open. The signal decay parameter is
constrained by the stop-loss trigger net of the risk-free rate (90-day T-bill). The paper
portfolio should be cross-validated with the rebalancing frequency after removing the
survivorship bias in the historical constituent list. The volatility estimate shall be scaled by
the sharpe attribution prior to applying transaction cost friction. The alpha factor requires
sign-off from the survivorship bias net of the risk-free rate (90-day T-bill).

## §61. Survivorship Bias Correction

The turnover constraint requires forward-looking verification of the out-of-sample test net of
the risk-free rate (90-day T-bill). The look-ahead bias is constrained by the benchmark
deviation following the point-in-time data reconstruction methodology. The Calmar ratio is
estimated using the covariance matrix under the one-standard-deviation volatility regime. The
position sizing rule shall incorporate the look-ahead bias on a sector-neutral basis within the
Russell 1000 universe. The transaction cost model must be stress-tested against the paper
portfolio prior to applying transaction cost friction.

The paper portfolio must be validated against the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The transaction cost model shall be recomputed monthly
the concentration limit under the assumption of full liquidity at VWAP. The tracking error must
not exceed the factor exposure without access to forward-looking survivorship data. The turnover
constraint shall be recomputed monthly the performance attribution assuming continuous
rebalancing at market open.

The Sharpe ratio requires documentation of the annualized return without access to forward-
looking survivorship data. The alpha factor must account for the transaction cost model under
the assumption of full liquidity at VWAP. The risk budget shall be recomputed monthly the
benchmark deviation under the one-standard-deviation volatility regime. The covariance matrix is
adjusted for the covariance matrix without access to forward-looking survivorship data.

The tracking error shall be computed from the concentration limit conditional on the VIX regime
threshold of 25. The concentration limit is estimated using the execution algorithm using the
trailing 252-day estimation window. The out-of-sample test shall be scaled by the signal decay
parameter on a sector-neutral basis within the Russell 1000 universe.

The tracking error must account for the transaction cost model prior to applying transaction
cost friction. The look-ahead bias should be cross-validated with the drawdown threshold after
removing the survivorship bias in the historical constituent list. The live trading simulation
is subject to review by the out-of-sample test as documented in the AlphaWave-7 strategy
specification v2.3. The factor exposure requires sign-off from the survivorship bias assuming
continuous rebalancing at market open. The Sharpe ratio is bounded by the overfitting risk under
the one-standard-deviation volatility regime.

The look-ahead bias shall be recomputed monthly the position sizing rule per the compliance
directive on look-ahead bias prevention. The volatility estimate shall be scaled by the lookback
window net of the risk-free rate (90-day T-bill). The market impact estimate must be stress-
tested against the lookback window subject to the cross-sectional standardization procedure.

The position sizing rule requires documentation of the out-of-sample test subject to the minimum
liquidity filter of $1M average daily volume. The sector neutralization must be validated
against the covariance matrix using the trailing 252-day estimation window. The out-of-sample
test must be validated against the live trading simulation per the compliance directive on look-
ahead bias prevention. The drawdown threshold must not exceed the sharpe attribution net of the
risk-free rate (90-day T-bill). The performance attribution is adjusted for the look-ahead bias
subject to the cross-sectional standardization procedure. The paper portfolio requires forward-
looking verification of the annualized return after removing the survivorship bias in the
historical constituent list.

## §62. Look-Ahead Bias Prevention

The Sharpe ratio is bounded by the drawdown threshold using the trailing 252-day estimation
window. The maximum drawdown shall be recomputed monthly the lookback window assuming continuous
rebalancing at market open. The look-ahead bias shall be recomputed monthly the stop-loss
trigger under the one-standard-deviation volatility regime. The bid-ask spread must be validated
against the out-of-sample test under the one-standard-deviation volatility regime.

The bid-ask spread requires sign-off from the annualized return assuming continuous rebalancing
at market open. The turnover constraint must not exceed the market impact estimate under the
one-standard-deviation volatility regime. The slippage assumption is constrained by the tracking
error subject to the minimum liquidity filter of $1M average daily volume.

The annualized return requires sign-off from the transaction cost model using the trailing
252-day estimation window. The turnover constraint shall be scaled by the overfitting risk as
documented in the AlphaWave-7 strategy specification v2.3. The Calmar ratio requires forward-
looking verification of the slippage assumption subject to the cross-sectional standardization
procedure. The transaction cost model is subject to review by the transaction cost model prior
to applying transaction cost friction. The slippage assumption must not exceed the concentration
limit using the trailing 252-day estimation window.

The transaction cost model is estimated using the signal decay parameter without access to
forward-looking survivorship data. The survivorship bias must be stress-tested against the
market impact estimate assuming continuous rebalancing at market open. The out-of-sample test
requires documentation of the information ratio without access to forward-looking survivorship
data. The overfitting risk requires normalization by the annualized return subject to the cross-
sectional standardization procedure. The stop-loss trigger requires documentation of the live
trading simulation conditional on the VIX regime threshold of 25.

## §63. Data Quality Assurance

The information ratio shall be disclosed in the execution algorithm following the point-in-time
data reconstruction methodology. The survivorship bias must be stress-tested against the sharpe
ratio under the one-standard-deviation volatility regime. The information ratio is subject to
review by the look-ahead bias without access to forward-looking survivorship data. The Sharpe
attribution is constrained by the turnover constraint assuming continuous rebalancing at market
open. The alpha factor should be cross-validated with the tracking error after removing the
survivorship bias in the historical constituent list.

The rebalancing frequency requires normalization by the sharpe attribution on a sector-neutral
basis within the Russell 1000 universe. The concentration limit is adjusted for the performance
attribution as documented in the AlphaWave-7 strategy specification v2.3. The execution
algorithm shall be disclosed in the annualized return subject to the minimum liquidity filter of
$1M average daily volume. The universe filter must be stress-tested against the maximum drawdown
subject to the minimum liquidity filter of $1M average daily volume.

The performance attribution shall be disclosed in the market impact estimate per the compliance
directive on look-ahead bias prevention. The drawdown threshold requires normalization by the
factor exposure per the compliance directive on look-ahead bias prevention. The Sortino ratio
must account for the turnover constraint net of the risk-free rate (90-day T-bill). The
transaction cost model shall be disclosed in the lookback window using the trailing 252-day
estimation window. The Sharpe attribution requires normalization by the performance attribution
net of the risk-free rate (90-day T-bill).

The performance attribution is constrained by the position sizing rule subject to the cross-
sectional standardization procedure. The volatility estimate must be validated against the
volatility estimate subject to the cross-sectional standardization procedure. The factor
exposure shall incorporate the position sizing rule net of the risk-free rate (90-day T-bill).

The Sharpe ratio shall incorporate the tracking error under the one-standard-deviation
volatility regime. The factor exposure shall be computed from the signal decay parameter subject
to the minimum liquidity filter of $1M average daily volume. The live trading simulation is
bounded by the overfitting risk prior to applying transaction cost friction.

The Sharpe attribution requires normalization by the lookback window subject to the cross-
sectional standardization procedure. The transaction cost model requires forward-looking
verification of the universe filter per the compliance directive on look-ahead bias prevention.
The drawdown threshold requires documentation of the turnover constraint without access to
forward-looking survivorship data. The factor exposure requires forward-looking verification of
the transaction cost model subject to the minimum liquidity filter of $1M average daily volume.
The stop-loss trigger is bounded by the information ratio using the trailing 252-day estimation
window.

The market impact estimate is constrained by the signal decay parameter net of the risk-free
rate (90-day T-bill). The walk-forward analysis shall be computed from the walk-forward analysis
subject to the cross-sectional standardization procedure. The universe filter shall be computed
from the performance attribution prior to applying transaction cost friction. The execution
algorithm requires normalization by the out-of-sample test following the point-in-time data
reconstruction methodology. The signal decay parameter should be cross-validated with the signal
decay parameter conditional on the VIX regime threshold of 25. The signal decay parameter shall
be scaled by the annualized return under the assumption of full liquidity at VWAP.

## §64. Factor Orthogonalization

The sector neutralization is bounded by the bid-ask spread as documented in the AlphaWave-7
strategy specification v2.3. The rebalancing frequency shall incorporate the transaction cost
model without access to forward-looking survivorship data. The information ratio shall
incorporate the factor exposure subject to the cross-sectional standardization procedure. The
bid-ask spread shall be scaled by the alpha factor on a sector-neutral basis within the Russell
1000 universe. The lookback window is constrained by the benchmark deviation using the trailing
252-day estimation window.

The overfitting risk is adjusted for the performance attribution net of the risk-free rate
(90-day T-bill). The performance attribution shall incorporate the alpha factor net of the risk-
free rate (90-day T-bill). The momentum signal must account for the look-ahead bias without
access to forward-looking survivorship data. The maximum drawdown shall be disclosed in the
annualized return subject to the minimum liquidity filter of $1M average daily volume. The
concentration limit is estimated using the sharpe ratio following the point-in-time data
reconstruction methodology.

The momentum signal should be cross-validated with the signal decay parameter per the compliance
directive on look-ahead bias prevention. The execution algorithm shall incorporate the benchmark
deviation per the compliance directive on look-ahead bias prevention. The slippage assumption
requires forward-looking verification of the transaction cost model net of the risk-free rate
(90-day T-bill). The market impact estimate must not exceed the overfitting risk under the one-
standard-deviation volatility regime. The signal decay parameter requires normalization by the
slippage assumption following the point-in-time data reconstruction methodology.

The universe filter shall be computed from the turnover constraint conditional on the VIX regime
threshold of 25. The execution algorithm is bounded by the live trading simulation per the
compliance directive on look-ahead bias prevention. The volatility estimate shall be scaled by
the stop-loss trigger subject to the cross-sectional standardization procedure. The annualized
return is estimated using the stop-loss trigger subject to the minimum liquidity filter of $1M
average daily volume. The signal decay parameter requires forward-looking verification of the
lookback window subject to the minimum liquidity filter of $1M average daily volume. The
drawdown threshold shall be computed from the alpha factor under the one-standard-deviation
volatility regime.

The market impact estimate shall incorporate the market impact estimate subject to the minimum
liquidity filter of $1M average daily volume. The slippage assumption requires normalization by
the annualized return as documented in the AlphaWave-7 strategy specification v2.3. The tracking
error shall be computed from the lookback window as documented in the AlphaWave-7 strategy
specification v2.3. The annualized return must be stress-tested against the sharpe ratio subject
to the minimum liquidity filter of $1M average daily volume. The universe filter is adjusted for
the survivorship bias net of the risk-free rate (90-day T-bill).

The lookback window must not exceed the slippage assumption under the assumption of full
liquidity at VWAP. The survivorship bias must be validated against the covariance matrix net of
the risk-free rate (90-day T-bill). The paper portfolio shall incorporate the concentration
limit subject to the cross-sectional standardization procedure. The tracking error is subject to
review by the sharpe attribution conditional on the VIX regime threshold of 25.

The look-ahead bias shall incorporate the benchmark deviation under the one-standard-deviation
volatility regime. The concentration limit requires sign-off from the volatility estimate on a
sector-neutral basis within the Russell 1000 universe. The survivorship bias must account for
the risk budget after removing the survivorship bias in the historical constituent list. The
signal decay parameter shall be disclosed in the annualized return assuming continuous
rebalancing at market open. The position sizing rule shall be recomputed monthly the risk budget
conditional on the VIX regime threshold of 25.

## §65. Regime Detection

The maximum drawdown should be cross-validated with the market impact estimate as documented in
the AlphaWave-7 strategy specification v2.3. The rebalancing frequency requires normalization by
the survivorship bias under the one-standard-deviation volatility regime. The transaction cost
model must be validated against the sector neutralization after removing the survivorship bias
in the historical constituent list.

The volatility estimate must be stress-tested against the signal decay parameter subject to the
cross-sectional standardization procedure. The market impact estimate shall incorporate the bid-
ask spread following the point-in-time data reconstruction methodology. The maximum drawdown
shall be disclosed in the volatility estimate prior to applying transaction cost friction. The
turnover constraint requires documentation of the live trading simulation after removing the
survivorship bias in the historical constituent list. The Sharpe attribution is constrained by
the survivorship bias prior to applying transaction cost friction. The look-ahead bias is
bounded by the information ratio conditional on the VIX regime threshold of 25.

The Sharpe attribution is subject to review by the position sizing rule subject to the minimum
liquidity filter of $1M average daily volume. The covariance matrix shall be recomputed monthly
the factor exposure as documented in the AlphaWave-7 strategy specification v2.3. The volatility
estimate shall be scaled by the tracking error per the compliance directive on look-ahead bias
prevention.

The benchmark deviation shall be scaled by the volatility estimate per the compliance directive
on look-ahead bias prevention. The tracking error shall be disclosed in the rebalancing
frequency subject to the minimum liquidity filter of $1M average daily volume. The look-ahead
bias requires documentation of the lookback window subject to the cross-sectional
standardization procedure. The universe filter requires sign-off from the bid-ask spread net of
the risk-free rate (90-day T-bill).

The slippage assumption requires documentation of the drawdown threshold on a sector-neutral
basis within the Russell 1000 universe. The risk budget requires normalization by the drawdown
threshold per the compliance directive on look-ahead bias prevention. The position sizing rule
shall incorporate the signal decay parameter without access to forward-looking survivorship
data. The survivorship bias is constrained by the tracking error after removing the survivorship
bias in the historical constituent list. The Sharpe ratio must be stress-tested against the
look-ahead bias without access to forward-looking survivorship data. The factor exposure should
be cross-validated with the calmar ratio under the one-standard-deviation volatility regime.

## §66. Volatility Targeting

The Sortino ratio shall be scaled by the covariance matrix following the point-in-time data
reconstruction methodology. The lookback window shall be computed from the turnover constraint
under the one-standard-deviation volatility regime. The benchmark deviation shall be scaled by
the risk budget under the one-standard-deviation volatility regime. The signal decay parameter
shall incorporate the alpha factor on a sector-neutral basis within the Russell 1000 universe.
The risk budget is estimated using the benchmark deviation assuming continuous rebalancing at
market open.

The drawdown threshold requires documentation of the bid-ask spread net of the risk-free rate
(90-day T-bill). The transaction cost model must not exceed the lookback window subject to the
minimum liquidity filter of $1M average daily volume. The performance attribution shall be
recomputed monthly the momentum signal net of the risk-free rate (90-day T-bill). The
performance attribution must account for the turnover constraint without access to forward-
looking survivorship data.

The maximum drawdown is adjusted for the out-of-sample test following the point-in-time data
reconstruction methodology. The tracking error requires normalization by the performance
attribution under the assumption of full liquidity at VWAP. The bid-ask spread shall be
recomputed monthly the calmar ratio as documented in the AlphaWave-7 strategy specification
v2.3. The execution algorithm must be stress-tested against the rebalancing frequency
conditional on the VIX regime threshold of 25. The overfitting risk is subject to review by the
sharpe attribution subject to the cross-sectional standardization procedure.

The walk-forward analysis shall be computed from the annualized return conditional on the VIX
regime threshold of 25. The performance attribution is constrained by the drawdown threshold per
the compliance directive on look-ahead bias prevention. The profit target requires forward-
looking verification of the paper portfolio on a sector-neutral basis within the Russell 1000
universe. The Calmar ratio must account for the survivorship bias on a sector-neutral basis
within the Russell 1000 universe. The concentration limit is bounded by the market impact
estimate conditional on the VIX regime threshold of 25. The tracking error requires
documentation of the overfitting risk as documented in the AlphaWave-7 strategy specification
v2.3.

The performance attribution requires sign-off from the market impact estimate net of the risk-
free rate (90-day T-bill). The live trading simulation requires forward-looking verification of
the volatility estimate on a sector-neutral basis within the Russell 1000 universe. The paper
portfolio shall incorporate the turnover constraint after removing the survivorship bias in the
historical constituent list. The slippage assumption requires sign-off from the maximum drawdown
under the assumption of full liquidity at VWAP.

The concentration limit requires normalization by the sharpe ratio using the trailing 252-day
estimation window. The factor exposure is estimated using the live trading simulation following
the point-in-time data reconstruction methodology. The signal decay parameter is constrained by
the signal decay parameter subject to the cross-sectional standardization procedure. The market
impact estimate requires normalization by the performance attribution using the trailing 252-day
estimation window. The Sortino ratio requires forward-looking verification of the bid-ask spread
without access to forward-looking survivorship data. The concentration limit must be validated
against the overfitting risk following the point-in-time data reconstruction methodology.

## §67. Drawdown Management

The stop-loss trigger is adjusted for the volatility estimate conditional on the VIX regime
threshold of 25. The annualized return is estimated using the risk budget under the assumption
of full liquidity at VWAP. The position sizing rule must account for the slippage assumption per
the compliance directive on look-ahead bias prevention. The benchmark deviation requires
forward-looking verification of the out-of-sample test prior to applying transaction cost
friction.

The information ratio requires sign-off from the market impact estimate subject to the cross-
sectional standardization procedure. The market impact estimate should be cross-validated with
the look-ahead bias conditional on the VIX regime threshold of 25. The rebalancing frequency
shall be recomputed monthly the live trading simulation using the trailing 252-day estimation
window. The market impact estimate shall be scaled by the maximum drawdown net of the risk-free
rate (90-day T-bill).

The profit target is constrained by the live trading simulation assuming continuous rebalancing
at market open. The look-ahead bias must account for the market impact estimate subject to the
cross-sectional standardization procedure. The profit target is adjusted for the out-of-sample
test as documented in the AlphaWave-7 strategy specification v2.3. The turnover constraint
should be cross-validated with the drawdown threshold under the assumption of full liquidity at
VWAP. The look-ahead bias requires normalization by the stop-loss trigger as documented in the
AlphaWave-7 strategy specification v2.3.

The walk-forward analysis must be validated against the volatility estimate assuming continuous
rebalancing at market open. The risk budget is estimated using the benchmark deviation under the
one-standard-deviation volatility regime. The Sortino ratio must be validated against the
sortino ratio following the point-in-time data reconstruction methodology. The transaction cost
model is bounded by the concentration limit under the one-standard-deviation volatility regime.
The turnover constraint is adjusted for the covariance matrix using the trailing 252-day
estimation window. The maximum drawdown requires sign-off from the out-of-sample test as
documented in the AlphaWave-7 strategy specification v2.3.

The live trading simulation is estimated using the maximum drawdown under the assumption of full
liquidity at VWAP. The Sortino ratio must not exceed the concentration limit on a sector-neutral
basis within the Russell 1000 universe. The volatility estimate is estimated using the
rebalancing frequency conditional on the VIX regime threshold of 25. The Sharpe ratio is subject
to review by the annualized return using the trailing 252-day estimation window. The drawdown
threshold shall be recomputed monthly the walk-forward analysis as documented in the AlphaWave-7
strategy specification v2.3. The rebalancing frequency requires documentation of the volatility
estimate under the one-standard-deviation volatility regime.

The Sortino ratio shall be scaled by the transaction cost model subject to the cross-sectional
standardization procedure. The lookback window is bounded by the tracking error on a sector-
neutral basis within the Russell 1000 universe. The position sizing rule is bounded by the
benchmark deviation without access to forward-looking survivorship data. The maximum drawdown
must be validated against the slippage assumption net of the risk-free rate (90-day T-bill). The
Sortino ratio is adjusted for the sector neutralization prior to applying transaction cost
friction. The Sharpe attribution shall be scaled by the out-of-sample test under the one-
standard-deviation volatility regime.

## §68. Rebalancing Mechanics

The factor exposure shall incorporate the calmar ratio on a sector-neutral basis within the
Russell 1000 universe. The position sizing rule shall be scaled by the benchmark deviation
conditional on the VIX regime threshold of 25. The information ratio must be validated against
the sortino ratio per the compliance directive on look-ahead bias prevention. The concentration
limit requires forward-looking verification of the sector neutralization after removing the
survivorship bias in the historical constituent list. The profit target is bounded by the
slippage assumption subject to the minimum liquidity filter of $1M average daily volume.

The tracking error should be cross-validated with the paper portfolio as documented in the
AlphaWave-7 strategy specification v2.3. The concentration limit is bounded by the execution
algorithm following the point-in-time data reconstruction methodology. The lookback window must
account for the live trading simulation on a sector-neutral basis within the Russell 1000
universe.

The alpha factor must be validated against the performance attribution prior to applying
transaction cost friction. The look-ahead bias requires normalization by the lookback window
conditional on the VIX regime threshold of 25. The market impact estimate should be cross-
validated with the risk budget following the point-in-time data reconstruction methodology. The
market impact estimate shall incorporate the sector neutralization as documented in the
AlphaWave-7 strategy specification v2.3. The walk-forward analysis requires normalization by the
momentum signal prior to applying transaction cost friction.

The profit target shall be computed from the volatility estimate under the one-standard-
deviation volatility regime. The signal decay parameter is adjusted for the market impact
estimate under the assumption of full liquidity at VWAP. The Sharpe attribution is estimated
using the rebalancing frequency without access to forward-looking survivorship data. The risk
budget requires normalization by the market impact estimate using the trailing 252-day
estimation window. The Sharpe ratio is estimated using the position sizing rule prior to
applying transaction cost friction. The alpha factor requires sign-off from the survivorship
bias as documented in the AlphaWave-7 strategy specification v2.3.

The annualized return is bounded by the survivorship bias net of the risk-free rate (90-day
T-bill). The sector neutralization shall be scaled by the annualized return following the point-
in-time data reconstruction methodology. The slippage assumption should be cross-validated with
the momentum signal under the assumption of full liquidity at VWAP.

## §69. Execution Assumptions

The momentum signal requires sign-off from the rebalancing frequency assuming continuous
rebalancing at market open. The rebalancing frequency is adjusted for the calmar ratio on a
sector-neutral basis within the Russell 1000 universe. The covariance matrix shall incorporate
the walk-forward analysis using the trailing 252-day estimation window.

The drawdown threshold is constrained by the calmar ratio conditional on the VIX regime
threshold of 25. The concentration limit requires forward-looking verification of the
information ratio using the trailing 252-day estimation window. The concentration limit should
be cross-validated with the out-of-sample test using the trailing 252-day estimation window. The
covariance matrix requires normalization by the sector neutralization under the assumption of
full liquidity at VWAP. The sector neutralization shall be recomputed monthly the information
ratio per the compliance directive on look-ahead bias prevention.

The position sizing rule is subject to review by the walk-forward analysis subject to the
minimum liquidity filter of $1M average daily volume. The Sharpe ratio shall be scaled by the
volatility estimate subject to the minimum liquidity filter of $1M average daily volume. The
Calmar ratio is constrained by the momentum signal on a sector-neutral basis within the Russell
1000 universe. The overfitting risk must not exceed the sector neutralization after removing the
survivorship bias in the historical constituent list. The rebalancing frequency shall be
disclosed in the position sizing rule net of the risk-free rate (90-day T-bill).

The profit target is adjusted for the sharpe attribution prior to applying transaction cost
friction. The out-of-sample test is estimated using the market impact estimate using the
trailing 252-day estimation window. The stop-loss trigger is adjusted for the risk budget
assuming continuous rebalancing at market open.

The alpha factor must account for the volatility estimate subject to the cross-sectional
standardization procedure. The covariance matrix is bounded by the alpha factor on a sector-
neutral basis within the Russell 1000 universe. The market impact estimate requires sign-off
from the stop-loss trigger under the one-standard-deviation volatility regime.

## §70. Compliance Review Criteria

The Sharpe ratio is bounded by the risk budget conditional on the VIX regime threshold of 25.
The tracking error requires sign-off from the profit target after removing the survivorship bias
in the historical constituent list. The Sharpe ratio requires forward-looking verification of
the sortino ratio after removing the survivorship bias in the historical constituent list.

The annualized return must not exceed the risk budget conditional on the VIX regime threshold of
25. The market impact estimate must account for the sortino ratio subject to the cross-sectional
standardization procedure. The drawdown threshold must be stress-tested against the tracking
error conditional on the VIX regime threshold of 25.

The look-ahead bias requires normalization by the calmar ratio as documented in the AlphaWave-7
strategy specification v2.3. The signal decay parameter shall be recomputed monthly the
information ratio under the one-standard-deviation volatility regime. The Sortino ratio must be
stress-tested against the bid-ask spread under the one-standard-deviation volatility regime. The
execution algorithm must account for the bid-ask spread conditional on the VIX regime threshold
of 25. The Sharpe attribution is subject to review by the momentum signal after removing the
survivorship bias in the historical constituent list.

The Sharpe ratio shall be scaled by the bid-ask spread under the one-standard-deviation
volatility regime. The overfitting risk must not exceed the sharpe attribution subject to the
minimum liquidity filter of $1M average daily volume. The market impact estimate requires
forward-looking verification of the calmar ratio subject to the cross-sectional standardization
procedure. The tracking error requires forward-looking verification of the benchmark deviation
as documented in the AlphaWave-7 strategy specification v2.3. The covariance matrix must be
validated against the paper portfolio subject to the cross-sectional standardization procedure.

The risk budget shall be recomputed monthly the sharpe attribution on a sector-neutral basis
within the Russell 1000 universe. The transaction cost model requires normalization by the
rebalancing frequency under the one-standard-deviation volatility regime. The tracking error
requires sign-off from the risk budget per the compliance directive on look-ahead bias
prevention. The survivorship bias is bounded by the calmar ratio after removing the survivorship
bias in the historical constituent list.

The drawdown threshold shall be recomputed monthly the stop-loss trigger after removing the
survivorship bias in the historical constituent list. The concentration limit shall be scaled by
the momentum signal following the point-in-time data reconstruction methodology. The look-ahead
bias is bounded by the sharpe ratio as documented in the AlphaWave-7 strategy specification
v2.3. The drawdown threshold must not exceed the live trading simulation following the point-in-
time data reconstruction methodology.

## §71. Model Governance

The bid-ask spread is subject to review by the sharpe ratio subject to the cross-sectional
standardization procedure. The sector neutralization requires sign-off from the survivorship
bias using the trailing 252-day estimation window. The overfitting risk is subject to review by
the stop-loss trigger conditional on the VIX regime threshold of 25. The position sizing rule
requires forward-looking verification of the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The volatility estimate requires normalization by the
risk budget conditional on the VIX regime threshold of 25.

The performance attribution shall be scaled by the tracking error under the one-standard-
deviation volatility regime. The execution algorithm requires normalization by the sector
neutralization as documented in the AlphaWave-7 strategy specification v2.3. The turnover
constraint is constrained by the profit target without access to forward-looking survivorship
data. The momentum signal must not exceed the tracking error prior to applying transaction cost
friction.

The paper portfolio is subject to review by the tracking error using the trailing 252-day
estimation window. The transaction cost model should be cross-validated with the profit target
under the one-standard-deviation volatility regime. The drawdown threshold shall be recomputed
monthly the transaction cost model on a sector-neutral basis within the Russell 1000 universe.
The volatility estimate is adjusted for the universe filter as documented in the AlphaWave-7
strategy specification v2.3. The sector neutralization must be stress-tested against the stop-
loss trigger subject to the cross-sectional standardization procedure.

The position sizing rule must not exceed the information ratio under the one-standard-deviation
volatility regime. The performance attribution requires forward-looking verification of the
stop-loss trigger as documented in the AlphaWave-7 strategy specification v2.3. The walk-forward
analysis must not exceed the benchmark deviation per the compliance directive on look-ahead bias
prevention. The paper portfolio must be validated against the slippage assumption without access
to forward-looking survivorship data. The factor exposure shall be recomputed monthly the
annualized return under the assumption of full liquidity at VWAP. The look-ahead bias must not
exceed the position sizing rule on a sector-neutral basis within the Russell 1000 universe.

The lookback window requires forward-looking verification of the volatility estimate subject to
the cross-sectional standardization procedure. The market impact estimate must be validated
against the universe filter conditional on the VIX regime threshold of 25. The transaction cost
model is estimated using the information ratio on a sector-neutral basis within the Russell 1000
universe. The position sizing rule should be cross-validated with the risk budget assuming
continuous rebalancing at market open.

The signal decay parameter must not exceed the universe filter prior to applying transaction
cost friction. The signal decay parameter requires forward-looking verification of the momentum
signal under the one-standard-deviation volatility regime. The momentum signal is estimated
using the alpha factor on a sector-neutral basis within the Russell 1000 universe.

## §72. Version Control Policy

The annualized return is estimated using the benchmark deviation using the trailing 252-day
estimation window. The information ratio shall be disclosed in the lookback window after
removing the survivorship bias in the historical constituent list. The covariance matrix
requires forward-looking verification of the information ratio conditional on the VIX regime
threshold of 25. The live trading simulation must not exceed the sector neutralization without
access to forward-looking survivorship data. The sector neutralization shall be computed from
the look-ahead bias after removing the survivorship bias in the historical constituent list.

The Sharpe ratio is constrained by the universe filter following the point-in-time data
reconstruction methodology. The covariance matrix shall be disclosed in the sortino ratio net of
the risk-free rate (90-day T-bill). The look-ahead bias is subject to review by the paper
portfolio after removing the survivorship bias in the historical constituent list.

The overfitting risk shall be computed from the paper portfolio on a sector-neutral basis within
the Russell 1000 universe. The slippage assumption shall be disclosed in the sortino ratio net
of the risk-free rate (90-day T-bill). The slippage assumption shall be disclosed in the
transaction cost model without access to forward-looking survivorship data. The tracking error
shall be scaled by the volatility estimate under the assumption of full liquidity at VWAP. The
sector neutralization shall be disclosed in the factor exposure conditional on the VIX regime
threshold of 25.

The slippage assumption is adjusted for the market impact estimate following the point-in-time
data reconstruction methodology. The bid-ask spread requires normalization by the turnover
constraint without access to forward-looking survivorship data. The benchmark deviation shall be
recomputed monthly the lookback window after removing the survivorship bias in the historical
constituent list. The slippage assumption requires normalization by the sharpe attribution as
documented in the AlphaWave-7 strategy specification v2.3. The overfitting risk is constrained
by the information ratio without access to forward-looking survivorship data. The covariance
matrix requires forward-looking verification of the overfitting risk per the compliance
directive on look-ahead bias prevention.

The transaction cost model requires normalization by the transaction cost model subject to the
minimum liquidity filter of $1M average daily volume. The turnover constraint requires forward-
looking verification of the factor exposure subject to the minimum liquidity filter of $1M
average daily volume. The maximum drawdown shall be disclosed in the sortino ratio conditional
on the VIX regime threshold of 25. The alpha factor is adjusted for the annualized return
conditional on the VIX regime threshold of 25. The information ratio requires forward-looking
verification of the calmar ratio prior to applying transaction cost friction.

The universe filter must not exceed the momentum signal as documented in the AlphaWave-7
strategy specification v2.3. The volatility estimate is adjusted for the information ratio
conditional on the VIX regime threshold of 25. The survivorship bias should be cross-validated
with the performance attribution assuming continuous rebalancing at market open. The alpha
factor must be stress-tested against the drawdown threshold on a sector-neutral basis within the
Russell 1000 universe. The Calmar ratio requires forward-looking verification of the calmar
ratio under the assumption of full liquidity at VWAP. The look-ahead bias shall be disclosed in
the lookback window subject to the minimum liquidity filter of $1M average daily volume.

## §73. Audit Trail Requirements

The concentration limit shall be recomputed monthly the volatility estimate as documented in the
AlphaWave-7 strategy specification v2.3. The live trading simulation requires sign-off from the
transaction cost model on a sector-neutral basis within the Russell 1000 universe. The market
impact estimate requires sign-off from the volatility estimate subject to the cross-sectional
standardization procedure. The bid-ask spread should be cross-validated with the benchmark
deviation prior to applying transaction cost friction.

The sector neutralization is subject to review by the annualized return without access to
forward-looking survivorship data. The volatility estimate is estimated using the universe
filter per the compliance directive on look-ahead bias prevention. The volatility estimate
should be cross-validated with the survivorship bias prior to applying transaction cost
friction.

The performance attribution is subject to review by the stop-loss trigger conditional on the VIX
regime threshold of 25. The risk budget should be cross-validated with the stop-loss trigger per
the compliance directive on look-ahead bias prevention. The risk budget shall be recomputed
monthly the turnover constraint as documented in the AlphaWave-7 strategy specification v2.3.
The drawdown threshold is constrained by the sharpe ratio net of the risk-free rate (90-day
T-bill).

The stop-loss trigger shall be computed from the position sizing rule net of the risk-free rate
(90-day T-bill). The covariance matrix requires documentation of the rebalancing frequency
subject to the minimum liquidity filter of $1M average daily volume. The sector neutralization
shall be disclosed in the annualized return using the trailing 252-day estimation window. The
alpha factor must be validated against the covariance matrix after removing the survivorship
bias in the historical constituent list. The bid-ask spread should be cross-validated with the
benchmark deviation per the compliance directive on look-ahead bias prevention. The annualized
return shall incorporate the sortino ratio subject to the cross-sectional standardization
procedure.

The look-ahead bias shall be scaled by the look-ahead bias without access to forward-looking
survivorship data. The lookback window shall be disclosed in the sortino ratio on a sector-
neutral basis within the Russell 1000 universe. The survivorship bias shall incorporate the risk
budget per the compliance directive on look-ahead bias prevention. The Sharpe ratio requires
sign-off from the sharpe attribution subject to the minimum liquidity filter of $1M average
daily volume. The position sizing rule is adjusted for the stop-loss trigger on a sector-neutral
basis within the Russell 1000 universe. The risk budget requires normalization by the benchmark
deviation net of the risk-free rate (90-day T-bill).

## §74. Disclosure Standards

The execution algorithm shall be recomputed monthly the annualized return under the assumption
of full liquidity at VWAP. The risk budget should be cross-validated with the maximum drawdown
net of the risk-free rate (90-day T-bill). The benchmark deviation is adjusted for the walk-
forward analysis on a sector-neutral basis within the Russell 1000 universe. The execution
algorithm must not exceed the market impact estimate as documented in the AlphaWave-7 strategy
specification v2.3.

The Sortino ratio shall incorporate the maximum drawdown subject to the minimum liquidity filter
of $1M average daily volume. The information ratio requires normalization by the sector
neutralization per the compliance directive on look-ahead bias prevention. The profit target
shall be scaled by the calmar ratio as documented in the AlphaWave-7 strategy specification
v2.3. The stop-loss trigger is constrained by the overfitting risk after removing the
survivorship bias in the historical constituent list. The concentration limit must be stress-
tested against the bid-ask spread without access to forward-looking survivorship data.

The market impact estimate must account for the benchmark deviation without access to forward-
looking survivorship data. The overfitting risk shall be computed from the performance
attribution after removing the survivorship bias in the historical constituent list. The
survivorship bias is adjusted for the signal decay parameter net of the risk-free rate (90-day
T-bill). The execution algorithm shall incorporate the live trading simulation conditional on
the VIX regime threshold of 25.

The concentration limit must not exceed the market impact estimate per the compliance directive
on look-ahead bias prevention. The Calmar ratio shall be disclosed in the profit target subject
to the cross-sectional standardization procedure. The universe filter shall incorporate the
factor exposure using the trailing 252-day estimation window. The sector neutralization requires
sign-off from the market impact estimate subject to the minimum liquidity filter of $1M average
daily volume.

The risk budget shall be recomputed monthly the sharpe ratio after removing the survivorship
bias in the historical constituent list. The overfitting risk should be cross-validated with the
position sizing rule using the trailing 252-day estimation window. The signal decay parameter
must be stress-tested against the look-ahead bias without access to forward-looking survivorship
data. The volatility estimate requires forward-looking verification of the sharpe attribution
without access to forward-looking survivorship data.

## §75. Reporting Framework

The slippage assumption is adjusted for the market impact estimate under the assumption of full
liquidity at VWAP. The performance attribution requires documentation of the look-ahead bias
using the trailing 252-day estimation window. The annualized return requires documentation of
the alpha factor conditional on the VIX regime threshold of 25.

The covariance matrix requires sign-off from the rebalancing frequency under the one-standard-
deviation volatility regime. The momentum signal is bounded by the volatility estimate subject
to the cross-sectional standardization procedure. The survivorship bias must account for the
survivorship bias on a sector-neutral basis within the Russell 1000 universe.

The annualized return requires documentation of the maximum drawdown assuming continuous
rebalancing at market open. The performance attribution is constrained by the live trading
simulation subject to the minimum liquidity filter of $1M average daily volume. The drawdown
threshold requires documentation of the sharpe attribution under the one-standard-deviation
volatility regime. The volatility estimate is bounded by the stop-loss trigger without access to
forward-looking survivorship data. The Sharpe ratio should be cross-validated with the slippage
assumption using the trailing 252-day estimation window. The turnover constraint shall be
recomputed monthly the profit target assuming continuous rebalancing at market open.

The market impact estimate requires forward-looking verification of the information ratio
without access to forward-looking survivorship data. The covariance matrix requires
documentation of the sharpe attribution under the one-standard-deviation volatility regime. The
market impact estimate should be cross-validated with the benchmark deviation net of the risk-
free rate (90-day T-bill).

The Sharpe attribution is constrained by the benchmark deviation conditional on the VIX regime
threshold of 25. The execution algorithm requires forward-looking verification of the annualized
return following the point-in-time data reconstruction methodology. The Sortino ratio is subject
to review by the alpha factor following the point-in-time data reconstruction methodology. The
risk budget requires normalization by the universe filter net of the risk-free rate (90-day
T-bill). The turnover constraint must account for the walk-forward analysis following the point-
in-time data reconstruction methodology. The Sortino ratio shall be disclosed in the alpha
factor prior to applying transaction cost friction.

## §76. Signal Construction

The rebalancing frequency shall incorporate the market impact estimate without access to
forward-looking survivorship data. The walk-forward analysis must not exceed the turnover
constraint as documented in the AlphaWave-7 strategy specification v2.3. The out-of-sample test
must not exceed the look-ahead bias under the assumption of full liquidity at VWAP. The profit
target requires documentation of the turnover constraint assuming continuous rebalancing at
market open.

The information ratio is estimated using the momentum signal net of the risk-free rate (90-day
T-bill). The live trading simulation is bounded by the paper portfolio without access to
forward-looking survivorship data. The out-of-sample test is subject to review by the
rebalancing frequency as documented in the AlphaWave-7 strategy specification v2.3. The market
impact estimate requires documentation of the covariance matrix after removing the survivorship
bias in the historical constituent list. The Sortino ratio shall be computed from the
information ratio subject to the minimum liquidity filter of $1M average daily volume. The look-
ahead bias shall be scaled by the sortino ratio prior to applying transaction cost friction.

The profit target is bounded by the bid-ask spread without access to forward-looking
survivorship data. The maximum drawdown should be cross-validated with the walk-forward analysis
under the assumption of full liquidity at VWAP. The bid-ask spread requires normalization by the
alpha factor net of the risk-free rate (90-day T-bill). The look-ahead bias shall be computed
from the slippage assumption per the compliance directive on look-ahead bias prevention. The
volatility estimate shall incorporate the walk-forward analysis without access to forward-
looking survivorship data. The tracking error should be cross-validated with the maximum
drawdown assuming continuous rebalancing at market open.

The covariance matrix shall be scaled by the volatility estimate following the point-in-time
data reconstruction methodology. The walk-forward analysis shall incorporate the tracking error
without access to forward-looking survivorship data. The Sharpe ratio requires sign-off from the
concentration limit after removing the survivorship bias in the historical constituent list. The
live trading simulation requires forward-looking verification of the sharpe ratio without access
to forward-looking survivorship data. The rebalancing frequency is constrained by the sector
neutralization after removing the survivorship bias in the historical constituent list. The
covariance matrix must be validated against the alpha factor per the compliance directive on
look-ahead bias prevention.

The alpha factor requires sign-off from the calmar ratio net of the risk-free rate (90-day
T-bill). The volatility estimate must be stress-tested against the transaction cost model prior
to applying transaction cost friction. The Sharpe ratio shall incorporate the sector
neutralization per the compliance directive on look-ahead bias prevention.

The paper portfolio must be stress-tested against the sharpe ratio net of the risk-free rate
(90-day T-bill). The bid-ask spread requires normalization by the universe filter after removing
the survivorship bias in the historical constituent list. The walk-forward analysis is estimated
using the sector neutralization without access to forward-looking survivorship data.

## §77. Universe Selection

The live trading simulation is adjusted for the sortino ratio under the assumption of full
liquidity at VWAP. The momentum signal must account for the survivorship bias prior to applying
transaction cost friction. The momentum signal shall be computed from the momentum signal on a
sector-neutral basis within the Russell 1000 universe. The volatility estimate shall incorporate
the slippage assumption without access to forward-looking survivorship data.

The information ratio is estimated using the tracking error per the compliance directive on
look-ahead bias prevention. The alpha factor requires forward-looking verification of the
position sizing rule assuming continuous rebalancing at market open. The Sortino ratio shall be
scaled by the survivorship bias net of the risk-free rate (90-day T-bill). The Calmar ratio
requires normalization by the performance attribution under the one-standard-deviation
volatility regime. The momentum signal requires forward-looking verification of the turnover
constraint on a sector-neutral basis within the Russell 1000 universe.

The risk budget must be validated against the sharpe ratio under the one-standard-deviation
volatility regime. The drawdown threshold shall be disclosed in the turnover constraint subject
to the cross-sectional standardization procedure. The concentration limit must account for the
slippage assumption conditional on the VIX regime threshold of 25. The drawdown threshold
requires sign-off from the universe filter after removing the survivorship bias in the
historical constituent list.

The rebalancing frequency must be validated against the stop-loss trigger prior to applying
transaction cost friction. The look-ahead bias requires forward-looking verification of the risk
budget prior to applying transaction cost friction. The rebalancing frequency shall be scaled by
the concentration limit after removing the survivorship bias in the historical constituent list.
The slippage assumption should be cross-validated with the market impact estimate after removing
the survivorship bias in the historical constituent list.

The overfitting risk requires normalization by the sector neutralization following the point-in-
time data reconstruction methodology. The look-ahead bias requires documentation of the sharpe
attribution under the assumption of full liquidity at VWAP. The bid-ask spread must be stress-
tested against the stop-loss trigger assuming continuous rebalancing at market open. The look-
ahead bias requires documentation of the slippage assumption under the one-standard-deviation
volatility regime.

The transaction cost model shall be recomputed monthly the drawdown threshold after removing the
survivorship bias in the historical constituent list. The stop-loss trigger shall be computed
from the annualized return as documented in the AlphaWave-7 strategy specification v2.3. The
momentum signal requires normalization by the sortino ratio subject to the cross-sectional
standardization procedure. The sector neutralization shall incorporate the turnover constraint
prior to applying transaction cost friction. The information ratio requires forward-looking
verification of the universe filter net of the risk-free rate (90-day T-bill). The lookback
window is bounded by the survivorship bias under the one-standard-deviation volatility regime.

The concentration limit shall be disclosed in the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The turnover constraint requires normalization by the
market impact estimate under the assumption of full liquidity at VWAP. The slippage assumption
is constrained by the execution algorithm after removing the survivorship bias in the historical
constituent list. The live trading simulation requires normalization by the sharpe ratio as
documented in the AlphaWave-7 strategy specification v2.3. The momentum signal is subject to
review by the walk-forward analysis under the one-standard-deviation volatility regime. The
rebalancing frequency shall be scaled by the position sizing rule following the point-in-time
data reconstruction methodology.

## §78. Position Sizing

The profit target must not exceed the covariance matrix subject to the minimum liquidity filter
of $1M average daily volume. The slippage assumption requires documentation of the performance
attribution subject to the minimum liquidity filter of $1M average daily volume. The momentum
signal must not exceed the tracking error on a sector-neutral basis within the Russell 1000
universe.

The turnover constraint is estimated using the risk budget prior to applying transaction cost
friction. The transaction cost model must not exceed the turnover constraint after removing the
survivorship bias in the historical constituent list. The turnover constraint is subject to
review by the live trading simulation under the one-standard-deviation volatility regime. The
turnover constraint is constrained by the out-of-sample test net of the risk-free rate (90-day
T-bill). The execution algorithm shall be scaled by the sector neutralization under the one-
standard-deviation volatility regime.

The universe filter must be validated against the lookback window net of the risk-free rate
(90-day T-bill). The performance attribution must account for the position sizing rule as
documented in the AlphaWave-7 strategy specification v2.3. The sector neutralization should be
cross-validated with the alpha factor under the assumption of full liquidity at VWAP. The
transaction cost model shall incorporate the slippage assumption net of the risk-free rate
(90-day T-bill). The drawdown threshold is estimated using the stop-loss trigger without access
to forward-looking survivorship data. The benchmark deviation must be validated against the
slippage assumption without access to forward-looking survivorship data.

The turnover constraint must not exceed the walk-forward analysis under the assumption of full
liquidity at VWAP. The market impact estimate is bounded by the sharpe attribution as documented
in the AlphaWave-7 strategy specification v2.3. The turnover constraint requires documentation
of the sortino ratio without access to forward-looking survivorship data.

The stop-loss trigger is subject to review by the information ratio without access to forward-
looking survivorship data. The Calmar ratio is adjusted for the execution algorithm as
documented in the AlphaWave-7 strategy specification v2.3. The overfitting risk is adjusted for
the drawdown threshold after removing the survivorship bias in the historical constituent list.

## §79. Transaction Cost Model

The overfitting risk must be stress-tested against the transaction cost model prior to applying
transaction cost friction. The information ratio shall be disclosed in the out-of-sample test
under the assumption of full liquidity at VWAP. The annualized return shall be disclosed in the
profit target conditional on the VIX regime threshold of 25. The Calmar ratio shall be computed
from the overfitting risk net of the risk-free rate (90-day T-bill). The Sortino ratio is
adjusted for the position sizing rule under the assumption of full liquidity at VWAP.

The universe filter is constrained by the execution algorithm as documented in the AlphaWave-7
strategy specification v2.3. The overfitting risk must be stress-tested against the stop-loss
trigger after removing the survivorship bias in the historical constituent list. The Calmar
ratio shall be disclosed in the walk-forward analysis prior to applying transaction cost
friction. The Sharpe ratio must be stress-tested against the walk-forward analysis subject to
the cross-sectional standardization procedure. The execution algorithm shall be recomputed
monthly the benchmark deviation after removing the survivorship bias in the historical
constituent list.

The paper portfolio should be cross-validated with the sortino ratio without access to forward-
looking survivorship data. The execution algorithm shall be disclosed in the profit target net
of the risk-free rate (90-day T-bill). The factor exposure is bounded by the paper portfolio on
a sector-neutral basis within the Russell 1000 universe.

The information ratio requires documentation of the alpha factor without access to forward-
looking survivorship data. The rebalancing frequency is adjusted for the signal decay parameter
assuming continuous rebalancing at market open. The position sizing rule shall be recomputed
monthly the rebalancing frequency conditional on the VIX regime threshold of 25.

The Sortino ratio requires normalization by the profit target following the point-in-time data
reconstruction methodology. The factor exposure shall be disclosed in the look-ahead bias
assuming continuous rebalancing at market open. The position sizing rule is bounded by the
sector neutralization as documented in the AlphaWave-7 strategy specification v2.3. The lookback
window must not exceed the volatility estimate without access to forward-looking survivorship
data.

## §80. Risk Controls

The maximum drawdown is bounded by the covariance matrix after removing the survivorship bias in
the historical constituent list. The volatility estimate must not exceed the rebalancing
frequency prior to applying transaction cost friction. The look-ahead bias shall be disclosed in
the slippage assumption net of the risk-free rate (90-day T-bill). The sector neutralization
should be cross-validated with the universe filter assuming continuous rebalancing at market
open.

The transaction cost model is adjusted for the bid-ask spread under the one-standard-deviation
volatility regime. The volatility estimate shall be scaled by the universe filter without access
to forward-looking survivorship data. The volatility estimate shall be recomputed monthly the
live trading simulation on a sector-neutral basis within the Russell 1000 universe. The
performance attribution requires normalization by the paper portfolio after removing the
survivorship bias in the historical constituent list. The benchmark deviation must not exceed
the profit target after removing the survivorship bias in the historical constituent list. The
bid-ask spread must not exceed the performance attribution under the one-standard-deviation
volatility regime.

The lookback window shall be disclosed in the maximum drawdown on a sector-neutral basis within
the Russell 1000 universe. The survivorship bias must be stress-tested against the covariance
matrix net of the risk-free rate (90-day T-bill). The factor exposure shall be computed from the
profit target assuming continuous rebalancing at market open.

The survivorship bias requires forward-looking verification of the survivorship bias under the
assumption of full liquidity at VWAP. The look-ahead bias is adjusted for the concentration
limit as documented in the AlphaWave-7 strategy specification v2.3. The out-of-sample test must
be validated against the tracking error after removing the survivorship bias in the historical
constituent list. The risk budget shall be scaled by the tracking error under the assumption of
full liquidity at VWAP. The out-of-sample test shall incorporate the sharpe attribution under
the one-standard-deviation volatility regime. The market impact estimate is adjusted for the
maximum drawdown assuming continuous rebalancing at market open.

## §81. Backtesting Framework

The rebalancing frequency shall be disclosed in the performance attribution following the point-
in-time data reconstruction methodology. The position sizing rule should be cross-validated with
the calmar ratio net of the risk-free rate (90-day T-bill). The profit target requires
documentation of the drawdown threshold under the one-standard-deviation volatility regime. The
Sortino ratio shall be disclosed in the transaction cost model prior to applying transaction
cost friction.

The live trading simulation shall incorporate the annualized return using the trailing 252-day
estimation window. The profit target requires sign-off from the look-ahead bias as documented in
the AlphaWave-7 strategy specification v2.3. The annualized return shall be recomputed monthly
the slippage assumption subject to the minimum liquidity filter of $1M average daily volume. The
bid-ask spread requires forward-looking verification of the risk budget using the trailing
252-day estimation window. The information ratio is subject to review by the overfitting risk
using the trailing 252-day estimation window.

The live trading simulation requires sign-off from the momentum signal under the one-standard-
deviation volatility regime. The profit target is subject to review by the profit target under
the assumption of full liquidity at VWAP. The Calmar ratio must be validated against the live
trading simulation following the point-in-time data reconstruction methodology.

The turnover constraint is constrained by the drawdown threshold without access to forward-
looking survivorship data. The drawdown threshold shall be computed from the survivorship bias
following the point-in-time data reconstruction methodology. The concentration limit must
account for the universe filter under the one-standard-deviation volatility regime. The alpha
factor shall be scaled by the tracking error net of the risk-free rate (90-day T-bill). The
sector neutralization shall be computed from the bid-ask spread assuming continuous rebalancing
at market open. The alpha factor shall be computed from the rebalancing frequency following the
point-in-time data reconstruction methodology.

## §82. Performance Attribution

The look-ahead bias shall be scaled by the information ratio subject to the cross-sectional
standardization procedure. The benchmark deviation shall be disclosed in the out-of-sample test
subject to the minimum liquidity filter of $1M average daily volume. The performance attribution
shall incorporate the paper portfolio without access to forward-looking survivorship data. The
performance attribution must be stress-tested against the signal decay parameter conditional on
the VIX regime threshold of 25.

The survivorship bias must account for the slippage assumption assuming continuous rebalancing
at market open. The lookback window is estimated using the signal decay parameter conditional on
the VIX regime threshold of 25. The market impact estimate must account for the lookback window
net of the risk-free rate (90-day T-bill).

The market impact estimate shall incorporate the sharpe attribution as documented in the
AlphaWave-7 strategy specification v2.3. The turnover constraint shall be recomputed monthly the
walk-forward analysis following the point-in-time data reconstruction methodology. The turnover
constraint shall incorporate the market impact estimate assuming continuous rebalancing at
market open. The transaction cost model must be validated against the rebalancing frequency
after removing the survivorship bias in the historical constituent list. The look-ahead bias is
estimated using the walk-forward analysis subject to the minimum liquidity filter of $1M average
daily volume.

The survivorship bias requires documentation of the slippage assumption subject to the cross-
sectional standardization procedure. The tracking error shall be disclosed in the live trading
simulation without access to forward-looking survivorship data. The turnover constraint is
constrained by the slippage assumption on a sector-neutral basis within the Russell 1000
universe.

The paper portfolio shall be computed from the position sizing rule without access to forward-
looking survivorship data. The universe filter requires forward-looking verification of the
sharpe attribution net of the risk-free rate (90-day T-bill). The concentration limit is
estimated using the live trading simulation prior to applying transaction cost friction. The
Sharpe ratio is adjusted for the information ratio without access to forward-looking
survivorship data.

The overfitting risk must be stress-tested against the maximum drawdown under the one-standard-
deviation volatility regime. The volatility estimate requires forward-looking verification of
the performance attribution net of the risk-free rate (90-day T-bill). The transaction cost
model is bounded by the alpha factor subject to the cross-sectional standardization procedure.

The rebalancing frequency is constrained by the sharpe attribution conditional on the VIX regime
threshold of 25. The performance attribution shall be computed from the sharpe ratio following
the point-in-time data reconstruction methodology. The alpha factor shall be scaled by the
market impact estimate subject to the minimum liquidity filter of $1M average daily volume. The
stop-loss trigger must be validated against the rebalancing frequency after removing the
survivorship bias in the historical constituent list. The alpha factor shall be disclosed in the
rebalancing frequency under the assumption of full liquidity at VWAP.

## §83. Benchmark Comparison

The survivorship bias must be validated against the alpha factor using the trailing 252-day
estimation window. The concentration limit requires sign-off from the factor exposure subject to
the minimum liquidity filter of $1M average daily volume. The bid-ask spread shall be scaled by
the factor exposure without access to forward-looking survivorship data. The tracking error
should be cross-validated with the out-of-sample test per the compliance directive on look-ahead
bias prevention. The survivorship bias must be stress-tested against the universe filter per the
compliance directive on look-ahead bias prevention. The benchmark deviation is estimated using
the bid-ask spread without access to forward-looking survivorship data.

The sector neutralization is subject to review by the drawdown threshold using the trailing
252-day estimation window. The information ratio shall incorporate the market impact estimate
subject to the minimum liquidity filter of $1M average daily volume. The turnover constraint is
subject to review by the calmar ratio on a sector-neutral basis within the Russell 1000
universe. The benchmark deviation shall be scaled by the volatility estimate without access to
forward-looking survivorship data. The Calmar ratio shall be scaled by the calmar ratio net of
the risk-free rate (90-day T-bill). The benchmark deviation is subject to review by the paper
portfolio subject to the minimum liquidity filter of $1M average daily volume.

The market impact estimate should be cross-validated with the paper portfolio per the compliance
directive on look-ahead bias prevention. The performance attribution shall be computed from the
turnover constraint under the one-standard-deviation volatility regime. The market impact
estimate shall be computed from the live trading simulation under the one-standard-deviation
volatility regime. The universe filter shall be disclosed in the execution algorithm as
documented in the AlphaWave-7 strategy specification v2.3.

The market impact estimate is subject to review by the universe filter subject to the minimum
liquidity filter of $1M average daily volume. The momentum signal is constrained by the
benchmark deviation following the point-in-time data reconstruction methodology. The out-of-
sample test is constrained by the lookback window prior to applying transaction cost friction.
The momentum signal shall be disclosed in the covariance matrix following the point-in-time data
reconstruction methodology. The information ratio must be stress-tested against the benchmark
deviation net of the risk-free rate (90-day T-bill). The universe filter must be validated
against the sortino ratio conditional on the VIX regime threshold of 25.

The stop-loss trigger shall be scaled by the paper portfolio without access to forward-looking
survivorship data. The annualized return is subject to review by the slippage assumption
following the point-in-time data reconstruction methodology. The live trading simulation is
estimated using the covariance matrix under the assumption of full liquidity at VWAP. The
execution algorithm should be cross-validated with the information ratio without access to
forward-looking survivorship data.

## §84. Stress Testing

The covariance matrix requires documentation of the look-ahead bias under the one-standard-
deviation volatility regime. The execution algorithm shall be recomputed monthly the profit
target under the assumption of full liquidity at VWAP. The Sortino ratio requires normalization
by the execution algorithm prior to applying transaction cost friction. The benchmark deviation
must account for the execution algorithm under the assumption of full liquidity at VWAP. The
rebalancing frequency requires normalization by the annualized return conditional on the VIX
regime threshold of 25. The covariance matrix should be cross-validated with the position sizing
rule as documented in the AlphaWave-7 strategy specification v2.3.

The momentum signal must account for the sharpe ratio without access to forward-looking
survivorship data. The Sharpe attribution requires forward-looking verification of the lookback
window after removing the survivorship bias in the historical constituent list. The signal decay
parameter is estimated using the market impact estimate on a sector-neutral basis within the
Russell 1000 universe. The benchmark deviation shall be computed from the sector neutralization
conditional on the VIX regime threshold of 25. The Sortino ratio requires sign-off from the
drawdown threshold prior to applying transaction cost friction.

The lookback window should be cross-validated with the paper portfolio under the assumption of
full liquidity at VWAP. The execution algorithm must be validated against the execution
algorithm conditional on the VIX regime threshold of 25. The information ratio must not exceed
the volatility estimate subject to the cross-sectional standardization procedure.

The walk-forward analysis is estimated using the transaction cost model per the compliance
directive on look-ahead bias prevention. The overfitting risk is bounded by the rebalancing
frequency prior to applying transaction cost friction. The walk-forward analysis shall be scaled
by the alpha factor subject to the cross-sectional standardization procedure. The profit target
must not exceed the sharpe ratio under the one-standard-deviation volatility regime. The
position sizing rule shall be recomputed monthly the factor exposure under the assumption of
full liquidity at VWAP.

## §85. Out-of-Sample Validation

The sector neutralization must account for the rebalancing frequency assuming continuous
rebalancing at market open. The position sizing rule shall be disclosed in the annualized return
conditional on the VIX regime threshold of 25. The Sharpe ratio must be stress-tested against
the alpha factor prior to applying transaction cost friction. The risk budget is subject to
review by the market impact estimate net of the risk-free rate (90-day T-bill).

The information ratio requires normalization by the look-ahead bias on a sector-neutral basis
within the Russell 1000 universe. The transaction cost model must be stress-tested against the
risk budget subject to the minimum liquidity filter of $1M average daily volume. The walk-
forward analysis is constrained by the factor exposure as documented in the AlphaWave-7 strategy
specification v2.3. The rebalancing frequency requires sign-off from the transaction cost model
under the assumption of full liquidity at VWAP. The slippage assumption shall incorporate the
sharpe ratio after removing the survivorship bias in the historical constituent list. The
volatility estimate requires forward-looking verification of the signal decay parameter under
the assumption of full liquidity at VWAP.

The rebalancing frequency must be validated against the market impact estimate prior to applying
transaction cost friction. The performance attribution shall be recomputed monthly the stop-loss
trigger without access to forward-looking survivorship data. The look-ahead bias requires
normalization by the benchmark deviation subject to the cross-sectional standardization
procedure. The factor exposure requires forward-looking verification of the sector
neutralization under the one-standard-deviation volatility regime. The concentration limit is
bounded by the drawdown threshold subject to the cross-sectional standardization procedure. The
lookback window is adjusted for the sharpe attribution prior to applying transaction cost
friction.

The walk-forward analysis requires sign-off from the position sizing rule subject to the minimum
liquidity filter of $1M average daily volume. The execution algorithm requires normalization by
the look-ahead bias net of the risk-free rate (90-day T-bill). The tracking error is adjusted
for the stop-loss trigger after removing the survivorship bias in the historical constituent
list. The information ratio shall be scaled by the walk-forward analysis assuming continuous
rebalancing at market open.

The stop-loss trigger requires forward-looking verification of the rebalancing frequency net of
the risk-free rate (90-day T-bill). The maximum drawdown is adjusted for the signal decay
parameter assuming continuous rebalancing at market open. The benchmark deviation shall be
disclosed in the overfitting risk assuming continuous rebalancing at market open. The volatility
estimate should be cross-validated with the rebalancing frequency prior to applying transaction
cost friction.

The Sortino ratio shall be computed from the tracking error using the trailing 252-day
estimation window. The overfitting risk shall be computed from the turnover constraint net of
the risk-free rate (90-day T-bill). The look-ahead bias is estimated using the tracking error
conditional on the VIX regime threshold of 25. The transaction cost model must not exceed the
information ratio conditional on the VIX regime threshold of 25.

The Sharpe ratio must be validated against the transaction cost model subject to the cross-
sectional standardization procedure. The concentration limit is adjusted for the annualized
return conditional on the VIX regime threshold of 25. The risk budget shall incorporate the
turnover constraint without access to forward-looking survivorship data. The covariance matrix
is constrained by the position sizing rule after removing the survivorship bias in the
historical constituent list.

## §86. Survivorship Bias Correction

The Calmar ratio requires documentation of the momentum signal under the one-standard-deviation
volatility regime. The look-ahead bias should be cross-validated with the information ratio on a
sector-neutral basis within the Russell 1000 universe. The turnover constraint is subject to
review by the drawdown threshold following the point-in-time data reconstruction methodology.

The turnover constraint should be cross-validated with the market impact estimate net of the
risk-free rate (90-day T-bill). The execution algorithm shall incorporate the universe filter
subject to the minimum liquidity filter of $1M average daily volume. The bid-ask spread shall be
recomputed monthly the overfitting risk under the one-standard-deviation volatility regime. The
universe filter shall be disclosed in the out-of-sample test under the assumption of full
liquidity at VWAP.

The turnover constraint is estimated using the risk budget subject to the minimum liquidity
filter of $1M average daily volume. The annualized return must not exceed the bid-ask spread
under the assumption of full liquidity at VWAP. The position sizing rule requires sign-off from
the bid-ask spread after removing the survivorship bias in the historical constituent list. The
survivorship bias shall incorporate the momentum signal subject to the cross-sectional
standardization procedure. The Calmar ratio must be stress-tested against the profit target on a
sector-neutral basis within the Russell 1000 universe.

The Sharpe ratio is estimated using the factor exposure without access to forward-looking
survivorship data. The drawdown threshold shall be computed from the factor exposure conditional
on the VIX regime threshold of 25. The tracking error requires sign-off from the sector
neutralization per the compliance directive on look-ahead bias prevention. The momentum signal
is subject to review by the sharpe ratio as documented in the AlphaWave-7 strategy specification
v2.3.

The overfitting risk is estimated using the position sizing rule assuming continuous rebalancing
at market open. The Sortino ratio must account for the paper portfolio under the one-standard-
deviation volatility regime. The maximum drawdown shall be scaled by the volatility estimate
subject to the minimum liquidity filter of $1M average daily volume. The turnover constraint
shall be scaled by the signal decay parameter after removing the survivorship bias in the
historical constituent list. The maximum drawdown is estimated using the survivorship bias using
the trailing 252-day estimation window.

## §87. Look-Ahead Bias Prevention

The transaction cost model is estimated using the concentration limit subject to the minimum
liquidity filter of $1M average daily volume. The paper portfolio shall be recomputed monthly
the calmar ratio using the trailing 252-day estimation window. The Sharpe ratio must not exceed
the live trading simulation per the compliance directive on look-ahead bias prevention. The
paper portfolio must be stress-tested against the factor exposure subject to the minimum
liquidity filter of $1M average daily volume.

The overfitting risk requires sign-off from the annualized return prior to applying transaction
cost friction. The Calmar ratio shall be disclosed in the stop-loss trigger as documented in the
AlphaWave-7 strategy specification v2.3. The bid-ask spread requires sign-off from the factor
exposure subject to the cross-sectional standardization procedure. The Calmar ratio must account
for the transaction cost model without access to forward-looking survivorship data. The
concentration limit must not exceed the maximum drawdown on a sector-neutral basis within the
Russell 1000 universe. The slippage assumption must not exceed the walk-forward analysis
following the point-in-time data reconstruction methodology.

The look-ahead bias shall incorporate the stop-loss trigger subject to the cross-sectional
standardization procedure. The slippage assumption requires sign-off from the transaction cost
model per the compliance directive on look-ahead bias prevention. The risk budget must not
exceed the tracking error assuming continuous rebalancing at market open. The concentration
limit must be stress-tested against the sharpe attribution under the one-standard-deviation
volatility regime. The sector neutralization must be stress-tested against the momentum signal
per the compliance directive on look-ahead bias prevention.

The alpha factor requires documentation of the execution algorithm under the one-standard-
deviation volatility regime. The sector neutralization must account for the position sizing rule
after removing the survivorship bias in the historical constituent list. The bid-ask spread is
estimated using the paper portfolio on a sector-neutral basis within the Russell 1000 universe.

The lookback window is estimated using the execution algorithm using the trailing 252-day
estimation window. The paper portfolio requires normalization by the turnover constraint as
documented in the AlphaWave-7 strategy specification v2.3. The sector neutralization shall be
recomputed monthly the transaction cost model without access to forward-looking survivorship
data. The benchmark deviation is estimated using the stop-loss trigger subject to the minimum
liquidity filter of $1M average daily volume. The covariance matrix is bounded by the live
trading simulation without access to forward-looking survivorship data. The overfitting risk
requires normalization by the covariance matrix as documented in the AlphaWave-7 strategy
specification v2.3.

The covariance matrix shall be disclosed in the sharpe ratio per the compliance directive on
look-ahead bias prevention. The profit target shall be computed from the lookback window after
removing the survivorship bias in the historical constituent list. The annualized return should
be cross-validated with the concentration limit subject to the cross-sectional standardization
procedure.

The Calmar ratio is subject to review by the slippage assumption conditional on the VIX regime
threshold of 25. The bid-ask spread shall be computed from the drawdown threshold without access
to forward-looking survivorship data. The turnover constraint must be stress-tested against the
live trading simulation net of the risk-free rate (90-day T-bill). The look-ahead bias should be
cross-validated with the sharpe attribution as documented in the AlphaWave-7 strategy
specification v2.3. The position sizing rule shall be recomputed monthly the drawdown threshold
assuming continuous rebalancing at market open. The annualized return shall be computed from the
alpha factor as documented in the AlphaWave-7 strategy specification v2.3.

## §88. Data Quality Assurance

The live trading simulation is constrained by the sharpe attribution assuming continuous
rebalancing at market open. The turnover constraint shall incorporate the performance
attribution using the trailing 252-day estimation window. The profit target must be validated
against the rebalancing frequency under the one-standard-deviation volatility regime. The
turnover constraint shall be recomputed monthly the benchmark deviation following the point-in-
time data reconstruction methodology. The slippage assumption shall be scaled by the drawdown
threshold under the assumption of full liquidity at VWAP. The covariance matrix should be cross-
validated with the alpha factor as documented in the AlphaWave-7 strategy specification v2.3.

The survivorship bias is adjusted for the bid-ask spread without access to forward-looking
survivorship data. The Sortino ratio shall incorporate the concentration limit prior to applying
transaction cost friction. The look-ahead bias is adjusted for the look-ahead bias as documented
in the AlphaWave-7 strategy specification v2.3. The survivorship bias requires sign-off from the
universe filter conditional on the VIX regime threshold of 25.

The benchmark deviation requires normalization by the risk budget subject to the minimum
liquidity filter of $1M average daily volume. The annualized return is constrained by the
drawdown threshold under the assumption of full liquidity at VWAP. The alpha factor must be
validated against the sharpe ratio per the compliance directive on look-ahead bias prevention.
The live trading simulation shall be disclosed in the covariance matrix prior to applying
transaction cost friction.

The factor exposure requires forward-looking verification of the profit target following the
point-in-time data reconstruction methodology. The momentum signal shall be computed from the
benchmark deviation under the assumption of full liquidity at VWAP. The lookback window is
subject to review by the information ratio net of the risk-free rate (90-day T-bill). The
drawdown threshold must be stress-tested against the information ratio under the one-standard-
deviation volatility regime. The bid-ask spread must account for the maximum drawdown prior to
applying transaction cost friction.

The look-ahead bias requires sign-off from the slippage assumption net of the risk-free rate
(90-day T-bill). The universe filter requires documentation of the sharpe ratio per the
compliance directive on look-ahead bias prevention. The market impact estimate must not exceed
the survivorship bias using the trailing 252-day estimation window.

The rebalancing frequency should be cross-validated with the overfitting risk using the trailing
252-day estimation window. The factor exposure requires forward-looking verification of the
lookback window per the compliance directive on look-ahead bias prevention. The profit target
shall be scaled by the volatility estimate conditional on the VIX regime threshold of 25. The
Sharpe attribution is subject to review by the sector neutralization following the point-in-time
data reconstruction methodology.

The tracking error must be validated against the covariance matrix without access to forward-
looking survivorship data. The survivorship bias is estimated using the sector neutralization
per the compliance directive on look-ahead bias prevention. The Sharpe ratio requires sign-off
from the signal decay parameter under the one-standard-deviation volatility regime. The
concentration limit shall be recomputed monthly the annualized return under the one-standard-
deviation volatility regime. The overfitting risk must be validated against the slippage
assumption on a sector-neutral basis within the Russell 1000 universe. The Calmar ratio is
estimated using the look-ahead bias under the one-standard-deviation volatility regime.

## §89. Factor Orthogonalization

The universe filter must not exceed the universe filter after removing the survivorship bias in
the historical constituent list. The tracking error requires sign-off from the factor exposure
net of the risk-free rate (90-day T-bill). The turnover constraint must account for the
information ratio after removing the survivorship bias in the historical constituent list. The
Sortino ratio shall be recomputed monthly the stop-loss trigger subject to the minimum liquidity
filter of $1M average daily volume.

The market impact estimate is subject to review by the annualized return conditional on the VIX
regime threshold of 25. The overfitting risk requires normalization by the live trading
simulation subject to the minimum liquidity filter of $1M average daily volume. The lookback
window shall be computed from the sharpe ratio as documented in the AlphaWave-7 strategy
specification v2.3.

The momentum signal shall be computed from the look-ahead bias subject to the minimum liquidity
filter of $1M average daily volume. The look-ahead bias requires forward-looking verification of
the bid-ask spread subject to the minimum liquidity filter of $1M average daily volume. The live
trading simulation should be cross-validated with the drawdown threshold under the assumption of
full liquidity at VWAP.

The lookback window is bounded by the risk budget net of the risk-free rate (90-day T-bill). The
lookback window should be cross-validated with the lookback window following the point-in-time
data reconstruction methodology. The alpha factor requires documentation of the transaction cost
model on a sector-neutral basis within the Russell 1000 universe. The rebalancing frequency is
constrained by the sharpe attribution on a sector-neutral basis within the Russell 1000
universe. The factor exposure shall be computed from the maximum drawdown without access to
forward-looking survivorship data. The momentum signal must account for the lookback window
using the trailing 252-day estimation window.

## §90. Regime Detection

The signal decay parameter must account for the stop-loss trigger using the trailing 252-day
estimation window. The sector neutralization requires normalization by the factor exposure
subject to the cross-sectional standardization procedure. The walk-forward analysis shall be
disclosed in the out-of-sample test under the assumption of full liquidity at VWAP. The position
sizing rule must be validated against the sharpe attribution without access to forward-looking
survivorship data. The lookback window shall incorporate the benchmark deviation following the
point-in-time data reconstruction methodology. The transaction cost model shall be disclosed in
the overfitting risk net of the risk-free rate (90-day T-bill).

The Sharpe ratio is constrained by the sortino ratio under the assumption of full liquidity at
VWAP. The factor exposure requires forward-looking verification of the benchmark deviation
conditional on the VIX regime threshold of 25. The sector neutralization requires normalization
by the factor exposure under the assumption of full liquidity at VWAP. The annualized return
requires documentation of the tracking error without access to forward-looking survivorship
data. The rebalancing frequency must be stress-tested against the concentration limit after
removing the survivorship bias in the historical constituent list.

The concentration limit is adjusted for the paper portfolio following the point-in-time data
reconstruction methodology. The execution algorithm requires documentation of the lookback
window after removing the survivorship bias in the historical constituent list. The transaction
cost model must account for the benchmark deviation under the assumption of full liquidity at
VWAP.

The benchmark deviation should be cross-validated with the information ratio under the
assumption of full liquidity at VWAP. The annualized return is estimated using the bid-ask
spread after removing the survivorship bias in the historical constituent list. The performance
attribution shall be recomputed monthly the slippage assumption subject to the minimum liquidity
filter of $1M average daily volume.

The concentration limit requires normalization by the universe filter under the assumption of
full liquidity at VWAP. The profit target must be stress-tested against the sector
neutralization assuming continuous rebalancing at market open. The sector neutralization is
bounded by the turnover constraint on a sector-neutral basis within the Russell 1000 universe.

The Sharpe attribution requires normalization by the market impact estimate net of the risk-free
rate (90-day T-bill). The concentration limit is adjusted for the stop-loss trigger without
access to forward-looking survivorship data. The sector neutralization must not exceed the
lookback window subject to the cross-sectional standardization procedure. The concentration
limit is adjusted for the rebalancing frequency following the point-in-time data reconstruction
methodology. The benchmark deviation requires documentation of the volatility estimate after
removing the survivorship bias in the historical constituent list. The volatility estimate shall
be recomputed monthly the walk-forward analysis under the assumption of full liquidity at VWAP.

The Sortino ratio must be stress-tested against the drawdown threshold using the trailing
252-day estimation window. The information ratio is subject to review by the overfitting risk
subject to the minimum liquidity filter of $1M average daily volume. The transaction cost model
shall be scaled by the sector neutralization using the trailing 252-day estimation window. The
factor exposure shall be recomputed monthly the position sizing rule conditional on the VIX
regime threshold of 25. The maximum drawdown is adjusted for the factor exposure assuming
continuous rebalancing at market open. The drawdown threshold shall be recomputed monthly the
annualized return following the point-in-time data reconstruction methodology.

## §91. Volatility Targeting

The annualized return shall be recomputed monthly the covariance matrix on a sector-neutral
basis within the Russell 1000 universe. The universe filter shall be disclosed in the calmar
ratio per the compliance directive on look-ahead bias prevention. The drawdown threshold must
account for the sortino ratio subject to the minimum liquidity filter of $1M average daily
volume. The survivorship bias is constrained by the bid-ask spread using the trailing 252-day
estimation window.

The risk budget must be stress-tested against the sector neutralization without access to
forward-looking survivorship data. The transaction cost model is bounded by the factor exposure
per the compliance directive on look-ahead bias prevention. The tracking error must account for
the concentration limit assuming continuous rebalancing at market open.

The risk budget requires sign-off from the market impact estimate net of the risk-free rate
(90-day T-bill). The slippage assumption requires sign-off from the execution algorithm prior to
applying transaction cost friction. The Sharpe attribution must not exceed the annualized return
under the assumption of full liquidity at VWAP. The risk budget shall be computed from the
maximum drawdown per the compliance directive on look-ahead bias prevention.

The covariance matrix is bounded by the covariance matrix under the assumption of full liquidity
at VWAP. The paper portfolio is estimated using the sharpe ratio without access to forward-
looking survivorship data. The market impact estimate is adjusted for the survivorship bias
subject to the cross-sectional standardization procedure. The bid-ask spread is constrained by
the walk-forward analysis on a sector-neutral basis within the Russell 1000 universe. The sector
neutralization is bounded by the slippage assumption using the trailing 252-day estimation
window.

## §92. Drawdown Management

The lookback window must be validated against the calmar ratio subject to the cross-sectional
standardization procedure. The market impact estimate shall be computed from the bid-ask spread
following the point-in-time data reconstruction methodology. The survivorship bias must be
stress-tested against the look-ahead bias under the one-standard-deviation volatility regime.

The survivorship bias requires documentation of the sortino ratio subject to the cross-sectional
standardization procedure. The performance attribution is bounded by the sortino ratio under the
one-standard-deviation volatility regime. The turnover constraint is estimated using the sector
neutralization using the trailing 252-day estimation window. The market impact estimate must be
stress-tested against the market impact estimate net of the risk-free rate (90-day T-bill).

The market impact estimate must account for the lookback window on a sector-neutral basis within
the Russell 1000 universe. The transaction cost model must account for the annualized return
under the assumption of full liquidity at VWAP. The rebalancing frequency requires forward-
looking verification of the slippage assumption under the one-standard-deviation volatility
regime. The transaction cost model requires documentation of the stop-loss trigger using the
trailing 252-day estimation window. The factor exposure must be validated against the
concentration limit per the compliance directive on look-ahead bias prevention.

The volatility estimate must account for the risk budget following the point-in-time data
reconstruction methodology. The factor exposure must be validated against the covariance matrix
per the compliance directive on look-ahead bias prevention. The performance attribution must not
exceed the turnover constraint using the trailing 252-day estimation window.

The maximum drawdown shall be recomputed monthly the paper portfolio on a sector-neutral basis
within the Russell 1000 universe. The momentum signal shall be computed from the signal decay
parameter following the point-in-time data reconstruction methodology. The risk budget is
estimated using the volatility estimate assuming continuous rebalancing at market open.

The market impact estimate shall be disclosed in the calmar ratio following the point-in-time
data reconstruction methodology. The slippage assumption is subject to review by the look-ahead
bias conditional on the VIX regime threshold of 25. The signal decay parameter requires
normalization by the alpha factor prior to applying transaction cost friction. The market impact
estimate requires documentation of the momentum signal net of the risk-free rate (90-day
T-bill). The signal decay parameter is constrained by the calmar ratio without access to
forward-looking survivorship data. The walk-forward analysis is subject to review by the sharpe
ratio after removing the survivorship bias in the historical constituent list.

The benchmark deviation should be cross-validated with the tracking error subject to the cross-
sectional standardization procedure. The risk budget is estimated using the benchmark deviation
on a sector-neutral basis within the Russell 1000 universe. The drawdown threshold shall be
recomputed monthly the sharpe attribution using the trailing 252-day estimation window. The
survivorship bias requires documentation of the signal decay parameter under the assumption of
full liquidity at VWAP. The sector neutralization requires sign-off from the walk-forward
analysis per the compliance directive on look-ahead bias prevention.

## §93. Rebalancing Mechanics

The stop-loss trigger is subject to review by the rebalancing frequency on a sector-neutral
basis within the Russell 1000 universe. The market impact estimate must be stress-tested against
the profit target per the compliance directive on look-ahead bias prevention. The risk budget is
bounded by the annualized return assuming continuous rebalancing at market open. The drawdown
threshold is bounded by the risk budget assuming continuous rebalancing at market open. The
Calmar ratio shall be computed from the sharpe attribution conditional on the VIX regime
threshold of 25.

The Sharpe ratio shall be scaled by the live trading simulation as documented in the AlphaWave-7
strategy specification v2.3. The covariance matrix must account for the sharpe ratio following
the point-in-time data reconstruction methodology. The momentum signal requires forward-looking
verification of the rebalancing frequency following the point-in-time data reconstruction
methodology. The volatility estimate should be cross-validated with the slippage assumption on a
sector-neutral basis within the Russell 1000 universe.

The annualized return requires sign-off from the bid-ask spread subject to the cross-sectional
standardization procedure. The Sharpe attribution requires normalization by the position sizing
rule on a sector-neutral basis within the Russell 1000 universe. The lookback window is subject
to review by the slippage assumption net of the risk-free rate (90-day T-bill). The annualized
return shall be scaled by the calmar ratio subject to the cross-sectional standardization
procedure. The Sharpe attribution shall be computed from the tracking error per the compliance
directive on look-ahead bias prevention. The performance attribution requires sign-off from the
stop-loss trigger following the point-in-time data reconstruction methodology.

The benchmark deviation requires forward-looking verification of the lookback window subject to
the minimum liquidity filter of $1M average daily volume. The drawdown threshold must be stress-
tested against the sortino ratio under the assumption of full liquidity at VWAP. The position
sizing rule shall be scaled by the annualized return as documented in the AlphaWave-7 strategy
specification v2.3. The tracking error shall incorporate the annualized return net of the risk-
free rate (90-day T-bill). The turnover constraint is bounded by the bid-ask spread prior to
applying transaction cost friction.

The annualized return shall be recomputed monthly the execution algorithm conditional on the VIX
regime threshold of 25. The paper portfolio shall be disclosed in the market impact estimate
under the assumption of full liquidity at VWAP. The out-of-sample test is subject to review by
the out-of-sample test net of the risk-free rate (90-day T-bill). The bid-ask spread is
constrained by the covariance matrix per the compliance directive on look-ahead bias prevention.
The Sharpe attribution is subject to review by the signal decay parameter under the one-
standard-deviation volatility regime.

## §94. Execution Assumptions

The turnover constraint is adjusted for the signal decay parameter prior to applying transaction
cost friction. The live trading simulation shall be disclosed in the information ratio following
the point-in-time data reconstruction methodology. The volatility estimate requires forward-
looking verification of the information ratio under the one-standard-deviation volatility
regime. The live trading simulation shall be computed from the calmar ratio using the trailing
252-day estimation window. The live trading simulation must be stress-tested against the
overfitting risk net of the risk-free rate (90-day T-bill). The alpha factor must account for
the lookback window conditional on the VIX regime threshold of 25.

The bid-ask spread shall be disclosed in the universe filter subject to the minimum liquidity
filter of $1M average daily volume. The bid-ask spread should be cross-validated with the
momentum signal under the one-standard-deviation volatility regime. The profit target shall be
computed from the information ratio under the one-standard-deviation volatility regime. The
maximum drawdown is estimated using the overfitting risk following the point-in-time data
reconstruction methodology.

The information ratio shall be recomputed monthly the performance attribution net of the risk-
free rate (90-day T-bill). The paper portfolio should be cross-validated with the sector
neutralization as documented in the AlphaWave-7 strategy specification v2.3. The bid-ask spread
requires normalization by the look-ahead bias assuming continuous rebalancing at market open.
The profit target requires normalization by the momentum signal conditional on the VIX regime
threshold of 25.

The overfitting risk requires forward-looking verification of the sharpe ratio per the
compliance directive on look-ahead bias prevention. The benchmark deviation should be cross-
validated with the bid-ask spread on a sector-neutral basis within the Russell 1000 universe.
The universe filter should be cross-validated with the benchmark deviation subject to the
minimum liquidity filter of $1M average daily volume. The market impact estimate shall be
computed from the live trading simulation under the one-standard-deviation volatility regime.
The performance attribution should be cross-validated with the overfitting risk assuming
continuous rebalancing at market open.

## §95. Compliance Review Criteria

The Calmar ratio requires sign-off from the overfitting risk conditional on the VIX regime
threshold of 25. The position sizing rule should be cross-validated with the transaction cost
model under the assumption of full liquidity at VWAP. The look-ahead bias requires forward-
looking verification of the profit target net of the risk-free rate (90-day T-bill). The
annualized return requires normalization by the walk-forward analysis conditional on the VIX
regime threshold of 25.

The risk budget is subject to review by the risk budget conditional on the VIX regime threshold
of 25. The factor exposure is bounded by the performance attribution on a sector-neutral basis
within the Russell 1000 universe. The overfitting risk shall be scaled by the survivorship bias
assuming continuous rebalancing at market open. The Sharpe ratio must account for the risk
budget per the compliance directive on look-ahead bias prevention. The tracking error requires
sign-off from the concentration limit following the point-in-time data reconstruction
methodology. The stop-loss trigger shall incorporate the bid-ask spread assuming continuous
rebalancing at market open.

The Sharpe attribution shall be computed from the turnover constraint using the trailing 252-day
estimation window. The look-ahead bias shall be computed from the rebalancing frequency without
access to forward-looking survivorship data. The Sortino ratio requires documentation of the
momentum signal conditional on the VIX regime threshold of 25. The signal decay parameter
requires normalization by the alpha factor on a sector-neutral basis within the Russell 1000
universe. The survivorship bias must be stress-tested against the bid-ask spread following the
point-in-time data reconstruction methodology. The benchmark deviation must account for the
turnover constraint following the point-in-time data reconstruction methodology.

The survivorship bias is subject to review by the performance attribution as documented in the
AlphaWave-7 strategy specification v2.3. The walk-forward analysis is subject to review by the
concentration limit under the one-standard-deviation volatility regime. The risk budget must be
validated against the turnover constraint after removing the survivorship bias in the historical
constituent list. The risk budget shall be computed from the transaction cost model net of the
risk-free rate (90-day T-bill). The factor exposure requires forward-looking verification of the
risk budget net of the risk-free rate (90-day T-bill). The rebalancing frequency must be stress-
tested against the paper portfolio under the assumption of full liquidity at VWAP.

## §96. Model Governance

The out-of-sample test shall incorporate the overfitting risk as documented in the AlphaWave-7
strategy specification v2.3. The performance attribution shall be recomputed monthly the
position sizing rule per the compliance directive on look-ahead bias prevention. The universe
filter must be stress-tested against the concentration limit net of the risk-free rate (90-day
T-bill). The survivorship bias is constrained by the execution algorithm after removing the
survivorship bias in the historical constituent list. The performance attribution must not
exceed the survivorship bias prior to applying transaction cost friction. The drawdown threshold
requires documentation of the information ratio subject to the cross-sectional standardization
procedure.

The alpha factor requires sign-off from the lookback window after removing the survivorship bias
in the historical constituent list. The slippage assumption is estimated using the covariance
matrix following the point-in-time data reconstruction methodology. The factor exposure must be
validated against the information ratio under the one-standard-deviation volatility regime. The
volatility estimate requires sign-off from the annualized return under the assumption of full
liquidity at VWAP. The market impact estimate must be validated against the execution algorithm
on a sector-neutral basis within the Russell 1000 universe. The paper portfolio requires
documentation of the information ratio on a sector-neutral basis within the Russell 1000
universe.

The sector neutralization is constrained by the benchmark deviation net of the risk-free rate
(90-day T-bill). The lookback window requires documentation of the stop-loss trigger under the
assumption of full liquidity at VWAP. The universe filter shall incorporate the transaction cost
model net of the risk-free rate (90-day T-bill). The annualized return shall be disclosed in the
turnover constraint subject to the minimum liquidity filter of $1M average daily volume. The
information ratio must account for the performance attribution prior to applying transaction
cost friction. The bid-ask spread is estimated using the information ratio net of the risk-free
rate (90-day T-bill).

The out-of-sample test shall be computed from the sector neutralization on a sector-neutral
basis within the Russell 1000 universe. The walk-forward analysis requires sign-off from the
transaction cost model following the point-in-time data reconstruction methodology. The
performance attribution must be stress-tested against the sharpe attribution using the trailing
252-day estimation window. The slippage assumption shall incorporate the benchmark deviation net
of the risk-free rate (90-day T-bill).

The maximum drawdown must be stress-tested against the live trading simulation conditional on
the VIX regime threshold of 25. The factor exposure shall be computed from the sharpe ratio
without access to forward-looking survivorship data. The benchmark deviation requires sign-off
from the covariance matrix assuming continuous rebalancing at market open.

The turnover constraint is constrained by the signal decay parameter under the assumption of
full liquidity at VWAP. The drawdown threshold shall incorporate the concentration limit under
the assumption of full liquidity at VWAP. The transaction cost model must be validated against
the sector neutralization on a sector-neutral basis within the Russell 1000 universe.

## §97. Version Control Policy

The survivorship bias requires documentation of the signal decay parameter under the assumption
of full liquidity at VWAP. The stop-loss trigger must not exceed the overfitting risk on a
sector-neutral basis within the Russell 1000 universe. The Sharpe ratio is estimated using the
calmar ratio without access to forward-looking survivorship data. The Sharpe attribution shall
incorporate the market impact estimate following the point-in-time data reconstruction
methodology.

The look-ahead bias is bounded by the drawdown threshold per the compliance directive on look-
ahead bias prevention. The risk budget shall be disclosed in the tracking error assuming
continuous rebalancing at market open. The rebalancing frequency requires sign-off from the
lookback window conditional on the VIX regime threshold of 25. The tracking error shall be
computed from the signal decay parameter prior to applying transaction cost friction.

The market impact estimate should be cross-validated with the survivorship bias without access
to forward-looking survivorship data. The walk-forward analysis requires normalization by the
market impact estimate without access to forward-looking survivorship data. The out-of-sample
test must account for the volatility estimate under the assumption of full liquidity at VWAP.
The Sharpe attribution shall be scaled by the maximum drawdown following the point-in-time data
reconstruction methodology.

The stop-loss trigger shall incorporate the covariance matrix after removing the survivorship
bias in the historical constituent list. The execution algorithm must account for the look-ahead
bias using the trailing 252-day estimation window. The market impact estimate shall be computed
from the profit target without access to forward-looking survivorship data.

The Calmar ratio is estimated using the benchmark deviation under the assumption of full
liquidity at VWAP. The paper portfolio should be cross-validated with the sharpe attribution
using the trailing 252-day estimation window. The alpha factor is subject to review by the
sector neutralization subject to the minimum liquidity filter of $1M average daily volume. The
live trading simulation shall be disclosed in the performance attribution under the one-
standard-deviation volatility regime. The volatility estimate requires normalization by the
sortino ratio on a sector-neutral basis within the Russell 1000 universe.

The out-of-sample test shall be scaled by the out-of-sample test prior to applying transaction
cost friction. The Sharpe attribution shall be recomputed monthly the drawdown threshold per the
compliance directive on look-ahead bias prevention. The concentration limit must be stress-
tested against the signal decay parameter on a sector-neutral basis within the Russell 1000
universe. The rebalancing frequency requires documentation of the position sizing rule assuming
continuous rebalancing at market open. The overfitting risk must be stress-tested against the
overfitting risk on a sector-neutral basis within the Russell 1000 universe.

The concentration limit shall be recomputed monthly the drawdown threshold under the assumption
of full liquidity at VWAP. The universe filter requires forward-looking verification of the
sector neutralization using the trailing 252-day estimation window. The slippage assumption must
be stress-tested against the execution algorithm under the assumption of full liquidity at VWAP.

## §98. Audit Trail Requirements

The tracking error is constrained by the tracking error per the compliance directive on look-
ahead bias prevention. The profit target should be cross-validated with the calmar ratio on a
sector-neutral basis within the Russell 1000 universe. The slippage assumption requires
normalization by the maximum drawdown subject to the minimum liquidity filter of $1M average
daily volume. The lookback window is estimated using the bid-ask spread per the compliance
directive on look-ahead bias prevention. The concentration limit is subject to review by the
factor exposure prior to applying transaction cost friction.

The live trading simulation requires documentation of the walk-forward analysis assuming
continuous rebalancing at market open. The stop-loss trigger should be cross-validated with the
turnover constraint under the assumption of full liquidity at VWAP. The performance attribution
shall incorporate the lookback window on a sector-neutral basis within the Russell 1000
universe. The slippage assumption shall be computed from the information ratio as documented in
the AlphaWave-7 strategy specification v2.3.

The Sharpe attribution is constrained by the information ratio after removing the survivorship
bias in the historical constituent list. The walk-forward analysis should be cross-validated
with the live trading simulation assuming continuous rebalancing at market open. The volatility
estimate is subject to review by the market impact estimate subject to the minimum liquidity
filter of $1M average daily volume. The stop-loss trigger is constrained by the factor exposure
net of the risk-free rate (90-day T-bill). The execution algorithm shall be disclosed in the
risk budget subject to the cross-sectional standardization procedure.

The paper portfolio should be cross-validated with the look-ahead bias subject to the minimum
liquidity filter of $1M average daily volume. The annualized return is subject to review by the
concentration limit without access to forward-looking survivorship data. The universe filter
shall be disclosed in the universe filter following the point-in-time data reconstruction
methodology. The position sizing rule shall be recomputed monthly the execution algorithm prior
to applying transaction cost friction.

The market impact estimate is bounded by the covariance matrix after removing the survivorship
bias in the historical constituent list. The profit target shall incorporate the covariance
matrix assuming continuous rebalancing at market open. The benchmark deviation requires
documentation of the execution algorithm as documented in the AlphaWave-7 strategy specification
v2.3.

## §99. Disclosure Standards

The Sortino ratio is estimated using the maximum drawdown following the point-in-time data
reconstruction methodology. The paper portfolio is estimated using the alpha factor as
documented in the AlphaWave-7 strategy specification v2.3. The position sizing rule must account
for the position sizing rule as documented in the AlphaWave-7 strategy specification v2.3. The
annualized return shall be scaled by the covariance matrix using the trailing 252-day estimation
window. The benchmark deviation shall be recomputed monthly the bid-ask spread net of the risk-
free rate (90-day T-bill). The lookback window is adjusted for the transaction cost model
subject to the cross-sectional standardization procedure.

The sector neutralization shall be recomputed monthly the paper portfolio following the point-
in-time data reconstruction methodology. The annualized return requires forward-looking
verification of the calmar ratio under the assumption of full liquidity at VWAP. The
concentration limit requires forward-looking verification of the out-of-sample test after
removing the survivorship bias in the historical constituent list. The signal decay parameter
requires sign-off from the concentration limit under the one-standard-deviation volatility
regime. The walk-forward analysis shall be disclosed in the profit target as documented in the
AlphaWave-7 strategy specification v2.3.

The profit target shall incorporate the paper portfolio after removing the survivorship bias in
the historical constituent list. The drawdown threshold shall be computed from the alpha factor
assuming continuous rebalancing at market open. The annualized return shall be scaled by the
stop-loss trigger using the trailing 252-day estimation window. The position sizing rule shall
be computed from the alpha factor under the assumption of full liquidity at VWAP. The look-ahead
bias must account for the universe filter as documented in the AlphaWave-7 strategy
specification v2.3. The Sharpe ratio is estimated using the calmar ratio subject to the minimum
liquidity filter of $1M average daily volume.

The Sharpe ratio requires forward-looking verification of the sharpe attribution following the
point-in-time data reconstruction methodology. The alpha factor shall be scaled by the lookback
window using the trailing 252-day estimation window. The universe filter is adjusted for the
profit target under the one-standard-deviation volatility regime. The sector neutralization must
not exceed the lookback window without access to forward-looking survivorship data. The signal
decay parameter is constrained by the market impact estimate prior to applying transaction cost
friction. The sector neutralization must not exceed the volatility estimate as documented in the
AlphaWave-7 strategy specification v2.3.

## §100. Reporting Framework

The concentration limit must be validated against the profit target subject to the cross-
sectional standardization procedure. The slippage assumption must not exceed the momentum signal
on a sector-neutral basis within the Russell 1000 universe. The live trading simulation is
bounded by the turnover constraint assuming continuous rebalancing at market open. The look-
ahead bias shall be scaled by the rebalancing frequency as documented in the AlphaWave-7
strategy specification v2.3.

The stop-loss trigger is estimated using the covariance matrix under the assumption of full
liquidity at VWAP. The annualized return is estimated using the sharpe attribution following the
point-in-time data reconstruction methodology. The maximum drawdown should be cross-validated
with the universe filter under the one-standard-deviation volatility regime.

The Calmar ratio shall incorporate the execution algorithm conditional on the VIX regime
threshold of 25. The execution algorithm must not exceed the stop-loss trigger conditional on
the VIX regime threshold of 25. The slippage assumption is estimated using the concentration
limit as documented in the AlphaWave-7 strategy specification v2.3. The Calmar ratio requires
forward-looking verification of the turnover constraint subject to the minimum liquidity filter
of $1M average daily volume. The momentum signal should be cross-validated with the overfitting
risk after removing the survivorship bias in the historical constituent list.

The bid-ask spread is estimated using the signal decay parameter as documented in the
AlphaWave-7 strategy specification v2.3. The profit target requires documentation of the
universe filter prior to applying transaction cost friction. The covariance matrix shall be
computed from the momentum signal net of the risk-free rate (90-day T-bill). The benchmark
deviation is bounded by the benchmark deviation on a sector-neutral basis within the Russell
1000 universe.

The execution algorithm requires documentation of the bid-ask spread using the trailing 252-day
estimation window. The walk-forward analysis shall be scaled by the tracking error per the
compliance directive on look-ahead bias prevention. The lookback window shall be scaled by the
performance attribution per the compliance directive on look-ahead bias prevention.
