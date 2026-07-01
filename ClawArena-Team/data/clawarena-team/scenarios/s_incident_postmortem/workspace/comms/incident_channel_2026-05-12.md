# Incident Channel — #inc-2026-05-12

Synthetic export of #inc-2026-05-12 between 14:23 UTC and 15:10 UTC.
Times are UTC. Names are aliases.

[14:23] alerts-bot: 🚨 payments-api elevated error rate (>5%) for last 60s. p99=8400ms.
[14:24] alerts-bot: 🚨 redis-fleet-2 eviction count >10k/s, sustained.
[14:24] tracy-on-call: Got the page. Looking now.
[14:25] tracy-on-call: Eviction storm on redis-fleet-2. Probably the cause — last week's runbook flagged this exact pattern.
[14:26] tracy-on-call: Going to drain redis-fleet-2 client connections to stabilise.
[14:27] samir-sre: Concur — cache eviction storm matches rb03. Tracy, want me to flip the eviction policy to allkeys-lfu temporarily?
[14:28] tracy-on-call: Yes. Pull the plug on writes from auth-edge first; that's the noisy caller per the cache-quota dashboard.
[14:29] samir-sre: Done — auth-edge writes disabled. No change yet.
[14:30] tracy-on-call: Updates on the status page. Calling it 'cache fleet under load — investigating'.
[14:33] tracy-on-call: Hmm, payments p99 still rising even after cache writes are off. Weird.
[14:35] samir-sre: Let me look at memory dashboards. payments-api memory looks crazy — 94%? Was at 60% before.
[14:36] samir-sre: Wait — payments memory pressure HIGH at 14:23 already, BEFORE the eviction storm started at 14:24. We had the order wrong.
[14:38] tracy-on-call: ...so maybe payments is the trigger, not the cache.
[14:39] tracy-on-call: Restarting payments-api pods. We'll diagnose root cause after.
[14:46] alerts-bot: ✅ payments-api error rate back below 0.5%.
[14:46] alerts-bot: ✅ redis-fleet-2 eviction normalised.
[14:48] tracy-on-call: OK we're back. I'll capture initial timeline; full RCA tomorrow. Status: cache eviction storm on redis-fleet-2, contained by pod restart.
[14:55] samir-sre: Tracy, I still think we got the direction wrong. Memory spike preceded evictions. Want to leave that in the RCA explicitly.
[15:02] tracy-on-call: Noted. Add it to the postmortem doc. I'm logging off.

## Sidebar — earlier in the day

[11:13] release-bot: morning standup notes posted in #team-platform
[12:10] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[12:16] tracy-on-call: morning standup notes posted in #team-platform
[10:45] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:15] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:21] release-bot: FYI capacity planning meeting moved to Thursday
[12:00] samir-sre: user-profile p99 at 42ms — within SLO
[10:55] bots-channel: FYI capacity planning meeting moved to Thursday
[13:46] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[11:35] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[13:38] release-bot: morning standup notes posted in #team-platform
[11:54] alerts-bot: FYI capacity planning meeting moved to Thursday
[12:27] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[10:27] tracy-on-call: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:51] tracy-on-call: morning standup notes posted in #team-platform
[11:42] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:36] samir-sre: no major releases on the calendar for Friday
[10:35] release-bot: no major releases on the calendar for Friday
[10:06] release-bot: running through the runbook rotation update with @samir-sre
[12:26] bots-channel: cache-fleet-2 throughput within nominal range this morning

## Sidebar — earlier in the day

[10:58] bots-channel: shipping the new auth-edge canary at 15% — looking healthy
[13:11] bots-channel: cache-fleet-2 throughput within nominal range this morning
[12:24] bots-channel: running through the runbook rotation update with @samir-sre
[11:42] release-bot: running through the runbook rotation update with @samir-sre
[10:59] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:11] alerts-bot: no major releases on the calendar for Friday
[12:35] bots-channel: FYI capacity planning meeting moved to Thursday
[13:24] bots-channel: no major releases on the calendar for Friday
[13:28] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[12:23] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:32] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:06] alerts-bot: user-profile p99 at 42ms — within SLO
[10:06] bots-channel: morning standup notes posted in #team-platform
[13:35] tracy-on-call: FYI capacity planning meeting moved to Thursday
[13:21] release-bot: cache-fleet-2 throughput within nominal range this morning
[13:53] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[12:22] release-bot: FYI capacity planning meeting moved to Thursday
[11:25] bots-channel: cache-fleet-2 throughput within nominal range this morning
[13:09] bots-channel: morning standup notes posted in #team-platform
[13:38] release-bot: cache-fleet-2 throughput within nominal range this morning

