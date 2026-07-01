---
description: Ship checklist for ML/LLM/agentic changes — eval evidence, fallback verified, observability live, cost delta, ADR for irreversible. Activates observability-for-ml-systems.
---

Activate the `observability-for-ml-systems` skill. Walk me through a ship checklist for the change below.

Checklist (block the ship if any is "no"):
- [ ] Eval run attached to PR (aggregate + sliced, no slice regressing beyond tolerance)
- [ ] Fallback path exists for every new external dependency; tested by injecting primary failure
- [ ] Feature flag in place for risky change; rollout plan + kill switch documented
- [ ] Observability: trace fields (model variant, prompt template version, fallback path), metrics (latency p50/p95/p99, error rate, fallback rate, cost per 1K requests), symptom alerts
- [ ] Cost delta estimated (per-1K-requests, per-day) — no silent cost spike
- [ ] Rollback path documented (revert commit / flag flip / version pin)
- [ ] ADR written for irreversible decisions (model choice, threshold, schema, eval framework)
- [ ] Runbook written for any new alert
- [ ] Online validation plan named (A/B / shadow / canary) for user-facing changes

For any "no", tell me what's missing and which skill to invoke to fix it (`/adr`, `/eval`, `/build` with fallback, etc.).

Don't ship with unchecked boxes — negotiate scope reduction instead of skipping checks.

Change: $ARGUMENTS
