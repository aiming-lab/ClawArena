#!/usr/bin/env bash
# MetaClawBench environment variables — source this file before running experiments.
#
#   source scripts/metaclaw-bench/env.sh
#
# Required variables:
#   BENCHMARK_BASE_URL  — upstream LLM API base URL
#   BENCHMARK_API_KEY   — upstream LLM API key
#   BENCHMARK_MODEL     — model identifier (e.g. gpt-5.1)
#   GATEWAY_MODULES_DIR — absolute path to the gateway-modules project root
#
# Optional:
#   BENCHMARK_ROOT      — ClawArena project root (auto-detected if not set)

# ── Upstream LLM (edit to match your provider) ───────────────────────────────
export BENCHMARK_BASE_URL="${BENCHMARK_BASE_URL:-https://openai-api.shenmishajing.workers.dev/v1}"
export BENCHMARK_API_KEY="${BENCHMARK_API_KEY:-}"
export BENCHMARK_MODEL="${BENCHMARK_MODEL:-gpt-5.1}"

# ── mm-metaclaw gateway location ─────────────────────────────────────────────
# Set this to the absolute path of your local mm-metaclaw gateway-modules checkout.
export GATEWAY_MODULES_DIR="${GATEWAY_MODULES_DIR:-}"

# ── ClawArena root (auto-detect from script location) ────────────────────────
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export BENCHMARK_ROOT="${BENCHMARK_ROOT:-$(cd "$_SCRIPT_DIR/../.." && pwd)}"

echo "BENCHMARK_BASE_URL  : ${BENCHMARK_BASE_URL}"
echo "BENCHMARK_API_KEY   : ***"
echo "BENCHMARK_MODEL     : ${BENCHMARK_MODEL}"
echo "GATEWAY_MODULES_DIR : ${GATEWAY_MODULES_DIR}"
echo "BENCHMARK_ROOT      : ${BENCHMARK_ROOT}"
