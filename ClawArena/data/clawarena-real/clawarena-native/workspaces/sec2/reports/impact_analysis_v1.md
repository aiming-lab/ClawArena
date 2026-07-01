# Impact Analysis — v1 (Initial Assessment)

**Date**: 2026-01-10
**Prepared by**: Li Wei
**Status**: SUPERSEDED by impact_analysis_v2.md (Update 1)

## Affected Keys

| Key Type | Service | Status | Key Prefix |
|---|---|---|---|
| OpenAI API Key | OpenAI API | Active (unrevoked) | sk-proj- |
| AWS Access Key | AWS S3, IAM | Active (unrevoked) | AKIA |

**affected_keys_count: 2**

## Affected Services

- openai (text generation, summarization)
- aws (S3 data storage, IAM identity)

## Risk Assessment

- External IP 185.234.219.44 accessed GetCallerIdentity and ListBuckets
- No confirmed data exfiltration (pending CloudTrail audit)
- GitHub Secret Scanning: 75% push protection precision rate

## References
- GitGuardian State of Secrets Sprawl 2024: 1212x surge in OpenAI key leaks in 2023
- 2.6% of secrets revoked within 1 hour (industry benchmark)
- 39 million secrets leaked across GitHub in 2024
