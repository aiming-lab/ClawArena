#!/usr/bin/env bash
# Baseline: openclaw agent connects directly to the LLM, no mm-metaclaw overlay.
# Use this as the control group for comparing mm-metaclaw module effects.
#
# Usage:
#   source scripts/metaclaw-bench/env.sh   # or set vars manually
#   bash scripts/metaclaw-bench/run_baseline.sh

source "$(dirname "$0")/_common.sh"

_run_clawarena "baseline" \
    --model-id "$BENCHMARK_MODEL" \
    --api-base "$BENCHMARK_BASE_URL" \
    --api-key  "$BENCHMARK_API_KEY"
