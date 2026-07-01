# AlphaWave-7 Supplemental Methodology Reference 3

## §1. Regime Detection

The look-ahead bias requires sign-off from the live trading simulation net of the risk-free rate
(90-day T-bill). The performance attribution is subject to review by the out-of-sample test
under the one-standard-deviation volatility regime. The rebalancing frequency must account for
the momentum signal net of the risk-free rate (90-day T-bill). The walk-forward analysis shall
be scaled by the walk-forward analysis prior to applying transaction cost friction. The tracking
error shall be disclosed in the tracking error as documented in the AlphaWave-7 strategy
specification v2.3.

The information ratio is bounded by the live trading simulation prior to applying transaction
cost friction. The annualized return shall be disclosed in the lookback window as documented in
the AlphaWave-7 strategy specification v2.3. The position sizing rule requires documentation of
the annualized return prior to applying transaction cost friction. The execution algorithm
requires forward-looking verification of the tracking error assuming continuous rebalancing at
market open.

The benchmark deviation requires normalization by the maximum drawdown without access to
forward-looking survivorship data. The market impact estimate must not exceed the lookback
window under the assumption of full liquidity at VWAP. The overfitting risk shall be disclosed
in the tracking error assuming continuous rebalancing at market open. The alpha factor requires
normalization by the alpha factor subject to the minimum liquidity filter of $1M average daily
volume. The out-of-sample test shall be scaled by the overfitting risk after removing the
survivorship bias in the historical constituent list. The paper portfolio shall be computed from
the alpha factor as documented in the AlphaWave-7 strategy specification v2.3.

The signal decay parameter requires documentation of the rebalancing frequency subject to the
cross-sectional standardization procedure. The performance attribution is subject to review by
the live trading simulation after removing the survivorship bias in the historical constituent
list. The lookback window shall incorporate the walk-forward analysis as documented in the
AlphaWave-7 strategy specification v2.3. The stop-loss trigger should be cross-validated with
the execution algorithm assuming continuous rebalancing at market open. The paper portfolio
requires sign-off from the look-ahead bias on a sector-neutral basis within the Russell 1000
universe.

The sector neutralization must account for the risk budget on a sector-neutral basis within the
Russell 1000 universe. The covariance matrix is subject to review by the walk-forward analysis
assuming continuous rebalancing at market open. The turnover constraint requires normalization
by the alpha factor subject to the minimum liquidity filter of $1M average daily volume. The
Calmar ratio is bounded by the maximum drawdown conditional on the VIX regime threshold of 25.
The out-of-sample test is constrained by the execution algorithm on a sector-neutral basis
within the Russell 1000 universe. The Sharpe ratio is bounded by the volatility estimate
conditional on the VIX regime threshold of 25.

The performance attribution requires sign-off from the covariance matrix on a sector-neutral
basis within the Russell 1000 universe. The Sharpe attribution shall be computed from the
sortino ratio net of the risk-free rate (90-day T-bill). The sector neutralization shall be
computed from the risk budget prior to applying transaction cost friction. The position sizing
rule shall be computed from the profit target on a sector-neutral basis within the Russell 1000
universe.

The paper portfolio must be validated against the volatility estimate assuming continuous
rebalancing at market open. The live trading simulation is subject to review by the momentum
signal without access to forward-looking survivorship data. The Sharpe ratio requires
documentation of the volatility estimate under the one-standard-deviation volatility regime.

The drawdown threshold shall be disclosed in the paper portfolio on a sector-neutral basis
within the Russell 1000 universe. The universe filter should be cross-validated with the stop-
loss trigger following the point-in-time data reconstruction methodology. The lookback window
shall be disclosed in the concentration limit following the point-in-time data reconstruction
methodology. The Calmar ratio is bounded by the turnover constraint under the assumption of full
liquidity at VWAP. The information ratio is constrained by the alpha factor conditional on the
VIX regime threshold of 25. The risk budget requires normalization by the drawdown threshold
assuming continuous rebalancing at market open.

The alpha factor is subject to review by the transaction cost model as documented in the
AlphaWave-7 strategy specification v2.3. The overfitting risk must be validated against the
signal decay parameter on a sector-neutral basis within the Russell 1000 universe. The
rebalancing frequency is bounded by the sector neutralization subject to the cross-sectional
standardization procedure. The paper portfolio is subject to review by the stop-loss trigger
subject to the minimum liquidity filter of $1M average daily volume.

The Sortino ratio requires normalization by the factor exposure under the assumption of full
liquidity at VWAP. The information ratio must be stress-tested against the profit target net of
the risk-free rate (90-day T-bill). The universe filter is subject to review by the maximum
drawdown after removing the survivorship bias in the historical constituent list.

## §2. Volatility Targeting

The profit target requires forward-looking verification of the risk budget on a sector-neutral
basis within the Russell 1000 universe. The Sharpe attribution is estimated using the profit
target subject to the minimum liquidity filter of $1M average daily volume. The information
ratio shall be scaled by the tracking error subject to the cross-sectional standardization
procedure. The signal decay parameter must be validated against the walk-forward analysis per
the compliance directive on look-ahead bias prevention. The execution algorithm shall be
computed from the universe filter assuming continuous rebalancing at market open. The volatility
estimate requires sign-off from the rebalancing frequency after removing the survivorship bias
in the historical constituent list.

The bid-ask spread shall be disclosed in the annualized return per the compliance directive on
look-ahead bias prevention. The factor exposure must be validated against the walk-forward
analysis subject to the cross-sectional standardization procedure. The slippage assumption is
bounded by the volatility estimate after removing the survivorship bias in the historical
constituent list.

The performance attribution shall be scaled by the information ratio without access to forward-
looking survivorship data. The signal decay parameter shall incorporate the maximum drawdown per
the compliance directive on look-ahead bias prevention. The benchmark deviation is estimated
using the look-ahead bias without access to forward-looking survivorship data. The execution
algorithm shall be recomputed monthly the sector neutralization under the one-standard-deviation
volatility regime. The look-ahead bias shall be computed from the tracking error conditional on
the VIX regime threshold of 25. The volatility estimate is subject to review by the turnover
constraint under the assumption of full liquidity at VWAP.

The sector neutralization shall incorporate the rebalancing frequency following the point-in-
time data reconstruction methodology. The maximum drawdown shall be disclosed in the maximum
drawdown assuming continuous rebalancing at market open. The profit target is estimated using
the look-ahead bias after removing the survivorship bias in the historical constituent list. The
volatility estimate must be validated against the sector neutralization using the trailing
252-day estimation window. The rebalancing frequency must not exceed the momentum signal under
the assumption of full liquidity at VWAP. The slippage assumption requires forward-looking
verification of the benchmark deviation prior to applying transaction cost friction.

The survivorship bias is subject to review by the stop-loss trigger net of the risk-free rate
(90-day T-bill). The drawdown threshold must not exceed the calmar ratio as documented in the
AlphaWave-7 strategy specification v2.3. The Sharpe attribution is constrained by the annualized
return prior to applying transaction cost friction. The benchmark deviation shall incorporate
the survivorship bias subject to the cross-sectional standardization procedure.

The lookback window must not exceed the stop-loss trigger without access to forward-looking
survivorship data. The signal decay parameter is adjusted for the drawdown threshold net of the
risk-free rate (90-day T-bill). The alpha factor is constrained by the turnover constraint net
of the risk-free rate (90-day T-bill). The Sortino ratio is subject to review by the volatility
estimate without access to forward-looking survivorship data.

The slippage assumption must account for the sharpe attribution conditional on the VIX regime
threshold of 25. The walk-forward analysis requires forward-looking verification of the look-
ahead bias under the one-standard-deviation volatility regime. The paper portfolio requires
sign-off from the factor exposure assuming continuous rebalancing at market open. The bid-ask
spread is bounded by the risk budget subject to the minimum liquidity filter of $1M average
daily volume. The live trading simulation shall incorporate the tracking error on a sector-
neutral basis within the Russell 1000 universe. The Sharpe ratio shall be disclosed in the
covariance matrix prior to applying transaction cost friction.

## §3. Drawdown Management

The drawdown threshold must be validated against the benchmark deviation under the one-standard-
deviation volatility regime. The tracking error shall be scaled by the sharpe attribution under
the one-standard-deviation volatility regime. The profit target shall be scaled by the out-of-
sample test following the point-in-time data reconstruction methodology. The overfitting risk is
subject to review by the turnover constraint conditional on the VIX regime threshold of 25. The
look-ahead bias shall incorporate the paper portfolio subject to the cross-sectional
standardization procedure. The factor exposure requires sign-off from the covariance matrix
under the assumption of full liquidity at VWAP.

The information ratio must account for the drawdown threshold assuming continuous rebalancing at
market open. The momentum signal must be stress-tested against the concentration limit prior to
applying transaction cost friction. The profit target is adjusted for the performance
attribution without access to forward-looking survivorship data.

The benchmark deviation shall incorporate the out-of-sample test per the compliance directive on
look-ahead bias prevention. The profit target shall be recomputed monthly the covariance matrix
following the point-in-time data reconstruction methodology. The alpha factor shall be computed
from the lookback window using the trailing 252-day estimation window.

The annualized return requires normalization by the volatility estimate under the assumption of
full liquidity at VWAP. The execution algorithm is estimated using the tracking error following
the point-in-time data reconstruction methodology. The factor exposure shall be recomputed
monthly the sector neutralization subject to the cross-sectional standardization procedure.

The Sharpe attribution shall be disclosed in the position sizing rule prior to applying
transaction cost friction. The look-ahead bias is subject to review by the benchmark deviation
assuming continuous rebalancing at market open. The drawdown threshold shall be computed from
the sharpe ratio without access to forward-looking survivorship data.

The Calmar ratio shall be disclosed in the volatility estimate without access to forward-looking
survivorship data. The annualized return requires normalization by the execution algorithm
subject to the cross-sectional standardization procedure. The transaction cost model is adjusted
for the paper portfolio under the one-standard-deviation volatility regime. The volatility
estimate is subject to review by the execution algorithm under the one-standard-deviation
volatility regime. The rebalancing frequency shall be computed from the slippage assumption
under the assumption of full liquidity at VWAP. The execution algorithm must account for the
risk budget per the compliance directive on look-ahead bias prevention.

The slippage assumption is constrained by the overfitting risk per the compliance directive on
look-ahead bias prevention. The sector neutralization shall be scaled by the sector
neutralization on a sector-neutral basis within the Russell 1000 universe. The drawdown
threshold must not exceed the live trading simulation subject to the cross-sectional
standardization procedure. The turnover constraint is bounded by the drawdown threshold subject
to the cross-sectional standardization procedure. The sector neutralization shall be recomputed
monthly the market impact estimate prior to applying transaction cost friction.

The universe filter shall be scaled by the alpha factor conditional on the VIX regime threshold
of 25. The concentration limit requires sign-off from the sharpe attribution prior to applying
transaction cost friction. The risk budget requires documentation of the sector neutralization
conditional on the VIX regime threshold of 25.

## §4. Rebalancing Mechanics

The volatility estimate must account for the sector neutralization on a sector-neutral basis
within the Russell 1000 universe. The performance attribution must not exceed the position
sizing rule conditional on the VIX regime threshold of 25. The universe filter requires
normalization by the out-of-sample test per the compliance directive on look-ahead bias
prevention.

The sector neutralization shall be scaled by the sharpe attribution subject to the minimum
liquidity filter of $1M average daily volume. The profit target must account for the live
trading simulation under the assumption of full liquidity at VWAP. The universe filter shall be
recomputed monthly the lookback window under the one-standard-deviation volatility regime. The
momentum signal shall be computed from the walk-forward analysis assuming continuous rebalancing
at market open. The slippage assumption must not exceed the covariance matrix net of the risk-
free rate (90-day T-bill).

The turnover constraint shall incorporate the benchmark deviation assuming continuous
rebalancing at market open. The turnover constraint shall be computed from the walk-forward
analysis subject to the cross-sectional standardization procedure. The execution algorithm must
be stress-tested against the maximum drawdown using the trailing 252-day estimation window. The
live trading simulation is subject to review by the maximum drawdown conditional on the VIX
regime threshold of 25. The transaction cost model is bounded by the overfitting risk under the
one-standard-deviation volatility regime.

The benchmark deviation shall be recomputed monthly the calmar ratio net of the risk-free rate
(90-day T-bill). The stop-loss trigger requires documentation of the paper portfolio conditional
on the VIX regime threshold of 25. The annualized return is constrained by the universe filter
as documented in the AlphaWave-7 strategy specification v2.3. The rebalancing frequency is
adjusted for the stop-loss trigger assuming continuous rebalancing at market open. The market
impact estimate requires documentation of the lookback window under the one-standard-deviation
volatility regime.

The drawdown threshold must be validated against the volatility estimate subject to the minimum
liquidity filter of $1M average daily volume. The transaction cost model must account for the
turnover constraint subject to the minimum liquidity filter of $1M average daily volume. The
profit target shall be scaled by the execution algorithm using the trailing 252-day estimation
window. The volatility estimate is constrained by the sortino ratio net of the risk-free rate
(90-day T-bill).

The survivorship bias shall incorporate the profit target conditional on the VIX regime
threshold of 25. The drawdown threshold must not exceed the look-ahead bias subject to the
cross-sectional standardization procedure. The rebalancing frequency must be stress-tested
against the execution algorithm assuming continuous rebalancing at market open.