## Sidebar — earlier in the day

[12:32] tracy-on-call: FYI capacity planning meeting moved to Thursday
[11:52] bots-channel: cache-fleet-2 throughput within nominal range this morning
[10:37] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[12:57] release-bot: cache-fleet-2 throughput within nominal range this morning
[10:44] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:46] release-bot: morning standup notes posted in #team-platform
[13:22] bots-channel: morning standup notes posted in #team-platform
[11:34] bots-channel: FYI capacity planning meeting moved to Thursday
[10:06] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[12:19] bots-channel: FYI capacity planning meeting moved to Thursday
[12:28] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[12:42] samir-sre: FYI capacity planning meeting moved to Thursday
[10:15] samir-sre: user-profile p99 at 42ms — within SLO
[13:25] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[13:30] samir-sre: FYI capacity planning meeting moved to Thursday
[11:44] samir-sre: FYI capacity planning meeting moved to Thursday
[13:21] bots-channel: user-profile p99 at 42ms — within SLO
[12:02] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:00] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:22] tracy-on-call: FYI capacity planning meeting moved to Thursday

## Sidebar — earlier in the day

[12:46] samir-sre: cache-fleet-2 throughput within nominal range this morning
[10:09] alerts-bot: no major releases on the calendar for Friday
[12:51] tracy-on-call: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:57] samir-sre: no major releases on the calendar for Friday
[12:06] samir-sre: morning standup notes posted in #team-platform
[13:57] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[11:26] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[11:46] samir-sre: morning standup notes posted in #team-platform
[13:53] release-bot: running through the runbook rotation update with @samir-sre
[13:26] tracy-on-call: running through the runbook rotation update with @samir-sre
[11:37] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[10:48] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:21] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[13:01] bots-channel: user-profile p99 at 42ms — within SLO
[11:14] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:38] samir-sre: no major releases on the calendar for Friday
[13:41] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[13:50] tracy-on-call: FYI capacity planning meeting moved to Thursday
[12:20] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[12:19] release-bot: shipping the new auth-edge canary at 15% — looking healthy

## Sidebar — earlier in the day

[13:45] samir-sre: no major releases on the calendar for Friday
[13:01] samir-sre: no major releases on the calendar for Friday
[12:32] release-bot: morning standup notes posted in #team-platform
[12:10] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[13:25] release-bot: morning standup notes posted in #team-platform
[12:30] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[10:56] samir-sre: FYI capacity planning meeting moved to Thursday
[10:14] tracy-on-call: no major releases on the calendar for Friday
[13:16] bots-channel: user-profile p99 at 42ms — within SLO
[11:14] samir-sre: user-profile p99 at 42ms — within SLO
[11:19] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[12:13] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[10:53] tracy-on-call: FYI capacity planning meeting moved to Thursday
[13:38] bots-channel: cache-fleet-2 throughput within nominal range this morning
[13:35] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[12:48] release-bot: no major releases on the calendar for Friday
[12:34] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:39] release-bot: morning standup notes posted in #team-platform
[13:43] tracy-on-call: morning standup notes posted in #team-platform
[12:16] samir-sre: morning standup notes posted in #team-platform

## Sidebar — earlier in the day

