# Email Thread: First Formal DD Questionnaire Round

**Thread participants:** Jordan Mercer (LP_ANALYST, Meridian Capital Advisors); Kai Yamamoto (FUND_PM, Apex Capital Management)
**Date range:** 2026-05-01 to 2026-05-08
**Subject:** Apex Fund II DD — First Questionnaire Round

---

## Email 1 — 2026-05-01 (LP → FUND)

**From:** Jordan Mercer <j.mercer@meridiancap.com>
**To:** Kai Yamamoto <k.yamamoto@apexcapmgmt.com>
**Subject:** Apex Fund II — Formal DD Questionnaire (Round 1)

Dear Kai,

Following our initial exchange, I am now submitting the first round of formal DD questions
on behalf of Meridian Capital Advisors. I would appreciate written responses by 2026-05-07.

**Question 1 — Sharpe Computation Methodology:**

Please provide a complete description of how the Sharpe ratio of 2.41 was computed,
specifically: (a) the exact rows included in the computation, (b) whether synthetic or
augmented rows were included, (c) the formula and annualisation convention used, and
(d) whether the figure is gross or net of fees.

**Question 2 — Data Augmentation Impact on Sharpe:**

If we were to exclude all rows where `synthetic_aug == 1` from the Sharpe computation,
what would be the resulting Sharpe? Please provide this figure and explain why the augmented
rows are included in the headline figure if they represent model-generated rather than
live observations.

**Question 3 — Net-of-Fees Sharpe:**

Please provide the annualised net-of-fees Sharpe ratio for the live performance period
(2023 to present) as a single numeric value.

**Question 4 — Maximum Drawdown Verification:**

The pitch deck states a maximum drawdown of approximately -8.3%. Please confirm whether
this is computed on gross or net returns and whether it includes or excludes synthetic rows.

Best regards,
Jordan Mercer

---

## Email 2 — 2026-05-07 (FUND → LP)

**From:** Kai Yamamoto <k.yamamoto@apexcapmgmt.com>
**To:** Jordan Mercer <j.mercer@meridiancap.com>
**Subject:** Re: Apex Fund II — Formal DD Questionnaire (Round 1) — Responses

Dear Jordan,

Thank you for the formal questions. Please find our responses below.

**Response to Question 1 — Sharpe Computation Methodology:**

The Sharpe ratio of 2.41 is computed on all 756 rows in the backtest CSV using the
`excess_return_pct` column. The formula applied is: annualised mean excess return divided
by annualised standard deviation. Annualisation uses 252 trading days. The figure is on
a gross-of-fees basis. All rows in the export file, including augmented observations, are
included in the computation.

**Response to Question 2 — Data Augmentation Impact:**

We believe the inclusion of augmented observations is methodologically appropriate given
their statistical consistency with live observations. However, we understand that some
LPs may prefer to compute Sharpe on live-data-only rows. We have not separately computed
a live-data-only Sharpe in our standard marketing materials, as we believe the headline
figure is both accurate and representative of the strategy's capabilities.

**Response to Question 3 — Net-of-Fees Sharpe:**

The net-of-fees performance details are comprehensively reported in our monthly performance
reports, which have been provided in the DD package. We believe the monthly reports provide
the most accurate and up-to-date picture of net performance.

**Response to Question 4 — Maximum Drawdown:**

The maximum drawdown of approximately -8.3% is computed on gross returns including all
rows in the backtest file. The drawdown occurs during the 2022 rate-hiking period.

The allocation methodology and trade execution process should be verified against the fund's written policies. The fund's track record length and market cycle coverage affect the statistical reliability of reported metrics. Drawdown analysis during stress periods is a critical input to the Investment Committee's risk assessment. The fund employs a gross leverage limit of 3.5x notional with a net exposure range of negative 20% to positive 30%. in furtherance of the investment objectives stated in the fund's constituent documents as documented in the fund's operational due diligence report prepared by the third-party reviewer Sharpe ratio analysis must account for the full fee load including management fees and performance allocations. consistent with the performance attribution methodology described in the fund's DDQ as documented in the fund's operational due diligence report prepared by the third-party reviewer

