# NovaBridge Security Incident Postmortem — DRAFT v1

**Status**: DRAFT — Pending final review
**Classification**: CONFIDENTIAL

---

## Executive Summary

On January 10, 2026, NovaBridge detected a GitHub Secret Scanning alert for an OpenAI API key
committed to the `novabridge/backend` repository. Investigation revealed the key had been active
and externally accessed within minutes of the commit.

This postmortem references the CircleCI January 2023 incident as a comparable case study.

---

## CircleCI Incident Reference (2023)

According to the CircleCI January 2023 incident report:

- **Data exfiltration date**: 2022-12-22
- **Customer anomaly detection date**: 2022-12-25 *(NOTE: This date is under review — see Update 2)*
- **GitHub OAuth token rotation completed**: 2023-01-07T07:30:00Z
- **Malware artifact**: PTX-Player.dmg
  SHA256: 8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf
- **Attack vector**: Session cookie theft via malware on an engineer's laptop

*The customer detection date of 2022-12-25 was cited in early drafts. The CircleCI official
post-mortem should be consulted for the authoritative date — this draft is pending correction.*

---

## NovaBridge Incident Timeline

| Time (UTC) | Event |
|---|---|
| 2026-01-10 07:58:00 | Huang Min commits code containing OpenAI API key |
| 2026-01-10 08:00:00 | GitHub Push Protection triggers alert (openai_api_key, validity=active) |
| 2026-01-10 08:03:00 | GitGuardian webhook fires, key confirmed active |
| 2026-01-10 08:05:00 | First external scan detected in CloudTrail (GetCallerIdentity from 185.234.219.44) |
| 2026-01-10 08:15:00 | Li Wei begins incident response |
| 2026-01-10 08:20:00 | AWS GuardDuty findings generated |

---

## Initial Scope Assessment

- **Affected keys (v1)**: 2 (OpenAI API key, AWS IAM key)
- **Affected services (v1)**: OpenAI API, AWS S3

*NOTE: Scope was later expanded in Update 1. See impact_analysis_v2.md.*

---

## Remediation Steps (Partial)

1. Revoke OpenAI API key (PENDING)
2. Disable AWS IAM user key (AKIA prefix — long-term credential)
3. Apply AWS Config rule ACCESS_KEYS_ROTATED to enforce rotation policy
4. Patch codebase — move secrets to environment variables / secrets manager

---

## References

- CircleCI Incident Report: https://circleci.com/blog/jan-4-2023-incident-report/
- AWS GuardDuty: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html
- GitGuardian Remediation: https://www.gitguardian.com/remediation/openai-api-key