[13:06] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[12:07] bots-channel: no major releases on the calendar for Friday
[13:40] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[13:01] samir-sre: running through the runbook rotation update with @samir-sre
[10:17] bots-channel: user-profile p99 at 42ms — within SLO
[11:28] alerts-bot: no major releases on the calendar for Friday
[11:27] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[10:00] release-bot: user-profile p99 at 42ms — within SLO
[11:46] release-bot: user-profile p99 at 42ms — within SLO
[13:16] tracy-on-call: FYI capacity planning meeting moved to Thursday
[12:09] tracy-on-call: no major releases on the calendar for Friday
[13:56] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:15] bots-channel: user-profile p99 at 42ms — within SLO
[13:38] bots-channel: running through the runbook rotation update with @samir-sre
[12:53] bots-channel: no major releases on the calendar for Friday
[12:48] samir-sre: cache-fleet-2 throughput within nominal range this morning
[12:01] alerts-bot: running through the runbook rotation update with @samir-sre
[10:41] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[10:23] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[13:21] alerts-bot: running through the runbook rotation update with @samir-sre

## Sidebar — earlier in the day

[11:18] bots-channel: running through the runbook rotation update with @samir-sre
[11:19] release-bot: running through the runbook rotation update with @samir-sre
[13:51] tracy-on-call: morning standup notes posted in #team-platform
[12:19] samir-sre: cache-fleet-2 throughput within nominal range this morning
[11:19] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[11:49] release-bot: no major releases on the calendar for Friday
[10:07] alerts-bot: no major releases on the calendar for Friday
[12:43] tracy-on-call: user-profile p99 at 42ms — within SLO
[11:42] tracy-on-call: FYI capacity planning meeting moved to Thursday
[13:33] bots-channel: running through the runbook rotation update with @samir-sre
[12:49] alerts-bot: morning standup notes posted in #team-platform
[10:15] samir-sre: FYI capacity planning meeting moved to Thursday
[12:01] samir-sre: morning standup notes posted in #team-platform
[11:55] tracy-on-call: FYI capacity planning meeting moved to Thursday
[10:55] tracy-on-call: morning standup notes posted in #team-platform
[13:11] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[11:15] tracy-on-call: morning standup notes posted in #team-platform
[13:42] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[11:33] tracy-on-call: running through the runbook rotation update with @samir-sre
[10:46] release-bot: user-profile p99 at 42ms — within SLO

## Sidebar — earlier in the day

[10:26] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:34] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:17] samir-sre: running through the runbook rotation update with @samir-sre
[13:20] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[13:09] tracy-on-call: user-profile p99 at 42ms — within SLO
[11:59] release-bot: cache-fleet-2 throughput within nominal range this morning
[13:24] alerts-bot: no major releases on the calendar for Friday
[12:04] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:54] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:23] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:27] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[12:41] samir-sre: FYI capacity planning meeting moved to Thursday
[11:14] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[12:48] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[10:39] tracy-on-call: FYI capacity planning meeting moved to Thursday
[11:05] release-bot: user-profile p99 at 42ms — within SLO
[13:52] bots-channel: FYI capacity planning meeting moved to Thursday
[11:03] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[11:51] alerts-bot: FYI capacity planning meeting moved to Thursday
[12:35] alerts-bot: user-profile p99 at 42ms — within SLO

## Sidebar — earlier in the day

[10:53] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:03] release-bot: morning standup notes posted in #team-platform
[13:17] bots-channel: cache-fleet-2 throughput within nominal range this morning
[12:05] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[10:29] tracy-on-call: morning standup notes posted in #team-platform
[10:08] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[12:15] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:42] alerts-bot: FYI capacity planning meeting moved to Thursday
[13:25] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[13:18] tracy-on-call: no major releases on the calendar for Friday
[13:34] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[10:45] tracy-on-call: running through the runbook rotation update with @samir-sre
[11:25] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:14] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:59] release-bot: FYI capacity planning meeting moved to Thursday
[11:30] samir-sre: running through the runbook rotation update with @samir-sre
[12:10] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[11:16] samir-sre: no major releases on the calendar for Friday
[11:05] samir-sre: FYI capacity planning meeting moved to Thursday
[10:41] tracy-on-call: running through the runbook rotation update with @samir-sre

## Sidebar — earlier in the day

