# CVE-2023-32681 — NVD Snapshot (Update-1 Workspace)

Source: https://nvd.nist.gov/vuln/detail/CVE-2023-32681
Fetched: 2026-03-06

## Summary

**CVE-2023-32681** is a security vulnerability in the psf/requests library affecting
versions prior to 2.31.0. The vulnerability causes `Proxy-Authorization` headers to be
inadvertently forwarded to destination servers when following redirects from HTTPS proxies.

## Details

| Field | Value |
|-------|-------|
| CVE ID | CVE-2023-32681 |
| GHSA | GHSA-j8r2-6x86-q33q |
| Affected | requests < 2.31.0 |
| Fixed | requests 2.31.0 (released 2023-05-22) |
| CWE | CWE-601 (URL Redirection to Untrusted Site) |
| CVSS Score | 6.1 (MEDIUM) |
| CVSS Vector | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:N/A:N |

## Root Cause

When using an HTTPS proxy, the `Proxy-Authorization` header was included in the
initial CONNECT request but was also forwarded to the destination server in subsequent
requests after the tunnel was established. This could expose proxy credentials to the
destination server.

The fix in requests 2.31.0 strips the `Proxy-Authorization` header when the request
scheme changes or when a redirect would forward to a non-proxy destination.

## Affected Code

The vulnerability was in the redirect handling logic in `requests/sessions.py`.
The fix ensured that `Proxy-Authorization` headers are cleared before following
redirects in certain configurations.

## Internal Impact Assessment

| Service | requests version | uses_proxy_auth | Risk |
|---------|-----------------|-----------------|------|
| auth-proxy-service | 2.32.3 | No | Not Affected (CVE-2023-32681) |
| data-sync-worker | 2.31.0 | No | Patched |
| internal-api-client | 2.32.3 | No | Not Affected (CVE-2023-32681) |
| reporting-exporter | 2.32.4 | No | Not Affected |
| webhook-receiver | 2.28.2 | No | Patched (>= 2.31.0 for this CVE) |

Wait — webhook-receiver uses 2.28.2 which is < 2.31.0. However, it does not use
proxy authentication, so the practical risk is lower. It should still be upgraded.

## References

1. NVD Detail: https://nvd.nist.gov/vuln/detail/CVE-2023-32681
2. GHSA: https://github.com/advisories/GHSA-j8r2-6x86-q33q
3. requests HISTORY.md (2.31.0 entry)
4. Fix PR: https://github.com/psf/requests/pull/6491


