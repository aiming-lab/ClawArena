// pkg/pool.go — pool monitoring and health-check helpers.

package redis

import (
	"context"
	"log"
	"time"
)

// WatchPoolHealth logs pool stats every interval.
// Useful for alerting when pool utilisation approaches MaxPoolSize.
func WatchPoolHealth(exec *CommandExecutor, interval time.Duration) {
	go func() {
		ticker := time.NewTicker(interval)
		defer ticker.Stop()
		for range ticker.C {
			stats := exec.PoolStats()
			if stats == nil {
				continue
			}
			utilisation := float64(stats.TotalConns) / float64(exec.cfg.MaxPoolSize)
			log.Printf(
				"[redis-pool] total=%d idle=%d stale=%d util=%.1f%%",
				stats.TotalConns, stats.IdleConns, stats.StaleConns,
				utilisation*100,
			)
			if utilisation > 0.85 {
				log.Printf("[redis-pool] WARNING: pool utilisation > 85%%! Consider increasing MaxPoolSize (currently %d).", exec.cfg.MaxPoolSize)
			}
		}
	}()
}

// Ping verifies connectivity.
func (e *CommandExecutor) Ping(ctx context.Context) error {
	return e.client.Ping(ctx).Err()
}
