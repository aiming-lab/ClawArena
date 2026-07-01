# network_traces/ — Network Evidence

| File | Content | Note |
|---|---|---|
| capture.pcap | Binary pcap — requires tshark | Use `bash tools/run_pcap_query.sh` |
| falco_rules.yaml | Falco detection rules for staging | Contains exfil IP + C2 domain |

## Parsing capture.pcap

The pcap file is binary and CANNOT be read directly.
Use: `bash tools/run_pcap_query.sh dns` — to see DNS queries
Use: `bash tools/run_pcap_query.sh tcp` — to see TCP SYN packets

Key evidence in capture.pcap:
- DNS query: c2.exfil-ops.ru → 45.61.135.99
- TCP SYN: 185.220.101.42 → 10.100.1.15:22 (initial access)
- TCP SYN: 10.100.1.15 → 45.61.135.99:443 (exfil attempt)
