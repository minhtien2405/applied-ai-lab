# `eval/golden/` — Golden dataset

> Curated input/expected_output pairs for regression testing.

## Schema (JSONL, one sample per line)

```json
{"id": "q-001", "input": "user query", "expected_output": "reference answer",
 "retrieval_context": ["chunk1", "chunk2"], "context": ["optional system prompt"]}
```

| Field | Required | Description |
|---|---|---|
| `id` | yes | Stable identifier for regression tracking across runs |
| `input` | yes | User query / prompt |
| `expected_output` | yes | Reference answer (ground truth) |
| `retrieval_context` | no (default `[]`) | Chunks the model should ground on (for RAG faithfulness) |
| `context` | no (default `[]`) | Additional context (system prompt, session memory, etc.) |

Lines starting with `#` are treated as comments and skipped. Blank lines are skipped.

## Curation principles

1. **From real traces > synthetic** — as the Lab matures, replace synthetic samples with captures from real usage (especially production failures).
2. **One assertion per concern** — don't overload one sample to test faithfulness + relevancy + tone. Split if needed.
3. **Version filenames, not columns** — `golden-v1.jsonl`, `golden-v2.jsonl` forces explicit PR review when dataset changes.
4. **50–200 samples is the sweet spot** — too few = flaky, too many = slow CI.

## Current state (Q3 2026 Tier 1)

`sample_golden.jsonl` — 10 minimal synthetic samples (generic knowledge Q&A) to demonstrate the harness. Replace with real Lab-domain samples as use-cases land (Q4 2026 MCP agent, etc.).

## Adding a new sample

1. Pick a real failure mode the Lab should catch.
2. Write the `input` (user query) + `expected_output` (reference answer).
3. Add `retrieval_context` if testing RAG faithfulness.
4. Append to `sample_golden.jsonl` (or create `golden-vN.jsonl` if curating new batch).
5. Run `make eval` locally to verify scores.
6. PR — CI gate will run regression check vs baseline.
