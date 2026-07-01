package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)

// namespaceCache stores per-namespace label snapshots.
// KNOWN ISSUE: validateNamespace() has a race condition at line 87.
type namespaceCache struct {
	mu    sync.RWMutex
	cache map[string]map[string]string
}

var nsCache = &namespaceCache{cache: make(map[string]map[string]string)}

// refreshNamespaceCache updates nsCache every 30s in a background goroutine.
// BUG: The write lock is acquired AFTER the List call; concurrent readers in
// validateNamespace() may read a partially-updated entry.
func refreshNamespaceCache(ctx context.Context) {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			// Simulate namespace fetch (in production uses k8s client)
			newLabels := map[string]map[string]string{
				"payments": {"admission-webhook": "enabled", "env": "production"},
			}
			// BUG: lock acquired too late — window between newLabels population
			// and Lock() allows concurrent readers to see inconsistent state
			nsCache.mu.Lock()
			for ns, labels := range newLabels {
				nsCache.cache[ns] = labels
			}
			nsCache.mu.Unlock()
		}
	}
}

// validateNamespace checks whether the target namespace has the required label.
//
// RACE CONDITION (line 87): nsCache.mu.RLock() is called AFTER an unlocked
// read of nsCache.cache[namespace] on line 86. Under concurrent load, a
// background refreshNamespaceCache() goroutine may be writing a new snapshot
// between the two reads, yielding a partially-updated label map.
func validateNamespace(namespace string) (bool, string) {
	// Line 85: fast-path check — intentionally unlocked
	existingLabels, found := nsCache.cache[namespace] // line 86: UNLOCKED READ
	if !found {
		nsCache.mu.RLock() // line 87: <<< RACE: lock acquired after unlocked read above
		defer nsCache.mu.RUnlock()
		existingLabels, found = nsCache.cache[namespace]
		if !found {
			return false, fmt.Sprintf("namespace %q not in cache", namespace)
		}
	}

	if val, ok := existingLabels["admission-webhook"]; !ok || val != "enabled" {
		return false, fmt.Sprintf("namespace %q missing admission-webhook=enabled label", namespace)
	}
	return true, ""
}

// admitPod is the core admission handler.
func admitPod(namespace string) (bool, string) {
	return validateNamespace(namespace)
}

func serveAdmit(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Namespace string `json:"namespace"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	allowed, reason := admitPod(req.Namespace)
	resp := map[string]interface{}{"allowed": allowed, "reason": reason}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	go refreshNamespaceCache(ctx)

	// Seed initial cache
	nsCache.mu.Lock()
	nsCache.cache["payments"] = map[string]string{"admission-webhook": "enabled"}
	nsCache.mu.Unlock()

	http.HandleFunc("/validate", serveAdmit)
	log.Println("Admission webhook listening on :8443")
	log.Fatal(http.ListenAndServeTLS(":8443", "/certs/tls.crt", "/certs/tls.key", nil))
}