[11:26] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:33] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:31] bots-channel: morning standup notes posted in #team-platform
[10:48] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:53] release-bot: no major releases on the calendar for Friday
[11:33] alerts-bot: running through the runbook rotation update with @samir-sre
[12:08] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:52] tracy-on-call: FYI capacity planning meeting moved to Thursday
[10:39] tracy-on-call: morning standup notes posted in #team-platform
[12:47] alerts-bot: user-profile p99 at 42ms — within SLO
[13:38] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[13:04] release-bot: running through the runbook rotation update with @samir-sre
[10:10] samir-sre: user-profile p99 at 42ms — within SLO
[10:09] release-bot: user-profile p99 at 42ms — within SLO
[10:14] release-bot: user-profile p99 at 42ms — within SLO
[12:52] bots-channel: running through the runbook rotation update with @samir-sre
[10:10] release-bot: user-profile p99 at 42ms — within SLO
[10:44] samir-sre: running through the runbook rotation update with @samir-sre
[12:00] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[10:57] alerts-bot: no major releases on the calendar for Friday

## Sidebar — earlier in the day

[13:31] samir-sre: running through the runbook rotation update with @samir-sre
[13:34] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:12] alerts-bot: user-profile p99 at 42ms — within SLO
[13:56] release-bot: no major releases on the calendar for Friday
[10:32] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:37] alerts-bot: running through the runbook rotation update with @samir-sre
[12:04] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[13:18] alerts-bot: no major releases on the calendar for Friday
[12:51] bots-channel: running through the runbook rotation update with @samir-sre
[12:52] bots-channel: morning standup notes posted in #team-platform
[13:33] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[10:45] release-bot: user-profile p99 at 42ms — within SLO
[13:13] samir-sre: no major releases on the calendar for Friday
[11:58] bots-channel: cache-fleet-2 throughput within nominal range this morning
[13:43] tracy-on-call: morning standup notes posted in #team-platform
[12:56] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[10:12] alerts-bot: FYI capacity planning meeting moved to Thursday
[10:03] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:21] samir-sre: morning standup notes posted in #team-platform
[13:48] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC

## Sidebar — earlier in the day

[11:39] tracy-on-call: no major releases on the calendar for Friday
[12:47] release-bot: morning standup notes posted in #team-platform
[13:45] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:23] bots-channel: FYI capacity planning meeting moved to Thursday
[13:24] alerts-bot: no major releases on the calendar for Friday
[12:29] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[10:10] bots-channel: user-profile p99 at 42ms — within SLO
[10:29] alerts-bot: running through the runbook rotation update with @samir-sre
[13:15] alerts-bot: running through the runbook rotation update with @samir-sre
[12:06] bots-channel: running through the runbook rotation update with @samir-sre
[11:19] alerts-bot: morning standup notes posted in #team-platform
[11:07] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[13:07] tracy-on-call: no major releases on the calendar for Friday
[10:41] alerts-bot: FYI capacity planning meeting moved to Thursday
[12:06] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[13:57] release-bot: running through the runbook rotation update with @samir-sre
[11:36] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[11:37] tracy-on-call: running through the runbook rotation update with @samir-sre
[12:00] bots-channel: FYI capacity planning meeting moved to Thursday
[12:06] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy

## Sidebar — earlier in the day

[12:56] bots-channel: cache-fleet-2 throughput within nominal range this morning
[12:44] alerts-bot: user-profile p99 at 42ms — within SLO
[13:47] tracy-on-call: morning standup notes posted in #team-platform
[12:47] samir-sre: shipping the new auth-edge canary at 15% — looking healthy
[10:56] release-bot: FYI capacity planning meeting moved to Thursday
[12:05] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[11:38] bots-channel: no major releases on the calendar for Friday
[12:55] samir-sre: morning standup notes posted in #team-platform
[13:23] samir-sre: no major releases on the calendar for Friday
[11:57] alerts-bot: morning standup notes posted in #team-platform
[13:49] bots-channel: running through the runbook rotation update with @samir-sre
[13:48] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[11:33] bots-channel: morning standup notes posted in #team-platform
[11:25] bots-channel: morning standup notes posted in #team-platform
[11:46] release-bot: user-profile p99 at 42ms — within SLO
[10:39] samir-sre: cache-fleet-2 throughput within nominal range this morning
[13:34] tracy-on-call: morning standup notes posted in #team-platform
[11:22] bots-channel: FYI capacity planning meeting moved to Thursday
[10:40] samir-sre: user-profile p99 at 42ms — within SLO
[11:28] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC

## Sidebar — earlier in the day

[11:02] release-bot: user-profile p99 at 42ms — within SLO
[10:34] tracy-on-call: running through the runbook rotation update with @samir-sre
[13:44] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy
[10:16] release-bot: FYI capacity planning meeting moved to Thursday
[10:10] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:28] bots-channel: FYI capacity planning meeting moved to Thursday
[13:56] release-bot: FYI capacity planning meeting moved to Thursday
[10:33] bots-channel: morning standup notes posted in #team-platform
[13:10] tracy-on-call: no major releases on the calendar for Friday
[10:44] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[10:33] bots-channel: no major releases on the calendar for Friday
[12:56] release-bot: user-profile p99 at 42ms — within SLO
[11:56] alerts-bot: no major releases on the calendar for Friday
[11:41] samir-sre: running through the runbook rotation update with @samir-sre
[11:29] alerts-bot: morning standup notes posted in #team-platform
[10:41] samir-sre: morning standup notes posted in #team-platform
[10:41] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[12:12] alerts-bot: morning standup notes posted in #team-platform
[11:53] release-bot: cache-fleet-2 throughput within nominal range this morning
[11:00] bots-channel: no major releases on the calendar for Friday

## Sidebar — earlier in the day

[13:10] bots-channel: user-profile p99 at 42ms — within SLO
[13:47] samir-sre: running through the runbook rotation update with @samir-sre
[10:06] samir-sre: morning standup notes posted in #team-platform
[11:29] release-bot: user-profile p99 at 42ms — within SLO
[13:04] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:45] bots-channel: FYI capacity planning meeting moved to Thursday
[13:35] bots-channel: shipping the new auth-edge canary at 15% — looking healthy
[10:10] alerts-bot: user-profile p99 at 42ms — within SLO
[10:39] release-bot: running through the runbook rotation update with @samir-sre
[12:55] samir-sre: FYI capacity planning meeting moved to Thursday
[10:56] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[11:59] tracy-on-call: user-profile p99 at 42ms — within SLO
[13:11] bots-channel: cache-fleet-2 throughput within nominal range this morning
[11:51] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:59] release-bot: running through the runbook rotation update with @samir-sre
[13:52] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[10:45] bots-channel: running through the runbook rotation update with @samir-sre
[13:32] tracy-on-call: no major releases on the calendar for Friday
[11:49] release-bot: FYI capacity planning meeting moved to Thursday
[11:19] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy

## Sidebar — earlier in the day

[10:38] alerts-bot: FYI capacity planning meeting moved to Thursday
[13:44] bots-channel: shipping the new auth-edge canary at 15% — looking healthy
[13:58] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:34] alerts-bot: morning standup notes posted in #team-platform
[10:55] samir-sre: FYI capacity planning meeting moved to Thursday
[10:22] alerts-bot: user-profile p99 at 42ms — within SLO
[13:13] bots-channel: cache-fleet-2 throughput within nominal range this morning
[10:33] bots-channel: FYI capacity planning meeting moved to Thursday
[13:16] release-bot: user-profile p99 at 42ms — within SLO
[13:33] tracy-on-call: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:18] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[13:57] alerts-bot: morning standup notes posted in #team-platform
[11:22] samir-sre: cache-fleet-2 throughput within nominal range this morning
[10:11] alerts-bot: morning standup notes posted in #team-platform
[12:38] alerts-bot: running through the runbook rotation update with @samir-sre
[13:36] bots-channel: FYI capacity planning meeting moved to Thursday
[11:33] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:38] alerts-bot: FYI capacity planning meeting moved to Thursday
[10:38] bots-channel: cache-fleet-2 throughput within nominal range this morning
[13:16] samir-sre: running through the runbook rotation update with @samir-sre

## Sidebar — earlier in the day

