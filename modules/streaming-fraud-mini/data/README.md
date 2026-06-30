# `data/` — synthetic tx event generator

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Generate **synthetic** transaction events that mimic the shape of real payment-fraud streams — without touching any real data. Used by [`ingest/`](../ingest/README.md) to feed Kafka.

## What it does (planned)

- Deterministic, seeded generator producing tx events per the schema in [`spec.md` §6.1](../spec.md).
- configurable rate (default ~1k events/s), configurable fraud-rate (default ~2%).
- injects behavioural patterns for 3 fraud archetypes:
  - **scam** — sudden high-amount spike on a long-dormant user.
  - **ATO** (account takeover) — velocity burst + new device/country.
  - **payment fraud** — rapid distinct-merchant hits in a short window.
- emits both **live mode** (label=0, score real-time) and **replay mode** (label included, for offline eval).

## Expected interface (planned)

```python
from streaming_fraud_mini.data import TxEventGenerator

gen = TxEventGenerator(seed=42, rate_per_s=1000, fraud_rate=0.02)
for event in gen.stream():
    ...
```

CLI: `python -m streaming_fraud_mini.data --rate 1000 --fraud-rate 0.02 --out kafka | file`

## Dependencies

- `pydantic` (event schema validation) — already in repo `pyproject.toml`.
- no external dataset required for v1 (synthetic only).

## IP boundary

- Synthetic only. No real PII, no real card numbers, no real merchant IDs.
- Patterns are generic industry knowledge (velocity = fraud signal), not employer-specific.

## Status

`NOT_STARTED` — generator lands in W1.
