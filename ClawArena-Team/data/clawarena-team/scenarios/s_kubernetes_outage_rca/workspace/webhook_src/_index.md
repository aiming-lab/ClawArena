# webhook_src/ — Index

Admission webhook source code for payment-svc (wave3).

| File | Description |
|---|---|
| webhook.go | Main Go source — validateNamespace() race at line 87 |
| webhook_test.go | Test suite — TestValidateNamespace_ConcurrentAccess FAILS with -race |
| go.mod | Go module (go 1.21, stdlib only) |
| vendor/ | Vendor stub for offline testing |
| pregenerated_test_stderr.txt | Pre-generated test output (fallback if go unavailable) |

NOTE: Run `bash tools/run_webhook_tests.sh` to execute tests and see stderr.
