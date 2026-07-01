# Slack — #incidents (2026-05-23 18:42–19:05)

**alertbot** [18:42]: :rotating_light: SEV-2 checkout-service p99 > 200ms
**sarah_sre** [18:43]: On it. Pulling Jaeger. Anyone else seeing errors?
**devops_raj** [18:44]: Error rate jumped to 12% in checkout. Order-service looks fine.
**alice_dev** [18:45]: Just deployed redis-client-v3.2.1 yesterday (2026-05-22). Pool config changed.
**sarah_sre** [18:46]: Good lead. Checking the Go code now.
**bob_arch** [18:48]: Is it the postgres connections again? We had that last quarter.
**sarah_sre** [18:49]: Trace says Redis, not postgres. The slow span is in CommandExecutor.
**alice_dev** [18:51]: Found it — MaxPoolSize dropped from 20 to 5 in v3.2.1. PR #4412.
**devops_raj** [18:52]: Roll back redis-client or hotfix?
**sarah_sre** [18:53]: Roll back to v3.1.x, then scale pool in config. Applying now.
**alertbot** [19:04]: :white_check_mark: checkout-service.p99_latency recovered (44 ms).
**sarah_sre** [19:05]: Good. Will file postmortem. Root cause confirmed: pool exhaustion.
