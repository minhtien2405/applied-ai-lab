# `features/` — streaming aggregation → Redis feature store

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Consume `tx-events` from Kafka, compute **rolling-window aggregations**, and write features to Redis for sub-ms online lookup by the scoring service.

## What it does (planned)

- Streaming job (Flink *or* Spark Structured Streaming — decide end of W2).
- Windows: 1 minute, 5 minutes, 1 hour.
- Aggregations per `user_id` (and optionally per `card_id`):
  - **velocity** = count of tx in window.
  - **amount-sum** = sum of amount in window.
  - **distinct-merchant** = cardinality of merchant_id in window.
- Output written to Redis as hash keys with TTL = window-length + grace.
- Idempotent: replays produce same feature state.

## Expected interface (planned)

```python
from streaming_fraud_mini.features import FeatureJob

job = FeatureJob(bootstrap="localhost:9092", redis="localhost:6379")
job.run()  # blocking streaming job
```

Redis key layout (planned): `feat:user:<uid>:1m` → hash `{vel, amt_sum, distinct_merch, as_of_ms}`.

## Dependencies

- `pyflink` *or* `pyspark` (decide in W2).
- `redis-py` (async).
- local Redis via `docker-compose`.

## IP boundary

- Window choices (1m/5m/1h) are industry-standard. No employer-specific feature definitions.
- No proprietary feature store framework (e.g. no Feast internal forks) — plain Redis.

## Status

`NOT_STARTED` — streaming job lands in W2.
