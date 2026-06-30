# `spec.md` — streaming-fraud-mini

> Requirements + design decisions + IP boundary note for the streaming-fraud-mini module. Scaffold stage — no implementation yet.
>
> Bilingual notes (EN + VI) where a design decision needs extra justification. Public repo face stays English.

## 1. Problem statement (EN)

Build a **mini-scale, end-to-end streaming fraud-detection pipeline** that:

1. Ingests synthetic transaction events from a Kafka topic.
2. Computes streaming aggregations (velocity, count, amount-sum) over rolling windows.
3. Looks up features from Redis and scores each event with a GBDT model served via Triton.
4. Fuses rule + ML + policy into a treatment decision (block / challenge / cool-down / manual / allow).
5. Monitors feature/score drift and sliced recall, alerting on recall drop.
6. Runs an eval-gated CI workflow on fraud-specific golden scenarios (reusing root `eval/`).

### 1.1 Tóm tắt (VI)

Xây pipeline **fraud detection mini-scale end-to-end** (Kafka → streaming feature → Redis → Triton → decision → monitor → eval gate) để **giữ intuition về hệ lớn** mà không động tới code/data công ty. Mục đích chính = **learning + interview evidence**, không phải production.

## 2. Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Emit synthetic tx events at ~1k/s to a local Kafka topic | P0 |
| FR-2 | Compute rolling windows: count, amount-sum, distinct-merchant over 1m / 5m / 1h | P0 |
| FR-3 | Store + lookup features in Redis with < 5 ms p95 latency | P0 |
| FR-4 | Train a GBDT (XGBoost/LightGBM) baseline, export ONNX, parity within 1e-4 vs Python | P0 |
| FR-5 | Serve via Triton (REST + gRPC), p95 < 50 ms per score call | P0 |
| FR-6 | Canary 10% traffic to a challenger model; shadow-traffic log diffs | P1 |
| FR-7 | Decision engine maps (rule signals, ML score, policy) → 5 treatments | P0 |
| FR-8 | Drift detection (PSI/KS) on features + score; sliced recall by channel & amount bucket | P0 |
| FR-9 | Recall-drop > tolerance blocks CI (regression via root `eval/`) | P0 |
| FR-10 | `docker-compose up` boots Kafka + Redis + Triton + Flink/Spark + sidecar | P0 |

## 3. Non-functional requirements

- **Latency:** end-to-end (Kafka in → treatment out) p95 < 200 ms on a single laptop.
- **Throughput:** sustain 1k events/s.
- **Reproducibility:** deterministic synthetic data seed; pinned container versions.
- **Observability:** OpenTelemetry traces span producer → window → Redis → Triton → decision.
- **Security:** no real PII, no real card numbers — synthetic only.

## 4. Design decisions

### 4.1 Why Kafka + Flink + Redis + Triton? (B-B-D-T-R sketch)

- **Business:** need a real-time pipeline that mirrors how production fraud systems look — event-driven, low-latency, eval-gated.
- **Bottleneck:** online scoring latency + feature freshness; batch ETL would be stale by minutes.
- **Decision:** Kafka (bus) + Flink (streaming windows) + Redis (hot features) + Triton (model server).
- **Trade-off:** Flink adds operational complexity vs. Spark Structured Streaming — picked Flink for native low-latency windows; Spark is the fallback if Flink ops cost too high.
- **Result (target):** p95 < 200 ms end-to-end, feature freshness < 1 s.
- **Differently:** if rebuilding, would consider **Kafka Streams** (lighter) instead of Flink for mini-scale — but Flink is closer to industry default, better for evidence.

### 4.2 Why GBDT, not deep learning? (VI)

GBDT (XGBoost/LightGBM) là workhorse cho tabular fraud — train nhanh, interpret dễ, footprint nhỏ, serve qua ONNX trên Triton gọn. Deep learning cho fraud phức tạp hơn, lợi ích không rõ ở mini-scale. **Quyết định: GBDT v1, DL để v2 nếu cần.**

### 4.3 Why 5 treatments (not just block/allow)?

Production fraud không nhị phân. `challenge` (OTP/step-up), `cool-down` (delay + review), `manual` (analyst queue) giảm false-positive block — quan trọng cho UX. **5 treatments** cho phép demo policy matrix realistic.

### 4.4 Why reuse root `eval/`?

Repo đã có `eval/` skeleton (DeepEval + golden + regression). Fork sẽ tạo divergence. **Quyết định: mở rộng root `eval/`** với `--suite fraud` mode + `fraud_golden.jsonl`. Giữ CI gate thống nhất.

## 5. IP boundary note (BẮT BUỘC)

- **Module greenfield từ scratch.** Không copy/fork/reuse code, schema, config, model, data từ employer (cũ hoặc hiện tại) hoặc freelance.
- **Không nhắc tên "Golf/ScanIT/Got It/VG Corp"** hay bất kỳ tên công ty nào trong toàn bộ module. Chỉ dùng generic "Fraud/Risk ML day job".
- **Data chỉ synthetic hoặc public dataset** (Kaggle IEEE-CIS, Kaggle Credit Card Fraud) — attribute rõ nguồn.
- **Stack open-source only** — không internal tool công ty.
- **Design pattern (streaming window, canary, shadow, drift alert, eval gate) không có copyright** — implement clean là skill demonstration, không phải IP reuse.
- **Honesty rule:** nếu interviewer hỏi "code này ở đâu ra" → câu thật: *"em build từ scratch, áp dụng pattern industry chuẩn"*, không *"lấy code cũ polish"*.

## 6. Interface contracts (planned, NOT_STARTED)

### 6.1 tx event schema (Avro-ish, synthetic)

```jsonc
{
  "tx_id": "uuid",
  "user_id": "u_#####",
  "card_id": "c_#####",
  "merchant_id": "m_###",
  "channel": "web | mobile | atm | pos",
  "amount": 12.34,
  "currency": "USD",
  "ts_ms": 1719700000000,
  "country": "VN",
  "label": 0  // 1 only in labeled replay mode; 0 in live mode
}
```

### 6.2 feature lookup response (Redis)

```jsonc
{
  "user_id": "u_#####",
  "vel_1m": 3, "vel_5m": 11, "vel_1h": 42,
  "amt_sum_1m": 120.5, "amt_sum_5m": 540.0, "amt_sum_1h": 2100.0,
  "distinct_merchant_1h": 7,
  "as_of_ms": 1719700000123
}
```

### 6.3 score response (Triton / FastAPI sidecar)

```jsonc
{ "tx_id": "...", "score": 0.83, "model": "gbdt-v1", "mode": "primary | canary | shadow" }
```

### 6.4 decision response

```jsonc
{
  "tx_id": "...",
  "treatment": "block | challenge | cooldown | manual | allow",
  "reasons": ["rule:velocity>10", "ml:score>0.8"],
  "policy_version": "2026.06.30"
}
```

## 7. Open questions (resolve during implement)

- [ ] Flink vs Spark Structured Streaming — decide end of W2.
- [ ] Public dataset vs pure synthetic for W3 baseline — try Kaggle IEEE-CIS first; fallback synthetic.
- [ ] Triton vs simpler FastAPI-only serving — keep Triton for evidence value even if overkill at mini-scale.
- [ ] Whether to add LLM scam-classifier in v2 — defer; not in 8-week plan.

## 8. Status

`NOT_STARTED` — spec + scaffold landed. Implementation begins W1.
