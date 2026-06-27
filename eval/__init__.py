"""L6 Eval Harness — DeepEval-based regression gate.

Greenfield implementation using only open-source DeepEval framework.

Principles (see ARCHITECTURE.md + PATTERN_REGISTRY.md "Harness Engineering"):
- Golden dataset from real traces (start synthetic, grow from production)
- Rubric binary pass/fail (DeepEval metrics with threshold)
- Delta-vs-baseline regression guard
- CI gate blocking merge

Submodules:
- golden: GoldenSample model + JSONL loader
- metrics: default metric suite factories
- runner: regression guard (current vs baseline)
"""

from __future__ import annotations

from eval.golden import GoldenSample, load_golden, to_test_case
from eval.metrics import default_metrics
from eval.runner import EvalConfig, check_regression, load_baseline

__all__ = [
    "GoldenSample",
    "load_golden",
    "to_test_case",
    "default_metrics",
    "EvalConfig",
    "check_regression",
    "load_baseline",
]

__version__ = "0.1.0"