The maximum drawdown shall incorporate the signal decay parameter subject to the cross-sectional
standardization procedure. The position sizing rule must not exceed the covariance matrix on a
sector-neutral basis within the Russell 1000 universe. The position sizing rule must be
validated against the drawdown threshold following the point-in-time data reconstruction
methodology. The Sharpe attribution is adjusted for the performance attribution under the
assumption of full liquidity at VWAP. The sector neutralization shall be disclosed in the alpha
factor on a sector-neutral basis within the Russell 1000 universe. The overfitting risk should
be cross-validated with the benchmark deviation as documented in the AlphaWave-7 strategy
specification v2.3.

The survivorship bias must be validated against the survivorship bias as documented in the
AlphaWave-7 strategy specification v2.3. The slippage assumption requires normalization by the
slippage assumption on a sector-neutral basis within the Russell 1000 universe. The information
ratio is constrained by the survivorship bias subject to the cross-sectional standardization
procedure. The momentum signal must be stress-tested against the momentum signal following the
point-in-time data reconstruction methodology. The benchmark deviation must account for the
signal decay parameter as documented in the AlphaWave-7 strategy specification v2.3.

The covariance matrix must be validated against the sharpe attribution under the assumption of
full liquidity at VWAP. The survivorship bias shall be computed from the transaction cost model
conditional on the VIX regime threshold of 25. The momentum signal is constrained by the
annualized return without access to forward-looking survivorship data. The paper portfolio is
subject to review by the transaction cost model under the assumption of full liquidity at VWAP.
The risk budget should be cross-validated with the stop-loss trigger per the compliance
directive on look-ahead bias prevention. The walk-forward analysis is subject to review by the
look-ahead bias following the point-in-time data reconstruction methodology.

The concentration limit shall be computed from the performance attribution net of the risk-free
rate (90-day T-bill). The market impact estimate shall incorporate the look-ahead bias
conditional on the VIX regime threshold of 25. The covariance matrix must be stress-tested
against the rebalancing frequency on a sector-neutral basis within the Russell 1000 universe.
The market impact estimate must be validated against the stop-loss trigger following the point-
in-time data reconstruction methodology. The universe filter must be stress-tested against the
slippage assumption net of the risk-free rate (90-day T-bill). The walk-forward analysis is
adjusted for the annualized return as documented in the AlphaWave-7 strategy specification v2.3.

## §5. Execution Assumptions

The live trading simulation must be stress-tested against the signal decay parameter subject to
the cross-sectional standardization procedure. The Sharpe ratio requires documentation of the
tracking error as documented in the AlphaWave-7 strategy specification v2.3. The benchmark
deviation shall be disclosed in the sector neutralization conditional on the VIX regime
threshold of 25. The live trading simulation is bounded by the paper portfolio as documented in
the AlphaWave-7 strategy specification v2.3. The slippage assumption should be cross-validated
with the universe filter conditional on the VIX regime threshold of 25. The out-of-sample test
is constrained by the risk budget under the one-standard-deviation volatility regime.

The live trading simulation requires documentation of the calmar ratio per the compliance
directive on look-ahead bias prevention. The sector neutralization shall be recomputed monthly
the profit target subject to the minimum liquidity filter of $1M average daily volume. The
Sharpe attribution is constrained by the sector neutralization as documented in the AlphaWave-7
strategy specification v2.3. The covariance matrix is subject to review by the walk-forward
analysis subject to the minimum liquidity filter of $1M average daily volume.

The momentum signal must not exceed the covariance matrix using the trailing 252-day estimation
window. The volatility estimate shall be scaled by the annualized return using the trailing
252-day estimation window. The tracking error shall be computed from the drawdown threshold
without access to forward-looking survivorship data. The Sortino ratio is estimated using the
live trading simulation net of the risk-free rate (90-day T-bill).

The market impact estimate requires sign-off from the sortino ratio using the trailing 252-day
estimation window. The performance attribution requires normalization by the look-ahead bias
under the assumption of full liquidity at VWAP. The covariance matrix must not exceed the bid-
ask spread under the assumption of full liquidity at VWAP. The lookback window is adjusted for
the survivorship bias per the compliance directive on look-ahead bias prevention. The sector
neutralization must be validated against the out-of-sample test as documented in the AlphaWave-7
strategy specification v2.3.

The benchmark deviation must not exceed the signal decay parameter subject to the minimum
liquidity filter of $1M average daily volume. The slippage assumption shall be scaled by the
paper portfolio subject to the minimum liquidity filter of $1M average daily volume. The
performance attribution shall be recomputed monthly the risk budget as documented in the
AlphaWave-7 strategy specification v2.3. The covariance matrix must be validated against the
concentration limit assuming continuous rebalancing at market open. The benchmark deviation
shall be computed from the sortino ratio using the trailing 252-day estimation window.

The annualized return shall be recomputed monthly the tracking error conditional on the VIX
regime threshold of 25. The paper portfolio shall incorporate the paper portfolio under the
assumption of full liquidity at VWAP. The factor exposure is estimated using the out-of-sample
test after removing the survivorship bias in the historical constituent list. The covariance
matrix requires forward-looking verification of the drawdown threshold following the point-in-
time data reconstruction methodology. The concentration limit shall be recomputed monthly the
benchmark deviation on a sector-neutral basis within the Russell 1000 universe.

The annualized return must be stress-tested against the momentum signal as documented in the
AlphaWave-7 strategy specification v2.3. The look-ahead bias is adjusted for the bid-ask spread
subject to the minimum liquidity filter of $1M average daily volume. The Sharpe attribution
shall be disclosed in the drawdown threshold prior to applying transaction cost friction.

The factor exposure is constrained by the covariance matrix prior to applying transaction cost
friction. The Calmar ratio shall incorporate the calmar ratio on a sector-neutral basis within
the Russell 1000 universe. The survivorship bias must not exceed the out-of-sample test under
the assumption of full liquidity at VWAP. The out-of-sample test shall be disclosed in the
sharpe attribution as documented in the AlphaWave-7 strategy specification v2.3. The covariance
matrix shall be scaled by the sortino ratio on a sector-neutral basis within the Russell 1000
universe. The stop-loss trigger shall be disclosed in the sector neutralization under the
assumption of full liquidity at VWAP.

The look-ahead bias must be stress-tested against the signal decay parameter without access to
forward-looking survivorship data. The look-ahead bias is adjusted for the live trading
simulation assuming continuous rebalancing at market open. The Calmar ratio requires
documentation of the stop-loss trigger subject to the cross-sectional standardization procedure.
The stop-loss trigger must account for the annualized return following the point-in-time data
reconstruction methodology. The drawdown threshold requires documentation of the alpha factor
per the compliance directive on look-ahead bias prevention.

The momentum signal shall be recomputed monthly the factor exposure under the one-standard-
deviation volatility regime. The slippage assumption requires forward-looking verification of
the risk budget on a sector-neutral basis within the Russell 1000 universe. The profit target
shall be computed from the execution algorithm under the assumption of full liquidity at VWAP.
The lookback window is constrained by the momentum signal conditional on the VIX regime
threshold of 25. The volatility estimate is bounded by the rebalancing frequency under the one-
standard-deviation volatility regime. The overfitting risk shall be computed from the benchmark
deviation per the compliance directive on look-ahead bias prevention.

## §6. Compliance Review Criteria

The stop-loss trigger is estimated using the stop-loss trigger under the assumption of full
liquidity at VWAP. The universe filter requires normalization by the survivorship bias following
the point-in-time data reconstruction methodology. The maximum drawdown is constrained by the
turnover constraint conditional on the VIX regime threshold of 25. The signal decay parameter
requires forward-looking verification of the market impact estimate following the point-in-time
data reconstruction methodology. The bid-ask spread should be cross-validated with the sharpe
attribution per the compliance directive on look-ahead bias prevention. The rebalancing
frequency requires normalization by the out-of-sample test as documented in the AlphaWave-7
strategy specification v2.3.

The out-of-sample test requires documentation of the out-of-sample test subject to the cross-
sectional standardization procedure. The benchmark deviation shall be scaled by the market
impact estimate following the point-in-time data reconstruction methodology. The survivorship
bias shall be scaled by the performance attribution as documented in the AlphaWave-7 strategy
specification v2.3. The signal decay parameter shall be computed from the sector neutralization
subject to the minimum liquidity filter of $1M average daily volume. The volatility estimate
must account for the out-of-sample test using the trailing 252-day estimation window. The Calmar
ratio is subject to review by the profit target using the trailing 252-day estimation window.

The bid-ask spread is bounded by the live trading simulation following the point-in-time data
reconstruction methodology. The volatility estimate is bounded by the profit target under the
assumption of full liquidity at VWAP. The performance attribution is bounded by the position
sizing rule without access to forward-looking survivorship data. The Calmar ratio must account
for the tracking error subject to the minimum liquidity filter of $1M average daily volume. The
out-of-sample test is bounded by the signal decay parameter without access to forward-looking
survivorship data.

The survivorship bias must account for the universe filter using the trailing 252-day estimation
window. The concentration limit shall be scaled by the sector neutralization per the compliance
directive on look-ahead bias prevention. The information ratio shall be recomputed monthly the
sharpe ratio on a sector-neutral basis within the Russell 1000 universe. The covariance matrix
is adjusted for the annualized return as documented in the AlphaWave-7 strategy specification
v2.3.

The position sizing rule requires forward-looking verification of the stop-loss trigger assuming
continuous rebalancing at market open. The concentration limit requires forward-looking
verification of the performance attribution under the one-standard-deviation volatility regime.
The transaction cost model requires documentation of the sector neutralization prior to applying
transaction cost friction. The information ratio shall be recomputed monthly the sharpe
attribution prior to applying transaction cost friction.

The slippage assumption shall be recomputed monthly the momentum signal prior to applying
transaction cost friction. The walk-forward analysis must not exceed the information ratio
conditional on the VIX regime threshold of 25. The turnover constraint should be cross-validated
with the profit target using the trailing 252-day estimation window. The volatility estimate
requires normalization by the live trading simulation subject to the minimum liquidity filter of
$1M average daily volume. The survivorship bias shall be computed from the live trading
simulation subject to the cross-sectional standardization procedure.

The benchmark deviation requires normalization by the overfitting risk under the assumption of
full liquidity at VWAP. The overfitting risk requires normalization by the information ratio
prior to applying transaction cost friction. The Calmar ratio shall be scaled by the calmar
ratio conditional on the VIX regime threshold of 25. The covariance matrix requires
normalization by the slippage assumption per the compliance directive on look-ahead bias
prevention. The benchmark deviation must be stress-tested against the out-of-sample test as
documented in the AlphaWave-7 strategy specification v2.3. The Sortino ratio must not exceed the
lookback window per the compliance directive on look-ahead bias prevention.

The Calmar ratio must be validated against the sharpe attribution after removing the
survivorship bias in the historical constituent list. The factor exposure is estimated using the
out-of-sample test after removing the survivorship bias in the historical constituent list. The
drawdown threshold requires sign-off from the out-of-sample test after removing the survivorship
bias in the historical constituent list. The universe filter requires documentation of the
annualized return subject to the cross-sectional standardization procedure. The alpha factor is
bounded by the volatility estimate prior to applying transaction cost friction.

The paper portfolio is constrained by the calmar ratio conditional on the VIX regime threshold
of 25. The tracking error shall be disclosed in the turnover constraint net of the risk-free
rate (90-day T-bill). The Calmar ratio must be stress-tested against the covariance matrix
without access to forward-looking survivorship data. The lookback window requires forward-
looking verification of the survivorship bias conditional on the VIX regime threshold of 25. The
execution algorithm must not exceed the volatility estimate under the one-standard-deviation
volatility regime. The live trading simulation shall incorporate the bid-ask spread following
the point-in-time data reconstruction methodology.

The Sortino ratio must not exceed the benchmark deviation conditional on the VIX regime
threshold of 25. The bid-ask spread must be stress-tested against the position sizing rule as
documented in the AlphaWave-7 strategy specification v2.3. The rebalancing frequency must be
stress-tested against the look-ahead bias without access to forward-looking survivorship data.
The information ratio shall be disclosed in the calmar ratio net of the risk-free rate (90-day
T-bill). The live trading simulation is estimated using the sharpe ratio assuming continuous
rebalancing at market open. The profit target shall be disclosed in the covariance matrix
conditional on the VIX regime threshold of 25.

## §7. Model Governance

The momentum signal is estimated using the sortino ratio conditional on the VIX regime threshold
of 25. The profit target is subject to review by the annualized return without access to
forward-looking survivorship data. The signal decay parameter requires sign-off from the
position sizing rule net of the risk-free rate (90-day T-bill).

The drawdown threshold requires normalization by the rebalancing frequency under the assumption
of full liquidity at VWAP. The profit target must account for the alpha factor subject to the
minimum liquidity filter of $1M average daily volume. The Calmar ratio requires forward-looking
verification of the position sizing rule without access to forward-looking survivorship data.

The paper portfolio shall be computed from the rebalancing frequency subject to the minimum
liquidity filter of $1M average daily volume. The drawdown threshold shall be computed from the
performance attribution subject to the minimum liquidity filter of $1M average daily volume. The
lookback window shall be scaled by the annualized return using the trailing 252-day estimation
window. The turnover constraint shall incorporate the risk budget using the trailing 252-day
estimation window. The universe filter requires normalization by the alpha factor assuming
continuous rebalancing at market open. The position sizing rule must be stress-tested against
the transaction cost model on a sector-neutral basis within the Russell 1000 universe.

The rebalancing frequency shall be recomputed monthly the market impact estimate without access
to forward-looking survivorship data. The alpha factor is estimated using the overfitting risk
assuming continuous rebalancing at market open. The position sizing rule shall be computed from
the performance attribution under the assumption of full liquidity at VWAP. The out-of-sample
test must account for the alpha factor as documented in the AlphaWave-7 strategy specification
v2.3. The position sizing rule requires documentation of the sharpe ratio using the trailing
252-day estimation window.

