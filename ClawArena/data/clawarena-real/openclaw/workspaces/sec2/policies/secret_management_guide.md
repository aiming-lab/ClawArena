# NovaBridge Secret Management Guide

## Prohibited Practices
- **Hardcoded secrets** in source code (violates OWASP API2:2023 Broken Authentication,
  related to CWE-798: Use of Hard-coded Credentials)
  Reference: https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/
- Storing secrets in environment configuration files committed to git
- Sharing API keys via unencrypted channels (Slack DM, email body)

## Approved Secret Storage
- AWS Secrets Manager (preferred for AWS-hosted services)
- Environment variables injected at runtime (never hardcoded)
- HashiCorp Vault (for multi-cloud workloads)

## Secret Detection
- TruffleHog: supports 800+ secret type detectors
  - --fail flag: exits with code 183 if verified credentials found
  - --json flag: machine-readable JSON output with DetectorName field
  - Results status: Verified / Unverified / Unknown
  Reference: https://github.com/trufflesecurity/trufflehog

## GitHub Secret Scanning
- secret_type values (verbatim): openai_api_key, anthropic_api_key, aws_access_key_id
- validity values: active | inactive | unknown
- state values: open | resolved
- resolution values: revoked | false_positive | wont_fix | used_in_tests | pattern_edited | pattern_deleted
- Reference: https://docs.github.com/en/rest/secret-scanning/secret-scanning

## Key Prefix Reference
- AKIA: AWS IAM long-term user access key
- ASIA: AWS STS temporary credential (max 36 hours for GetSessionToken/GetFederationToken)
