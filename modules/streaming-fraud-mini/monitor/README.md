# `monitor/` — drift detection + sliced eval + recall-drop alert

> Spec only. No implementation yet. Status: `NOT_STARTED`.

## Purpose

Continuous monitoring of **feature drift**, **score drift**, and **sliced recall** — so the team catches model degradation before users do. This is the "Grafana for fraud" mini version.

## What it does (planned)

- **Drift detection:** PSI (Population Stability Index) + KS test on key features (`vel_1m`, `amt_sum_5m`) and on the score distribution. Compares last 1 h vs. baseline.
- **Sliced eval:** recall + precision per slice — by `channel` (web/mobile/atm/pos), by amount bucket (< 10, 10–100, 100–1000, > 100), by country.
- **Recall-drop alert:** if recall on any slice drops > tolerance vs. baseline → fire alert (log + optional webhook). Triggers eval-gate regression block in CI.
- **Audit log consumption:** reads `decision/` audit log to compute observed treatments + (in replay mode) outcomes.

## Expected interface (planned)

```python
from streaming_fraud_mini.monitor import DriftMonitor, SlicedEval

DriftMonitor(features_stream, baseline).run()  # emits alerts
SlicedEval(decisions, labels).report()  # returns sliced recall/precision table
```

CLI: `python -m streaming_fraud_mini.monitor --window 1h --alert-on recall_drop`

## Dependencies

- `numpy`, `scipy` (KS test, PSI).
- `opentelemetry-sdk` (metrics + traces).
- optional: Grafana + Loki via `docker-compose` (visual dashboard).

## IP boundary

- PSI, KS, sliced-recall are industry-standard monitoring primitives. No employer-specific alert thresholds or dashboard JSONs copied.

## Status

`NOT_STARTED` — monitor lands in W6.
