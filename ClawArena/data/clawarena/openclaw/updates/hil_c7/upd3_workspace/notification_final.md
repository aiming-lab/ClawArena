# Customer Notification -- Security Incident (Final, Approved by Jordan Park)

**Date:** W2 Day 5 (December 6, 2024) -- Approved
**Sent:** W2 Day 6 (December 7, 2024)
**Author:** Alex Rivera (drafted), Jordan Park (approved)
**Recipients:** All 2,340 affected customers
**Strategy:** Full Transparency (Phase 2)

---

## Final Notification Email

**Subject:** Important Security Notice -- NexaFlow Pipeline Configuration Data

Dear [Customer Name],

We are writing to notify you of a security incident that affected NexaFlow customer accounts between November 5 and November 26, 2024.

**What happened:**
An API endpoint in our v2 pipeline configuration service was incorrectly configured without authentication, which allowed unauthorized access to your pipeline configuration data during this period. This issue was identified through a responsible disclosure by an external security researcher on November 26.

**What information was accessible:**
The following information associated with your NexaFlow account was accessible during this period:
- Account name
- Company name
- Pipeline name(s)
- API keys associated with your pipelines
- Pipeline configuration details

**What was NOT accessible:**
- Payment information
- Passwords
- Government-issued identification
- Personal addresses or phone numbers

**What we have done:**
1. **Disabled the vulnerable endpoint** within 2 hours of the researcher's report (November 26)
2. **Force-rotated all affected API keys** within 4 hours of discovery -- your new API key was automatically generated and is available in your NexaFlow dashboard
3. **Conducted a comprehensive forensic investigation** with an independent security consultant to determine the full scope and timeline
4. **Implemented a security review gate** for all future API endpoint changes
5. **Added automated authentication verification** to our CI/CD pipeline

**We have no evidence that this data was used maliciously.** Our forensic investigation found no indicators of the exposed API keys being used for unauthorized pipeline operations during the exposure window.

**What you should do:**
- Verify that your pipeline configurations are using the rotated API keys (check your NexaFlow dashboard)
- Monitor your pipeline execution logs for any unexpected activity
- Contact our security team at security@nexaflow.io if you have questions or concerns

We are deeply sorry for this incident. We take the security of your data seriously and recognize that we fell short of the standard you expect from us. We are committed to the process improvements described above to ensure this type of vulnerability cannot recur.

For questions or additional information, please contact:
- Security team: security@nexaflow.io
- Your account manager (enterprise customers will receive personal outreach)

Sincerely,
Jordan Park
CEO, NexaFlow

---

## Changes from Draft v1

| Element | Draft v1 (Phase 1) | Final (Phase 2) |
|---------|-------------------|------------------|
| Timeline | Not disclosed | Nov 5 -- Nov 26 (full disclosure) |
| Scope | Not disclosed | Explicit: pipeline config data + API keys |
| Framing | "Security configuration issue" | "Security incident" with full acknowledgment |
| Tone | "No action required" | "We are deeply sorry" + remediation steps |
| Root cause | Not mentioned | "Incorrectly configured without authentication" |
| Remediation | "Precautionary measure" | Full list of 5 remediation actions |
| Recipients | Under 500 (targeted) | All 2,340 affected customers |

## Jordan's Sign-off Note

Alex -- this is the right call. Legal confirmed we're covered for GDPR and state notification requirements with this approach. It's going to be a rough few weeks but we're not hiding anything.

---

*This notification was reviewed by NexaFlow's outside legal counsel and satisfies GDPR Article 33 supervisory authority notification requirements and US state data breach notification laws (CCPA, NY SHIELD Act).*