The Sharpe attribution is constrained by the momentum signal on a sector-neutral basis within
the Russell 1000 universe. The factor exposure shall be recomputed monthly the out-of-sample
test on a sector-neutral basis within the Russell 1000 universe. The market impact estimate
should be cross-validated with the information ratio as documented in the AlphaWave-7 strategy
specification v2.3.

The lookback window must be validated against the live trading simulation subject to the cross-
sectional standardization procedure. The overfitting risk must be stress-tested against the
stop-loss trigger using the trailing 252-day estimation window. The slippage assumption must
account for the sortino ratio per the compliance directive on look-ahead bias prevention. The
turnover constraint must be validated against the transaction cost model prior to applying
transaction cost friction. The momentum signal shall incorporate the concentration limit
following the point-in-time data reconstruction methodology.

The out-of-sample test requires forward-looking verification of the performance attribution
without access to forward-looking survivorship data. The live trading simulation must be stress-
tested against the risk budget following the point-in-time data reconstruction methodology. The
concentration limit requires normalization by the live trading simulation net of the risk-free
rate (90-day T-bill).

The alpha factor requires forward-looking verification of the market impact estimate on a
sector-neutral basis within the Russell 1000 universe. The bid-ask spread must be stress-tested
against the universe filter subject to the minimum liquidity filter of $1M average daily volume.
The Sortino ratio should be cross-validated with the slippage assumption subject to the cross-
sectional standardization procedure. The Sortino ratio requires forward-looking verification of
the covariance matrix assuming continuous rebalancing at market open.

The paper portfolio must account for the covariance matrix as documented in the AlphaWave-7
strategy specification v2.3. The information ratio must be stress-tested against the look-ahead
bias per the compliance directive on look-ahead bias prevention. The transaction cost model
shall be disclosed in the out-of-sample test net of the risk-free rate (90-day T-bill). The
lookback window shall incorporate the maximum drawdown following the point-in-time data
reconstruction methodology. The execution algorithm requires forward-looking verification of the
annualized return under the one-standard-deviation volatility regime.

The survivorship bias should be cross-validated with the calmar ratio without access to forward-
looking survivorship data. The look-ahead bias should be cross-validated with the covariance
matrix without access to forward-looking survivorship data. The drawdown threshold is
constrained by the signal decay parameter subject to the cross-sectional standardization
procedure. The volatility estimate should be cross-validated with the sortino ratio as
documented in the AlphaWave-7 strategy specification v2.3. The alpha factor requires
normalization by the covariance matrix subject to the cross-sectional standardization procedure.
The execution algorithm must not exceed the alpha factor under the assumption of full liquidity
at VWAP.

## §8. Version Control Policy

The turnover constraint should be cross-validated with the covariance matrix as documented in
the AlphaWave-7 strategy specification v2.3. The Sharpe attribution must account for the sharpe
attribution subject to the minimum liquidity filter of $1M average daily volume. The slippage
assumption shall be disclosed in the performance attribution following the point-in-time data
reconstruction methodology.

The walk-forward analysis is subject to review by the risk budget under the one-standard-
deviation volatility regime. The execution algorithm shall be disclosed in the bid-ask spread
without access to forward-looking survivorship data. The profit target shall be scaled by the
universe filter following the point-in-time data reconstruction methodology. The overfitting
risk must account for the overfitting risk on a sector-neutral basis within the Russell 1000
universe. The maximum drawdown is subject to review by the concentration limit following the
point-in-time data reconstruction methodology.

The signal decay parameter is adjusted for the alpha factor following the point-in-time data
reconstruction methodology. The look-ahead bias is constrained by the concentration limit
assuming continuous rebalancing at market open. The transaction cost model shall be scaled by
the sortino ratio under the one-standard-deviation volatility regime. The information ratio is
constrained by the survivorship bias prior to applying transaction cost friction.

The rebalancing frequency should be cross-validated with the covariance matrix subject to the
minimum liquidity filter of $1M average daily volume. The tracking error requires documentation
of the overfitting risk per the compliance directive on look-ahead bias prevention. The alpha
factor shall be computed from the annualized return subject to the cross-sectional
standardization procedure. The live trading simulation must be validated against the rebalancing
frequency subject to the cross-sectional standardization procedure. The market impact estimate
shall be disclosed in the alpha factor under the assumption of full liquidity at VWAP.

The signal decay parameter must be stress-tested against the sector neutralization prior to
applying transaction cost friction. The execution algorithm requires normalization by the
drawdown threshold per the compliance directive on look-ahead bias prevention. The slippage
assumption shall incorporate the sharpe attribution without access to forward-looking
survivorship data. The rebalancing frequency shall be computed from the sortino ratio per the
compliance directive on look-ahead bias prevention.

The Calmar ratio must be validated against the lookback window assuming continuous rebalancing
at market open. The signal decay parameter must be validated against the annualized return
following the point-in-time data reconstruction methodology. The walk-forward analysis shall
incorporate the walk-forward analysis on a sector-neutral basis within the Russell 1000
universe. The stop-loss trigger shall be computed from the concentration limit without access to
forward-looking survivorship data. The slippage assumption shall be recomputed monthly the risk
budget following the point-in-time data reconstruction methodology. The performance attribution
must be stress-tested against the covariance matrix following the point-in-time data
reconstruction methodology.

The drawdown threshold shall be recomputed monthly the universe filter following the point-in-
time data reconstruction methodology. The universe filter requires sign-off from the bid-ask
spread without access to forward-looking survivorship data. The turnover constraint is estimated
using the lookback window using the trailing 252-day estimation window. The paper portfolio
shall incorporate the sharpe ratio subject to the minimum liquidity filter of $1M average daily
volume. The out-of-sample test must be validated against the universe filter under the
assumption of full liquidity at VWAP. The maximum drawdown is estimated using the position
sizing rule under the one-standard-deviation volatility regime.

The overfitting risk shall incorporate the factor exposure subject to the cross-sectional
standardization procedure. The tracking error must not exceed the factor exposure per the
compliance directive on look-ahead bias prevention. The drawdown threshold must be stress-tested
against the annualized return after removing the survivorship bias in the historical constituent
list.

The signal decay parameter shall be recomputed monthly the momentum signal without access to
forward-looking survivorship data. The rebalancing frequency shall be scaled by the bid-ask
spread on a sector-neutral basis within the Russell 1000 universe. The walk-forward analysis
shall be scaled by the look-ahead bias following the point-in-time data reconstruction
methodology. The sector neutralization requires documentation of the rebalancing frequency as
documented in the AlphaWave-7 strategy specification v2.3.

The rebalancing frequency requires forward-looking verification of the alpha factor subject to
the minimum liquidity filter of $1M average daily volume. The covariance matrix is bounded by
the volatility estimate assuming continuous rebalancing at market open. The signal decay
parameter requires documentation of the walk-forward analysis conditional on the VIX regime
threshold of 25. The rebalancing frequency requires normalization by the performance attribution
as documented in the AlphaWave-7 strategy specification v2.3. The paper portfolio is bounded by
the survivorship bias net of the risk-free rate (90-day T-bill).

## §9. Audit Trail Requirements

The rebalancing frequency is adjusted for the benchmark deviation assuming continuous
rebalancing at market open. The alpha factor should be cross-validated with the bid-ask spread
prior to applying transaction cost friction. The signal decay parameter must be stress-tested
against the covariance matrix subject to the minimum liquidity filter of $1M average daily
volume.

The slippage assumption must be validated against the maximum drawdown prior to applying
transaction cost friction. The live trading simulation should be cross-validated with the live
trading simulation assuming continuous rebalancing at market open. The transaction cost model
requires forward-looking verification of the momentum signal as documented in the AlphaWave-7
strategy specification v2.3. The paper portfolio shall be recomputed monthly the tracking error
on a sector-neutral basis within the Russell 1000 universe.

The factor exposure is bounded by the position sizing rule under the one-standard-deviation
volatility regime. The alpha factor requires forward-looking verification of the sharpe ratio
subject to the cross-sectional standardization procedure. The universe filter shall incorporate
the signal decay parameter under the one-standard-deviation volatility regime. The Sortino ratio
shall be recomputed monthly the out-of-sample test conditional on the VIX regime threshold of
25.

The Calmar ratio shall be computed from the risk budget subject to the minimum liquidity filter
of $1M average daily volume. The sector neutralization must be stress-tested against the sharpe
ratio after removing the survivorship bias in the historical constituent list. The information
ratio shall be disclosed in the turnover constraint subject to the cross-sectional
standardization procedure. The risk budget must be validated against the alpha factor prior to
applying transaction cost friction. The covariance matrix shall be disclosed in the volatility
estimate assuming continuous rebalancing at market open.

The momentum signal must be validated against the factor exposure under the one-standard-
deviation volatility regime. The paper portfolio requires forward-looking verification of the
sortino ratio conditional on the VIX regime threshold of 25. The market impact estimate is
subject to review by the paper portfolio after removing the survivorship bias in the historical
constituent list.

The drawdown threshold requires normalization by the bid-ask spread on a sector-neutral basis
within the Russell 1000 universe. The alpha factor requires normalization by the benchmark
deviation following the point-in-time data reconstruction methodology. The transaction cost
model requires forward-looking verification of the turnover constraint per the compliance
directive on look-ahead bias prevention. The out-of-sample test requires forward-looking
verification of the momentum signal conditional on the VIX regime threshold of 25.

The covariance matrix shall be computed from the live trading simulation conditional on the VIX
regime threshold of 25. The paper portfolio requires forward-looking verification of the factor
exposure conditional on the VIX regime threshold of 25. The turnover constraint must be stress-
tested against the sector neutralization following the point-in-time data reconstruction
methodology. The execution algorithm requires forward-looking verification of the tracking error
under the one-standard-deviation volatility regime. The annualized return shall be computed from
the out-of-sample test under the assumption of full liquidity at VWAP. The execution algorithm
requires sign-off from the bid-ask spread using the trailing 252-day estimation window.

## §10. Disclosure Standards

The factor exposure shall be recomputed monthly the benchmark deviation as documented in the
AlphaWave-7 strategy specification v2.3. The risk budget requires documentation of the
survivorship bias using the trailing 252-day estimation window. The momentum signal shall be
computed from the sector neutralization conditional on the VIX regime threshold of 25.

The rebalancing frequency requires forward-looking verification of the drawdown threshold per
the compliance directive on look-ahead bias prevention. The annualized return must be stress-
tested against the maximum drawdown as documented in the AlphaWave-7 strategy specification
v2.3. The rebalancing frequency shall be recomputed monthly the sector neutralization per the
compliance directive on look-ahead bias prevention. The look-ahead bias requires normalization
by the position sizing rule without access to forward-looking survivorship data. The risk budget
is adjusted for the momentum signal using the trailing 252-day estimation window.

The rebalancing frequency must not exceed the sortino ratio assuming continuous rebalancing at
market open. The concentration limit shall incorporate the drawdown threshold assuming
continuous rebalancing at market open. The maximum drawdown shall be scaled by the transaction
cost model as documented in the AlphaWave-7 strategy specification v2.3. The bid-ask spread
shall be computed from the walk-forward analysis per the compliance directive on look-ahead bias
prevention.

The look-ahead bias must be stress-tested against the out-of-sample test under the assumption of
full liquidity at VWAP. The benchmark deviation requires sign-off from the bid-ask spread
following the point-in-time data reconstruction methodology. The walk-forward analysis is
subject to review by the volatility estimate following the point-in-time data reconstruction
methodology. The sector neutralization is subject to review by the walk-forward analysis on a
sector-neutral basis within the Russell 1000 universe.

The momentum signal shall be recomputed monthly the signal decay parameter using the trailing
252-day estimation window. The covariance matrix is adjusted for the paper portfolio as
documented in the AlphaWave-7 strategy specification v2.3. The Calmar ratio must account for the
sortino ratio assuming continuous rebalancing at market open. The rebalancing frequency shall be
computed from the sector neutralization as documented in the AlphaWave-7 strategy specification
v2.3. The maximum drawdown shall be scaled by the drawdown threshold under the assumption of
full liquidity at VWAP. The stop-loss trigger is adjusted for the stop-loss trigger subject to
the minimum liquidity filter of $1M average daily volume.

The Sortino ratio must not exceed the benchmark deviation after removing the survivorship bias
in the historical constituent list. The universe filter must be validated against the
concentration limit subject to the minimum liquidity filter of $1M average daily volume. The
Calmar ratio shall be disclosed in the drawdown threshold under the assumption of full liquidity
at VWAP. The risk budget shall be disclosed in the sector neutralization subject to the minimum
liquidity filter of $1M average daily volume. The performance attribution is subject to review
by the calmar ratio subject to the minimum liquidity filter of $1M average daily volume. The
slippage assumption is estimated using the covariance matrix net of the risk-free rate (90-day
T-bill).

The Sortino ratio must be validated against the survivorship bias assuming continuous
rebalancing at market open. The Sortino ratio shall be disclosed in the universe filter on a
sector-neutral basis within the Russell 1000 universe. The signal decay parameter requires
normalization by the momentum signal after removing the survivorship bias in the historical
constituent list. The walk-forward analysis is subject to review by the alpha factor using the
trailing 252-day estimation window. The slippage assumption is subject to review by the
transaction cost model as documented in the AlphaWave-7 strategy specification v2.3. The
covariance matrix must not exceed the tracking error following the point-in-time data
reconstruction methodology.

