# Network Telemetry Directory

| File | Description |
|------|-------------|
| `router_syslog.log` | Full router syslog including DHCP/ARP/NAT events |
| `dhcp_leases.json` | Current and historical DHCP lease table |
| `firmware_versions.json` | Firmware version manifest for all devices |
| `mdns_discovery.log` | mDNS/Bonjour device discovery log |

The unknown device `a4:cf:12:8e:7b:3d` appears in both `router_syslog.log`
and `dhcp_leases.json` around 02:14. Its firmware and vendor classification
will be clarified by the vendor notice when it arrives.
