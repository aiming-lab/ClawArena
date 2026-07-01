# Vulnerability Report Draft v2

## Status: DRAFT v2 — Contains Error — Pending Supersede

## IMPORTANT CORRECTION NOTICE

This draft v2 contained an error: it incorrectly stated that requests 2.32.3
includes a partial fix for CVE-2024-47081. This is FALSE.
**requests 2.32.3 does NOT contain any fix for CVE-2024-47081.**
The fix was introduced only in requests 2.32.4.

Additionally, this draft incorrectly referenced PR#6963
(commit `5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`, author awoimbee) as the official fix.
The correct authoritative fix is PR#6965
(commit `57acb7c26d809cf864ec439b8bcd6364702022d5`, author sethmlarson).

This document is superseded by the authoritative record in `analysis/fix_commit.json`
(after UPDATE-2 is applied).

## Original v2 Content (DO NOT USE — ERRONEOUS)

~~CVE-2024-47081 is partially addressed in requests 2.32.3...~~
~~The fix commit SHA is 5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b...~~

These statements were erroneous and have been retracted via UPDATE-2.
