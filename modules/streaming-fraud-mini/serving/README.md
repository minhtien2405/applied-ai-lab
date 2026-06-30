# `serving/` — Triton model serving + canary + shadow

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Serve the trained GBDT model (ONNX) via **NVIDIA Triton** with a **FastAPI** sidecar for non-ML decisions. Support **canary** (10% traffic to challenger) and **shadow traffic** (log diffs without affecting users).

## What it does (planned)

- Triton model repository layout for ONNX GBDT (`gbdt-v1`, `gbdt-v2-canary`).
- REST + gRPC endpoints.
- FastAPI sidecar: fetches Redis feature, calls Triton, returns score.
- canary routing: 10% of tx_id hashes → challenger model.
- shadow traffic: every primary call also calls challenger, diff logged (no user impact).
- p95 latency target < 50 ms per score.

## Expected interface (planned)

```
POST /score
{ "tx_id": "...", "user_id": "..." }
→ { "tx_id": "...", "score": 0.83, "model": "gbdt-v1", "mode": "primary" }
```

gRPC mirror for batched scoring.

## Dependencies

- `tritonclient` (HTTP + gRPC).
- `fastapi`, `uvicorn`.
- ONNX model from W3 training.

## IP boundary

- No employer model weights, no employer feature schemas. GBDT trained on public/synthetic data only.
- Triton config (`config.pbtxt`) is open-source convention; no employer-specific dynamic batching params copied.

## Status

`NOT_STARTED` — Triton + canary + shadow land in W4.
