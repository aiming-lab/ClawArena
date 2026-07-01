"""checkout/routes.py — FastAPI route definitions."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .handler import process_checkout

router = APIRouter(prefix="/api/v2")


class CheckoutRequest(BaseModel):
    customer_id: str
    items: list[dict]


class CheckoutResponse(BaseModel):
    order_id: str
    status: str
    elapsed_ms: float


@router.post("/checkout", response_model=CheckoutResponse)
async def checkout(req: CheckoutRequest) -> CheckoutResponse:
    try:
        result = process_checkout(req.customer_id, {"items": req.items})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return CheckoutResponse(**result)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
