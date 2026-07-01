# Written DD Questionnaire Responses — Apex Capital Management Fund II

**Respondent:** Kai Yamamoto, Portfolio Manager, Apex Capital Management
**Date of response:** 2026-05-10
**To:** Jordan Mercer, Meridian Capital Advisors
**Re:** Preliminary DD Questionnaire — Apex Systematic Fund II

---

## Section 1: Strategy Overview

**Q1.1: Please provide a brief description of the investment strategy and the primary sources
of alpha generation.**

Apex Systematic Fund II employs a quantitative long/short equity strategy targeting systematic
alpha through multi-factor signal construction across the US equity universe. The primary alpha
sources are: (i) medium-term price momentum signals with a holding period of approximately
twenty to sixty trading days; (ii) earnings revision and estimate dispersion signals derived
from consensus analyst forecast data; (iii) quality and profitability factors incorporating
balance sheet metrics; and (iv) sentiment signals derived from alternative data including
news flow analytics and options market activity.

The portfolio is constructed through a constrained mean-variance optimisation framework
that maximises the information ratio subject to sector neutralisation, factor neutralisation,
and turnover constraints. The rebalancing frequency is weekly with intra-week execution
triggered by signal threshold breaches.

**Q1.2: How long has the current strategy been in live operation?**

The current strategy, as reflected in Apex Fund II, has been in live operation since the fund's
inception on 2023-01-01. Prior to that date, the portfolio manager operated a predecessor fund
(Apex Capital Management Fund I, a different strategy vehicle with different signal construction)
which was wound down in 2022. The backtest data provided covers 2018-01-02 to 2025-12-31 and
incorporates live performance data from 2023-01-01 onward.

**Q1.3: Has the strategy undergone any material changes since inception?**

No material changes to the investment strategy have been made since the fund's inception. The
signal weights and optimisation constraints have been subject to minor calibration adjustments
within the bounds described in the strategy documentation, consistent with the portfolio
manager's ongoing model maintenance responsibilities. All calibration changes are logged and
available for review in the strategy documentation.

---

## Section 2: Performance and Backtest Methodology

**Q2.1: Please confirm the Sharpe ratio cited in the pitch deck and describe the computation
methodology.**

The pitch deck states a Sharpe ratio of 2.41 for the 2018–2025 backtest period. This figure
is computed as the annualised mean excess return divided by the annualised standard deviation
of excess returns, where excess return is computed as the daily strategy return minus the
contemporaneous US three-month T-bill rate. The figure is computed on all available data
points in the backtest export file for the stated period.

We believe this figure accurately reflects the strategy's risk-adjusted performance
characteristics as demonstrated by the backtest. The strategy employs a conservative backtest
methodology that incorporates realistic transaction cost assumptions and avoids the use of
in-sample parameter optimisation on the final held-out test period.

**Q2.2: Please describe the data augmentation technique referenced in prior correspondence
and explain how it is reflected in the backtest data.**

The backtest file provided to prospective LPs includes certain rows that utilise a proprietary
data augmentation technique designed to improve the stability of signal estimation during
periods of low cross-sectional volatility. This technique generates synthetic return observations
that are statistically consistent with the observed return distribution and are used internally
to improve signal calibration. These augmented observations are included in the backtest export
as additional data points.

We believe the inclusion of augmented observations in the Sharpe computation is methodologically
defensible given that they are statistically indistinguishable from live observations. The column
`synthetic_aug` in the CSV flags these rows for transparency, though we recommend treating them
as valid data points in any performance analysis.

**Q2.3: What is the maximum drawdown over the backtest period?**

The maximum drawdown over the full 2018–2025 backtest period is approximately negative 8.3%.
This occurs during the volatility regime of 2022. The drawdown recovery period was approximately
seven months following the trough.

---

## Section 3: Fees and LP Economics

**Q3.1: Please confirm the fund's fee structure.**

Apex Capital Management Fund II charges a management fee of 1.5% per annum of net asset value,
accrued daily and payable quarterly, and a performance allocation of 20% of net profits above
a 6% per annum hurdle rate, subject to a high-water mark provision. No other fees are charged
to the fund. The general partner does not charge any organisational, placement, or monitoring
fees to the fund.

**Q3.2: Please provide the net-of-fees Sharpe ratio for the live performance period.**

Net performance data is fully covered in our monthly performance reports which are provided
to all prospective LPs as part of the standard DD package. The monthly reports contain a
complete breakdown of performance attribution including all fee deductions. We would direct
you to review those reports for the precise net-of-fees figures, as they are computed on a
monthly basis consistent with the fund's accounting procedures.

**Q3.3: What is the hurdle rate mechanism, and how does it interact with the high-water mark?**

The 6% per annum hurdle rate is a hard hurdle, meaning the performance allocation applies
only to profits above the hurdle. The high-water mark ensures that the performance allocation
is not charged on recovery of prior losses. The hurdle rate is computed on a simple daily
accrual basis (6% / 252 per trading day). Performance allocation is calculated and accrued
monthly but crystallised annually at the December 31 year-end.

---

## Section 4: Risk Management

**Q4.1: Please describe the fund's risk management framework and key risk limits.**

The fund's risk management framework is described in detail in the risk framework document
included in the DD package. Key limits include: maximum gross leverage of 3.5x notional;
net exposure range of negative 20% to positive 30% of NAV; single-stock position limit of
2.5% of NAV on the long side and 1.5% on the short side; sector concentration limit of
25% net exposure per GICS sector; and a portfolio-level 1-day 99% VaR limit of 1.5% of NAV.

The portfolio manager has discretion to reduce gross leverage below 2x during periods of
elevated market stress as defined by a 30-day realised volatility trigger.

**Q4.2: How does the fund handle model risk and overfitting in the signal construction?**

Model risk is managed through a rigorous out-of-sample testing protocol applied to all
signal additions and modifications. The primary out-of-sample test window covers the most
recent twenty-four months of data, which is held out of all signal calibration procedures.
Cross-validation is employed for parameter estimation. The portfolio manager reviews the
information coefficient and alpha decay of each signal quarterly and depreciates signals
whose live performance diverges materially from backtest expectations.

---

## Section 5: Operational and Compliance

**Q5.1: Who are the fund's service providers?**

Prime brokerage: Goldman Sachs Prime Services and Morgan Stanley Prime Brokerage (dual prime).
Fund administrator: Citco Fund Services, responsible for independent NAV calculation and
investor reporting. Auditor: Ernst & Young LLP, New York. Legal counsel: Schulte Roth & Zabel
(fund formation and ongoing) and Davis Polk & Wardwell (regulatory). Data vendors include
FactSet, Bloomberg, and a proprietary alternative data aggregator.

**Q5.2: Has the fund or the investment manager been subject to any regulatory actions or
investor disputes?**

Neither Apex Capital Management nor the Fund has been subject to any SEC enforcement action,
formal examination findings, investor dispute resolution proceedings, or material litigation.
The investment manager's Form ADV Part 2 is current and available upon request.

---

*These responses are provided in good faith by Kai Yamamoto on behalf of Apex Capital
Management. They are subject to the disclaimers set forth in the Fund's offering documents.*