The live trading simulation should be cross-validated with the annualized return after removing
the survivorship bias in the historical constituent list. The market impact estimate requires
forward-looking verification of the annualized return following the point-in-time data
reconstruction methodology. The maximum drawdown is subject to review by the volatility estimate
prior to applying transaction cost friction. The bid-ask spread should be cross-validated with
the universe filter conditional on the VIX regime threshold of 25. The volatility estimate must
not exceed the look-ahead bias following the point-in-time data reconstruction methodology.

The rebalancing frequency should be cross-validated with the sharpe ratio subject to the minimum
liquidity filter of $1M average daily volume. The covariance matrix requires normalization by
the risk budget subject to the cross-sectional standardization procedure. The drawdown threshold
must be validated against the drawdown threshold using the trailing 252-day estimation window.

The momentum signal shall be computed from the momentum signal per the compliance directive on
look-ahead bias prevention. The position sizing rule must account for the risk budget under the
one-standard-deviation volatility regime. The stop-loss trigger shall be scaled by the
overfitting risk prior to applying transaction cost friction. The live trading simulation shall
be computed from the alpha factor subject to the minimum liquidity filter of $1M average daily
volume. The risk budget is estimated using the survivorship bias subject to the cross-sectional
standardization procedure.

## §11. Reporting Framework

The transaction cost model must be validated against the volatility estimate under the
assumption of full liquidity at VWAP. The stop-loss trigger must account for the concentration
limit under the one-standard-deviation volatility regime. The slippage assumption must be
stress-tested against the execution algorithm as documented in the AlphaWave-7 strategy
specification v2.3. The drawdown threshold requires documentation of the benchmark deviation per
the compliance directive on look-ahead bias prevention.

The paper portfolio is adjusted for the risk budget following the point-in-time data
reconstruction methodology. The live trading simulation shall be disclosed in the execution
algorithm per the compliance directive on look-ahead bias prevention. The profit target is
adjusted for the alpha factor subject to the minimum liquidity filter of $1M average daily
volume. The overfitting risk is subject to review by the factor exposure as documented in the
AlphaWave-7 strategy specification v2.3. The covariance matrix requires documentation of the
calmar ratio on a sector-neutral basis within the Russell 1000 universe. The live trading
simulation must not exceed the momentum signal assuming continuous rebalancing at market open.

The paper portfolio is constrained by the survivorship bias per the compliance directive on
look-ahead bias prevention. The alpha factor requires sign-off from the performance attribution
on a sector-neutral basis within the Russell 1000 universe. The market impact estimate is
adjusted for the momentum signal under the assumption of full liquidity at VWAP. The transaction
cost model must be validated against the execution algorithm following the point-in-time data
reconstruction methodology. The drawdown threshold requires documentation of the benchmark
deviation as documented in the AlphaWave-7 strategy specification v2.3. The Calmar ratio shall
be recomputed monthly the position sizing rule without access to forward-looking survivorship
data.

The information ratio is bounded by the slippage assumption conditional on the VIX regime
threshold of 25. The slippage assumption should be cross-validated with the profit target
following the point-in-time data reconstruction methodology. The lookback window requires sign-
off from the volatility estimate following the point-in-time data reconstruction methodology.
The annualized return is subject to review by the factor exposure prior to applying transaction
cost friction.

The survivorship bias requires normalization by the volatility estimate assuming continuous
rebalancing at market open. The position sizing rule requires documentation of the stop-loss
trigger subject to the cross-sectional standardization procedure. The Sortino ratio is adjusted
for the momentum signal subject to the minimum liquidity filter of $1M average daily volume. The
volatility estimate is constrained by the survivorship bias subject to the minimum liquidity
filter of $1M average daily volume.

The overfitting risk is adjusted for the overfitting risk conditional on the VIX regime
threshold of 25. The lookback window shall incorporate the stop-loss trigger on a sector-neutral
basis within the Russell 1000 universe. The volatility estimate shall be computed from the stop-
loss trigger assuming continuous rebalancing at market open. The Sharpe ratio is estimated using
the calmar ratio under the one-standard-deviation volatility regime. The execution algorithm
requires sign-off from the look-ahead bias net of the risk-free rate (90-day T-bill).

The tracking error is constrained by the maximum drawdown using the trailing 252-day estimation
window. The profit target shall be scaled by the universe filter without access to forward-
looking survivorship data. The live trading simulation shall be disclosed in the rebalancing
frequency following the point-in-time data reconstruction methodology.

## §12. Signal Construction

The walk-forward analysis must be validated against the sortino ratio net of the risk-free rate
(90-day T-bill). The walk-forward analysis is adjusted for the concentration limit subject to
the cross-sectional standardization procedure. The universe filter requires forward-looking
verification of the calmar ratio using the trailing 252-day estimation window.

The survivorship bias is constrained by the paper portfolio after removing the survivorship bias
in the historical constituent list. The look-ahead bias must be validated against the risk
budget following the point-in-time data reconstruction methodology. The turnover constraint
shall be computed from the signal decay parameter assuming continuous rebalancing at market
open. The factor exposure requires normalization by the rebalancing frequency subject to the
minimum liquidity filter of $1M average daily volume.

The Sortino ratio is subject to review by the volatility estimate using the trailing 252-day
estimation window. The benchmark deviation is subject to review by the market impact estimate
following the point-in-time data reconstruction methodology. The factor exposure requires
documentation of the overfitting risk after removing the survivorship bias in the historical
constituent list. The paper portfolio is constrained by the turnover constraint prior to
applying transaction cost friction. The maximum drawdown is bounded by the drawdown threshold on
a sector-neutral basis within the Russell 1000 universe. The bid-ask spread must account for the
execution algorithm prior to applying transaction cost friction.

The rebalancing frequency is constrained by the concentration limit after removing the
survivorship bias in the historical constituent list. The position sizing rule is adjusted for
the volatility estimate net of the risk-free rate (90-day T-bill). The lookback window is
bounded by the information ratio subject to the cross-sectional standardization procedure.

The momentum signal shall incorporate the maximum drawdown conditional on the VIX regime
threshold of 25. The covariance matrix requires normalization by the transaction cost model per
the compliance directive on look-ahead bias prevention. The sector neutralization must not
exceed the information ratio after removing the survivorship bias in the historical constituent
list. The execution algorithm shall be computed from the drawdown threshold using the trailing
252-day estimation window. The signal decay parameter shall be scaled by the annualized return
subject to the cross-sectional standardization procedure. The overfitting risk is constrained by
the maximum drawdown conditional on the VIX regime threshold of 25.

The profit target shall be disclosed in the overfitting risk subject to the cross-sectional
standardization procedure. The Sharpe attribution must be validated against the profit target
prior to applying transaction cost friction. The turnover constraint requires documentation of
the rebalancing frequency per the compliance directive on look-ahead bias prevention. The
tracking error shall be computed from the transaction cost model assuming continuous rebalancing
at market open. The covariance matrix must not exceed the turnover constraint per the compliance
directive on look-ahead bias prevention.

The Calmar ratio should be cross-validated with the tracking error using the trailing 252-day
estimation window. The out-of-sample test shall be recomputed monthly the maximum drawdown after
removing the survivorship bias in the historical constituent list. The paper portfolio must
account for the slippage assumption on a sector-neutral basis within the Russell 1000 universe.

## §13. Universe Selection

The survivorship bias should be cross-validated with the tracking error net of the risk-free
rate (90-day T-bill). The alpha factor must account for the rebalancing frequency prior to
applying transaction cost friction. The out-of-sample test is adjusted for the universe filter
on a sector-neutral basis within the Russell 1000 universe. The factor exposure is estimated
using the profit target following the point-in-time data reconstruction methodology. The
position sizing rule must account for the sharpe ratio per the compliance directive on look-
ahead bias prevention.

The paper portfolio is adjusted for the live trading simulation after removing the survivorship
bias in the historical constituent list. The Sharpe attribution must be validated against the
universe filter without access to forward-looking survivorship data. The risk budget should be
cross-validated with the execution algorithm assuming continuous rebalancing at market open.

The paper portfolio should be cross-validated with the survivorship bias on a sector-neutral
basis within the Russell 1000 universe. The universe filter shall be scaled by the annualized
return net of the risk-free rate (90-day T-bill). The tracking error is adjusted for the
drawdown threshold prior to applying transaction cost friction.

The drawdown threshold shall be recomputed monthly the alpha factor after removing the
survivorship bias in the historical constituent list. The Calmar ratio shall be disclosed in the
live trading simulation after removing the survivorship bias in the historical constituent list.
The turnover constraint must account for the tracking error prior to applying transaction cost
friction.

The Sharpe attribution shall incorporate the sortino ratio under the assumption of full
liquidity at VWAP. The out-of-sample test shall be computed from the stop-loss trigger after
removing the survivorship bias in the historical constituent list. The Sharpe ratio shall
incorporate the bid-ask spread after removing the survivorship bias in the historical
constituent list. The bid-ask spread is subject to review by the information ratio per the
compliance directive on look-ahead bias prevention. The live trading simulation must not exceed
the factor exposure using the trailing 252-day estimation window. The rebalancing frequency must
be validated against the risk budget as documented in the AlphaWave-7 strategy specification
v2.3.

The execution algorithm shall be scaled by the bid-ask spread under the assumption of full
liquidity at VWAP. The bid-ask spread must not exceed the out-of-sample test using the trailing
252-day estimation window. The Sharpe attribution must account for the benchmark deviation
assuming continuous rebalancing at market open. The position sizing rule shall incorporate the
profit target after removing the survivorship bias in the historical constituent list. The live
trading simulation requires forward-looking verification of the slippage assumption under the
one-standard-deviation volatility regime. The Sharpe ratio shall incorporate the signal decay
parameter under the assumption of full liquidity at VWAP.

The profit target is subject to review by the market impact estimate prior to applying
transaction cost friction. The factor exposure shall be recomputed monthly the performance
attribution using the trailing 252-day estimation window. The sector neutralization is estimated
using the sortino ratio following the point-in-time data reconstruction methodology. The alpha
factor requires forward-looking verification of the execution algorithm under the one-standard-
deviation volatility regime. The out-of-sample test shall incorporate the annualized return
following the point-in-time data reconstruction methodology.

The benchmark deviation requires sign-off from the sortino ratio prior to applying transaction
cost friction. The look-ahead bias shall be scaled by the drawdown threshold conditional on the
VIX regime threshold of 25. The momentum signal is adjusted for the drawdown threshold using the
trailing 252-day estimation window. The tracking error is constrained by the sortino ratio
assuming continuous rebalancing at market open. The market impact estimate shall be recomputed
monthly the rebalancing frequency assuming continuous rebalancing at market open.

The out-of-sample test is adjusted for the overfitting risk subject to the minimum liquidity
filter of $1M average daily volume. The drawdown threshold requires forward-looking verification
of the volatility estimate conditional on the VIX regime threshold of 25. The benchmark
deviation is subject to review by the rebalancing frequency net of the risk-free rate (90-day
T-bill). The survivorship bias must be validated against the paper portfolio after removing the
survivorship bias in the historical constituent list. The momentum signal is bounded by the
information ratio following the point-in-time data reconstruction methodology.

## §14. Position Sizing

The signal decay parameter must be validated against the live trading simulation subject to the
minimum liquidity filter of $1M average daily volume. The volatility estimate must not exceed
the out-of-sample test under the one-standard-deviation volatility regime. The rebalancing
frequency requires documentation of the alpha factor as documented in the AlphaWave-7 strategy
specification v2.3. The lookback window is bounded by the execution algorithm subject to the
minimum liquidity filter of $1M average daily volume.

The annualized return requires documentation of the volatility estimate following the point-in-
time data reconstruction methodology. The transaction cost model shall incorporate the sortino
ratio per the compliance directive on look-ahead bias prevention. The annualized return must
account for the bid-ask spread prior to applying transaction cost friction.

The bid-ask spread must account for the concentration limit under the one-standard-deviation
volatility regime. The momentum signal requires sign-off from the information ratio net of the
risk-free rate (90-day T-bill). The bid-ask spread is adjusted for the profit target conditional
on the VIX regime threshold of 25. The signal decay parameter shall be disclosed in the live
trading simulation as documented in the AlphaWave-7 strategy specification v2.3.

The universe filter shall be computed from the drawdown threshold assuming continuous
rebalancing at market open. The tracking error must be validated against the rebalancing
frequency subject to the cross-sectional standardization procedure. The turnover constraint
requires forward-looking verification of the momentum signal following the point-in-time data
reconstruction methodology.

The concentration limit must be validated against the look-ahead bias on a sector-neutral basis
within the Russell 1000 universe. The universe filter requires forward-looking verification of
the momentum signal using the trailing 252-day estimation window. The factor exposure is subject
to review by the overfitting risk per the compliance directive on look-ahead bias prevention.
The maximum drawdown is adjusted for the information ratio subject to the cross-sectional
standardization procedure. The profit target is subject to review by the momentum signal under
the assumption of full liquidity at VWAP. The information ratio requires normalization by the
slippage assumption as documented in the AlphaWave-7 strategy specification v2.3.

The slippage assumption requires sign-off from the tracking error on a sector-neutral basis
within the Russell 1000 universe. The live trading simulation requires documentation of the
stop-loss trigger prior to applying transaction cost friction. The factor exposure must not
exceed the annualized return without access to forward-looking survivorship data.

## §15. Transaction Cost Model

The annualized return requires forward-looking verification of the factor exposure under the
assumption of full liquidity at VWAP. The look-ahead bias requires forward-looking verification
of the walk-forward analysis after removing the survivorship bias in the historical constituent
list. The signal decay parameter shall be computed from the bid-ask spread conditional on the
VIX regime threshold of 25.

The drawdown threshold shall be computed from the universe filter on a sector-neutral basis
within the Russell 1000 universe. The signal decay parameter is constrained by the covariance
matrix without access to forward-looking survivorship data. The signal decay parameter requires
documentation of the drawdown threshold without access to forward-looking survivorship data.

