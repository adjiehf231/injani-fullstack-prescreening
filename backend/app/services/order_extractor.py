"""
PT Injani Systems - Fullstack Developer Prescreening
Q1: AI-Powered WhatsApp Order Processing (Ollama / Gemma 3 Prompting & Extraction Engine)
"""

import json
import re
from typing import Optional, Dict, Any
from app.schemas.order import (
    CustomerIntent,
    OrderItem,
    ExtractionResult,
    WhatsAppIncomingMessage
)

SYSTEM_PROMPT_GEMMA = """You are an automated WhatsApp order parser for PT Injani Systems building materials and goods distribution.
Your task is to extract structured order details from customer chat messages.

You must classify the customer's intent into exactly one of:
- "order": The customer intends to purchase, order, or request delivery of goods.
- "inquiry": The customer is asking about prices, stock, specifications, delivery time, or store location.
- "complaint": The customer is reporting an issue, defective items, late delivery, or billing error.
- "other": Casual greetings, spam, or unrelated remarks.

For orders, extract every distinct item requested:
- item_name: Name of the product (e.g. "cement", "paint", "bata merah", "besi 10mm").
- quantity: Numeric value (float or integer).
- unit: Standardized unit (e.g. "bag", "tin", "kg", "pcs", "meter", "box").
- specifications: Color, brand, grade, or dimensions if stated.

Output ONLY valid JSON matching this schema:
{
  "intent": "order" | "inquiry" | "complaint" | "other",
  "items": [
    {
      "item_name": "string",
      "quantity": 0.0,
      "unit": "string | null",
      "specifications": "string | null"
    }
  ],
  "confidence": 0.0 to 1.0,
  "requires_clarification": boolean,
  "clarification_prompt": "string | null",
  "natural_reply": "Polite and helpful auto-reply to the customer in the same language as their message"
}
"""

FEW_SHOT_EXAMPLES = [
    {
        "user": "I'd like 3 bags of cement and 2 tins of paint please",
        "assistant": {
            "intent": "order",
            "items": [
                {"item_name": "cement", "quantity": 3.0, "unit": "bag", "specifications": None},
                {"item_name": "paint", "quantity": 2.0, "unit": "tin", "specifications": None}
            ],
            "confidence": 0.98,
            "requires_clarification": False,
            "clarification_prompt": None,
            "natural_reply": "Thank you! We have received your order for 3 bags of cement and 2 tins of paint. Could you please provide your delivery address?"
        }
    },
    {
        "user": "Halo mas, semen tiga roda sak 50kg harganya berapa ya per sak? Ada promo ga?",
        "assistant": {
            "intent": "inquiry",
            "items": [
                {"item_name": "semen tiga roda", "quantity": 1.0, "unit": "bag", "specifications": "50kg"}
            ],
            "confidence": 0.95,
            "requires_clarification": False,
            "clarification_prompt": None,
            "natural_reply": "Halo! Saya akan meneruskan permintaan Anda untuk memeriksa harga resmi dan ketersediaan stok Semen Tiga Roda 50kg ke katalog kami. Ada hal lain yang bisa kami bantu?"
        }
    },
    {
        "user": "Barang pesanan saya kemarin kenapa belum sampai ya? Padahal janjinya pagi ini.",
        "assistant": {
            "intent": "complaint",
            "items": [],
            "confidence": 0.96,
            "requires_clarification": False,
            "clarification_prompt": None,
            "natural_reply": "Mohon maaf atas keterlambatannya. Boleh kami minta nomor pesanan atau nama penerima agar tim logistik kami langsung mengecek posisi armada pengiriman?"
        }
    }
]


def build_gemma_prompt(message_text: str) -> str:
    """Formats prompt with Gemma 3 instruction tags (<start_of_turn>...<end_of_turn>)."""
    prompt = f"<start_of_turn>system\n{SYSTEM_PROMPT_GEMMA}\n\nHere are few-shot reference examples:\n"
    for ex in FEW_SHOT_EXAMPLES:
        prompt += f"\nCustomer: {ex['user']}\nJSON Output:\n{json.dumps(ex['assistant'], indent=2)}\n"
    prompt += f"<end_of_turn>\n<start_of_turn>user\nParse this message: \"{message_text}\"<end_of_turn>\n<start_of_turn>model\n"
    return prompt


