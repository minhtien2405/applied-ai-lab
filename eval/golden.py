"""Golden dataset model + loader.

Golden samples are curated input/expected_output pairs used for regression testing.
Start with synthetic samples; grow from production traces as the Lab matures.

Schema (JSONL, one sample per line):
    {"id": "...", "input": "...", "expected_output": "...",
     "retrieval_context": ["...", ...], "context": ["...", ...]}
"""

from __future__ import annotations

import json
from pathlib import Path

from deepeval.test_case import LLMTestCase
from pydantic import BaseModel, Field

GOLDEN_DIR = Path(__file__).parent / "golden"


class GoldenSample(BaseModel):
    """One golden sample — minimal schema for L6 skeleton.

    Fields:
        id: stable identifier for regression tracking across runs
        input: user query / prompt
        expected_output: reference answer (ground truth)
        retrieval_context: chunks the model should ground on (for RAG faithfulness)
        context: additional context (optional, e.g. system prompt, session memory)
    """

    id: str = Field(..., description="Stable identifier for regression tracking")
    input: str
    expected_output: str
    retrieval_context: list[str] = Field(default_factory=list)
    context: list[str] = Field(default_factory=list)


def load_golden(filename: str = "sample_golden.jsonl") -> list[GoldenSample]:
    """Load golden samples from JSONL file in eval/golden/.

    Skips blank lines and lines starting with `#`.
    """
    path = GOLDEN_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Golden file not found: {path}")
    samples: list[GoldenSample] = []
    with path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at {path}:{line_num}: {e}") from e
            samples.append(GoldenSample(**data))
    return samples


def to_test_case(sample: GoldenSample) -> LLMTestCase:
    """Convert a GoldenSample into a DeepEval LLMTestCase.

    Note: `actual_output` is set to `expected_output` for the skeleton (Tier 1).
    In Tier 2, the test runner will call the Lab's agent/runtime to produce
    `actual_output`, then metrics evaluate it against `expected_output` + `retrieval_context`.
    """
    return LLMTestCase(
        input=sample.input,
        actual_output=sample.expected_output,  # placeholder — wire to agent runtime in Tier 2
        expected_output=sample.expected_output,
        retrieval_context=sample.retrieval_context or None,
        context=sample.context or None,
    )
