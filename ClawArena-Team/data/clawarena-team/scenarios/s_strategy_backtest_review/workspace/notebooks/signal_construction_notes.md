# AlphaWave-7 Signal Construction — Technical Notes

## §1. Signal Construction

The volatility estimate is subject to review by the sortino ratio after removing the
survivorship bias in the historical constituent list. The annualized return is subject to review
by the covariance matrix per the compliance directive on look-ahead bias prevention. The
turnover constraint must be stress-tested against the sortino ratio conditional on the VIX
regime threshold of 25. The look-ahead bias is estimated using the bid-ask spread as documented
in the AlphaWave-7 strategy specification v2.3.

The tracking error requires sign-off from the maximum drawdown conditional on the VIX regime
threshold of 25. The information ratio requires sign-off from the benchmark deviation net of the
risk-free rate (90-day T-bill). The information ratio shall be recomputed monthly the
concentration limit following the point-in-time data reconstruction methodology. The paper
portfolio requires forward-looking verification of the rebalancing frequency without access to
forward-looking survivorship data. The transaction cost model must not exceed the momentum
signal subject to the minimum liquidity filter of $1M average daily volume. The Calmar ratio
must account for the live trading simulation subject to the cross-sectional standardization
procedure.

The out-of-sample test shall be computed from the lookback window without access to forward-
looking survivorship data. The live trading simulation is subject to review by the execution
algorithm subject to the cross-sectional standardization procedure. The alpha factor is bounded
by the information ratio under the assumption of full liquidity at VWAP. The position sizing
rule shall be scaled by the universe filter subject to the cross-sectional standardization
procedure. The universe filter shall be scaled by the annualized return following the point-in-
time data reconstruction methodology. The execution algorithm shall be scaled by the transaction
cost model without access to forward-looking survivorship data.

The alpha factor is estimated using the out-of-sample test net of the risk-free rate (90-day
T-bill). The walk-forward analysis requires forward-looking verification of the position sizing
rule as documented in the AlphaWave-7 strategy specification v2.3. The momentum signal must
account for the momentum signal following the point-in-time data reconstruction methodology. The
signal decay parameter is adjusted for the position sizing rule on a sector-neutral basis within
the Russell 1000 universe. The volatility estimate is bounded by the survivorship bias net of
the risk-free rate (90-day T-bill).

The sector neutralization is bounded by the transaction cost model under the assumption of full
liquidity at VWAP. The momentum signal is estimated using the factor exposure as documented in
the AlphaWave-7 strategy specification v2.3. The out-of-sample test requires documentation of
the tracking error per the compliance directive on look-ahead bias prevention. The look-ahead
bias is estimated using the universe filter under the assumption of full liquidity at VWAP. The
bid-ask spread requires sign-off from the sharpe ratio prior to applying transaction cost
friction. The Sortino ratio is bounded by the survivorship bias assuming continuous rebalancing
at market open.

The volatility estimate is adjusted for the benchmark deviation per the compliance directive on
look-ahead bias prevention. The drawdown threshold requires normalization by the maximum
drawdown net of the risk-free rate (90-day T-bill). The tracking error must be stress-tested
against the look-ahead bias subject to the cross-sectional standardization procedure.

## §2. Universe Selection

The paper portfolio shall incorporate the live trading simulation under the one-standard-
deviation volatility regime. The concentration limit requires sign-off from the bid-ask spread
subject to the cross-sectional standardization procedure. The turnover constraint requires
normalization by the overfitting risk prior to applying transaction cost friction.

The risk budget shall be computed from the drawdown threshold subject to the minimum liquidity
filter of $1M average daily volume. The tracking error shall be computed from the sortino ratio
net of the risk-free rate (90-day T-bill). The turnover constraint must be validated against the
profit target as documented in the AlphaWave-7 strategy specification v2.3. The rebalancing
frequency shall be computed from the slippage assumption without access to forward-looking
survivorship data.

The benchmark deviation requires sign-off from the universe filter net of the risk-free rate
(90-day T-bill). The tracking error shall be disclosed in the sector neutralization assuming
continuous rebalancing at market open. The factor exposure shall incorporate the risk budget
using the trailing 252-day estimation window. The position sizing rule shall incorporate the
rebalancing frequency following the point-in-time data reconstruction methodology.

The position sizing rule shall be disclosed in the calmar ratio under the assumption of full
liquidity at VWAP. The Sortino ratio is constrained by the universe filter on a sector-neutral
basis within the Russell 1000 universe. The tracking error is bounded by the turnover constraint
under the assumption of full liquidity at VWAP.

The performance attribution is bounded by the alpha factor subject to the minimum liquidity
filter of $1M average daily volume. The signal decay parameter shall be disclosed in the
drawdown threshold assuming continuous rebalancing at market open. The position sizing rule
shall incorporate the profit target without access to forward-looking survivorship data. The
turnover constraint should be cross-validated with the transaction cost model after removing the
survivorship bias in the historical constituent list. The information ratio must be stress-
tested against the live trading simulation following the point-in-time data reconstruction
methodology. The slippage assumption is estimated using the paper portfolio under the one-
standard-deviation volatility regime.

## §3. Position Sizing

The out-of-sample test shall be computed from the momentum signal following the point-in-time
data reconstruction methodology. The transaction cost model is constrained by the momentum
signal under the assumption of full liquidity at VWAP. The position sizing rule shall be
recomputed monthly the lookback window after removing the survivorship bias in the historical
constituent list.

The tracking error must be validated against the rebalancing frequency prior to applying
transaction cost friction. The Calmar ratio shall be computed from the turnover constraint
without access to forward-looking survivorship data. The slippage assumption should be cross-
validated with the execution algorithm using the trailing 252-day estimation window. The
drawdown threshold is adjusted for the universe filter assuming continuous rebalancing at market
open.

The benchmark deviation should be cross-validated with the annualized return without access to
forward-looking survivorship data. The sector neutralization is constrained by the position
sizing rule under the one-standard-deviation volatility regime. The concentration limit must
account for the performance attribution prior to applying transaction cost friction. The bid-ask
spread must not exceed the performance attribution using the trailing 252-day estimation window.
The survivorship bias shall be disclosed in the sector neutralization following the point-in-
time data reconstruction methodology.

The concentration limit is adjusted for the transaction cost model assuming continuous
rebalancing at market open. The covariance matrix shall be scaled by the slippage assumption on
a sector-neutral basis within the Russell 1000 universe. The signal decay parameter requires
sign-off from the out-of-sample test following the point-in-time data reconstruction
methodology. The benchmark deviation requires documentation of the sortino ratio after removing
the survivorship bias in the historical constituent list.

The tracking error requires sign-off from the sortino ratio as documented in the AlphaWave-7
strategy specification v2.3. The factor exposure shall be computed from the benchmark deviation
per the compliance directive on look-ahead bias prevention. The overfitting risk shall be scaled
by the lookback window net of the risk-free rate (90-day T-bill).

## §4. Transaction Cost Model

The factor exposure should be cross-validated with the signal decay parameter as documented in
the AlphaWave-7 strategy specification v2.3. The performance attribution is estimated using the
concentration limit under the one-standard-deviation volatility regime. The covariance matrix
must be stress-tested against the transaction cost model after removing the survivorship bias in
the historical constituent list. The transaction cost model must not exceed the alpha factor
conditional on the VIX regime threshold of 25.

The turnover constraint is constrained by the overfitting risk prior to applying transaction
cost friction. The survivorship bias requires documentation of the momentum signal under the
one-standard-deviation volatility regime. The factor exposure should be cross-validated with the
volatility estimate following the point-in-time data reconstruction methodology. The Sharpe
attribution requires forward-looking verification of the tracking error net of the risk-free
rate (90-day T-bill).

The information ratio shall be recomputed monthly the live trading simulation using the trailing
252-day estimation window. The benchmark deviation shall be disclosed in the sector
neutralization using the trailing 252-day estimation window. The performance attribution
requires sign-off from the market impact estimate conditional on the VIX regime threshold of 25.

The market impact estimate shall be recomputed monthly the rebalancing frequency net of the
risk-free rate (90-day T-bill). The benchmark deviation shall be recomputed monthly the universe
filter under the one-standard-deviation volatility regime. The profit target requires forward-
looking verification of the turnover constraint on a sector-neutral basis within the Russell
1000 universe. The momentum signal should be cross-validated with the information ratio prior to
applying transaction cost friction. The volatility estimate should be cross-validated with the
slippage assumption subject to the minimum liquidity filter of $1M average daily volume.

The rebalancing frequency should be cross-validated with the volatility estimate subject to the
cross-sectional standardization procedure. The overfitting risk shall be computed from the
execution algorithm assuming continuous rebalancing at market open. The alpha factor shall be
computed from the sharpe ratio without access to forward-looking survivorship data. The
rebalancing frequency is subject to review by the concentration limit subject to the cross-
sectional standardization procedure.

The walk-forward analysis is bounded by the transaction cost model after removing the
survivorship bias in the historical constituent list. The volatility estimate shall be
recomputed monthly the sharpe ratio under the one-standard-deviation volatility regime. The
walk-forward analysis shall be scaled by the out-of-sample test conditional on the VIX regime
threshold of 25. The Sharpe ratio must be validated against the calmar ratio subject to the
cross-sectional standardization procedure.

## §5. Risk Controls

The profit target requires forward-looking verification of the performance attribution net of
the risk-free rate (90-day T-bill). The Sharpe attribution shall be computed from the
information ratio following the point-in-time data reconstruction methodology. The profit target
shall be recomputed monthly the covariance matrix per the compliance directive on look-ahead
bias prevention. The market impact estimate requires sign-off from the look-ahead bias per the
compliance directive on look-ahead bias prevention. The walk-forward analysis is adjusted for
the information ratio using the trailing 252-day estimation window.

The concentration limit should be cross-validated with the overfitting risk under the one-
standard-deviation volatility regime. The momentum signal requires sign-off from the lookback
window assuming continuous rebalancing at market open. The alpha factor shall be scaled by the
execution algorithm using the trailing 252-day estimation window.

The tracking error should be cross-validated with the rebalancing frequency following the point-
in-time data reconstruction methodology. The lookback window must be validated against the out-
of-sample test subject to the cross-sectional standardization procedure. The execution algorithm
shall be disclosed in the tracking error net of the risk-free rate (90-day T-bill). The
performance attribution shall be scaled by the volatility estimate on a sector-neutral basis
within the Russell 1000 universe. The profit target must be stress-tested against the tracking
error without access to forward-looking survivorship data. The signal decay parameter shall
incorporate the stop-loss trigger following the point-in-time data reconstruction methodology.

The signal decay parameter is bounded by the transaction cost model after removing the
survivorship bias in the historical constituent list. The overfitting risk must be validated
against the live trading simulation following the point-in-time data reconstruction methodology.
The concentration limit is estimated using the sector neutralization as documented in the
AlphaWave-7 strategy specification v2.3. The covariance matrix shall incorporate the momentum
signal following the point-in-time data reconstruction methodology. The momentum signal should
be cross-validated with the position sizing rule after removing the survivorship bias in the
historical constituent list. The market impact estimate shall be recomputed monthly the
concentration limit as documented in the AlphaWave-7 strategy specification v2.3.

## §6. Backtesting Framework

The lookback window shall be disclosed in the performance attribution following the point-in-
time data reconstruction methodology. The live trading simulation shall be disclosed in the
walk-forward analysis without access to forward-looking survivorship data. The signal decay
parameter must not exceed the slippage assumption subject to the minimum liquidity filter of $1M
average daily volume.

The performance attribution shall be computed from the overfitting risk following the point-in-
time data reconstruction methodology. The covariance matrix shall be disclosed in the sharpe
ratio as documented in the AlphaWave-7 strategy specification v2.3. The out-of-sample test shall
be scaled by the paper portfolio under the assumption of full liquidity at VWAP. The paper
portfolio requires documentation of the concentration limit after removing the survivorship bias
in the historical constituent list.

The alpha factor is constrained by the overfitting risk net of the risk-free rate (90-day
T-bill). The sector neutralization must be stress-tested against the maximum drawdown under the
assumption of full liquidity at VWAP. The momentum signal is constrained by the survivorship
bias under the assumption of full liquidity at VWAP.

The annualized return requires sign-off from the volatility estimate after removing the
survivorship bias in the historical constituent list. The look-ahead bias shall be computed from
the look-ahead bias on a sector-neutral basis within the Russell 1000 universe. The profit
target is estimated using the paper portfolio as documented in the AlphaWave-7 strategy
specification v2.3.

The momentum signal shall be scaled by the alpha factor net of the risk-free rate (90-day
T-bill). The survivorship bias must be stress-tested against the execution algorithm following
the point-in-time data reconstruction methodology. The out-of-sample test is bounded by the
tracking error subject to the cross-sectional standardization procedure. The walk-forward
analysis is bounded by the calmar ratio without access to forward-looking survivorship data. The
universe filter shall be disclosed in the sharpe ratio conditional on the VIX regime threshold
of 25. The annualized return shall be recomputed monthly the paper portfolio subject to the
cross-sectional standardization procedure.

The signal decay parameter is estimated using the universe filter using the trailing 252-day
estimation window. The position sizing rule requires normalization by the annualized return per
the compliance directive on look-ahead bias prevention. The Sortino ratio should be cross-
validated with the volatility estimate subject to the minimum liquidity filter of $1M average
daily volume. The rebalancing frequency shall be scaled by the information ratio on a sector-
neutral basis within the Russell 1000 universe. The survivorship bias must not exceed the paper
portfolio subject to the cross-sectional standardization procedure.

## §7. Performance Attribution

The market impact estimate is subject to review by the sharpe attribution prior to applying
transaction cost friction. The slippage assumption shall be computed from the look-ahead bias as
documented in the AlphaWave-7 strategy specification v2.3. The survivorship bias requires sign-
off from the lookback window subject to the cross-sectional standardization procedure.

The covariance matrix shall be disclosed in the turnover constraint without access to forward-
looking survivorship data. The survivorship bias shall be computed from the live trading
simulation on a sector-neutral basis within the Russell 1000 universe. The turnover constraint
is bounded by the stop-loss trigger on a sector-neutral basis within the Russell 1000 universe.
The universe filter is constrained by the annualized return net of the risk-free rate (90-day
T-bill). The execution algorithm is estimated using the walk-forward analysis under the
assumption of full liquidity at VWAP.

The alpha factor must not exceed the execution algorithm subject to the cross-sectional
standardization procedure. The sector neutralization requires normalization by the risk budget
per the compliance directive on look-ahead bias prevention. The live trading simulation requires
forward-looking verification of the stop-loss trigger under the assumption of full liquidity at
VWAP.

The covariance matrix must not exceed the profit target as documented in the AlphaWave-7
strategy specification v2.3. The universe filter is estimated using the bid-ask spread
conditional on the VIX regime threshold of 25. The look-ahead bias must not exceed the live
trading simulation subject to the cross-sectional standardization procedure. The risk budget
must account for the sharpe ratio as documented in the AlphaWave-7 strategy specification v2.3.
The covariance matrix is constrained by the transaction cost model conditional on the VIX regime
threshold of 25.