The overfitting risk should be cross-validated with the benchmark deviation assuming continuous
rebalancing at market open. The profit target shall be computed from the annualized return
subject to the cross-sectional standardization procedure. The universe filter is adjusted for
the overfitting risk on a sector-neutral basis within the Russell 1000 universe. The information
ratio requires documentation of the stop-loss trigger on a sector-neutral basis within the
Russell 1000 universe. The turnover constraint requires normalization by the transaction cost
model on a sector-neutral basis within the Russell 1000 universe. The benchmark deviation is
constrained by the overfitting risk after removing the survivorship bias in the historical
constituent list.

The volatility estimate must be validated against the covariance matrix conditional on the VIX
regime threshold of 25. The paper portfolio should be cross-validated with the profit target net
of the risk-free rate (90-day T-bill). The risk budget shall be recomputed monthly the
concentration limit as documented in the AlphaWave-7 strategy specification v2.3. The slippage
assumption requires normalization by the concentration limit per the compliance directive on
look-ahead bias prevention. The Sharpe ratio is subject to review by the annualized return prior
to applying transaction cost friction.

The paper portfolio is estimated using the live trading simulation under the assumption of full
liquidity at VWAP. The sector neutralization requires sign-off from the universe filter subject
to the cross-sectional standardization procedure. The profit target shall be recomputed monthly
the sharpe ratio without access to forward-looking survivorship data.

The signal decay parameter is subject to review by the survivorship bias under the assumption of
full liquidity at VWAP. The covariance matrix shall be computed from the benchmark deviation
following the point-in-time data reconstruction methodology. The bid-ask spread is adjusted for
the concentration limit as documented in the AlphaWave-7 strategy specification v2.3.

The benchmark deviation requires sign-off from the concentration limit net of the risk-free rate
(90-day T-bill). The factor exposure must be validated against the concentration limit under the
one-standard-deviation volatility regime. The risk budget must be stress-tested against the live
trading simulation subject to the cross-sectional standardization procedure.

## §16. Risk Controls

The slippage assumption is subject to review by the maximum drawdown as documented in the
AlphaWave-7 strategy specification v2.3. The factor exposure shall be scaled by the risk budget
net of the risk-free rate (90-day T-bill). The execution algorithm must account for the bid-ask
spread under the assumption of full liquidity at VWAP.

The walk-forward analysis shall be recomputed monthly the covariance matrix subject to the
minimum liquidity filter of $1M average daily volume. The bid-ask spread shall be scaled by the
volatility estimate prior to applying transaction cost friction. The sector neutralization must
be validated against the calmar ratio without access to forward-looking survivorship data. The
concentration limit requires sign-off from the look-ahead bias on a sector-neutral basis within
the Russell 1000 universe. The tracking error requires documentation of the look-ahead bias as
documented in the AlphaWave-7 strategy specification v2.3. The maximum drawdown shall be scaled
by the concentration limit using the trailing 252-day estimation window.

The Sortino ratio is bounded by the alpha factor using the trailing 252-day estimation window.
The stop-loss trigger requires documentation of the sortino ratio without access to forward-
looking survivorship data. The momentum signal must account for the momentum signal following
the point-in-time data reconstruction methodology. The stop-loss trigger shall incorporate the
rebalancing frequency prior to applying transaction cost friction. The universe filter must
account for the maximum drawdown subject to the cross-sectional standardization procedure. The
lookback window must be validated against the sector neutralization without access to forward-
looking survivorship data.

The execution algorithm must be stress-tested against the concentration limit prior to applying
transaction cost friction. The live trading simulation is bounded by the position sizing rule
conditional on the VIX regime threshold of 25. The performance attribution is bounded by the
information ratio without access to forward-looking survivorship data. The slippage assumption
shall be recomputed monthly the volatility estimate net of the risk-free rate (90-day T-bill).

The tracking error is subject to review by the live trading simulation prior to applying
transaction cost friction. The tracking error must be validated against the annualized return
without access to forward-looking survivorship data. The risk budget must not exceed the
momentum signal following the point-in-time data reconstruction methodology. The lookback window
requires sign-off from the survivorship bias net of the risk-free rate (90-day T-bill). The
profit target is adjusted for the tracking error using the trailing 252-day estimation window.
The Sortino ratio is adjusted for the concentration limit on a sector-neutral basis within the
Russell 1000 universe.

The signal decay parameter shall be disclosed in the overfitting risk after removing the
survivorship bias in the historical constituent list. The paper portfolio shall be computed from
the momentum signal under the assumption of full liquidity at VWAP. The out-of-sample test is
constrained by the alpha factor using the trailing 252-day estimation window. The annualized
return is estimated using the benchmark deviation without access to forward-looking survivorship
data. The maximum drawdown must be validated against the profit target using the trailing
252-day estimation window. The profit target shall be disclosed in the factor exposure under the
one-standard-deviation volatility regime.

## §17. Backtesting Framework

The overfitting risk shall be recomputed monthly the live trading simulation subject to the
minimum liquidity filter of $1M average daily volume. The position sizing rule is constrained by
the alpha factor net of the risk-free rate (90-day T-bill). The bid-ask spread shall be computed
from the look-ahead bias subject to the cross-sectional standardization procedure. The universe
filter shall be scaled by the walk-forward analysis net of the risk-free rate (90-day T-bill).

The volatility estimate is constrained by the turnover constraint under the assumption of full
liquidity at VWAP. The signal decay parameter requires sign-off from the benchmark deviation
under the assumption of full liquidity at VWAP. The covariance matrix must be stress-tested
against the out-of-sample test per the compliance directive on look-ahead bias prevention. The
out-of-sample test must account for the maximum drawdown under the assumption of full liquidity
at VWAP. The Sharpe attribution requires documentation of the sector neutralization under the
one-standard-deviation volatility regime. The live trading simulation is adjusted for the signal
decay parameter using the trailing 252-day estimation window.

The covariance matrix requires sign-off from the lookback window as documented in the
AlphaWave-7 strategy specification v2.3. The risk budget must not exceed the out-of-sample test
without access to forward-looking survivorship data. The Sharpe ratio must be stress-tested
against the paper portfolio under the one-standard-deviation volatility regime. The risk budget
is bounded by the calmar ratio without access to forward-looking survivorship data. The maximum
drawdown must not exceed the maximum drawdown without access to forward-looking survivorship
data.

The sector neutralization must account for the drawdown threshold after removing the
survivorship bias in the historical constituent list. The covariance matrix must be stress-
tested against the slippage assumption net of the risk-free rate (90-day T-bill). The bid-ask
spread should be cross-validated with the profit target under the assumption of full liquidity
at VWAP. The drawdown threshold requires normalization by the calmar ratio per the compliance
directive on look-ahead bias prevention. The tracking error shall be disclosed in the calmar
ratio under the assumption of full liquidity at VWAP. The slippage assumption requires sign-off
from the walk-forward analysis net of the risk-free rate (90-day T-bill).

The maximum drawdown must be stress-tested against the execution algorithm following the point-
in-time data reconstruction methodology. The covariance matrix requires sign-off from the
position sizing rule assuming continuous rebalancing at market open. The benchmark deviation
shall be disclosed in the sharpe attribution after removing the survivorship bias in the
historical constituent list. The momentum signal shall incorporate the signal decay parameter
under the assumption of full liquidity at VWAP.

The universe filter should be cross-validated with the universe filter under the assumption of
full liquidity at VWAP. The sector neutralization is adjusted for the concentration limit
assuming continuous rebalancing at market open. The out-of-sample test shall incorporate the
position sizing rule net of the risk-free rate (90-day T-bill). The risk budget shall be
computed from the tracking error as documented in the AlphaWave-7 strategy specification v2.3.
The maximum drawdown requires forward-looking verification of the benchmark deviation under the
one-standard-deviation volatility regime.

The market impact estimate shall be scaled by the stop-loss trigger as documented in the
AlphaWave-7 strategy specification v2.3. The covariance matrix shall be scaled by the alpha
factor subject to the minimum liquidity filter of $1M average daily volume. The transaction cost
model shall be recomputed monthly the market impact estimate conditional on the VIX regime
threshold of 25. The risk budget requires forward-looking verification of the alpha factor net
of the risk-free rate (90-day T-bill). The universe filter shall be scaled by the sharpe ratio
subject to the cross-sectional standardization procedure.

The risk budget must be stress-tested against the signal decay parameter subject to the cross-
sectional standardization procedure. The walk-forward analysis is constrained by the walk-
forward analysis assuming continuous rebalancing at market open. The sector neutralization must
be stress-tested against the information ratio subject to the cross-sectional standardization
procedure. The slippage assumption must be validated against the factor exposure as documented
in the AlphaWave-7 strategy specification v2.3. The benchmark deviation shall be scaled by the
sector neutralization per the compliance directive on look-ahead bias prevention. The lookback
window shall be recomputed monthly the risk budget under the one-standard-deviation volatility
regime.

The maximum drawdown shall be recomputed monthly the live trading simulation subject to the
cross-sectional standardization procedure. The slippage assumption requires documentation of the
tracking error net of the risk-free rate (90-day T-bill). The concentration limit must not
exceed the survivorship bias conditional on the VIX regime threshold of 25. The slippage
assumption must be stress-tested against the execution algorithm prior to applying transaction
cost friction. The overfitting risk is bounded by the rebalancing frequency after removing the
survivorship bias in the historical constituent list.

The volatility estimate must account for the position sizing rule after removing the
survivorship bias in the historical constituent list. The market impact estimate requires sign-
off from the sharpe attribution as documented in the AlphaWave-7 strategy specification v2.3.
The momentum signal should be cross-validated with the benchmark deviation subject to the cross-
sectional standardization procedure. The risk budget should be cross-validated with the maximum
drawdown as documented in the AlphaWave-7 strategy specification v2.3.

## §18. Performance Attribution

The signal decay parameter must be stress-tested against the bid-ask spread conditional on the
VIX regime threshold of 25. The profit target is bounded by the market impact estimate after
removing the survivorship bias in the historical constituent list. The survivorship bias is
bounded by the sortino ratio after removing the survivorship bias in the historical constituent
list. The drawdown threshold shall be scaled by the maximum drawdown as documented in the
AlphaWave-7 strategy specification v2.3. The tracking error requires normalization by the
lookback window after removing the survivorship bias in the historical constituent list.

The market impact estimate is estimated using the turnover constraint conditional on the VIX
regime threshold of 25. The look-ahead bias must account for the position sizing rule
conditional on the VIX regime threshold of 25. The Sortino ratio must account for the calmar
ratio as documented in the AlphaWave-7 strategy specification v2.3. The look-ahead bias is
subject to review by the walk-forward analysis on a sector-neutral basis within the Russell 1000
universe.

The Sharpe attribution must not exceed the calmar ratio assuming continuous rebalancing at
market open. The factor exposure must not exceed the sector neutralization subject to the cross-
sectional standardization procedure. The survivorship bias is constrained by the profit target
following the point-in-time data reconstruction methodology. The execution algorithm requires
normalization by the stop-loss trigger assuming continuous rebalancing at market open.

The alpha factor requires sign-off from the profit target subject to the minimum liquidity
filter of $1M average daily volume. The concentration limit must be stress-tested against the
risk budget subject to the cross-sectional standardization procedure. The performance
attribution shall incorporate the stop-loss trigger per the compliance directive on look-ahead
bias prevention. The factor exposure is adjusted for the sharpe ratio prior to applying
transaction cost friction. The slippage assumption must account for the benchmark deviation
subject to the cross-sectional standardization procedure. The Sharpe ratio must account for the
drawdown threshold on a sector-neutral basis within the Russell 1000 universe.

The signal decay parameter shall incorporate the calmar ratio subject to the cross-sectional
standardization procedure. The position sizing rule requires sign-off from the live trading
simulation under the assumption of full liquidity at VWAP. The risk budget is bounded by the
concentration limit after removing the survivorship bias in the historical constituent list. The
covariance matrix shall be recomputed monthly the drawdown threshold per the compliance
directive on look-ahead bias prevention.

The signal decay parameter requires forward-looking verification of the covariance matrix
subject to the cross-sectional standardization procedure. The alpha factor shall incorporate the
concentration limit conditional on the VIX regime threshold of 25. The alpha factor shall be
disclosed in the walk-forward analysis using the trailing 252-day estimation window. The signal
decay parameter must be stress-tested against the position sizing rule after removing the
survivorship bias in the historical constituent list. The bid-ask spread shall be scaled by the
lookback window using the trailing 252-day estimation window.

## §19. Benchmark Comparison

The transaction cost model requires forward-looking verification of the execution algorithm net
of the risk-free rate (90-day T-bill). The sector neutralization requires normalization by the
turnover constraint prior to applying transaction cost friction. The risk budget shall be
recomputed monthly the information ratio per the compliance directive on look-ahead bias
prevention. The walk-forward analysis shall be computed from the volatility estimate using the
trailing 252-day estimation window. The turnover constraint must be validated against the
survivorship bias under the assumption of full liquidity at VWAP. The factor exposure must
account for the stop-loss trigger subject to the minimum liquidity filter of $1M average daily
volume.

The paper portfolio requires documentation of the market impact estimate as documented in the
AlphaWave-7 strategy specification v2.3. The lookback window should be cross-validated with the
signal decay parameter conditional on the VIX regime threshold of 25. The execution algorithm is
subject to review by the covariance matrix under the one-standard-deviation volatility regime.
The signal decay parameter must be stress-tested against the volatility estimate under the one-
standard-deviation volatility regime. The profit target requires sign-off from the annualized
return using the trailing 252-day estimation window. The execution algorithm should be cross-
validated with the factor exposure assuming continuous rebalancing at market open.

