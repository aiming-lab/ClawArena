#!/usr/bin/env bash
# check_vulnerable.sh — 检测本机 OpenSSH 版本是否受 CVE-2024-6387 影响
# 受影响范围: 8.5p1 <= openssh < 9.8p1 (glibc-based Linux)

set -euo pipefail

AFFECTED_MIN="8.5p1"
PATCHED_VERSION="9.8p1"
CVE="CVE-2024-6387"

echo "=== SSH Version Vulnerability Check for $CVE ==="

if ! command -v ssh &>/dev/null; then
    echo "ERROR: ssh command not found"
    exit 1
fi

SSH_VERSION=$(ssh -V 2>&1 | grep -oP 'OpenSSH_[0-9]+\.[0-9]+p[0-9]+')
echo "Detected: $SSH_VERSION"

# Parse version numbers for comparison
MAJOR=$(echo "$SSH_VERSION" | grep -oP '(?<=OpenSSH_)\d+')
MINOR=$(echo "$SSH_VERSION" | grep -oP '(?<=\.)\d+(?=p)')
PATCH=$(echo "$SSH_VERSION" | grep -oP '(?<=p)\d+')

# Vulnerable: 8.5p1 <= version <= 9.7p1
if [[ "$MAJOR" -eq 8 && "$MINOR" -ge 5 ]] || [[ "$MAJOR" -eq 9 && "$MINOR" -le 7 ]]; then
    echo "RESULT: VULNERABLE to $CVE"
    echo "Recommended: Upgrade to OpenSSH $PATCHED_VERSION or apply workaround (LoginGraceTime 0)"
    exit 1
else
    echo "RESULT: NOT VULNERABLE to $CVE"
    echo "Current version $SSH_VERSION is either pre-regression or patched."
    exit 0
fi
