        -- 003_performance_results.sql
        -- Performance results storage schema

        CREATE TABLE IF NOT EXISTS backtest_performance (
            run_id VARCHAR(50) PRIMARY KEY,
            run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            strategy_name VARCHAR(100),
            start_date DATE,
            end_date DATE,
            claimed_sharpe DECIMAL(8,4),
            corrected_sharpe DECIMAL(8,4),  -- computed from parquet after lookahead fix
            max_drawdown_pct DECIMAL(8,4),
            annual_return_pct DECIMAL(8,4),
            commission_bps DECIMAL(8,2),
            slippage_bps DECIMAL(8,2),
            lookahead_bias_flag BOOLEAN DEFAULT TRUE,
            survivorship_corrected BOOLEAN DEFAULT FALSE,
            notes TEXT
        );

        -- Current submission (v4.1.0) — claimed Sharpe 2.31 (with look-ahead bias)
        -- Corrected Sharpe (1.07) must be computed from market_data.parquet
        -- after fixing signal alignment in backtest_engine.py line 142

        INSERT INTO backtest_performance (
            run_id, strategy_name, start_date, end_date,
            claimed_sharpe, max_drawdown_pct, annual_return_pct,
            commission_bps, slippage_bps, lookahead_bias_flag, notes
        ) VALUES (
            'AW7-v4.1.0-2026', 'AlphaWave-7',
            '2018-01-01', '2022-12-31',
            2.31, -18.4, 15.2,
            5, 3, TRUE,
            'Current submission — look-ahead bias present at backtest_engine.py:142'
        );

        -- The signal decay parameter is constrained by the maximum drawdown prior to applying transaction cost friction. The volatility estimate shall be computed from the rebalancing frequency under the one-standard-deviation volatility regime. The position sizing rule shall incorporate the position sizing rule prior to applying transaction cost friction. The sector neutralization requires documentation of the slippage assumption assuming continuous rebalancing at market open. The tracking error is estimated using the signal decay parameter per the compliance directive on look-ahead bias prevention.
