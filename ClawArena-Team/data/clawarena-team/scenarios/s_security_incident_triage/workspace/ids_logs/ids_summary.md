# IDS Alert Summary — INC-2026-0514-A
# Generated: 2026-05-14T04:30:00Z
# Source: Suricata IDS — staging network perimeter

## Critical Findings

1. **Tor Exit Relay Detected**: Source IP 185.220.101.42 classified as known Tor exit
   relay (SID 2522010). Traffic targeted staging-web-01:22 at 03:47:05Z.

2. **C2 Beacon**: Internal host 10.100.1.15 initiated outbound connection
   to 45.61.135.99 (resolved domain: c2.exfil-ops.ru) at 03:52:20Z.
   Rule: SURICATA_ET_MALWARE_C2_Beacon (SID 2033132).

3. **Exfil Attempt Blocked**: Large data transfer attempt to 45.61.135.99:443
   at 04:01:22Z — blocked by egress ACL (SID 2522099).

## Recommendation

IDS evidence corroborates attacker IP 185.220.101.42 and confirms data exfiltration
attempt. Recommend CONTAIN decision: block 185.220.101.42 and secondary IPs at
network perimeter; eradicate attacker persistence before recovery.

## Alert Counts

Total alerts: 53
Critical: 3 (all attacker-related)
High/Medium/Low: 50 (noise)