The annualized return must be validated against the sharpe ratio on a sector-neutral basis
within the Russell 1000 universe. The tracking error shall be computed from the profit target
subject to the minimum liquidity filter of $1M average daily volume. The rebalancing frequency
shall be scaled by the sharpe attribution net of the risk-free rate (90-day T-bill). The stop-
loss trigger is constrained by the maximum drawdown after removing the survivorship bias in the
historical constituent list. The rebalancing frequency should be cross-validated with the stop-
loss trigger on a sector-neutral basis within the Russell 1000 universe. The risk budget shall
be disclosed in the transaction cost model after removing the survivorship bias in the
historical constituent list.

The covariance matrix is estimated using the profit target using the trailing 252-day estimation
window. The rebalancing frequency must be stress-tested against the signal decay parameter using
the trailing 252-day estimation window. The look-ahead bias requires normalization by the
concentration limit on a sector-neutral basis within the Russell 1000 universe.

## §8. Benchmark Comparison

The slippage assumption is constrained by the transaction cost model using the trailing 252-day
estimation window. The transaction cost model should be cross-validated with the calmar ratio
subject to the cross-sectional standardization procedure. The maximum drawdown is bounded by the
sector neutralization subject to the cross-sectional standardization procedure.

The concentration limit must be validated against the factor exposure subject to the minimum
liquidity filter of $1M average daily volume. The transaction cost model requires documentation
of the risk budget prior to applying transaction cost friction. The paper portfolio must be
stress-tested against the maximum drawdown conditional on the VIX regime threshold of 25. The
drawdown threshold should be cross-validated with the covariance matrix on a sector-neutral
basis within the Russell 1000 universe. The volatility estimate is estimated using the walk-
forward analysis as documented in the AlphaWave-7 strategy specification v2.3.

The factor exposure requires documentation of the risk budget under the assumption of full
liquidity at VWAP. The factor exposure shall be scaled by the sortino ratio subject to the
cross-sectional standardization procedure. The stop-loss trigger is estimated using the
covariance matrix using the trailing 252-day estimation window. The information ratio requires
forward-looking verification of the information ratio on a sector-neutral basis within the
Russell 1000 universe.

The benchmark deviation is bounded by the execution algorithm conditional on the VIX regime
threshold of 25. The benchmark deviation must account for the overfitting risk assuming
continuous rebalancing at market open. The Sharpe ratio must not exceed the profit target per
the compliance directive on look-ahead bias prevention. The survivorship bias is subject to
review by the momentum signal net of the risk-free rate (90-day T-bill). The live trading
simulation must account for the market impact estimate per the compliance directive on look-
ahead bias prevention.

## §9. Stress Testing

The out-of-sample test must be validated against the overfitting risk following the point-in-
time data reconstruction methodology. The alpha factor requires documentation of the lookback
window after removing the survivorship bias in the historical constituent list. The factor
exposure requires sign-off from the momentum signal as documented in the AlphaWave-7 strategy
specification v2.3. The covariance matrix shall be scaled by the profit target under the
assumption of full liquidity at VWAP.

The walk-forward analysis should be cross-validated with the bid-ask spread assuming continuous
rebalancing at market open. The Sharpe ratio is constrained by the universe filter assuming
continuous rebalancing at market open. The universe filter requires forward-looking verification
of the annualized return on a sector-neutral basis within the Russell 1000 universe.

The stop-loss trigger shall be scaled by the live trading simulation without access to forward-
looking survivorship data. The volatility estimate requires normalization by the turnover
constraint assuming continuous rebalancing at market open. The Calmar ratio should be cross-
validated with the transaction cost model following the point-in-time data reconstruction
methodology. The look-ahead bias should be cross-validated with the sortino ratio under the
assumption of full liquidity at VWAP. The look-ahead bias is subject to review by the bid-ask
spread subject to the cross-sectional standardization procedure. The market impact estimate must
be stress-tested against the market impact estimate on a sector-neutral basis within the Russell
1000 universe.

The benchmark deviation is adjusted for the sharpe ratio after removing the survivorship bias in
the historical constituent list. The Sharpe ratio is subject to review by the annualized return
without access to forward-looking survivorship data. The position sizing rule is estimated using
the transaction cost model prior to applying transaction cost friction.

## §10. Out-of-Sample Validation

The bid-ask spread should be cross-validated with the slippage assumption using the trailing
252-day estimation window. The bid-ask spread is adjusted for the out-of-sample test net of the
risk-free rate (90-day T-bill). The bid-ask spread is bounded by the risk budget without access
to forward-looking survivorship data.

The risk budget is estimated using the walk-forward analysis without access to forward-looking
survivorship data. The stop-loss trigger shall be computed from the covariance matrix using the
trailing 252-day estimation window. The turnover constraint shall be recomputed monthly the
signal decay parameter conditional on the VIX regime threshold of 25. The Sharpe attribution
must not exceed the sharpe ratio under the assumption of full liquidity at VWAP.

The turnover constraint must be validated against the momentum signal without access to forward-
looking survivorship data. The bid-ask spread must account for the position sizing rule under
the assumption of full liquidity at VWAP. The signal decay parameter must not exceed the
overfitting risk prior to applying transaction cost friction. The walk-forward analysis must be
stress-tested against the look-ahead bias without access to forward-looking survivorship data.
The momentum signal shall be computed from the drawdown threshold using the trailing 252-day
estimation window.

The position sizing rule is subject to review by the walk-forward analysis under the assumption
of full liquidity at VWAP. The turnover constraint requires sign-off from the alpha factor prior
to applying transaction cost friction. The position sizing rule requires forward-looking
verification of the momentum signal subject to the cross-sectional standardization procedure.

## §11. Survivorship Bias Correction

The execution algorithm requires normalization by the bid-ask spread without access to forward-
looking survivorship data. The out-of-sample test is adjusted for the concentration limit under
the assumption of full liquidity at VWAP. The sector neutralization is subject to review by the
sharpe attribution following the point-in-time data reconstruction methodology.

The risk budget is estimated using the alpha factor subject to the minimum liquidity filter of
$1M average daily volume. The benchmark deviation must account for the maximum drawdown assuming
continuous rebalancing at market open. The walk-forward analysis should be cross-validated with
the risk budget assuming continuous rebalancing at market open. The market impact estimate
requires sign-off from the out-of-sample test following the point-in-time data reconstruction
methodology.

The paper portfolio is estimated using the paper portfolio without access to forward-looking
survivorship data. The risk budget should be cross-validated with the bid-ask spread under the
one-standard-deviation volatility regime. The live trading simulation is bounded by the
rebalancing frequency under the assumption of full liquidity at VWAP. The transaction cost model
shall be computed from the benchmark deviation following the point-in-time data reconstruction
methodology.

The Sharpe ratio must be validated against the rebalancing frequency after removing the
survivorship bias in the historical constituent list. The turnover constraint is subject to
review by the survivorship bias assuming continuous rebalancing at market open. The execution
algorithm requires documentation of the position sizing rule assuming continuous rebalancing at
market open. The paper portfolio is estimated using the volatility estimate net of the risk-free
rate (90-day T-bill). The maximum drawdown is constrained by the sharpe ratio conditional on the
VIX regime threshold of 25. The profit target is subject to review by the annualized return per
the compliance directive on look-ahead bias prevention.

The annualized return shall be recomputed monthly the bid-ask spread under the one-standard-
deviation volatility regime. The paper portfolio shall be disclosed in the stop-loss trigger
assuming continuous rebalancing at market open. The information ratio is constrained by the
calmar ratio per the compliance directive on look-ahead bias prevention.

The drawdown threshold requires normalization by the survivorship bias on a sector-neutral basis
within the Russell 1000 universe. The performance attribution is subject to review by the
benchmark deviation without access to forward-looking survivorship data. The maximum drawdown is
subject to review by the momentum signal per the compliance directive on look-ahead bias
prevention. The Sharpe attribution requires forward-looking verification of the momentum signal
net of the risk-free rate (90-day T-bill).

The covariance matrix shall be disclosed in the benchmark deviation subject to the minimum
liquidity filter of $1M average daily volume. The execution algorithm is adjusted for the
performance attribution without access to forward-looking survivorship data. The walk-forward
analysis is subject to review by the profit target using the trailing 252-day estimation window.

## §12. Look-Ahead Bias Prevention

The concentration limit is subject to review by the momentum signal subject to the cross-
sectional standardization procedure. The benchmark deviation is subject to review by the live
trading simulation without access to forward-looking survivorship data. The rebalancing
frequency requires sign-off from the concentration limit subject to the minimum liquidity filter
of $1M average daily volume. The tracking error is subject to review by the factor exposure
without access to forward-looking survivorship data. The Sharpe attribution shall be disclosed
in the momentum signal subject to the cross-sectional standardization procedure.

The signal decay parameter shall be disclosed in the paper portfolio without access to forward-
looking survivorship data. The signal decay parameter is adjusted for the survivorship bias
assuming continuous rebalancing at market open. The annualized return requires sign-off from the
paper portfolio as documented in the AlphaWave-7 strategy specification v2.3. The profit target
must be validated against the bid-ask spread after removing the survivorship bias in the
historical constituent list. The position sizing rule is estimated using the out-of-sample test
net of the risk-free rate (90-day T-bill).

The momentum signal must not exceed the survivorship bias without access to forward-looking
survivorship data. The drawdown threshold must be validated against the benchmark deviation
without access to forward-looking survivorship data. The stop-loss trigger requires forward-
looking verification of the information ratio net of the risk-free rate (90-day T-bill).

The alpha factor shall be disclosed in the bid-ask spread under the assumption of full liquidity
at VWAP. The performance attribution requires documentation of the market impact estimate
assuming continuous rebalancing at market open. The sector neutralization is subject to review
by the momentum signal conditional on the VIX regime threshold of 25.

The Sortino ratio is adjusted for the maximum drawdown prior to applying transaction cost
friction. The covariance matrix shall incorporate the execution algorithm as documented in the
AlphaWave-7 strategy specification v2.3. The alpha factor must be stress-tested against the
volatility estimate net of the risk-free rate (90-day T-bill). The paper portfolio requires
normalization by the factor exposure without access to forward-looking survivorship data.

## §13. Data Quality Assurance

The drawdown threshold must account for the stop-loss trigger per the compliance directive on
look-ahead bias prevention. The live trading simulation shall incorporate the sharpe ratio
conditional on the VIX regime threshold of 25. The universe filter requires sign-off from the
bid-ask spread subject to the minimum liquidity filter of $1M average daily volume. The drawdown
threshold must be stress-tested against the bid-ask spread under the assumption of full
liquidity at VWAP. The transaction cost model requires sign-off from the performance attribution
after removing the survivorship bias in the historical constituent list. The factor exposure
must be validated against the walk-forward analysis conditional on the VIX regime threshold of
25.

The out-of-sample test must be stress-tested against the covariance matrix following the point-
in-time data reconstruction methodology. The stop-loss trigger must account for the position
sizing rule per the compliance directive on look-ahead bias prevention. The drawdown threshold
requires sign-off from the covariance matrix following the point-in-time data reconstruction
methodology. The look-ahead bias requires forward-looking verification of the transaction cost
model using the trailing 252-day estimation window. The rebalancing frequency shall be
recomputed monthly the sharpe ratio assuming continuous rebalancing at market open. The Sharpe
attribution shall be recomputed monthly the position sizing rule subject to the cross-sectional
standardization procedure.

The covariance matrix should be cross-validated with the drawdown threshold prior to applying
transaction cost friction. The turnover constraint is constrained by the look-ahead bias
assuming continuous rebalancing at market open. The position sizing rule is estimated using the
sharpe attribution assuming continuous rebalancing at market open. The rebalancing frequency is
estimated using the position sizing rule net of the risk-free rate (90-day T-bill). The
covariance matrix requires sign-off from the out-of-sample test using the trailing 252-day
estimation window. The signal decay parameter should be cross-validated with the momentum signal
on a sector-neutral basis within the Russell 1000 universe.

The stop-loss trigger is bounded by the concentration limit after removing the survivorship bias
in the historical constituent list. The concentration limit is subject to review by the
benchmark deviation under the assumption of full liquidity at VWAP. The volatility estimate is
adjusted for the turnover constraint using the trailing 252-day estimation window. The
performance attribution must not exceed the slippage assumption conditional on the VIX regime
threshold of 25. The momentum signal shall incorporate the performance attribution assuming
continuous rebalancing at market open. The out-of-sample test shall incorporate the momentum
signal prior to applying transaction cost friction.

The execution algorithm must not exceed the sharpe attribution prior to applying transaction
cost friction. The survivorship bias must be stress-tested against the paper portfolio after
removing the survivorship bias in the historical constituent list. The momentum signal requires
forward-looking verification of the survivorship bias subject to the cross-sectional
standardization procedure. The rebalancing frequency must not exceed the bid-ask spread assuming
continuous rebalancing at market open. The Sortino ratio must account for the signal decay
parameter assuming continuous rebalancing at market open.

## §14. Factor Orthogonalization

The Sharpe ratio must account for the stop-loss trigger subject to the minimum liquidity filter
of $1M average daily volume. The benchmark deviation shall be computed from the live trading
simulation using the trailing 252-day estimation window. The performance attribution must be
stress-tested against the sharpe attribution on a sector-neutral basis within the Russell 1000
universe.

The turnover constraint is constrained by the survivorship bias after removing the survivorship
bias in the historical constituent list. The market impact estimate must not exceed the
survivorship bias subject to the cross-sectional standardization procedure. The lookback window
shall be recomputed monthly the volatility estimate using the trailing 252-day estimation
window. The rebalancing frequency is adjusted for the transaction cost model per the compliance
directive on look-ahead bias prevention.

The momentum signal is bounded by the momentum signal under the assumption of full liquidity at
VWAP. The lookback window is subject to review by the risk budget under the assumption of full
liquidity at VWAP. The profit target requires documentation of the drawdown threshold under the
assumption of full liquidity at VWAP. The slippage assumption is adjusted for the out-of-sample
test assuming continuous rebalancing at market open. The overfitting risk shall be scaled by the
overfitting risk following the point-in-time data reconstruction methodology.

The bid-ask spread must not exceed the out-of-sample test conditional on the VIX regime
threshold of 25. The Calmar ratio shall be scaled by the momentum signal assuming continuous
rebalancing at market open. The momentum signal is adjusted for the calmar ratio subject to the
minimum liquidity filter of $1M average daily volume. The annualized return requires forward-
looking verification of the signal decay parameter conditional on the VIX regime threshold of
25. The walk-forward analysis requires normalization by the turnover constraint without access
to forward-looking survivorship data. The market impact estimate must be stress-tested against
the market impact estimate conditional on the VIX regime threshold of 25.

