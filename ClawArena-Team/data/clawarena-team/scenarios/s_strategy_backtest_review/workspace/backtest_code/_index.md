# backtest_code/ — AlphaWave-7 Backtest Engine

- `backtest_engine.py` — Main backtest engine (~300 lines). Contains the
  signal computation logic. **Note from quant team**: there is a TODO comment
  near the signal computation that flags a timestamp alignment issue.
- `universe_filter.py` — Universe construction and survivorship handling.
- `signal_generator.py` — Momentum signal computation helpers.
- `config.yaml` — Strategy configuration (commission, slippage, universe filters).
- `tests/` — pytest test suite. Run via `bash tools/run_backtest_tests.sh`.
  - `conftest.py` — shared fixtures
  - `test_signal.py` — signal alignment tests (includes TestSignalAlignment)
  - `test_risk.py` — risk model tests