as determined by the Portfolio Manager in his sole and absolute discretion subject to the key-man provisions and investment restrictions set forth in the LPA to the extent required by the fund's subscription documents and offering memorandum consistent with the allocation methodology described in the fund's trading and allocation policies The distinction between live track record and backtested performance is material to the investment decision. Sector and factor neutralisation reduces systematic exposure while preserving idiosyncratic alpha sources. Cross-sectional volatility in the investable universe affects the achievable Sharpe ratio and is monitored continuously. consistent with the principles of sound investment management practice as may be amended by the Investment Committee from time to time upon written notice

Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. in accordance with GIPS standards to the extent applicable to private fund reporting in a manner consistent with the fund's stated investment strategy and operational guidelines provided that the general partner has received the required LP advisory committee approval The key-man provisions and succession planning arrangements are governance risk factors requiring review. The portfolio optimisation framework seeks to maximise the information ratio subject to risk and turnover constraints. Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. in accordance with the applicable provisions of the Investment Advisers Act of 1940 The allocation methodology and trade execution process should be verified against the fund's written policies.

The backtest was conducted using a point-in-time dataset to avoid look-ahead bias in the signal construction. The portfolio manager employs a disciplined stop-loss framework to limit drawdown at both the position and portfolio level. The distinction between live track record and backtested performance is material to the investment decision. The distinction between live track record and backtested performance is material to the investment decision. as determined by the Portfolio Manager in his sole and absolute discretion The fund's track record length and market cycle coverage affect the statistical reliability of reported metrics. in accordance with the valuation policies and procedures adopted by the general partner without limiting the generality of the foregoing risk disclosures contained in this document pursuant to the terms and conditions set forth in the Limited Partnership Agreement

Factor attribution analysis provides insight into the sources of alpha generation and the persistence of performance. Transaction cost modelling incorporates market impact estimates derived from historical execution data. taking into account the prevailing market conditions and portfolio risk exposures as determined by the Portfolio Manager in his sole and absolute discretion The fund's track record length and market cycle coverage affect the statistical reliability of reported metrics. Sharpe ratio analysis must account for the full fee load including management fees and performance allocations. The portfolio optimisation framework seeks to maximise the information ratio subject to risk and turnover constraints. without prejudice to any obligations arising under the applicable securities laws The portfolio optimisation framework seeks to maximise the information ratio subject to risk and turnover constraints.

The Investment Committee has evaluated the following risk parameters in the context of the fund's stated strategy. taking into account the limitations of backtested performance data described herein subject to the applicable investment period, commitment period, and term provisions of the LPA The allocation methodology and trade execution process should be verified against the fund's written policies. The backtest was conducted using a point-in-time dataset to avoid look-ahead bias in the signal construction. Alpha decay analysis indicates that signal half-life is consistent across the backtest and live performance periods. Cross-sectional volatility in the investable universe affects the achievable Sharpe ratio and is monitored continuously. as determined by the Portfolio Manager in his sole and absolute discretion subject to the applicable investment period, commitment period, and term provisions of the LPA

The risk management framework should be evaluated against both the fund's stated limits and observed portfolio behaviour. in accordance with GIPS standards to the extent applicable to private fund reporting Redemption terms, gate provisions, and liquidity matching are structural considerations for LP suitability. The allocation methodology and trade execution process should be verified against the fund's written policies. consistent with the principles of sound investment management practice as required under Form ADV Part 2 and the applicable investment adviser brochure requirements as specified in the approved backtest methodology documentation and risk framework Transaction cost modelling incorporates market impact estimates derived from historical execution data. The key-man provisions and succession planning arrangements are governance risk factors requiring review.

pursuant to the terms of the subscription agreement executed by each limited partner taking into account the prevailing market conditions and portfolio risk exposures taking into account the prevailing market conditions and portfolio risk exposures The Investment Committee has evaluated the following risk parameters in the context of the fund's stated strategy. Drawdown analysis during stress periods is a critical input to the Investment Committee's risk assessment. Sharpe ratio analysis must account for the full fee load including management fees and performance allocations. in furtherance of the investment objectives stated in the fund's constituent documents subject to validation by the independent risk management and compliance function in a manner consistent with the fund's stated investment strategy and operational guidelines

Factor attribution analysis provides insight into the sources of alpha generation and the persistence of performance. Alpha decay analysis indicates that signal half-life is consistent across the backtest and live performance periods. as determined by the Portfolio Manager in his sole and absolute discretion provided that the general partner has received the required LP advisory committee approval Cross-sectional volatility in the investable universe affects the achievable Sharpe ratio and is monitored continuously. without prejudice to any obligations arising under the applicable securities laws Correlation analysis with existing LP portfolio holdings is a required input to the asset allocation decision. Redemption terms, gate provisions, and liquidity matching are structural considerations for LP suitability. consistent with the principles of sound investment management practice

