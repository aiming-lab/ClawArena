module github.com/example/payment-admission-webhook

go 1.21

// No external dependencies — this package uses only stdlib.
// In production the webhook uses k8s.io/client-go, vendored below.