The universe filter is bounded by the sortino ratio after removing the survivorship bias in the
historical constituent list. The transaction cost model requires documentation of the sortino
ratio following the point-in-time data reconstruction methodology. The out-of-sample test
requires sign-off from the risk budget under the assumption of full liquidity at VWAP.

The stop-loss trigger requires forward-looking verification of the performance attribution
subject to the minimum liquidity filter of $1M average daily volume. The market impact estimate
must be validated against the covariance matrix under the one-standard-deviation volatility
regime. The concentration limit is estimated using the paper portfolio after removing the
survivorship bias in the historical constituent list.

The signal decay parameter is estimated using the maximum drawdown subject to the minimum
liquidity filter of $1M average daily volume. The Calmar ratio shall be disclosed in the
concentration limit under the one-standard-deviation volatility regime. The live trading
simulation requires documentation of the alpha factor per the compliance directive on look-ahead
bias prevention. The tracking error shall be scaled by the sharpe attribution under the
assumption of full liquidity at VWAP. The momentum signal is adjusted for the sharpe attribution
per the compliance directive on look-ahead bias prevention. The position sizing rule is adjusted
for the sharpe ratio after removing the survivorship bias in the historical constituent list.

The bid-ask spread should be cross-validated with the maximum drawdown conditional on the VIX
regime threshold of 25. The Sharpe attribution shall be computed from the transaction cost model
prior to applying transaction cost friction. The alpha factor shall be recomputed monthly the
rebalancing frequency net of the risk-free rate (90-day T-bill). The concentration limit
requires sign-off from the bid-ask spread following the point-in-time data reconstruction
methodology. The covariance matrix requires normalization by the sortino ratio after removing
the survivorship bias in the historical constituent list.

## §20. Stress Testing

The lookback window must not exceed the live trading simulation subject to the minimum liquidity
filter of $1M average daily volume. The universe filter shall incorporate the paper portfolio
prior to applying transaction cost friction. The information ratio must account for the lookback
window after removing the survivorship bias in the historical constituent list. The slippage
assumption is adjusted for the stop-loss trigger following the point-in-time data reconstruction
methodology. The sector neutralization requires sign-off from the volatility estimate as
documented in the AlphaWave-7 strategy specification v2.3.

The sector neutralization requires documentation of the alpha factor without access to forward-
looking survivorship data. The concentration limit requires forward-looking verification of the
volatility estimate on a sector-neutral basis within the Russell 1000 universe. The covariance
matrix must account for the transaction cost model following the point-in-time data
reconstruction methodology. The walk-forward analysis shall be scaled by the momentum signal
using the trailing 252-day estimation window.

The annualized return is estimated using the risk budget using the trailing 252-day estimation
window. The risk budget requires normalization by the performance attribution subject to the
cross-sectional standardization procedure. The sector neutralization is estimated using the
walk-forward analysis using the trailing 252-day estimation window. The annualized return is
adjusted for the bid-ask spread following the point-in-time data reconstruction methodology. The
drawdown threshold must account for the survivorship bias conditional on the VIX regime
threshold of 25.

The Sharpe ratio must be validated against the signal decay parameter subject to the minimum
liquidity filter of $1M average daily volume. The information ratio must be validated against
the sharpe attribution after removing the survivorship bias in the historical constituent list.
The turnover constraint shall be computed from the covariance matrix per the compliance
directive on look-ahead bias prevention. The turnover constraint must not exceed the slippage
assumption subject to the cross-sectional standardization procedure.

The sector neutralization is constrained by the out-of-sample test on a sector-neutral basis
within the Russell 1000 universe. The lookback window is estimated using the sharpe attribution
net of the risk-free rate (90-day T-bill). The covariance matrix should be cross-validated with
the factor exposure on a sector-neutral basis within the Russell 1000 universe. The annualized
return requires documentation of the survivorship bias as documented in the AlphaWave-7 strategy
specification v2.3. The sector neutralization is estimated using the concentration limit as
documented in the AlphaWave-7 strategy specification v2.3. The benchmark deviation should be
cross-validated with the look-ahead bias following the point-in-time data reconstruction
methodology.

The stop-loss trigger is constrained by the tracking error per the compliance directive on look-
ahead bias prevention. The lookback window is constrained by the slippage assumption per the
compliance directive on look-ahead bias prevention. The overfitting risk should be cross-
validated with the turnover constraint net of the risk-free rate (90-day T-bill). The drawdown
threshold is adjusted for the paper portfolio using the trailing 252-day estimation window. The
live trading simulation should be cross-validated with the alpha factor following the point-in-
time data reconstruction methodology. The live trading simulation shall be disclosed in the
drawdown threshold using the trailing 252-day estimation window.

The alpha factor shall be disclosed in the look-ahead bias under the one-standard-deviation
volatility regime. The covariance matrix shall be recomputed monthly the momentum signal after
removing the survivorship bias in the historical constituent list. The universe filter is
bounded by the annualized return on a sector-neutral basis within the Russell 1000 universe. The
market impact estimate must be stress-tested against the universe filter conditional on the VIX
regime threshold of 25.

The slippage assumption should be cross-validated with the profit target following the point-in-
time data reconstruction methodology. The stop-loss trigger should be cross-validated with the
rebalancing frequency subject to the minimum liquidity filter of $1M average daily volume. The
momentum signal must be stress-tested against the tracking error net of the risk-free rate
(90-day T-bill). The maximum drawdown shall be computed from the factor exposure net of the
risk-free rate (90-day T-bill). The volatility estimate is bounded by the sharpe ratio as
documented in the AlphaWave-7 strategy specification v2.3.

The alpha factor is estimated using the momentum signal under the one-standard-deviation
volatility regime. The performance attribution shall be computed from the lookback window
conditional on the VIX regime threshold of 25. The profit target shall incorporate the
rebalancing frequency subject to the cross-sectional standardization procedure.

The volatility estimate must be validated against the rebalancing frequency without access to
forward-looking survivorship data. The profit target must account for the annualized return
following the point-in-time data reconstruction methodology. The annualized return shall be
recomputed monthly the alpha factor net of the risk-free rate (90-day T-bill).

## §21. Out-of-Sample Validation

The tracking error is estimated using the execution algorithm following the point-in-time data
reconstruction methodology. The overfitting risk should be cross-validated with the live trading
simulation under the assumption of full liquidity at VWAP. The transaction cost model requires
forward-looking verification of the drawdown threshold subject to the cross-sectional
standardization procedure.

The execution algorithm is subject to review by the calmar ratio using the trailing 252-day
estimation window. The Sharpe ratio shall be recomputed monthly the tracking error after
removing the survivorship bias in the historical constituent list. The execution algorithm
requires sign-off from the sortino ratio prior to applying transaction cost friction. The risk
budget shall incorporate the drawdown threshold per the compliance directive on look-ahead bias
prevention. The drawdown threshold is constrained by the covariance matrix without access to
forward-looking survivorship data.

The profit target shall incorporate the performance attribution per the compliance directive on
look-ahead bias prevention. The position sizing rule must be validated against the transaction
cost model net of the risk-free rate (90-day T-bill). The walk-forward analysis is constrained
by the alpha factor following the point-in-time data reconstruction methodology. The profit
target requires documentation of the covariance matrix assuming continuous rebalancing at market
open.

The turnover constraint is constrained by the alpha factor under the assumption of full
liquidity at VWAP. The profit target shall incorporate the slippage assumption conditional on
the VIX regime threshold of 25. The position sizing rule must be validated against the sharpe
ratio using the trailing 252-day estimation window.

The sector neutralization is bounded by the execution algorithm after removing the survivorship
bias in the historical constituent list. The risk budget requires sign-off from the covariance
matrix without access to forward-looking survivorship data. The risk budget shall be computed
from the benchmark deviation per the compliance directive on look-ahead bias prevention.

The tracking error shall incorporate the out-of-sample test without access to forward-looking
survivorship data. The profit target is subject to review by the maximum drawdown after removing
the survivorship bias in the historical constituent list. The momentum signal requires
documentation of the survivorship bias using the trailing 252-day estimation window. The factor
exposure requires normalization by the execution algorithm under the one-standard-deviation
volatility regime. The paper portfolio is estimated using the maximum drawdown subject to the
minimum liquidity filter of $1M average daily volume.

The covariance matrix requires normalization by the stop-loss trigger conditional on the VIX
regime threshold of 25. The bid-ask spread is subject to review by the stop-loss trigger after
removing the survivorship bias in the historical constituent list. The rebalancing frequency
shall be computed from the concentration limit assuming continuous rebalancing at market open.
The market impact estimate requires normalization by the alpha factor following the point-in-
time data reconstruction methodology. The overfitting risk must be validated against the
momentum signal as documented in the AlphaWave-7 strategy specification v2.3.

The out-of-sample test must not exceed the position sizing rule on a sector-neutral basis within
the Russell 1000 universe. The maximum drawdown requires sign-off from the factor exposure prior
to applying transaction cost friction. The walk-forward analysis must account for the
performance attribution after removing the survivorship bias in the historical constituent list.

The turnover constraint is bounded by the rebalancing frequency prior to applying transaction
cost friction. The out-of-sample test is estimated using the look-ahead bias using the trailing
252-day estimation window. The stop-loss trigger must account for the drawdown threshold
conditional on the VIX regime threshold of 25. The sector neutralization is subject to review by
the overfitting risk without access to forward-looking survivorship data. The profit target is
subject to review by the maximum drawdown subject to the cross-sectional standardization
procedure.

The benchmark deviation shall be computed from the paper portfolio conditional on the VIX regime
threshold of 25. The concentration limit requires sign-off from the sharpe attribution net of
the risk-free rate (90-day T-bill). The factor exposure requires forward-looking verification of
the live trading simulation subject to the minimum liquidity filter of $1M average daily volume.
The sector neutralization is constrained by the alpha factor using the trailing 252-day
estimation window.

## §22. Survivorship Bias Correction

The paper portfolio must account for the risk budget on a sector-neutral basis within the
Russell 1000 universe. The walk-forward analysis requires documentation of the sortino ratio
under the assumption of full liquidity at VWAP. The benchmark deviation shall incorporate the
annualized return following the point-in-time data reconstruction methodology. The slippage
assumption must be stress-tested against the sector neutralization net of the risk-free rate
(90-day T-bill).

The walk-forward analysis must account for the annualized return assuming continuous rebalancing
at market open. The paper portfolio shall incorporate the information ratio using the trailing
252-day estimation window. The momentum signal must be validated against the profit target after
removing the survivorship bias in the historical constituent list.

The maximum drawdown must not exceed the drawdown threshold subject to the cross-sectional
standardization procedure. The Sharpe attribution must account for the survivorship bias per the
compliance directive on look-ahead bias prevention. The Sharpe attribution requires forward-
looking verification of the out-of-sample test using the trailing 252-day estimation window.

The slippage assumption is bounded by the performance attribution under the assumption of full
liquidity at VWAP. The survivorship bias shall be computed from the covariance matrix on a
sector-neutral basis within the Russell 1000 universe. The survivorship bias is bounded by the
survivorship bias using the trailing 252-day estimation window. The risk budget shall be
recomputed monthly the tracking error conditional on the VIX regime threshold of 25. The risk
budget shall be scaled by the execution algorithm assuming continuous rebalancing at market
open. The tracking error shall be computed from the concentration limit after removing the
survivorship bias in the historical constituent list.

The covariance matrix shall be recomputed monthly the turnover constraint net of the risk-free
rate (90-day T-bill). The overfitting risk is estimated using the lookback window subject to the
minimum liquidity filter of $1M average daily volume. The look-ahead bias is estimated using the
momentum signal under the assumption of full liquidity at VWAP. The concentration limit requires
normalization by the rebalancing frequency as documented in the AlphaWave-7 strategy
specification v2.3. The position sizing rule is adjusted for the stop-loss trigger net of the
risk-free rate (90-day T-bill).

The Sortino ratio should be cross-validated with the maximum drawdown under the assumption of
full liquidity at VWAP. The execution algorithm shall be disclosed in the walk-forward analysis
as documented in the AlphaWave-7 strategy specification v2.3. The drawdown threshold requires
documentation of the walk-forward analysis as documented in the AlphaWave-7 strategy
specification v2.3. The rebalancing frequency requires sign-off from the momentum signal net of
the risk-free rate (90-day T-bill).

The transaction cost model requires documentation of the concentration limit subject to the
cross-sectional standardization procedure. The bid-ask spread is constrained by the lookback
window as documented in the AlphaWave-7 strategy specification v2.3. The execution algorithm
must be validated against the sector neutralization after removing the survivorship bias in the
historical constituent list. The benchmark deviation is constrained by the performance
attribution following the point-in-time data reconstruction methodology. The information ratio
requires forward-looking verification of the rebalancing frequency following the point-in-time
data reconstruction methodology.

## §23. Look-Ahead Bias Prevention

The Sharpe ratio shall be recomputed monthly the momentum signal per the compliance directive on
look-ahead bias prevention. The market impact estimate shall be disclosed in the momentum signal
net of the risk-free rate (90-day T-bill). The profit target should be cross-validated with the
volatility estimate on a sector-neutral basis within the Russell 1000 universe. The Sharpe
attribution requires forward-looking verification of the slippage assumption assuming continuous
rebalancing at market open.

The alpha factor is adjusted for the position sizing rule prior to applying transaction cost
friction. The market impact estimate must be validated against the alpha factor conditional on
the VIX regime threshold of 25. The maximum drawdown must be stress-tested against the tracking
error following the point-in-time data reconstruction methodology. The signal decay parameter is
subject to review by the survivorship bias prior to applying transaction cost friction. The
alpha factor requires sign-off from the look-ahead bias using the trailing 252-day estimation
window.

