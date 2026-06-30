# `ingest/` — Kafka producer

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Pull synthetic tx events from [`data/`](../data/README.md) and publish to a local Kafka topic `tx-events`. First hop of the pipeline.

## What it does (planned)

- Kafka producer client (single-broker, local docker-compose).
- configurable target topic, acks (`all` for durability in mini-scale).
- schema-validated publish (reject malformed events; log + drop).
- emits OpenTelemetry span per published batch.
- backpressure: bounded in-memory queue; drops + logs on overflow.

## Expected interface (planned)

```python
from streaming_fraud_mini.ingest import KafkaProducer

prod = KafkaProducer(bootstrap="localhost:9092", topic="tx-events")
prod.publish_batch(events)
```

CLI: `python -m streaming_fraud_mini.ingest --rate 1000 --topic tx-events`

## Dependencies

- `confluent-kafka` *or* `aiokafka` (pick in W1).
- local Kafka via `docker-compose` (see root `docker-compose.yml` — extend with kafka + zookeeper).

## IP boundary

- No employer-specific producer config, serializer, or schema registry. Plain JSON or Avro-with-public-schema only.

## Status

`NOT_STARTED` — producer lands in W1.
