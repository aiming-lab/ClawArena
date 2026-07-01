# Security Context: CVE-2024-47081 Triage & Remediation

## Summary

This document provides the security engineering context for CVE-2024-47081,
a credential-leakage vulnerability in the psf/requests library affecting all
versions prior to 2.32.4.

## Vulnerability Details

| Field | Value |
|-------|-------|
| CVE ID | CVE-2024-47081 |
| GHSA ID | GHSA-9hjg-9r4m-mvj7 |
| CVSS Score | 5.3 (MEDIUM) |
| CVSS Vector | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N |
| CWE | CWE-522 (Insufficiently Protected Credentials) |
| Affected | requests < 2.32.4 |
| Fixed | requests == 2.32.4 (released 2025-06-10) |
| Workaround | Set ``trust_env=False`` on Session objects |

## Root Cause

The vulnerability resided in the `get_netrc_auth` function in
`src/requests/utils.py`. The vulnerable code used:

```python
host = ri.netloc.split(':')[0]
```

to extract the hostname for netrc credential lookup. Python's `urlparse`
sets `netloc` to the network location component of the URL, which includes
userinfo, host, and port. For a URL like `http://example.com:@evil.com/`, `netloc` is
`example.com:@evil.com`, so `netloc.split(':')[0]` yields `example.com`.
However, the actual HTTP request targets `evil.com`.

The fix replaces this with `ri.hostname`, which correctly uses Python's
URL parser to return only the hostname portion, stripping userinfo and port.

## Authoritative Sources

- **NVD Detail**: https://nvd.nist.gov/vuln/detail/CVE-2024-47081
- **GitHub Issue**: https://github.com/psf/requests/issues/6964
- **Official Fix PR**: https://github.com/psf/requests/pull/6965
  - Commit: `57acb7c26d809cf864ec439b8bcd6364702022d5` (sethmlarson)
- **Alternative PR (superseded)**: https://github.com/psf/requests/pull/6963
  - Commit: `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b` (awoimbee)
  - NOTE: PR#6963 was superseded by PR#6965. Do not reference PR#6963 as the
    authoritative fix.

## Related Vulnerability

CVE-2023-32681 (GHSA-j8r2-6x86-q33q): Fixed in requests 2.31.0.
Proxy-Authorization header was inadvertently forwarded to destination servers
when following HTTPS proxy redirects.

## Internal Impact

Our company's Python services use requests==2.32.3. Services that:
- Use `.netrc` for credential storage AND
- Allow user-controlled or externally-sourced URLs
...are potentially vulnerable to credential exfiltration.

See `analysis/affected_services.json` for the internal service inventory.

## Remediation Plan

1. Apply patch to internal fork (company/requests-patched)
2. Write and pass regression tests
3. Update all internal services to requests >= 2.32.4
4. Short-term workaround: set `trust_env=False` on all Session objects
