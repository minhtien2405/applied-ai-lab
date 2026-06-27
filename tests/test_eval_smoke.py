"""Smoke tests for L6 Eval Harness.

These tests do NOT call any LLM judge — they validate the harness plumbing:
- Golden samples load correctly
- GoldenSample schema is respected
- to_test_case conversion works
- Regression guard logic (check_regression) is correct
- Baseline loads/parses

Run with: `make test-smoke` (no API key needed).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval.golden import GoldenSample, load_golden, to_test_case
from eval.runner import EvalConfig, check_regression, load_baseline
from eval.metrics import default_metrics, metric_names


def test_golden_loads() -> None:
    """All 10 sample golden samples load and parse."""
    samples = load_golden()
    assert len(samples) == 10, f"Expected 10 samples, got {len(samples)}"
    for s in samples:
        assert s.id.startswith("q-")
        assert s.input
        assert s.expected_output
        assert s.retrieval_context  # all current samples have retrieval context


def test_golden_schema() -> None:
    """GoldenSample validates required fields."""
    sample = GoldenSample(
        id="test-1",
        input="test input",
        expected_output="test output",
    )
    assert sample.retrieval_context == []
    assert sample.context == []

    with pytest.raises(Exception):
        GoldenSample(id="test-2", input="missing expected")  # type: ignore[call-arg]


def test_to_test_case() -> None:
    """GoldenSample converts to DeepEval LLMTestCase."""
    sample = GoldenSample(
        id="test-conv",
        input="What is X?",
        expected_output="X is Y.",
        retrieval_context=["X is defined as Y."],
    )
    tc = to_test_case(sample)
    assert tc.input == "What is X?"
    assert tc.expected_output == "X is Y."
    # In Tier 1 skeleton, actual_output == expected_output (placeholder)
    assert tc.actual_output == "X is Y."
    assert tc.retrieval_context == ["X is defined as Y."]


def test_default_metrics_factory() -> None:
    """default_metrics returns 3 DeepEval metric instances."""
    metrics = default_metrics(threshold=0.8)
    assert len(metrics) == 3
    names = metric_names()
    assert names == ["faithfulness", "answer_relevancy", "conciseness"]


def test_baseline_loads() -> None:
    """baseline.json parses and has expected metric keys."""
    baseline = load_baseline()
    assert isinstance(baseline, dict)
    # baseline.json should have at least the 3 default metric names
    for name in metric_names():
        assert name in baseline, f"Missing {name} in baseline.json"
        assert 0.0 <= baseline[name] <= 1.0, f"{name} score out of [0,1] range"


def test_check_regression_pass() -> None:
    """Regression guard passes when current >= baseline - tolerance."""
    baseline = {"faithfulness": 0.80, "answer_relevancy": 0.85}
    current = {"faithfulness": 0.82, "answer_relevancy": 0.83}
    # delta faithfulness: +0.02 (ok), answer_relevancy: -0.02 (within 0.05 tolerance)
    passed, reasons = check_regression(current, baseline, tolerance=0.05)
    assert passed is True
    assert len(reasons) == 2


def test_check_regression_fail() -> None:
    """Regression guard fails when current < baseline - tolerance."""
    baseline = {"faithfulness": 0.80}
    current = {"faithfulness": 0.70}  # delta -0.10 > tolerance 0.05
    passed, reasons = check_regression(current, baseline, tolerance=0.05)
    assert passed is False
    assert any("REGRESSED" in r for r in reasons)


def test_check_regression_missing_metric() -> None:
    """Regression guard fails when a baseline metric is missing in current."""
    baseline = {"faithfulness": 0.80, "answer_relevancy": 0.85}
    current = {"faithfulness": 0.82}  # answer_relevancy missing
    passed, reasons = check_regression(current, baseline, tolerance=0.05)
    assert passed is False
    assert any("MISSING" in r for r in reasons)


def test_check_regression_empty_baseline() -> None:
    """Empty baseline = first run, no regression to check."""
    passed, reasons = check_regression({"faithfulness": 0.5}, baseline={}, tolerance=0.05)
    assert passed is True
    assert any("no baseline" in r for r in reasons)


def test_eval_config_defaults() -> None:
    """EvalConfig has sensible defaults."""
    cfg = EvalConfig()
    assert cfg.threshold == 0.7
    assert cfg.baseline_delta_tolerance == 0.05


def test_golden_file_format() -> None:
    """sample_golden.jsonl is valid JSONL (one JSON object per line)."""
    golden_path = Path(__file__).parent.parent / "eval" / "golden" / "sample_golden.jsonl"
    assert golden_path.exists(), f"Golden file missing: {golden_path}"
    with golden_path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            # Each non-blank line must be valid JSON
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON at line {line_num}: {e}")
