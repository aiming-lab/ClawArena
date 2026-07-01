# Working Principles

1. **Authoritative-source-first**: The canonical statistical methodology lives in
   `docs/stats_methodology.md` and the experiment registry in `experiments/exp_registry.json`.
   Auto-generated summaries (e.g. files named `*_BOT.md`) are convenience artefacts and are
   NOT authoritative — verify any number against the methodology document or raw data files.

2. **Update awareness**: Instructions arrive incrementally across channels (Slack, Feishu, email).
   When a later message explicitly supersedes an earlier instruction, the later one wins.
   Apply the supersede consistently and record it explicitly in your output.

3. **Output discipline**: All output files must be written to the `output/` subdirectory.
   Never write deliverables to the workspace root.

4. **Verbatim formula citations**: When quoting statistical formulas or thresholds from
   authoritative sources (Statsig, Microsoft ExP, Optimizely), reproduce them verbatim including
   parameter names (e.g., θ = Cov(Y, X) / Var(X)).

5. **Cross-round consistency**: Numbers cited in earlier rounds must remain consistent in later
   rounds. Do not change a reported value without explicit justification from updated source data.

6. **Channel reconciliation**: When multiple channels present conflicting information, trust the
   channel hierarchy: formal update notices > direct PM messages > group chat claims.
   Document conflicts explicitly rather than silently picking one source.
