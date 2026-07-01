# data_pipeline/ index

SQL migration scripts for AlphaWave-7 data preparation pipeline.

- `001_create_tick_schema.sql` — creates tick_data and universe_constituents tables.
- `002_universe_survivorship_filter.sql` — applies listing-status filter.
  **Note**: This filter introduces survivorship bias by excluding delisted tickers.
  7 tickers are excluded (see voice_memos/researcher_memo.wav for authoritative count).
- `003_performance_results.sql` — performance metrics and backtest results storage.
