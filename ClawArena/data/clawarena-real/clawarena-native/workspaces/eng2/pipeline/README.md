# Pipeline layout

Author your deliverables here as tasks require:
- `bronze/ingest.py`     — read raw parquet/csv into DuckDB (Bronze)
- `silver/clean.py`      — apply quality rules (Silver)
- `silver/enrich.py`     — join taxi_zone_lookup for Borough
- `gold/`                — aggregations

Config under `config/` is read-only reference (schema + quality rules).
