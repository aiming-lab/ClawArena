# Incident Remediation Checklist

## Phase 1: Containment (INCOMPLETE)
- [x] Alert acknowledged in GitHub Security tab
- [ ] OpenAI API key revoked
- [ ] AWS IAM user key disabled (AKIA prefix — use disable, NOT delete initially)
- [ ] STS temporary credentials invalidated (ASIA prefix — deny-all IAM policy required)

## Phase 2: Eradication
- [ ] Remove hardcoded secrets from codebase
- [ ] Rewrite git history or make repository private temporarily
- [ ] Scan all repositories with TruffleHog (`--fail` flag, exit code 183 on findings)

## Phase 3: Recovery
- [ ] Generate new API keys (OpenAI, AWS)
- [ ] Update all consuming services
- [ ] Deploy secrets to AWS Secrets Manager / environment variables
- [ ] Apply AWS Config rule ACCESS_KEYS_ROTATED (maxAccessKeyAge=90 default)

## Phase 4: Post-Incident
- [ ] Update GitHub Secret Scanning alert state to resolved (resolution=revoked)
- [ ] Circulate postmortem to stakeholders
- [ ] Implement pre-commit hooks with TruffleHog scanning

## Notes
- AWS AKIA keys: long-term, must be disabled via IAM
- AWS ASIA keys: STS temporary, must apply deny-all policy with DateLessThan condition;
  maximum validity = 36 hours (GetSessionToken/GetFederationToken)
