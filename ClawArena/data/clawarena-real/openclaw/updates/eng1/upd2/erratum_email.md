# Erratum Email — Update-2 (2026-03-10)

From: alice@company.example
To: engineering@company.example
Subject: CORRECTION: CVE-2024-47081 Fix Commit SHA & Version Clarification

Team,

I need to correct two errors from my previous email (2026-03-06):

## Correction 1: Fix Commit SHA

My previous email incorrectly instructed you to record PR#6963's commit SHA
(`5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`) as the authoritative fix.

**This was wrong. Please update `analysis/fix_commit.json` immediately.**

The correct authoritative fix is **PR#6965** (by sethmlarson):
- Commit SHA: `57acb7c26d809cf864ec439b8bcd6364702022d5`
- GHSA: `GHSA-9hjg-9r4m-mvj7`
- PR: https://github.com/psf/requests/pull/6965

PR#6963 (awoimbee) was an earlier alternative that was **superseded** by PR#6965.
The updated `fix_commit.json` must reflect this supersede with:
- `commit_sha`: `57acb7c26d809cf864ec439b8bcd6364702022d5`
- `supersedes_pr`: `"6963"`
- `authoritative_pr`: `"6965"`

## Correction 2: requests 2.32.3 Partial Fix Claim

My previous email also incorrectly stated that requests 2.32.3 contains a
partial mitigation for CVE-2024-47081. **This is false.**

requests 2.32.3 does NOT contain any fix for CVE-2024-47081.
The fix was introduced only in 2.32.4 (released 2025-06-10).
The 2.32.3 change was an unrelated SSLContext fix.

Please disregard the earlier "partial mitigation" claim entirely.

Apologies for the confusion.

Alice
