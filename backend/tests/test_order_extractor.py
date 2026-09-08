"""
Unit tests for WhatsApp Order Extractor and Evaluation Methodology (Q1)
"""

import pytest
from app.schemas.order import CustomerIntent
from app.services.order_extractor import WhatsAppOrderExtractor, build_gemma_prompt
from app.services.evaluator import (
    LLMExtractionEvaluator,
    GroundTruthSample,
    GroundTruthItem
)


@pytest.fixture
def extractor():
    return WhatsAppOrderExtractor()


@pytest.fixture
def evaluator():
    return LLMExtractionEvaluator()


def test_order_intent_and_entity_extraction(extractor):
    msg = "I'd like 3 bags of cement and 2 tins of paint please"
    result = extractor.extract_with_rules_fallback(msg)

    assert result.intent == CustomerIntent.ORDER
    assert len(result.items) == 2

    cement = next((i for i in result.items if "cement" in i.item_name), None)
    assert cement is not None
    assert cement.quantity == 3.0
    assert cement.unit == "bag"

    paint = next((i for i in result.items if "paint" in i.item_name), None)
    assert paint is not None
    assert paint.quantity == 2.0
    assert paint.unit == "tin"
    assert "Thank you" in result.natural_reply or "Terima kasih" in result.natural_reply


def test_indonesian_unit_normalization(extractor):
    msg = "Tolong kirim 5 sak semen dan 2 kaleng cat ya"
    result = extractor.extract_with_rules_fallback(msg)

    assert result.intent == CustomerIntent.ORDER
    assert len(result.items) == 2

    # Verify unit normalization: sak -> bag, kaleng -> tin
    semen = next(i for i in result.items if "semen" in i.item_name)
    assert semen.quantity == 5.0
    assert semen.unit == "bag"

    cat = next(i for i in result.items if "cat" in i.item_name)
    assert cat.quantity == 2.0
    assert cat.unit == "tin"


def test_inquiry_intent_detection(extractor):
    msg = "Halo pak, berapa harga semen tiga roda 50kg hari ini?"
    result = extractor.extract_with_rules_fallback(msg)

    assert result.intent == CustomerIntent.INQUIRY
    assert len(result.items) == 0


def test_complaint_intent_detection(extractor):
    msg = "Barang pesanan saya kemarin kenapa belum sampai? Sudah ditunggu dari pagi."
    result = extractor.extract_with_rules_fallback(msg)

    assert result.intent == CustomerIntent.COMPLAINT
    assert result.requires_clarification is False


def test_prompt_builder_structure():
    prompt = build_gemma_prompt("I want 10 boxes of tiles")
    assert "<start_of_turn>system" in prompt
    assert "<start_of_turn>user" in prompt
    assert "<start_of_turn>model" in prompt
    assert "order" in prompt


def test_evaluator_metrics_calculation(evaluator):
    samples = [
        GroundTruthSample(
            message="3 bags of cement and 2 tins of paint",
            expected_intent="order",
            expected_items=[
                GroundTruthItem("cement", 3.0, "bag"),
                GroundTruthItem("paint", 2.0, "tin")
            ]
        ),
        GroundTruthSample(
            message="Berapa harga semen?",
            expected_intent="inquiry",
            expected_items=[]
        )
    ]

    predictions = [
        {
            "intent": "order",
            "items": [
                {"item_name": "cement", "quantity": 3.0, "unit": "bag"},
                {"item_name": "paint", "quantity": 2.0, "unit": "tin"}
            ],
            "is_valid_json": True
        },
        {
            "intent": "inquiry",
            "items": [],
            "is_valid_json": True
        }
    ]

    latencies = [15.2, 10.4]
    metrics = evaluator.evaluate(samples, predictions, latencies)

    assert metrics.total_samples == 2
    assert metrics.intent_accuracy_pct == 100.0
    assert metrics.exact_match_rate_pct == 100.0
    assert metrics.entity_precision == 1.0
    assert metrics.entity_recall == 1.0
    assert metrics.entity_f1 == 1.0
    assert metrics.avg_latency_ms == 12.8