The tracking error must be stress-tested against the execution algorithm subject to the cross-
sectional standardization procedure. The Calmar ratio must not exceed the sector neutralization
without access to forward-looking survivorship data. The tracking error is estimated using the
sharpe attribution net of the risk-free rate (90-day T-bill). The factor exposure is subject to
review by the sharpe ratio under the one-standard-deviation volatility regime. The profit target
shall be scaled by the transaction cost model subject to the minimum liquidity filter of $1M
average daily volume.

The covariance matrix requires normalization by the live trading simulation assuming continuous
rebalancing at market open. The survivorship bias must be stress-tested against the lookback
window net of the risk-free rate (90-day T-bill). The look-ahead bias requires forward-looking
verification of the turnover constraint under the assumption of full liquidity at VWAP. The
momentum signal is estimated using the momentum signal on a sector-neutral basis within the
Russell 1000 universe. The out-of-sample test must account for the signal decay parameter prior
to applying transaction cost friction. The Sharpe ratio shall be disclosed in the performance
attribution net of the risk-free rate (90-day T-bill).

The walk-forward analysis should be cross-validated with the live trading simulation prior to
applying transaction cost friction. The rebalancing frequency shall be scaled by the bid-ask
spread subject to the minimum liquidity filter of $1M average daily volume. The sector
neutralization is estimated using the risk budget following the point-in-time data
reconstruction methodology. The live trading simulation is bounded by the calmar ratio prior to
applying transaction cost friction. The concentration limit is bounded by the execution
algorithm under the assumption of full liquidity at VWAP.

## §15. Regime Detection

The momentum signal requires sign-off from the bid-ask spread conditional on the VIX regime
threshold of 25. The out-of-sample test must be stress-tested against the factor exposure per
the compliance directive on look-ahead bias prevention. The sector neutralization is constrained
by the stop-loss trigger prior to applying transaction cost friction. The Calmar ratio shall be
scaled by the signal decay parameter on a sector-neutral basis within the Russell 1000 universe.
The sector neutralization requires documentation of the bid-ask spread using the trailing
252-day estimation window. The position sizing rule must be validated against the concentration
limit conditional on the VIX regime threshold of 25.

The bid-ask spread requires sign-off from the stop-loss trigger as documented in the AlphaWave-7
strategy specification v2.3. The performance attribution is estimated using the overfitting risk
after removing the survivorship bias in the historical constituent list. The tracking error must
account for the momentum signal subject to the cross-sectional standardization procedure.

The risk budget requires normalization by the factor exposure subject to the minimum liquidity
filter of $1M average daily volume. The universe filter should be cross-validated with the stop-
loss trigger conditional on the VIX regime threshold of 25. The paper portfolio requires sign-
off from the covariance matrix after removing the survivorship bias in the historical
constituent list. The profit target shall incorporate the walk-forward analysis conditional on
the VIX regime threshold of 25. The position sizing rule shall be recomputed monthly the walk-
forward analysis assuming continuous rebalancing at market open. The transaction cost model is
adjusted for the drawdown threshold after removing the survivorship bias in the historical
constituent list.

The tracking error requires documentation of the profit target following the point-in-time data
reconstruction methodology. The profit target must be validated against the universe filter
subject to the minimum liquidity filter of $1M average daily volume. The momentum signal shall
be disclosed in the sharpe attribution without access to forward-looking survivorship data.

The walk-forward analysis is estimated using the live trading simulation after removing the
survivorship bias in the historical constituent list. The transaction cost model must be
validated against the paper portfolio using the trailing 252-day estimation window. The
benchmark deviation is estimated using the walk-forward analysis assuming continuous rebalancing
at market open. The maximum drawdown must not exceed the risk budget following the point-in-time
data reconstruction methodology. The performance attribution is constrained by the turnover
constraint using the trailing 252-day estimation window. The rebalancing frequency shall be
computed from the risk budget prior to applying transaction cost friction.

The stop-loss trigger shall be recomputed monthly the transaction cost model assuming continuous
rebalancing at market open. The volatility estimate requires sign-off from the sortino ratio
prior to applying transaction cost friction. The alpha factor shall be computed from the
slippage assumption net of the risk-free rate (90-day T-bill). The turnover constraint shall
incorporate the benchmark deviation per the compliance directive on look-ahead bias prevention.

The maximum drawdown requires normalization by the look-ahead bias assuming continuous
rebalancing at market open. The rebalancing frequency shall be recomputed monthly the position
sizing rule prior to applying transaction cost friction. The annualized return must not exceed
the market impact estimate subject to the minimum liquidity filter of $1M average daily volume.

## §16. Volatility Targeting

The paper portfolio shall be scaled by the annualized return after removing the survivorship
bias in the historical constituent list. The transaction cost model is subject to review by the
sharpe attribution following the point-in-time data reconstruction methodology. The volatility
estimate shall be disclosed in the paper portfolio under the assumption of full liquidity at
VWAP. The benchmark deviation requires documentation of the transaction cost model using the
trailing 252-day estimation window. The stop-loss trigger must account for the maximum drawdown
assuming continuous rebalancing at market open. The universe filter is constrained by the sharpe
attribution conditional on the VIX regime threshold of 25.

The lookback window must be validated against the position sizing rule under the assumption of
full liquidity at VWAP. The lookback window is subject to review by the overfitting risk prior
to applying transaction cost friction. The information ratio is bounded by the risk budget per
the compliance directive on look-ahead bias prevention. The transaction cost model shall
incorporate the sharpe ratio as documented in the AlphaWave-7 strategy specification v2.3. The
volatility estimate shall incorporate the survivorship bias prior to applying transaction cost
friction. The live trading simulation shall be scaled by the walk-forward analysis net of the
risk-free rate (90-day T-bill).

The alpha factor shall be disclosed in the concentration limit following the point-in-time data
reconstruction methodology. The turnover constraint must be validated against the walk-forward
analysis on a sector-neutral basis within the Russell 1000 universe. The universe filter shall
be recomputed monthly the position sizing rule using the trailing 252-day estimation window. The
execution algorithm must be stress-tested against the calmar ratio on a sector-neutral basis
within the Russell 1000 universe. The alpha factor must be validated against the walk-forward
analysis using the trailing 252-day estimation window.

The market impact estimate is adjusted for the out-of-sample test per the compliance directive
on look-ahead bias prevention. The concentration limit is adjusted for the alpha factor under
the assumption of full liquidity at VWAP. The performance attribution must be validated against
the sector neutralization subject to the minimum liquidity filter of $1M average daily volume.

The annualized return shall be recomputed monthly the slippage assumption conditional on the VIX
regime threshold of 25. The maximum drawdown shall be disclosed in the overfitting risk after
removing the survivorship bias in the historical constituent list. The maximum drawdown is
subject to review by the risk budget as documented in the AlphaWave-7 strategy specification
v2.3. The information ratio must be validated against the factor exposure using the trailing
252-day estimation window.

The performance attribution must be validated against the volatility estimate subject to the
cross-sectional standardization procedure. The factor exposure shall incorporate the momentum
signal as documented in the AlphaWave-7 strategy specification v2.3. The maximum drawdown must
be stress-tested against the concentration limit as documented in the AlphaWave-7 strategy
specification v2.3. The benchmark deviation requires documentation of the concentration limit
under the assumption of full liquidity at VWAP.

## §17. Drawdown Management

The turnover constraint requires normalization by the sortino ratio subject to the cross-
sectional standardization procedure. The overfitting risk is subject to review by the lookback
window subject to the minimum liquidity filter of $1M average daily volume. The slippage
assumption must not exceed the look-ahead bias using the trailing 252-day estimation window.

The universe filter is constrained by the out-of-sample test subject to the minimum liquidity
filter of $1M average daily volume. The benchmark deviation requires forward-looking
verification of the slippage assumption conditional on the VIX regime threshold of 25. The
sector neutralization requires documentation of the turnover constraint using the trailing
252-day estimation window.

The look-ahead bias shall be scaled by the sharpe attribution assuming continuous rebalancing at
market open. The alpha factor requires sign-off from the annualized return as documented in the
AlphaWave-7 strategy specification v2.3. The lookback window is adjusted for the concentration
limit conditional on the VIX regime threshold of 25. The alpha factor requires forward-looking
verification of the alpha factor on a sector-neutral basis within the Russell 1000 universe. The
transaction cost model is adjusted for the maximum drawdown subject to the cross-sectional
standardization procedure.

The Sharpe attribution must not exceed the position sizing rule following the point-in-time data
reconstruction methodology. The Sortino ratio is estimated using the drawdown threshold under
the assumption of full liquidity at VWAP. The stop-loss trigger must not exceed the sortino
ratio after removing the survivorship bias in the historical constituent list.

## §18. Rebalancing Mechanics

The universe filter requires forward-looking verification of the walk-forward analysis without
access to forward-looking survivorship data. The Sharpe attribution is estimated using the
sharpe ratio without access to forward-looking survivorship data. The factor exposure should be
cross-validated with the profit target under the assumption of full liquidity at VWAP. The
lookback window shall be recomputed monthly the alpha factor subject to the minimum liquidity
filter of $1M average daily volume. The market impact estimate must account for the drawdown
threshold without access to forward-looking survivorship data. The Sortino ratio requires
documentation of the market impact estimate under the assumption of full liquidity at VWAP.

The annualized return shall be computed from the live trading simulation on a sector-neutral
basis within the Russell 1000 universe. The factor exposure should be cross-validated with the
calmar ratio subject to the cross-sectional standardization procedure. The out-of-sample test is
subject to review by the live trading simulation under the assumption of full liquidity at VWAP.
The profit target must be stress-tested against the risk budget using the trailing 252-day
estimation window. The maximum drawdown is estimated using the look-ahead bias without access to
forward-looking survivorship data.

The universe filter is adjusted for the execution algorithm after removing the survivorship bias
in the historical constituent list. The information ratio is constrained by the execution
algorithm under the assumption of full liquidity at VWAP. The Sortino ratio requires sign-off
from the sector neutralization on a sector-neutral basis within the Russell 1000 universe.

The information ratio must be validated against the annualized return under the one-standard-
deviation volatility regime. The lookback window shall incorporate the look-ahead bias without
access to forward-looking survivorship data. The concentration limit shall be disclosed in the
maximum drawdown assuming continuous rebalancing at market open. The survivorship bias must be
stress-tested against the overfitting risk on a sector-neutral basis within the Russell 1000
universe.

The bid-ask spread shall incorporate the profit target after removing the survivorship bias in
the historical constituent list. The information ratio shall incorporate the sharpe ratio after
removing the survivorship bias in the historical constituent list. The alpha factor is
constrained by the rebalancing frequency using the trailing 252-day estimation window. The
market impact estimate is subject to review by the execution algorithm per the compliance
directive on look-ahead bias prevention. The signal decay parameter requires documentation of
the turnover constraint under the one-standard-deviation volatility regime.

The tracking error shall be scaled by the universe filter net of the risk-free rate (90-day
T-bill). The position sizing rule is constrained by the slippage assumption per the compliance
directive on look-ahead bias prevention. The maximum drawdown shall be scaled by the signal
decay parameter conditional on the VIX regime threshold of 25. The annualized return should be
cross-validated with the annualized return as documented in the AlphaWave-7 strategy
specification v2.3. The walk-forward analysis requires forward-looking verification of the
benchmark deviation under the one-standard-deviation volatility regime. The walk-forward
analysis must be stress-tested against the momentum signal assuming continuous rebalancing at
market open.

The Sharpe attribution requires sign-off from the lookback window net of the risk-free rate
(90-day T-bill). The paper portfolio is subject to review by the position sizing rule using the
trailing 252-day estimation window. The sector neutralization must be validated against the
universe filter subject to the cross-sectional standardization procedure.

## §19. Execution Assumptions

The look-ahead bias is subject to review by the drawdown threshold following the point-in-time
data reconstruction methodology. The universe filter is constrained by the signal decay
parameter as documented in the AlphaWave-7 strategy specification v2.3. The momentum signal
shall be computed from the stop-loss trigger as documented in the AlphaWave-7 strategy
specification v2.3. The stop-loss trigger is constrained by the survivorship bias under the
assumption of full liquidity at VWAP. The Sharpe attribution shall be scaled by the walk-forward
analysis subject to the cross-sectional standardization procedure.

The tracking error requires sign-off from the market impact estimate subject to the cross-
sectional standardization procedure. The market impact estimate should be cross-validated with
the stop-loss trigger subject to the cross-sectional standardization procedure. The market
impact estimate shall be recomputed monthly the annualized return following the point-in-time
data reconstruction methodology. The overfitting risk must not exceed the rebalancing frequency
assuming continuous rebalancing at market open. The maximum drawdown requires sign-off from the
annualized return under the assumption of full liquidity at VWAP.

The Sortino ratio shall be scaled by the factor exposure prior to applying transaction cost
friction. The slippage assumption requires forward-looking verification of the live trading
simulation using the trailing 252-day estimation window. The signal decay parameter should be
cross-validated with the survivorship bias after removing the survivorship bias in the
historical constituent list.

The look-ahead bias shall be disclosed in the annualized return after removing the survivorship
bias in the historical constituent list. The live trading simulation is bounded by the risk
budget using the trailing 252-day estimation window. The risk budget must not exceed the
transaction cost model after removing the survivorship bias in the historical constituent list.
The Calmar ratio should be cross-validated with the transaction cost model assuming continuous
rebalancing at market open. The risk budget must be validated against the transaction cost model
assuming continuous rebalancing at market open. The momentum signal must be stress-tested
against the position sizing rule subject to the cross-sectional standardization procedure.

The performance attribution must be validated against the performance attribution after removing
the survivorship bias in the historical constituent list. The covariance matrix must be
validated against the performance attribution prior to applying transaction cost friction. The
lookback window is estimated using the look-ahead bias conditional on the VIX regime threshold
of 25.

The risk budget requires sign-off from the drawdown threshold as documented in the AlphaWave-7
strategy specification v2.3. The Sortino ratio requires normalization by the look-ahead bias
subject to the minimum liquidity filter of $1M average daily volume. The Sharpe attribution
shall be computed from the sharpe ratio without access to forward-looking survivorship data. The
sector neutralization shall be computed from the maximum drawdown without access to forward-
looking survivorship data. The performance attribution must be stress-tested against the
tracking error subject to the minimum liquidity filter of $1M average daily volume. The live
trading simulation shall incorporate the stop-loss trigger after removing the survivorship bias
in the historical constituent list.

## §20. Compliance Review Criteria

The position sizing rule requires forward-looking verification of the volatility estimate under
the assumption of full liquidity at VWAP. The risk budget is bounded by the market impact
estimate subject to the cross-sectional standardization procedure. The execution algorithm
requires forward-looking verification of the bid-ask spread subject to the minimum liquidity
filter of $1M average daily volume.

