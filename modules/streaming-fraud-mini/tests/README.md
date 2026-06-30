# `tests/` — test plan

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Test plan for `streaming-fraud-mini`. Implementation lands alongside each weekly deliverable.

## Test layers

| Layer | What | Where | Marker |
|---|---|---|---|
| **Unit** | pure functions: feature computation, policy matrix, drift math, schema validation | `tests/test_*.py` under module | `pytest` default |
| **Integration** | Kafka → Flink → Redis → Triton → decision on local docker-compose | `tests/test_integration_*.py` | `@pytest.mark.integration` |
| **Smoke** | fast, no services, no LLM — validates plumbing + config | `tests/test_smoke_*.py` | `@pytest.mark.smoke` |
| **Eval** | fraud golden regression vs. baseline | root `tests/test_eval_*` extended | `@pytest.mark.eval` |

## Planned test files (NOT_STARTED)

- `test_data_generator.py` — deterministic seed, fraud-rate honoured, schema valid.
- `test_ingest_producer.py` — publish/consume round-trip on local Kafka.
- `test_features_window.py` — window correctness, idempotent replay, Redis TTL.
- `test_serving_triton.py` — score endpoint responds, ONNX parity, canary routing %, shadow diff logged.
- `test_decision_policy.py` — 5 treatments wired, policy version respected, audit log written.
- `test_monitor_drift.py` — PSI/KS on injected drift, recall-drop alert fires.
- `test_integration_e2e.py` — `docker-compose up` → emit 1k events → treatments observed.
- `test_smoke_pipeline.py` — config + import sanity, no services required.

## CI integration

- Smoke tests run on every PR (fast, no services).
- Integration + eval run on `docker-compose`-available runner (planned W7–W8).
- Root `.github/workflows/eval-gate.yml` extended with fraud suite (planned).

## Dependencies

- `pytest`, `pytest-asyncio`, `pytest-cov` — already in repo `pyproject.toml`.
- `testcontainers` (planned) — for Kafka/Redis integration without manual docker.

## IP boundary

- All test fixtures synthetic. No employer data, no employer test cases copied.

## Status

`NOT_STARTED` — tests land incrementally week by week alongside each deliverable.
