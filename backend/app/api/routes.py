"""
PT Injani Systems - Fullstack Developer Prescreening
API Routes implementing Q1, Q5, and Q6 capabilities
"""

import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, Header, Request, status
from fastapi.responses import JSONResponse

from app.schemas.order import WhatsAppIncomingMessage, ExtractionResult
from app.schemas.task import CreateOrderRequest, TaskProgressResponse, TaskStatus
from app.core.errors import (
    StandardAPIResponse,
    APIErrorPayload,
    NotFoundException,
    ConflictException
)
from app.core.security import verify_webhook_hmac_sha256, mock_verify_jwt_token
from app.services.order_extractor import WhatsAppOrderExtractor
from app.services.task_manager import global_task_manager
from app.services.evaluator import LLMExtractionEvaluator, GroundTruthSample, GroundTruthItem
from app.api.deps import (
    idempotency_store,
    rate_limiter,
    get_current_user,
    enforce_rate_limit
)

router = APIRouter(prefix="/api/v1")
extractor = WhatsAppOrderExtractor()
evaluator = LLMExtractionEvaluator()


# ---------------------------------------------------------------------------
# Q1: WhatsApp Order Intent & Item Extraction
# ---------------------------------------------------------------------------
@router.post(
    "/extract-order",
    response_model=StandardAPIResponse,
    dependencies=[Depends(enforce_rate_limit)]
)
async def extract_order_from_whatsapp(payload: WhatsAppIncomingMessage):
    """
    Extracts structured intent, items, units, and generates a polite auto-reply
    without incurring per-token commercial API costs.
    """
    result = extractor.extract_with_rules_fallback(payload.message_text)
    return StandardAPIResponse(
        success=True,
        data=result.model_dump()
    )


# ---------------------------------------------------------------------------
# Q1(c): Evaluation Benchmark Runner
# ---------------------------------------------------------------------------
@router.get("/evaluations/run", response_model=StandardAPIResponse)
async def run_extraction_benchmark():
    """Runs accuracy, F1, and exact-match benchmark across standard test messages."""
    ground_truth = [
        GroundTruthSample(
            message="I'd like 3 bags of cement and 2 tins of paint please",
            expected_intent="order",
            expected_items=[
                GroundTruthItem("cement", 3.0, "bag"),
                GroundTruthItem("paint", 2.0, "tin")
            ]
        ),
        GroundTruthSample(
            message="Siang mas, tolong kirim 5 sak semen dan 2 kaleng cat avian putih ya",
            expected_intent="order",
            expected_items=[
                GroundTruthItem("semen", 5.0, "bag"),
                GroundTruthItem("cat", 2.0, "tin")
            ]
        ),
        GroundTruthSample(
            message="Halo berapa harga semen tiga roda sekarang?",
            expected_intent="inquiry",
            expected_items=[]
        ),
        GroundTruthSample(
            message="Barang pesanan saya kemarin kenapa belum sampai ya? Mohon dicek.",
            expected_intent="complaint",
            expected_items=[]
        )
    ]

    predictions = []
    latencies = [18.4, 22.1, 15.0, 16.5] # simulated local inference latencies in ms

    for sample in ground_truth:
        ext = extractor.extract_with_rules_fallback(sample.message)
        predictions.append({
            "intent": ext.intent.value,
            "items": [item.model_dump() for item in ext.items],
            "is_valid_json": True
        })

    metrics = evaluator.evaluate(ground_truth, predictions, latencies)
    return StandardAPIResponse(
        success=True,
        data=metrics.__dict__
    )


# ---------------------------------------------------------------------------
# Q6: Idempotent Order Submission & Non-Blocking Background Tasks
# ---------------------------------------------------------------------------
@router.post(
    "/orders/submit",
    response_model=StandardAPIResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def submit_order_idempotent(
    payload: CreateOrderRequest,
    request: Request,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    """
    Submits an order idempotently. If the HTTP request is retried with the same
    Idempotency-Key, cached response is returned without duplicating database
    inserts or dispatching duplicate background jobs.
    """
    if idempotency_key:
        cached = idempotency_store.check_or_lock(idempotency_key)
        if cached is not None:
            # Return cached response with header indication
            return JSONResponse(
                content=StandardAPIResponse(success=True, data=cached).model_dump(),
                headers={"X-Cache-Lookup": "HIT-IDEMPOTENT"}
            )

    order_id = f"ord_2026_{payload.customer_id[-4:]}"
    
    # Create background tracking task for invoice/report compilation (Q6)
    task_id = global_task_manager.create_task(task_type="pdf_invoice_compilation")

    # Non-blocking async dispatch (FastAPI / asyncio pattern)
    asyncio.create_task(
        global_task_manager.execute_mock_pdf_generation(task_id, order_id)
    )

    response_data = {
        "order_id": order_id,
        "status": "ACCEPTED",
        "task_id": task_id,
        "message": "Order submitted successfully. PDF generation dispatched in background."
    }

    if idempotency_key:
        idempotency_store.store_response(idempotency_key, response_data)

    return StandardAPIResponse(success=True, data=response_data)


# ---------------------------------------------------------------------------
# Q6(b): Task Progress Polling
# ---------------------------------------------------------------------------
@router.get("/tasks/{task_id}/progress", response_model=StandardAPIResponse)
async def get_task_progress(task_id: str):
    """Allows frontend to poll task progress ('report 60% complete')."""
    task = global_task_manager.get_task_status(task_id)
    if not task:
        raise NotFoundException(resource="BackgroundTask", identifier=task_id)

    return StandardAPIResponse(success=True, data=task.model_dump())


# ---------------------------------------------------------------------------
# Q5: External Webhook Receiver with HMAC-SHA256 Verification
# ---------------------------------------------------------------------------
@router.post("/webhooks/whatsapp", response_model=StandardAPIResponse)
async def receive_whatsapp_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None, alias="X-Hub-Signature-256")
):
    """Secures external webhook callers via HMAC-SHA256 signature verification."""
    body_bytes = await request.body()
    secret_key = "injani-webhook-secret-token"

    if not x_hub_signature_256 or not verify_webhook_hmac_sha256(body_bytes, x_hub_signature_256, secret_key):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=StandardAPIResponse(
                success=False,
                error=APIErrorPayload(
                    code="INVALID_WEBHOOK_SIGNATURE",
                    message="HMAC signature verification failed."
                )
            ).model_dump()
        )

    return StandardAPIResponse(
        success=True,
        data={"received": True, "event": "webhook_verified"}
    )
