# ArcNode Comparison Reference: October 30, 2023 Incident

_Source: https://blog.cloudflare.com/cloudflare-incident-on-october-30-2023/_

## Summary

| Field | Value |
|-------|-------|
| Incident Start | 2023-10-30T19:54:00Z |
| Incident End | 2023-10-30T20:31:00Z |
| Duration | 37 minutes |
| Root Cause Component | Workers KV deployment tool |
| Services Affected | 11 services (Workers KV, Pages, Access, WARP, Images API, etc.) |
| Resolution | Break-glass mechanism bypassing normal tooling |
| Corrective Actions | 5 actions prioritised for the quarter |

## Root Cause

A deployment tool bug returned a staging build GUID mixed with production releases,
causing HTTP 401 errors from KV and HTTP 500 from Pages.

## Comparison with June 20, 2024 Incident

The June 20 incident differs significantly:
- Duration: 100 minutes (vs. 37 minutes for Oct 30)
- Root cause: Lua infinite-recursion bug + backbone congestion (two causal chains)
- Peak error rate: 2.1% CDN (vs. localised 401/500 errors in Oct 30)

DO NOT confuse the 37-minute Oct30 duration with the June 20 incident duration.
