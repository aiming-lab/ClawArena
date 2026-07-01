#!/usr/bin/env bash
# run_pcap_query.sh — tshark wrapper for capture.pcap
# Usage: bash tools/run_pcap_query.sh [query_type]
#
# query_type options:
#   dns        — show all DNS queries
#   tcp        — show all TCP SYN connections (src/dst IP + port)
#   full       — all packets summary
#   (default)  — dns + tcp combined

PCAP="network_traces/capture.pcap"

if [ ! -f "$PCAP" ]; then
    echo "ERROR: $PCAP not found" >&2
    exit 1
fi

if ! command -v tshark &>/dev/null; then
    echo "ERROR: tshark not found in PATH. Install with: apt-get install tshark" >&2
    exit 1
fi

QUERY="${1:-all}"

case "$QUERY" in
    dns)
        echo "=== DNS Queries ==="
        tshark -r "$PCAP" -Y "dns.qry.name" -T fields \
            -e frame.time -e ip.src -e ip.dst -e dns.qry.name -e dns.a \
            2>/dev/null
        ;;
    tcp)
        echo "=== TCP SYN Packets ==="
        tshark -r "$PCAP" -Y "tcp.flags.syn==1 and tcp.flags.ack==0" \
            -T fields -e frame.time -e ip.src -e ip.dst -e tcp.dstport \
            2>/dev/null
        ;;
    full)
        echo "=== Packet Summary ==="
        tshark -r "$PCAP" 2>/dev/null
        ;;
    *)
        echo "=== DNS Queries ==="
        tshark -r "$PCAP" -Y "dns.qry.name" -T fields \
            -e frame.time -e ip.src -e ip.dst -e dns.qry.name -e dns.a \
            2>/dev/null
        echo ""
        echo "=== TCP SYN Connections ==="
        tshark -r "$PCAP" -Y "tcp.flags.syn==1 and tcp.flags.ack==0" \
            -T fields -e frame.time -e ip.src -e ip.dst -e tcp.dstport \
            2>/dev/null
        ;;
esac
