"""
PT Injani Systems - Fullstack Developer Prescreening
Q5: Standardized, Typed Error Handling Architecture (RFC 7807 & API Envelopes)
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ErrorDetailItem(BaseModel):
    field: Optional[str] = Field(None, description="Field path that triggered the validation error")
    message: str = Field(..., description="Specific failure reason")
    code: Optional[str] = Field(None, description="Granular error code, e.g. INVALID_QUANTITY")


class APIErrorPayload(BaseModel):
    code: str = Field(..., description="High level domain error code, e.g. VALIDATION_ERROR, NOT_FOUND")
    message: str = Field(..., description="Human readable error explanation")
    details: Optional[List[ErrorDetailItem]] = Field(default=None)
    trace_id: Optional[str] = Field(default=None, description="Unique correlation ID for log tracing")


class StandardAPIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[APIErrorPayload] = None


class RFC7807ProblemDetails(BaseModel):
    """
    IETF RFC 7807 standard for HTTP API Problem Details.
    Recommended for public REST APIs and external webhook callers.
    """
    type: str = Field("about:blank", description="URI reference identifying the problem type")
    title: str = Field(..., description="Short, human-readable summary of the problem")
    status: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Human-readable explanation specific to this occurrence")
    instance: Optional[str] = Field(None, description="URI reference identifying the specific occurrence")
    invalid_params: Optional[List[ErrorDetailItem]] = None


class DomainException(Exception):
    """Base application exception with status code and error code mapping."""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[List[ErrorDetailItem]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []


class NotFoundException(DomainException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} with id '{identifier}' was not found.",
            code="RESOURCE_NOT_FOUND",
            status_code=404
        )


class ConflictException(DomainException):
    def __init__(self, message: str, code: str = "RESOURCE_CONFLICT"):
        super().__init__(message=message, code=code, status_code=409)


class RateLimitExceededException(DomainException):
    def __init__(self, retry_after_seconds: int = 60):
        super().__init__(
            message=f"Rate limit exceeded. Please retry in {retry_after_seconds} seconds.",
            code="RATE_LIMIT_EXCEEDED",
            status_code=429
        )
        self.retry_after_seconds = retry_after_seconds