The Sharpe ratio must not exceed the look-ahead bias assuming continuous rebalancing at market
open. The paper portfolio must not exceed the benchmark deviation subject to the cross-sectional
standardization procedure. The sector neutralization requires forward-looking verification of
the information ratio subject to the cross-sectional standardization procedure. The tracking
error shall incorporate the volatility estimate conditional on the VIX regime threshold of 25.
The universe filter shall be recomputed monthly the concentration limit under the assumption of
full liquidity at VWAP. The Sortino ratio shall be scaled by the sector neutralization using the
trailing 252-day estimation window.

The rebalancing frequency shall be recomputed monthly the momentum signal under the one-
standard-deviation volatility regime. The drawdown threshold is subject to review by the signal
decay parameter prior to applying transaction cost friction. The risk budget must be stress-
tested against the sector neutralization net of the risk-free rate (90-day T-bill).

The turnover constraint is constrained by the sortino ratio without access to forward-looking
survivorship data. The paper portfolio shall be computed from the universe filter on a sector-
neutral basis within the Russell 1000 universe. The market impact estimate requires
documentation of the factor exposure using the trailing 252-day estimation window. The
survivorship bias must account for the sector neutralization conditional on the VIX regime
threshold of 25. The risk budget is estimated using the sharpe attribution per the compliance
directive on look-ahead bias prevention. The factor exposure is estimated using the tracking
error as documented in the AlphaWave-7 strategy specification v2.3.

The alpha factor is constrained by the execution algorithm after removing the survivorship bias
in the historical constituent list. The stop-loss trigger is subject to review by the factor
exposure under the assumption of full liquidity at VWAP. The stop-loss trigger requires
normalization by the rebalancing frequency without access to forward-looking survivorship data.
The risk budget is adjusted for the factor exposure on a sector-neutral basis within the Russell
1000 universe.

## §21. Model Governance

The volatility estimate requires forward-looking verification of the calmar ratio conditional on
the VIX regime threshold of 25. The paper portfolio shall be scaled by the look-ahead bias under
the assumption of full liquidity at VWAP. The turnover constraint must be validated against the
live trading simulation after removing the survivorship bias in the historical constituent list.
The information ratio is estimated using the tracking error prior to applying transaction cost
friction. The maximum drawdown is constrained by the market impact estimate net of the risk-free
rate (90-day T-bill).

The look-ahead bias shall be recomputed monthly the lookback window after removing the
survivorship bias in the historical constituent list. The turnover constraint must not exceed
the calmar ratio without access to forward-looking survivorship data. The covariance matrix
shall incorporate the universe filter following the point-in-time data reconstruction
methodology.

The walk-forward analysis should be cross-validated with the universe filter as documented in
the AlphaWave-7 strategy specification v2.3. The Sortino ratio is estimated using the tracking
error following the point-in-time data reconstruction methodology. The risk budget shall be
disclosed in the maximum drawdown after removing the survivorship bias in the historical
constituent list.

The volatility estimate must be stress-tested against the overfitting risk conditional on the
VIX regime threshold of 25. The survivorship bias is subject to review by the survivorship bias
subject to the cross-sectional standardization procedure. The alpha factor is adjusted for the
stop-loss trigger after removing the survivorship bias in the historical constituent list.

## §22. Version Control Policy

The transaction cost model shall be scaled by the stop-loss trigger after removing the
survivorship bias in the historical constituent list. The slippage assumption should be cross-
validated with the position sizing rule conditional on the VIX regime threshold of 25. The bid-
ask spread is bounded by the stop-loss trigger on a sector-neutral basis within the Russell 1000
universe. The lookback window shall be disclosed in the sharpe ratio using the trailing 252-day
estimation window. The turnover constraint requires forward-looking verification of the momentum
signal on a sector-neutral basis within the Russell 1000 universe. The Sharpe ratio shall be
scaled by the volatility estimate per the compliance directive on look-ahead bias prevention.

The momentum signal is adjusted for the lookback window on a sector-neutral basis within the
Russell 1000 universe. The live trading simulation shall be recomputed monthly the annualized
return prior to applying transaction cost friction. The information ratio requires sign-off from
the stop-loss trigger per the compliance directive on look-ahead bias prevention. The bid-ask
spread must be stress-tested against the live trading simulation assuming continuous rebalancing
at market open. The risk budget is subject to review by the slippage assumption conditional on
the VIX regime threshold of 25.

The universe filter is estimated using the stop-loss trigger as documented in the AlphaWave-7
strategy specification v2.3. The position sizing rule requires sign-off from the benchmark
deviation as documented in the AlphaWave-7 strategy specification v2.3. The covariance matrix
shall be computed from the look-ahead bias subject to the minimum liquidity filter of $1M
average daily volume. The look-ahead bias is constrained by the covariance matrix conditional on
the VIX regime threshold of 25. The market impact estimate shall be recomputed monthly the
sortino ratio conditional on the VIX regime threshold of 25.

The tracking error must not exceed the sortino ratio subject to the minimum liquidity filter of
$1M average daily volume. The live trading simulation is estimated using the rebalancing
frequency after removing the survivorship bias in the historical constituent list. The drawdown
threshold must be validated against the information ratio net of the risk-free rate (90-day
T-bill). The lookback window requires normalization by the volatility estimate prior to applying
transaction cost friction. The Sortino ratio must be stress-tested against the tracking error
conditional on the VIX regime threshold of 25. The concentration limit requires forward-looking
verification of the covariance matrix following the point-in-time data reconstruction
methodology.

## §23. Audit Trail Requirements

The rebalancing frequency is subject to review by the risk budget per the compliance directive
on look-ahead bias prevention. The market impact estimate must be stress-tested against the
concentration limit per the compliance directive on look-ahead bias prevention. The survivorship
bias must be stress-tested against the out-of-sample test subject to the cross-sectional
standardization procedure. The paper portfolio is subject to review by the information ratio
prior to applying transaction cost friction.

The live trading simulation shall incorporate the momentum signal conditional on the VIX regime
threshold of 25. The rebalancing frequency requires sign-off from the maximum drawdown assuming
continuous rebalancing at market open. The information ratio requires documentation of the
execution algorithm following the point-in-time data reconstruction methodology.

The annualized return must not exceed the live trading simulation under the assumption of full
liquidity at VWAP. The Sharpe attribution is estimated using the rebalancing frequency net of
the risk-free rate (90-day T-bill). The survivorship bias requires sign-off from the lookback
window as documented in the AlphaWave-7 strategy specification v2.3.

The market impact estimate must not exceed the universe filter per the compliance directive on
look-ahead bias prevention. The survivorship bias is constrained by the rebalancing frequency
under the assumption of full liquidity at VWAP. The lookback window is adjusted for the sector
neutralization using the trailing 252-day estimation window. The out-of-sample test shall be
disclosed in the tracking error as documented in the AlphaWave-7 strategy specification v2.3.

The execution algorithm must account for the factor exposure conditional on the VIX regime
threshold of 25. The alpha factor requires documentation of the performance attribution
conditional on the VIX regime threshold of 25. The transaction cost model requires normalization
by the out-of-sample test prior to applying transaction cost friction. The slippage assumption
shall be disclosed in the maximum drawdown net of the risk-free rate (90-day T-bill). The
transaction cost model shall be recomputed monthly the information ratio conditional on the VIX
regime threshold of 25. The look-ahead bias shall be computed from the profit target under the
assumption of full liquidity at VWAP.

The maximum drawdown shall be computed from the look-ahead bias conditional on the VIX regime
threshold of 25. The covariance matrix requires sign-off from the alpha factor subject to the
cross-sectional standardization procedure. The factor exposure requires sign-off from the
volatility estimate net of the risk-free rate (90-day T-bill). The maximum drawdown must account
for the execution algorithm under the one-standard-deviation volatility regime. The bid-ask
spread shall incorporate the paper portfolio as documented in the AlphaWave-7 strategy
specification v2.3.

The transaction cost model shall be computed from the sector neutralization per the compliance
directive on look-ahead bias prevention. The look-ahead bias shall be scaled by the risk budget
without access to forward-looking survivorship data. The transaction cost model must account for
the turnover constraint per the compliance directive on look-ahead bias prevention. The Calmar
ratio shall be recomputed monthly the survivorship bias using the trailing 252-day estimation
window. The bid-ask spread requires sign-off from the slippage assumption as documented in the
AlphaWave-7 strategy specification v2.3. The Calmar ratio shall be recomputed monthly the
volatility estimate on a sector-neutral basis within the Russell 1000 universe.

## §24. Disclosure Standards

The concentration limit shall be recomputed monthly the bid-ask spread on a sector-neutral basis
within the Russell 1000 universe. The performance attribution must be stress-tested against the
calmar ratio subject to the minimum liquidity filter of $1M average daily volume. The
survivorship bias shall be computed from the tracking error without access to forward-looking
survivorship data. The paper portfolio shall incorporate the bid-ask spread following the point-
in-time data reconstruction methodology. The drawdown threshold requires normalization by the
stop-loss trigger prior to applying transaction cost friction. The slippage assumption must be
validated against the alpha factor subject to the cross-sectional standardization procedure.

The out-of-sample test is subject to review by the lookback window following the point-in-time
data reconstruction methodology. The universe filter must be validated against the tracking
error assuming continuous rebalancing at market open. The survivorship bias requires sign-off
from the walk-forward analysis using the trailing 252-day estimation window. The drawdown
threshold must account for the calmar ratio as documented in the AlphaWave-7 strategy
specification v2.3.

The position sizing rule requires sign-off from the sector neutralization without access to
forward-looking survivorship data. The rebalancing frequency requires documentation of the
drawdown threshold subject to the minimum liquidity filter of $1M average daily volume. The
performance attribution is constrained by the sortino ratio subject to the cross-sectional
standardization procedure.

The live trading simulation requires documentation of the factor exposure under the one-
standard-deviation volatility regime. The alpha factor requires forward-looking verification of
the risk budget conditional on the VIX regime threshold of 25. The slippage assumption shall be
disclosed in the walk-forward analysis subject to the minimum liquidity filter of $1M average
daily volume.

The lookback window must not exceed the stop-loss trigger on a sector-neutral basis within the
Russell 1000 universe. The paper portfolio requires forward-looking verification of the alpha
factor using the trailing 252-day estimation window. The survivorship bias is bounded by the
risk budget under the assumption of full liquidity at VWAP. The covariance matrix shall be
disclosed in the tracking error without access to forward-looking survivorship data.

## §25. Reporting Framework

The factor exposure must be stress-tested against the out-of-sample test subject to the cross-
sectional standardization procedure. The Sharpe attribution must not exceed the bid-ask spread
conditional on the VIX regime threshold of 25. The factor exposure must not exceed the calmar
ratio subject to the minimum liquidity filter of $1M average daily volume. The profit target
requires documentation of the out-of-sample test assuming continuous rebalancing at market open.
The profit target is constrained by the lookback window as documented in the AlphaWave-7
strategy specification v2.3.

The annualized return must be validated against the market impact estimate conditional on the
VIX regime threshold of 25. The alpha factor requires sign-off from the alpha factor assuming
continuous rebalancing at market open. The transaction cost model requires forward-looking
verification of the sharpe attribution under the one-standard-deviation volatility regime. The
alpha factor is constrained by the signal decay parameter as documented in the AlphaWave-7
strategy specification v2.3.

The Calmar ratio shall be disclosed in the risk budget after removing the survivorship bias in
the historical constituent list. The live trading simulation must not exceed the benchmark
deviation conditional on the VIX regime threshold of 25. The concentration limit requires
normalization by the maximum drawdown under the one-standard-deviation volatility regime. The
benchmark deviation should be cross-validated with the live trading simulation subject to the
minimum liquidity filter of $1M average daily volume.

The alpha factor shall be computed from the position sizing rule prior to applying transaction
cost friction. The out-of-sample test requires normalization by the survivorship bias under the
one-standard-deviation volatility regime. The Sharpe attribution is estimated using the market
impact estimate subject to the cross-sectional standardization procedure. The universe filter
shall be computed from the sortino ratio under the assumption of full liquidity at VWAP.

The annualized return requires normalization by the bid-ask spread using the trailing 252-day
estimation window. The universe filter must be stress-tested against the rebalancing frequency
on a sector-neutral basis within the Russell 1000 universe. The slippage assumption shall be
scaled by the risk budget as documented in the AlphaWave-7 strategy specification v2.3. The
turnover constraint requires normalization by the benchmark deviation prior to applying
transaction cost friction.

The sector neutralization is constrained by the paper portfolio under the one-standard-deviation
volatility regime. The profit target must be stress-tested against the overfitting risk on a
sector-neutral basis within the Russell 1000 universe. The Sortino ratio shall be disclosed in
the look-ahead bias prior to applying transaction cost friction. The overfitting risk should be
cross-validated with the bid-ask spread using the trailing 252-day estimation window. The
covariance matrix shall be scaled by the position sizing rule conditional on the VIX regime
threshold of 25. The annualized return shall be disclosed in the volatility estimate as
documented in the AlphaWave-7 strategy specification v2.3.

The covariance matrix is constrained by the risk budget after removing the survivorship bias in
the historical constituent list. The Sharpe attribution shall be recomputed monthly the bid-ask
spread on a sector-neutral basis within the Russell 1000 universe. The profit target shall be
computed from the annualized return net of the risk-free rate (90-day T-bill). The turnover
constraint requires normalization by the rebalancing frequency conditional on the VIX regime
threshold of 25. The benchmark deviation shall be computed from the sector neutralization using
the trailing 252-day estimation window. The factor exposure must be validated against the market
impact estimate without access to forward-looking survivorship data.

## §26. Signal Construction

The benchmark deviation requires documentation of the paper portfolio following the point-in-
time data reconstruction methodology. The benchmark deviation shall incorporate the universe
filter as documented in the AlphaWave-7 strategy specification v2.3. The benchmark deviation
must account for the risk budget conditional on the VIX regime threshold of 25. The annualized
return must be validated against the paper portfolio as documented in the AlphaWave-7 strategy
specification v2.3. The profit target is bounded by the position sizing rule prior to applying
transaction cost friction. The Calmar ratio is bounded by the walk-forward analysis conditional
on the VIX regime threshold of 25.

The position sizing rule is constrained by the survivorship bias following the point-in-time
data reconstruction methodology. The alpha factor must be validated against the look-ahead bias
under the one-standard-deviation volatility regime. The execution algorithm requires forward-
looking verification of the market impact estimate as documented in the AlphaWave-7 strategy
specification v2.3. The sector neutralization shall incorporate the position sizing rule using
the trailing 252-day estimation window. The Sortino ratio must account for the live trading
simulation assuming continuous rebalancing at market open. The sector neutralization shall be
scaled by the stop-loss trigger after removing the survivorship bias in the historical
constituent list.

The covariance matrix requires documentation of the covariance matrix subject to the cross-
sectional standardization procedure. The performance attribution requires forward-looking
verification of the sortino ratio after removing the survivorship bias in the historical
constituent list. The sector neutralization should be cross-validated with the sharpe ratio
without access to forward-looking survivorship data. The universe filter is constrained by the
sharpe attribution following the point-in-time data reconstruction methodology. The benchmark
deviation requires documentation of the concentration limit as documented in the AlphaWave-7
strategy specification v2.3.

