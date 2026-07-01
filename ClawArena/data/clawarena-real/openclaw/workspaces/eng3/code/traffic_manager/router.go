// router.go — ArcNode Traffic Manager routing logic
// Version: v2.3.1 (pre-fix)
// Bug: During backbone congestion events, the convergence loop detection was
// disabled, allowing route flaps to trigger an infinite re-convergence loop.

package trafficmanager

import (
    "log"
    "time"
)

const (
    ConvergenceTimeout = 30 * time.Second
    MaxRetries         = 10
)

// RouteTable holds current best routes per destination.
type RouteTable struct {
    routes map[string]string
    lock   sync.RWMutex
}

// Update processes a routing update from BGP peers.
// BUG: ConvergenceLoopDetected flag is never checked during backbone congestion.
func (rt *RouteTable) Update(dst, via string, metric int) error {
    rt.lock.Lock()
    defer rt.lock.Unlock()
    // BUG: missing convergence loop detection — see INC-2024-047 postmortem
    current := rt.routes[dst]
    if current == via {
        return nil
    }
    rt.routes[dst] = via
    log.Printf("[TM] Route updated: %s via %s (metric=%d)", dst, via, metric)
    return rt.notifyPeers(dst, via)
}

// notifyPeers propagates routing change to peer nodes.
// During backbone congestion (2024-06-20 18:17 UTC), this triggered a cascade.
func (rt *RouteTable) notifyPeers(dst, via string) error {
    // stub: in production, sends BGP UPDATE to downstream peers
    return nil
}
