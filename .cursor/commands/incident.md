---
description: Respond to a production ML incident — mitigate-first, then RCA, then permanent fix (S-A-R-L). Activates ml-incident-response.
---

Activate the `ml-incident-response` skill. We have an active production ML incident. Walk me through it in the strict order below — do NOT skip mitigation to debug.

1. **Declare** — state what's broken, since when, who's affected, severity (SEV1/2/3). Name IC / comms / ops leads (can be one person, but say so). Open an incident channel. Start a timeline doc.
2. **Capture initial state** — before mitigating: error rate, latency, fallback rate, drift signals, recent deploys (24h), recent config changes. Save a sample of failing inputs (PII-redacted).
3. **Mitigate-first** — pick the cheapest restore: rollback / flag flip / increase fallback aggressiveness / disable feature / throttle. Verify user-visible metrics recovering.
4. **Communicate** — internal (incident channel + stakeholders, cadence by severity) + external (status page if user-facing SEV1, within 30 min). Format: what's broken, what we're doing, what users should expect, next update time.
5. **RCA** — only after mitigation. Use `debugging-ml-failures`: reproduce, localize, reduce, classify flakiness-vs-regression.
6. **Permanent fix** — fix root cause (not symptom); add golden case; tighten alert; run eval.
7. **Post-mortem** — within 5 business days. S-A-R-L. Blameless. Action items with owners + due dates.

If I'm tempted to debug before mitigating, push back: "mitigate first, debug second — users are affected".

Incident: $ARGUMENTS