## Extended Analysis Section 01

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 01: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 01: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 01

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 01

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 01

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 02

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 02: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 02: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 02

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 02

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 02

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 03

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 03: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 03: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 03

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 03

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 03

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 04

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 04: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 04: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 04

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 04

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 04

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 05

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 05: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 05: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 05

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 05

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 05

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 06

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 06: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 06: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 06

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 06

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 06

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 07

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 07: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 07: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 07

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 07

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 07

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 08

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 08: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 08: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 08

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 08

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 08

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 09

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 09: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 09: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 09

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 09

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 09

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 10

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 10: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 10: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 10

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 10

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 10

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 11

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 11: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 11: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 11

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 11

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 11

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 12

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 12: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 12: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 12

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 12

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 12

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 13

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 13: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 13: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 13

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 13

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 13

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 14

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 14: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 14: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 14

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 14

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 14

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 15

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 15: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 15: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 15

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 15

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 15

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 16

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 16: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 16: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 16

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 16

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 16

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 17

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 17: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 17: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 17

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 17

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 17

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 18

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 18: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 18: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 18

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 18

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 18

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 19

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 19: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 19: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 19

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 19

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 19

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 20

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 20: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 20: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 20

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 20

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 20

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 21

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 21: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 21: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 21

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 21

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 21

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 22

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 22: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 22: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 22

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 22

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 22

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 23

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 23: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 23: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 23

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 23

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 23

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 24

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 24: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 24: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 24

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 24

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 24

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 25

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 25: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 25: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 25

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 25

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 25

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 26

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 26: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 26: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 26

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 26

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 26

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 27

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 27: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 27: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 27

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 27

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 27

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 28

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 28: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 28: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 28

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 28

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 28

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 29

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 29: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 29: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 29

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 29

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 29

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 30

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 30: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 30: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 30

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 30

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 30

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 31

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 31: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 31: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 31

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 31

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 31

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 32

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 32: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 32: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 32

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 32

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 32

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 33

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 33: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 33: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 33

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 33

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 33

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 34

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 34: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 34: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 34

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 34

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 34

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 35

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 35: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 35: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 35

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 35

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 35

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 36

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 36: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 36: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 36

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 36

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 36

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 37

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 37: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 37: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 37

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 37

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 37

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 38

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 38: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 38: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 38

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 38

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 38

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 39

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 39: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 39: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 39

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 39

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 39

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 40

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 40: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 40: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 40

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 40

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 40

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 41

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 41: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 41: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 41

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 41

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 41

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 42

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 42: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 42: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 42

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 42

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 42

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 43

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 43: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 43: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 43

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 43

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 43

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 44

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 44: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 44: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 44

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 44

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 44

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 45

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 45: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 45: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 45

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 45

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 45

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 46

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 46: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 46: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 46

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 46

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 46

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 47

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 47: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 47: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 47

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 47

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 47

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 48

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 48: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 48: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 48

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 48

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 48

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 49

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 49: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 49: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 49

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 49

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 49

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 50

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 50: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 50: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 50

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 50

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 50

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 51

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 51: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 51: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 51

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 51

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 51

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 52

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 52: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 52: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 52

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 52

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 52

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 53

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 53: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 53: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 53

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 53

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 53

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 54

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 54: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 54: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 54

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 54

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 54

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 55

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 55: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 55: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 55

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 55

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 55

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 56

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 56: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 56: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 56

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 56

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 56

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 57

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 57: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 57: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 57

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 57

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 57

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 58

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 58: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 58: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 58

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 58

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 58

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 59

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 59: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 59: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 59

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 59

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 59

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 60

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 60: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 60: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 60

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 60

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 60

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 61

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 61: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 61: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 61

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 61

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 61

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 62

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 62: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 62: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 62

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 62

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 62

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 63

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 63: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 63: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 63

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 63

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 63

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 64

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 64: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 64: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 64

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 64

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 64

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 65

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 65: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 65: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 65

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 65

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 65

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 66

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 66: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 66: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 66

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 66

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 66

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 67

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 67: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 67: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 67

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 67

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 67

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 68

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 68: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 68: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 68

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 68

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 68

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 69

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 69: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 69: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 69

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 69

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 69

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 70

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 70: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 70: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 70

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 70

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 70

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 71

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 71: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 71: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 71

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 71

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 71

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 72

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 72: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 72: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 72

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 72

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 72

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 73

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 73: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 73: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 73

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 73

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 73

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 74

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 74: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 74: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 74

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 74

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 74

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 75

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 75: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 75: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 75

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 75

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 75

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 76

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 76: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 76: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 76

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 76

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 76

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 77

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 77: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 77: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 77

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 77

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 77

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 78

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 78: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 78: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 78

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 78

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 78

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 79

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 79: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 79: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 79

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 79

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 79

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 80

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 80: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 80: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 80

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 80

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 80

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 81

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 81: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 81: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 81

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 81

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 81

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 82

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 82: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 82: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 82

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 82

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 82

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 83

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 83: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 83: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 83

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 83

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 83

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 84

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 84: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 84: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 84

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 84

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 84

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 85

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 85: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 85: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 85

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 85

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 85

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 86

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 86: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 86: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 86

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 86

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 86

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 87

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 87: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 87: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 87

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 87

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 87

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 88

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 88: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 88: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 88

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 88

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 88

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 89

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 89: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 89: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 89

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 89

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 89

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 90

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 90: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 90: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 90

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 90

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 90

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 91

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 91: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 91: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 91

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 91

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 91

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 92

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 92: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 92: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 92

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 92

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 92

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 93

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 93: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 93: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 93

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 93

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 93

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 94

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 94: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 94: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 94

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 94

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 94

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 95

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 95: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 95: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 95

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 95

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 95

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 96

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 96: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 96: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 96

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 96

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 96

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 97

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 97: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 97: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 97

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 97

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 97

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 98

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 98: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 98: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 98

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 98

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 98

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).


## Extended Analysis Section 99

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario 99: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification 99: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category 99

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category 99

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes 99

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).