[10:59] alerts-bot: morning standup notes posted in #team-platform
[11:29] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[10:09] samir-sre: user-profile p99 at 42ms — within SLO
[12:17] release-bot: shipping the new auth-edge canary at 15% — looking healthy
[13:18] alerts-bot: FYI capacity planning meeting moved to Thursday
[10:11] release-bot: morning standup notes posted in #team-platform
[13:24] samir-sre: running through the runbook rotation update with @samir-sre
[12:06] alerts-bot: FYI capacity planning meeting moved to Thursday
[11:24] tracy-on-call: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:49] bots-channel: morning standup notes posted in #team-platform
[11:41] samir-sre: cache-fleet-2 throughput within nominal range this morning
[13:15] bots-channel: shipping the new auth-edge canary at 15% — looking healthy
[10:51] bots-channel: morning standup notes posted in #team-platform
[10:58] samir-sre: no major releases on the calendar for Friday
[13:29] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[12:36] samir-sre: cache-fleet-2 throughput within nominal range this morning
[10:56] alerts-bot: FYI capacity planning meeting moved to Thursday
[10:29] samir-sre: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:48] bots-channel: cache-fleet-2 throughput within nominal range this morning
[12:25] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC

## Sidebar — earlier in the day

[13:26] bots-channel: morning standup notes posted in #team-platform
[12:53] release-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[10:58] release-bot: running through the runbook rotation update with @samir-sre
[13:21] alerts-bot: cache-fleet-2 throughput within nominal range this morning
[11:25] samir-sre: running through the runbook rotation update with @samir-sre
[12:04] bots-channel: cache-fleet-2 throughput within nominal range this morning
[11:22] alerts-bot: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:55] tracy-on-call: cache-fleet-2 throughput within nominal range this morning
[11:17] alerts-bot: user-profile p99 at 42ms — within SLO
[10:54] tracy-on-call: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:12] samir-sre: morning standup notes posted in #team-platform
[12:03] release-bot: no major releases on the calendar for Friday
[11:26] release-bot: no major releases on the calendar for Friday
[10:37] alerts-bot: user-profile p99 at 42ms — within SLO
[10:52] samir-sre: no major releases on the calendar for Friday
[11:22] alerts-bot: FYI capacity planning meeting moved to Thursday
[10:23] bots-channel: user-profile p99 at 42ms — within SLO
[13:47] bots-channel: morning standup notes posted in #team-platform
[13:50] alerts-bot: running through the runbook rotation update with @samir-sre
[10:56] alerts-bot: shipping the new auth-edge canary at 15% — looking healthy

## Sidebar — earlier in the day

[12:16] samir-sre: user-profile p99 at 42ms — within SLO
[11:26] bots-channel: FYI capacity planning meeting moved to Thursday
[10:28] samir-sre: user-profile p99 at 42ms — within SLO
[11:28] tracy-on-call: morning standup notes posted in #team-platform
[13:40] release-bot: FYI capacity planning meeting moved to Thursday
[13:36] tracy-on-call: morning standup notes posted in #team-platform
[13:04] tracy-on-call: shipping the new auth-edge canary at 15% — looking healthy
[11:57] samir-sre: morning standup notes posted in #team-platform
[11:24] alerts-bot: user-profile p99 at 42ms — within SLO
[10:59] bots-channel: deployment of orders-api v23.4 succeeded at 11:02 UTC
[13:14] tracy-on-call: deployment of orders-api v23.4 succeeded at 11:02 UTC
[11:17] tracy-on-call: morning standup notes posted in #team-platform
[11:02] samir-sre: FYI capacity planning meeting moved to Thursday
[10:32] bots-channel: morning standup notes posted in #team-platform
[11:49] tracy-on-call: user-profile p99 at 42ms — within SLO
[12:49] samir-sre: morning standup notes posted in #team-platform
[13:15] samir-sre: no major releases on the calendar for Friday
[13:45] release-bot: running through the runbook rotation update with @samir-sre
[12:43] bots-channel: FYI capacity planning meeting moved to Thursday
[10:55] samir-sre: FYI capacity planning meeting moved to Thursday
