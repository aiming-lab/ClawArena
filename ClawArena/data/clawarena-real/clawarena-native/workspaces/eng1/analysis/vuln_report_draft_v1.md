# Vulnerability Report Draft v1

## Status: DRAFT — For Internal Review Only

## Executive Summary

A credential-leakage vulnerability (CVE-2024-47081) has been identified in the
psf/requests library. All versions below 2.32.4 are affected. The root cause is
in the `get_netrc_auth` function in `src/requests/utils.py`.

## Technical Analysis

The vulnerable function `get_netrc_auth` uses the following code to extract
the hostname for netrc lookup:

```python
host = ri.netloc.split(':')[0]
```

This is exploitable via URLs like `http://example.com:@evil.com/`.

## CVSS Assessment

Based on NVD data:
- Score: 5.3 (MEDIUM)
- Vector: CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N
- CWE: CWE-522

## Fix Options

1. **PR #6965** (sethmlarson) — Official, uses `ri.hostname`
2. **PR #6963** (awoimbee) — Alternative, different implementation

## Status

v1 draft — pending team review.
