# `eval/` — eval gate integration + fraud golden plan

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

This sub-folder **does NOT fork** the root `eval/` harness. It documents how `streaming-fraud-mini` **plugs into** the root `eval/` (runner, metrics, golden, baseline) and adds fraud-specific scenarios.

## Plan

- Reuse root `eval/runner.py` — extend with `--suite fraud` mode (planned, NOT_STARTED).
- Reuse root `eval/metrics.py` — add fraud metrics: precision, recall, F1 per slice, PSI drift, alert latency (planned).
- Reuse root `eval/golden/` — add `fraud_golden.jsonl` (planned).
- Reuse root `eval/baseline.json` — add a `fraud` block (planned).

## Fraud golden scenario taxonomy (planned)

Three fraud archetypes, each with positive + negative samples:

| Archetype | Positive example | Negative example |
|---|---|---|
| **scam** | sudden high-amount spike on dormant user | loyal user occasional high-amount purchase |
| **ATO** | velocity burst + new country | traveling user with notify-on |
| **payment fraud** | rapid distinct-merchant hits | power-user normal daily spending |

Target: 30+ golden samples (10 per archetype), balanced positives/negatives.

## CI gate behaviour (planned)

- `make eval-smoke` (no LLM, fast) — runs structural checks on fraud golden.
- `make eval-fraud` (planned) — runs full fraud regression vs. `baseline.json`.
- recall drop > tolerance on any slice → **CI blocks merge** (same mechanism as root eval-gate).

## Dependencies

- root `eval/` package — already in repo.

## IP boundary

- Golden scenarios are synthetic, constructed from generic fraud-industry patterns. No employer real-prod traces.

## Status

`NOT_STARTED` — eval integration lands in W7.
