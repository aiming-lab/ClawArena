# Migration Runbook (Bronze → Silver → Gold)

1. Bronze: ingest raw monthly extracts into DuckDB, conforming to schema_v2.
2. Silver: apply quality_rules (drop negative fares, out-of-range timestamps, extreme distance),
   join taxi_zone_lookup for Borough, dedup.
3. Gold: daily aggregates + payment-type × borough pivots for Carol's reporting.

House style: four-decimal numerics; verbatim field names; scripts carry shebang + utf-8 header.
