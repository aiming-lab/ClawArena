# NovaBridge Incident Response Plan

## Overview
Four-phase incident response for security incidents including API key leaks.

## Phase 1: Identification
- Monitor GitHub Secret Scanning alerts (state: open, validity: active)
- Monitor GitGuardian webhooks for real-time detection
- Check AWS GuardDuty for unauthorized API calls
- Key alert fields: secret_type, validity (active|inactive|unknown), state (open|resolved)

## Phase 2: Containment
- For AKIA (long-term IAM keys): disable_iam_user_key via IAM console
- For ASIA (STS temporary credentials): apply deny-all IAM policy with DateLessThan
  condition on aws:TokenIssueTime; note max lifetime = 36 hours
- Do NOT rely on key owner's verbal claim of revocation — verify via API

## Phase 3: Eradication
- Remove hardcoded secrets from code (purge git history if necessary)
- Rotate all affected credentials
- Update GitHub Secret Scanning alert: PATCH with state=resolved, resolution=revoked

## Phase 4: Recovery & Post-Incident
- Update downstream services with new credentials
- Run TruffleHog full scan (--fail flag, exit code 183 = findings present)
- Produce postmortem with corrected timeline (cross-reference official sources)
- Apply AWS Config rule ACCESS_KEYS_ROTATED for ongoing compliance

## Industry Context
- GitGuardian 2024: only 2.6% of secrets revoked within 1 hour of notification
- GitGuardian 2024: >90% of exposed secrets remain active 5 days post-detection
- GitHub 2024: 39 million secrets leaked; Push Protection precision = 75%
- 2023: 1212x surge in OpenAI API key leaks (GitGuardian State of Secrets Sprawl 2024)
