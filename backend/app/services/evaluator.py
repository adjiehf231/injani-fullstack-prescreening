"""
PT Injani Systems - Fullstack Developer Prescreening
Q1(c): Evaluation Methodology & Metrics Harness for LLM Entity Extraction
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class GroundTruthItem:
    item_name: str
    quantity: float
    unit: str


@dataclass
class GroundTruthSample:
    message: str
    expected_intent: str
    expected_items: List[GroundTruthItem]


@dataclass
class EvaluationMetricsResult:
    total_samples: int
    intent_accuracy_pct: float
    json_validity_rate_pct: float
    entity_precision: float
    entity_recall: float
    entity_f1: float
    exact_match_rate_pct: float
    avg_latency_ms: float
    p95_latency_ms: float


class LLMExtractionEvaluator:
    """
    Computes rigorous classification and information extraction metrics:
    - Intent Accuracy: Correct Intent / Total Samples
    - Entity Extraction (Precision, Recall, F1): Token/Slot matching for item_name, quantity, and unit
    - Exact Match (EM): All entities and intent match ground truth 100%
    - JSON Validity Rate: Syntactic compliance of LLM output
    """

    def _match_item(self, pred: Dict[str, Any], truth: GroundTruthItem) -> bool:
        # Match item name (substring/exact), quantity float equality, and normalized unit
        pred_name = str(pred.get("item_name", "")).strip().lower()
        truth_name = truth.item_name.strip().lower()
        name_match = (pred_name in truth_name) or (truth_name in pred_name)
        qty_match = abs(float(pred.get("quantity", 0)) - truth.quantity) < 1e-4
        
        pred_unit = str(pred.get("unit", "")).strip().lower()
        truth_unit = truth.unit.strip().lower()
        unit_match = pred_unit == truth_unit

        return name_match and qty_match and unit_match

    def evaluate(
        self,
        samples: List[GroundTruthSample],
        predictions: List[Dict[str, Any]],
        latencies_ms: List[float]
    ) -> EvaluationMetricsResult:
        if not samples:
            raise ValueError("Evaluation requires at least one ground truth sample.")

        total = len(samples)
        correct_intent = 0
        exact_matches = 0
        valid_json_count = 0

        total_true_positives = 0
        total_predicted_entities = 0
        total_ground_truth_entities = 0

        for sample, pred in zip(samples, predictions):
            if pred.get("is_valid_json", True):
                valid_json_count += 1

            # 1. Intent Accuracy
            pred_intent = str(pred.get("intent", "")).lower()
            if pred_intent == sample.expected_intent.lower():
                correct_intent += 1

            # 2. Entity Level Evaluation
            pred_items = pred.get("items", [])
            total_predicted_entities += len(pred_items)
            total_ground_truth_entities += len(sample.expected_items)

            matched_ground_truth = set()
            sample_tp = 0

            for p_item in pred_items:
                for idx, gt_item in enumerate(sample.expected_items):
                    if idx not in matched_ground_truth and self._match_item(p_item, gt_item):
                        matched_ground_truth.add(idx)
                        sample_tp += 1
                        break
            
            total_true_positives += sample_tp

            # 3. Exact Match Rate (EM)
            if (pred_intent == sample.expected_intent.lower() 
                and sample_tp == len(sample.expected_items) 
                and len(pred_items) == len(sample.expected_items)):
                exact_matches += 1

        # Calculate Precision, Recall, F1
        precision = (total_true_positives / total_predicted_entities) if total_predicted_entities > 0 else 0.0
        recall = (total_true_positives / total_ground_truth_entities) if total_ground_truth_entities > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        # Latency statistics
        sorted_latencies = sorted(latencies_ms) if latencies_ms else [0.0]
        avg_lat = sum(sorted_latencies) / len(sorted_latencies)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p95_lat = sorted_latencies[min(p95_idx, len(sorted_latencies) - 1)]

        return EvaluationMetricsResult(
            total_samples=total,
            intent_accuracy_pct=round((correct_intent / total) * 100, 2),
            json_validity_rate_pct=round((valid_json_count / total) * 100, 2),
            entity_precision=round(precision, 4),
            entity_recall=round(recall, 4),
            entity_f1=round(f1, 4),
            exact_match_rate_pct=round((exact_matches / total) * 100, 2),
            avg_latency_ms=round(avg_lat, 2),
            p95_latency_ms=round(p95_lat, 2),
        )
