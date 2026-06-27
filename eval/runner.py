"""Regression guard — compare current eval scores vs baseline.

Principles:
- Delta-vs-baseline, NOT static threshold (chống flakiness from LLM judge variance)
- Tolerance knob (5% default — tighten for regulated paths, widen for exploratory)
- Block merge when regression > tolerance

baseline.json format:
    {"faithfulness": 0.8, "answer_relevancy": 0.85, "conciseness": 0.75}
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

BASELINE_PATH = Path(__file__).parent / "baseline.json"


@dataclass(frozen=True)
class EvalConfig:
    """Eval run configuration.

    Attributes:
        threshold: minimum score per metric to pass (binary pass/fail per metric)
        baseline_delta_tolerance: max regression vs baseline (0.05 = 5%)
    """

    threshold: float = 0.7
    baseline_delta_tolerance: float = 0.05


def load_baseline() -> dict[str, float]:
    """Load regression baseline scores from baseline.json.

    Returns empty dict if baseline file doesn't exist (first run — no baseline yet).
    """
    if not BASELINE_PATH.exists():
        return {}
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def save_baseline(scores: dict[str, float]) -> None:
    """Save current scores as new baseline (run this after confirming a good run).

    Use: `python -m eval.runner --update-baseline` (future) or manual edit.
    """
    BASELINE_PATH.write_text(
        json.dumps(scores, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def check_regression(
    current_scores: dict[str, float],
    baseline: dict[str, float],
    tolerance: float = 0.05,
) -> tuple[bool, list[str]]:
    """Regression guard: return (passed, reasons) comparing current vs baseline.

    A metric regresses if `current < baseline - tolerance`.
    Metrics not in baseline are skipped (new metric — no regression to check).
    Metrics in baseline but missing in current are flagged as failures.
    """
    reasons: list[str] = []
    passed = True
    for metric_name, baseline_score in baseline.items():
        current_score = current_scores.get(metric_name)
        if current_score is None:
            reasons.append(f"  {metric_name}: MISSING in current run (was in baseline)")
            passed = False
            continue
        delta = current_score - baseline_score
        if delta < -tolerance:
            reasons.append(
                f"  {metric_name}: REGRESSED {delta:+.3f} "
                f"(current={current_score:.3f}, baseline={baseline_score:.3f}, "
                f"tolerance={tolerance:.3f})"
            )
            passed = False
        else:
            reasons.append(
                f"  {metric_name}: ok {delta:+.3f} "
                f"(current={current_score:.3f}, baseline={baseline_score:.3f})"
            )
    if not baseline:
        reasons.append("  (no baseline yet — first run, all metrics pass if above threshold)")
    return passed, reasons
