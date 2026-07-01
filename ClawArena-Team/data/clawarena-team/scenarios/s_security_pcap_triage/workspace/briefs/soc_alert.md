# SOC Alert — Potential C2 Beacon Detected

**Incident ID** : SEC-2026-0419
**Detected**   : 2026-05-23 02:14:03 UTC
**Severity**   : HIGH
**Analyst**    : Maya Chen (paged on-call)

## Summary

SOC monitoring detected an outbound TCP connection from an internal host
to an unusual destination port. The source IP is **not** in our asset inventory
and the destination port (4444) is commonly associated with Metasploit / Netcat
reverse shells.

## Details

| Field | Value |
|-------|-------|
| Source IP | 10.42.7.183 |
| Destination IP | 10.0.0.50 |
| Destination Port | 4444 |
| Protocol | TCP |
| First seen | 2026-05-23 02:14:03 UTC |
| Connection count | 12 packets in 90 seconds |

## Evidence locations

- Raw capture : `pcap/2026-05-23_capture.pcap`
- Team discussion : `slack/soc_channel_screenshot.png`
- Forensics bundle : `forensics/evidence_bundle.zip` (password in Slack thread)

## Status

Triage in progress. IR escalation pending analyst decision.
