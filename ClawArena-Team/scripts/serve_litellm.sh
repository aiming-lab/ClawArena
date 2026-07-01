#!/bin/bash
# Start the litellm proxy (Bedrock Claude -> OpenAI-compatible on :4000). Local use only,
# no master key.
#
# Auth: export AWS_BEARER_TOKEN_BEDROCK (and optionally AWS_REGION_NAME) before running,
# e.g. `export AWS_BEARER_TOKEN_BEDROCK=...`. If $CATEAM_BEDROCK_ENV points at a file that
# sets these, it is sourced automatically.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "${CATEAM_BEDROCK_ENV:-}" ] && [ -f "${CATEAM_BEDROCK_ENV}" ]; then
  # shellcheck disable=SC1090
  source "${CATEAM_BEDROCK_ENV}"
fi

export AWS_BEARER_TOKEN_BEDROCK
export AWS_REGION_NAME="${AWS_REGION_NAME:-us-east-1}"

exec litellm \
  --config "${SCRIPT_DIR}/litellm_bedrock.yaml" \
  --host 127.0.0.1 --port 4000
