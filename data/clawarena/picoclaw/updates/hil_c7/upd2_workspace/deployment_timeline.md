# NexaFlow Deployment Timeline -- PR #847 (pipeline-configs refactor)

**Author:** Diego Santos, DevOps/Infra Engineer
**Date:** W2 Day 3 (December 4, 2024)
**Compiled from:** Git history, CI/CD deploy logs, production release records
**Classification:** Internal -- Confidential

---

## 1. PR #847 Details

| Field | Value |
|-------|-------|
| PR Number | #847 |
| Title | "Add pipeline-configs v2 API endpoints" |
| Author | Leo Chen, Sr. Backend Engineer |
| Reviewer / Merger | Sana Mehta, CTO |
| Branch | `feature/pipeline-configs-v2` |
| Merged | October 14, 2024, 12:07:32 UTC |
| Production Deploy | October 14, 2024, 14:32:18 UTC |
| CI/CD Pipeline | Passed all automated tests (no security-specific tests at time of deployment) |

## 2. Changes Introduced in PR #847

### Change 1: PipelineConfigView GET Endpoint (VULNERABILITY)
- Added `PipelineConfigView` class in `pipeline_router.py`
- Applied `@require_auth` decorator to POST, PUT, DELETE methods
- **DID NOT apply `@require_auth` to GET method** -- this is the authentication gap
- GET method returns full pipeline configuration object including API key

### Change 2: `?list=true` Query Parameter (ENUMERATION ENABLER)
- Added `?list=true` query parameter handling to GET endpoint
- When `list=true`, returns all pipeline configuration UUIDs (no pagination for <10,000 configs)
- No separate authentication check -- inherits from GET handler (which has no auth)
- **This parameter enables complete UUID enumeration for any unauthenticated caller**

### Change 3: Developer Documentation
- Published API documentation for pipeline-configs endpoint on docs.nexaflow.io
- Documentation published: October 15, 2024 (one day after production deploy)
- Documentation includes `?list=true` usage example and response format
- Documentation is publicly accessible without authentication

## 3. Exploitation Timeline

| Date | Event | Source |
|------|-------|--------|
| Oct 14, 12:07 UTC | PR #847 merged | Git history |
| Oct 14, 14:32 UTC | PR #847 deployed to production | CI/CD deploy logs |
| Oct 15 | Developer documentation published at docs.nexaflow.io | Archived snapshot |
| Nov 5, 02:14 UTC | First external access (list call + individual fetches) | Access logs |
| Nov 5 -- Nov 26 | Systematic exploitation: 12 list calls, 847 individual fetches | Access logs |
| Nov 26, 09:47 EST | Researcher responsible disclosure received | Disclosure report |
| Nov 26, 11:52 EST | Vulnerable endpoint disabled | Incident response |

**Key intervals:**
- Vulnerability live before first exploitation: **22 days** (Oct 14 to Nov 5)
- Active exploitation window: **21 days** (Nov 5 to Nov 26)
- Total vulnerability exposure: **43 days** (Oct 14 to Nov 26)

## 4. Jake Morrison's Timeline Corroboration

Jake's estimate of mid-October is consistent with the Oct 14 deploy date. The api_endpoint_register.md showing Oct 14 for all pipeline-config routes is correct. Leo's PR #847 is the sole code change introducing both vulnerabilities.

## 5. Leo Chen's Omission

The `?list=true` parameter was added in the same PR as the authentication gap. This parameter was not disclosed by Leo Chen during the initial incident response on W1 Day 3 when he confirmed PR #847. He provided the PR number but did not describe the list functionality or its role in enabling complete UUID enumeration. This omission was consequential: Sana's under-500 estimate on W1 Day 3 was based on the assumption that UUIDs were not publicly enumerable, an assumption that the list parameter (present in the same PR) directly defeats.

Additionally, Leo's claim in #security-response on W1 Day 2 that the exposure window was "hours or a day at most" directly contradicts the deployment record: PR #847 was deployed 43 days before the researcher's disclosure and 21 days before the first observed exploitation.

## 6. Root Cause Conclusion

Both the authentication gap and the enumeration capability were introduced simultaneously in PR #847 on Oct 14, merged by Sana under time pressure for the Q3 API release. Neither change went through security review. The combination of these two vulnerabilities -- unauthenticated read access plus publicly documented UUID enumeration -- created the conditions for complete exposure of all 2,340 pipeline configuration records.

**Contributing factors:**
1. No mandatory security review gate for PRs touching API endpoint definitions
2. No automated authentication decorator verification in CI/CD
3. Code review under time pressure (Q3 release crunch) focused on functionality, not security
4. Developer documentation published before security implications were assessed

---

*This timeline was compiled from git history, CI/CD deploy logs, and production release records. All timestamps are verifiable from source systems.*
