# `decision/` — rule + ML + policy → treatment

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Fuse **rule signals**, **ML score**, and **policy** into one of 5 treatments: `block`, `challenge`, `cool-down`, `manual`, `allow`. This is where the system decides what actually happens to a tx.

## What it does (planned)

- Rule engine: simple predicates on features + raw event (e.g. `vel_1m > 10`, `amount > 5000 & country != home_country`).
- ML gate: score thresholds with hysteresis (avoid flapping near boundary).
- Policy matrix: combines rule signals + ML bucket → treatment. Policy is versioned (`policy_version`), loaded from YAML.
- audit log: every decision logs `{tx_id, signals, score, treatment, policy_version, ts}`.
- analyst queue: `manual` treatment enqueues for review (in-memory queue in v1).

## Treatments (5)

| Treatment | Meaning |
|---|---|
| `block` | reject tx, notify user |
| `challenge` | step-up auth (OTP / device verify) |
| `cooldown` | delay + review before allow |
| `manual` | analyst queue |
| `allow` | proceed |

## Expected interface (planned)

```python
from streaming_fraud_mini.decision import DecisionEngine

eng = DecisionEngine(policy_path="policy/v1.yaml")
treatment = eng.decide(event, features, score)
```

## Dependencies

- `pydantic` (signal + decision schema).
- `pyyaml` (policy load).
- no external rule engine framework — keep dependency surface small.

## IP boundary

- Policy rules are generic fraud-industry knowledge (velocity = signal, high-amount + new-country = signal). No employer-specific rule lists, thresholds, or policy versions copied.

## Status

`NOT_STARTED` — decision engine lands in W5.
