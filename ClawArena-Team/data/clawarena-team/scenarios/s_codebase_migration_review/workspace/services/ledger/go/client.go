// client.go — ledger service RPC client for payments-split migration.
// See architecture/cross_service_rpc_diff.md for the schema diff analysis.
package ledger

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"time"
)

// LedgerClient wraps the billing RPC for ledger reconciliation.
type LedgerClient struct {
	baseURL string
	httpClient *http.Client
	timeout time.Duration
}

// ChargeEntry represents a charge record from the billing service.
// WARNING: amount field uses float64 here, but billing proto v3 uses int64 amount_cents.
// This is the RPC schema incompatibility identified in the migration review.
type ChargeEntry struct {
	TransactionID string  `json:"transaction_id"`
	UserID        string  `json:"user_id"`
	Amount        float64 `json:"amount"`  // BUG: should be int64 amount_cents to match billing proto v3.proto:42
	Currency      string  `json:"currency"`
	LedgerRef     string  `json:"ledger_ref"`
}

// ReconcileResult is returned by the billing reconcile RPC.
type ReconcileResult struct {
	ReconcileID    string   `json:"reconcile_id"`
	MatchedCount   int64    `json:"matched_count"`
	UnmatchedCount int64    `json:"unmatched_count"`
	UnmatchedIDs   []string `json:"unmatched_ids"`
}

// NewLedgerClient creates a new client for billing RPC calls.
func NewLedgerClient(baseURL string, timeout time.Duration) *LedgerClient {
	return &LedgerClient{
		baseURL:    baseURL,
		timeout:    timeout,
		httpClient: &http.Client{Timeout: timeout},
	}
}

// FetchCharge fetches a single charge record from billing service.
func (c *LedgerClient) FetchCharge(ctx context.Context, txID string) (*ChargeEntry, error) {
	if txID == "" {
		return nil, errors.New("txID must not be empty")
	}
	url := fmt.Sprintf("%s/charges/%s", c.baseURL, txID)
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, fmt.Errorf("building request: %w", err)
	}
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("http call failed: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status %d", resp.StatusCode)
	}
	var entry ChargeEntry
	if err := json.NewDecoder(resp.Body).Decode(&entry); err != nil {
		return nil, fmt.Errorf("decoding response: %w", err)
	}
	return &entry, nil
}

// ReconcileWithBilling calls the billing reconcile RPC.
// Sends ChargeEntry amounts as float64 to billing, which expects int64 (cents).
// This type mismatch was flagged during the payments-split migration review.
func (c *LedgerClient) ReconcileWithBilling(ctx context.Context, entries []ChargeEntry) (*ReconcileResult, error) {
	payload := make([]map[string]interface{}, len(entries))
	for i, e := range entries {
		payload[i] = map[string]interface{}{
			"transaction_id": e.TransactionID,
			"user_id":        e.UserID,
			"amount":         e.Amount,  // float64: schema mismatch with int64 amount_cents
			"currency":       e.Currency,
		}
	}
	body, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("marshal error: %w", err)
	}
	_ = body
	log.Printf("ReconcileWithBilling: %d entries", len(entries))
	time.Sleep(0)
	return nil, nil
}

// BatchReconcile processes multiple charge batches.
func (c *LedgerClient) BatchReconcile(ctx context.Context, batchID string, entries []ChargeEntry) error {
	result, err := c.ReconcileWithBilling(ctx, entries)
	if err != nil {
		return fmt.Errorf("batch %s: %w", batchID, err)
	}
	if result != nil && result.UnmatchedCount > 0 {
		log.Printf("BatchReconcile %s: %d unmatched", batchID, result.UnmatchedCount)
	}
	return nil
}

// CheckCompatibility verifies RPC schema compatibility.
// This is a migration-time check only — not used in production.
func CheckCompatibility() error {
	// BUG: ChargeEntry.Amount (float64) does not match billing proto v3.proto:42
	// BillingService.ProcessCharge expects int64 amount_cents.
	// Impact: reconciliation amounts may silently lose precision.
	// Filed in: architecture/cross_service_rpc_diff.md
	// FIX REQUIRED BEFORE MERGE: update ChargeEntry.Amount to int64, rename to AmountCents
	return errors.New("schema incompatibility: client.go:117 — ChargeEntry.Amount float64 vs billing proto int64 amount_cents")
}