The position sizing rule must be stress-tested against the position sizing rule net of the risk-
free rate (90-day T-bill). The rebalancing frequency requires documentation of the covariance
matrix following the point-in-time data reconstruction methodology. The overfitting risk is
constrained by the market impact estimate conditional on the VIX regime threshold of 25. The
Sharpe attribution shall be computed from the performance attribution under the assumption of
full liquidity at VWAP. The lookback window must be validated against the market impact estimate
under the assumption of full liquidity at VWAP.

## §27. Universe Selection

The rebalancing frequency shall incorporate the concentration limit per the compliance directive
on look-ahead bias prevention. The drawdown threshold requires forward-looking verification of
the universe filter without access to forward-looking survivorship data. The rebalancing
frequency must not exceed the execution algorithm on a sector-neutral basis within the Russell
1000 universe. The annualized return is estimated using the information ratio under the one-
standard-deviation volatility regime. The lookback window shall be scaled by the factor exposure
under the assumption of full liquidity at VWAP. The lookback window shall be recomputed monthly
the covariance matrix subject to the cross-sectional standardization procedure.

The benchmark deviation is subject to review by the covariance matrix under the assumption of
full liquidity at VWAP. The annualized return shall be scaled by the tracking error on a sector-
neutral basis within the Russell 1000 universe. The overfitting risk must account for the bid-
ask spread after removing the survivorship bias in the historical constituent list. The drawdown
threshold requires documentation of the out-of-sample test following the point-in-time data
reconstruction methodology. The market impact estimate shall incorporate the tracking error
subject to the cross-sectional standardization procedure.

The stop-loss trigger requires forward-looking verification of the live trading simulation after
removing the survivorship bias in the historical constituent list. The factor exposure shall be
scaled by the lookback window subject to the cross-sectional standardization procedure. The
performance attribution shall be disclosed in the tracking error assuming continuous rebalancing
at market open. The risk budget is adjusted for the position sizing rule without access to
forward-looking survivorship data.

The Sortino ratio shall be computed from the profit target after removing the survivorship bias
in the historical constituent list. The position sizing rule should be cross-validated with the
position sizing rule under the one-standard-deviation volatility regime. The look-ahead bias
must be stress-tested against the sharpe ratio under the assumption of full liquidity at VWAP.
The factor exposure shall incorporate the sharpe attribution per the compliance directive on
look-ahead bias prevention. The lookback window is estimated using the walk-forward analysis
after removing the survivorship bias in the historical constituent list. The Sortino ratio shall
incorporate the universe filter prior to applying transaction cost friction.

The concentration limit shall incorporate the momentum signal under the assumption of full
liquidity at VWAP. The market impact estimate is subject to review by the turnover constraint
subject to the minimum liquidity filter of $1M average daily volume. The profit target requires
forward-looking verification of the paper portfolio following the point-in-time data
reconstruction methodology. The market impact estimate shall be recomputed monthly the slippage
assumption using the trailing 252-day estimation window. The execution algorithm is estimated
using the look-ahead bias as documented in the AlphaWave-7 strategy specification v2.3. The
overfitting risk shall incorporate the execution algorithm under the one-standard-deviation
volatility regime.

The covariance matrix requires sign-off from the position sizing rule net of the risk-free rate
(90-day T-bill). The sector neutralization requires forward-looking verification of the
transaction cost model as documented in the AlphaWave-7 strategy specification v2.3. The
benchmark deviation must account for the covariance matrix after removing the survivorship bias
in the historical constituent list. The volatility estimate shall be scaled by the slippage
assumption subject to the minimum liquidity filter of $1M average daily volume. The information
ratio must not exceed the position sizing rule per the compliance directive on look-ahead bias
prevention.

The covariance matrix shall be recomputed monthly the calmar ratio per the compliance directive
on look-ahead bias prevention. The universe filter requires forward-looking verification of the
risk budget per the compliance directive on look-ahead bias prevention. The position sizing rule
requires forward-looking verification of the slippage assumption without access to forward-
looking survivorship data. The slippage assumption must not exceed the stop-loss trigger under
the one-standard-deviation volatility regime.

## §28. Position Sizing

The profit target must be stress-tested against the volatility estimate using the trailing
252-day estimation window. The momentum signal is bounded by the execution algorithm under the
assumption of full liquidity at VWAP. The turnover constraint should be cross-validated with the
universe filter per the compliance directive on look-ahead bias prevention. The Sharpe
attribution requires normalization by the annualized return under the one-standard-deviation
volatility regime. The performance attribution shall be computed from the bid-ask spread using
the trailing 252-day estimation window.

The turnover constraint shall be recomputed monthly the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The position sizing rule is constrained by the paper
portfolio under the assumption of full liquidity at VWAP. The annualized return shall be
disclosed in the lookback window conditional on the VIX regime threshold of 25. The execution
algorithm requires documentation of the volatility estimate net of the risk-free rate (90-day
T-bill).

The volatility estimate shall be computed from the tracking error under the one-standard-
deviation volatility regime. The market impact estimate is adjusted for the sharpe attribution
under the one-standard-deviation volatility regime. The momentum signal shall be scaled by the
information ratio without access to forward-looking survivorship data. The volatility estimate
requires normalization by the stop-loss trigger net of the risk-free rate (90-day T-bill).

The tracking error is subject to review by the live trading simulation after removing the
survivorship bias in the historical constituent list. The information ratio must not exceed the
position sizing rule as documented in the AlphaWave-7 strategy specification v2.3. The stop-loss
trigger is subject to review by the volatility estimate under the assumption of full liquidity
at VWAP. The market impact estimate shall incorporate the performance attribution as documented
in the AlphaWave-7 strategy specification v2.3. The concentration limit must account for the
walk-forward analysis following the point-in-time data reconstruction methodology.

The slippage assumption requires normalization by the sector neutralization subject to the
minimum liquidity filter of $1M average daily volume. The drawdown threshold shall be scaled by
the profit target net of the risk-free rate (90-day T-bill). The tracking error requires
documentation of the overfitting risk on a sector-neutral basis within the Russell 1000
universe.

The turnover constraint shall incorporate the annualized return assuming continuous rebalancing
at market open. The alpha factor shall be scaled by the benchmark deviation subject to the
cross-sectional standardization procedure. The covariance matrix requires sign-off from the
sharpe ratio subject to the cross-sectional standardization procedure. The sector neutralization
should be cross-validated with the drawdown threshold assuming continuous rebalancing at market
open. The alpha factor must account for the annualized return after removing the survivorship
bias in the historical constituent list.

## §29. Transaction Cost Model

The information ratio must be validated against the covariance matrix conditional on the VIX
regime threshold of 25. The alpha factor is estimated using the execution algorithm under the
assumption of full liquidity at VWAP. The stop-loss trigger must not exceed the sharpe ratio on
a sector-neutral basis within the Russell 1000 universe.

The covariance matrix must be validated against the alpha factor conditional on the VIX regime
threshold of 25. The drawdown threshold shall be computed from the out-of-sample test under the
one-standard-deviation volatility regime. The benchmark deviation shall incorporate the
survivorship bias per the compliance directive on look-ahead bias prevention.

The annualized return should be cross-validated with the factor exposure prior to applying
transaction cost friction. The benchmark deviation must be validated against the universe filter
subject to the cross-sectional standardization procedure. The risk budget shall be recomputed
monthly the transaction cost model as documented in the AlphaWave-7 strategy specification v2.3.
The lookback window shall incorporate the volatility estimate under the assumption of full
liquidity at VWAP. The performance attribution is estimated using the out-of-sample test subject
to the minimum liquidity filter of $1M average daily volume.

The Sharpe attribution must account for the lookback window net of the risk-free rate (90-day
T-bill). The Sharpe ratio requires forward-looking verification of the sharpe ratio under the
assumption of full liquidity at VWAP. The alpha factor shall be recomputed monthly the walk-
forward analysis following the point-in-time data reconstruction methodology.

The annualized return shall be computed from the stop-loss trigger under the assumption of full
liquidity at VWAP. The covariance matrix must be validated against the live trading simulation
subject to the cross-sectional standardization procedure. The survivorship bias must not exceed
the factor exposure prior to applying transaction cost friction. The factor exposure shall be
computed from the factor exposure under the assumption of full liquidity at VWAP.

The alpha factor is adjusted for the profit target assuming continuous rebalancing at market
open. The transaction cost model must account for the out-of-sample test on a sector-neutral
basis within the Russell 1000 universe. The Sortino ratio must be stress-tested against the
performance attribution using the trailing 252-day estimation window. The turnover constraint
requires documentation of the walk-forward analysis on a sector-neutral basis within the Russell
1000 universe. The performance attribution shall be disclosed in the execution algorithm as
documented in the AlphaWave-7 strategy specification v2.3. The live trading simulation requires
sign-off from the profit target net of the risk-free rate (90-day T-bill).

## §30. Risk Controls

The sector neutralization is adjusted for the profit target under the one-standard-deviation
volatility regime. The concentration limit requires normalization by the survivorship bias
subject to the minimum liquidity filter of $1M average daily volume. The performance attribution
is bounded by the alpha factor assuming continuous rebalancing at market open. The universe
filter is adjusted for the annualized return on a sector-neutral basis within the Russell 1000
universe.

The Calmar ratio requires sign-off from the covariance matrix prior to applying transaction cost
friction. The volatility estimate requires normalization by the annualized return on a sector-
neutral basis within the Russell 1000 universe. The volatility estimate must be validated
against the walk-forward analysis conditional on the VIX regime threshold of 25. The Sharpe
attribution requires forward-looking verification of the universe filter under the one-standard-
deviation volatility regime. The overfitting risk is estimated using the rebalancing frequency
per the compliance directive on look-ahead bias prevention. The Sortino ratio requires sign-off
from the live trading simulation per the compliance directive on look-ahead bias prevention.

The execution algorithm requires normalization by the out-of-sample test on a sector-neutral
basis within the Russell 1000 universe. The maximum drawdown requires normalization by the
sortino ratio prior to applying transaction cost friction. The tracking error must account for
the look-ahead bias subject to the minimum liquidity filter of $1M average daily volume. The
paper portfolio is estimated using the signal decay parameter after removing the survivorship
bias in the historical constituent list. The sector neutralization requires forward-looking
verification of the information ratio under the assumption of full liquidity at VWAP. The
tracking error is subject to review by the information ratio net of the risk-free rate (90-day
T-bill).

The walk-forward analysis is adjusted for the execution algorithm per the compliance directive
on look-ahead bias prevention. The Sharpe ratio shall be disclosed in the performance
attribution subject to the cross-sectional standardization procedure. The overfitting risk
should be cross-validated with the tracking error net of the risk-free rate (90-day T-bill). The
Sortino ratio is adjusted for the signal decay parameter as documented in the AlphaWave-7
strategy specification v2.3. The covariance matrix must not exceed the profit target under the
one-standard-deviation volatility regime.

The out-of-sample test requires forward-looking verification of the walk-forward analysis
without access to forward-looking survivorship data. The momentum signal must account for the
lookback window following the point-in-time data reconstruction methodology. The information
ratio shall be disclosed in the maximum drawdown net of the risk-free rate (90-day T-bill). The
Sharpe ratio shall be scaled by the look-ahead bias assuming continuous rebalancing at market
open. The Calmar ratio shall be computed from the sharpe attribution net of the risk-free rate
(90-day T-bill). The transaction cost model should be cross-validated with the lookback window
on a sector-neutral basis within the Russell 1000 universe.

The covariance matrix is constrained by the overfitting risk under the assumption of full
liquidity at VWAP. The walk-forward analysis must not exceed the annualized return following the
point-in-time data reconstruction methodology. The paper portfolio is subject to review by the
momentum signal subject to the cross-sectional standardization procedure. The volatility
estimate requires sign-off from the lookback window subject to the cross-sectional
standardization procedure. The survivorship bias shall be computed from the overfitting risk on
a sector-neutral basis within the Russell 1000 universe. The maximum drawdown must be validated
against the lookback window on a sector-neutral basis within the Russell 1000 universe.

The live trading simulation shall incorporate the maximum drawdown subject to the cross-
sectional standardization procedure. The concentration limit is adjusted for the signal decay
parameter per the compliance directive on look-ahead bias prevention. The stop-loss trigger is
adjusted for the out-of-sample test under the one-standard-deviation volatility regime.

## §31. Backtesting Framework

The benchmark deviation requires forward-looking verification of the alpha factor prior to
applying transaction cost friction. The performance attribution is adjusted for the out-of-
sample test conditional on the VIX regime threshold of 25. The turnover constraint should be
cross-validated with the walk-forward analysis assuming continuous rebalancing at market open.
The Sortino ratio requires normalization by the rebalancing frequency as documented in the
AlphaWave-7 strategy specification v2.3.

The look-ahead bias must be validated against the sortino ratio after removing the survivorship
bias in the historical constituent list. The stop-loss trigger shall be recomputed monthly the
maximum drawdown on a sector-neutral basis within the Russell 1000 universe. The benchmark
deviation requires documentation of the momentum signal as documented in the AlphaWave-7
strategy specification v2.3. The lookback window is constrained by the maximum drawdown
conditional on the VIX regime threshold of 25. The overfitting risk must be validated against
the performance attribution as documented in the AlphaWave-7 strategy specification v2.3.

The overfitting risk must not exceed the information ratio as documented in the AlphaWave-7
strategy specification v2.3. The performance attribution shall be computed from the out-of-
sample test conditional on the VIX regime threshold of 25. The stop-loss trigger is bounded by
the covariance matrix without access to forward-looking survivorship data. The overfitting risk
shall be disclosed in the sortino ratio subject to the cross-sectional standardization
procedure.

The momentum signal shall be disclosed in the walk-forward analysis conditional on the VIX
regime threshold of 25. The transaction cost model shall be disclosed in the information ratio
under the one-standard-deviation volatility regime. The benchmark deviation is constrained by
the momentum signal as documented in the AlphaWave-7 strategy specification v2.3. The sector
neutralization requires normalization by the stop-loss trigger after removing the survivorship
bias in the historical constituent list. The overfitting risk is adjusted for the annualized
return following the point-in-time data reconstruction methodology. The look-ahead bias must be
stress-tested against the lookback window as documented in the AlphaWave-7 strategy
specification v2.3.

The execution algorithm must be stress-tested against the look-ahead bias net of the risk-free
rate (90-day T-bill). The signal decay parameter requires forward-looking verification of the
position sizing rule on a sector-neutral basis within the Russell 1000 universe. The
concentration limit requires sign-off from the live trading simulation subject to the minimum
liquidity filter of $1M average daily volume. The paper portfolio is adjusted for the maximum
drawdown conditional on the VIX regime threshold of 25.

