# `eval/` — L6 Eval Harness

> DeepEval-based regression gate for the AI Systems Lab.

## Status

**Tier 1 (skeleton)** — Q3 2026 first capability. Folder + module README + smoke test landed. Functional eval run (Tier 2) pending wiring to agent runtime (L2).

## Purpose

Every prompt / model / agent change is a code change → deserves regression testing. This module:

- Loads golden samples (`eval/golden/*.jsonl`)
- Runs DeepEval metrics (faithfulness, answer-relevancy, conciseness + custom G-Eval)
- Compares scores vs baseline (`eval/baseline.json`) — regression guard
- Blocks CI merge when score regresses beyond tolerance

## Layout

```
eval/
├── __init__.py        # public API exports
├── golden.py          # GoldenSample model + JSONL loader
├── metrics.py         # default metric suite factory
├── runner.py          # regression guard (current vs baseline)
├── baseline.json      # regression baseline scores
└── golden/
    ├── README.md      # how to curate golden samples
    └── sample_golden.jsonl  # 10 minimal synthetic samples
```

## Usage

### Smoke test (no LLM call, fast)

```bash
make test-smoke
```

### Full eval (requires LLM endpoint for judge)

```bash
export OPENAI_API_KEY=...
make eval
```

### Update baseline after a confirmed good run

```python
from eval.runner import save_baseline
save_baseline({"faithfulness": 0.82, "answer_relevancy": 0.88, "conciseness": 0.79})
```

## Principles

1. **Golden from real traces** — start synthetic, grow from production failures
2. **Binary pass/fail via threshold** — no vague Likert scales
3. **Delta-vs-baseline** — not static threshold (chống LLM judge flakiness)
4. **Generator != judge** — different model family for judge (set `DEEPEVAL_MODEL`)
5. **CI gate blocking merge** — `.github/workflows/eval-gate.yml`
6. **Per-line prompt ablation** (future) — Anthropic April 23 incident lesson

## Greenfield

This module is fresh code using only the open-source DeepEval framework. No code reused from any employer or freelance project. Design patterns (golden + judge + regression) are not copyrightable.

## Next steps (Tier 2)

- [ ] Wire `actual_output` to L2 Agent Runtime (currently set to `expected_output` placeholder)
- [ ] Add agent trajectory metrics (tool order, cost, memory) when L2 lands
- [ ] Grow golden to 50+ samples from real Lab usage
- [ ] Add per-line system-prompt ablation script (Anthropic April 23 lesson)
- [ ] Add DeepEval MCP Task Completion metric (for Q4 2026 L5 MCP module)
