#!/usr/bin/env bash
# ============================================================
#  ClawArena — environment variables example
#  Copy this file, fill in your values, then point
#  test_run.py's API_KEY_SCRIPT to it.
#
#  Usage:
#    cp scripts/env_example.sh scripts/env.sh   # make a copy
#    vim scripts/env.sh                          # fill in keys
#    # then in test_run.py, set:
#    #   API_KEY_SCRIPT = "scripts/env.sh"
# ============================================================

# ── LLM Provider (required) ──────────────────────────────────
# These are read by clawarena's provider system.
# See docs/provider-usage-guide.md for the full priority chain.
export CLAWARENA_PROVIDER=openai
export CLAWARENA_MODEL_ID=gpt-5.2
export CLAWARENA_API_BASE=https://api.openai.com/v1
export CLAWARENA_API_KEY=sk-your-api-key-here

# ── Framework-specific (optional) ────────────────────────────
# Uncomment if using the corresponding framework.

# # OpenClaw — uses the provider config above by default.
# #   Set OPENCLAW_API_KEY only if OpenClaw needs a different key.
# export OPENCLAW_API_KEY=sk-...

# # Claude Code — requires Anthropic credentials.
# export ANTHROPIC_API_KEY=sk-ant-...
# #   Or use OAuth: run `claude login` beforehand.

# # Nanobot — override provider for nanobot specifically.
# export NANOBOT_PROVIDERS__CUSTOM__API_KEY=${CLAWARENA_API_KEY}
# export NANOBOT_PROVIDERS__CUSTOM__API_BASE=${CLAWARENA_API_BASE}
# export NANOBOT_AGENTS__DEFAULTS__MODEL=${CLAWARENA_MODEL_ID}

# ── Advanced (optional) ──────────────────────────────────────
# # Claude Code compaction interval (0 = disable)
# export CLAWARENA_COMPACT_INTERVAL=25

echo "[env] CLAWARENA_PROVIDER=${CLAWARENA_PROVIDER}"
echo "[env] CLAWARENA_MODEL_ID=${CLAWARENA_MODEL_ID}"
echo "[env] CLAWARENA_API_BASE=${CLAWARENA_API_BASE}"
echo "[env] CLAWARENA_API_KEY=***"
echo "[env] Environment loaded."
