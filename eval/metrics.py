"""Default metric suite for L6 Eval Harness.

Uses DeepEval's built-in metrics + G-Eval for custom criteria.
All metrics are LLM-as-judge (DeepEval supports cross-family judge via env config).

Principles:
- Generator != judge (avoid self-affirming eval)
- Binary pass/fail via threshold
- Cross-family judge (set DEEPEVAL_MODEL to a different family than the generator)
"""

from __future__ import annotations

from typing import Any

from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval,
)
from deepeval.test_case import LLMTestCaseParams


def default_metrics(threshold: float = 0.7) -> list[Any]:
    """Return default metric suite for L6 skeleton.

    Suite:
    - FaithfulnessMetric: is the answer grounded in retrieval_context? (RAG core)
    - AnswerRelevancyMetric: does the answer address the input?
    - GEval "conciseness": custom criterion — answer is concise, no fluff

    Returns DeepEval metric instances. Each metric has `.score` (0-1) and `.is_successful()`
    after being measured against a test case.
    """
    return [
        FaithfulnessMetric(threshold=threshold),
        AnswerRelevancyMetric(threshold=threshold),
        GEval(
            name="conciseness",
            criteria=(
                "Determine whether the actual output is concise, direct, "
                "and free of unnecessary filler or repetition."
            ),
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=threshold,
        ),
    ]


def metric_names() -> list[str]:
    """Return the canonical metric names used in baseline.json for regression tracking."""
    return ["faithfulness", "answer_relevancy", "conciseness"]