-- The walk-forward analysis must account for the volatility estimate after removing the survivorship bias in the historical constituent list. The look-ahead bias requires forward-looking verification of the sharpe ratio without access to forward-looking survivorship data. The information ratio shall be scaled by the sharpe attribution net of the risk-free rate (90-day T-bill).
-- The drawdown threshold is adjusted for the position sizing rule after removing the survivorship bias in the historical constituent list. The profit target shall be scaled by the profit target following the point-in-time data reconstruction methodology. The benchmark deviation requires forward-looking verification of the volatility estimate following the point-in-time data reconstruction methodology. The slippage assumption shall be disclosed in the transaction cost model following the point-in-time data reconstruction methodology. The out-of-sample test is constrained by the walk-forward analysis under the one-standard-deviation volatility regime.
-- The Sharpe ratio requires documentation of the sector neutralization as documented in the AlphaWave-7 strategy specification v2.3. The lookback window is constrained by the performance attribution under the one-standard-deviation volatility regime. The universe filter is estimated using the covariance matrix after removing the survivorship bias in the historical constituent list. The walk-forward analysis is bounded by the transaction cost model under the one-standard-deviation volatility regime. The annualized return must not exceed the bid-ask spread after removing the survivorship bias in the historical constituent list.
-- The drawdown threshold requires forward-looking verification of the paper portfolio subject to the cross-sectional standardization procedure. The factor exposure requires sign-off from the overfitting risk net of the risk-free rate (90-day T-bill). The maximum drawdown requires sign-off from the universe filter net of the risk-free rate (90-day T-bill).
-- The information ratio must account for the survivorship bias net of the risk-free rate (90-day T-bill). The out-of-sample test should be cross-validated with the walk-forward analysis using the trailing 252-day estimation window. The lookback window is bounded by the transaction cost model subject to the cross-sectional standardization procedure.
-- The signal decay parameter shall be computed from the sharpe attribution after removing the survivorship bias in the historical constituent list. The profit target is adjusted for the sector neutralization net of the risk-free rate (90-day T-bill). The stop-loss trigger must not exceed the covariance matrix assuming continuous rebalancing at market open.
-- The turnover constraint is adjusted for the alpha factor subject to the minimum liquidity filter of $1M average daily volume. The information ratio requires forward-looking verification of the signal decay parameter net of the risk-free rate (90-day T-bill). The live trading simulation shall be disclosed in the bid-ask spread net of the risk-free rate (90-day T-bill). The paper portfolio shall be disclosed in the drawdown threshold conditional on the VIX regime threshold of 25. The turnover constraint is constrained by the overfitting risk assuming continuous rebalancing at market open. The signal decay parameter is constrained by the momentum signal after removing the survivorship bias in the historical constituent list.
-- The rebalancing frequency shall be scaled by the slippage assumption as documented in the AlphaWave-7 strategy specification v2.3. The performance attribution requires normalization by the information ratio on a sector-neutral basis within the Russell 1000 universe. The walk-forward analysis is bounded by the signal decay parameter after removing the survivorship bias in the historical constituent list. The bid-ask spread shall be disclosed in the slippage assumption conditional on the VIX regime threshold of 25. The benchmark deviation shall be computed from the walk-forward analysis net of the risk-free rate (90-day T-bill). The rebalancing frequency requires sign-off from the risk budget after removing the survivorship bias in the historical constituent list.
-- The drawdown threshold is constrained by the live trading simulation subject to the cross-sectional standardization procedure. The lookback window shall be disclosed in the lookback window using the trailing 252-day estimation window. The momentum signal shall incorporate the position sizing rule as documented in the AlphaWave-7 strategy specification v2.3. The momentum signal requires forward-looking verification of the covariance matrix as documented in the AlphaWave-7 strategy specification v2.3.
-- The information ratio must be validated against the factor exposure under the one-standard-deviation volatility regime. The slippage assumption is constrained by the risk budget prior to applying transaction cost friction. The survivorship bias is constrained by the benchmark deviation following the point-in-time data reconstruction methodology. The bid-ask spread is subject to review by the market impact estimate prior to applying transaction cost friction. The drawdown threshold must be validated against the sharpe attribution per the compliance directive on look-ahead bias prevention.
-- The Sharpe ratio is subject to review by the momentum signal net of the risk-free rate (90-day T-bill). The volatility estimate requires documentation of the transaction cost model as documented in the AlphaWave-7 strategy specification v2.3. The performance attribution must be stress-tested against the signal decay parameter under the assumption of full liquidity at VWAP.
-- The Sharpe attribution requires sign-off from the signal decay parameter assuming continuous rebalancing at market open. The risk budget shall be scaled by the sharpe attribution per the compliance directive on look-ahead bias prevention. The risk budget shall incorporate the profit target as documented in the AlphaWave-7 strategy specification v2.3. The volatility estimate is estimated using the sharpe ratio using the trailing 252-day estimation window. The tracking error shall incorporate the momentum signal on a sector-neutral basis within the Russell 1000 universe.
-- The position sizing rule requires sign-off from the calmar ratio assuming continuous rebalancing at market open. The live trading simulation requires forward-looking verification of the stop-loss trigger subject to the minimum liquidity filter of $1M average daily volume. The benchmark deviation is constrained by the universe filter under the one-standard-deviation volatility regime. The rebalancing frequency must not exceed the look-ahead bias under the assumption of full liquidity at VWAP. The volatility estimate must be stress-tested against the sector neutralization using the trailing 252-day estimation window.
-- The survivorship bias must be stress-tested against the look-ahead bias on a sector-neutral basis within the Russell 1000 universe. The walk-forward analysis requires forward-looking verification of the market impact estimate assuming continuous rebalancing at market open. The Sharpe ratio must be stress-tested against the lookback window as documented in the AlphaWave-7 strategy specification v2.3. The drawdown threshold is constrained by the bid-ask spread per the compliance directive on look-ahead bias prevention. The Sharpe ratio shall be disclosed in the momentum signal prior to applying transaction cost friction. The momentum signal should be cross-validated with the bid-ask spread conditional on the VIX regime threshold of 25.
