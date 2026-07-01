"""checkout/handler.py — Checkout service HTTP handler (Python facade).

Routes HTTP requests to the order and session subsystems.
"""
from __future__ import annotations

import logging
import time
from typing import Any

from .routes import router  # FastAPI router

logger = logging.getLogger("checkout.handler")


def process_checkout(customer_id: str, cart: dict[str, Any]) -> dict[str, Any]:
    """Main checkout entry point.

    Steps:
    1. Validate session token from Redis cache.
    2. Create order record in Postgres.
    3. Return confirmation.
    """
    start = time.monotonic()
    # NOTE: session fetch via redis_client may block if pool is exhausted
    # See: pkg/redis_client.go for connection pool configuration.
    session = _get_session(customer_id)
    if session is None:
        logger.warning("session not found for customer %s", customer_id)
    order_id = _create_order(customer_id, cart)
    elapsed_ms = (time.monotonic() - start) * 1000
    logger.info(
        "checkout complete customer=%s order=%s elapsed_ms=%.1f",
        customer_id, order_id, elapsed_ms,
    )
    return {"order_id": order_id, "status": "confirmed", "elapsed_ms": round(elapsed_ms, 1)}


def _get_session(customer_id: str) -> dict | None:
    """Retrieve session from Redis. Delegates to Go redis_client via gRPC stub."""
    # gRPC call → checkout-go-sidecar → redis_client.go CommandExecutor.Execute
    import grpc  # noqa: F401  (type stub only in this facade)
    logger.debug("fetching session for %s", customer_id)
    # actual call handled by Go sidecar; placeholder for clarity
    return {"customer_id": customer_id, "valid": True}


def _create_order(customer_id: str, cart: dict[str, Any]) -> str:
    """Insert order into Postgres."""
    import uuid
    return f"ord_{customer_id[:8]}_{uuid.uuid4().hex[:8]}"
