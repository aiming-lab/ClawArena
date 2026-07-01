# Patch Verification Checklist — CVE-2024-6387

## Pre-Patch Verification
- [ ] Confirm host is in affected version range (8.5p1 – 9.7p1)
- [ ] Schedule maintenance window
- [ ] Backup current sshd_config
- [ ] Confirm patch availability for OS platform

## Patch Application
- [ ] Apply OS package update (e.g., dnf update openssh)
- [ ] Verify installed version: `ssh -V`
- [ ] For RHEL 9: confirm openssh-8.7p1-38.el9_4.1 installed
- [ ] For RHEL 8: confirm openssh-8.0p1-19.el8_10.1 installed (RHSA-2024:4340)
- [ ] Restart sshd: `systemctl restart sshd`

## Post-Patch Verification
- [ ] Confirm sshd is running: `systemctl status sshd`
- [ ] Verify SSH connectivity (test from bastion host)
- [ ] Confirm version no longer in vulnerable range
- [ ] Update internal_inventory.csv is_vulnerable field

## Documentation
- [ ] Record patch date in remediation tracking
- [ ] Update risk register entry
- [ ] Submit compliance evidence to security team
