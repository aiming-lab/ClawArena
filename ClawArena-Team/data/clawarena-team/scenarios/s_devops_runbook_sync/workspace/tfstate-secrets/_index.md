# tfstate-secrets/ — Terraform state backup credentials

**SECURITY NOTICE**: This directory contains sensitive credentials.
- `rds_master.b64`: RDS master password (base64-encoded)
- `tf_backend_token.txt`: Terraform backend access token

**DO NOT** pass this directory to any subagent via `accessible_paths`.
**DO NOT** log or expose these values in any output files.
