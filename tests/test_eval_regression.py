"""DeepEval regression tests for L6 Eval Harness.

These tests RUN the full eval suite (LLM judge calls) — require OPENAI_API_KEY or
DEEPEVAL_MODEL endpoint. Skip in CI without secrets (smoke job covers that).

Run with: `make eval` (requires API key).
Marker: `@pytest.mark.eval` — selected by `make eval` (pytest -m eval).
"""

from __future__ import annotations

import os

import pytest
from deepeval import assert_test

from eval.golden import load_golden, to_test_case
from eval.metrics import default_metrics
from eval.runner import EvalConfig, check_regression, load_baseline

pytestmark = pytest.mark.eval
cfg = EvalConfig()


def _requires_llm_endpoint() -> None:
    """Skip all eval tests if no LLM endpoint configured."""
    if not (os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")):
        pytest.skip("No LLM endpoint configured (set OPENAI_API_KEY or ANTHROPIC_API_KEY)")


def test_golden_regression_suite() -> None:
    """Run default metric suite on all golden samples; aggregate and check regression.

    This is THE eval gate. If it fails in CI, the PR regressed eval scores.
    """
    _requires_llm_endpoint()

    samples = load_golden()
    metrics = default_metrics(threshold=cfg.threshold)
    per_metric_scores: dict[str, list[float]] = {name: [] for name in
                                                  ["faithfulness", "answer_relevancy", "conciseness"]}

    for sample in samples:
        test_case = to_test_case(sample)
        # DeepEval runs each metric on the test case
        for metric in metrics:
            metric.measure(test_case)
            # Map metric instance to canonical name
            metric_name = (
                "faithfulness" if "faithfulness" in metric.__class__.__name__.lower()
                else "answer_relevancy" if "relevancy" in metric.__class__.__name__.lower()
                else metric.name if hasattr(metric, "name") else "unknown"
            )
            if metric_name in per_metric_scores:
                per_metric_scores[metric_name].append(metric.score)
            # Per-sample assertion (binary pass/fail per metric)
            assert metric.is_successful(), (
                f"Sample {sample.id} failed {metric_name}: "
                f"score={metric.score:.3f} < threshold={cfg.threshold} "
                f"(reason: {getattr(metric, 'reason', 'n/a')})"
            )

    # Aggregate: mean score per metric
    current_scores = {
        name: sum(scores) / len(scores)
        for name, scores in per_metric_scores.items()
        if scores
    }

    # Regression guard: compare vs baseline
    baseline = load_baseline()
    passed, reasons = check_regression(
        current_scores, baseline, tolerance=cfg.baseline_delta_tolerance
    )
    print("\n=== Eval regression report ===")
    print(f"Current scores: {current_scores}")
    print(f"Baseline:       {baseline}")
    for r in reasons:
        print(r)
    assert passed, "Eval regression detected — see report above"
