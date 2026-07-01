"""ClawArena-native harness — vendored, self-contained agent harness.

This package is a deterministic, fully Python-implemented agent harness
ported from ArcBench (agent loop, tools, system prompt, compaction,
``<system-reminder>`` injection, sandbox) plus a WorkflowTool ported from
SMbench. Unlike the external CLI-subprocess engines (openclaw / claude-code /
nanobot / picoclaw), this harness has no external binary dependency, so the
benchmark stays fixed and reproducible across runs.

Only relative imports are used inside the sub-packages, so the vendored tree
is self-contained under ``clawarena.native``.
"""
