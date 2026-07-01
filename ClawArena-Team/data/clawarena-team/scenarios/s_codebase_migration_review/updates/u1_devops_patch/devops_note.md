# DevOps Update — 2026-05-26

Added `0043_split_safety.sql` as a follow-up to the PII-risk migration
`0042_pii_columns.sql`. This patch adds audit triggers and row-level security
policies to mitigate the risk identified in the shared_deps_audit.

Please evaluate how this patch interacts with `0042_pii_columns.sql` before
reaching a final merge decision.

— DevOps / Platform Team
