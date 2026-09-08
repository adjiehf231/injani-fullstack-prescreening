"""
PT Injani Systems - Fullstack Developer Prescreening
Q1: WhatsApp Order Intent & Entity Extraction Schemas
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class CustomerIntent(str, Enum):
    ORDER = "order"
    INQUIRY = "inquiry"
    COMPLAINT = "complaint"
    OTHER = "other"


class OrderItem(BaseModel):
    item_name: str = Field(..., description="Canonical or extracted name of the item requested", min_length=1)
    quantity: float = Field(..., description="Numeric quantity requested", gt=0)
    unit: Optional[str] = Field(None, description="Standardized unit of measurement, e.g. bag, tin, kg, pcs")
    specifications: Optional[str] = Field(None, description="Color, brand, size, or quality specifications")

    @field_validator("unit")
    @classmethod
    def normalize_unit(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        v_clean = v.strip().lower()
        # Normalization mapping for common Indonesian & English construction trade units
        mapping = {
            "sak": "bag",
            "zak": "bag",
            "kantong": "bag",
            "bag": "bag",
            "bags": "bag",
            "tin": "tin",
            "tins": "tin",
            "kaleng": "tin",
            "pail": "pail",
            "kg": "kg",
            "kilo": "kg",
            "meter": "meter",
            "m": "meter",
            "pcs": "pcs",
            "buah": "pcs",
            "lembar": "sheet",
            "batang": "bar",
            "dus": "box",
            "box": "box",
        }
        return mapping.get(v_clean, v_clean)


class ExtractionResult(BaseModel):
    intent: CustomerIntent = Field(..., description="Primary classification of the user message")
    items: List[OrderItem] = Field(default_factory=list, description="Extracted list of order items")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the extraction between 0 and 1")
    requires_clarification: bool = Field(False, description="True if ambiguity exists in item, quantity, or unit")
    clarification_prompt: Optional[str] = Field(None, description="Clarification question to ask if ambiguous")
    natural_reply: str = Field(..., description="Professional, polite response to send back to the WhatsApp customer")


class WhatsAppIncomingMessage(BaseModel):
    sender_phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    customer_name: Optional[str] = None
    message_text: str = Field(..., min_length=1)
    timestamp: str
