# Working Principles

1. **Authoritative-source-first**: Ground-truth query plans and statistics live in
   `reports/explain_plans/` and `reports/pgstatstatements_snapshot.csv`. Bot-generated
   summaries (e.g. files named `*BOT*` or from the internal Slack bot) are convenience
   artefacts and NOT authoritative — verify any number against the actual EXPLAIN JSON or
   pg_stat_statements snapshot.

2. **Verbatim PostgreSQL identifiers**: Use exact parameter names from the PostgreSQL docs
   (e.g. `seq_page_cost`, `random_page_cost`, `cpu_tuple_cost`, `default_statistics_target`).
   Never invent abbreviations or aliases.

3. **Output directory discipline**: All work products (analysis JSON, DDL files, SQL scripts,
   reports) are written to the `work/` directory. Do NOT write deliverables to `reports/`,
   `configs/`, `db/`, `scripts/`, or `archive/`.

4. **Schema discipline**: JSON deliverables use snake_case field names exclusively.
   Never use camelCase or PascalCase in JSON output keys.

5. **Production DDL safety**: Every `CREATE INDEX` statement targeting the production database
   must use the `CONCURRENTLY` keyword to avoid table-locking.

6. **Temporal awareness**: Optimization recommendations arrive incrementally. When an
   authoritative notice supersedes a prior recommendation, the later instruction wins —
   revise prior outputs rather than stacking contradictory logic.

7. **Index-type accuracy**: Hash indexes support only equality (`=`) operations — they cannot
   satisfy range predicates (`<`, `>`, `BETWEEN`). Always select the correct index type for
   the query predicate pattern.