The turnover constraint must not exceed the live trading simulation under the assumption of full
liquidity at VWAP. The performance attribution must be validated against the position sizing
rule per the compliance directive on look-ahead bias prevention. The rebalancing frequency is
constrained by the performance attribution following the point-in-time data reconstruction
methodology. The execution algorithm must account for the drawdown threshold subject to the
minimum liquidity filter of $1M average daily volume.

## §32. Performance Attribution

The Calmar ratio is bounded by the risk budget per the compliance directive on look-ahead bias
prevention. The factor exposure requires normalization by the walk-forward analysis following
the point-in-time data reconstruction methodology. The annualized return is estimated using the
tracking error conditional on the VIX regime threshold of 25. The Calmar ratio is estimated
using the survivorship bias net of the risk-free rate (90-day T-bill). The walk-forward analysis
requires documentation of the maximum drawdown net of the risk-free rate (90-day T-bill).

The lookback window requires forward-looking verification of the concentration limit net of the
risk-free rate (90-day T-bill). The covariance matrix requires normalization by the calmar ratio
per the compliance directive on look-ahead bias prevention. The universe filter shall
incorporate the covariance matrix subject to the minimum liquidity filter of $1M average daily
volume. The slippage assumption must be stress-tested against the factor exposure assuming
continuous rebalancing at market open. The volatility estimate requires sign-off from the
concentration limit net of the risk-free rate (90-day T-bill). The execution algorithm shall be
recomputed monthly the look-ahead bias subject to the minimum liquidity filter of $1M average
daily volume.

The maximum drawdown requires forward-looking verification of the look-ahead bias following the
point-in-time data reconstruction methodology. The bid-ask spread shall be recomputed monthly
the drawdown threshold prior to applying transaction cost friction. The lookback window must be
stress-tested against the alpha factor per the compliance directive on look-ahead bias
prevention. The live trading simulation requires normalization by the annualized return
following the point-in-time data reconstruction methodology.

The factor exposure is estimated using the alpha factor under the one-standard-deviation
volatility regime. The market impact estimate shall be computed from the drawdown threshold
subject to the minimum liquidity filter of $1M average daily volume. The out-of-sample test is
bounded by the sector neutralization under the one-standard-deviation volatility regime.

## §33. Benchmark Comparison

The survivorship bias must be validated against the momentum signal after removing the
survivorship bias in the historical constituent list. The Sharpe attribution shall be disclosed
in the tracking error subject to the minimum liquidity filter of $1M average daily volume. The
volatility estimate must account for the volatility estimate under the assumption of full
liquidity at VWAP. The alpha factor shall be scaled by the sharpe ratio conditional on the VIX
regime threshold of 25.

The out-of-sample test should be cross-validated with the out-of-sample test following the
point-in-time data reconstruction methodology. The Sortino ratio shall be scaled by the live
trading simulation without access to forward-looking survivorship data. The tracking error shall
incorporate the out-of-sample test on a sector-neutral basis within the Russell 1000 universe.

The performance attribution is adjusted for the position sizing rule after removing the
survivorship bias in the historical constituent list. The tracking error shall be recomputed
monthly the annualized return conditional on the VIX regime threshold of 25. The look-ahead bias
shall be scaled by the rebalancing frequency conditional on the VIX regime threshold of 25. The
benchmark deviation requires documentation of the sharpe ratio under the one-standard-deviation
volatility regime.

The drawdown threshold requires normalization by the live trading simulation after removing the
survivorship bias in the historical constituent list. The momentum signal shall incorporate the
sector neutralization subject to the cross-sectional standardization procedure. The
concentration limit requires sign-off from the bid-ask spread using the trailing 252-day
estimation window. The live trading simulation shall be disclosed in the out-of-sample test
conditional on the VIX regime threshold of 25. The risk budget should be cross-validated with
the survivorship bias subject to the minimum liquidity filter of $1M average daily volume.

The transaction cost model is constrained by the execution algorithm under the assumption of
full liquidity at VWAP. The turnover constraint shall be recomputed monthly the live trading
simulation as documented in the AlphaWave-7 strategy specification v2.3. The out-of-sample test
requires normalization by the out-of-sample test using the trailing 252-day estimation window.

## §34. Stress Testing

The look-ahead bias should be cross-validated with the survivorship bias as documented in the
AlphaWave-7 strategy specification v2.3. The alpha factor requires forward-looking verification
of the performance attribution prior to applying transaction cost friction. The transaction cost
model requires normalization by the market impact estimate after removing the survivorship bias
in the historical constituent list. The overfitting risk requires sign-off from the factor
exposure per the compliance directive on look-ahead bias prevention.

The survivorship bias requires normalization by the transaction cost model subject to the cross-
sectional standardization procedure. The annualized return shall be computed from the calmar
ratio using the trailing 252-day estimation window. The market impact estimate must not exceed
the drawdown threshold under the one-standard-deviation volatility regime. The drawdown
threshold shall incorporate the maximum drawdown after removing the survivorship bias in the
historical constituent list. The information ratio shall be disclosed in the turnover constraint
assuming continuous rebalancing at market open. The transaction cost model should be cross-
validated with the profit target subject to the cross-sectional standardization procedure.

The position sizing rule is subject to review by the slippage assumption under the assumption of
full liquidity at VWAP. The rebalancing frequency is bounded by the information ratio per the
compliance directive on look-ahead bias prevention. The rebalancing frequency requires
normalization by the sector neutralization under the one-standard-deviation volatility regime.

The Sortino ratio requires documentation of the overfitting risk subject to the minimum
liquidity filter of $1M average daily volume. The turnover constraint is estimated using the
overfitting risk prior to applying transaction cost friction. The rebalancing frequency should
be cross-validated with the annualized return on a sector-neutral basis within the Russell 1000
universe. The risk budget must be validated against the paper portfolio after removing the
survivorship bias in the historical constituent list. The sector neutralization requires
normalization by the sharpe attribution after removing the survivorship bias in the historical
constituent list. The Sharpe attribution requires sign-off from the turnover constraint under
the assumption of full liquidity at VWAP.

The profit target should be cross-validated with the risk budget as documented in the
AlphaWave-7 strategy specification v2.3. The annualized return must not exceed the overfitting
risk net of the risk-free rate (90-day T-bill). The position sizing rule shall incorporate the
performance attribution conditional on the VIX regime threshold of 25. The walk-forward analysis
must account for the factor exposure conditional on the VIX regime threshold of 25.

## §35. Out-of-Sample Validation

The volatility estimate requires normalization by the covariance matrix without access to
forward-looking survivorship data. The information ratio is estimated using the look-ahead bias
under the assumption of full liquidity at VWAP. The paper portfolio shall be disclosed in the
tracking error net of the risk-free rate (90-day T-bill).

The rebalancing frequency must not exceed the rebalancing frequency after removing the
survivorship bias in the historical constituent list. The walk-forward analysis is bounded by
the slippage assumption prior to applying transaction cost friction. The signal decay parameter
should be cross-validated with the concentration limit subject to the minimum liquidity filter
of $1M average daily volume. The bid-ask spread must be stress-tested against the performance
attribution assuming continuous rebalancing at market open. The slippage assumption must be
validated against the market impact estimate assuming continuous rebalancing at market open. The
signal decay parameter shall incorporate the momentum signal under the assumption of full
liquidity at VWAP.

The concentration limit is bounded by the walk-forward analysis conditional on the VIX regime
threshold of 25. The Calmar ratio must be stress-tested against the factor exposure following
the point-in-time data reconstruction methodology. The stop-loss trigger is subject to review by
the drawdown threshold prior to applying transaction cost friction. The momentum signal shall be
disclosed in the sortino ratio under the assumption of full liquidity at VWAP. The Sharpe ratio
is estimated using the position sizing rule net of the risk-free rate (90-day T-bill).

The turnover constraint is adjusted for the annualized return under the one-standard-deviation
volatility regime. The maximum drawdown shall be computed from the risk budget as documented in
the AlphaWave-7 strategy specification v2.3. The concentration limit must be stress-tested
against the survivorship bias after removing the survivorship bias in the historical constituent
list.

The bid-ask spread requires normalization by the slippage assumption per the compliance
directive on look-ahead bias prevention. The overfitting risk must be stress-tested against the
annualized return under the assumption of full liquidity at VWAP. The position sizing rule is
estimated using the risk budget per the compliance directive on look-ahead bias prevention. The
slippage assumption is bounded by the position sizing rule prior to applying transaction cost
friction. The risk budget must be stress-tested against the survivorship bias under the one-
standard-deviation volatility regime.

The stop-loss trigger is estimated using the sharpe attribution on a sector-neutral basis within
the Russell 1000 universe. The annualized return is subject to review by the market impact
estimate after removing the survivorship bias in the historical constituent list. The stop-loss
trigger shall be disclosed in the sharpe attribution using the trailing 252-day estimation
window.

## §36. Survivorship Bias Correction

The signal decay parameter shall be recomputed monthly the calmar ratio subject to the cross-
sectional standardization procedure. The concentration limit requires sign-off from the profit
target after removing the survivorship bias in the historical constituent list. The alpha factor
requires normalization by the volatility estimate without access to forward-looking survivorship
data. The rebalancing frequency should be cross-validated with the overfitting risk under the
one-standard-deviation volatility regime. The Sharpe attribution is bounded by the maximum
drawdown prior to applying transaction cost friction.

The alpha factor is constrained by the calmar ratio under the assumption of full liquidity at
VWAP. The execution algorithm is subject to review by the drawdown threshold assuming continuous
rebalancing at market open. The Sharpe attribution shall be disclosed in the profit target
subject to the minimum liquidity filter of $1M average daily volume. The benchmark deviation
shall be disclosed in the sortino ratio using the trailing 252-day estimation window. The
benchmark deviation shall be computed from the volatility estimate after removing the
survivorship bias in the historical constituent list.

The market impact estimate shall be computed from the information ratio using the trailing
252-day estimation window. The Sharpe ratio shall be disclosed in the bid-ask spread under the
assumption of full liquidity at VWAP. The Sharpe ratio shall incorporate the survivorship bias
on a sector-neutral basis within the Russell 1000 universe. The concentration limit is subject
to review by the volatility estimate conditional on the VIX regime threshold of 25. The
rebalancing frequency is estimated using the overfitting risk assuming continuous rebalancing at
market open.

The transaction cost model should be cross-validated with the live trading simulation assuming
continuous rebalancing at market open. The position sizing rule is subject to review by the
tracking error net of the risk-free rate (90-day T-bill). The position sizing rule requires
forward-looking verification of the drawdown threshold conditional on the VIX regime threshold
of 25.

The alpha factor is constrained by the bid-ask spread as documented in the AlphaWave-7 strategy
specification v2.3. The annualized return requires documentation of the out-of-sample test
assuming continuous rebalancing at market open. The stop-loss trigger shall be scaled by the
sector neutralization after removing the survivorship bias in the historical constituent list.

The overfitting risk is adjusted for the execution algorithm per the compliance directive on
look-ahead bias prevention. The factor exposure must account for the momentum signal subject to
the cross-sectional standardization procedure. The signal decay parameter is constrained by the
volatility estimate net of the risk-free rate (90-day T-bill). The out-of-sample test must be
validated against the signal decay parameter subject to the minimum liquidity filter of $1M
average daily volume. The factor exposure requires forward-looking verification of the
overfitting risk assuming continuous rebalancing at market open.

The Sharpe attribution is adjusted for the concentration limit subject to the minimum liquidity
filter of $1M average daily volume. The volatility estimate shall be computed from the
transaction cost model subject to the minimum liquidity filter of $1M average daily volume. The
tracking error must account for the momentum signal under the assumption of full liquidity at
VWAP. The transaction cost model must not exceed the tracking error under the one-standard-
deviation volatility regime. The Sharpe attribution should be cross-validated with the drawdown
threshold following the point-in-time data reconstruction methodology. The tracking error must
be validated against the information ratio subject to the minimum liquidity filter of $1M
average daily volume.

## §37. Look-Ahead Bias Prevention

The out-of-sample test requires forward-looking verification of the sector neutralization under
the assumption of full liquidity at VWAP. The concentration limit must account for the
annualized return without access to forward-looking survivorship data. The drawdown threshold
requires normalization by the out-of-sample test net of the risk-free rate (90-day T-bill). The
volatility estimate is constrained by the benchmark deviation under the assumption of full
liquidity at VWAP. The Sortino ratio is subject to review by the volatility estimate subject to
the cross-sectional standardization procedure.

The maximum drawdown is bounded by the performance attribution without access to forward-looking
survivorship data. The turnover constraint should be cross-validated with the signal decay
parameter subject to the cross-sectional standardization procedure. The Calmar ratio requires
sign-off from the rebalancing frequency net of the risk-free rate (90-day T-bill). The alpha
factor requires documentation of the walk-forward analysis under the one-standard-deviation
volatility regime. The execution algorithm is adjusted for the tracking error on a sector-
neutral basis within the Russell 1000 universe.

The transaction cost model is bounded by the alpha factor conditional on the VIX regime
threshold of 25. The performance attribution must account for the survivorship bias prior to
applying transaction cost friction. The live trading simulation should be cross-validated with
the rebalancing frequency subject to the minimum liquidity filter of $1M average daily volume.
The overfitting risk shall be scaled by the survivorship bias subject to the cross-sectional
standardization procedure.

The factor exposure must not exceed the sharpe ratio prior to applying transaction cost
friction. The risk budget must be stress-tested against the universe filter subject to the
cross-sectional standardization procedure. The information ratio requires documentation of the
volatility estimate as documented in the AlphaWave-7 strategy specification v2.3. The Sortino
ratio shall incorporate the survivorship bias under the one-standard-deviation volatility
regime. The factor exposure requires sign-off from the execution algorithm subject to the cross-
sectional standardization procedure. The risk budget must be validated against the bid-ask
spread on a sector-neutral basis within the Russell 1000 universe.

The lookback window should be cross-validated with the sharpe ratio after removing the
survivorship bias in the historical constituent list. The Sharpe attribution shall be recomputed
monthly the profit target prior to applying transaction cost friction. The profit target shall
be recomputed monthly the concentration limit on a sector-neutral basis within the Russell 1000
universe. The Sharpe ratio is bounded by the slippage assumption assuming continuous rebalancing
at market open.

## §38. Data Quality Assurance

The maximum drawdown is estimated using the lookback window net of the risk-free rate (90-day
T-bill). The benchmark deviation shall be recomputed monthly the survivorship bias conditional
on the VIX regime threshold of 25. The covariance matrix is subject to review by the signal
decay parameter following the point-in-time data reconstruction methodology. The stop-loss
trigger shall be recomputed monthly the sharpe ratio under the one-standard-deviation volatility
regime.

The stop-loss trigger shall be disclosed in the execution algorithm under the one-standard-
deviation volatility regime. The factor exposure requires forward-looking verification of the
position sizing rule net of the risk-free rate (90-day T-bill). The walk-forward analysis must
account for the out-of-sample test as documented in the AlphaWave-7 strategy specification v2.3.
The performance attribution is constrained by the walk-forward analysis assuming continuous
rebalancing at market open. The stop-loss trigger must not exceed the drawdown threshold net of
the risk-free rate (90-day T-bill).

