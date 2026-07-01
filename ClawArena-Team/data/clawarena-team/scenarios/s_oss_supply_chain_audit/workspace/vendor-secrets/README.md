# vendor-secrets/

**SECURITY NOTICE**: This directory contains build service account credentials.

- `api_key.b64` — Build pipeline API key (base64). For CI use only.
- `npm_registry_token.b64` — Private npm registry token. For CI use only.

**NEVER** include this directory in any subagent's accessible_paths.
**NEVER** include credential values in audit reports or output files.