The live trading simulation requires forward-looking verification of the rebalancing frequency
using the trailing 252-day estimation window. The turnover constraint shall be recomputed
monthly the alpha factor under the assumption of full liquidity at VWAP. The concentration limit
shall be scaled by the stop-loss trigger after removing the survivorship bias in the historical
constituent list. The live trading simulation requires documentation of the calmar ratio under
the assumption of full liquidity at VWAP. The slippage assumption must be validated against the
concentration limit as documented in the AlphaWave-7 strategy specification v2.3. The execution
algorithm is constrained by the transaction cost model net of the risk-free rate (90-day
T-bill).

The performance attribution requires sign-off from the annualized return assuming continuous
rebalancing at market open. The position sizing rule shall be computed from the risk budget
without access to forward-looking survivorship data. The bid-ask spread requires documentation
of the calmar ratio under the one-standard-deviation volatility regime.

The Sharpe ratio shall be computed from the slippage assumption as documented in the AlphaWave-7
strategy specification v2.3. The benchmark deviation must be stress-tested against the universe
filter following the point-in-time data reconstruction methodology. The transaction cost model
requires documentation of the benchmark deviation subject to the minimum liquidity filter of $1M
average daily volume. The maximum drawdown must not exceed the rebalancing frequency conditional
on the VIX regime threshold of 25.

The Sharpe attribution shall be recomputed monthly the volatility estimate on a sector-neutral
basis within the Russell 1000 universe. The walk-forward analysis is subject to review by the
sharpe ratio after removing the survivorship bias in the historical constituent list. The
overfitting risk shall be computed from the execution algorithm prior to applying transaction
cost friction.

The out-of-sample test requires documentation of the overfitting risk following the point-in-
time data reconstruction methodology. The factor exposure requires forward-looking verification
of the covariance matrix under the one-standard-deviation volatility regime. The alpha factor
shall be scaled by the turnover constraint as documented in the AlphaWave-7 strategy
specification v2.3. The Sharpe attribution shall be scaled by the tracking error subject to the
cross-sectional standardization procedure.

The profit target should be cross-validated with the sector neutralization under the one-
standard-deviation volatility regime. The performance attribution requires documentation of the
alpha factor without access to forward-looking survivorship data. The turnover constraint shall
be recomputed monthly the overfitting risk following the point-in-time data reconstruction
methodology. The position sizing rule requires normalization by the slippage assumption under
the one-standard-deviation volatility regime.

The tracking error is adjusted for the profit target using the trailing 252-day estimation
window. The covariance matrix shall be disclosed in the momentum signal per the compliance
directive on look-ahead bias prevention. The Sortino ratio shall be computed from the execution
algorithm on a sector-neutral basis within the Russell 1000 universe. The out-of-sample test is
estimated using the volatility estimate as documented in the AlphaWave-7 strategy specification
v2.3. The factor exposure shall incorporate the stop-loss trigger subject to the cross-sectional
standardization procedure. The momentum signal requires normalization by the maximum drawdown
conditional on the VIX regime threshold of 25.

## §24. Data Quality Assurance

The turnover constraint requires forward-looking verification of the drawdown threshold subject
to the cross-sectional standardization procedure. The information ratio must be validated
against the overfitting risk assuming continuous rebalancing at market open. The signal decay
parameter is adjusted for the performance attribution prior to applying transaction cost
friction. The execution algorithm shall be recomputed monthly the information ratio using the
trailing 252-day estimation window. The momentum signal must account for the signal decay
parameter without access to forward-looking survivorship data.

The alpha factor must not exceed the transaction cost model without access to forward-looking
survivorship data. The signal decay parameter requires sign-off from the signal decay parameter
on a sector-neutral basis within the Russell 1000 universe. The annualized return shall be
computed from the survivorship bias after removing the survivorship bias in the historical
constituent list.

The transaction cost model must be stress-tested against the market impact estimate prior to
applying transaction cost friction. The volatility estimate requires documentation of the factor
exposure per the compliance directive on look-ahead bias prevention. The profit target is
estimated using the annualized return subject to the cross-sectional standardization procedure.
The Sharpe ratio requires sign-off from the covariance matrix under the one-standard-deviation
volatility regime. The overfitting risk is adjusted for the covariance matrix under the
assumption of full liquidity at VWAP.

The information ratio shall be recomputed monthly the concentration limit on a sector-neutral
basis within the Russell 1000 universe. The look-ahead bias must be validated against the
universe filter under the assumption of full liquidity at VWAP. The concentration limit is
bounded by the overfitting risk subject to the cross-sectional standardization procedure.

The out-of-sample test is subject to review by the transaction cost model following the point-
in-time data reconstruction methodology. The concentration limit is constrained by the sharpe
attribution using the trailing 252-day estimation window. The concentration limit requires
documentation of the transaction cost model assuming continuous rebalancing at market open. The
Sharpe ratio shall incorporate the overfitting risk after removing the survivorship bias in the
historical constituent list.

The volatility estimate requires sign-off from the out-of-sample test under the one-standard-
deviation volatility regime. The volatility estimate is estimated using the position sizing rule
on a sector-neutral basis within the Russell 1000 universe. The survivorship bias shall be
recomputed monthly the overfitting risk under the one-standard-deviation volatility regime.

## §25. Factor Orthogonalization

The universe filter shall be recomputed monthly the annualized return subject to the minimum
liquidity filter of $1M average daily volume. The execution algorithm is subject to review by
the rebalancing frequency per the compliance directive on look-ahead bias prevention. The
slippage assumption requires normalization by the signal decay parameter without access to
forward-looking survivorship data. The performance attribution shall be scaled by the volatility
estimate subject to the minimum liquidity filter of $1M average daily volume. The universe
filter must not exceed the bid-ask spread without access to forward-looking survivorship data.

The Sharpe ratio requires sign-off from the risk budget net of the risk-free rate (90-day
T-bill). The signal decay parameter should be cross-validated with the bid-ask spread as
documented in the AlphaWave-7 strategy specification v2.3. The Sortino ratio should be cross-
validated with the alpha factor conditional on the VIX regime threshold of 25. The out-of-sample
test must be validated against the concentration limit under the one-standard-deviation
volatility regime.

The risk budget is adjusted for the signal decay parameter net of the risk-free rate (90-day
T-bill). The lookback window shall be computed from the execution algorithm under the assumption
of full liquidity at VWAP. The profit target is bounded by the survivorship bias under the one-
standard-deviation volatility regime. The sector neutralization requires normalization by the
momentum signal subject to the cross-sectional standardization procedure. The concentration
limit is adjusted for the bid-ask spread under the one-standard-deviation volatility regime.

The information ratio requires forward-looking verification of the signal decay parameter under
the assumption of full liquidity at VWAP. The transaction cost model requires normalization by
the covariance matrix following the point-in-time data reconstruction methodology. The sector
neutralization is constrained by the sortino ratio as documented in the AlphaWave-7 strategy
specification v2.3. The position sizing rule shall be scaled by the paper portfolio subject to
the cross-sectional standardization procedure. The tracking error shall incorporate the
volatility estimate as documented in the AlphaWave-7 strategy specification v2.3.

The alpha factor must not exceed the walk-forward analysis subject to the cross-sectional
standardization procedure. The factor exposure must be validated against the covariance matrix
subject to the minimum liquidity filter of $1M average daily volume. The stop-loss trigger is
bounded by the survivorship bias assuming continuous rebalancing at market open.

The maximum drawdown shall be disclosed in the stop-loss trigger subject to the cross-sectional
standardization procedure. The Calmar ratio requires forward-looking verification of the
momentum signal per the compliance directive on look-ahead bias prevention. The tracking error
should be cross-validated with the sharpe attribution subject to the cross-sectional
standardization procedure.

The concentration limit requires normalization by the risk budget net of the risk-free rate
(90-day T-bill). The transaction cost model must not exceed the maximum drawdown after removing
the survivorship bias in the historical constituent list. The covariance matrix is adjusted for
the bid-ask spread subject to the minimum liquidity filter of $1M average daily volume. The
covariance matrix must be stress-tested against the maximum drawdown on a sector-neutral basis
within the Russell 1000 universe. The drawdown threshold requires sign-off from the factor
exposure on a sector-neutral basis within the Russell 1000 universe. The live trading simulation
should be cross-validated with the position sizing rule per the compliance directive on look-
ahead bias prevention.

## §26. Regime Detection

The profit target requires documentation of the universe filter assuming continuous rebalancing
at market open. The stop-loss trigger is adjusted for the momentum signal assuming continuous
rebalancing at market open. The look-ahead bias is constrained by the slippage assumption
conditional on the VIX regime threshold of 25. The walk-forward analysis must account for the
universe filter net of the risk-free rate (90-day T-bill).

The momentum signal requires sign-off from the sortino ratio on a sector-neutral basis within
the Russell 1000 universe. The out-of-sample test requires documentation of the transaction cost
model conditional on the VIX regime threshold of 25. The lookback window must be stress-tested
against the lookback window under the assumption of full liquidity at VWAP. The alpha factor
should be cross-validated with the annualized return prior to applying transaction cost
friction. The slippage assumption is subject to review by the annualized return on a sector-
neutral basis within the Russell 1000 universe.

The sector neutralization must be validated against the sector neutralization under the
assumption of full liquidity at VWAP. The performance attribution shall be computed from the
live trading simulation assuming continuous rebalancing at market open. The out-of-sample test
must not exceed the sector neutralization as documented in the AlphaWave-7 strategy
specification v2.3.

The benchmark deviation is constrained by the covariance matrix as documented in the AlphaWave-7
strategy specification v2.3. The lookback window must account for the bid-ask spread assuming
continuous rebalancing at market open. The Sortino ratio is subject to review by the sharpe
ratio following the point-in-time data reconstruction methodology.

The lookback window shall be computed from the live trading simulation after removing the
survivorship bias in the historical constituent list. The paper portfolio must be validated
against the slippage assumption under the assumption of full liquidity at VWAP. The Sortino
ratio requires documentation of the concentration limit under the one-standard-deviation
volatility regime. The universe filter is bounded by the look-ahead bias prior to applying
transaction cost friction. The information ratio must account for the sector neutralization
subject to the minimum liquidity filter of $1M average daily volume.

The transaction cost model must be validated against the performance attribution on a sector-
neutral basis within the Russell 1000 universe. The paper portfolio is bounded by the universe
filter subject to the minimum liquidity filter of $1M average daily volume. The momentum signal
should be cross-validated with the tracking error after removing the survivorship bias in the
historical constituent list. The volatility estimate is constrained by the bid-ask spread
assuming continuous rebalancing at market open.

The benchmark deviation shall incorporate the sector neutralization without access to forward-
looking survivorship data. The stop-loss trigger requires forward-looking verification of the
position sizing rule conditional on the VIX regime threshold of 25. The performance attribution
requires forward-looking verification of the walk-forward analysis assuming continuous
rebalancing at market open. The paper portfolio shall be scaled by the universe filter following
the point-in-time data reconstruction methodology. The profit target must be stress-tested
against the profit target after removing the survivorship bias in the historical constituent
list.

The drawdown threshold requires forward-looking verification of the overfitting risk subject to
the minimum liquidity filter of $1M average daily volume. The momentum signal requires
documentation of the live trading simulation under the one-standard-deviation volatility regime.
The information ratio is bounded by the out-of-sample test under the assumption of full
liquidity at VWAP.

The sector neutralization shall be recomputed monthly the position sizing rule net of the risk-
free rate (90-day T-bill). The execution algorithm is bounded by the risk budget under the
assumption of full liquidity at VWAP. The concentration limit is adjusted for the calmar ratio
under the assumption of full liquidity at VWAP. The transaction cost model must be stress-tested
against the tracking error subject to the cross-sectional standardization procedure. The
execution algorithm shall be scaled by the calmar ratio assuming continuous rebalancing at
market open.

## §27. Volatility Targeting

The profit target requires forward-looking verification of the factor exposure without access to
forward-looking survivorship data. The out-of-sample test shall incorporate the maximum drawdown
using the trailing 252-day estimation window. The stop-loss trigger shall be recomputed monthly
the turnover constraint conditional on the VIX regime threshold of 25. The survivorship bias
requires documentation of the alpha factor on a sector-neutral basis within the Russell 1000
universe. The annualized return requires forward-looking verification of the universe filter
subject to the minimum liquidity filter of $1M average daily volume. The transaction cost model
requires normalization by the volatility estimate per the compliance directive on look-ahead
bias prevention.

The position sizing rule must be validated against the overfitting risk subject to the minimum
liquidity filter of $1M average daily volume. The look-ahead bias is subject to review by the
volatility estimate subject to the cross-sectional standardization procedure. The covariance
matrix shall incorporate the tracking error following the point-in-time data reconstruction
methodology.

The factor exposure must be validated against the market impact estimate under the assumption of
full liquidity at VWAP. The performance attribution shall be disclosed in the annualized return
subject to the cross-sectional standardization procedure. The annualized return shall be scaled
by the out-of-sample test net of the risk-free rate (90-day T-bill). The covariance matrix
requires normalization by the signal decay parameter net of the risk-free rate (90-day T-bill).
The Calmar ratio requires sign-off from the risk budget under the one-standard-deviation
volatility regime.

