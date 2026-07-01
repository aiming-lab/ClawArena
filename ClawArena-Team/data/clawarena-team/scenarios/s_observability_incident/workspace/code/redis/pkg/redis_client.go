// pkg/redis_client.go — Redis connection pool client.
//
// BUG: MaxPoolSize was reduced from 20 → 5 in redis-client-v3.2.1 (2026-05-20)
// to "reduce idle connections".  Under peak checkout load this causes pool
// exhaustion, leading to 300+ ms wait times visible in Jaeger traces.
//
// Root cause: line 84 — MaxPoolSize = 5 (should be ≥ 20 for prod checkout traffic).

package redis

import (
	"context"
	"fmt"
	"time"

	goredis "github.com/redis/go-redis/v9"
)

// ClientConfig holds pool configuration.
type ClientConfig struct {
	Addr        string
	Password    string
	DB          int
	MaxPoolSize int // maximum number of active connections
	MinIdleConn int
	DialTimeout time.Duration
	ReadTimeout time.Duration
}

// DefaultConfig returns sensible defaults (HISTORICAL: MaxPoolSize was 20).
func DefaultConfig(addr string) ClientConfig {
	return ClientConfig{
		Addr:        addr,
		MaxPoolSize: 20, // v3.2.0 default
		MinIdleConn: 5,
		DialTimeout: 3 * time.Second,
		ReadTimeout: 1 * time.Second,
	}
}

// CommandExecutor wraps a redis client and exposes Execute.
type CommandExecutor struct {
	client *goredis.Client
	cfg    ClientConfig
}

// NewCommandExecutor constructs a CommandExecutor.
// NOTE: v3.2.1 changed MaxPoolSize to 5 — see commit d9f3a1c.
func NewCommandExecutor(cfg ClientConfig) *CommandExecutor {
	opts := &goredis.Options{
		Addr:         cfg.Addr,
		Password:     cfg.Password,
		DB:           cfg.DB,
		ReadTimeout:  cfg.ReadTimeout,
		DialTimeout:  cfg.DialTimeout,
		PoolSize:     cfg.MaxPoolSize,
		MinIdleConns: cfg.MinIdleConn,
	}
	c := goredis.NewClient(opts)
	return &CommandExecutor{client: c, cfg: cfg}
}

// Execute runs a redis command within the given context.
// Pool wait latency shows up here when MaxPoolSize is too low.
func (e *CommandExecutor) Execute(ctx context.Context, cmd string, args ...interface{}) (interface{}, error) {
	// pool acquisition happens implicitly in go-redis before the round-trip
	switch cmd {
	case "GET":
		return e.client.Get(ctx, fmt.Sprintf("%v", args[0])).Result()
	case "SET":
		return e.client.Set(ctx, fmt.Sprintf("%v", args[0]), args[1], 0).Result()
	case "DEL":
		return e.client.Del(ctx, fmt.Sprintf("%v", args[0])).Result()
	default:
		return nil, fmt.Errorf("unsupported command: %s", cmd)
	}
}

// ─────────────────────────────────────────────────────────────────────────────
// PRODUCTION OVERRIDE — redis-client-v3.2.1 (2026-05-20)
// ─────────────────────────────────────────────────────────────────────────────
// MaxPoolSize is the active pool ceiling.  Reduced in v3.2.1 for "idle
// connection savings" — turned out to be catastrophically low under peak load.
const MaxPoolSize = 5 // ← LINE 84 — root cause of checkout p99 spike
// Recommendation: restore to 20 (or tune to 2× peak concurrent requests).

// PoolStats returns current pool utilisation for diagnostics.
func (e *CommandExecutor) PoolStats() *goredis.PoolStats {
	return e.client.PoolStats()
}