class WhatsAppOrderExtractor:
    """
    Handles local model inference (via Ollama REST API or rule-based deterministic fallback for testing).
    Enforces Pydantic validation on the JSON output.
    """

    def __init__(self, ollama_url: str = "http://localhost:11434", model_name: str = "gemma3:4b"):
        self.ollama_url = ollama_url
        self.model_name = model_name

    def parse_llm_json_response(self, raw_response: str) -> Dict[str, Any]:
        """Extracts JSON even if model outputs markdown fences or conversational preamble."""
        clean_text = raw_response.strip()
        
        # Remove ```json ... ``` code blocks if present
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean_text, re.DOTALL)
        if json_match:
            clean_text = json_match.group(1)
        else:
            # Match outermost curly braces
            braces_match = re.search(r"(\{.*\})", clean_text, re.DOTALL)
            if braces_match:
                clean_text = braces_match.group(1)

        return json.loads(clean_text)

    def extract_with_rules_fallback(self, message: str) -> ExtractionResult:
        """
        Deterministic parser used when Ollama daemon is offline (e.g. unit tests or edge fallback).
        Ensures the pipeline is robust and testable without requiring a live GPU server.
        """
        msg_lower = message.lower()

        # Intent detection
        if any(w in msg_lower for w in ["komplain", "belum sampai", "rusak", "pecah", "kecewa", "salah kirim"]):
            return ExtractionResult(
                intent=CustomerIntent.COMPLAINT,
                items=[],
                confidence=0.92,
                requires_clarification=False,
                natural_reply="Mohon maaf atas kendala yang dialami. Mohon informasikan nomor faktur atau invoice Anda agar dapat segera kami tindaklanjuti."
            )

        if any(w in msg_lower for w in ["berapa", "harga", "ready", "stock", "stok", "apakah ada", "bisa tanya"]):
            return ExtractionResult(
                intent=CustomerIntent.INQUIRY,
                items=[],
                confidence=0.88,
                requires_clarification=False,
                natural_reply="Terima kasih telah menghubungi kami. Untuk informasi harga dan ketersediaan stok material, silakan sebutkan jenis dan perkiraan jumlah yang dibutuhkan."
            )

        # Order extraction with regex for quantity, unit, and item
        # e.g.: "3 bags of cement and 2 tins of paint" or "3 sak semen dan 2 kaleng cat"
        patterns = [
            r"(\d+(?:\.\d+)?)\s*(bags?|tins?|sak|zak|kaleng|pail|kg|pcs|lembar|meter|dus|box)?\s*(?:of|)\s*([a-zA-Z\s]+?)(?=\s*(?:and|dan|,|$))",
        ]
        
        items: list[OrderItem] = []
        for pat in patterns:
            matches = re.finditer(pat, msg_lower)
            for m in matches:
                qty_str, unit_str, name_str = m.groups()
                name_clean = name_str.replace("please", "").replace("tolong", "").replace("ya", "").strip()
                if name_clean and not name_clean.startswith("halo"):
                    items.append(
                        OrderItem(
                            item_name=name_clean,
                            quantity=float(qty_str),
                            unit=unit_str if unit_str else "pcs"
                        )
                    )

        if items:
            item_desc = ", ".join(f"{it.quantity:g} {it.unit} {it.item_name}" for it in items)
            return ExtractionResult(
                intent=CustomerIntent.ORDER,
                items=items,
                confidence=0.95,
                requires_clarification=False,
                natural_reply=f"Terima kasih, pesanan Anda untuk {item_desc} telah kami catat. Mohon kirimkan alamat lengkap pengiriman untuk estimasi ongkos kirim."
            )

        return ExtractionResult(
            intent=CustomerIntent.OTHER,
            items=[],
            confidence=0.70,
            requires_clarification=True,
            clarification_prompt="Boleh dijelaskan material atau barang apa yang ingin Anda pesan?",
            natural_reply="Halo! Selamat datang di layanan kami. Apakah ada material atau barang yang ingin Anda pesan hari ini?"
        )
