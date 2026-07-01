# Fix Comparison: PR#6963 vs PR#6965

## Background

Two pull requests were submitted to fix CVE-2024-47081:

- **PR#6963** (awoimbee, commit `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`)
- **PR#6965** (sethmlarson, commit `57acb7c26d809cf864ec439b8bcd6364702022d5`) ← **OFFICIAL FIX**

## PR#6963 (Superseded)

- Author: awoimbee
- Commit: `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`
- Approach: More complex URL parsing with additional userinfo stripping
- Status: **SUPERSEDED** by PR#6965
- Review notes: sigmavirus24 noted this approach was more complex than necessary

## PR#6965 (Official)

- Author: sethmlarson
- Commit: `57acb7c26d809cf864ec439b8bcd6364702022d5`
- Approach: Simple replacement of `ri.netloc.split(':')[0]` with `ri.hostname`
- GHSA: `GHSA-9hjg-9r4m-mvj7`
- Status: **MERGED — OFFICIAL FIX**
- Review notes: Cleaner approach using Python's built-in hostname parsing

## Recommendation

Always reference PR#6965 and commit `57acb7c26d809cf864ec439b8bcd6364702022d5` as the authoritative fix.
PR#6963 and commit `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b` are obsolete and should not be cited in
security documentation.

## Technical Difference

```diff
# Before (vulnerable):
- host = ri.netloc.split(':')[0]

# After (PR#6965 fix):
+ host = ri.hostname
+ if host is None:
+     return None
```

The `ri.hostname` attribute correctly handles all URL forms including those with
userinfo components (`user@host` syntax), returning only the hostname without
port or userinfo.