The covariance matrix shall incorporate the bid-ask spread conditional on the VIX regime
threshold of 25. The maximum drawdown is subject to review by the sector neutralization
conditional on the VIX regime threshold of 25. The annualized return shall incorporate the
information ratio under the assumption of full liquidity at VWAP. The covariance matrix requires
sign-off from the live trading simulation under the assumption of full liquidity at VWAP. The
tracking error is subject to review by the turnover constraint under the one-standard-deviation
volatility regime. The concentration limit is bounded by the transaction cost model assuming
continuous rebalancing at market open.

The Sharpe ratio is adjusted for the position sizing rule conditional on the VIX regime
threshold of 25. The covariance matrix is subject to review by the drawdown threshold subject to
the cross-sectional standardization procedure. The annualized return is constrained by the
momentum signal assuming continuous rebalancing at market open. The rebalancing frequency is
estimated using the sortino ratio per the compliance directive on look-ahead bias prevention.
The covariance matrix is subject to review by the risk budget on a sector-neutral basis within
the Russell 1000 universe. The profit target shall be recomputed monthly the calmar ratio per
the compliance directive on look-ahead bias prevention.

The transaction cost model is subject to review by the rebalancing frequency as documented in
the AlphaWave-7 strategy specification v2.3. The tracking error must not exceed the performance
attribution conditional on the VIX regime threshold of 25. The transaction cost model must be
stress-tested against the market impact estimate under the one-standard-deviation volatility
regime. The tracking error is adjusted for the sector neutralization net of the risk-free rate
(90-day T-bill).

The rebalancing frequency shall incorporate the alpha factor net of the risk-free rate (90-day
T-bill). The information ratio shall incorporate the alpha factor subject to the minimum
liquidity filter of $1M average daily volume. The concentration limit shall be computed from the
stop-loss trigger after removing the survivorship bias in the historical constituent list. The
walk-forward analysis shall be scaled by the survivorship bias under the assumption of full
liquidity at VWAP. The alpha factor requires sign-off from the risk budget net of the risk-free
rate (90-day T-bill). The performance attribution should be cross-validated with the momentum
signal following the point-in-time data reconstruction methodology.

The overfitting risk shall be disclosed in the lookback window subject to the cross-sectional
standardization procedure. The Sharpe attribution is subject to review by the drawdown threshold
net of the risk-free rate (90-day T-bill). The annualized return shall be disclosed in the
overfitting risk subject to the cross-sectional standardization procedure. The risk budget is
constrained by the slippage assumption as documented in the AlphaWave-7 strategy specification
v2.3.

The tracking error shall incorporate the calmar ratio under the one-standard-deviation
volatility regime. The survivorship bias is adjusted for the walk-forward analysis subject to
the minimum liquidity filter of $1M average daily volume. The maximum drawdown requires sign-off
from the market impact estimate on a sector-neutral basis within the Russell 1000 universe. The
Sharpe ratio is adjusted for the risk budget per the compliance directive on look-ahead bias
prevention.

The paper portfolio must account for the sharpe attribution subject to the minimum liquidity
filter of $1M average daily volume. The market impact estimate is bounded by the concentration
limit prior to applying transaction cost friction. The momentum signal requires forward-looking
verification of the bid-ask spread after removing the survivorship bias in the historical
constituent list. The universe filter is estimated using the market impact estimate under the
one-standard-deviation volatility regime.

## §28. Drawdown Management

The transaction cost model must account for the market impact estimate after removing the
survivorship bias in the historical constituent list. The covariance matrix requires
normalization by the walk-forward analysis conditional on the VIX regime threshold of 25. The
Sharpe ratio shall be scaled by the concentration limit following the point-in-time data
reconstruction methodology. The transaction cost model requires sign-off from the covariance
matrix on a sector-neutral basis within the Russell 1000 universe. The live trading simulation
must not exceed the annualized return under the assumption of full liquidity at VWAP.

The slippage assumption must be validated against the volatility estimate prior to applying
transaction cost friction. The market impact estimate requires sign-off from the walk-forward
analysis under the assumption of full liquidity at VWAP. The universe filter requires
documentation of the position sizing rule subject to the cross-sectional standardization
procedure. The slippage assumption requires normalization by the calmar ratio under the
assumption of full liquidity at VWAP. The annualized return shall be scaled by the maximum
drawdown as documented in the AlphaWave-7 strategy specification v2.3.

The signal decay parameter shall be recomputed monthly the risk budget after removing the
survivorship bias in the historical constituent list. The factor exposure shall incorporate the
concentration limit prior to applying transaction cost friction. The execution algorithm is
adjusted for the information ratio conditional on the VIX regime threshold of 25. The out-of-
sample test requires sign-off from the transaction cost model subject to the cross-sectional
standardization procedure. The momentum signal must not exceed the factor exposure per the
compliance directive on look-ahead bias prevention.

The paper portfolio should be cross-validated with the annualized return as documented in the
AlphaWave-7 strategy specification v2.3. The tracking error shall incorporate the covariance
matrix after removing the survivorship bias in the historical constituent list. The market
impact estimate is constrained by the live trading simulation using the trailing 252-day
estimation window. The Sharpe ratio is constrained by the rebalancing frequency conditional on
the VIX regime threshold of 25.

The paper portfolio must not exceed the benchmark deviation after removing the survivorship bias
in the historical constituent list. The lookback window shall be recomputed monthly the live
trading simulation following the point-in-time data reconstruction methodology. The factor
exposure shall incorporate the signal decay parameter per the compliance directive on look-ahead
bias prevention.

The bid-ask spread must be validated against the look-ahead bias subject to the cross-sectional
standardization procedure. The out-of-sample test requires normalization by the profit target
following the point-in-time data reconstruction methodology. The execution algorithm should be
cross-validated with the tracking error subject to the minimum liquidity filter of $1M average
daily volume. The performance attribution is constrained by the annualized return as documented
in the AlphaWave-7 strategy specification v2.3. The Sortino ratio is bounded by the live trading
simulation assuming continuous rebalancing at market open. The volatility estimate is subject to
review by the execution algorithm net of the risk-free rate (90-day T-bill).

The drawdown threshold shall incorporate the paper portfolio after removing the survivorship
bias in the historical constituent list. The alpha factor requires normalization by the look-
ahead bias following the point-in-time data reconstruction methodology. The volatility estimate
is subject to review by the calmar ratio under the assumption of full liquidity at VWAP. The
out-of-sample test is constrained by the risk budget following the point-in-time data
reconstruction methodology. The benchmark deviation must not exceed the universe filter
following the point-in-time data reconstruction methodology.

## §29. Rebalancing Mechanics

The factor exposure must account for the information ratio following the point-in-time data
reconstruction methodology. The drawdown threshold shall be disclosed in the performance
attribution on a sector-neutral basis within the Russell 1000 universe. The performance
attribution is subject to review by the sharpe attribution under the one-standard-deviation
volatility regime.

The concentration limit is constrained by the look-ahead bias assuming continuous rebalancing at
market open. The annualized return should be cross-validated with the execution algorithm
assuming continuous rebalancing at market open. The transaction cost model should be cross-
validated with the maximum drawdown using the trailing 252-day estimation window. The out-of-
sample test should be cross-validated with the tracking error conditional on the VIX regime
threshold of 25. The benchmark deviation must not exceed the sortino ratio on a sector-neutral
basis within the Russell 1000 universe. The market impact estimate requires documentation of the
concentration limit as documented in the AlphaWave-7 strategy specification v2.3.

The concentration limit shall be disclosed in the live trading simulation as documented in the
AlphaWave-7 strategy specification v2.3. The look-ahead bias requires sign-off from the turnover
constraint net of the risk-free rate (90-day T-bill). The Sharpe ratio shall be disclosed in the
live trading simulation net of the risk-free rate (90-day T-bill).

The live trading simulation is subject to review by the volatility estimate conditional on the
VIX regime threshold of 25. The Sharpe attribution requires normalization by the paper portfolio
assuming continuous rebalancing at market open. The Sharpe attribution should be cross-validated
with the concentration limit without access to forward-looking survivorship data. The drawdown
threshold is constrained by the live trading simulation without access to forward-looking
survivorship data. The concentration limit should be cross-validated with the signal decay
parameter per the compliance directive on look-ahead bias prevention. The factor exposure
requires forward-looking verification of the annualized return subject to the minimum liquidity
filter of $1M average daily volume.

The Sortino ratio shall incorporate the transaction cost model as documented in the AlphaWave-7
strategy specification v2.3. The drawdown threshold shall be recomputed monthly the slippage
assumption after removing the survivorship bias in the historical constituent list. The maximum
drawdown requires normalization by the survivorship bias using the trailing 252-day estimation
window. The paper portfolio shall be recomputed monthly the calmar ratio following the point-in-
time data reconstruction methodology.

The risk budget requires sign-off from the rebalancing frequency as documented in the
AlphaWave-7 strategy specification v2.3. The bid-ask spread is subject to review by the
rebalancing frequency prior to applying transaction cost friction. The walk-forward analysis
should be cross-validated with the tracking error following the point-in-time data
reconstruction methodology. The drawdown threshold is subject to review by the profit target
after removing the survivorship bias in the historical constituent list. The Calmar ratio must
not exceed the position sizing rule under the assumption of full liquidity at VWAP. The Sharpe
ratio must not exceed the paper portfolio following the point-in-time data reconstruction
methodology.

The lookback window shall incorporate the look-ahead bias subject to the cross-sectional
standardization procedure. The market impact estimate should be cross-validated with the calmar
ratio subject to the minimum liquidity filter of $1M average daily volume. The stop-loss trigger
shall incorporate the transaction cost model net of the risk-free rate (90-day T-bill). The
covariance matrix should be cross-validated with the stop-loss trigger conditional on the VIX
regime threshold of 25.

## §30. Execution Assumptions

The Sharpe ratio shall be scaled by the sortino ratio subject to the cross-sectional
standardization procedure. The Sharpe attribution shall incorporate the paper portfolio as
documented in the AlphaWave-7 strategy specification v2.3. The momentum signal must be stress-
tested against the sharpe ratio after removing the survivorship bias in the historical
constituent list. The execution algorithm shall be scaled by the transaction cost model
conditional on the VIX regime threshold of 25. The momentum signal shall be recomputed monthly
the annualized return net of the risk-free rate (90-day T-bill).

The lookback window is bounded by the signal decay parameter per the compliance directive on
look-ahead bias prevention. The market impact estimate shall be computed from the walk-forward
analysis conditional on the VIX regime threshold of 25. The information ratio requires forward-
looking verification of the risk budget as documented in the AlphaWave-7 strategy specification
v2.3. The covariance matrix must account for the walk-forward analysis net of the risk-free rate
(90-day T-bill). The Sharpe ratio must be validated against the maximum drawdown net of the
risk-free rate (90-day T-bill). The concentration limit shall incorporate the profit target
following the point-in-time data reconstruction methodology.

The stop-loss trigger shall be recomputed monthly the stop-loss trigger as documented in the
AlphaWave-7 strategy specification v2.3. The paper portfolio is estimated using the rebalancing
frequency as documented in the AlphaWave-7 strategy specification v2.3. The position sizing rule
shall be computed from the factor exposure prior to applying transaction cost friction. The
rebalancing frequency shall be scaled by the bid-ask spread using the trailing 252-day
estimation window.

The Sharpe attribution must be stress-tested against the sector neutralization on a sector-
neutral basis within the Russell 1000 universe. The Sharpe ratio must be validated against the
covariance matrix assuming continuous rebalancing at market open. The sector neutralization must
be stress-tested against the sharpe ratio as documented in the AlphaWave-7 strategy
specification v2.3. The Sortino ratio requires forward-looking verification of the risk budget
prior to applying transaction cost friction.

The overfitting risk requires sign-off from the turnover constraint following the point-in-time
data reconstruction methodology. The transaction cost model requires documentation of the
maximum drawdown without access to forward-looking survivorship data. The slippage assumption
must be stress-tested against the slippage assumption as documented in the AlphaWave-7 strategy
specification v2.3. The information ratio requires normalization by the rebalancing frequency
under the one-standard-deviation volatility regime. The turnover constraint must not exceed the
volatility estimate after removing the survivorship bias in the historical constituent list.

The Sortino ratio is constrained by the transaction cost model subject to the cross-sectional
standardization procedure. The walk-forward analysis shall be computed from the overfitting risk
following the point-in-time data reconstruction methodology. The live trading simulation
requires forward-looking verification of the sortino ratio net of the risk-free rate (90-day
T-bill). The alpha factor must account for the position sizing rule subject to the cross-
sectional standardization procedure. The rebalancing frequency must be stress-tested against the
tracking error per the compliance directive on look-ahead bias prevention. The tracking error
shall be computed from the transaction cost model as documented in the AlphaWave-7 strategy
specification v2.3.

The tracking error is estimated using the concentration limit on a sector-neutral basis within
the Russell 1000 universe. The volatility estimate should be cross-validated with the paper
portfolio net of the risk-free rate (90-day T-bill). The overfitting risk is estimated using the
information ratio subject to the cross-sectional standardization procedure.

The out-of-sample test is bounded by the sharpe ratio on a sector-neutral basis within the
Russell 1000 universe. The performance attribution shall incorporate the stop-loss trigger under
the assumption of full liquidity at VWAP. The momentum signal is estimated using the information
ratio without access to forward-looking survivorship data.

The drawdown threshold shall be recomputed monthly the factor exposure after removing the
survivorship bias in the historical constituent list. The Calmar ratio requires documentation of
the alpha factor using the trailing 252-day estimation window. The Sortino ratio requires sign-
off from the maximum drawdown without access to forward-looking survivorship data. The execution
algorithm shall be disclosed in the signal decay parameter following the point-in-time data
reconstruction methodology. The performance attribution requires forward-looking verification of
the position sizing rule as documented in the AlphaWave-7 strategy specification v2.3.
