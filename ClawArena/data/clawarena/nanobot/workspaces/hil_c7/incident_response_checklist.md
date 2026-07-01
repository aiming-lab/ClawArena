# NexaFlow Security Incident Response Checklist (SOC 2 Aligned)

**Template Version:** 1.2
**Last Updated:** October 1, 2024
**Author:** Jake Morrison, Security Consultant (drafted for SOC 2 preparation)
**Classification:** Internal

---

## 1. Scope Assessment

- [ ] Cross-reference access logs, endpoint documentation, and data inventory before estimating exposure scope.
- [ ] Identify all affected endpoints and the specific data types accessible through each.
- [ ] Determine the exposure window: when was the vulnerability introduced and when was it remediated?
- [ ] Enumerate all external IP addresses that accessed the vulnerable endpoint.
- [ ] Distinguish between legitimate customer traffic and anomalous external access.
- [ ] Validate scope estimates against the total data inventory (upper bound check).
- [ ] Document the estimation methodology and confidence level for the scope figure.

**Important:** Do not commit to a scope estimate in any external communication until the access log analysis is complete. Preliminary estimates based on single-source analysis (e.g., request count extrapolation) are insufficient for regulatory reporting.

## 2. Notification Timeline

### GDPR Article 33 (if applicable)
- **Supervisory authority notification:** Within 72 hours of confirmed scope.
- **Trigger:** Personal data breach affecting EU data subjects.
- **Content required:** Nature of breach, categories of data, approximate number of data subjects, likely consequences, measures taken.

### US State Laws
- **CCPA (California):** Notification to affected California residents "in the most expedient time possible and without unreasonable delay."
- **NY SHIELD Act (New York):** Notification "in the most expedient time possible and without unreasonable delay" to New York residents.
- **General guidance:** Most state laws require notification within 30-60 days of confirmed breach.

### Contractual Obligations
- [ ] Review all enterprise customer contracts for data breach notification clauses.
- [ ] Identify customers with specific SLA windows (e.g., 24-hour, 48-hour notification requirements).
- [ ] Prioritize notification to contractually-obligated customers.

## 3. Containment

- [ ] Disable or patch the vulnerable endpoint immediately.
- [ ] Rotate all affected credentials (API keys, tokens, passwords).
- [ ] Preserve all access logs for forensic analysis -- do not rotate or archive logs until investigation is complete.
- [ ] Verify no other endpoints share the same vulnerability pattern.
- [ ] Implement temporary rate limiting or IP blocking if exploitation is ongoing.

## 4. Root Cause Documentation

- [ ] Identify the specific code change that introduced the vulnerability.
- [ ] Document the PR number, commit hash, author, and approver.
- [ ] Determine whether the code change went through security review.
- [ ] Identify any process failures that allowed the vulnerability to be deployed (e.g., missing automated security checks in CI/CD).
- [ ] Document the deployment date and the date the vulnerability became exploitable.

## 5. Remediation

- [ ] Patch the vulnerability (add authentication, fix authorization logic).
- [ ] Conduct a full audit of all API endpoints for similar vulnerabilities.
- [ ] Implement automated authentication decorator verification in CI/CD pipeline.
- [ ] Establish a mandatory security review gate for PRs touching API endpoint definitions.
- [ ] Update the incident response runbook with lessons learned.

## 6. Communication Plan

- [ ] Prepare internal briefing for executive team.
- [ ] Draft customer notification email -- review with legal counsel before sending.
- [ ] Prepare regulatory filing if required by GDPR Article 33 or state laws.
- [ ] Coordinate with customer success team for enterprise customer outreach.
- [ ] Document the full incident timeline for the post-incident review.

---

*This checklist is aligned with SOC 2 Trust Services Criteria (CC7.3: Incident Management) and should be completed for all security incidents classified as High or Critical severity.*
