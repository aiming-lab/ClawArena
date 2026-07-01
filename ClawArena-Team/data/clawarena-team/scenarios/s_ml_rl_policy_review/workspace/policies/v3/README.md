# rotpen-rdd policy v3 (production)

Deployed: 2026-05-10. Stable; no incidents in the 12 days since deployment.

Architecture: PPO with a 2-stage curriculum (balance → swingup).
Hyperparameters frozen at QNET reference values (see `release_report_excerpts.md`).

`policy_v3.zip.placeholder` stands in for the 18.4 MiB weights file (binary
omitted from this review workspace to keep size sane). Real eval ran the actual
weights.