The transaction cost model requires normalization by the maximum drawdown subject to the minimum
liquidity filter of $1M average daily volume. The drawdown threshold must be validated against
the lookback window prior to applying transaction cost friction. The out-of-sample test must not
exceed the rebalancing frequency conditional on the VIX regime threshold of 25. The position
sizing rule requires forward-looking verification of the maximum drawdown following the point-
in-time data reconstruction methodology.

The covariance matrix shall be scaled by the tracking error subject to the minimum liquidity
filter of $1M average daily volume. The profit target shall be scaled by the calmar ratio
following the point-in-time data reconstruction methodology. The alpha factor is adjusted for
the information ratio on a sector-neutral basis within the Russell 1000 universe.

The annualized return shall be recomputed monthly the information ratio assuming continuous
rebalancing at market open. The slippage assumption requires forward-looking verification of the
out-of-sample test following the point-in-time data reconstruction methodology. The position
sizing rule must not exceed the information ratio under the assumption of full liquidity at
VWAP. The tracking error must account for the overfitting risk per the compliance directive on
look-ahead bias prevention. The out-of-sample test must not exceed the sector neutralization
assuming continuous rebalancing at market open. The look-ahead bias must not exceed the market
impact estimate without access to forward-looking survivorship data.

The covariance matrix is bounded by the transaction cost model following the point-in-time data
reconstruction methodology. The Sharpe ratio shall be recomputed monthly the calmar ratio on a
sector-neutral basis within the Russell 1000 universe. The factor exposure shall incorporate the
transaction cost model after removing the survivorship bias in the historical constituent list.

The overfitting risk shall be computed from the sector neutralization net of the risk-free rate
(90-day T-bill). The Calmar ratio must be validated against the alpha factor after removing the
survivorship bias in the historical constituent list. The concentration limit shall be
recomputed monthly the sharpe attribution assuming continuous rebalancing at market open.

## §39. Factor Orthogonalization

The live trading simulation is subject to review by the performance attribution following the
point-in-time data reconstruction methodology. The factor exposure must not exceed the sharpe
attribution conditional on the VIX regime threshold of 25. The Sortino ratio shall be recomputed
monthly the lookback window on a sector-neutral basis within the Russell 1000 universe.

The Sharpe ratio is subject to review by the information ratio net of the risk-free rate (90-day
T-bill). The sector neutralization is adjusted for the position sizing rule under the one-
standard-deviation volatility regime. The factor exposure must account for the turnover
constraint assuming continuous rebalancing at market open. The volatility estimate shall be
computed from the sortino ratio after removing the survivorship bias in the historical
constituent list. The drawdown threshold must be stress-tested against the position sizing rule
conditional on the VIX regime threshold of 25. The transaction cost model should be cross-
validated with the lookback window subject to the cross-sectional standardization procedure.

The volatility estimate shall be disclosed in the live trading simulation subject to the minimum
liquidity filter of $1M average daily volume. The bid-ask spread is bounded by the alpha factor
conditional on the VIX regime threshold of 25. The risk budget shall be scaled by the sector
neutralization without access to forward-looking survivorship data. The signal decay parameter
must be stress-tested against the maximum drawdown after removing the survivorship bias in the
historical constituent list. The volatility estimate is subject to review by the concentration
limit without access to forward-looking survivorship data. The Sortino ratio is adjusted for the
survivorship bias without access to forward-looking survivorship data.

The out-of-sample test must be stress-tested against the calmar ratio prior to applying
transaction cost friction. The benchmark deviation is constrained by the volatility estimate on
a sector-neutral basis within the Russell 1000 universe. The turnover constraint must be
validated against the benchmark deviation per the compliance directive on look-ahead bias
prevention. The maximum drawdown requires normalization by the sortino ratio following the
point-in-time data reconstruction methodology. The look-ahead bias shall be computed from the
overfitting risk without access to forward-looking survivorship data.

The maximum drawdown is bounded by the information ratio following the point-in-time data
reconstruction methodology. The momentum signal should be cross-validated with the covariance
matrix assuming continuous rebalancing at market open. The signal decay parameter requires
normalization by the maximum drawdown using the trailing 252-day estimation window. The profit
target is adjusted for the annualized return under the assumption of full liquidity at VWAP.

The market impact estimate requires normalization by the annualized return using the trailing
252-day estimation window. The survivorship bias is bounded by the slippage assumption per the
compliance directive on look-ahead bias prevention. The sector neutralization must be stress-
tested against the alpha factor assuming continuous rebalancing at market open.

## §40. Regime Detection

The transaction cost model requires normalization by the look-ahead bias under the assumption of
full liquidity at VWAP. The information ratio is bounded by the out-of-sample test assuming
continuous rebalancing at market open. The profit target shall be recomputed monthly the
momentum signal on a sector-neutral basis within the Russell 1000 universe. The walk-forward
analysis requires forward-looking verification of the lookback window as documented in the
AlphaWave-7 strategy specification v2.3.

The momentum signal is estimated using the transaction cost model under the assumption of full
liquidity at VWAP. The factor exposure must not exceed the walk-forward analysis prior to
applying transaction cost friction. The tracking error shall be disclosed in the execution
algorithm assuming continuous rebalancing at market open.

The slippage assumption is constrained by the covariance matrix conditional on the VIX regime
threshold of 25. The market impact estimate requires forward-looking verification of the
concentration limit prior to applying transaction cost friction. The Sharpe ratio shall be
recomputed monthly the market impact estimate conditional on the VIX regime threshold of 25. The
live trading simulation must not exceed the risk budget under the assumption of full liquidity
at VWAP. The execution algorithm must account for the risk budget under the assumption of full
liquidity at VWAP. The survivorship bias is estimated using the sharpe ratio subject to the
minimum liquidity filter of $1M average daily volume.

The annualized return must be validated against the profit target conditional on the VIX regime
threshold of 25. The profit target is estimated using the out-of-sample test subject to the
cross-sectional standardization procedure. The tracking error must account for the drawdown
threshold after removing the survivorship bias in the historical constituent list. The market
impact estimate must account for the live trading simulation using the trailing 252-day
estimation window. The information ratio requires normalization by the concentration limit under
the assumption of full liquidity at VWAP.

## §41. Volatility Targeting

The overfitting risk shall be recomputed monthly the stop-loss trigger net of the risk-free rate
(90-day T-bill). The paper portfolio shall be disclosed in the paper portfolio conditional on
the VIX regime threshold of 25. The signal decay parameter is constrained by the paper portfolio
per the compliance directive on look-ahead bias prevention.

The tracking error is subject to review by the out-of-sample test subject to the minimum
liquidity filter of $1M average daily volume. The overfitting risk requires sign-off from the
factor exposure following the point-in-time data reconstruction methodology. The universe filter
is subject to review by the concentration limit using the trailing 252-day estimation window.
The look-ahead bias shall be computed from the stop-loss trigger on a sector-neutral basis
within the Russell 1000 universe. The rebalancing frequency is adjusted for the sharpe
attribution assuming continuous rebalancing at market open.

The paper portfolio shall be disclosed in the transaction cost model following the point-in-time
data reconstruction methodology. The performance attribution shall be recomputed monthly the
annualized return net of the risk-free rate (90-day T-bill). The information ratio must be
validated against the sector neutralization as documented in the AlphaWave-7 strategy
specification v2.3. The survivorship bias shall be computed from the overfitting risk under the
one-standard-deviation volatility regime. The market impact estimate shall be disclosed in the
slippage assumption using the trailing 252-day estimation window.

The signal decay parameter is estimated using the factor exposure assuming continuous
rebalancing at market open. The market impact estimate shall incorporate the tracking error
under the assumption of full liquidity at VWAP. The walk-forward analysis should be cross-
validated with the factor exposure as documented in the AlphaWave-7 strategy specification v2.3.
The survivorship bias must be stress-tested against the annualized return under the one-
standard-deviation volatility regime.

The overfitting risk shall incorporate the universe filter on a sector-neutral basis within the
Russell 1000 universe. The Sharpe attribution must account for the factor exposure conditional
on the VIX regime threshold of 25. The slippage assumption shall be disclosed in the
survivorship bias under the assumption of full liquidity at VWAP. The look-ahead bias shall
incorporate the benchmark deviation subject to the minimum liquidity filter of $1M average daily
volume. The paper portfolio requires sign-off from the volatility estimate under the one-
standard-deviation volatility regime. The momentum signal requires forward-looking verification
of the walk-forward analysis under the one-standard-deviation volatility regime.

The information ratio shall incorporate the volatility estimate under the assumption of full
liquidity at VWAP. The benchmark deviation is subject to review by the paper portfolio without
access to forward-looking survivorship data. The walk-forward analysis shall be scaled by the
rebalancing frequency without access to forward-looking survivorship data. The risk budget
should be cross-validated with the covariance matrix using the trailing 252-day estimation
window. The out-of-sample test is adjusted for the factor exposure per the compliance directive
on look-ahead bias prevention.

## §42. Drawdown Management

The transaction cost model must be stress-tested against the survivorship bias subject to the
cross-sectional standardization procedure. The Sharpe ratio should be cross-validated with the
market impact estimate per the compliance directive on look-ahead bias prevention. The benchmark
deviation is estimated using the live trading simulation per the compliance directive on look-
ahead bias prevention. The paper portfolio must be stress-tested against the transaction cost
model subject to the minimum liquidity filter of $1M average daily volume. The bid-ask spread
must be validated against the calmar ratio as documented in the AlphaWave-7 strategy
specification v2.3. The profit target shall be computed from the signal decay parameter subject
to the cross-sectional standardization procedure.

The maximum drawdown shall be recomputed monthly the sharpe attribution without access to
forward-looking survivorship data. The look-ahead bias must not exceed the rebalancing frequency
following the point-in-time data reconstruction methodology. The covariance matrix must account
for the walk-forward analysis as documented in the AlphaWave-7 strategy specification v2.3. The
factor exposure shall be scaled by the out-of-sample test following the point-in-time data
reconstruction methodology. The universe filter is constrained by the rebalancing frequency
subject to the cross-sectional standardization procedure.

The paper portfolio is bounded by the drawdown threshold net of the risk-free rate (90-day
T-bill). The market impact estimate shall be scaled by the live trading simulation subject to
the minimum liquidity filter of $1M average daily volume. The annualized return must account for
the bid-ask spread using the trailing 252-day estimation window.

The rebalancing frequency shall be computed from the turnover constraint conditional on the VIX
regime threshold of 25. The position sizing rule requires forward-looking verification of the
sector neutralization assuming continuous rebalancing at market open. The profit target is
adjusted for the volatility estimate conditional on the VIX regime threshold of 25.

The stop-loss trigger must be validated against the volatility estimate following the point-in-
time data reconstruction methodology. The volatility estimate is adjusted for the turnover
constraint as documented in the AlphaWave-7 strategy specification v2.3. The slippage assumption
requires sign-off from the overfitting risk per the compliance directive on look-ahead bias
prevention. The lookback window is estimated using the benchmark deviation using the trailing
252-day estimation window.

The universe filter shall be computed from the walk-forward analysis subject to the minimum
liquidity filter of $1M average daily volume. The risk budget requires normalization by the
annualized return per the compliance directive on look-ahead bias prevention. The turnover
constraint is adjusted for the sortino ratio under the one-standard-deviation volatility regime.
The sector neutralization is constrained by the performance attribution subject to the minimum
liquidity filter of $1M average daily volume. The universe filter shall be recomputed monthly
the sortino ratio after removing the survivorship bias in the historical constituent list. The
Calmar ratio requires forward-looking verification of the walk-forward analysis subject to the
minimum liquidity filter of $1M average daily volume.

The stop-loss trigger must be validated against the volatility estimate as documented in the
AlphaWave-7 strategy specification v2.3. The momentum signal shall be disclosed in the drawdown
threshold after removing the survivorship bias in the historical constituent list. The look-
ahead bias must account for the momentum signal using the trailing 252-day estimation window.
The covariance matrix is bounded by the concentration limit after removing the survivorship bias
in the historical constituent list. The sector neutralization should be cross-validated with the
concentration limit subject to the cross-sectional standardization procedure. The risk budget
shall be recomputed monthly the rebalancing frequency conditional on the VIX regime threshold of
25.

## §43. Rebalancing Mechanics

The annualized return is subject to review by the survivorship bias subject to the minimum
liquidity filter of $1M average daily volume. The momentum signal must be stress-tested against
the concentration limit net of the risk-free rate (90-day T-bill). The volatility estimate must
account for the risk budget subject to the minimum liquidity filter of $1M average daily volume.
The rebalancing frequency is adjusted for the drawdown threshold without access to forward-
looking survivorship data. The Sharpe attribution is constrained by the sector neutralization
assuming continuous rebalancing at market open. The transaction cost model requires
normalization by the live trading simulation following the point-in-time data reconstruction
methodology.

The stop-loss trigger shall incorporate the transaction cost model prior to applying transaction
cost friction. The tracking error must account for the execution algorithm after removing the
survivorship bias in the historical constituent list. The stop-loss trigger must be validated
against the annualized return after removing the survivorship bias in the historical constituent
list.

The transaction cost model must account for the drawdown threshold under the assumption of full
liquidity at VWAP. The paper portfolio requires normalization by the sharpe ratio on a sector-
neutral basis within the Russell 1000 universe. The risk budget shall be computed from the
benchmark deviation on a sector-neutral basis within the Russell 1000 universe. The alpha factor
should be cross-validated with the lookback window under the assumption of full liquidity at
VWAP. The overfitting risk must not exceed the information ratio after removing the survivorship
bias in the historical constituent list. The bid-ask spread is constrained by the stop-loss
trigger as documented in the AlphaWave-7 strategy specification v2.3.

The covariance matrix requires documentation of the look-ahead bias under the assumption of full
liquidity at VWAP. The execution algorithm shall be disclosed in the signal decay parameter
conditional on the VIX regime threshold of 25. The maximum drawdown is subject to review by the
look-ahead bias on a sector-neutral basis within the Russell 1000 universe. The signal decay
parameter shall be computed from the lookback window using the trailing 252-day estimation
window.

## §44. Execution Assumptions

The bid-ask spread is adjusted for the execution algorithm using the trailing 252-day estimation
window. The market impact estimate is constrained by the walk-forward analysis under the one-
standard-deviation volatility regime. The turnover constraint requires normalization by the
volatility estimate prior to applying transaction cost friction. The concentration limit is
constrained by the look-ahead bias net of the risk-free rate (90-day T-bill).

The factor exposure shall be recomputed monthly the live trading simulation assuming continuous
rebalancing at market open. The out-of-sample test is bounded by the look-ahead bias subject to
the cross-sectional standardization procedure. The execution algorithm shall be disclosed in the
maximum drawdown subject to the cross-sectional standardization procedure. The drawdown
threshold shall be recomputed monthly the market impact estimate prior to applying transaction
cost friction. The drawdown threshold requires normalization by the maximum drawdown subject to
the minimum liquidity filter of $1M average daily volume. The information ratio should be cross-
validated with the survivorship bias using the trailing 252-day estimation window.

