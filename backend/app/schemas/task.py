"""
PT Injani Systems - Fullstack Developer Prescreening
Q6: Background Task Status & Progress Reporting Schemas
"""

from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskProgressResponse(BaseModel):
    task_id: str = Field(..., description="Unique UUID of the background task")
    status: TaskStatus = Field(..., description="Current execution status")
    progress_percent: int = Field(..., ge=0, le=100, description="Completion percentage (0 to 100)")
    current_step: str = Field(..., description="Human-readable description of current step")
    result: Optional[Dict[str, Any]] = Field(None, description="Task output if COMPLETED")
    error: Optional[str] = Field(None, description="Error detail if FAILED")
    created_at: str
    updated_at: str


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    items: list[dict] = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=5)