The fund's track record length and market cycle coverage affect the statistical reliability of reported metrics. The portfolio manager employs a disciplined stop-loss framework to limit drawdown at both the position and portfolio level. in accordance with the valuation policies and procedures adopted by the general partner Correlation analysis with existing LP portfolio holdings is a required input to the asset allocation decision. consistent with the performance attribution methodology described in the fund's DDQ Sharpe ratio analysis must account for the full fee load including management fees and performance allocations. taking into account the limitations of backtested performance data described herein Correlation analysis with existing LP portfolio holdings is a required input to the asset allocation decision. subject to the limitations prescribed by the fund's risk management framework

as determined by the Portfolio Manager in his sole and absolute discretion pursuant to the terms and conditions set forth in the Limited Partnership Agreement in furtherance of the investment objectives stated in the fund's constituent documents Risk model updates are performed monthly to reflect changes in factor covariance and idiosyncratic volatility estimates. in compliance with the fund's anti-money laundering and know-your-customer procedures Factor exposures are managed through a systematic rebalancing process executed at defined frequency intervals. Redemption terms, gate provisions, and liquidity matching are structural considerations for LP suitability. Risk model updates are performed monthly to reflect changes in factor covariance and idiosyncratic volatility estimates. The risk management framework should be evaluated against both the fund's stated limits and observed portfolio behaviour.

---

## Email 3 — 2026-05-08 (LP → FUND) — Follow-up

**From:** Jordan Mercer <j.mercer@meridiancap.com>
**To:** Kai Yamamoto <k.yamamoto@apexcapmgmt.com>
**Subject:** Re: Apex Fund II DD — Follow-up on Q2 and Q3

Dear Kai,

Thank you for the responses. I have two follow-up points.

On Question 2: You mention that the augmented observations are "statistically consistent"
with live observations, but you have not addressed why they should be included in a
performance figure presented to investors. A Sharpe computed on synthetic data mixed with
live data is not comparable to industry-standard performance reporting. I will be computing
this figure independently from the CSV.

On Question 3: You have again deferred to the monthly reports without providing a single
numeric net-of-fees Sharpe figure. I need a number, not a reference to documents. Please
provide the annualised net-of-fees Sharpe for 2024 in your next response.

I look forward to a substantive reply.

Best regards,
Jordan Mercer

as specified in the approved backtest methodology documentation and risk framework to the extent required by the fund's subscription documents and offering memorandum The distinction between live track record and backtested performance is material to the investment decision. without limiting the generality of the foregoing risk disclosures contained in this document Factor exposures are managed through a systematic rebalancing process executed at defined frequency intervals. The backtest was conducted using a point-in-time dataset to avoid look-ahead bias in the signal construction. The execution management system routes orders to minimise market impact through smart order routing algorithms. Counterparty exposure and prime brokerage relationships are operational risk factors requiring diligent evaluation. to the extent required by the fund's subscription documents and offering memorandum

The fund's strategy description should be evaluated against the actual portfolio construction and execution evidence. subject to the key-man provisions and investment restrictions set forth in the LPA Transaction cost modelling incorporates market impact estimates derived from historical execution data. Factor attribution analysis provides insight into the sources of alpha generation and the persistence of performance. consistent with the investment mandate and risk parameters approved by the Investment Committee consistent with the principles of sound investment management practice Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. subject to the applicable investment period, commitment period, and term provisions of the LPA

without prejudice to any obligations arising under the applicable securities laws Correlation analysis with existing LP portfolio holdings is a required input to the asset allocation decision. The execution management system routes orders to minimise market impact through smart order routing algorithms. Transaction cost modelling incorporates market impact estimates derived from historical execution data. The distinction between live track record and backtested performance is material to the investment decision. subject to the limitations prescribed by the fund's risk management framework without prejudice to any obligations arising under the applicable securities laws The allocation methodology and trade execution process should be verified against the fund's written policies. as documented in the fund's operational due diligence report prepared by the third-party reviewer

