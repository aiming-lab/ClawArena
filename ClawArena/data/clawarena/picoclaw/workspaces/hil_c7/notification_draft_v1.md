# Customer Notification Draft v1.0 -- Security Update

**Date:** W1 Day 3 (November 28, 2024)
**Author:** Alex Rivera, Product Manager
**Status:** DRAFT -- Pending Jordan Park (CEO) review
**Strategy:** Minimal disclosure (Phase 1)

---

## Draft Email

**Subject:** NexaFlow Security Update -- API Key Rotation

Dear [Customer Name],

We recently identified and resolved a security configuration issue in our API infrastructure. As a precautionary measure, we have rotated your API key for the following pipeline(s):

- [Pipeline Name 1]
- [Pipeline Name 2]

Your new API key is: `[NEW_API_KEY]`

**What happened:** During a routine security review, we identified a configuration issue that has been resolved. Your data security is our top priority.

**What we did:** We immediately addressed the configuration issue and proactively rotated API keys for affected accounts as a precautionary measure.

**What you need to do:** Update your pipeline configuration to use the new API key provided above. Your previous key has been invalidated.

**No action is required beyond updating your API key.** If you have questions or concerns, please contact our support team at support@nexaflow.io.

Thank you for your continued trust in NexaFlow.

Best regards,
The NexaFlow Security Team

---

## Internal Notes (do not include in customer email)

- This draft follows Jordan's Phase 1 "minimal disclosure" strategy
- Framed as a "security configuration issue" -- no mention of data exposure
- No timeline disclosed (Nov 5 -- Nov 26 exposure window omitted)
- No scope disclosed (number of affected records omitted)
- No mention of external researcher disclosure
- No mention of the vulnerability being publicly accessible for weeks
- Key rotation presented as "precautionary" rather than "remedial"
- **Open question:** Does this level of disclosure satisfy GDPR Article 33 and state notification laws? Legal review pending.

---

*This draft will be updated based on final scope confirmation and Jordan's disclosure strategy decision.*