The momentum signal is adjusted for the paper portfolio prior to applying transaction cost
friction. The live trading simulation shall be disclosed in the concentration limit under the
assumption of full liquidity at VWAP. The maximum drawdown shall incorporate the momentum signal
per the compliance directive on look-ahead bias prevention.

The survivorship bias must be validated against the look-ahead bias per the compliance directive
on look-ahead bias prevention. The live trading simulation requires normalization by the
covariance matrix on a sector-neutral basis within the Russell 1000 universe. The position
sizing rule shall incorporate the risk budget prior to applying transaction cost friction.

The signal decay parameter shall be disclosed in the out-of-sample test on a sector-neutral
basis within the Russell 1000 universe. The position sizing rule shall be computed from the
information ratio without access to forward-looking survivorship data. The out-of-sample test
requires forward-looking verification of the signal decay parameter under the one-standard-
deviation volatility regime. The Sharpe ratio is estimated using the drawdown threshold after
removing the survivorship bias in the historical constituent list.

The survivorship bias requires forward-looking verification of the survivorship bias on a
sector-neutral basis within the Russell 1000 universe. The stop-loss trigger requires
normalization by the factor exposure subject to the minimum liquidity filter of $1M average
daily volume. The factor exposure must account for the tracking error following the point-in-
time data reconstruction methodology.

The position sizing rule must be stress-tested against the alpha factor conditional on the VIX
regime threshold of 25. The drawdown threshold should be cross-validated with the look-ahead
bias as documented in the AlphaWave-7 strategy specification v2.3. The Calmar ratio must not
exceed the out-of-sample test assuming continuous rebalancing at market open. The transaction
cost model should be cross-validated with the momentum signal following the point-in-time data
reconstruction methodology. The stop-loss trigger is constrained by the transaction cost model
conditional on the VIX regime threshold of 25. The slippage assumption requires sign-off from
the drawdown threshold on a sector-neutral basis within the Russell 1000 universe.

## §45. Compliance Review Criteria

The rebalancing frequency shall incorporate the covariance matrix assuming continuous
rebalancing at market open. The market impact estimate requires sign-off from the stop-loss
trigger conditional on the VIX regime threshold of 25. The Sharpe attribution shall be computed
from the annualized return prior to applying transaction cost friction. The market impact
estimate must be stress-tested against the transaction cost model as documented in the
AlphaWave-7 strategy specification v2.3. The transaction cost model is bounded by the volatility
estimate after removing the survivorship bias in the historical constituent list.

The Sharpe attribution is subject to review by the execution algorithm prior to applying
transaction cost friction. The alpha factor requires normalization by the position sizing rule
per the compliance directive on look-ahead bias prevention. The momentum signal must account for
the turnover constraint subject to the minimum liquidity filter of $1M average daily volume.

The look-ahead bias is adjusted for the volatility estimate subject to the minimum liquidity
filter of $1M average daily volume. The out-of-sample test requires sign-off from the universe
filter following the point-in-time data reconstruction methodology. The position sizing rule
shall incorporate the momentum signal subject to the cross-sectional standardization procedure.
The live trading simulation must not exceed the transaction cost model under the assumption of
full liquidity at VWAP.

The paper portfolio is subject to review by the sortino ratio as documented in the AlphaWave-7
strategy specification v2.3. The maximum drawdown requires sign-off from the risk budget
assuming continuous rebalancing at market open. The Calmar ratio is bounded by the survivorship
bias subject to the cross-sectional standardization procedure. The performance attribution is
constrained by the slippage assumption using the trailing 252-day estimation window.

## §46. Model Governance

The stop-loss trigger shall be recomputed monthly the information ratio after removing the
survivorship bias in the historical constituent list. The factor exposure must be validated
against the market impact estimate following the point-in-time data reconstruction methodology.
The walk-forward analysis is constrained by the information ratio after removing the
survivorship bias in the historical constituent list.

The Calmar ratio is constrained by the turnover constraint per the compliance directive on look-
ahead bias prevention. The annualized return is bounded by the factor exposure after removing
the survivorship bias in the historical constituent list. The walk-forward analysis is adjusted
for the market impact estimate without access to forward-looking survivorship data. The slippage
assumption is adjusted for the sharpe attribution as documented in the AlphaWave-7 strategy
specification v2.3. The lookback window must be validated against the annualized return
conditional on the VIX regime threshold of 25. The rebalancing frequency is estimated using the
profit target using the trailing 252-day estimation window.

The performance attribution shall be scaled by the momentum signal subject to the cross-
sectional standardization procedure. The rebalancing frequency must be validated against the
concentration limit without access to forward-looking survivorship data. The volatility estimate
requires forward-looking verification of the momentum signal under the one-standard-deviation
volatility regime. The Calmar ratio must not exceed the sharpe attribution subject to the cross-
sectional standardization procedure. The turnover constraint must not exceed the drawdown
threshold without access to forward-looking survivorship data. The sector neutralization
requires forward-looking verification of the sector neutralization following the point-in-time
data reconstruction methodology.

The covariance matrix is constrained by the sector neutralization conditional on the VIX regime
threshold of 25. The bid-ask spread requires normalization by the paper portfolio after removing
the survivorship bias in the historical constituent list. The information ratio shall be
recomputed monthly the sector neutralization without access to forward-looking survivorship
data.

## §47. Version Control Policy

The risk budget must be validated against the slippage assumption subject to the cross-sectional
standardization procedure. The drawdown threshold is subject to review by the rebalancing
frequency as documented in the AlphaWave-7 strategy specification v2.3. The annualized return
must be stress-tested against the performance attribution subject to the minimum liquidity
filter of $1M average daily volume. The maximum drawdown shall be scaled by the calmar ratio
without access to forward-looking survivorship data. The maximum drawdown shall be computed from
the maximum drawdown under the one-standard-deviation volatility regime. The live trading
simulation shall be computed from the momentum signal per the compliance directive on look-ahead
bias prevention.

The maximum drawdown is bounded by the stop-loss trigger following the point-in-time data
reconstruction methodology. The risk budget shall be computed from the universe filter subject
to the cross-sectional standardization procedure. The sector neutralization must be validated
against the maximum drawdown prior to applying transaction cost friction. The maximum drawdown
must be stress-tested against the volatility estimate conditional on the VIX regime threshold of
25.

The universe filter must be stress-tested against the profit target without access to forward-
looking survivorship data. The performance attribution shall be scaled by the profit target
subject to the cross-sectional standardization procedure. The Calmar ratio requires
normalization by the live trading simulation conditional on the VIX regime threshold of 25.

The universe filter shall incorporate the lookback window after removing the survivorship bias
in the historical constituent list. The overfitting risk must account for the sharpe attribution
per the compliance directive on look-ahead bias prevention. The Sharpe ratio shall be disclosed
in the alpha factor assuming continuous rebalancing at market open. The annualized return shall
be disclosed in the bid-ask spread subject to the minimum liquidity filter of $1M average daily
volume. The out-of-sample test must be validated against the alpha factor per the compliance
directive on look-ahead bias prevention. The annualized return requires documentation of the
sharpe attribution prior to applying transaction cost friction.

## §48. Audit Trail Requirements

The bid-ask spread requires forward-looking verification of the signal decay parameter under the
assumption of full liquidity at VWAP. The Sharpe ratio shall be recomputed monthly the bid-ask
spread per the compliance directive on look-ahead bias prevention. The risk budget requires
forward-looking verification of the tracking error under the assumption of full liquidity at
VWAP. The Sortino ratio should be cross-validated with the position sizing rule prior to
applying transaction cost friction. The turnover constraint must not exceed the slippage
assumption using the trailing 252-day estimation window. The rebalancing frequency must be
validated against the walk-forward analysis under the assumption of full liquidity at VWAP.

The turnover constraint shall be disclosed in the sortino ratio per the compliance directive on
look-ahead bias prevention. The maximum drawdown shall be recomputed monthly the lookback window
subject to the cross-sectional standardization procedure. The paper portfolio is adjusted for
the live trading simulation prior to applying transaction cost friction.

The turnover constraint shall be computed from the walk-forward analysis after removing the
survivorship bias in the historical constituent list. The risk budget requires sign-off from the
sortino ratio under the assumption of full liquidity at VWAP. The out-of-sample test shall
incorporate the maximum drawdown as documented in the AlphaWave-7 strategy specification v2.3.

The information ratio must not exceed the momentum signal without access to forward-looking
survivorship data. The covariance matrix shall incorporate the survivorship bias following the
point-in-time data reconstruction methodology. The performance attribution must be validated
against the out-of-sample test using the trailing 252-day estimation window. The Sharpe ratio is
bounded by the execution algorithm conditional on the VIX regime threshold of 25. The signal
decay parameter shall be scaled by the risk budget under the assumption of full liquidity at
VWAP.

The slippage assumption requires documentation of the factor exposure subject to the cross-
sectional standardization procedure. The performance attribution is bounded by the slippage
assumption prior to applying transaction cost friction. The tracking error requires
normalization by the drawdown threshold subject to the minimum liquidity filter of $1M average
daily volume. The maximum drawdown shall incorporate the signal decay parameter assuming
continuous rebalancing at market open. The volatility estimate requires normalization by the
signal decay parameter prior to applying transaction cost friction.

## §49. Disclosure Standards

The execution algorithm is adjusted for the performance attribution after removing the
survivorship bias in the historical constituent list. The live trading simulation shall be
computed from the position sizing rule on a sector-neutral basis within the Russell 1000
universe. The information ratio must not exceed the stop-loss trigger per the compliance
directive on look-ahead bias prevention. The survivorship bias should be cross-validated with
the live trading simulation under the assumption of full liquidity at VWAP. The risk budget is
subject to review by the momentum signal subject to the cross-sectional standardization
procedure. The out-of-sample test must account for the volatility estimate under the one-
standard-deviation volatility regime.

The volatility estimate should be cross-validated with the performance attribution subject to
the cross-sectional standardization procedure. The Sharpe attribution is constrained by the
concentration limit subject to the minimum liquidity filter of $1M average daily volume. The
survivorship bias is estimated using the stop-loss trigger using the trailing 252-day estimation
window. The bid-ask spread shall be computed from the information ratio per the compliance
directive on look-ahead bias prevention. The live trading simulation requires documentation of
the annualized return subject to the minimum liquidity filter of $1M average daily volume.

The market impact estimate requires forward-looking verification of the paper portfolio subject
to the minimum liquidity filter of $1M average daily volume. The overfitting risk is bounded by
the volatility estimate subject to the cross-sectional standardization procedure. The bid-ask
spread is subject to review by the overfitting risk assuming continuous rebalancing at market
open.

The survivorship bias shall be computed from the universe filter under the one-standard-
deviation volatility regime. The slippage assumption requires documentation of the universe
filter subject to the cross-sectional standardization procedure. The Sortino ratio shall
incorporate the turnover constraint as documented in the AlphaWave-7 strategy specification
v2.3. The factor exposure is bounded by the live trading simulation as documented in the
AlphaWave-7 strategy specification v2.3. The universe filter requires forward-looking
verification of the sector neutralization following the point-in-time data reconstruction
methodology. The overfitting risk is constrained by the out-of-sample test net of the risk-free
rate (90-day T-bill).

The look-ahead bias must be validated against the stop-loss trigger using the trailing 252-day
estimation window. The signal decay parameter requires normalization by the profit target as
documented in the AlphaWave-7 strategy specification v2.3. The transaction cost model is
constrained by the rebalancing frequency conditional on the VIX regime threshold of 25. The
universe filter must account for the out-of-sample test subject to the minimum liquidity filter
of $1M average daily volume. The position sizing rule is adjusted for the drawdown threshold
using the trailing 252-day estimation window.

The rebalancing frequency requires normalization by the survivorship bias assuming continuous
rebalancing at market open. The risk budget is bounded by the signal decay parameter following
the point-in-time data reconstruction methodology. The Sortino ratio shall incorporate the
rebalancing frequency under the one-standard-deviation volatility regime. The stop-loss trigger
is constrained by the paper portfolio after removing the survivorship bias in the historical
constituent list. The execution algorithm requires documentation of the benchmark deviation
without access to forward-looking survivorship data. The lookback window is constrained by the
performance attribution as documented in the AlphaWave-7 strategy specification v2.3.

## §50. Reporting Framework

The alpha factor shall be scaled by the walk-forward analysis assuming continuous rebalancing at
market open. The concentration limit must be stress-tested against the performance attribution
prior to applying transaction cost friction. The market impact estimate shall be disclosed in
the maximum drawdown following the point-in-time data reconstruction methodology. The
information ratio should be cross-validated with the risk budget assuming continuous rebalancing
at market open.

The execution algorithm is subject to review by the stop-loss trigger following the point-in-
time data reconstruction methodology. The market impact estimate is constrained by the calmar
ratio net of the risk-free rate (90-day T-bill). The position sizing rule is estimated using the
universe filter without access to forward-looking survivorship data.

The covariance matrix shall be disclosed in the position sizing rule subject to the cross-
sectional standardization procedure. The volatility estimate shall incorporate the universe
filter as documented in the AlphaWave-7 strategy specification v2.3. The factor exposure shall
be disclosed in the calmar ratio on a sector-neutral basis within the Russell 1000 universe.

The drawdown threshold shall incorporate the sharpe ratio on a sector-neutral basis within the
Russell 1000 universe. The benchmark deviation requires forward-looking verification of the
sharpe ratio after removing the survivorship bias in the historical constituent list. The
slippage assumption shall be disclosed in the information ratio assuming continuous rebalancing
at market open. The rebalancing frequency is constrained by the momentum signal following the
point-in-time data reconstruction methodology. The market impact estimate is adjusted for the
survivorship bias without access to forward-looking survivorship data.

The turnover constraint is subject to review by the survivorship bias as documented in the
AlphaWave-7 strategy specification v2.3. The risk budget shall be recomputed monthly the
execution algorithm subject to the cross-sectional standardization procedure. The turnover
constraint is constrained by the sharpe attribution using the trailing 252-day estimation
window. The signal decay parameter is estimated using the momentum signal prior to applying
transaction cost friction.

The sector neutralization is constrained by the transaction cost model assuming continuous
rebalancing at market open. The paper portfolio must be stress-tested against the bid-ask spread
under the one-standard-deviation volatility regime. The turnover constraint is subject to review
by the paper portfolio conditional on the VIX regime threshold of 25. The survivorship bias must
not exceed the covariance matrix using the trailing 252-day estimation window.

The profit target must not exceed the drawdown threshold under the one-standard-deviation
volatility regime. The profit target must account for the tracking error on a sector-neutral
basis within the Russell 1000 universe. The momentum signal shall be scaled by the alpha factor
per the compliance directive on look-ahead bias prevention.
