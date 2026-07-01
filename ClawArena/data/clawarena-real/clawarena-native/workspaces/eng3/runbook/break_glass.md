# Break-Glass Emergency Operations

## When to Use

Use these procedures only during active SEV-1 when normal tooling is impaired.

## Disable DDoS Rate-Limit Rule (Emergency)

```bash
# Disable DDoS mitigation rule globally
arcnode-admin rule disable --rule-id ddos-mit-2024-0620 --global
```

## Force Restart Edge Lua Workers

```bash
# Restart all Lua workers on affected PoPs
arcnode-admin lua-workers restart --region europe-west --all
```

## Traffic Manager Failover

```bash
# Override Traffic Manager route convergence
arcnode-admin tm failover --mode manual --target stable-backbone
```

## Post-Emergency Checklist

- [ ] Document break-glass actions in postmortem timeline
- [ ] Notify EM (Zhang Lei) of any break-glass usage
- [ ] Schedule review of break-glass effectiveness within 48h
