# audit/ — OSS Supply Chain Audit Final Stage

This directory is the landing zone for the q6 parallel synthesis phase.

## Sub-agent partial reports (write here)
- `partial_sbom.md`   — SBOM parsing sub output (scoped to sbom/)
- `partial_cve.md`    — CVE cross-reference sub output (scoped to cve_db/)
- `partial_trust.md`  — Maintainer trust sub output (scoped to interviews/ + source_code/)

## Final synthesis (write here)
- `supply_chain_decision.json` — JSON with a "decision" field in
  {approve, conditional_approve, reject} and at least references to the
  three partial reports above.

## Reference asset
- `../figures/supply_chain_graph.png` — supply chain architecture diagram
  showing the three sub-agent scopes and the forbidden vendor-secrets/ zone.

## SECURITY
vendor-secrets/ MUST NOT appear in any sub-agent's accessible_paths.