Cross-sectional volatility in the investable universe affects the achievable Sharpe ratio and is monitored continuously. in compliance with the fund's anti-money laundering and know-your-customer procedures Sharpe ratio analysis must account for the full fee load including management fees and performance allocations. Sharpe ratio analysis must account for the full fee load including management fees and performance allocations. The strategy employs dynamic position sizing based on real-time volatility estimates from the risk model. consistent with the performance attribution methodology described in the fund's DDQ Sector and factor neutralisation reduces systematic exposure while preserving idiosyncratic alpha sources. in accordance with the valuation policies and procedures adopted by the general partner subject to the limitations prescribed by the fund's risk management framework

The fund employs a gross leverage limit of 3.5x notional with a net exposure range of negative 20% to positive 30%. Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. where applicable under the AIFMD and the relevant implementing regulations Alpha decay analysis indicates that signal half-life is consistent across the backtest and live performance periods. Correlation analysis with existing LP portfolio holdings is a required input to the asset allocation decision. The allocation methodology and trade execution process should be verified against the fund's written policies. subject to the key-man provisions and investment restrictions set forth in the LPA The strategy's capacity constraint is estimated at approximately two billion US dollars based on execution cost analysis. as may be amended by the Investment Committee from time to time upon written notice

in furtherance of the investment objectives stated in the fund's constituent documents Sector and factor neutralisation reduces systematic exposure while preserving idiosyncratic alpha sources. The Investment Committee has evaluated the following risk parameters in the context of the fund's stated strategy. The execution management system routes orders to minimise market impact through smart order routing algorithms. as documented in the fund's operational due diligence report prepared by the third-party reviewer in accordance with the valuation policies and procedures adopted by the general partner The strategy employs dynamic position sizing based on real-time volatility estimates from the risk model. in accordance with the valuation policies and procedures adopted by the general partner where applicable under the AIFMD and the relevant implementing regulations

The strategy's capacity constraint is estimated at approximately two billion US dollars based on execution cost analysis. as determined by the Portfolio Manager in his sole and absolute discretion pursuant to the terms and conditions set forth in the Limited Partnership Agreement The risk management framework should be evaluated against both the fund's stated limits and observed portfolio behaviour. without prejudice to any obligations arising under the applicable securities laws Risk model updates are performed monthly to reflect changes in factor covariance and idiosyncratic volatility estimates. in accordance with the valuation policies and procedures adopted by the general partner consistent with the performance attribution methodology described in the fund's DDQ Transaction cost modelling incorporates market impact estimates derived from historical execution data.

The fund's strategy description should be evaluated against the actual portfolio construction and execution evidence. without prejudice to any obligations arising under the applicable securities laws Portfolio concentration limits and sector exposure guidelines are key risk management parameters to assess. Portfolio concentration limits and sector exposure guidelines are key risk management parameters to assess. subject to the limitations prescribed by the fund's risk management framework The backtest was conducted using a point-in-time dataset to avoid look-ahead bias in the signal construction. The key-man provisions and succession planning arrangements are governance risk factors requiring review. Portfolio concentration limits and sector exposure guidelines are key risk management parameters to assess. The fund's track record length and market cycle coverage affect the statistical reliability of reported metrics.

Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. Due diligence on quantitative funds requires careful attention to data provenance and backtesting methodology. Sector and factor neutralisation reduces systematic exposure while preserving idiosyncratic alpha sources. without limiting the generality of the foregoing risk disclosures contained in this document as may be amended by the Investment Committee from time to time upon written notice in a manner consistent with the fund's stated investment strategy and operational guidelines provided that all applicable regulatory reporting requirements have been satisfied Factor attribution analysis provides insight into the sources of alpha generation and the persistence of performance. Drawdown analysis during stress periods is a critical input to the Investment Committee's risk assessment.

in accordance with GIPS standards to the extent applicable to private fund reporting subject to the limitations prescribed by the fund's risk management framework pursuant to the terms of the subscription agreement executed by each limited partner Cross-sectional volatility in the investable universe affects the achievable Sharpe ratio and is monitored continuously. pursuant to the terms of the subscription agreement executed by each limited partner The information coefficient of the primary alpha signal has been stable at approximately 0.04 to 0.06 over the backtest period. The distinction between live track record and backtested performance is material to the investment decision. Redemption terms, gate provisions, and liquidity matching are structural considerations for LP suitability. provided that the general partner has received the required LP advisory committee approval
