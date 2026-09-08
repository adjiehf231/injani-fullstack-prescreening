"""
PT Injani Systems - Fullstack Developer Prescreening
FastAPI Application Entry Point with Centralized Error Handling
"""

import uuid
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.errors import (
    DomainException,
    StandardAPIResponse,
    APIErrorPayload,
    ErrorDetailItem
)
from app.api.routes import router as api_router

app = FastAPI(
    title="Injani Systems - Fullstack Backend Service",
    description="Python FastAPI service handling order extraction, background tasks, and webhook verification",
    version="1.0.0"
)

# CORS configuration for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Centralized Exception Handler: Domain Exceptions
@app.exception_handler(DomainException)
async def handle_domain_exception(request: Request, exc: DomainException):
    correlation_id = str(uuid.uuid4())
    error_payload = APIErrorPayload(
        code=exc.code,
        message=exc.message,
        details=exc.details if exc.details else None,
        trace_id=correlation_id
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardAPIResponse(success=False, error=error_payload).model_dump()
    )


# Centralized Exception Handler: Pydantic / FastAPI Validation Errors (422)
@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    correlation_id = str(uuid.uuid4())
    details = []
    for err in exc.errors():
        field_path = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        details.append(
            ErrorDetailItem(
                field=field_path or "root",
                message=err["msg"],
                code=err.get("type", "VALIDATION_FAILED")
            )
        )

    error_payload = APIErrorPayload(
        code="VALIDATION_ERROR",
        message="The request payload failed structural validation.",
        details=details,
        trace_id=correlation_id
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StandardAPIResponse(success=False, error=error_payload).model_dump()
    )


# Centralized Exception Handler: Unhandled Server Errors (500)
# Prevents leaking database stack traces to clients (OWASP Top 10 Security Standard)
@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception):
    correlation_id = str(uuid.uuid4())
    # In production: logger.exception(f"Unhandled error [trace_id={correlation_id}]: {str(exc)}")
    error_payload = APIErrorPayload(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred. Please quote the trace ID to technical support.",
        trace_id=correlation_id
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=StandardAPIResponse(success=False, error=error_payload).model_dump()
    )


# Health check endpoint for Cloud Run and Kubernetes probes
@app.get("/healthz", tags=["System"])
async def health_check():
    return {"status": "HEALTHY", "service": "injani-backend"}


# Mount API Router
app.include_router(api_router)
