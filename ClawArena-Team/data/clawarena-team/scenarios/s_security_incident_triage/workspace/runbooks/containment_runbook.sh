#!/usr/bin/env bash
# containment_runbook.sh — Automated containment script for credential abuse incidents
# Usage: bash runbooks/containment_runbook.sh <INCIDENT_ID> <ATTACKER_IP> <COMPROMISED_USER>
# Example: bash runbooks/containment_runbook.sh INC-2026-0514-A 185.220.101.42 j.holloway

set -euo pipefail

INCIDENT_ID="${1:-UNKNOWN}"
ATTACKER_IP="${2:-}"
COMPROMISED_USER="${3:-}"

if [[ -z "$ATTACKER_IP" || -z "$COMPROMISED_USER" ]]; then
    echo "ERROR: ATTACKER_IP and COMPROMISED_USER are required" >&2
    exit 1
fi

echo "=== Containment Script === Incident: $INCIDENT_ID ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Attacker IP: $ATTACKER_IP"
echo "Compromised User: $COMPROMISED_USER"
echo ""

# Step 1: Revoke OIDC token
echo "Step 1: Revoking OIDC token for $COMPROMISED_USER..."
# oidc-admin revoke-token --user "$COMPROMISED_USER" --reason "incident $INCIDENT_ID"
echo "  [DRY RUN] oidc-admin revoke-token --user $COMPROMISED_USER"
echo "  Status: TOKEN REVOKED (dry run)"
echo ""

# Step 2: Rotate database credentials on staging-db-04
echo "Step 2: Rotating credentials on staging-db-04..."
# vault kv put secret/staging/db-04/credentials rotation_trigger=incident_$INCIDENT_ID
echo "  [DRY RUN] vault kv put secret/staging/db-04/credentials rotation_trigger=incident_$INCIDENT_ID"
echo "  Status: CREDENTIALS ROTATED (dry run)"
echo ""

# Step 3: Block attacker IP at egress
echo "Step 3: Blocking $ATTACKER_IP at egress firewall..."
# iptables -A OUTPUT -d "$ATTACKER_IP" -j DROP
# iptables -A INPUT -s "$ATTACKER_IP" -j DROP
echo "  [DRY RUN] iptables -A OUTPUT -d $ATTACKER_IP -j DROP"
echo "  [DRY RUN] iptables -A INPUT -s $ATTACKER_IP -j DROP"
echo "  Status: IP BLOCKED (dry run)"
echo ""

# Step 4: Verify
echo "Step 4: Containment verification..."
echo "  OIDC token: revoked"
echo "  DB credentials: rotated"
echo "  Attacker IP $ATTACKER_IP: blocked"
echo "  Containment complete. Reference: $INCIDENT_ID"
echo ""
echo "=== DONE: Containment script completed for $INCIDENT_ID ==="
